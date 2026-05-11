"""
1688 → 店小秘 采集流水线
用法：python pipeline.py
"""

import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib.parse
import html
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import xlwt

# ── 配置 ──────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, 'apify_config.json')

try:
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        CONFIG = json.load(f)
except FileNotFoundError:
    CONFIG = {}

API_TOKEN        = CONFIG.get('apify_token', '')
SEARCH_ACTOR     = CONFIG.get('search_actor_id', '').replace('/', '~')
DETAIL_ACTOR     = CONFIG.get('detail_actor_id', '').replace('/', '~')
# 上货固定值
PRICE_PLUS  = 190   # 申报价格 = 采购价 + PRICE_PLUS (CNY)
PKG_LENGTH  = 15    # 包装尺寸 cm
PKG_WIDTH   = 10
PKG_HEIGHT  = 2
WEIGHT_G    = 350   # 固定克重 g（女士牛仔短裤）
RETAIL_USD  = 60    # 建议零售价 USD
BATCH_SIZE       = int(CONFIG.get('detail_batch_size', 10))

FEISHU_APP_ID          = CONFIG.get('feishu_app_id', '')
FEISHU_APP_SECRET      = CONFIG.get('feishu_app_secret', '')
FEISHU_WIKI_TOKEN      = CONFIG.get('feishu_wiki_token', '')
FEISHU_PREVIEW_TABLE   = CONFIG.get('feishu_preview_table_id', '')   # 上传预览表（审核勾选用）
FEISHU_GOODS_TABLE     = CONFIG.get('feishu_goods_table_id', '')     # 货品表
FEISHU_MIAOSHOU_TABLE  = CONFIG.get('feishu_miaoshou_table_id', '') # 店小秘格式表

# 产品编号格式：PREFIX-N（按前缀自增）
CATEGORY_PREFIX = CONFIG.get('category_prefix', 'NSNZDK')

# ── 万邦(Onebound) API ────────────────────────────────────────────────────────
ONEBOUND_BASE   = 'https://api-gw.onebound.cn'
ONEBOUND_KEY    = CONFIG.get('onebound_key', '')
ONEBOUND_SECRET = CONFIG.get('onebound_secret', '')

DATA_DIR            = os.path.abspath(os.getenv('RPA_DATA_DIR') or os.getenv('UPLOAD_ASSISTANT_DATA_DIR') or os.path.join(BASE_DIR, 'data'))
IMAGES_DIR          = os.path.join(DATA_DIR, 'images')
COLLECTED_PATH      = os.path.join(DATA_DIR, 'collected_ids.json')
PROD_NO_COUNTER_PATH = os.path.join(DATA_DIR, 'prod_no_counter.json')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

# ── Apify 工具函数 ─────────────────────────────────────────────────────────────

def _apify_post(path, payload):
    url = f"https://api.apify.com/v2/{path}?token={API_TOKEN}"
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data,
                                  headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        print(f"  API错误 {e.code}: {body[:500]}")
        raise

def _apify_get(path):
    url = f"https://api.apify.com/v2/{path}?token={API_TOKEN}"
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))

def _wait_for_run(run_id, label=''):
    while True:
        status = _apify_get(f"actor-runs/{run_id}")['data']['status']
        print(f"  [{label}] 状态: {status}")
        if status in ('SUCCEEDED', 'FAILED', 'ABORTED', 'TIMED-OUT'):
            return status
        time.sleep(15)

def _get_dataset(dataset_id):
    url = (f"https://api.apify.com/v2/datasets/{dataset_id}/items"
           f"?token={API_TOKEN}&limit=9999")
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read().decode('utf-8'))

def _fix_enc(obj):
    """修复 ecomscrape 返回的 surrogate-escaped 编码问题（latin1→utf-8）"""
    if isinstance(obj, str):
        try:
            return obj.encode('latin1').decode('utf-8')
        except Exception:
            return obj
    elif isinstance(obj, dict):
        return {k: _fix_enc(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_fix_enc(v) for v in obj]
    return obj

# ── 万邦 API 详情获取 ─────────────────────────────────────────────────────────

def _onebound_item_get(offer_id):
    """调万邦 API 获取1688商品详情，返回原始 item dict；失败返回 None。"""
    url = (f"{ONEBOUND_BASE}/1688/item_get/"
           f"?key={ONEBOUND_KEY}&secret={ONEBOUND_SECRET}"
           f"&num_iid={offer_id}&lang=zh-CN")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode('utf-8'))
        err = data.get('error', '')
        if err and err != '0':
            print(f"  [onebound] {offer_id} 失败: {err} — {data.get('reason', '')}")
            return None
        return data.get('item')
    except Exception as e:
        print(f"  [onebound] {offer_id} 请求异常: {e}")
        return None


def _parse_onebound_item(offer_id, item):
    """
    把万邦 item dict 转成 pipeline 内部格式：
    {id, url, title, image_url, images, attributes,
     wholesale_skus: {sku_props, sku_info_map_original}}
    """
    title   = item.get('title', '')
    pic_url = item.get('pic_url', '')
    images  = item.get('images') or []
    if isinstance(images, str):
        images = [images]
    if pic_url and pic_url not in images:
        images = [pic_url] + list(images)
    images = list(images)

    raw_skus  = (item.get('skus') or {}).get('sku') or []
    props_img = item.get('props_img') or {}

    # 重建 sku_props 和 sku_info_map
    prop_map     = {}   # fid -> {prop: str, values: {vid -> {name, imageUrl?}}}
    sku_info_map = {}

    for sku in raw_skus:
        props_name = sku.get('properties_name', '') or ''
        price      = str(sku.get('price') or sku.get('total_price') or '0')
        quantity   = str(sku.get('quantity') or '0')
        sku_id     = str(sku.get('sku_id') or '')
        spec_id    = str(sku.get('spec_id') or '')

        # properties_name 格式："fid1:vid1:pname1:vname1;fid2:vid2:pname2:vname2"
        parts      = [p for p in props_name.split(';') if p.strip()]
        key_vals   = []

        for part in parts:
            segs = part.split(':')
            if len(segs) < 4:
                continue
            fid, vid, pname, vname = segs[0], segs[1], segs[2], segs[3]

            if fid not in prop_map:
                prop_map[fid] = {'prop': pname, 'values': {}}

            if vid not in prop_map[fid]['values']:
                entry = {'name': vname}
                img_url = props_img.get(f"{fid}:{vid}", '')
                if img_url:
                    entry['image_url'] = img_url   # snake_case: _extract_color_entries 读此字段
                prop_map[fid]['values'][vid] = entry

            key_vals.append((pname, vname))

        # sku_info_map key：颜色>尺码（与旧格式对齐）
        color = next((v for p, v in key_vals if p in ('颜色', '颜色分类')), '')
        size  = next((v for p, v in key_vals if p == '尺码'), '')
        if color and size:
            map_key = f"{color}>{size}"
        elif color:
            map_key = color
        elif key_vals:
            map_key = '>'.join(v for _, v in key_vals)
        else:
            map_key = sku_id

        sku_info_map[map_key] = {
            'discountPrice': price,
            'price':         price,
            'canBookCount':  quantity,
            'skuId':         sku_id,
            'specId':        spec_id,
            'specAttrs':     map_key,
            'spec_attrs':    map_key,   # snake_case alias for _lookup_price
            'promotionSku':  'false',
            'saleCount':     '0',
        }

    # 颜色(3216)排前、尺码(450)排后
    _ORDER = {'3216': 0, '450': 1}
    sku_props = [
        {'fid': fid, 'prop': d['prop'], 'value': list(d['values'].values())}
        for fid, d in sorted(prop_map.items(), key=lambda x: _ORDER.get(x[0], 99))
    ]

    # 顶层价格兜底（取所有 SKU 最低价；若无 SKU 则用 item.price）
    sku_prices = [float(s.get('price', 0)) for s in sku_info_map.values() if s.get('price')]
    price_min  = min((p for p in sku_prices if p > 0), default=0.0)
    if price_min == 0.0:
        try:
            price_min = float(item.get('price', 0) or 0)
        except Exception:
            price_min = 0.0

    return {
        'id':          str(offer_id),
        'url':         f'https://detail.1688.com/offer/{offer_id}.html',
        'title':       title,
        'image_url':   images[0] if images else '',
        'images':      images[:8],
        'attributes':  [],
        'price_min':   price_min,   # 兜底价格（供 _get_base_price 读取）
        'wholesale_skus': {
            'sku_props':            sku_props,
            'sku_info_map_original': sku_info_map,
        },
    }


# ── 去重历史 ──────────────────────────────────────────────────────────────────

# ── 产品主编号生成 ────────────────────────────────────────────────────────────

def _next_product_no(prefix=None):
    """生成下一个产品主编号：PREFIX-N（按前缀自增，持久化到文件）"""
    if prefix is None:
        prefix = CATEGORY_PREFIX
    counter = {}
    if os.path.exists(PROD_NO_COUNTER_PATH):
        with open(PROD_NO_COUNTER_PATH, 'r', encoding='utf-8') as f:
            counter = json.load(f)
    n = counter.get(prefix, 0) + 1
    counter[prefix] = n
    with open(PROD_NO_COUNTER_PATH, 'w', encoding='utf-8') as f:
        json.dump(counter, f)
    return f'{prefix}-{n}'


def assign_product_numbers(offer_ids, prefix=None):
    """为一批商品依次分配产品主编号，返回 {offer_id: prod_no}"""
    return {oid: _next_product_no(prefix) for oid in offer_ids if oid}


