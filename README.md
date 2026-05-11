# 上货助手

本项目从 `prototype/上货助手原型.html` 落地为可运行版本。

## 当前版本

- FastAPI 后端
- SQLite 本地数据库
- 商品库 CRUD
- 商品库单主图上传与展示
- 真实采集/文件导入、勾选入库、商品处理预览
- 店小秘导入表导出与本地上货任务记录
- 发布记录、缺图检查、运行日志查看
- API、提示词、运行设置管理
- 商品库仪表盘、缺图检测
- 上货预检、真实 RPA 安全阻断、导出表格下载
- 商品处理字段编辑：英文标题、颜色尺码、SKU、申报价、重量尺寸、库存、发货时效、站外链接
- 每个上货任务生成日志和 manifest JSON，便于复盘本次导出商品快照
- 商品采集页支持配置关键词、来源、数量、价格区间、黑名单，并执行 1688 / 万邦 API 真实采集
- 采集结果页支持下载导入模板，并从 CSV/XLSX 导入外部采集候选商品
- 采集任务仅保留 1688 / 万邦 API；真实采集凭据缺失时明确阻断并记录原因
- 采集页提供采集器预检，统一检查万邦 API、1688 Cookie 的就绪状态
- 1688 / 万邦 API 采集会在创建任务后自动执行，不再需要人工确认
- 外部采集任务支持从 JSON/CSV/XLSX 回填结果，回填后进入采集结果候选池
- 外部采集任务支持从 JSON/CSV/XLSX 回填结果，回填后进入采集结果候选池
- 采集候选支持按来源、状态、价格、销量排序筛选，并支持批量跳过/删除
- 候选导入和采集写入会按 `source_url` 或 `source + title` 去重
- 内置 `scripts/smoke_test.py` 冒烟测试，覆盖采集禁用模拟、入库、补图、处理、导出、JSON 回填
- `/api/system/status` 可查看数据库、图片目录、RPA、采集器和预检状态
- 商品库支持批量改状态、批量删除
- 上货任务支持单任务删除、清空全部任务与发布记录
- 发布记录支持按结果和关键词筛选
- 商品处理支持本地安全标题生成；未配置 DeepSeek Key 时不会联网，使用本地标题 stub
- 商品库支持 Nano Banana 图生图任务：提交后保存 task_id，查询完成后下载处理图到本地；未配置 Key 时明确阻断
- 设置中心新增系统诊断面板，展示数据库、图片目录、RPA、采集、上货预检状态
- 系统诊断面板现在提供可用/需处理 checklist 和具体操作建议
- 前端核心加载请求统一错误提示，避免接口失败时静默无反馈

## 安全默认值

- `enable_real_rpa=false` 默认阻断真实 RPA 上货，避免误操作。
- 商品库只展示/保留 1 张主图；采集、上传等其它流程仍可保留多图规则。
- 本地占位主图和本地模拟采集已移除；缺图商品必须上传真实商品图或使用供应商图片。
- 万邦 Key/Secret、1688 Cookie 未配置时，不会伪造真实采集结果，会明确阻断并提示缺少的配置。
- 1688 Cookie 采集会使用本地 Cookie 文件请求 1688 搜索页；Cookie 失效/风控时会失败并提示重新导出 Cookie。

## 当前闭环

1. 在商品采集页配置关键词、价格区间、黑名单并开始 1688 / 万邦 API 真实采集。
2. 或在采集结果页下载模板，把外部采集结果 CSV/XLSX/JSON 导入候选商品。
3. 在采集结果页勾选候选商品加入商品库。
4. 上传真实主图或使用采集到的供应商图片。
5. 在商品处理页检查导出字段。
6. 必要时编辑商品处理字段，保存后会影响后续导出表。
7. 生成店小秘导入表并下载 `.xlsx`。
8. 创建上货任务；真实 RPA 仍受安全开关保护。
9. 在任务列表打开 Log，查看运行日志和 manifest 商品快照。

## 外部采集回填

- 1688 外部任务会先生成请求快照，并自动执行万邦 API 或 1688 Cookie 采集。
- 你可以在外部工具执行后，把结果 JSON/CSV/XLSX 通过“回填结果”导回对应采集任务。
- JSON 支持数组、`items`、`data`、`results` 等常见结构；字段优先识别 `title`、`url`、`image_url`、`price`、`sales`、`image_count`。

## 启动

```powershell
cd D:\projects\upload-assistant
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

打开：http://127.0.0.1:8000

## 本地客户端打包

Windows 本地打包为普通用户可双击运行的客户端目录：

```powershell
cd D:\projects\upload-assistant
.\scripts\package_backend.ps1 -Clean
```

打包产物：

- 可分发目录：`dist\upload-assistant-backend`
- 可分发压缩包：`release\upload-assistant-local-client.zip`

启动方式：双击 `dist\upload-assistant-backend\启动上货助手.bat`

说明：

- 打包程序会内置 `frontend/` 静态页面。
- 运行数据写在 exe 同级 `data/`，包括数据库、图片、采集结果、导出表和日志。
- 重复双击不会重复启动后台；如果 `127.0.0.1:8000` 已有本应用，会直接打开页面。
- 如果 8000 端口被其他程序占用，后台会自动尝试 8001-8019。
- 需要真实店小秘 RPA 时，再双击 `启动上货执行器.bat`。
- 可用环境变量覆盖：`UPLOAD_ASSISTANT_HOST`、`UPLOAD_ASSISTANT_PORT`、`UPLOAD_ASSISTANT_DATA_DIR`、`UPLOAD_ASSISTANT_DB`、`UPLOAD_ASSISTANT_OPEN_BROWSER`。
- 页面提供“清理本地数据”，默认清理 7 天前成功任务的旧导出/旧日志/成功商品图片，失败商品不自动清理。