def load_collected():
    """加载历史已采集的 offer_id 集合"""
    if not os.path.exists(COLLECTED_PATH):
        return {}
    with open(COLLECTED_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def mark_collected(offer_ids, offers_info):
    """将本次成功采集的 offer_id 写入历史记录"""
    history = load_collected()
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for oid in offer_ids:
        if oid not in history:
            item = offers_info.get(oid, {})
            title = item.get('title', '')
            try:
                title = title.encode('latin1').decode('utf-8')
            except Exception:
                pass
            history[oid] = {'collected_at': ts, 'title': title[:60]}
    with open(COLLECTED_PATH, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    print(f"  已记录 {len(offer_ids)} 条到采集历史（历史总计 {len(history)} 条）")

# ── 第一阶段：关键词搜索，拿 offer_id 列表 ──────────────────────────────────────

def stage1_search(keywords, max_per_keyword=50):
    print("\n=== 第一阶段：关键词搜索 ===")
    all_offers = {}   # offer_id -> search result item

    for kw in keywords:
        actual_max = min(max_per_keyword, 1000)
        if max_per_keyword > 1000:
            print(f"  搜索关键词: {kw}（每词最多1000条，已自动截断）")
        else:
            print(f"  搜索关键词: {kw}")
        resp = _apify_post(f"acts/{SEARCH_ACTOR}/runs", {
            "queries": [kw],
            "maxProducts": actual_max,  # API 上限1000
            "sortBy": "va_rmdarkgmv30",
            "proxy": {"useApifyProxy": True, "apifyProxyGroups": ["RESIDENTIAL"]}
        })
        run_id    = resp['data']['id']
        dataset_id = resp['data']['defaultDatasetId']
        status    = _wait_for_run(run_id, kw)

        if status != 'SUCCEEDED':
            print(f"  警告：{kw} 搜索失败，跳过")
            continue

        items = _get_dataset(dataset_id)
        for item in items:
            oid = str(item.get('offer_id', ''))
            if oid and oid not in all_offers:
                all_offers[oid] = item

        print(f"  获得 {len(items)} 条，累计去重 {len(all_offers)} 条")

    # 保存搜索结果供后续测试脚本使用
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    search_path = os.path.join(DATA_DIR, f'search_raw_{ts}.json')
    with open(search_path, 'w', encoding='utf-8') as f:
        json.dump(all_offers, f, ensure_ascii=False, indent=2)
    print(f"  搜索结果已保存: {search_path}")

    return list(all_offers.keys()), all_offers

# ── 预览与筛选 ────────────────────────────────────────────────────────────────

def _get_search_price(item):
    """从 devcake 搜索结果提取参考价格，格式如 '35 ($4.90)'"""
    try:
        raw = item.get('price', '') or ''
        if raw:
            return float(raw.split()[0])
    except Exception:
        pass
    return 0.0

def preview_and_select(offer_ids, offers_info):
    """打印搜索结果预览，让用户选择要抓详情的商品"""
    print(f"\n=== 搜索结果预览（共 {len(offer_ids)} 条）===")
    print(f"{'序号':>4}  {'参考价':>7}  标题 / 链接")
    print("-" * 80)
    for idx, oid in enumerate(offer_ids, 1):
        item  = offers_info.get(oid, {})
        title = item.get('title', '(无标题)')
        try:
            title = title.encode('latin1').decode('utf-8')
        except Exception:
            pass
        price = _get_search_price(item)
        price_str = f"¥{price:.2f}" if price else "  未知"
        url = f"https://detail.1688.com/offer/{oid}.html"
        print(f"{idx:>4}  {price_str:>7}  {title[:40]}")
        print(f"            {url}")
    print("-" * 80)

    while True:
        sel = input(
            "\n请选择要采集详情的商品序号\n"
            "（格式示例：1,3,5-10 / 全选输入 all / 退出输入 q）: "
        ).strip().lower()

        if sel == 'q':
            return []
        if sel == 'all':
            return offer_ids[:]

        selected = []
        valid = True
        for part in sel.split(','):
            part = part.strip()
            if '-' in part:
                try:
                    a, b = part.split('-', 1)
                    for n in range(int(a), int(b) + 1):
                        if 1 <= n <= len(offer_ids):
                            oid = offer_ids[n - 1]
                            if oid not in selected:
                                selected.append(oid)
                        else:
                            print(f"  序号 {n} 超出范围，忽略")
                except ValueError:
                    print(f"  无法解析 '{part}'，请重新输入")
                    valid = False
                    break
            elif part.isdigit():
                n = int(part)
                if 1 <= n <= len(offer_ids):
                    oid = offer_ids[n - 1]
                    if oid not in selected:
                        selected.append(oid)
                else:
                    print(f"  序号 {n} 超出范围，忽略")
            else:
                print(f"  无法解析 '{part}'，请重新输入")
                valid = False
                break

        if valid and selected:
            print(f"  已选 {len(selected)} 条商品")
            return selected
        elif valid and not selected:
            print("  未选择任何商品，请重新输入")

# ── 第二阶段：批量抓详情页 ────────────────────────────────────────────────────

def stage2_details(offer_ids, total_limit):
    print(f"\n=== 第二阶段：抓取详情页（万邦 API，共 {len(offer_ids)} 条，限制 {total_limit} 条）===")
    offer_ids = [str(oid).strip() for oid in offer_ids if str(oid).strip()][:total_limit]

    if not ONEBOUND_KEY or not ONEBOUND_SECRET:
        print("  [错误] apify_config.json 中缺少 onebound_key / onebound_secret")
        return []

    details_by_offer = {}
    fail_ids         = []

    for i, oid in enumerate(offer_ids, 1):
        print(f"  [{i}/{len(offer_ids)}] {oid} ...", end='', flush=True)
        item = _onebound_item_get(oid)
        if item:
            parsed = _parse_onebound_item(oid, item)
            details_by_offer[oid] = parsed
            print(f" OK  {parsed['title'][:25]}" if parsed['title'] else " OK  (无标题)")
        else:
            fail_ids.append(oid)
            print(" FAIL")
        # 控速：~1 req/s，避免触发万邦限速
        if i < len(offer_ids):
            time.sleep(1.0)

    all_details   = [details_by_offer[oid] for oid in offer_ids if oid in details_by_offer]
    missing_final = [oid for oid in offer_ids if oid not in details_by_offer]

    if missing_final:
        print(f"\n[warn] 详情最终仍缺失 {len(missing_final)} 条: {', '.join(missing_final[:10])}")
    print(f"\n详情抓取完成：请求 {len(offer_ids)} 条，成功 {len(all_details)} 条，失败 {len(fail_ids)} 条")

    ts       = datetime.now().strftime('%Y%m%d_%H%M%S')
    raw_path = os.path.join(DATA_DIR, f'details_raw_{ts}.json')
    with open(raw_path, 'w', encoding='utf-8') as f:
        json.dump(all_details, f, ensure_ascii=False, indent=2)
    print(f"原始详情数据已保存: {raw_path}（{len(all_details)} 条）")
    return all_details


# ── [已废弃，保留备用] Apify playwright-scraper 详情抓取 ──────────────────────
def _stage2_apify_legacy(offer_ids, total_limit):
    """原 Apify playwright-scraper 方式（1688 反爬后已停用，仅作备用）"""
    offer_ids = [str(oid).strip() for oid in offer_ids if str(oid).strip()][:total_limit]

    PAGE_FN = r"""async function pageFunction(context) {
        const { page, request } = context;
        try {
            // 拦截 SKU API（reload 前注册，捕获刷新时的请求）
            let skuApiText = null;
            page.on('response', async (res) => {
                try {
                    const u = res.url();
                    if (u.includes('queryofferskuselectormodel') ||
                        u.includes('getSkuSelector') ||
                        u.includes('skuModel')) {
                        skuApiText = await res.text();
                    }
                } catch(e) {}
            });

            // 禁用 HTTP 缓存（CDP），确保 SKU API 重新触发
            try {
                const cdp = await page.context().newCDPSession(page);
                await cdp.send('Network.enable');
                await cdp.send('Network.setCacheDisabled', { cacheDisabled: true });
            } catch(e) {}

            // 重新导航（不是 reload）—— 完全干净的请求，清除 JS 状态
            try {
                await page.goto(request.url, { waitUntil: 'domcontentloaded', timeout: 60000 });
            } catch(e) {
                // goto 失败时退回 reload
                try { await page.reload({ waitUntil: 'domcontentloaded', timeout: 30000 }); } catch(e2) {}
            }
            // 等 load 完成，让客户端跳转结束，再做 evaluate
            try { await page.waitForLoadState('load', { timeout: 15000 }); } catch(e) {}
            // 等 networkidle，让懒加载 API 完成
            try { await page.waitForLoadState('networkidle', { timeout: 10000 }); } catch(e) {}
            await page.waitForTimeout(2000);

            const offerIdM = request.url.match(/\/offer\/(\d+)\.html/);
            const offerId = offerIdM ? offerIdM[1] : '';

            // 从 script 标签提取 window.context JSON（带重试，防止 context destroyed）
            let ctxData = null;
            for (let _try = 0; _try < 3; _try++) {
                try {
                    ctxData = await page.evaluate(() => {
                        for (const s of document.querySelectorAll('script')) {
                            const t = s.textContent || '';
                            if (!t.includes('offerImgList') && !t.includes('gallery')) continue;
                            const m = t.match(/window\.contextPath\s*,\s*(\{[\s\S]+\})\s*\)\s*;/);
                            if (m) { try { return JSON.parse(m[1]); } catch(e) {} }
                        }
                        return null;
                    });
                    break;
                } catch(e) {
                    if (_try < 2) await page.waitForTimeout(2000);
                }
            }

            let title = '', images = [];
            let skuProps = [], skuInfoMap = {};
            let _dbgCtxDataKeys = null;

            if (ctxData) {
                const d = (ctxData.result || {}).data || {};
                const gf = (d.gallery || {}).fields || {};
                title = gf.subject || '';
                images = (gf.offerImgList || []).filter(u => u);

                // 记录 data 顶层 key，方便调试 SKU 路径
                _dbgCtxDataKeys = Object.keys(d);

                // 尝试多路径提取 SKU
                const product = (d.product || {}).fields || d.product || {};
                const candidates = [
                    d.skuSelection, d.skuPreview, d.skuModel, d.skuSelector, d.sku,
                    (d.skuSelection || {}).fields, (d.skuPreview || {}).fields,
                    product, product.skuModel, product.skuSelector
                ];
                for (const c of candidates) {
                    if (!c) continue;
                    const sp = c.skuProps || c.skuPropList || c.skuPropsList
                               || ((c.skuSelectorModel || {}).skuPropsList)
                               || ((c.skuSelectorModel || {}).skuProps) || [];
                    if (sp.length) {
                        skuProps = sp;
                        skuInfoMap = c.skuInfoMap || c.skuMap || c.priceMap || {};
                        break;
                    }
                }

                // 调试：保存各候选 key
                try {
                    const productKeys = Object.keys((d.product || {}).fields || d.product || {});
                    _dbgCtxDataKeys = {
                        dataKeys: Object.keys(d),
                        skuSelKeys: Object.keys((d.skuSelection || {}).fields || d.skuSelection || {}),
                        skuPreviewKeys: Object.keys((d.skuPreview || {}).fields || d.skuPreview || {}),
                        productKeys: productKeys
                    };
                } catch(e) {}
            }

            // fallback1：从截获的 API 响应解析 SKU（JSONP 格式）
            if (skuProps.length === 0 && skuApiText) {
                try {
                    const m2 = skuApiText.match(/^[^(]+\(([\s\S]*)\)\s*$/);
                    if (m2) {
                        const aj = JSON.parse(m2[1]);
                        const sm2 = ((aj.data || {}).skuSelectorBizModel || {});
                        skuProps = (sm2.skuSelectorModel || {}).skuPropsList || sm2.skuProps || [];
                        skuInfoMap = sm2.skuInfoMap || {};
                    }
                } catch(e) {}
            }

            // fallback2：从 DOM 直接提取颜色（1688 页面渲染的 SKU 选择器）
            if (skuProps.length === 0) {
                for (let _try = 0; _try < 2; _try++) {
                try {
                    skuProps = await page.evaluate(() => {
                        // 找颜色标签组
                        const colorGroups = [];
                        // 匹配 class 含 sku-prop 或 color 的容器
                        const containers = document.querySelectorAll(
                            '[class*="sku-prop"], [class*="skuProp"], [class*="color-prop"],' +
                            '[data-prop-name="颜色"], [data-prop-name="Color"]'
                        );
                        for (const ctr of containers) {
                            const propName = ctr.getAttribute('data-prop-name') || '颜色';
                            const items = ctr.querySelectorAll(
                                '[class*="sku-item"], [class*="skuItem"], [class*="prop-item"], li, button'
                            );
                            if (!items.length) continue;
                            const values = [];
                            for (const it of items) {
                                const name = (it.getAttribute('title') || it.textContent || '').trim();
                                const img = it.querySelector('img');
                                const imageUrl = img ? (img.src || img.getAttribute('data-src') || '') : '';
                                if (name) values.push({ name, image_url: imageUrl });
                            }
                            if (values.length) colorGroups.push({ prop: propName, value: values });
                        }
                        return colorGroups;
                    });
                    break;
                } catch(e) {
                    if (_try < 1) await page.waitForTimeout(2000);
                }
                } // end for _try
            }

            // fallback3：ctxData 没有图片时，从 OG / 页面 img 标签提取
            if (images.length === 0) {
                for (let _try = 0; _try < 2; _try++) {
                    try {
                        images = await page.evaluate(() => {
                            // OG image
                            const og = document.querySelector('meta[property="og:image"]');
                            const ogUrl = og ? og.getAttribute('content') : '';
                            // 主图区 img
                            const imgs = Array.from(document.querySelectorAll(
                                '.detail-gallery img, .offer-photo img, .gallery-item img, .swiper-slide img'
                            ))
                            .map(i => (i.src || i.getAttribute('data-src') || '').replace(/_.+\.jpg/, '_.jpg'))
                            .filter(u => u && u.includes('alicdn') && !u.includes('no-image'));
                            return ogUrl ? [ogUrl, ...imgs].slice(0, 8) : imgs.slice(0, 8);
                        });
                        break;
                    } catch(e) {
                        if (_try < 1) await page.waitForTimeout(1500);
                    }
                }
            }

            return {
                id: offerId,
                url: request.url,
                title: title,
                image_url: images[0] || '',
                images: images.slice(0, 8),
                attributes: [],
                wholesale_skus: { sku_props: skuProps, sku_info_map_original: skuInfoMap },
                _dbg: { ctxDataKeys: _dbgCtxDataKeys, skuApiCaught: !!skuApiText, skuPropsLen: skuProps.length }
            };
        } catch(err) {
            const _m = request.url.match(/\/offer\/(\d+)\.html/);
            return { id: _m ? _m[1] : '', url: request.url, _error: String(err), title: '', image_url: '',
                     images: [], attributes: [], wholesale_skus: { sku_props: [], sku_info_map_original: {} } };
        }
    }"""

    def _run_detail_urls(url_list, label):
        try:
            print(f"  URL示例: {url_list[0]}")
            start_urls = [{'url': u} for u in url_list]
            resp = _apify_post('acts/apify~playwright-scraper/runs', {
                'startUrls': start_urls,
                'pageFunction': PAGE_FN,
                'proxyConfiguration': {
                    'useApifyProxy': True,
                    'apifyProxyGroups': ['RESIDENTIAL'],
                },
                'maxRequestsPerCrawl': len(url_list),
                'navigationTimeoutSecs': 120,
                'pageLoadTimeoutSecs': 120,
            })
            run_id = resp['data']['id']
            dataset_id = resp['data']['defaultDatasetId']
            status = _wait_for_run(run_id, label)
            if status != 'SUCCEEDED':
                print(f"  {label} 失败，跳过")
                return []
            raw_items = _get_dataset(dataset_id)
            items = [_fix_enc(item) for item in raw_items]
            print(f"  {label} dataset 返回 {len(items)} 条")
            return items
        except Exception as e:
            print(f"  {label} 出错: {e}")
            return []

    details_by_offer = {}
    unresolved = []

    for i in range(0, len(offer_ids), BATCH_SIZE):
        batch = offer_ids[i:i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        total_batches = (len(offer_ids) + BATCH_SIZE - 1) // BATCH_SIZE
        print(f"  批次 {batch_num}/{total_batches}，抓取 {len(batch)} 条详情...")

        url_list = [f"https://detail.1688.com/offer/{oid}.html" for oid in batch]
        items = _run_detail_urls(url_list, f"批次{batch_num}")

        got_in_batch = set()
        for item in items:
            oid = _item_offer_id(item)
            if not oid:
                continue
            got_in_batch.add(oid)
            if oid not in details_by_offer:
                details_by_offer[oid] = item

        print(f"  批次 {batch_num} 成功，获得 {len(got_in_batch)} 条")

        missing = [oid for oid in batch if oid not in got_in_batch]
        if missing:
            print(f"  [warn] 批次 {batch_num} 缺失 {len(missing)} 条，开始逐条补抓...")
            for oid in missing:
                retry_url = [f"https://detail.1688.com/offer/{oid}.html"]
                retry_items = _run_detail_urls(retry_url, f"批次{batch_num}-补抓 {oid}")
                found = False
                for item in retry_items:
                    rid = _item_offer_id(item)
                    if rid == oid:
                        details_by_offer[oid] = item
                        found = True
                        break
                if not found:
                    unresolved.append(oid)
                time.sleep(1)

        if i + BATCH_SIZE < len(offer_ids):
            time.sleep(3)

    all_details = [details_by_offer[oid] for oid in offer_ids if oid in details_by_offer]
    missing_final = [oid for oid in offer_ids if oid not in details_by_offer]

    if missing_final:
        print(f"\n[warn] 详情最终仍缺失 {len(missing_final)} 条: {', '.join(missing_final[:10])}")
    print(f"\n详情抓取完成：请求 {len(offer_ids)} 条，成功 {len(all_details)} 条")

    # 保存原始数据
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    raw_path = os.path.join(DATA_DIR, f'details_raw_{ts}.json')
    with open(raw_path, 'w', encoding='utf-8') as f:
        json.dump(all_details, f, ensure_ascii=False, indent=2)
    print(f"\n原始详情数据已保存: {raw_path}（{len(all_details)} 条）")
    # 打印调试信息（ctxData keys & SKU api 是否抓到）
    for p in all_details:
        dbg = p.get('_dbg', {})
        pid = p.get('id', p.get('url', '?'))
        sku_cnt = len((p.get('wholesale_skus') or {}).get('sku_props', []))
        ctx = dbg.get('ctxDataKeys') or {}
        print(f"  [{pid}] productKeys={ctx.get('productKeys') if isinstance(ctx,dict) else None}  skuApiCaught={dbg.get('skuApiCaught')}  sku_props={sku_cnt}")
    return all_details


# ── 图片下载 ──────────────────────────────────────────────────────────────────

def download_image(url, save_path, retries=3):
    if os.path.exists(save_path):
        return True
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.1688.com/'
    }
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as r:
                with open(save_path, 'wb') as f:
                    f.write(r.read())
            return True
        except Exception as e:
            if attempt == retries - 1:
                print(f"    图片下载失败: {url[:60]}... ({e})")
    return False

# ── 属性提取 ──────────────────────────────────────────────────────────────────

# 1688字段名 → 妙手字段名
ATTR_MAP = {
    '面料名称':       '材质',
    '主面料成分':     '_成分主',
    '主面料成分2':    '_成分辅',
    '主面料成分含量': '_成分主比例',
    '主面料成分2含量':'_成分辅比例',
    '工艺':           '_细节原始',
    '流行元素':       '_细节原始2',
    '款式':           '_类型原始',
    '裤型':           '_类型原始',
    '上市年份/季节':  '_季节原始',
    '风格':           '_风格原始',
    '跨境风格类型':   '_风格原始',
    '弹力':           '面料',      # 妙手"面料"字段存的是弹力值
    '克重':           '_克重',
    '面料克重':       '_克重',
    '单位克重':       '_克重',
    '克重(g/m²)':    '_克重',
    '面料克重(g/m²)': '_克重',
}

# 1688值 → 妙手合法选项（精确匹配下拉框）
MATERIAL_MAP = {
    '牛仔布': '牛仔布', '棉': '棉', '涤纶': '聚酯纤维(涤纶）',
    '聚酯纤维': '聚酯纤维(涤纶）', '氨纶': '氨纶', '莱卡': '莱卡（氨纶）',
    '人造丝': '人棉', '粘胶': '人棉', '莫代尔': '莫代尔',
    '天丝': '天丝（莱赛尔纤维）', '莱赛尔': '莱赛尔（天丝）',
    '腈纶': '腈纶', '尼龙': '尼龙', '亚麻': '亚麻', 'PU': 'PU',
    '棉混纺': '棉混纺',
}

DETAIL_MAP = {
    '手工磨破': '破洞', '磨破': '破洞', '破洞': '破洞',
    '流苏': '流苏', '毛边': '毛边缘', '刺绣': '刺绣',
    '拼接': '撞色', '抽绳': '抽绳', '口袋': '口袋',
    '镂空': '镂空', '系带': '系带', '百褶': '百褶',
    '蕾丝': '蕾丝拼接', '水洗': '水洗牛仔', '雪花': '雪花牛仔',
    '原色': '原色牛仔', '拉链': '拉链', '开衩': '开衩',
    '褶皱': '褶皱边', '荷叶边': '荷叶边', '贴布': '贴布',
    '罗纹': '罗纹',
}

TYPE_MAP = {
    '直筒裤': '直筒裤', '直筒型': '直筒裤',
    '阔腿裤': '阔腿裤', '阔腿型': '阔腿裤',
    '喇叭裤': '喇叭褲', '喇叭型': '喇叭褲',
    '短裤': '短裤型', '三分裤': '短裤型', '五分裤': '中裤',
    '七分裤': '中裤', '裙裤': '裙裤',
    '骑行裤': '骑行裤', '脚踏车裤': '脚踏车裤',
}

SEASON_MAP = {
    '春': '春', '夏': '夏', '秋': '春/秋', '冬': '冬',
    '春季': '春', '夏季': '夏', '秋季': '春/秋', '冬季': '冬',
    '春夏': '春/夏', '秋冬': '秋/冬',
    '四季': '春/夏',  # 最接近全年
}

STYLE_MAP = {
    '牛仔风': '休闲', '休闲': '休闲', '街头': '街头',
    '复古': '复古', '性感': '性感', '运动': '运动',
    '波西米亚': '波西米亚', '学院': '学院', '可爱': '可爱',
    '优雅': '优雅', '成熟': '成熟', '派对': '派对',
    '街头潮人': '街头', '性感辣妹': '性感', '基础款': '基础款',
}

ELASTICITY_MAP = {
    '高弹': '高弹', '中弹': '中弹', '微弹': '微弹',
    '无弹': '无弹', '低弹': '微弹',
}

DEFAULTS = {
    '品牌':      '无品牌',
    '是否透明':  '否',
    '图案':      '纯色',
    '护理说明':  '可机洗且不可干洗',
    '印花类型':  '无印花',
    '织造方式':  '梭织',
    '款式来源':  '现货款',
    '面料纹理1': '光面',
    '里料纹理':  '无里料/无内衬',
    '面料克重1': '300',
}

def _map_value(value, mapping):
    """尝试在映射表中找到匹配值，支持部分匹配"""
    if value in mapping:
        return mapping[value]
    for k, v in mapping.items():
        if k in value:
            return v
    return None

def _extract_season(raw):
    """从 '2025年春季' 提取 '春'"""
    for k, v in SEASON_MAP.items():
        if k in raw:
            return v
    return None

def extract_attrs(raw_attrs):
    """从 1688 attributes 列表提取并格式化为妙手自定义属性字符串"""
    tmp = {}
    for attr in (raw_attrs or []):
        name  = attr.get('name', '')
        value = attr.get('value', '')
        if not value:
            continue
        target_key = ATTR_MAP.get(name)
        if target_key:
            if target_key in tmp:
                tmp[target_key] += '/' + value
            else:
                tmp[target_key] = value

    result = dict(DEFAULTS)  # 从默认值开始

    # 材质
    raw_mat = tmp.get('材质', '')
    mapped_mat = _map_value(raw_mat, MATERIAL_MAP) if raw_mat else None
    if mapped_mat:
        result['材质'] = mapped_mat

    # 面料（弹力）
    raw_ela = tmp.get('面料', '')
    mapped_ela = _map_value(raw_ela, ELASTICITY_MAP) if raw_ela else None
    if mapped_ela:
        result['面料'] = mapped_ela

    # 细节（工艺+流行元素合并，多值用逗号）
    detail_parts = []
    for raw_key in ['_细节原始', '_细节原始2']:
        raw_val = tmp.get(raw_key, '')
        if raw_val:
            for v in raw_val.split(','):
                mapped = _map_value(v.strip(), DETAIL_MAP)
                if mapped and mapped not in detail_parts:
                    detail_parts.append(mapped)
    if detail_parts:
        result['细节'] = detail_parts[0]  # 妙手只支持单选

    # 类型
    raw_type = tmp.get('_类型原始', '')
    if raw_type:
        mapped_type = _map_value(raw_type, TYPE_MAP)
        if mapped_type:
            result['类型'] = mapped_type

    # 季节
    raw_season = tmp.get('_季节原始', '')
    if raw_season:
        mapped_season = _extract_season(raw_season)
        if mapped_season:
            result['季节'] = mapped_season

    # 风格
    raw_style = tmp.get('_风格原始', '')
    if raw_style:
        for v in raw_style.split('/'):
            mapped_style = _map_value(v.strip(), STYLE_MAP)
            if mapped_style:
                result['风格'] = mapped_style
                break

    # 过滤掉临时内部字段，只保留妙手合法字段
    final = {k: v for k, v in result.items() if not k.startswith('_')}
    return '；'.join(f"{k}:{v}" for k, v in final.items())

# ── 标题清洗 ──────────────────────────────────────────────────────────────────

DEEPSEEK_API_KEY = 'sk-34091d9be67642aea1a84b18992d2264'
DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

# 生成标题时跳过的属性（与标题无关）
_TITLE_SKIP_ATTRS = {'颜色', '尺码', '货号', '款号', '品牌', '颜色分类', '尺寸', '适用对象'}

# 标题中不希望出现的“跨境口吻”词
_TITLE_BANNED_TERMS_ZH = ['欧美', '跨境', '跨境电商', '外贸', '出口']
_TITLE_BANNED_PATTERNS_EN = [
    r'(?i)\bEuropean\s+and\s+American\b',
    r'(?i)\bcross[\s-]?border\b',
    r'(?i)\bforeign\s+trade\b',
    r'(?i)\bTemu\b',
]

def _translate_title_en_from_zh(title_zh):
    """将中文标题按一比一语义翻译为英文标题，不补充额外卖点。"""
    title_zh = str(title_zh or '').strip()
    if not title_zh:
        return ''

    prompt = (
        "将下面中文电商标题翻译成英文标题，必须一比一对应原文信息，不允许新增、删减或改写卖点。\\n"
        "要求：保持原有关键词顺序，语言自然简洁，不要品牌词，不要最高级词。\\n"
        "只返回 JSON：{\"title_en\": \"...\"}\\n\\n"
        f"中文标题：{title_zh}"
    )

    payload = json.dumps({
        'model':           'deepseek-chat',
        'messages':        [{'role': 'user', 'content': prompt}],
        'response_format': {'type': 'json_object'},
        'max_tokens':      120,
    }).encode('utf-8')

    req = urllib.request.Request(
        DEEPSEEK_API_URL, data=payload,
        headers={
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
            'Content-Type':  'application/json',
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            resp = json.loads(r.read().decode('utf-8'))
        content = resp['choices'][0]['message']['content']
        result = json.loads(content)
        en = str(result.get('title_en', '')).strip()
        en = _sanitize_title_market_terms(_normalize_title_year(en))
        return en
    except Exception as e:
        print(f"    [DeepSeek] 英文标题翻译失败: {e}")
        return ''


def _gen_temu_titles(product):
    """调用 DeepSeek 生成 Temu 合规的中英文标题。
    严格基于 1688 属性数据，不添加原文没有的内容。
    返回 (title_zh, title_en)；失败返回 (None, None)
    """
    orig_title = _fix_enc(product.get('title', ''))
    attrs = {
        _fix_enc(a.get('name', '')): _fix_enc(a.get('value', ''))
        for a in (product.get('attributes') or [])
    }
    attrs_text = '\n'.join(
        f"  {k}: {v}" for k, v in attrs.items()
        if k and v and k not in _TITLE_SKIP_ATTRS
    )

    def _build_title_prompt(orig, attrs, short_title=None):
        length_hint = (
            f"\n⚠️ 上次生成的标题「{short_title}」只有{len(short_title)}字，严重不足40字下限，"
            "本次必须补充版型、设计细节、穿着场景等描述，使字数达到40~50字。\n"
            if short_title else ''
        )
        return (
            "你是美国本土服饰电商的资深文案。根据以下1688商品信息，生成中英文产品标题。\n\n"
            f"【商品原始标题】\n{orig}\n\n"
            f"【商品属性——唯一可用信息，不得添加属性中没有的内容】\n{attrs}\n\n"
            f"{length_hint}"
            "【规则】\n"
            "- 中文标题结构：[材质] + [版型/剪裁] + [产品类型] + [设计细节] + [穿着场景/风格]\n"
            "  正确示例（注意长度）：\n"
            "  ✓ 棉混纺高腰直筒牛仔短裤女翻边热裤设计显腿长日常休闲街头风夏季（46字）\n"
            "  ✓ 弹力修身高腰牛仔长裤女美式复古直筒宽松显瘦水洗做旧日常通勤休闲（44字）\n"
            "  ✗ 棉混纺牛仔短裤（太短，仅9字）\n"
            "  - 不得包含任何空格和标点符号\n"
            "  - **字数必须在40~50汉字之间，少于40字视为错误**\n"
            "  - 严禁出现：颜色、尺码、数量、规格等变体属性信息\n"
            "- 英文标题：中文标题一比一翻译，80~100字符，不新增不删减\n"
            "- 禁止：欧美、跨境、外贸、出口、European and American、cross-border、foreign trade、Temu\n"
            "- 禁止：品牌词、最高级（luxury/best quality/premium）\n"
            "- 只返回 JSON：{\"title_zh\": \"...\", \"title_en\": \"...\"}"
        )

    def _call_deepseek_title(prompt_text):
        payload = json.dumps({
            'model':           'deepseek-chat',
            'messages':        [{'role': 'user', 'content': prompt_text}],
            'response_format': {'type': 'json_object'},
            'max_tokens':      220,
        }).encode('utf-8')
        req = urllib.request.Request(
            DEEPSEEK_API_URL, data=payload,
            headers={
                'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
                'Content-Type':  'application/json',
            }
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            resp = json.loads(r.read().decode('utf-8'))
        content = resp['choices'][0]['message']['content']
        return json.loads(content)

    try:
        zh = ''
        for attempt in range(3):   # 最多重试2次
            short_hint = zh if (zh and len(zh) < 40) else None
            prompt = _build_title_prompt(orig_title, attrs_text, short_hint)
            result = _call_deepseek_title(prompt)
            zh_raw = str(result.get('title_zh', '')).strip()
            zh_raw = _normalize_zh_title_no_punct_spaces(
                _sanitize_title_market_terms(_normalize_title_year(zh_raw))
            )
            if not zh_raw:
                break
            zh = zh_raw
            if len(zh) >= 40:
                break
            print(f"    [DeepSeek] 标题过短({len(zh)}字)，第{attempt+1}次重试...")
            time.sleep(0.5)

        if not zh:
            return None, None
        if len(zh) < 40:
            print(f"    [DeepSeek] 警告：标题仍不足40字（{len(zh)}字）：{zh}")

        en = _translate_title_en_from_zh(zh)
        if not en:
            en = str(result.get('title_en', '')).strip()
            en = _sanitize_title_market_terms(_normalize_title_year(en))

        return zh or None, en or None
    except Exception as e:
        print(f"    [DeepSeek] 标题生成失败: {e}")
        return None, None



_COLOR_ZH_EN = {
    '黑色': 'Black', '白色': 'White', '灰色': 'Gray', '深灰': 'Dark Gray', '浅灰': 'Light Gray',
    '黑灰': 'Charcoal', '烟灰': 'Smoke Gray', '深黑': 'Black', '纯黑': 'Black', '纯白': 'White',
    '米白色': 'Off White', '乳白色': 'Off White', '象牙白': 'Ivory White',
    '蓝色': 'Blue', '深蓝': 'Dark Blue', '浅蓝': 'Light Blue', '天蓝': 'Sky Blue',
    '藏蓝': 'Navy', '靛蓝': 'Indigo', '冰蓝': 'Ice Blue', '宝蓝': 'Royal Blue',
    '复古蓝': 'Vintage Blue', '水洗蓝': 'Washed Blue', '做旧蓝': 'Distressed Blue',
    '怀旧蓝': 'Nostalgic Blue', '牛仔蓝': 'Denim Blue', '中蓝': 'Medium Blue',
    '米色': 'Beige', '卡其': 'Khaki', '杏色': 'Apricot', '奶白': 'Cream',
    '浅卡其': 'Light Khaki', '深卡其': 'Dark Khaki',
    '棕色': 'Brown', '咖啡': 'Coffee', '驼色': 'Camel',
    '绿色': 'Green', '军绿': 'Army Green', '墨绿': 'Dark Green', '橄榄绿': 'Olive Green',
    '红色': 'Red', '酒红': 'Wine Red', '玫红': 'Rose Red', '砖红': 'Brick Red',
    '粉色': 'Pink', '浅粉': 'Light Pink', '豆沙': 'Dusty Rose',
    '紫色': 'Purple', '淡紫': 'Lavender', '紫罗兰': 'Violet',
    '橙色': 'Orange', '黄色': 'Yellow', '姜黄': 'Mustard',
    '透明': 'Transparent', '玫瑰金': 'Rose Gold', '古铜色': 'Bronze',
    '均码': 'One Size',
}

_COLOR_EN_ALIASES = {
    **{str(v).lower(): v for v in _COLOR_ZH_EN.values()},
    'grey': 'Gray',
    'offwhite': 'Off White',
    'ivory': 'Ivory White',
    'navy blue': 'Navy',
    'dark red': 'Dark Red',
    'powder blue': 'Powder Blue',
    'sea blue': 'Sea Blue',
    'olive': 'Olive',
}

_COLOR_CN_HINTS = [
    ('透明', 'Transparent'),
    ('玫瑰金', 'Rose Gold'),
    ('古铜', 'Bronze'),
    ('香槟', 'Champagne'),
    ('象牙', 'Ivory White'),
    ('乳白', 'Off White'),
    ('米白', 'Off White'),
    ('奶白', 'Cream'),
    ('深灰', 'Dark Gray'),
    ('浅灰', 'Light Gray'),
    ('灰', 'Gray'),
    ('藏青', 'Navy'),
    ('深蓝', 'Dark Blue'),
    ('浅蓝', 'Light Blue'),
    ('蓝', 'Blue'),
    ('军绿', 'Army Green'),
    ('橄榄绿', 'Olive Green'),
    ('橄榄', 'Olive'),
    ('墨绿', 'Dark Green'),
    ('浅绿', 'Light Green'),
    ('绿', 'Green'),
    ('酒红', 'Wine Red'),
    ('玫红', 'Rose Red'),
    ('深红', 'Dark Red'),
    ('红', 'Red'),
    ('粉', 'Pink'),
    ('卡其', 'Khaki'),
    ('杏', 'Apricot'),
    ('姜黄', 'Mustard'),
    ('柠檬黄', 'Lemon Yellow'),
    ('黄', 'Yellow'),
    ('橙', 'Orange'),
    ('紫罗兰', 'Violet'),
    ('淡紫', 'Lavender'),
    ('紫', 'Purple'),
    ('咖啡', 'Coffee'),
    ('驼', 'Camel'),
    ('棕', 'Brown'),
    ('黑', 'Black'),
    ('白', 'White'),
]


def _guess_color_from_chinese(text):
    text = str(text or '').strip()
    if not text:
        return ''
    for kw, color in _COLOR_CN_HINTS:
        if kw in text:
            return color
    return ''


def _extract_english_color(text):
    normalized = re.sub(r'[^A-Za-z\s]+', ' ', str(text or ''))
    normalized = re.sub(r'\s+', ' ', normalized).strip().lower()
    if not normalized:
        return ''

    for phrase in sorted(_COLOR_EN_ALIASES.keys(), key=len, reverse=True):
        if re.search(rf'\b{re.escape(phrase)}\b', normalized):
            return _COLOR_EN_ALIASES[phrase]
    return ''


def _normalize_color_text(raw_color):
    text = str(raw_color or '').strip()
    if not text:
        return ''

    # 去括号内容、数字、常见噪音符号，仅保留中英文词
    text = re.sub(r'\[[^\]]*\]', ' ', text)
    text = re.sub(r'\([^\)]*\)', ' ', text)
    text = re.sub(r'（[^）]*）', ' ', text)
    text = re.sub(r'\{[^\}]*\}', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text = re.sub(r'[#*]+', ' ', text)
    text = re.sub(r'[-_/\\|]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _extract_display_color(raw_color):
    """从原始颜色字符串提取可用颜色；提取失败返回空字符串。"""
    text = _normalize_color_text(raw_color)
    if not text:
        return ''

    mapped = _color_to_en(text)
    if mapped != text:
        return mapped

    for frag in re.findall(r'[\u4e00-\u9fff]{1,8}', text):
        direct = _color_to_en(frag)
        if direct != frag:
            return direct
        if frag.endswith('色'):
            stripped = frag[:-1]
            direct2 = _color_to_en(stripped)
            if direct2 != stripped:
                return direct2
        guess = _guess_color_from_chinese(frag)
        if guess:
            return guess

    en = _extract_english_color(text)
    if en:
        return en

    return ''


def _extract_color_entries(sku_props):
    """从 sku_props 提取去噪后的颜色列表（去重），并附带原始名与色块图。"""
    entries = []
    by_display = {}

    for prop in sku_props:
        if prop.get('prop') not in ('颜色', 'Color', 'color'):
            continue
        for v in prop.get('value', []):
            raw = str(v.get('name', '')).strip()
            if not raw:
                continue

            display = _extract_display_color(raw)
            if not display:
                continue

            key = display.lower()
            entry = by_display.get(key)
            if not entry:
                entry = {'raw': raw, 'display': display, 'image_url': ''}
                by_display[key] = entry
                entries.append(entry)

            img_url = str(v.get('image_url', '')).strip()
            if img_url and not entry['image_url']:
                entry['image_url'] = img_url

    return entries


def _color_to_en(color):
    """中文色名转英文；已是英文则尽量标准化后返回。"""
    color = str(color or '').strip()
    if not color:
        return ''

    r = _COLOR_ZH_EN.get(color)
    if r:
        return r

    if color.endswith('色'):
        r = _COLOR_ZH_EN.get(color[:-1])
        if r:
            return r

    key = re.sub(r'\s+', ' ', color).strip().lower()
    if key in _COLOR_EN_ALIASES:
        return _COLOR_EN_ALIASES[key]

    return color


def _normalize_size_token(token):
    """统一尺码写法：2XL/3XL/4XL → XXL/XXXL/XXXXL（大写）。"""
    token = str(token or '').strip().upper().replace(' ', '')
    if not token:
        return ''

    m = re.fullmatch(r'(\d+)XL', token)
    if m:
        n = int(m.group(1))
        if 1 <= n <= 10:
            return ('X' * n) + 'L'
    return token


def _size_match_variants(size):
    """生成尺码匹配别名，兼容数字XL与X重复写法。"""
    s = _normalize_size_token(size)
    if not s:
        return []

    variants = [s]
    m1 = re.fullmatch(r'(X+)L', s)
    if m1:
        variants.append(f"{len(m1.group(1))}XL")

    m2 = re.fullmatch(r'(\d+)XL', s)
    if m2:
        n = int(m2.group(1))
        if 1 <= n <= 10:
            variants.append(('X' * n) + 'L')

    seen = []
    for v in variants:
        if v not in seen:
            seen.append(v)
    return seen


def _clean_size(size):
    """提取尺码主体，去掉欧码/体重区间等尾随描述。
    例：'M95-105斤' → 'M'，'S码80-95斤' → 'S'，'3xl european size (44)' → 'XXXL'
    """
    if not size:
        return size

    s = str(size).replace('码', ' ').strip()
    s = re.sub(r'[\(（\[【].*?[\)）\]】]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()

    m = re.match(r'^(\d+\s*[A-Za-z]{1,4}|[A-Za-z]{1,4}\+?[A-Za-z]*|\d{2,3}(?:\.\d+)?(?=\D|$))', s)
    if not m:
        return s

    token = m.group(1).replace(' ', '')
    if re.fullmatch(r'\d+[A-Za-z]+', token) or re.fullmatch(r'[A-Za-z]+', token):
        token = token.upper()
    return _normalize_size_token(token)


def clean_title(title, blacklist):
    for word in blacklist:
        title = title.replace(word, '')
    title = ' '.join(title.split())
    return title[:100]


def _normalize_title_year(title):
    """标题中出现四位年份时统一替换为当年；无年份则保持不变。"""
    if not title:
        return title
    year = str(datetime.now().year)
    return re.sub(r'(?<!\d)(?:19|20)\d{2}(?!\d)', year, str(title))


def _normalize_zh_title_no_punct_spaces(title):
    """中文标题去空格与标点，仅保留中文/英文字母/数字。"""
    if not title:
        return ''
    out = str(title)
    out = re.sub(r'\s+', '', out)
    out = re.sub(r'[^\u4e00-\u9fffA-Za-z0-9]', '', out)
    return out.strip()


def _sanitize_title_market_terms(title):
    """移除标题中的跨境口吻词，保证面向美国本地消费者的表达。"""
    if not title:
        return title
    out = str(title)
    for term in _TITLE_BANNED_TERMS_ZH:
        out = out.replace(term, '')
    for pattern in _TITLE_BANNED_PATTERNS_EN:
        out = re.sub(pattern, '', out)
    out = re.sub(r'\s+', ' ', out)
    out = re.sub(r'\s*[-_/|,，;；]\s*$', '', out)
    return out.strip()


def _clean_filename(s, max_len=20):
    """清洗字符串用作文件/文件夹名：替换特殊字符为下划线，合并连续下划线"""
    s = re.sub(r'[\\/:*?"<>|#\s]+', '_', s)
    s = re.sub(r'_+', '_', s).strip('_')
    return s[:max_len]

# ── 飞书工具函数 ──────────────────────────────────────────────────────────────

def _feishu_token():
    """获取飞书 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = json.dumps({
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload,
                                  headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read().decode('utf-8'))
    if data.get('code') != 0:
        raise Exception(f"飞书 token 获取失败: {data.get('msg')}")
    return data['tenant_access_token']

def _feishu_resolve_wiki(token):
    """通过 wiki_token 解析出真实的 Bitable app_token，并列出所有表"""
    url = f"https://open.feishu.cn/open-apis/wiki/v2/spaces/get_node?token={FEISHU_WIKI_TOKEN}"
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read().decode('utf-8'))
    if data.get('code') != 0:
        raise Exception(f"Wiki 解析失败: {data.get('msg')}")
    app_token = data['data']['node']['obj_token']

    # 列出文档内所有表，方便核对 table ID
    list_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables"
    req2 = urllib.request.Request(list_url, headers={'Authorization': f'Bearer {token}'})
    with urllib.request.urlopen(req2, timeout=15) as r2:
        tdata = json.loads(r2.read().decode('utf-8'))
    # 列出文档内所有表，方便核对 table ID
    list_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables"
    req2 = urllib.request.Request(list_url, headers={'Authorization': f'Bearer {token}'})
    with urllib.request.urlopen(req2, timeout=15) as r2:
        tdata = json.loads(r2.read().decode('utf-8'))
    print(f"  app_token: {app_token}")
    print(f"  列表接口返回 code={tdata.get('code')} msg={tdata.get('msg')}")
    tables = tdata.get('data', {}).get('items', [])
    print(f"  文档内共 {len(tables)} 张表:")
    for t in tables:
        print(f"    {t['table_id']}  {t['name']}")
    return app_token
    if data.get('code') != 0:
        raise Exception(f"Wiki 解析失败: {data.get('msg')}")
    app_token = data['data']['node']['obj_token']
    return app_token

def _feishu_batch_create(token, app_token, table_id, records):
    """批量写入飞书多维表格记录（每次最多 500 条）"""
    url = (f"https://open.feishu.cn/open-apis/bitable/v1"
           f"/apps/{app_token}/tables/{table_id}/records/batch_create")
    payload = json.dumps({
        "records": [{"fields": r} for r in records]
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        raise Exception(f"飞书写入 HTTP 错误 {e.code}: {body[:300]}")
    if data.get('code') != 0:
        raise Exception(f"飞书写入失败: {data.get('msg')}")
    return data

def _feishu_list_records(token, app_token, table_id):
    """读取表格所有记录（自动翻页）"""
    all_items = []
    page_token = ''
    while True:
        url = (f"https://open.feishu.cn/open-apis/bitable/v1"
               f"/apps/{app_token}/tables/{table_id}/records"
               f"?page_size=500")
        if page_token:
            url += f"&page_token={page_token}"
        req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode('utf-8'))
        if data.get('code') != 0:
            raise Exception(f"飞书读取失败: {data.get('msg')}")
        items = data['data'].get('items', [])
        all_items.extend(items)
        if not data['data'].get('has_more'):
            break
        page_token = data['data'].get('page_token', '')
    return all_items

def _feishu_list_field_names(token, app_token, table_id):
    """读取表格字段名集合（自动翻页）"""
    names = set()
    page_token = ''
    while True:
        url = (f"https://open.feishu.cn/open-apis/bitable/v1"
               f"/apps/{app_token}/tables/{table_id}/fields"
               f"?page_size=500")
        if page_token:
            url += f"&page_token={page_token}"
        req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode('utf-8'))
        if data.get('code') != 0:
            raise Exception(f"飞书字段读取失败: {data.get('msg')}")
        for item in data.get('data', {}).get('items', []):
            name = str(item.get('field_name', '')).strip()
            if name:
                names.add(name)
        if not data.get('data', {}).get('has_more'):
            break
        page_token = data.get('data', {}).get('page_token', '')
    return names


def _probe_fields(token, app_token, table_id, sample_record):
    """逐字段试探，找出哪些字段名在飞书表里不存在"""
    print("  [诊断] 逐字段检测...")
    bad = []
    for key, val in sample_record.items():
        try:
            _feishu_batch_create(token, app_token, table_id, [{key: val}])
            print(f"    ✓ {key}")
        except Exception as e:
            msg = str(e)
            if 'FieldNameNotFound' in msg:
                print(f"    ✗ {key}  ← 字段名不存在")
                bad.append(key)
            else:
                print(f"    ~ {key}  ({msg[-40:]})")
    return bad

def _feishu_upload_image(image_url, token, app_token):
    """下载1688图片并上传到飞书，返回 file_token；失败返回 None（含重试）"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.1688.com/'
    }
    img_data = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(image_url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as r:
                img_data = r.read()
            break
        except Exception as e:
            print(f"    图片下载失败(第{attempt+1}次): {e}")
            if attempt < 2:
                time.sleep(2)
    if not img_data:
        return None

    fname = image_url.split('/')[-1].split('?')[0] or 'image.jpg'
    if '.' not in fname:
        fname += '.jpg'

    boundary = b'----FeishuUploadBoundary'

    def _field(name, value):
        return (b'--' + boundary + b'\r\n'
                + b'Content-Disposition: form-data; name="' + name.encode() + b'"\r\n\r\n'
                + value.encode() + b'\r\n')

    body = (
        _field('file_name', fname) +
        _field('parent_type', 'bitable_image') +
        _field('parent_node', app_token) +
        _field('size', str(len(img_data))) +
        b'--' + boundary + b'\r\n'
        b'Content-Disposition: form-data; name="file"; filename="' + fname.encode() + b'"\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' +
        img_data + b'\r\n' +
        b'--' + boundary + b'--\r\n'
    )

    upload_req = urllib.request.Request(
        'https://open.feishu.cn/open-apis/drive/v1/medias/upload_all',
        data=body,
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'multipart/form-data; boundary=----FeishuUploadBoundary',
        }
    )
    try:
        with urllib.request.urlopen(upload_req, timeout=30) as r:
            resp = json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8', errors='replace')
        print(f"    飞书上传失败 {e.code}: {err_body[:200]}")
        return None

    if resp.get('code') != 0:
        print(f"    飞书上传失败: {resp.get('msg')}")
        return None

    return resp['data']['file_token']

_img_cache = {}  # URL → file_token，避免同一图片重复上传

def _upload_img_list(urls, token, app_token, max_imgs=3):
    """批量下载并上传图片到飞书，返回附件格式列表 [{"file_token": "xxx"}, ...]"""
    result = []
    for url in urls:
        if not url or len(result) >= max_imgs:
            break
        if url in _img_cache:
            result.append({"file_token": _img_cache[url]})
            continue
        ft = _feishu_upload_image(url, token, app_token)
        if ft:
            _img_cache[url] = ft
            result.append({"file_token": ft})
    return result

def _push_records(token, app_token, table_id, records, label=''):
    """分批推送记录，每批 500 条"""
    pushed = 0
    for i in range(0, len(records), 500):
        batch = records[i:i + 500]
        _feishu_batch_create(token, app_token, table_id, batch)
        pushed += len(batch)
        if label:
            print(f"  [{label}] 已推送 {pushed}/{len(records)} 条")

# ── 第四阶段：搜索结果推表1（审核选品）────────────────────────────────────────

def stage4_push_review(offer_ids, offers_info, token, app_token):
    """将搜索结果推送到飞书表1（产品级，一款一行）供审核"""
    print(f"\n=== 第四阶段：推送审核表（{len(offer_ids)} 条）===")

    records = []
    total = len(offer_ids)
    for idx, oid in enumerate(offer_ids, 1):
        item  = offers_info.get(oid, {})
        title = item.get('title', f'商品{oid}')
        try:
            title = title.encode('latin1').decode('utf-8')
        except Exception:
            pass
        price     = _get_search_price(item)
        image_url = item.get('image_url', '')
        link      = f'https://detail.1688.com/offer/{oid}.html'
        record = {
            '选中采集': False,
            '产品名称': title[:100],
            '产品编号': oid,
            '采购链接': {'link': link, 'text': link},
            '供货价':   round(price, 2),
        }
        if image_url:
            print(f"  上传图片 {idx}/{total}...")
            file_token = _feishu_upload_image(image_url, token, app_token)
            if file_token:
                record['产品图片'] = [{"file_token": file_token}]
        records.append(record)

    _push_records(token, app_token, FEISHU_PREVIEW_TABLE, records, '表1')
    print(f"  表1写入完成，请在飞书审核并勾选「选中采集」")

# ── 第五阶段：读取勾选结果 ────────────────────────────────────────────────────

def stage5_read_selected(token, app_token):
    """从飞书表1读回被勾选的 offer_id 列表，同时返回中文标题映射"""
    print(f"\n=== 第五阶段：读取飞书勾选结果 ===")
    records = _feishu_list_records(token, app_token, FEISHU_PREVIEW_TABLE)

    selected   = []
    title_map  = {}   # offer_id -> 中文标题（来自 devcake 搜索结果）
    for rec in records:
        fields = rec.get('fields', {})
        if fields.get('选中采集') is True:
            raw = fields.get('产品编号', '')
            # 飞书数字字段会返回 float，去掉 .0 后缀
            if isinstance(raw, float):
                oid = str(int(raw))
            else:
                oid = str(raw).strip()
                if oid.endswith('.0'):
                    oid = oid[:-2]
            if oid:
                selected.append(oid)
                name = fields.get('产品名称', '')
                if isinstance(name, list):   # 飞书富文本字段有时返回列表
                    name = ''.join(seg.get('text', '') for seg in name)
                title_map[oid] = str(name).strip()

    print(f"  勾选了 {len(selected)} 条商品")
    return selected, title_map

# ── 第六阶段：详情推表2（店小秘格式）─────────────────────────────────────────

def _is_english_title(title):
    """判断标题是否缺少中文字符（ecomscrape 返回英文页时出现）"""
    return sum(1 for c in title if '\u4e00' <= c <= '\u9fff') == 0

SKU_IMG_TABLE_ID = 'tblDI0tawNADHTmV'   # 图生图处理表


def stage6_push_dianxiaomi(details, blacklist, token, app_token,
                            search_titles=None, prod_no_map=None):
    """将抓到的详情按 SKU 展开，推送到飞书店小秘格式表，同时同步图生图处理表。
    search_titles: {offer_id: 中文标题} 可选，ecomscrape 返回英文时用作 fallback
    prod_no_map:   {offer_id: prod_no}  可选，不传则用 offer_id 作产品货号
    """
    print(f"\n=== 第六阶段：推送店小秘表（{len(details)} 条商品）===")

    records     = []   # 店小秘格式表
    sku_records = []   # 图生图处理表（每颜色一行）

    for product in details:
        offer_id = str(product.get('id', ''))
        if not offer_id:
            continue

        title_raw = product.get('title', f'商品{offer_id}')
        if _is_english_title(title_raw) and search_titles and offer_id in search_titles:
            title_raw = search_titles[offer_id] or title_raw
        title_clean = clean_title(title_raw, blacklist)
        detail_url  = product.get('url', f'https://detail.1688.com/offer/{offer_id}.html')
        attrs_list  = product.get('attributes', [])
        description = build_description(attrs_list)

        # DeepSeek 生成中英文标题（失败则保留原始标题，英文留空）
        title_zh, title_en = _gen_temu_titles(product)
        if title_zh:
            title_clean = title_zh
            print(f"  [{offer_id}] 标题: {title_zh[:40]}")

        title_clean = _normalize_zh_title_no_punct_spaces(
            _sanitize_title_market_terms(_normalize_title_year(title_clean))
        )

        translated_en = _translate_title_en_from_zh(title_clean) if title_clean else ''
        if translated_en:
            title_en = translated_en
        title_en = _sanitize_title_market_terms(_normalize_title_year(title_en or ''))

        skus_data    = product.get('wholesale_skus', {}) or {}
        sku_props    = skus_data.get('sku_props', [])
        sku_info     = skus_data.get('sku_info_map_original', {})

        color_entries = _extract_color_entries(sku_props)
        sizes = []
        for prop in sku_props:
            if prop.get('prop') in ('尺码', '尺寸', 'Size', 'size'):
                for v in prop.get('value', []):
                    sizes.append(_clean_size(v['name']))

        if not color_entries:
            print(f"  [skip] {offer_id} 无可用颜色，已跳过")
            continue

        color_images = {e['raw']: e.get('image_url', '') for e in color_entries}
        color_display_by_raw = {e['raw']: e['display'] for e in color_entries}
        raw_colors = [e['raw'] for e in color_entries]

        # 兼容新抓取器格式：images 为字符串列表，旧格式为 main_images 对象列表
        _raw_imgs = product.get('images', [])
        if _raw_imgs and isinstance(_raw_imgs[0], dict):
            prod_images = [img.get('full_path_image_u_r_i', '') for img in _raw_imgs if img.get('full_path_image_u_r_i')]
        else:
            prod_images = [u for u in _raw_imgs if u]
        if not prod_images and product.get('image_url'):
            prod_images = [product['image_url']]
        # 若色块图为空（新抓取器无色图），用商品主图轮流分配给各颜色
        for i, entry in enumerate(color_entries):
            if not color_images.get(entry['raw']) and prod_images:
                color_images[entry['raw']] = prod_images[i % len(prod_images)]

        if sizes:
            attr_name1, attr_name2 = '颜色', '尺码'
            combos = [(c, s) for c in raw_colors for s in sizes]
        else:
            attr_name1, attr_name2 = '颜色', ''
            combos = [(c, '') for c in raw_colors]

        # 重量表：sku_id → 克
        weight_scale_info = (product.get('main_videos', {}) or {}) \
            .get('piece_weight_scale', {}) \
            .get('piece_weight_scale_info', [])

        # 产品主编号：优先用传入的 prod_no_map，回退到 offer_id
        prod_no     = prod_no_map.get(offer_id, offer_id) if prod_no_map else offer_id
        prod_folder = prod_no   # 只用产品编号，RPA识别简洁

        # （main_img_urls 已在 prod_images 中处理，此处保留变量以备扩展）

        # ── 图生图处理表：每个颜色一行 ──
        for color in raw_colors:
            display_color = color_display_by_raw.get(color, '')
            if not display_color:
                continue
            sku_rec = {
                'offer_id':   prod_no,
                '颜色':       display_color,
                '产品文件夹': prod_folder,
                '产品标题':   title_clean,   # 供图生图动态生成 prompt 用
            }
            img_url = color_images.get(color, '')
            if img_url:
                sku_rec['原始图链接'] = img_url
                ft = _feishu_upload_image(img_url, token, app_token)
                if ft:
                    sku_rec['原始图'] = [{'file_token': ft}]
                    sku_rec['图2']    = [{'file_token': ft}]   # 复用同一 file_token，无需二次上传
            sku_records.append(sku_rec)

        first = True
        for color, size in combos:
            display_color = color_display_by_raw.get(color, '')
            if not display_color:
                continue

            price_raw     = _lookup_price(sku_info, color, size, product)
            declare_price = round(price_raw + PRICE_PLUS, 2)
            platform_sku  = f"{prod_no}-{display_color}-{size}".strip('-')

            rec = {
                '*产品标题':            title_clean,
                '*英文标题':            title_en or '',
                '产品描述':             description if first else '',
                '产品货号':             prod_no,
                '*变种属性名称一':      attr_name1,
                '*变种属性值一':        display_color,
                '变种属性名称二':       attr_name2,
                '变种属性值二':         size,
                '*申报价格 (店铺币种)': str(declare_price),
                'SKU货号':             platform_sku,
                '*长（cm）':           str(PKG_LENGTH),
                '*宽（cm）':           str(PKG_WIDTH),
                '*高（cm）':           str(PKG_HEIGHT),
                '*重量（g）':          str(WEIGHT_G),
                '识别码类型':          '',
                '识别码':              '',
                '外包装形状':          '',
                '外包装类型':          '',
                '建议售价（USD）':     str(RETAIL_USD),
                '库存':                '999',
                '发货时效（天）':       '9',
            }
            if first:
                rec['站外产品链接'] = {'link': detail_url, 'text': detail_url}

            records.append(rec)
            first = False

    _push_records(token, app_token, FEISHU_MIAOSHOU_TABLE, records, '店小秘格式表')
    print(f"  店小秘格式表写入完成，共 {len(records)} 条 SKU 记录")

    if sku_records:
        try:
            _push_records(token, app_token, SKU_IMG_TABLE_ID, sku_records, '图生图处理表')
            print(f"  图生图处理表写入完成，共 {len(sku_records)} 条颜色记录")
        except Exception as e:
            print(f"  [warn] 图生图处理表写入失败: {e}")


def _extract_link_text(val):
    """提取飞书字段中的链接/文本值。"""
    if isinstance(val, dict):
        return str(val.get('link') or val.get('text') or '').strip()
    if isinstance(val, list):
        parts = []
        for seg in val:
            if isinstance(seg, dict):
                text = seg.get('link') or seg.get('text') or ''
                if text:
                    parts.append(str(text))
        return ''.join(parts).strip()
    return str(val).strip() if val else ''


def _color_key_variants(color):
    """生成颜色匹配键，兼容空格/下划线与中英文。"""
    color = str(color or '').strip()
    if not color:
        return []

    variants = []

    def _add(v):
        v = str(v or '').strip()
        if v and v not in variants:
            variants.append(v)

    _add(color)
    _add(color.replace('_', ' '))

    en = _color_to_en(color)
    _add(en)
    _add(en.replace('_', ' '))

    clean_color = _clean_filename(color, max_len=30)
    _add(clean_color)
    _add(clean_color.replace('_', ' '))

    clean_en = _clean_filename(_color_to_en(color), max_len=30)
    _add(clean_en)
    _add(clean_en.replace('_', ' '))

    return variants


def stage_sync_miaoshou_material_links(token, app_token,
                                      miaoshou_table_id=FEISHU_MIAOSHOU_TABLE,
                                      sku_table_id=SKU_IMG_TABLE_ID):
    """将图生图处理表的图1链接/AI白底图链接回填到店小秘格式表。"""
    print("\n=== 回填店小秘素材图（图1链接 + AI白底图链接） ===")

    img_records = _feishu_list_records(token, app_token, sku_table_id)
    color_link_map = {}   # (prod_no, color_variant) -> {'img1': url, 'bg': url}
    prod_link_map = {}    # prod_no -> {'img1': url, 'bg': url}

    def _merge_link(dst, img1_url, bg_url):
        if img1_url and not dst.get('img1'):
            dst['img1'] = img1_url
        if bg_url and not dst.get('bg'):
            dst['bg'] = bg_url

    for rec in img_records:
        fields = rec.get('fields', {})
        prod_no = str(fields.get('产品文件夹', '')).strip() or str(fields.get('offer_id', '')).strip()
        if not prod_no:
            continue

        img1_url = _extract_link_text(fields.get('图1链接', ''))
        bg_url = _extract_link_text(fields.get('AI白底图链接', ''))
        if not img1_url and not bg_url:
            continue

        prod_links = prod_link_map.setdefault(prod_no, {})
        _merge_link(prod_links, img1_url, bg_url)

        color = str(fields.get('颜色', '')).strip()
        for c in _color_key_variants(color):
            links = color_link_map.setdefault((prod_no, c), {})
            _merge_link(links, img1_url, bg_url)

    if not color_link_map and not prod_link_map:
        print("  未找到可用图1/白底图链接，跳过回填")
        return 0

    miaoshou_records = _feishu_list_records(token, app_token, miaoshou_table_id)
    updated_rows = 0
    material_updates = 0
    extra_text_updates = 0
    missing_optional_fields = set()

    miaoshou_field_names = None
    try:
        miaoshou_field_names = _feishu_list_field_names(token, app_token, miaoshou_table_id)
    except Exception as e:
        print(f"  [warn] 读取店小秘字段列表失败，将按写入返回动态探测: {e}")

    has_material_field = True
    optional_text_fields = [('图1链接', 'img1'), ('AI白底图链接', 'bg'), ('百度图链接', 'bg')]
    if miaoshou_field_names is not None:
        has_material_field = '*产品素材图' in miaoshou_field_names
        optional_text_fields = [
            (field_name, key)
            for field_name, key in optional_text_fields
            if field_name in miaoshou_field_names
        ]
        if not has_material_field:
            print("  [warn] 店小秘格式表缺少字段「*产品素材图」，已跳过素材图回填")
        if len(optional_text_fields) == 0:
            print("  店小秘格式表未配置图1链接/AI白底图链接/百度图链接字段，已跳过文本链接回填")

    for rec in miaoshou_records:
        rid = rec.get('record_id', '')
        fields = rec.get('fields', {})
        prod_no = str(fields.get('产品货号', '')).strip()
        color = str(fields.get('*变种属性值一', '')).strip()
        if not rid or not prod_no:
            continue

        links = {}
        for c in _color_key_variants(color):
            links = color_link_map.get((prod_no, c), {})
            if links:
                break
        if not links:
            links = prod_link_map.get(prod_no, {})

        img1_url = links.get('img1', '')
        bg_url = links.get('bg', '')
        if not img1_url and not bg_url:
            continue

        row_changed = False
        material_url = img1_url or bg_url

        if has_material_field and material_url:
            current_material = _extract_link_text(fields.get('*产品素材图', ''))
            if current_material != material_url:
                try:
                    _feishu_update_record(token, app_token, miaoshou_table_id, rid, {
                        '*产品素材图': material_url,
                    })
                    row_changed = True
                    material_updates += 1
                except Exception as e:
                    if 'AttachFieldConvFail' not in str(e):
                        print(f"  [warn] 回填失败 {prod_no}/{color}: {e}")
                    else:
                        ft = _feishu_upload_url_image(material_url, token, app_token)
                        if not ft:
                            print(f"  [warn] 回填失败 {prod_no}/{color}: 素材图上传附件失败")
                        else:
                            try:
                                _feishu_update_record(token, app_token, miaoshou_table_id, rid, {
                                    '*产品素材图': [{'file_token': ft}],
                                })
                                row_changed = True
                                material_updates += 1
                            except Exception as e2:
                                print(f"  [warn] 回填失败 {prod_no}/{color}: {e2}")

        target_url_by_key = {
            'img1': img1_url,
            'bg': bg_url,
        }
        for field_name, target_key in optional_text_fields:
            target_url = target_url_by_key.get(target_key, '')
            if not target_url:
                continue
            if field_name in missing_optional_fields:
                continue

            current_val = _extract_link_text(fields.get(field_name, ''))
            if current_val == target_url:
                continue

            try:
                _feishu_update_record(token, app_token, miaoshou_table_id, rid, {
                    field_name: target_url,
                })
                row_changed = True
                extra_text_updates += 1
            except Exception as e:
                if 'FieldNameNotFound' in str(e):
                    missing_optional_fields.add(field_name)
                    print(f"  [warn] 店小秘格式表缺少字段「{field_name}」，已跳过该字段回填")
                else:
                    print(f"  [warn] 回填失败 {prod_no}/{color} {field_name}: {e}")

        if row_changed:
            updated_rows += 1

    print(
        f"  回填完成：更新 {updated_rows} 行，"
        f"*产品素材图更新 {material_updates} 次，"
        f"文本链接更新 {extra_text_updates} 次"
    )
    return updated_rows


# ── 第三阶段：生成 XLS ────────────────────────────────────────────────────────
DXM_HEADERS = [
    '*产品标题',       '*英文标题',            '产品描述',            '产品货号',
    '*变种属性名称一',  '*变种属性值一',         '变种属性名称二',       '变种属性值二',
    '预览图',          '*申报价格\n(店铺币种)',  'SKU货号',
    '*长（cm）',       '*宽（cm）',            '*高（cm）',           '*重量（g）',
    '识别码类型',       '识别码',               '站外产品链接',
    '*轮播图',         '*产品素材图',
    '外包装形状',       '外包装类型',           '外包装图片',
    '建议售价（USD）',  '库存',                '发货时效（天）',
]

INSTRUCTIONS = (
    "各个字段说明：\n"
    "1、产品主编号：一个SKU一行，若多个SKU同属于一个产品，请填入相同的产品主编号\n"
    "2、产品主图：输入图片链接，多个用中文逗号分割。注意：同一产品只需第一个SKU填写产品主图，其他SKU可忽略此列\n"
    "3、详情图：输入图片链接，多个用中文逗号分割。注意：同一产品只需第一个SKU填写详情图，其他SKU可忽略此列\n"
    "4、自定义属性：输入产品属性，多个属性用分号分隔，例如：品牌:无品牌；材质:棉\n"
    "5、产品主编号、产品名称和SKU售价为必填项"
)

def build_description(attrs_list):
    """从属性列表生成简短描述"""
    parts = []
    keys = ['面料名称', '主面料成分', '弹力', '腰型', '裤型', '风格']
    attr_dict = {a['name']: a['value'] for a in (attrs_list or [])}
    for k in keys:
        if k in attr_dict:
            parts.append(attr_dict[k])
    return '，'.join(parts) if parts else ''

def stage3_generate_xls(details, blacklist, output_path, prod_no_map=None):
    print(f"\n=== 第三阶段：生成 XLS（{len(details)} 条商品）===")

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sheet1')

    for col, header in enumerate(DXM_HEADERS):
        ws.write(0, col, header)

    row = 1
    success_count = 0

    for product in details:
        offer_id = str(product.get('id', ''))
        if not offer_id:
            continue

        title_raw    = product.get('title', f'商品{offer_id}')
        title_clean  = _sanitize_title_market_terms(_normalize_title_year(clean_title(title_raw, blacklist)))
        detail_url   = product.get('url', f'https://detail.1688.com/offer/{offer_id}.html')
        attrs_list   = product.get('attributes', [])
        description  = build_description(attrs_list)

        main_images_data = product.get('main_images', [])
        main_image_urls = []
        for img in main_images_data[:8]:
            url = img.get('full_path_image_u_r_i', '')
            if url:
                main_image_urls.append(url)
                fname = url.split('/')[-1].split('?')[0]
                save  = os.path.join(IMAGES_DIR, offer_id, 'main', fname)
                download_image(url, save)

        main_img_str = '\n'.join(main_image_urls)  # 店小秘要求换行符分隔

        skus_data   = product.get('wholesale_skus', {}) or {}
        sku_props   = skus_data.get('sku_props', [])
        sku_info    = skus_data.get('sku_info_map_original', {})

        color_entries = _extract_color_entries(sku_props)
        sizes  = []
        for prop in sku_props:
            if prop.get('prop') in ('尺码', '尺寸', 'Size', 'size'):
                for v in prop.get('value', []):
                    sizes.append(_clean_size(v['name']))

        if not color_entries:
            print(f"  [skip] {offer_id} 无可用颜色，已跳过")
            continue

        color_images = {e['raw']: e.get('image_url', '') for e in color_entries}
        color_display_by_raw = {e['raw']: e['display'] for e in color_entries}
        raw_colors = [e['raw'] for e in color_entries]

        if sizes:
            attr_name1, attr_name2 = '颜色', '尺码'
            combos = [(c, s) for c in raw_colors for s in sizes]
        else:
            attr_name1, attr_name2 = '颜色', ''
            combos = [(c, '') for c in raw_colors]

        weight_scale_info = (product.get('main_videos', {}) or {}) \
            .get('piece_weight_scale', {}) \
            .get('piece_weight_scale_info', [])

        # 产品主编号：优先用传入的 prod_no_map，回退到 offer_id
        prod_no = prod_no_map.get(offer_id, offer_id) if prod_no_map else offer_id

        first_in_product = True
        for color, size in combos:
            display_color = color_display_by_raw.get(color, '')
            if not display_color:
                continue

            price_raw     = _lookup_price(sku_info, color, size, product)
            declare_price = round(price_raw + PRICE_PLUS, 2)
            sku_img       = color_images.get(color, '')
            platform_sku  = f"{prod_no}-{display_color}-{size}".strip('-')

            if sku_img:
                fname = sku_img.split('/')[-1].split('?')[0]
                save  = os.path.join(IMAGES_DIR, offer_id, 'sku', fname)
                download_image(sku_img, save)

            _write_dxm_row(
                ws, row, prod_no, title_clean, main_img_str, detail_url,
                description, attr_name1, display_color, attr_name2, size,
                sku_img, declare_price, platform_sku, first_in_product, WEIGHT_G
            )
            row += 1
            first_in_product = False

        success_count += 1
        if success_count % 10 == 0:
            print(f"  已处理 {success_count}/{len(details)} 条")

    wb.save(output_path)
    print(f"\nXLS 已生成: {output_path}")
    print(f"成功处理商品: {success_count} 条，总行数: {row - 1} 行")

def stage_download_sku_images(details, blacklist, prod_no_map=None):
    """下载 SKU 图片到本地，按商品/颜色整理好文件夹，供 RPA 使用。
    结构：data/sku_images/{prod_no}_{clean_title}/{clean_color}/1.jpg 2.jpg 3.jpg
      1.jpg = 色块图（无则用主图1）
      2.jpg = 主图第1张
      3.jpg = 主图第2张
    prod_no_map: {offer_id: prod_no} 可选，不传则用 offer_id 作文件夹前缀
    """
    print(f"\n=== 下载 SKU 图片（RPA 用，共 {len(details)} 条商品）===")
    SKU_IMG_DIR = os.path.join(DATA_DIR, 'sku_images')
    os.makedirs(SKU_IMG_DIR, exist_ok=True)

    for product in details:
        offer_id = str(product.get('id', ''))
        if not offer_id:
            continue

        prod_no     = prod_no_map.get(offer_id, offer_id) if prod_no_map else offer_id
        folder_name = prod_no   # 只用产品编号，RPA识别简洁
        product_dir = os.path.join(SKU_IMG_DIR, folder_name)
        os.makedirs(product_dir, exist_ok=True)

        # 主图（取前3张备用）—— 兼容新格式(strings)和旧格式(dicts)
        _raw_imgs = product.get('images', [])
        if _raw_imgs and isinstance(_raw_imgs[0], dict):
            main_img_urls = [img.get('full_path_image_u_r_i', '') for img in _raw_imgs[:3] if img.get('full_path_image_u_r_i')]
        else:
            main_img_urls = [u for u in _raw_imgs[:3] if u]
        if not main_img_urls and product.get('image_url'):
            main_img_urls = [product['image_url']]

        # 解析颜色 + 色块图
        color_entries = _extract_color_entries((product.get('wholesale_skus', {}) or {}).get('sku_props', []))
        if not color_entries:
            print(f"  [skip] {folder_name} 无可用颜色，已跳过")
            continue

        color_images = {e['raw']: e.get('image_url', '') for e in color_entries}
        # 若色块图为空（新抓取器无色图），用主图轮流分配
        for i, entry in enumerate(color_entries):
            if not color_images.get(entry['raw']) and main_img_urls:
                color_images[entry['raw']] = main_img_urls[i % len(main_img_urls)]

        for entry in color_entries:
            color = entry['raw']
            display_color = entry['display']
            color_dir = os.path.join(product_dir, display_color)
            os.makedirs(color_dir, exist_ok=True)

            img1 = color_images.get(color) or (main_img_urls[0] if main_img_urls else '')
            img2 = main_img_urls[0] if main_img_urls else ''
            img3 = main_img_urls[1] if len(main_img_urls) > 1 else ''

            for fname, url in [('1.jpg', img1), ('2.jpg', img2), ('3.jpg', img3)]:
                if url:
                    download_image(url, os.path.join(color_dir, fname))

        print(f"  {folder_name}  ({len(color_entries)} 色)")

    print(f"\n图片已保存到: {SKU_IMG_DIR}")


# ── SKU 图片飞书管理（推送 + 下载）────────────────────────────────────────────

def _resolve_app_token(token, wiki_token):
    """通过任意 wiki_token 解析出 Bitable app_token"""
    url = f'https://open.feishu.cn/open-apis/wiki/v2/spaces/get_node?token={wiki_token}'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read().decode('utf-8'))
    if data.get('code') != 0:
        raise Exception(f'Wiki 解析失败 code={data["code"]}: {data.get("msg")}')
    return data['data']['node']['obj_token']


def _feishu_upload_local_file(filepath, token, app_token):
    """上传本地图片文件到飞书 Bitable，返回 file_token；失败返回 None"""
    with open(filepath, 'rb') as f:
        img_data = f.read()

    fname = os.path.basename(filepath)
    boundary = b'----FeishuUploadBoundary'

    def _field(name, value):
        return (b'--' + boundary + b'\r\n'
                + b'Content-Disposition: form-data; name="' + name.encode() + b'"\r\n\r\n'
                + value.encode() + b'\r\n')

    # 根据扩展名选 Content-Type
    ext = fname.lower().rsplit('.', 1)[-1]
    ct  = {'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
           'png': 'image/png', 'webp': 'image/webp'}.get(ext, 'image/jpeg')

    body = (
        _field('file_name', fname) +
        _field('parent_type', 'bitable_image') +
        _field('parent_node', app_token) +
        _field('size', str(len(img_data))) +
        b'--' + boundary + b'\r\n'
        b'Content-Disposition: form-data; name="file"; filename="' + fname.encode() + b'"\r\n' +
        b'Content-Type: ' + ct.encode() + b'\r\n\r\n' +
        img_data + b'\r\n' +
        b'--' + boundary + b'--\r\n'
    )

    upload_req = urllib.request.Request(
        'https://open.feishu.cn/open-apis/drive/v1/medias/upload_all',
        data=body,
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'multipart/form-data; boundary=----FeishuUploadBoundary',
        }
    )
    try:
        with urllib.request.urlopen(upload_req, timeout=30) as r:
            resp = json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8', errors='replace')
        print(f'    本地文件上传失败 {e.code}: {err_body[:200]}')
        return None

    if resp.get('code') != 0:
        print(f'    本地文件上传失败: {resp.get("msg")}')
        return None
    return resp['data']['file_token']


def _feishu_download_file(file_token, token, dest_path, table_id=None):
    """从飞书下载附件，保存到 dest_path；返回 True/False
    多维表格附件需传 table_id，否则 API 返回 400。
    """
    import urllib.parse
    base = f'https://open.feishu.cn/open-apis/drive/v1/medias/{file_token}/download'
    if table_id:
        extra = urllib.parse.quote(json.dumps(
            {'bitablePerm': {'tableId': table_id, 'rev': 0}},
            separators=(',', ':')
        ))
        url = f'{base}?extra={extra}'
    else:
        url = base
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, 'wb') as f:
            f.write(data)
        return True
    except Exception as e:
        print(f'    飞书文件下载失败 {file_token}: {e}')
        return False


def stage_push_sku_to_feishu(token, app_token,
                              table_id='tblDI0tawNADHTmV'):
    """
    扫描 data/sku_images/ 下所有商品/颜色文件夹，
    每个颜色上传一张原始图到飞书多维表格（一行一色）。

    飞书表格需要字段：产品文件夹(文本) offer_id(文本) 颜色(文本) 原始图(附件)
    """
    sku_img_dir = os.path.join(DATA_DIR, 'sku_images')
    if not os.path.isdir(sku_img_dir):
        print('data/sku_images/ 不存在，请先运行 stage_download_sku_images')
        return

    prod_folders = sorted(
        f for f in os.listdir(sku_img_dir)
        if os.path.isdir(os.path.join(sku_img_dir, f))
    )
    print(f'\n=== 推送 SKU 图片到飞书（{len(prod_folders)} 个商品）===')

    records = []
    for prod_folder in prod_folders:
        offer_id    = prod_folder.split('_')[0]
        product_dir = os.path.join(sku_img_dir, prod_folder)

        color_folders = sorted(
            c for c in os.listdir(product_dir)
            if os.path.isdir(os.path.join(product_dir, c))
        )
        for color_folder in color_folders:
            color_dir = os.path.join(product_dir, color_folder)
            # 取第一张可用图（1.jpg 优先）
            img_path = None
            for fname in ['1.jpg', '2.jpg', '3.jpg']:
                p = os.path.join(color_dir, fname)
                if os.path.exists(p):
                    img_path = p
                    break
            if not img_path:
                continue

            print(f'  上传 {prod_folder}/{color_folder} ...')
            ft = _feishu_upload_local_file(img_path, token, app_token)
            record = {
                '产品文件夹': prod_folder,
                'offer_id':   int(offer_id),   # 飞书字段类型为数字
                '颜色':       color_folder,
            }
            if ft:
                record['原始图'] = [{'file_token': ft}]
            records.append(record)

    if not records:
        print('无可上传记录')
        return

    print(f'  共 {len(records)} 行，推送到飞书...')
    _push_records(token, app_token, table_id, records, 'SKU图片表')
    print(f'  推送完成')


def stage_download_sku_from_feishu(token, app_token,
                                    table_id='tblDI0tawNADHTmV'):
    """
    从飞书多维表格读取图1/图2/图3字段（附件），
    下载到本地对应的 data/sku_images/{产品文件夹}/{颜色}/ 目录。
    本地文件命名：1.jpg 2.jpg 3.jpg（覆盖旧文件）

    飞书表格需要字段：产品文件夹(文本) 颜色(文本) 图1(附件) 图2(附件) 图3(附件)
    """
    sku_img_dir = os.path.join(DATA_DIR, 'sku_images')
    print(f'\n=== 从飞书下载 SKU 图片 ===')

    items = _feishu_list_records(token, app_token, table_id)
    print(f'  共 {len(items)} 条记录')

    ok = fail = skip = 0
    for item in items:
        fields      = item.get('fields', {})
        prod_folder = str(fields.get('产品文件夹', '')).strip()
        color       = str(fields.get('颜色', '')).strip()

        if not prod_folder or not color:
            skip += 1
            continue

        dest_dir = os.path.join(sku_img_dir, prod_folder, color)

        # 0.jpg=AI白底图 1.jpg=图1 2.jpg=图2 3.jpg=图3
        for slot_name, col_name in [('0', 'AI白底图'), ('1', '图1'), ('2', '图2'), ('3', '图3')]:
            attachments = fields.get(col_name)
            if not attachments:
                continue
            # 飞书附件字段返回列表，取第一个
            if isinstance(attachments, list) and attachments:
                ft = attachments[0].get('file_token', '')
            else:
                continue
            if not ft:
                continue

            dest_path = os.path.join(dest_dir, f'{slot_name}.jpg')
            success   = _feishu_download_file(ft, token, dest_path, table_id=table_id)
            if success:
                print(f'  ✓ {prod_folder}/{color}/{slot_name}.jpg')
                ok += 1
            else:
                fail += 1

    print(f'\n下载完成：成功 {ok} 张，失败 {fail} 张，跳过 {skip} 行（无文件夹/颜色）')


# ── nano banana 图生图 ────────────────────────────────────────────────────────

NANOBANANA_API_KEY    = 'Em5EIwRxsz0UwpUUYrNtwngKvb'
NANOBANANA_SUBMIT_URL = 'https://api.wuyinkeji.com/api/async/image_nanoBanana2'
NANOBANANA_DETAIL_URL = 'https://api.wuyinkeji.com/api/async/detail'


def _feishu_update_record(token, app_token, table_id, record_id, fields):
    """PATCH 更新飞书多维表格单条记录"""
    url = (f"https://open.feishu.cn/open-apis/bitable/v1"
           f"/apps/{app_token}/tables/{table_id}/records/{record_id}")
    payload = json.dumps({'fields': fields}).encode('utf-8')
    req = urllib.request.Request(
        url, data=payload,
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        },
        method='PUT'
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode('utf-8'))
    if data.get('code') != 0:
        raise Exception(f"更新记录失败: {data.get('msg')}")
    return data


def _feishu_upload_url_image(url, token, app_token):
    """下载任意 URL 图片并上传到飞书，返回 file_token；失败返回 None"""
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            img_data = r.read()
    except Exception as e:
        print(f"    图片下载失败: {e}")
        return None

    fname = url.split('/')[-1].split('?')[0] or 'image.jpg'
    if '.' not in fname:
        fname += '.jpg'

    boundary = b'----FeishuUploadBoundary'

    def _field(name, value):
        return (b'--' + boundary + b'\r\n'
                + b'Content-Disposition: form-data; name="' + name.encode() + b'"\r\n\r\n'
                + value.encode() + b'\r\n')

    body = (
        _field('file_name', fname) +
        _field('parent_type', 'bitable_image') +
        _field('parent_node', app_token) +
        _field('size', str(len(img_data))) +
        b'--' + boundary + b'\r\n'
        b'Content-Disposition: form-data; name="file"; filename="' + fname.encode() + b'"\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' +
        img_data + b'\r\n' +
        b'--' + boundary + b'--\r\n'
    )
    upload_req = urllib.request.Request(
        'https://open.feishu.cn/open-apis/drive/v1/medias/upload_all',
        data=body,
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'multipart/form-data; boundary=----FeishuUploadBoundary',
        }
    )
    try:
        with urllib.request.urlopen(upload_req, timeout=30) as r:
            resp = json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"    飞书上传失败 {e.code}: {e.read().decode('utf-8', errors='replace')[:200]}")
        return None
    if resp.get('code') != 0:
        print(f"    飞书上传失败: {resp.get('msg')}")
        return None
    return resp['data']['file_token']


def _nanobanana_submit(img_url, prompt='', size='1344x1792', aspect_ratio='3:4'):
    """提交 nano banana 图生图任务，返回 task_key；失败返回 None"""
    payload = json.dumps({
        'key':         NANOBANANA_API_KEY,
        'prompt':      prompt,
        'size':        size,
        'aspectRatio': aspect_ratio,
        'urls':        [img_url],
    }).encode('utf-8')
    req = urllib.request.Request(
        NANOBANANA_SUBMIT_URL, data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode('utf-8'))
    except Exception as e:
        print(f"    提交失败: {e}")
        return None
    print(f"    提交响应: {data}")
    task_key = (data.get('data') or {}).get('id')
    if not task_key:
        print(f"    提交失败: 无 task_key（服务器返回 {data.get('code')} {data.get('msg', '')}）")
        return None
    return task_key


def _nanobanana_poll(task_id, max_wait=180):
    """轮询 nano banana 任务结果。
    返回：
      - 成功：结果图片 URL 列表
      - 任务失败：None
      - 超时：[]
    status: 0=排队中 1=处理中 2=完成 3=失败
    """
    url = f"{NANOBANANA_DETAIL_URL}?key={NANOBANANA_API_KEY}&id={task_id}"
    for attempt in range(max_wait // 5):
        time.sleep(5)
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                data = json.loads(r.read().decode('utf-8'))
        except Exception as e:
            print(f"    轮询异常: {e}")
            continue
        out    = data.get('data') or {}
        status = out.get('status')
        if status == 2:
            imgs = out.get('result') or []
            if isinstance(imgs, str):
                imgs = [imgs]
            return [u for u in imgs if u]
        if status == 3:
            print(f"    任务失败: {out.get('message', '')}")
            return None
        print(f"    等待中... ({(attempt + 1) * 5}s, status={status})")
    print(f"    超时（{max_wait}s）未完成")
    return []


def stage_nanobanana_process(token, app_token,
                              table_id=SKU_IMG_TABLE_ID,
                              prompt='纯白底，仅商品本身，无模特，无人体（无手、无脚、无任何身体部位）。平铺拍摄，影棚照明，干净产品图，高分辨率。保留扣子和拉链等所有结构性细节，去掉腰带及任何可拆卸配饰。服装表面平整，只允许服装自身结构产生的自然褶皱（如裤裆、膝盖处），禁止出现因折叠或堆放产生的杂乱压痕。禁止出现任何品牌商标、标签、logo、品牌文字或图案，背景色纯白#FFFFFF。',
                              size='1344x1792',
                              aspect_ratio='3:4',
                              force=False,
                              max_concurrency=20):
    """
    读取图生图处理表中有 原始图链接 但 AI白底图 为空的行，
    调用 nano banana 图生图，把结果图片写回 AI白底图 字段。
    """
    TASKS_FILE = os.path.join(DATA_DIR, 'nanobanana_tasks.json')

    def _load_tasks():
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_tasks(tasks):
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)

    print(f"\n=== nano banana 图生图处理 ===")
    records = _feishu_list_records(token, app_token, table_id)

    to_process = [
        {
            'record_id': rec['record_id'],
            'offer_id': rec.get('fields', {}).get('offer_id', ''),
            'color': rec.get('fields', {}).get('颜色', ''),
            'img_url': rec.get('fields', {}).get('原始图链接', ''),
        }
        for rec in records
        if rec.get('fields', {}).get('原始图链接')
        and (force or not rec.get('fields', {}).get('AI白底图'))
    ]

    max_workers = max(1, int(max_concurrency or 1))
    print(f"  待处理: {len(to_process)} 行（有原始图链接{'，强制重处理' if force else '且AI白底图为空'}）")
    print(f"  并发数: {max_workers}")

    saved_tasks = _load_tasks()
    tasks_lock = threading.Lock()

    def _process_one(i, total, item):
        rid = item['record_id']
        print(f"\n  [{i}/{total}] {item['offer_id']} - {item['color']}")

        with tasks_lock:
            task_key = saved_tasks.get(rid)
        if task_key:
            print(f"    复用已提交 task_key: {task_key}")
        else:
            task_key = _nanobanana_submit(item['img_url'], prompt, size, aspect_ratio)
            if not task_key:
                print(f"    跳过（提交失败）")
                return False
            print(f"    task_key: {task_key}")
            with tasks_lock:
                saved_tasks[rid] = task_key
                _save_tasks(saved_tasks)

        timeout_retry = 0
        result_urls = None
        while True:
            polled = _nanobanana_poll(task_key)

            if polled is None:
                _feishu_update_record(token, app_token, table_id, rid, {'状态': '失败'})
                with tasks_lock:
                    saved_tasks.pop(rid, None)
                    _save_tasks(saved_tasks)
                return False

            if polled:
                result_urls = polled
                break

            timeout_retry += 1
            with tasks_lock:
                saved_tasks.pop(rid, None)
                _save_tasks(saved_tasks)

            if timeout_retry > 3:
                try:
                    _feishu_update_record(token, app_token, table_id, rid, {'状态': '超时'})
                except Exception:
                    pass
                print(f"    超时失败：{item['offer_id']} - {item['color']}（已重提3次）")
                return False

            print(f"    超时，准备第 {timeout_retry} 次重新提交...")
            task_key = _nanobanana_submit(item['img_url'], prompt, size, aspect_ratio)
            if not task_key:
                print(f"    重新提交失败：{item['offer_id']} - {item['color']}")
                return False
            print(f"    新 task_key: {task_key}")
            with tasks_lock:
                saved_tasks[rid] = task_key
                _save_tasks(saved_tasks)

        print(f"    结果URL: {result_urls[0][:80]}...")

        ft = _feishu_upload_url_image(result_urls[0], token, app_token)
        if not ft:
            with tasks_lock:
                saved_tasks.pop(rid, None)
                _save_tasks(saved_tasks)
            return False

        _feishu_update_record(token, app_token, table_id, rid, {
            'AI白底图': [{'file_token': ft}],
            'AI白底图链接': result_urls[0],
            '图3': [{'file_token': ft}],
            '状态': '完成',
        })
        print(f"    写回 AI白底图/图3 成功")
        with tasks_lock:
            saved_tasks.pop(rid, None)
            _save_tasks(saved_tasks)
        return True

    ok = fail = 0
    if to_process:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(_process_one, i, len(to_process), item)
                for i, item in enumerate(to_process, 1)
            ]
            for future in as_completed(futures):
                try:
                    if future.result():
                        ok += 1
                    else:
                        fail += 1
                except Exception as e:
                    print(f"    并发任务异常: {e}")
                    fail += 1

    print(f"\n=== 完成：成功 {ok} 行，失败 {fail} 行 ===")


def stage_fill_main_images(details, token, app_token,
                           table_id=SKU_IMG_TABLE_ID):
    """
    为图生图处理表中缺少 图2/图3 的行补填商品主图。
    通过 原始图链接（色块图URL）反查对应商品的主图。
    details: 已加载的 details_raw 列表
    """
    print(f"\n=== 补填主图（图2/图3）===")

    # 建 色块图URL → 主图URL列表 的索引（图3用）
    color_url_to_main = {}
    for product in details:
        main_urls = [img.get('full_path_image_u_r_i', '')
                     for img in product.get('main_images', [])[:1]
                     if img.get('full_path_image_u_r_i')]
        skus = product.get('wholesale_skus', {}) or {}
        for prop in skus.get('sku_props', []):
            if prop.get('prop') in ('颜色', 'Color', 'color'):
                for v in prop.get('value', []):
                    if v.get('image_url'):
                        color_url_to_main[v['image_url']] = main_urls

    records = _feishu_list_records(token, app_token, table_id)
    to_fill = [
        {
            'record_id':    rec['record_id'],
            'prod_no':      str(rec.get('fields', {}).get('offer_id', '')),
            'orig_url':     str(rec.get('fields', {}).get('原始图链接', '')),
            'orig_ft':      (rec.get('fields', {}).get('原始图') or [{}])[0].get('file_token', ''),
            'has_图2':      bool(rec.get('fields', {}).get('图2')),
            'has_图3':      bool(rec.get('fields', {}).get('图3')),
        }
        for rec in records
        if not rec.get('fields', {}).get('图2') or not rec.get('fields', {}).get('图3')
    ]

    print(f"  待补填: {len(to_fill)} 行")
    ok = fail = 0

    for item in to_fill:
        update = {}

        # 图2：直接复用原始图的 file_token，无需重新上传
        if not item['has_图2']:
            if item['orig_ft']:
                update['图2'] = [{'file_token': item['orig_ft']}]
            elif item['orig_url']:
                ft2 = _feishu_upload_image(item['orig_url'], token, app_token)
                if ft2:
                    update['图2'] = [{'file_token': ft2}]

        # 图3：商品主图第1张
        if not item['has_图3']:
            main_urls = color_url_to_main.get(item['orig_url'], [])
            if main_urls:
                ft3 = _feishu_upload_image(main_urls[0], token, app_token)
                if ft3:
                    update['图3'] = [{'file_token': ft3}]

        if update:
            _feishu_update_record(token, app_token, table_id, item['record_id'], update)
            print(f"  [OK] {item['prod_no']} 补填 {list(update.keys())}")
            ok += 1
        else:
            print(f"  [SKIP] {item['prod_no']} 无可填内容")
            fail += 1

    print(f"\n=== 完成：成功 {ok} 行，失败 {fail} 行 ===")


def stage_nanobanana_model_photo(token, app_token,
                                  table_id=SKU_IMG_TABLE_ID,
                                  prompt='',
                                  size='1344x1792',
                                  aspect_ratio='3:4',
                                  max_concurrency=20):
    """
    读取图生图处理表中有 AI白底图链接 但 图1 为空的行，
    调用 nano banana 生成模特主图，写回 图1 字段。
    """
    TASKS_FILE = os.path.join(DATA_DIR, 'nanobanana_model_tasks.json')

    def _load_tasks():
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_tasks(tasks):
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)

    print(f"\n=== nano banana 模特主图生成 ===")
    records = _feishu_list_records(token, app_token, table_id)

    to_process = [
        {
            'record_id': rec['record_id'],
            'offer_id': rec.get('fields', {}).get('offer_id', ''),
            'color': rec.get('fields', {}).get('颜色', ''),
            'img_url': rec.get('fields', {}).get('AI白底图链接', ''),
            'title': str(rec.get('fields', {}).get('产品标题', '') or ''),
        }
        for rec in records
        if rec.get('fields', {}).get('AI白底图链接')
        and not rec.get('fields', {}).get('图1')
    ]

    # 根据标题关键词判断品类，动态补充款式描述到 prompt
    _GARMENT_KEYWORDS = [
        ('短裙', '短裙'),
        ('mini skirt', '短裙'),
        ('miniskirt', '短裙'),
        ('长裙', '长裙'),
        ('半身裙', '半身裙'),
        ('背带裙', '背带裙'),
        ('连衣裙', '连衣裙'),
        ('短裤', '短裤'),
        ('热裤', '短裤'),
        ('长裤', '长裤'),
        ('阔腿裤', '阔腿裤'),
        ('直筒裤', '长裤'),
    ]

    def _detect_garment(title):
        """从标题检测品类，返回中文款式名，用于注入 prompt。"""
        t = str(title or '').lower()
        for kw, label in _GARMENT_KEYWORDS:
            if kw.lower() in t:
                return label
        return ''

    def _build_model_prompt(base_prompt, title):
        """在 base_prompt 基础上插入品类限定语，避免 AI 生成错误款式。"""
        garment = _detect_garment(title)
        if not garment:
            return base_prompt
        inject = (
            f"【重要】本产品是{garment}，不是长裤也不是其他款式。"
            f"模特必须穿着图中展示的{garment}，裤脚/裙摆长度必须与原图完全一致，绝对不允许画成长裤或其他长度。"
        )
        return inject + '\n' + base_prompt

    max_workers = max(1, int(max_concurrency or 1))
    print(f"  待处理: {len(to_process)} 行（有AI白底图链接且图1为空）")
    print(f"  并发数: {max_workers}")

    saved_tasks = _load_tasks()
    tasks_lock = threading.Lock()

    def _process_one(i, total, item):
        rid = item['record_id']
        print(f"\n  [{i}/{total}] {item['offer_id']} - {item['color']}")

        item_prompt = _build_model_prompt(prompt, item['title'])
        garment = _detect_garment(item['title'])
        if garment:
            print(f"    [品类识别] {garment} → 已注入款式限定")

        with tasks_lock:
            task_key = saved_tasks.get(rid)
        if task_key:
            print(f"    复用已提交 task_key: {task_key}")
        else:
            task_key = _nanobanana_submit(item['img_url'], item_prompt, size, aspect_ratio)
            if not task_key:
                print(f"    跳过（提交失败）")
                return False
            print(f"    task_key: {task_key}")
            with tasks_lock:
                saved_tasks[rid] = task_key
                _save_tasks(saved_tasks)

        timeout_retry = 0
        result_urls = None
        while True:
            polled = _nanobanana_poll(task_key)

            if polled is None:
                _feishu_update_record(token, app_token, table_id, rid, {'状态': '模特图失败'})
                with tasks_lock:
                    saved_tasks.pop(rid, None)
                    _save_tasks(saved_tasks)
                return False

            if polled:
                result_urls = polled
                break

            timeout_retry += 1
            with tasks_lock:
                saved_tasks.pop(rid, None)
                _save_tasks(saved_tasks)

            if timeout_retry > 3:
                try:
                    _feishu_update_record(token, app_token, table_id, rid, {'状态': '模特图超时'})
                except Exception:
                    pass
                print(f"    模特图超时失败：{item['offer_id']} - {item['color']}（已重提3次）")
                return False

            print(f"    超时，准备第 {timeout_retry} 次重新提交...")
            task_key = _nanobanana_submit(item['img_url'], prompt, size, aspect_ratio)
            if not task_key:
                print(f"    模特图重新提交失败：{item['offer_id']} - {item['color']}")
                return False
            print(f"    新 task_key: {task_key}")
            with tasks_lock:
                saved_tasks[rid] = task_key
                _save_tasks(saved_tasks)

        print(f"    结果URL: {result_urls[0][:80]}...")

        ft = _feishu_upload_url_image(result_urls[0], token, app_token)
        if not ft:
            with tasks_lock:
                saved_tasks.pop(rid, None)
                _save_tasks(saved_tasks)
            return False

        update_fields = {
            '图1': [{'file_token': ft}],
            '图1链接': result_urls[0],
            '状态': '模特图完成',
        }
        try:
            _feishu_update_record(token, app_token, table_id, rid, update_fields)
        except Exception:
            update_fields.pop('图1链接', None)
            _feishu_update_record(token, app_token, table_id, rid, update_fields)
            print(f"    [warn] 图1链接字段不存在，跳过（请在飞书图生图处理表添加「图1链接(文本)」列）")

        print(f"    写回 图1 成功")
        with tasks_lock:
            saved_tasks.pop(rid, None)
            _save_tasks(saved_tasks)
        return True

    ok = fail = 0
    if to_process:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(_process_one, i, len(to_process), item)
                for i, item in enumerate(to_process, 1)
            ]
            for future in as_completed(futures):
                try:
                    if future.result():
                        ok += 1
                    else:
                        fail += 1
                except Exception as e:
                    print(f"    并发任务异常: {e}")
                    fail += 1

    print(f"\n=== 完成：成功 {ok} 行，失败 {fail} 行 ===")


def _get_base_price(product):
    """获取商品基础价格（兼容 Apify 和 Onebound 两种数据格式）"""
    # 优先读 Onebound 解析时写入的 price_min
    try:
        p = float(product.get('price_min', 0) or 0)
        if p > 0:
            return p
    except Exception:
        pass
    # 兼容 Apify wholesale_price_model 格式
    try:
        price_model = product.get('wholesale_price_model', {}) or {}
        final = price_model.get('final_price_model', {}) or {}
        trade = final.get('trade_without_promotion', {}) or {}
        price_str = trade.get('offer_min_price', '0')
        return float(price_str)
    except Exception:
        return 0.0

def _lookup_price(sku_info, color, size, product):
    """从 sku_info_map 查找对应 SKU 价格"""
    if not sku_info:
        return _get_base_price(product)

    size_variants = _size_match_variants(size)

    # 逐条匹配 spec_attrs
    for sku in sku_info.values():
        spec = html.unescape(sku.get('spec_attrs', ''))

        if color and size:
            matched = color in spec and any(v and v in spec for v in size_variants)
        elif color:
            matched = color in spec
        elif size:
            matched = any(v and v in spec for v in size_variants)
        else:
            matched = True

        if matched:
            price = float(sku.get('price', 0))
            if price > 0:
                return price
            # SKU 匹配但无 price 字段，回退到商品基础价
            return _get_base_price(product)

    return _get_base_price(product)


def _lookup_weight(sku_info, weight_scale_info, color, size, default=500):
    """从 piece_weight_scale_info 查找对应 SKU 重量（克）；找不到取均值，再回退 default"""
    if not weight_scale_info:
        return default

    # 建 sku_id → weight 映射
    id_weight = {str(item['sku_id']): item.get('weight', default)
                 for item in weight_scale_info if item.get('sku_id')}
    if not id_weight:
        return default

    size_variants = _size_match_variants(size)

    # 精确匹配：从 sku_info_map 找 sku_id
    for sku_id_str, sku in (sku_info or {}).items():
        spec = html.unescape(sku.get('spec_attrs', ''))
        if color and size:
            matched = color in spec and any(v and v in spec for v in size_variants)
        elif color:
            matched = color in spec
        elif size:
            matched = any(v and v in spec for v in size_variants)
        else:
            matched = True
        if matched and sku_id_str in id_weight:
            return id_weight[sku_id_str]

    # 无精确匹配，取所有 SKU 重量均值
    return round(sum(id_weight.values()) / len(id_weight))



def _write_dxm_row(ws, row, offer_id, title, main_img_str, detail_url,
                   description, attr_name1, attr_val1, attr_name2, attr_val2,
                   sku_img, declare_price, platform_sku, is_first, weight_g=500):
    first_main_img = main_img_str.split('\n')[0] if main_img_str else ''
    col_map = {
        '*产品标题':            title,
        '*英文标题':            '',
        '产品描述':             description if is_first else '',
        '产品货号':             offer_id,
        '*变种属性名称一':       attr_name1,
        '*变种属性值一':         attr_val1,
        '变种属性名称二':        attr_name2 if attr_name2 else None,
        '变种属性值二':          attr_val2 if attr_val2 else None,
        '预览图':               sku_img if sku_img else first_main_img,
        '*申报价格\n(店铺币种)': declare_price,
        'SKU货号':              platform_sku,
        '*长（cm）':            PKG_LENGTH,
        '*宽（cm）':            PKG_WIDTH,
        '*高（cm）':            PKG_HEIGHT,
        '*重量（g）':           weight_g,
        # 识别码类型/识别码：无值时留真空单元格，不填空字符串
        '站外产品链接':          detail_url if is_first else None,
        '*轮播图':              main_img_str,        # 每行都填，换行符分隔多图
        '*产品素材图':           first_main_img,      # 每行都填，只取第1张
        '建议售价（USD）':      RETAIL_USD,
        '库存':                 999,
        '发货时效（天）':        9,
    }
    for col, header in enumerate(DXM_HEADERS):
        val = col_map.get(header, None)
        if val is not None:
            ws.write(row, col, val)

# ── 主入口 ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  1688 → 店小秘 采集流水线")
    print("=" * 60)

    # 用户输入
    kw_input = input("\n请输入采集关键词（多个用逗号分隔，回车使用默认）: ").strip()
    if kw_input:
        keywords = [k.strip() for k in kw_input.split(',') if k.strip()]
    else:
        keywords = CONFIG.get('default_keywords', ['高腰牛仔裤女'])

    total_str = input("请输入采集总数量（回车默认50）: ").strip()
    total_limit = int(total_str) if total_str.isdigit() else 50

    bl_input = input("请输入黑名单词（多个用逗号分隔，回车跳过）: ").strip()
    blacklist = [w.strip() for w in bl_input.split(',') if w.strip()] if bl_input else []

    price_str = input("请输入采购价上限（回车不限制）: ").strip()
    max_price = float(price_str) if price_str.replace('.', '', 1).isdigit() else None

    max_per_kw = -(-total_limit // len(keywords))  # 向上取整，多关键词时均摊

    print(f"\n配置确认:")
    print(f"  关键词: {keywords}")
    print(f"  采集总数: {total_limit}")
    print(f"  黑名单: {blacklist}")
    print(f"  采购价上限: ¥{max_price}" if max_price else "  采购价上限: 不限制")

    # 飞书初始化（提前授权，失败早发现）
    token     = _feishu_token()
    app_token = _feishu_resolve_wiki(token)
    print(f"  飞书授权成功")

    # 第一阶段
    offer_ids, offers_info = stage1_search(keywords, max_per_keyword=max_per_kw)
    if not offer_ids:
        print("未获取到任何商品，退出")
        return

    # 去重过滤
    history = load_collected()
    before = len(offer_ids)
    offer_ids = [oid for oid in offer_ids if oid not in history]
    skipped = before - len(offer_ids)
    if skipped:
        print(f"\n去重过滤：跳过已采集 {skipped} 条，剩余 {len(offer_ids)} 条")
    if not offer_ids:
        print("所有搜索结果均已采集过，退出")
        return

    # 价格过滤（price=0 表示读取失败，放行不过滤）
    if max_price is not None:
        before_price = len(offer_ids)
        offer_ids = [oid for oid in offer_ids
                     if _get_search_price(offers_info.get(oid, {})) <= max_price]
        skipped_price = before_price - len(offer_ids)
        if skipped_price:
            print(f"价格过滤：跳过超过 ¥{max_price} 的商品 {skipped_price} 条，剩余 {len(offer_ids)} 条")
        if not offer_ids:
            print("过滤后无剩余商品，退出")
            return

    # 第四阶段：推搜索结果到飞书表1
    stage4_push_review(offer_ids, offers_info, token, app_token)

    # 等待用户在飞书勾选（循环直到有勾选为止）
    while True:
        input("\n请在飞书「上传预览表」中勾选「选中采集」，完成后按回车继续...")
        offer_ids, _ = stage5_read_selected(token, app_token)
        if offer_ids:
            break
        print("  还没有勾选任何商品，请在飞书表中勾选后再按回车")

    # 用 offers_info 里的 devcake 中文标题做 fallback
    search_titles = {}
    for oid in offer_ids:
        item = offers_info.get(oid, {})
        t = item.get('title', '')
        try:
            t = t.encode('latin1').decode('utf-8')
        except Exception:
            pass
        search_titles[oid] = t

    # 第二阶段：抓详情
    details = stage2_details(offer_ids, total_limit)
    if not details:
        print("未获取到详情数据，退出")
        return

    # 详情价格二次过滤（过滤掉实际采购价超标的商品）
    if max_price is not None:
        before = len(details)
        details = [p for p in details if _get_base_price(p) <= max_price]
        dropped = before - len(details)
        if dropped:
            print(f"详情价格过滤：移除超过 ¥{max_price} 的商品 {dropped} 条，剩余 {len(details)} 条")
        if not details:
            print("过滤后无剩余商品，退出")
            return

    # 统一分配产品主编号（stage6 飞书表 和 stage3 XLS 使用同一套编号）
    detail_offer_ids = [str(p.get('id', '')) for p in details if p.get('id')]
    prod_no_map = assign_product_numbers(detail_offer_ids)

    # 第六阶段：推店小秘格式到表2
    stage6_push_dianxiaomi(details, blacklist, token, app_token,
                            search_titles=search_titles, prod_no_map=prod_no_map)

    # 可选：图生图流程（推表后、RPA前）
    run_nanobanana = input("\n是否执行图生图流程？(y/n，默认y): ").strip().lower()
    if run_nanobanana != 'n':
        _menu_run('test_nanobanana.py')
    else:
        print('已跳过图生图流程。')

    # 第三阶段：生成本地 XLS（备用）
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = os.path.join(DATA_DIR, f'dianxiaomi_import_{ts}.xls')
    stage3_generate_xls(details, blacklist, output_path, prod_no_map=prod_no_map)

    # 下载 SKU 图片，按文件夹整理供 RPA 使用
    stage_download_sku_images(details, blacklist, prod_no_map=prod_no_map)

    # 写入采集历史（去重用）
    mark_collected(offer_ids, offers_info)

    print("\n全部完成！")
    print(f"  飞书表2已更新（店小秘格式）")
    print(f"  本地备份: {output_path}")

    start_rpa = input("\n是否开始RPA上传？(y/n，默认n): ").strip().lower()
    if start_rpa == 'y':
        _menu_run('rpa_upload.py', ['--import'])
    else:
        print('已跳过RPA上传。')



def _menu_run(script, args=None):
    """运行同目录脚本并直通输出"""
    if args is None:
        args = []
    cmd = [sys.executable, os.path.join(BASE_DIR, script), *args]
    print(f"\n>>> 执行: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, cwd=BASE_DIR, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[warn] 运行失败（exit={e.returncode}）: {script}")


def quick_menu():
    """快捷指令菜单：按数字执行流水线步骤"""
    actions = {
        '1': ('全流程采集（pipeline.py）', lambda: main()),
        '2': ('阶段2~6+图生图（读勾选→详情→推飞书→AI白底图→图1→导出）', lambda: _menu_run('test_stage2_6.py')),
        '3': ('图生图：阶段一+阶段二', lambda: _menu_run('test_nanobanana.py')),
        '4': ('仅阶段二（生成模特图）', lambda: _menu_run('run_model_photo.py')),
        '5': ('从飞书下载SKU图（0/1/2/3）', lambda: _menu_run('test_sku_feishu.py', ['download'])),
        '6': ('导出店小秘xlsx', lambda: _menu_run('export_miaoshou_xlsx.py')),
        '7': ('店小秘导入+RPA上图', lambda: _menu_run('rpa_upload.py', ['--import'])),
        '8': ('仅RPA上图（不导入xlsx）', lambda: _menu_run('rpa_upload.py')),
        'q': ('退出', None),
    }

    print('=' * 60)
    print('  店小秘采集流水线快捷菜单')
    print('=' * 60)
    for key in ['1', '2', '3', '4', '5', '6', '7', '8', 'q']:
        print(f"  {key}. {actions[key][0]}")

    while True:
        choice = input('\n请输入步骤编号: ').strip().lower()
        if choice in ('', '1'):
            choice = '1'
        if choice not in actions:
            print('无效编号，请重新输入')
            continue
        if choice == 'q':
            print('已退出')
            return

        print(f"\n已选择: {actions[choice][0]}")
        actions[choice][1]()
        return

if __name__ == '__main__':
    # 默认进入快捷菜单；如需直接跑原始全流程可用: python pipeline.py --full
    if len(sys.argv) > 1 and sys.argv[1] == '--full':
        main()
    else:
        quick_menu()
