from __future__ import annotations

import os
import base64
import json
import csv
import mimetypes
import re
import shutil
import subprocess
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html import escape, unescape
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import Body, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openpyxl import Workbook, load_workbook

def resolve_resource_dir() -> Path:
    frozen_base = getattr(sys, "_MEIPASS", None)
    if frozen_base:
        return Path(frozen_base)
    return Path(__file__).resolve().parents[2]


def resolve_runtime_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[2]


RESOURCE_DIR = resolve_resource_dir()
BASE_DIR = resolve_runtime_dir()
DATA_DIR = Path(os.environ.get("UPLOAD_ASSISTANT_DATA_DIR", BASE_DIR / "data"))
IMAGE_DIR = DATA_DIR / "images"
DB_PATH = Path(os.environ.get("UPLOAD_ASSISTANT_DB", DATA_DIR / "app.db"))
FRONTEND_DIR = RESOURCE_DIR / "frontend"
STATIC_DIR = FRONTEND_DIR / "static"
SCRIPT_SOURCE_DIR = Path(r"C:\Users\zyf\.accio\accounts\1753260534\agents\MID-27260534U1775454-06F6F0-2183-EB2CBD\project")
NANOBANANA_SUBMIT_URL = "https://api.wuyinkeji.com/api/async/image_nanoBanana2"
NANOBANANA_DETAIL_URL = "https://api.wuyinkeji.com/api/async/detail"
DEFAULT_IMAGE_PROMPT = "纯白底，仅商品本身，无模特，无人体部位。平铺拍摄，影棚照明，干净产品图，高分辨率。保留商品结构细节，去掉腰带及可拆卸配饰。背景色纯白#FFFFFF。"
VISION_CACHE_VERSION = "doubao-color-v2"

COLOR_ALIAS_ENTRIES = [
    ("black", "Black"),
    ("\u9ed1", "Black"),
    ("\u9ed1\u8272", "Black"),
    ("\u7eaf\u9ed1", "Black"),
    ("blk", "Black"),
    ("white", "White"),
    ("\u767d", "White"),
    ("\u767d\u8272", "White"),
    ("\u7eaf\u767d", "White"),
    ("ivory", "White"),
    ("\u7c73\u767d", "White"),
    ("\u8c61\u7259\u767d", "White"),
    ("beige", "Beige"),
    ("\u7c73\u8272", "Beige"),
    ("\u674f\u8272", "Beige"),
    ("\u674f", "Beige"),
    ("apricot", "Beige"),
    ("cream", "Beige"),
    ("\u5976\u6cb9\u8272", "Beige"),
    ("khaki", "Khaki"),
    ("\u5361\u5176", "Khaki"),
    ("\u5361\u5176\u8272", "Khaki"),
    ("camel", "Khaki"),
    ("\u9a7c\u8272", "Khaki"),
    ("brown", "Brown"),
    ("\u68d5\u8272", "Brown"),
    ("\u68d5", "Brown"),
    ("\u5496\u5561\u8272", "Brown"),
    ("coffee", "Brown"),
    ("chocolate", "Brown"),
    ("\u5de7\u514b\u529b\u8272", "Brown"),
    ("gray", "Grey"),
    ("grey", "Grey"),
    ("\u7070", "Grey"),
    ("\u7070\u8272", "Grey"),
    ("lightgray", "Grey"),
    ("\u6d45\u7070", "Grey"),
    ("darkgray", "Grey"),
    ("\u6df1\u7070", "Grey"),
    ("silvergray", "Grey"),
    ("red", "Red"),
    ("\u7ea2", "Red"),
    ("\u7ea2\u8272", "Red"),
    ("winered", "Red"),
    ("\u9152\u7ea2", "Red"),
    ("burgundy", "Red"),
    ("\u67a3\u7ea2", "Red"),
    ("\u73ab\u7ea2", "Red"),
    ("rosered", "Red"),
    ("pink", "Pink"),
    ("\u7c89", "Pink"),
    ("\u7c89\u8272", "Pink"),
    ("\u6d45\u7c89", "Pink"),
    ("\u85d5\u7c89", "Pink"),
    ("hotpink", "Pink"),
    ("\u6843\u7ea2", "Pink"),
    ("orange", "Orange"),
    ("\u6a59", "Orange"),
    ("\u6a59\u8272", "Orange"),
    ("\u6854\u8272", "Orange"),
    ("yellow", "Yellow"),
    ("\u9ec4", "Yellow"),
    ("\u9ec4\u8272", "Yellow"),
    ("\u59dc\u9ec4", "Yellow"),
    ("\u660e\u9ec4", "Yellow"),
    ("gold", "Gold"),
    ("\u91d1\u8272", "Gold"),
    ("\u91d1", "Gold"),
    ("green", "Green"),
    ("\u7eff", "Green"),
    ("\u7eff\u8272", "Green"),
    ("armygreen", "Green"),
    ("\u519b\u7eff", "Green"),
    ("olive", "Green"),
    ("\u6a44\u6984\u7eff", "Green"),
    ("mintgreen", "Green"),
    ("\u8584\u8377\u7eff", "Green"),
    ("\u58a8\u7eff", "Green"),
    ("\u6d45\u7eff", "Green"),
    ("\u6df1\u7eff", "Green"),
    ("blue", "Blue"),
    ("\u84dd", "Blue"),
    ("\u84dd\u8272", "Blue"),
    ("navy", "Blue"),
    ("navyblue", "Blue"),
    ("\u85cf\u9752", "Blue"),
    ("\u85cf\u84dd", "Blue"),
    ("\u6df1\u84dd", "Blue"),
    ("skyblue", "Blue"),
    ("\u5929\u84dd", "Blue"),
    ("lightblue", "Blue"),
    ("\u6d45\u84dd", "Blue"),
    ("denimblue", "Blue"),
    ("\u725b\u4ed4\u84dd", "Blue"),
    ("\u5b9d\u84dd", "Blue"),
    ("\u6e56\u84dd", "Blue"),
    ("purple", "Purple"),
    ("\u7d2b", "Purple"),
    ("\u7d2b\u8272", "Purple"),
    ("lavender", "Purple"),
    ("\u85b0\u8863\u8349\u7d2b", "Purple"),
    ("violet", "Purple"),
    ("\u6d45\u7d2b", "Purple"),
    ("\u6df1\u7d2b", "Purple"),
    ("silver", "Silver"),
    ("\u94f6\u8272", "Silver"),
    ("\u94f6", "Silver"),
    ("multi", "Multicolor"),
    ("multicolor", "Multicolor"),
    ("\u5f69\u8272", "Multicolor"),
    ("\u82b1\u8272", "Multicolor"),
    ("\u62fc\u8272", "Multicolor"),
    ("clear", "Clear"),
    ("\u900f\u660e", "Clear"),
]
MIAOSHOU_COLUMNS = [
    "*产品标题",
    "*英文标题",
    "产品描述",
    "产品货号",
    "*变种属性名称一",
    "*变种属性值一",
    "变种属性名称二",
    "变种属性值二",
    "预览图",
    "*申报价格\n(店铺币种)",
    "SKU货号",
    "*长（cm）",
    "*宽（cm）",
    "*高（cm）",
    "*重量（g）",
    "识别码类型",
    "识别码",
    "站外产品链接",
    "*轮播图",
    "*产品素材图",
    "外包装形状",
    "外包装类型",
    "外包装图片",
    "建议售价（USD）",
    "库存",
    "发货时效（天）",
]
RPA_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
RPA_ALLOWED_UPLOAD_SIZES = {"XS", "S", "M", "L", "XL", "XXL"}

DATA_DIR.mkdir(parents=True, exist_ok=True)
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="上货助手", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/images", StaticFiles(directory=IMAGE_DIR), name="images")


class Product(BaseModel):
    id: int
    title: str
    skc: str
    sku_summary: str
    main_image: Optional[str] = None
    purchase_price: float = 0
    first_mile: float = 0
    platform_cost: float = 0
    total_cost: float = 0
    estimated_profit: float = 0
    gross_margin: float = 0
    status: str
    created_at: str
    updated_at: str


class ProductPayload(BaseModel):
    title: str
    skc: str
    sku_summary: str = ""
    purchase_price: float = 0
    first_mile: float = 0
    platform_cost: float = 0
    status: str = "利润正常"



class CollectionItem(BaseModel):
    id: int
    title: str
    source: str
    source_url: str = ""
    price: float = 0
    sales: int = 0
    image_count: int = 0
    image_url: str = ""
    selected: bool = False
    status: str
    created_at: str


class CollectionItemPayload(BaseModel):
    title: str
    source: str = "1688"
    source_url: str = ""
    price: float = 0
    sales: int = 0
    image_count: int = 0
    image_url: str = ""


class CollectionTask(BaseModel):
    id: int
    keyword: str
    source: str = "1688"
    mode: str = "1688"
    collector: str = "1688_public_search"
    target_count: int = 10
    min_price: float = 0
    max_price: float = 0
    blacklist: str = ""
    status: str
    note: str = ""
    request_path: str = ""
    result_count: int = 0
    created_at: str
    updated_at: str


class CollectionTaskPayload(BaseModel):
    keyword: str
    source: str = "1688"
    mode: str = "1688"
    collector: str = "1688_public_search"
    target_count: int = 10
    min_price: float = 0
    max_price: float = 0
    blacklist: str = ""


class CollectionImportResult(BaseModel):
    imported_count: int
    skipped_count: int
    source: str
    filename: str


class CollectorCandidate(BaseModel):
    title: str
    source: str
    source_url: str = ""
    price: float = 0
    sales: int = 0
    image_count: int = 0
    image_url: str = ""


class CollectorRunResult(BaseModel):
    mode: str
    collector: str
    note: str = ""
    candidates: list[CollectorCandidate]


class ImportCollectionPayload(BaseModel):
    ids: list[int]


class CollectionBulkPayload(BaseModel):
    ids: list[int]


class ProductBulkStatusPayload(BaseModel):
    ids: list[int]
    status: str


class GenerateTitlePayload(BaseModel):
    product_id: int


class ProcessImagePayload(BaseModel):
    product_id: int
    source_image: str = ""


class ImageOption(BaseModel):
    label: str
    url: str
    kind: str = ""
    preview_url: str = ""
    color: str = ""
    size: str = ""
    sku_id: str = ""


class ColorImageAssignment(BaseModel):
    color: str
    image_url: str
    preview_url: str = ""
    source: str = ""
    sort_order: int = 0
    is_auto: bool = True
    confidence: float = 0


class DetailImageAssignment(BaseModel):
    image_url: str
    preview_url: str = ""
    source: str = ""
    sort_order: int = 0


class AutoAssignColorImagesPayload(BaseModel):
    product_id: int
    count_per_color: int = 3
    use_vision: bool = False
    user_confirmed_vision: bool = False


class ManualColorImageAssignmentPayload(BaseModel):
    product_id: int
    color: str
    slot_index: int
    image_url: str = ""


class ManualDetailImageAssignmentPayload(BaseModel):
    product_id: int
    slot_index: int
    image_url: str = ""


class DedupeProcessingImagesPayload(BaseModel):
    ids: list[int]


class DedupeProcessingImagesResult(BaseModel):
    product_count: int
    scanned_count: int
    removed_count: int
    detail_removed_count: int
    color_removed_count: int


class AutoAssignColorImagesResult(BaseModel):
    product_id: int
    count_per_color: int
    assigned_count: int
    colors: dict[str, int]


class ImageTask(BaseModel):
    id: int
    product_id: int
    provider: str
    task_id: str
    status: str
    source_image: str = ""
    result_url: str = ""
    local_path: str = ""
    prompt: str = ""
    note: str = ""
    created_at: str
    updated_at: str


class ProcessingItem(BaseModel):
    product_id: int
    title: str
    skc: str
    english_title: str
    color: str = ""
    size: str = ""
    sku_code: str
    declared_price: float = 0
    weight_g: int = 350
    length_cm: int = 15
    width_cm: int = 10
    height_cm: int = 2
    source_url: str = ""
    main_image: str = ""
    image_options: list[ImageOption] = []
    color_image_assignments: list[ColorImageAssignment] = []
    detail_image_assignments: list[DetailImageAssignment] = []
    detail_status: str = ""
    detail_note: str = ""
    image_status: str
    stock: int = 999
    ship_days: int = 9
    status: str


class ProcessingItemPayload(BaseModel):
    english_title: str = ""
    color: str = ""
    size: str = ""
    sku_code: str = ""
    declared_price: float = 0
    weight_g: int = 350
    length_cm: int = 15
    width_cm: int = 10
    height_cm: int = 2
    source_url: str = ""
    stock: int = 999
    ship_days: int = 9


class ProcessingBulkPayload(BaseModel):
    ids: list[int]
    fields: ProcessingItemPayload
    start_skc: str = ""


class UploadTask(BaseModel):
    id: int
    name: str
    status: str
    total_count: int = 0
    success_count: int = 0
    failed_count: int = 0
    export_path: str = ""
    run_log: str = ""
    created_at: str
    updated_at: str


class PublishRecord(BaseModel):
    id: int
    result: str
    skc: str
    title: str
    reason: str = ""
    created_at: str


class ApiConfig(BaseModel):
    key: str
    name: str
    enabled: bool = True
    base_url: str = ""
    model: str = ""
    api_key: str = ""
    usage: str = ""
    updated_at: str = ""


class AppSetting(BaseModel):
    key: str
    value: str
    updated_at: str = ""


class PromptTemplate(BaseModel):
    id: int
    name: str
    category: str = ""
    prompt_type: str = ""
    usage: str = ""
    content: str = ""
    status: str = "启用中"
    updated_at: str


class PromptTemplatePayload(BaseModel):
    name: str
    category: str = ""
    prompt_type: str = ""
    usage: str = ""
    content: str = ""
    status: str = "启用中"



def configured_script_dir() -> Path:
    configured = get_setting_value("script_dir", str(SCRIPT_SOURCE_DIR)).strip()
    return Path(configured) if configured else SCRIPT_SOURCE_DIR


def legacy_rpa_config() -> dict[str, object]:
    config_path = configured_script_dir() / "apify_config.json"
    if not config_path.exists():
        return {}
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def upload_image_source() -> str:
    configured = get_setting_value("upload_image_source", "").strip().lower()
    if configured in {"local", "cos"}:
        return configured
    legacy = str(legacy_rpa_config().get("image_source") or "local").strip().lower()
    return legacy if legacy in {"local", "cos"} else "local"


def cos_setting_value(key: str) -> str:
    configured = get_setting_value(key, "").strip()
    if configured:
        return configured
    legacy_key = key.removeprefix("cos_") if key.startswith("cos_") else key
    return str(legacy_rpa_config().get(key) or legacy_rpa_config().get(f"cos_{legacy_key}") or "").strip()


def cos_preflight() -> dict[str, object]:
    config = legacy_rpa_config()
    return {
        "image_source": upload_image_source(),
        "config_path": str(configured_script_dir() / "apify_config.json"),
        "config_exists": bool(config),
        "region": cos_setting_value("cos_region"),
        "bucket": cos_setting_value("cos_bucket"),
        "prefix": cos_setting_value("cos_prefix"),
        "secret_id_configured": bool(cos_setting_value("cos_secret_id")),
        "secret_key_configured": bool(cos_setting_value("cos_secret_key")),
    }


def upload_rpa_command(export_path: str) -> list[str]:
    command = ["python", "rpa_upload.py", "--import", export_path]
    if get_setting_value("upload_save_screenshots", "false").strip().lower() == "true":
        command.append("--debug-shots")
    for setting_key, cli_arg in [
        ("temu_shop_account", "--shop-account"),
        ("temu_site", "--site"),
        ("temu_product_template", "--product-template"),
        ("temu_size_template", "--size-template"),
        ("temu_warehouse_template", "--warehouse-template"),
        ("temu_logistics_template", "--logistics-template"),
    ]:
        value = get_setting_value(setting_key, "").strip()
        if value:
            command.extend([cli_arg, value])
    if get_setting_value("upload_auto_submit", "false").strip().lower() != "true":
        command.append("--no-publish")
    if upload_image_source() == "cos":
        command.extend(["--image-source", "cos"])
        for setting_key, cli_arg in [
            ("cos_region", "--cos-region"),
            ("cos_bucket", "--cos-bucket"),
            ("cos_prefix", "--cos-prefix"),
        ]:
            value = cos_setting_value(setting_key)
            if value:
                command.extend([cli_arg, value])
    return command


def display_upload_rpa_command(export_path: str) -> str:
    command = upload_rpa_command(export_path)
    redacted: list[str] = []
    skip_next = False
    for part in command:
        if skip_next:
            redacted.append("***")
            skip_next = False
            continue
        redacted.append(part)
    return " ".join(redacted)


def configured_rpa_sku_image_dir() -> Path:
    return configured_script_dir() / "data" / "sku_images"


DEFAULT_IMAGE_RECOGNITION_PROMPT = (
    "\u4f60\u662f\u7535\u5546\u5546\u54c1\u56fe\u7247\u989c\u8272\u8bc6\u522b\u52a9\u624b\uff0c"
    "\u53ea\u5224\u65ad\u56fe\u7247\u4e2d\u5546\u54c1\u4e3b\u4f53\u989c\u8272\uff0c"
    "\u4e0d\u8981\u53d7\u80cc\u666f\u3001\u6a21\u7279\u80a4\u8272\u3001\u6587\u5b57\u3001\u6c34\u5370\u5f71\u54cd\u3002\n\n"
    "\u5019\u9009\u989c\u8272 JSON\uff1a\n{color_json}\n\n"
    "\u4efb\u52a1\uff1a\n"
    "1. \u5224\u65ad\u56fe\u7247\u91cc\u7684\u5546\u54c1\u4e3b\u4f53\u6700\u63a5\u8fd1\u54ea\u4e2a\u5019\u9009\u989c\u8272\u3002\n"
    "2. matched_color \u5fc5\u987b\u4ece\u5019\u9009\u989c\u8272 JSON \u4e2d\u539f\u6837\u9009\u62e9\u4e00\u4e2a\u503c\u3002\n"
    "3. \u5982\u679c\u56fe\u7247\u4e0d\u662f\u5546\u54c1\u56fe\uff0cis_product_image=false\uff0cmatched_color=\"\"\u3002\n"
    "4. \u5982\u679c\u65e0\u6cd5\u5224\u65ad\u6216\u6ca1\u6709\u63a5\u8fd1\u989c\u8272\uff0cmatched_color=\"\"\u3002\n"
    "5. confidence \u8fd4\u56de 0 \u5230 1 \u7684\u6570\u5b57\u3002\n\n"
    "\u53ea\u8fd4\u56de\u4e00\u4e2a JSON \u5bf9\u8c61\uff0c\u4e0d\u8981\u8fd4\u56de\u89e3\u91ca\u6587\u5b57\uff0c"
    "\u4e0d\u8981\u4f7f\u7528 Markdown\u3002\n"
    "JSON \u5b57\u6bb5\u56fa\u5b9a\u4e3a\uff1amatched_color, confidence, is_product_image, reason\u3002"
)

DEFAULT_PROMPT_TEMPLATES = [
    ("Temu \u82f1\u6587\u6807\u9898\u751f\u6210", "\u5973\u88c5\u77ed\u88e4", "\u6807\u9898\u63d0\u793a\u8bcd", "\u6807\u9898\u751f\u6210", "\u6839\u636e\u5546\u54c1\u6807\u9898\u3001\u7c7b\u76ee\u3001\u989c\u8272\u548c\u5356\u70b9\u751f\u6210\u81ea\u7136\u51c6\u786e\u7684 Temu \u82f1\u6587\u6807\u9898\u3002", "\u542f\u7528\u4e2d"),
    ("\u725b\u4ed4\u77ed\u88e4\u4e3b\u56fe\u7cbe\u4fee", "\u5973\u88c5\u77ed\u88e4", "\u56fe\u751f\u56fe\u63d0\u793a\u8bcd", "\u4e3b\u56fe\u4f18\u5316", "\u4fdd\u7559\u5546\u54c1\u4e3b\u4f53\uff0c\u4f18\u5316\u5149\u7ebf\u3001\u8d28\u611f\u548c\u80cc\u666f\uff0c\u4e0d\u6539\u53d8\u5546\u54c1\u6b3e\u5f0f\u3002", "\u542f\u7528\u4e2d"),
    ("\u5546\u54c1\u989c\u8272\u56fe\u7247\u8bc6\u522b", "\u901a\u7528\u5546\u54c1", "\u56fe\u7247\u8bc6\u522b\u63d0\u793a\u8bcd", "\u989c\u8272\u5206\u56fe", DEFAULT_IMAGE_RECOGNITION_PROMPT, "\u542f\u7528\u4e2d"),
]


def looks_corrupted_text(value: str) -> bool:
    text = str(value or "")
    if not text:
        return False
    question_count = text.count("?")
    mojibake_markers = ["Ã", "Â", "Ð", "Ñ", "æ", "ç", "è", "é", "å", "¤", "½", "�"]
    return question_count >= max(3, len(text) // 3) or any(marker in text for marker in mojibake_markers)


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def product_from_row(row: sqlite3.Row) -> Product:
    return Product(**dict(row))


def collection_item_from_row(row: sqlite3.Row) -> CollectionItem:
    data = dict(row)
    data["selected"] = bool(data["selected"])
    return CollectionItem(**data)


def collection_task_from_row(row: sqlite3.Row) -> CollectionTask:
    return CollectionTask(**dict(row))


def collection_failure_note(provider: str, parsed_count: int, imported_count: int, skipped_count: int, base_note: str = "") -> str:
    prefix = f"{provider} 真实采集已执行，解析 {parsed_count} 条，写入 {imported_count} 条，跳过重复/无标题 {skipped_count} 条。"
    if imported_count > 0:
        return prefix
    if parsed_count <= 0:
        reason = "失败原因：接口没有返回商品，可能是关键词无结果、筛选条件过窄、API/Cookie 被限制，或平台页面结构变化。"
    elif skipped_count >= parsed_count:
        reason = "失败原因：解析到的商品全部被跳过，主要原因是重复商品或缺少标题，没有新增候选商品。"
    else:
        reason = "失败原因：本次没有写入新增候选商品，请检查关键词、价格区间、黑名单和采集来源配置。"
    return f"{prefix} {reason}"


def collection_empty_note(base_note: str, created_count: int, skipped_count: int, candidate_count: int) -> str:
    prefix = f"{base_note} 写入 {created_count} 条，跳过重复 {skipped_count} 条。".strip()
    if created_count > 0:
        return prefix
    if candidate_count <= 0:
        reason = "失败原因：采集器没有返回候选商品，请检查关键词、采集来源配置或外部接口状态。"
    elif skipped_count >= candidate_count:
        reason = "失败原因：候选商品全部是重复记录，没有新增采集结果。"
    else:
        reason = "失败原因：本次没有新增采集结果，请检查过滤条件和采集数据格式。"
    return f"{prefix} {reason}"


def collection_exception_note(error_detail: object) -> str:
    message = str(error_detail or "采集执行失败").strip()
    return message if message.startswith("失败原因：") else f"失败原因：{message}"


def normalize_header(value: object) -> str:
    return str(value or "").strip().lower().replace(" ", "").replace("_", "")


def first_value(row: dict[str, object], aliases: list[str], default: object = "") -> object:
    normalized_row = {normalize_header(key): value for key, value in row.items()}
    for alias in aliases:
        key = normalize_header(alias)
        if key in normalized_row and normalized_row[key] not in (None, ""):
            return normalized_row[key]
    return default


def to_float(value: object, default: float = 0) -> float:
    try:
        return float(str(value).replace("¥", "").replace(",", "").strip())
    except (TypeError, ValueError):
        return default


def to_int(value: object, default: int = 0) -> int:
    try:
        return int(float(str(value).replace(",", "").strip()))
    except (TypeError, ValueError):
        return default


def parse_collection_rows(file_path: Path) -> list[dict[str, object]]:
    if file_path.suffix.lower() == ".json":
        data = json.loads(file_path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data = data.get("items") or data.get("data") or data.get("results") or [data]
        if not isinstance(data, list):
            return []
        return [{normalize_header(key): value for key, value in item.items()} for item in data if isinstance(item, dict)]
    if file_path.suffix.lower() == ".csv":
        text = file_path.read_text(encoding="utf-8-sig", errors="replace")
        reader = csv.DictReader(text.splitlines())
        return [{normalize_header(key): value for key, value in row.items()} for row in reader]
    workbook = load_workbook(file_path, read_only=True, data_only=True)
    sheet = workbook.active
    rows = list(sheet.iter_rows(values_only=True))
    if not rows:
        return []
    headers = [normalize_header(value) for value in rows[0]]
    parsed: list[dict[str, object]] = []
    for values in rows[1:]:
        parsed.append({headers[index]: values[index] if index < len(values) else "" for index in range(len(headers))})
    return parsed


def collection_preflight() -> dict[str, object]:
    cookie_path = Path(get_setting_value("1688_cookie_path", "data/1688_cookies.json"))
    if not cookie_path.is_absolute():
        cookie_path = BASE_DIR / cookie_path
    inline_cookie = get_setting_value("1688_cookie")
    onebound_key = get_setting_value("onebound_key")
    onebound_secret = get_setting_value("onebound_secret")
    return {
        "default_mode": get_setting_value("collection_mode", "1688"),
        "1688": {
            "cookie_path": str(cookie_path),
            "cookie_exists": cookie_path.exists(),
            "inline_cookie_configured": bool(inline_cookie),
            "onebound_configured": bool(onebound_key and onebound_secret),
            "configured": bool(onebound_key and onebound_secret) or bool(inline_cookie) or cookie_path.exists(),
            "status": "ready" if (onebound_key and onebound_secret) else ("cookie_ready" if (inline_cookie or cookie_path.exists()) else "missing_credentials"),
        },
    }


def run_local_collector(payload: CollectionTaskPayload, task_id: int, mode: str, collector: str, note: str) -> CollectorRunResult:
    raise HTTPException(status_code=410, detail="本地模拟采集已移除，请使用 1688 / 万邦 API 真实采集或文件导入")


def write_collection_request(task_id: int, payload: CollectionTaskPayload, mode: str, collector: str) -> str:
    request_dir = DATA_DIR / "collection_requests"
    request_dir.mkdir(parents=True, exist_ok=True)
    target = request_dir / f"collection_task_{task_id}.json"
    request_payload = {
        "task_id": task_id,
        "mode": mode,
        "collector": collector,
        "keyword": payload.keyword,
        "source": payload.source,
        "target_count": payload.target_count,
        "min_price": payload.min_price,
        "max_price": payload.max_price,
        "blacklist": payload.blacklist,
        "created_at": now_text(),
        "execution_policy": "manual_review_required",
    }
    if mode == "1688":
        request_payload["1688"] = {
            "provider": "onebound" if get_setting_value("onebound_key") and get_setting_value("onebound_secret") else "cookie",
            "onebound_configured": bool(get_setting_value("onebound_key") and get_setting_value("onebound_secret")),
            "cookie_path": get_setting_value("1688_cookie_path", "data/1688_cookies.json"),
        }
    target.write_text(json.dumps(request_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(target)


def ensure_collection_request(task: sqlite3.Row) -> str:
    request_path = task["request_path"]
    if request_path and Path(request_path).exists():
        return request_path
    payload = CollectionTaskPayload(
        keyword=task["keyword"],
        source=task["source"],
        mode=task["mode"],
        collector=task["collector"],
        target_count=task["target_count"],
        min_price=task["min_price"],
        max_price=task["max_price"],
        blacklist=task["blacklist"],
    )
    return write_collection_request(task["id"], payload, task["mode"], task["collector"])


def resolve_collector(payload: CollectionTaskPayload) -> tuple[str, str, str]:
    requested_mode = payload.mode or get_setting_value("collection_mode", "1688")
    collector = payload.collector or requested_mode or "local"
    note = ""
    preflight = collection_preflight()
    if requested_mode == "1688":
        return "1688", "1688_public_search", note
    if requested_mode == "simulate":
        raise HTTPException(status_code=410, detail="本地模拟采集已移除，请选择 1688 / 万邦 API 采集")
    return requested_mode, collector, note


def run_collector(payload: CollectionTaskPayload, task_id: int) -> CollectorRunResult:
    mode, collector, note = resolve_collector(payload)
    if mode == "1688":
        return CollectorRunResult(
            mode=mode,
            collector=collector,
            note="真实采集请求已生成，需人工确认后再执行。",
            candidates=[],
        )
    raise HTTPException(status_code=400, detail=f"不支持的采集模式：{mode}")


def call_openai_compatible_chat(base_url: str, api_key: str, model: str, messages: list[dict[str, str]], timeout: int = 45) -> str:
    endpoint = base_url.rstrip("/")
    if not endpoint.endswith("/chat/completions"):
        endpoint = f"{endpoint}/v1/chat/completions"
    body = json.dumps({"model": model, "messages": messages, "temperature": 0.4}).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise HTTPException(status_code=502, detail=f"AI 接口返回错误：{exc.code} {detail}") from exc
    except urllib.error.URLError as exc:
        raise HTTPException(status_code=502, detail=f"AI 接口连接失败：{exc.reason}") from exc
    except TimeoutError as exc:
        raise HTTPException(status_code=504, detail="AI 接口请求超时") from exc
    try:
        return payload["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise HTTPException(status_code=502, detail="AI 接口返回格式异常") from exc


def extract_onebound_items(payload: object) -> list[dict[str, object]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []
    for key in ["items", "item", "data", "result", "results"]:
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
        if isinstance(value, dict):
            nested = extract_onebound_items(value)
            if nested:
                return nested
    return []


def normalize_onebound_items(items: list[dict[str, object]], source: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for item in items:
        normalized = {normalize_header(key): value for key, value in item.items()}
        title = first_value(normalized, ["title", "name", "subject", "商品标题"], "")
        num_iid = str(first_value(normalized, ["num_iid", "offer_id", "offerId", "id", "item_id"], "")).strip()
        url = str(first_value(normalized, ["detail_url", "url", "item_url", "link", "商品链接"], "")).strip()
        if not url and num_iid:
            url = f"https://detail.1688.com/offer/{num_iid}.html"
        image_url = str(first_value(normalized, ["pic_url", "image", "img", "main_image", "picurl", "image_url"], "")).strip()
        rows.append(
            {
                "title": title,
                "source": source,
                "url": url,
                "image_url": image_url,
                "price": first_value(normalized, ["price", "promotion_price", "sale_price", "orginal_price", "价格"], 0),
                "sales": first_value(normalized, ["sales", "sales_volume", "sale_count", "month_sales", "销量"], 0),
                "image_count": 1 if image_url else 0,
            }
        )
    return rows


def run_onebound_1688_search(payload: CollectionTaskPayload) -> list[dict[str, object]]:
    key = get_setting_value("onebound_key", "").strip()
    secret = get_setting_value("onebound_secret", "").strip()
    if not key or not secret:
        raise HTTPException(status_code=400, detail="万邦 API Key/Secret 未配置")
    params = {
        "key": key,
        "secret": secret,
        "q": payload.keyword.strip(),
        "page": "1",
        "page_size": str(max(1, min(int(payload.target_count or 1), 50))),
    }
    if payload.min_price:
        params["start_price"] = str(payload.min_price)
    if payload.max_price:
        params["end_price"] = str(payload.max_price)
    endpoint = "https://api-gw.onebound.cn/1688/item_search?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(endpoint, headers={"Accept": "application/json"}, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            data = json.loads(response.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise HTTPException(status_code=502, detail=f"万邦 API 返回错误：{exc.code} {detail}") from exc
    except urllib.error.URLError as exc:
        raise HTTPException(status_code=502, detail=f"万邦 API 连接失败：{exc.reason}") from exc
    except TimeoutError as exc:
        raise HTTPException(status_code=504, detail="万邦 API 请求超时") from exc
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=502, detail="万邦 API 返回非 JSON 内容") from exc
    error = first_value(data, ["error", "error_msg", "msg", "message"], "")
    code = str(first_value(data, ["error_code", "code"], "")).strip()
    items = extract_onebound_items(data)
    if not items and error:
        raise HTTPException(status_code=502, detail=f"万邦 API 错误：{code} {error}".strip())
    return normalize_onebound_items(items, payload.source or "1688")


def extract_offer_id(source_url: str) -> str:
    match = re.search(r"offer/(\d+)\.html", source_url or "")
    if match:
        return match.group(1)
    match = re.search(r"(?:num_iid|item_id|offer_id|id)=(\d+)", source_url or "")
    return match.group(1) if match else ""


def onebound_request(endpoint: str, params: dict[str, str], label: str) -> dict[str, object]:
    key = get_setting_value("onebound_key", "").strip()
    secret = get_setting_value("onebound_secret", "").strip()
    if not key or not secret:
        raise HTTPException(status_code=400, detail="万邦 API Key/Secret 未配置")
    query = {"key": key, "secret": secret, **params}
    url = f"https://api-gw.onebound.cn/1688/{endpoint}?" + urllib.parse.urlencode(query)
    request = urllib.request.Request(url, headers={"Accept": "application/json"}, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            payload = json.loads(response.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise HTTPException(status_code=502, detail=f"万邦 {label} 返回错误：{exc.code} {detail}") from exc
    except urllib.error.URLError as exc:
        raise HTTPException(status_code=502, detail=f"万邦 {label} 连接失败：{exc.reason}") from exc
    except TimeoutError as exc:
        raise HTTPException(status_code=504, detail=f"万邦 {label} 请求超时") from exc
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=502, detail=f"万邦 {label} 返回非 JSON 内容") from exc
    error = first_value(payload, ["error", "error_msg", "msg", "message"], "")
    code = str(first_value(payload, ["error_code", "code"], "")).strip()
    if error and not extract_onebound_items(payload):
        raise HTTPException(status_code=502, detail=f"万邦 {label} 错误：{code} {error}".strip())
    return payload


def run_onebound_1688_detail(source_url: str) -> dict[str, object]:
    offer_id = extract_offer_id(source_url)
    if not offer_id:
        raise HTTPException(status_code=400, detail="无法从商品链接提取 1688 offer id")
    return onebound_request("item_get", {"num_iid": offer_id}, "详情")


def first_dict(value: object) -> dict[str, object]:
    if isinstance(value, dict):
        if any(key in value for key in ["title", "item_imgs", "pic_url", "skus", "props_name", "desc_img"]):
            return value
        for key in ["item", "data", "result"]:
            if isinstance(value.get(key), dict):
                return first_dict(value[key])
        return value
    return {}


def flatten_strings(value: object) -> list[str]:
    values: list[str] = []
    if isinstance(value, str):
        if value.strip():
            values.append(value.strip())
    elif isinstance(value, list):
        for item in value:
            values.extend(flatten_strings(item))
    elif isinstance(value, dict):
        for item in value.values():
            values.extend(flatten_strings(item))
    return values


def extract_image_urls(value: object) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()
    for text in flatten_strings(value):
        if text.startswith("http") and re.search(r"\.(jpg|jpeg|png|webp|gif)(\?|$)", text, re.I) and text not in seen:
            seen.add(text)
            urls.append(text)
        for url in re.findall(r"https?://[^\s'\"<>]+", text):
            clean_url = url.rstrip(",;)]}")
            if re.search(r"\.(jpg|jpeg|png|webp|gif)(\?|$)", clean_url, re.I) and clean_url not in seen:
                seen.add(clean_url)
                urls.append(clean_url)
    return urls


def parse_1688_properties_name(value: str) -> dict[str, str]:
    props: dict[str, str] = {}
    for part in str(value or "").split(";"):
        pieces = part.split(":", 3)
        if len(pieces) == 4:
            props[f"{pieces[0]}:{pieces[1]}"] = pieces[3].strip()
    return props


def extract_named_prop(value: str, name: str) -> str:
    for part in str(value or "").split(";"):
        pieces = part.split(":", 3)
        if len(pieces) == 4 and pieces[2] == name:
            return pieces[3].strip()
    return ""


def normalize_prop_images(value: object) -> dict[str, str]:
    if isinstance(value, dict):
        value = value.get("prop_img") or value.get("props_img") or value.get("list") or value.get("data") or value
    if isinstance(value, dict):
        value = list(value.values())
    if not isinstance(value, list):
        return {}
    images: dict[str, str] = {}
    for item in value:
        if not isinstance(item, dict):
            continue
        key = str(item.get("properties") or item.get("property") or item.get("props") or "").strip()
        urls = extract_image_urls(item)
        if key and urls:
            images[key] = urls[0]
    return images


def normalize_detail_payload(payload: dict[str, object]) -> dict[str, object]:
    item = first_dict(payload)
    title = str(first_value(item, ["title", "name", "subject"], "")).strip()
    price = to_float(first_value(item, ["price", "promotion_price", "sale_price", "orginal_price"], 0), 0)
    main_images = extract_image_urls(first_value(item, ["item_imgs", "item_img", "pic_url", "pic_urls", "images", "imgs"], []))
    desc_images = extract_image_urls(first_value(item, ["desc_img", "desc_imgs", "desc_images", "detail_imgs", "detail_images"], []))
    all_images = extract_image_urls(item)
    prop_name_map = parse_1688_properties_name(str(item.get("props_name") or item.get("property_alias") or ""))
    prop_image_map = normalize_prop_images(item.get("prop_imgs") or item.get("props_img") or item.get("prop_images"))
    sku_rows: list[dict[str, object]] = []
    sku_source = item.get("skus") or item.get("sku") or item.get("sku_infos") or item.get("props_img") or []
    if isinstance(sku_source, dict):
        sku_source = sku_source.get("sku") or sku_source.get("skus") or sku_source.get("list") or sku_source.get("data") or list(sku_source.values())
    if not isinstance(sku_source, list):
        sku_source = []
    for index, sku in enumerate(sku_source):
        if not isinstance(sku, dict):
            continue
        normalized = {normalize_header(key): value for key, value in sku.items()}
        properties_name = str(first_value(normalized, ["properties_name", "propertiesname", "props_name"], "")).strip()
        properties = str(first_value(normalized, ["properties", "props"], "")).strip()
        color = extract_named_prop(properties_name, "颜色") or str(first_value(normalized, ["color", "颜色", "颜色分类", "prop_value", "propvalue"], "")).strip()
        size = extract_named_prop(properties_name, "尺码") or str(first_value(normalized, ["size", "尺码", "规格", "spec"], "")).strip()
        sku_id = str(first_value(normalized, ["sku_id", "skuid", "id", "spec_id"], "")).strip()
        images = extract_image_urls(sku)
        for prop_key in properties.split(";"):
            if prop_key in prop_image_map and prop_image_map[prop_key] not in images:
                images.append(prop_image_map[prop_key])
            if not color and prop_key in prop_name_map and prop_key.startswith("0:"):
                color = prop_name_map[prop_key]
            if not size and prop_key in prop_name_map and prop_key.startswith("1:"):
                size = prop_name_map[prop_key]
        sku_rows.append({"sku_id": sku_id, "color": color, "size": size, "images": images, "sort_order": index})
    return {"title": title, "price": price, "main_images": main_images, "desc_images": desc_images, "all_images": all_images, "skus": sku_rows}


def apply_detail_to_product(db: sqlite3.Connection, product_id: int, source_url: str, payload: dict[str, object]) -> dict[str, object]:
    detail = normalize_detail_payload(payload)
    timestamp = now_text()
    db.execute(
        """
        INSERT INTO product_detail_snapshots (product_id, provider, source_url, raw_json, status, note, updated_at)
        VALUES (?, 'onebound', ?, ?, 'completed', ?, ?)
        ON CONFLICT(product_id) DO UPDATE SET provider=excluded.provider, source_url=excluded.source_url,
        raw_json=excluded.raw_json, status=excluded.status, note=excluded.note, updated_at=excluded.updated_at
        """,
        (product_id, source_url, json.dumps(payload, ensure_ascii=False), "万邦详情采集完成", timestamp),
    )
    db.execute("DELETE FROM product_sku_images WHERE product_id = ?", (product_id,))
    image_order = 0
    inserted_keys: set[tuple[str, str, str, str]] = set()

    def insert_detail_image(url: str, source: str, color: str = "", size: str = "", sku_id: str = "") -> None:
        nonlocal image_order
        clean_url = str(url or "").strip()
        if not clean_url:
            return
        key = (source, clean_url, str(color or ""), str(size or ""))
        if key in inserted_keys:
            return
        inserted_keys.add(key)
        db.execute(
            """
            INSERT INTO product_sku_images (product_id, sku_id, color, size, image_url, sort_order, source, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (product_id, str(sku_id or ""), str(color or ""), str(size or ""), clean_url, image_order, source, timestamp),
        )
        image_order += 1

    for sku in detail["skus"]:
        for url in sku["images"]:
            insert_detail_image(url, "detail_sku_image", sku["color"], sku["size"], sku["sku_id"])
    for url in detail["main_images"]:
        insert_detail_image(url, "detail_main_image")
    desc_urls = detail.get("desc_images") or []
    fallback_detail_urls = [url for url in detail["all_images"] if url not in set(detail["main_images"])]
    for url in desc_urls or fallback_detail_urls[:40]:
        insert_detail_image(url, "detail_desc_image")
    colors = sorted({str(sku["color"]).strip() for sku in detail["skus"] if str(sku["color"]).strip()})
    sizes = sorted({str(sku["size"]).strip() for sku in detail["skus"] if str(sku["size"]).strip()})
    product = db.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    if product:
        title = detail["title"] or product["title"]
        purchase_price = float(detail["price"] or product["purchase_price"] or 0)
        payload_for_cost = ProductPayload(
            title=title,
            skc=product["skc"],
            sku_summary=f"{len(colors) or 1}色 × {len(sizes) or 1}码" if colors or sizes else product["sku_summary"],
            purchase_price=purchase_price,
            first_mile=float(product["first_mile"]),
            platform_cost=float(product["platform_cost"]),
            status=product["status"],
        )
        total_cost, estimated_profit, gross_margin = recalc(payload_for_cost)
        db.execute(
            """
            UPDATE products SET title = ?, sku_summary = ?, purchase_price = ?, total_cost = ?,
            estimated_profit = ?, gross_margin = ?, updated_at = ? WHERE id = ?
            """,
            (payload_for_cost.title, payload_for_cost.sku_summary, payload_for_cost.purchase_price, total_cost, estimated_profit, gross_margin, timestamp, product_id),
        )
    override = db.execute("SELECT * FROM processing_overrides WHERE product_id = ?", (product_id,)).fetchone()
    if override:
        color_text = " / ".join(colors) or override["color"]
        size_text = " / ".join(sizes) or override["size"]
        sku_code = override["sku_code"]
        if sku_code.endswith("COLOR-SIZE") and product:
            sku_code = f"{product['skc']}-{(colors[0] if colors else 'COLOR')}-{(sizes[0] if sizes else 'SIZE')}"
        db.execute(
            "UPDATE processing_overrides SET color = ?, size = ?, sku_code = ?, source_url = ?, updated_at = ? WHERE product_id = ?",
            (color_text, size_text, sku_code, source_url, timestamp, product_id),
        )
    return detail


def try_enrich_product_from_onebound_detail(db: sqlite3.Connection, product_id: int, source_url: str) -> str:
    if not source_url.startswith("http"):
        return "无详情链接，跳过万邦详情采集"
    if not get_setting_value("onebound_key") or not get_setting_value("onebound_secret"):
        db.execute(
            """
            INSERT INTO product_detail_snapshots (product_id, provider, source_url, raw_json, status, note, updated_at)
            VALUES (?, 'onebound', ?, '', 'skipped', '万邦 API Key/Secret 未配置，跳过详情采集', ?)
            ON CONFLICT(product_id) DO UPDATE SET source_url=excluded.source_url, status=excluded.status, note=excluded.note, updated_at=excluded.updated_at
            """,
            (product_id, source_url, now_text()),
        )
        return "万邦 API Key/Secret 未配置，跳过详情采集"
    try:
        detail_payload = run_onebound_1688_detail(source_url)
        detail = apply_detail_to_product(db, product_id, source_url, detail_payload)
        return f"万邦详情采集完成：{len(detail['skus'])} 个 SKU，{len(detail['all_images'])} 张图片"
    except HTTPException as exc:
        db.execute(
            """
            INSERT INTO product_detail_snapshots (product_id, provider, source_url, raw_json, status, note, updated_at)
            VALUES (?, 'onebound', ?, '', 'failed', ?, ?)
            ON CONFLICT(product_id) DO UPDATE SET source_url=excluded.source_url, status=excluded.status, note=excluded.note, updated_at=excluded.updated_at
            """,
            (product_id, source_url, str(exc.detail), now_text()),
        )
        return f"万邦详情采集失败：{exc.detail}"


def fetch_text(url: str, timeout: int = 25) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
            charset = response.headers.get_content_charset() or "utf-8"
            return raw.decode(charset, errors="replace")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:300]
        raise HTTPException(status_code=502, detail=f"真实采集页面返回错误：{exc.code} {detail}") from exc
    except urllib.error.URLError as exc:
        raise HTTPException(status_code=502, detail=f"真实采集连接失败：{exc.reason}") from exc
    except TimeoutError as exc:
        raise HTTPException(status_code=504, detail="真实采集请求超时") from exc


def load_cookie_header(cookie_path: Path) -> str:
    inline_cookie = get_setting_value("1688_cookie", "").strip()
    if inline_cookie:
        return inline_cookie
    if not cookie_path.exists():
        raise HTTPException(status_code=400, detail=f"1688 Cookie 文件不存在：{cookie_path}")
    text = cookie_path.read_text(encoding="utf-8", errors="replace").strip()
    if not text:
        raise HTTPException(status_code=400, detail=f"1688 Cookie 文件为空：{cookie_path}")
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return text
    if isinstance(data, dict):
        if isinstance(data.get("cookies"), list):
            data = data["cookies"]
        else:
            return "; ".join(f"{key}={value}" for key, value in data.items() if value not in (None, ""))
    if isinstance(data, list):
        parts = []
        for item in data:
            if isinstance(item, dict) and item.get("name") and item.get("value") is not None:
                parts.append(f"{item['name']}={item['value']}")
        return "; ".join(parts)
    raise HTTPException(status_code=400, detail="1688 Cookie 文件格式不支持，请使用浏览器导出的 cookies JSON 或 Cookie 字符串")


def fetch_text_with_cookie(url: str, cookie_header: str, timeout: int = 25) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cookie": cookie_header,
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
            charset = response.headers.get_content_charset() or "utf-8"
            return raw.decode(charset, errors="replace")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:300]
        raise HTTPException(status_code=502, detail=f"1688 返回错误：{exc.code} {detail}") from exc
    except urllib.error.URLError as exc:
        raise HTTPException(status_code=502, detail=f"1688 连接失败：{exc.reason}") from exc
    except TimeoutError as exc:
        raise HTTPException(status_code=504, detail="1688 请求超时") from exc


def clean_text(value: object) -> str:
    text = unescape(str(value or ""))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def find_near_price(text: str, start: int) -> float:
    window = text[max(0, start - 300): start + 800]
    matches = re.findall(r'(?:(?:price|salePrice|discountPrice|价格|￥|¥)["\'\s:=]*)(\d+(?:\.\d+)?)', window, flags=re.I)
    for match in matches:
        price = to_float(match)
        if 0 < price < 100000:
            return price
    return 0


def parse_1688_public_search(html: str, source: str, target_count: int, min_price: float, max_price: float, blacklist: str) -> list[dict[str, object]]:
    blacklist_words = [word.strip().lower() for word in blacklist.replace("，", ",").split(",") if word.strip()]
    rows: list[dict[str, object]] = []
    seen: set[str] = set()
    link_pattern = re.compile(r'href=["\'](?P<url>(?:https?:)?//(?:detail|offer|sale)\.1688\.com/[^"\']+)["\'][^>]*>(?P<title>.*?)</a>', re.I | re.S)
    for match in link_pattern.finditer(html):
        url = match.group("url")
        if url.startswith("//"):
            url = f"https:{url}"
        url = url.split("?")[0]
        title = clean_text(match.group("title"))
        if not title or len(title) < 4 or url in seen:
            continue
        if blacklist_words and any(word in title.lower() for word in blacklist_words):
            continue
        price = find_near_price(html, match.start())
        if min_price and price and price < min_price:
            continue
        if max_price and price and price > max_price:
            continue
        rows.append({"title": title, "source": source, "url": url, "price": price, "sales": 0, "image_count": 1})
        seen.add(url)
        if len(rows) >= target_count:
            return rows
    json_title_pattern = re.compile(r'["\'](?:subject|title|shortTitle|offerTitle)["\']\s*:\s*["\'](?P<title>[^"\']{4,160})["\']', re.I)
    urls = re.findall(r'(?:https?:)?//(?:detail|offer|sale)\.1688\.com/[^"\'\\\s]+', html, flags=re.I)
    url_index = 0
    for match in json_title_pattern.finditer(html):
        title = clean_text(match.group("title"))
        while url_index < len(urls) and urls[url_index].split("?")[0] in seen:
            url_index += 1
        url = urls[url_index].split("?")[0] if url_index < len(urls) else ""
        if url.startswith("//"):
            url = f"https:{url}"
        if not title or title in seen:
            continue
        if blacklist_words and any(word in title.lower() for word in blacklist_words):
            continue
        price = find_near_price(html, match.start())
        if min_price and price and price < min_price:
            continue
        if max_price and price and price > max_price:
            continue
        rows.append({"title": title, "source": source, "url": url, "price": price, "sales": 0, "image_count": 1})
        seen.add(url or title)
        if len(rows) >= target_count:
            break
    return rows


def run_1688_public_search(payload: CollectionTaskPayload) -> list[dict[str, object]]:
    keyword = payload.keyword.strip()
    if not keyword:
        raise HTTPException(status_code=400, detail="请输入采集关键词")
    cookie_path = Path(get_setting_value("1688_cookie_path", "data/1688_cookies.json"))
    if not cookie_path.is_absolute():
        cookie_path = BASE_DIR / cookie_path
    cookie_header = load_cookie_header(cookie_path)
    target_count = max(1, min(int(payload.target_count or 1), 50))
    min_price = max(float(payload.min_price or 0), 0)
    max_price = max(float(payload.max_price or 0), 0)
    query = urllib.parse.urlencode({"keywords": keyword}, encoding="utf-8")
    search_urls = [
        f"https://s.1688.com/selloffer/offer_search.htm?{query}",
        f"https://search.1688.com/selloffer/offer_search.htm?{query}",
    ]
    last_error = ""
    for url in search_urls:
        try:
            html = fetch_text_with_cookie(url, cookie_header)
            rows = parse_1688_public_search(html, payload.source or "1688", target_count, min_price, max_price, payload.blacklist)
            if rows:
                return rows
            if "login.1688.com" in html or "_____tmd_____" in html or "x5sec" in html:
                last_error = "Cookie 已失效或被 1688 风控拦截，请重新导出登录 Cookie"
            else:
                last_error = "页面已返回，但未解析到商品；可能页面结构变化"
        except HTTPException as exc:
            last_error = str(exc.detail)
    raise HTTPException(status_code=502, detail=f"1688 Cookie 真实采集失败：{last_error or '未返回商品'}")


def normalize_collection_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [{normalize_header(key): value for key, value in row.items()} for row in rows if isinstance(row, dict)]


def insert_collection_rows_with_db(db: sqlite3.Connection, rows: list[dict[str, object]], source: str) -> tuple[int, int]:
    imported = 0
    skipped = 0
    timestamp = now_text()
    existing_urls = {row["source_url"] for row in db.execute("SELECT source_url FROM collection_items WHERE source_url != ''").fetchall()}
    existing_keys = {f"{row['source']}::{row['title']}".lower() for row in db.execute("SELECT source, title FROM collection_items").fetchall()}
    for row in rows:
        title = str(first_value(row, ["title", "商品标题", "标题", "name", "productname", "producttitle"], "")).strip()
        if not title:
            skipped += 1
            continue
        row_source = str(first_value(row, ["source", "来源", "platform"], source)).strip() or source
        source_url = str(first_value(row, ["url", "source_url", "sourceurl", "链接", "商品链接", "link", "producturl"], "")).strip()
        dedupe_key = f"{row_source}::{title}".lower()
        if (source_url and source_url in existing_urls) or dedupe_key in existing_keys:
            skipped += 1
            continue
        price = to_float(first_value(row, ["price", "价格", "采购价", "saleprice", "currentprice"], 0))
        sales = to_int(first_value(row, ["sales", "销量", "月销量", "sold", "orders"], 0))
        image_count = to_int(first_value(row, ["image_count", "imagecount", "图片数", "图片数量", "images"], 0))
        image_url = str(first_value(row, ["image_url", "imageurl", "pic_url", "picurl", "图片", "主图", "main_image", "mainimage", "img"], "")).strip()
        if not image_url:
            skipped += 1
            continue
        db.execute(
            """
            INSERT INTO collection_items (title, source, source_url, image_url, price, sales, image_count, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?)
            """,
            (title, row_source, source_url, image_url, price, sales, image_count, timestamp),
        )
        if source_url:
            existing_urls.add(source_url)
        existing_keys.add(dedupe_key)
        imported += 1
    return imported, skipped


def insert_collection_rows(rows: list[dict[str, object]], source: str) -> tuple[int, int]:
    with connect() as db:
        return insert_collection_rows_with_db(db, rows, source)


def insert_collection_candidates(candidates: list[CollectorCandidate]) -> tuple[int, int]:
    imported = 0
    skipped = 0
    timestamp = now_text()
    with connect() as db:
        existing_urls = {row["source_url"] for row in db.execute("SELECT source_url FROM collection_items WHERE source_url != ''").fetchall()}
        existing_keys = {f"{row['source']}::{row['title']}".lower() for row in db.execute("SELECT source, title FROM collection_items").fetchall()}
        for candidate in candidates:
            dedupe_key = f"{candidate.source}::{candidate.title}".lower()
            if not candidate.image_url:
                skipped += 1
                continue
            if (candidate.source_url and candidate.source_url in existing_urls) or dedupe_key in existing_keys:
                skipped += 1
                continue
            db.execute(
                """
                INSERT INTO collection_items (title, source, source_url, image_url, price, sales, image_count, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?)
                """,
                (candidate.title, candidate.source, candidate.source_url, candidate.image_url, candidate.price, candidate.sales, candidate.image_count, timestamp),
            )
            if candidate.source_url:
                existing_urls.add(candidate.source_url)
            existing_keys.add(dedupe_key)
            imported += 1
    return imported, skipped


def insert_collection_candidates_with_db(db: sqlite3.Connection, candidates: list[CollectorCandidate]) -> tuple[int, int]:
    imported = 0
    skipped = 0
    timestamp = now_text()
    existing_urls = {row["source_url"] for row in db.execute("SELECT source_url FROM collection_items WHERE source_url != ''").fetchall()}
    existing_keys = {f"{row['source']}::{row['title']}".lower() for row in db.execute("SELECT source, title FROM collection_items").fetchall()}
    for candidate in candidates:
        dedupe_key = f"{candidate.source}::{candidate.title}".lower()
        if not candidate.image_url:
            skipped += 1
            continue
        if (candidate.source_url and candidate.source_url in existing_urls) or dedupe_key in existing_keys:
            skipped += 1
            continue
        db.execute(
            """
            INSERT INTO collection_items (title, source, source_url, image_url, price, sales, image_count, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?)
            """,
            (candidate.title, candidate.source, candidate.source_url, candidate.image_url, candidate.price, candidate.sales, candidate.image_count, timestamp),
        )
        if candidate.source_url:
            existing_urls.add(candidate.source_url)
        existing_keys.add(dedupe_key)
        imported += 1
    return imported, skipped


def recalc(payload: ProductPayload) -> tuple[float, float, float]:
    total_cost = round(payload.purchase_price + payload.first_mile + payload.platform_cost, 2)
    estimated_profit = round(max(total_cost * 0.66, 0), 2)
    gross_margin = round((estimated_profit / (total_cost + estimated_profit) * 100) if total_cost else 0, 1)
    return total_cost, estimated_profit, gross_margin


def init_db() -> None:
    with connect() as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                skc TEXT NOT NULL UNIQUE,
                sku_summary TEXT NOT NULL DEFAULT '',
                main_image TEXT,
                purchase_price REAL NOT NULL DEFAULT 0,
                first_mile REAL NOT NULL DEFAULT 0,
                platform_cost REAL NOT NULL DEFAULT 0,
                total_cost REAL NOT NULL DEFAULT 0,
                estimated_profit REAL NOT NULL DEFAULT 0,
                gross_margin REAL NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT '利润正常',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS collection_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                source TEXT NOT NULL DEFAULT '1688',
                source_url TEXT NOT NULL DEFAULT '',
                image_url TEXT NOT NULL DEFAULT '',
                price REAL NOT NULL DEFAULT 0,
                sales INTEGER NOT NULL DEFAULT 0,
                image_count INTEGER NOT NULL DEFAULT 0,
                selected INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS upload_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                total_count INTEGER NOT NULL DEFAULT 0,
                success_count INTEGER NOT NULL DEFAULT 0,
                failed_count INTEGER NOT NULL DEFAULT 0,
                export_path TEXT NOT NULL DEFAULT '',
                run_log TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS collection_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                source TEXT NOT NULL DEFAULT '1688',
                mode TEXT NOT NULL DEFAULT '1688',
                collector TEXT NOT NULL DEFAULT '1688_public_search',
                target_count INTEGER NOT NULL DEFAULT 10,
                min_price REAL NOT NULL DEFAULT 0,
                max_price REAL NOT NULL DEFAULT 0,
                blacklist TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'pending',
                note TEXT NOT NULL DEFAULT '',
                request_path TEXT NOT NULL DEFAULT '',
                result_count INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS processing_overrides (
                product_id INTEGER PRIMARY KEY,
                english_title TEXT NOT NULL DEFAULT '',
                color TEXT NOT NULL DEFAULT '',
                size TEXT NOT NULL DEFAULT '',
                sku_code TEXT NOT NULL DEFAULT '',
                declared_price REAL NOT NULL DEFAULT 0,
                weight_g INTEGER NOT NULL DEFAULT 350,
                length_cm INTEGER NOT NULL DEFAULT 15,
                width_cm INTEGER NOT NULL DEFAULT 10,
                height_cm INTEGER NOT NULL DEFAULT 2,
                source_url TEXT NOT NULL DEFAULT '',
                stock INTEGER NOT NULL DEFAULT 999,
                ship_days INTEGER NOT NULL DEFAULT 9,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS publish_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                result TEXT NOT NULL,
                skc TEXT NOT NULL,
                title TEXT NOT NULL,
                reason TEXT NOT NULL DEFAULT '',
                screenshot TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS api_configs (
                key TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                enabled INTEGER NOT NULL DEFAULT 1,
                base_url TEXT NOT NULL DEFAULT '',
                model TEXT NOT NULL DEFAULT '',
                api_key TEXT NOT NULL DEFAULT '',
                usage TEXT NOT NULL DEFAULT '',
                updated_at TEXT NOT NULL
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS image_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                provider TEXT NOT NULL DEFAULT 'nanobanana',
                task_id TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'submitted',
                source_image TEXT NOT NULL DEFAULT '',
                result_url TEXT NOT NULL DEFAULT '',
                local_path TEXT NOT NULL DEFAULT '',
                prompt TEXT NOT NULL DEFAULT '',
                note TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS product_detail_snapshots (
                product_id INTEGER PRIMARY KEY,
                provider TEXT NOT NULL DEFAULT '',
                source_url TEXT NOT NULL DEFAULT '',
                raw_json TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT '',
                note TEXT NOT NULL DEFAULT '',
                updated_at TEXT NOT NULL,
                FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS product_sku_images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                sku_id TEXT NOT NULL DEFAULT '',
                color TEXT NOT NULL DEFAULT '',
                size TEXT NOT NULL DEFAULT '',
                image_url TEXT NOT NULL DEFAULT '',
                sort_order INTEGER NOT NULL DEFAULT 0,
                source TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS product_color_image_assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                color TEXT NOT NULL DEFAULT '',
                image_url TEXT NOT NULL DEFAULT '',
                source TEXT NOT NULL DEFAULT '',
                sort_order INTEGER NOT NULL DEFAULT 0,
                is_auto INTEGER NOT NULL DEFAULT 1,
                confidence REAL NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS product_detail_image_assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                image_url TEXT NOT NULL DEFAULT '',
                source TEXT NOT NULL DEFAULT '',
                sort_order INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS product_image_vision_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                image_identity TEXT NOT NULL,
                image_url TEXT NOT NULL DEFAULT '',
                matched_color TEXT NOT NULL DEFAULT '',
                confidence REAL NOT NULL DEFAULT 0,
                is_product_image INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT '',
                provider TEXT NOT NULL DEFAULT '',
                raw_json TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(product_id, image_identity),
                FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS app_settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL DEFAULT '',
                updated_at TEXT NOT NULL
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS prompt_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL DEFAULT '',
                prompt_type TEXT NOT NULL DEFAULT '',
                usage TEXT NOT NULL DEFAULT '',
                content TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT '启用中',
                updated_at TEXT NOT NULL
            )
            """
        )
        upload_columns = [row[1] for row in db.execute("PRAGMA table_info(upload_tasks)").fetchall()]
        if "run_log" not in upload_columns:
            db.execute("ALTER TABLE upload_tasks ADD COLUMN run_log TEXT NOT NULL DEFAULT ''")
        collection_columns = [row[1] for row in db.execute("PRAGMA table_info(collection_items)").fetchall()]
        if "image_url" not in collection_columns:
            db.execute("ALTER TABLE collection_items ADD COLUMN image_url TEXT NOT NULL DEFAULT ''")
        collection_task_columns = [row[1] for row in db.execute("PRAGMA table_info(collection_tasks)").fetchall()]
        for column_name, ddl in [
            ("mode", "ALTER TABLE collection_tasks ADD COLUMN mode TEXT NOT NULL DEFAULT '1688'"),
            ("collector", "ALTER TABLE collection_tasks ADD COLUMN collector TEXT NOT NULL DEFAULT '1688_public_search'"),
            ("note", "ALTER TABLE collection_tasks ADD COLUMN note TEXT NOT NULL DEFAULT ''"),
            ("request_path", "ALTER TABLE collection_tasks ADD COLUMN request_path TEXT NOT NULL DEFAULT ''"),
        ]:
            if column_name not in collection_task_columns:
                db.execute(ddl)
        api_count = db.execute("SELECT COUNT(*) AS total FROM api_configs").fetchone()["total"]
        if api_count == 0:
            timestamp = now_text()
            db.executemany(
                "INSERT INTO api_configs (key, name, enabled, base_url, model, api_key, usage, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                [
                    ("deepseek", "DeepSeek 文案生成", 1, "https://api.deepseek.com", "deepseek-chat", "", "标题生成 / 文案优化", timestamp),
                    ("image", "Nano Banana 图生图", 1, NANOBANANA_SUBMIT_URL, "nano-banana", "", "图片处理 / 图生图", timestamp),
                ],
            )
        else:
            deepseek_api = db.execute("SELECT * FROM api_configs WHERE key = 'deepseek'").fetchone()
            if deepseek_api and (looks_corrupted_text(deepseek_api["name"]) or looks_corrupted_text(deepseek_api["usage"])):
                db.execute(
                    "UPDATE api_configs SET name = ?, usage = ?, updated_at = ? WHERE key = 'deepseek'",
                    ("DeepSeek 文案生成", "标题生成 / 文案优化", now_text()),
                )
            image_api = db.execute("SELECT * FROM api_configs WHERE key = 'image'").fetchone()
            if image_api and not image_api["base_url"] and image_api["model"] == "image-to-image":
                db.execute(
                    "UPDATE api_configs SET name = ?, base_url = ?, model = ?, usage = ?, updated_at = ? WHERE key = 'image'",
                    ("Nano Banana 图生图", NANOBANANA_SUBMIT_URL, "nano-banana", "图片处理 / 图生图", now_text()),
                )
        setting_count = db.execute("SELECT COUNT(*) AS total FROM app_settings").fetchone()["total"]
        if setting_count == 0:
            timestamp = now_text()
            db.executemany(
                "INSERT INTO app_settings (key, value, updated_at) VALUES (?, ?, ?)",
                [
                    ("database", "data/app.db", timestamp),
                    ("image_dir", "data/images", timestamp),
                    ("run_mode", "headless", timestamp),
                    ("max_retries", "2", timestamp),
                    ("cookie_path", "data/dxm_cookies.json", timestamp),
                    ("script_dir", str(SCRIPT_SOURCE_DIR), timestamp),
                    ("enable_real_rpa", "false", timestamp),
                    ("collection_mode", "1688", timestamp),
                    ("enable_external_collection", "false", timestamp),
                    ("onebound_key", "", timestamp),
                    ("onebound_secret", "", timestamp),
                    ("1688_cookie", "", timestamp),
                    ("1688_cookie_path", "data/1688_cookies.json", timestamp),
                    ("miaoshou_default_suggested_price_usd", "60", timestamp),
                    ("upload_image_source", "", timestamp),
                    ("cos_region", "", timestamp),
                    ("cos_bucket", "", timestamp),
                    ("cos_prefix", "", timestamp),
                    ("executor_mode", "local_python", timestamp),
                    ("executor_server_url", "http://127.0.0.1:8000", timestamp),
                    ("executor_bind_code", "", timestamp),
                    ("executor_download_url", "", timestamp),
                    ("executor_version", "0.1.0", timestamp),
                    ("executor_poll_seconds", "5", timestamp),
                    ("executor_heartbeat_timeout", "60", timestamp),
                    ("executor_task_scope", "manual", timestamp),
                    ("upload_fill_skc", "true", timestamp),
                    ("upload_skc_missing_policy", "pause", timestamp),
                    ("upload_auto_submit", "false", timestamp),
                    ("upload_error_policy", "skip", timestamp),
                    ("upload_save_screenshots", "false", timestamp),
                    ("upload_save_html", "false", timestamp),
                    ("upload_trace", "off", timestamp),
                    ("upload_step_delay_ms", "500", timestamp),
                    ("temu_shop_account", "", timestamp),
                    ("temu_site", "美国站", timestamp),
                    ("temu_product_template", "", timestamp),
                    ("temu_size_category", "", timestamp),
                    ("temu_size_template", "", timestamp),
                    ("temu_warehouse_template", "", timestamp),
                    ("temu_logistics_template", "", timestamp),
                    ("temu_ship_days", "9", timestamp),
                    ("temu_declare_markup", "239.0", timestamp),
                    ("temu_default_weight_g", "350", timestamp),
                    ("temu_default_stock", "999", timestamp),
                    ("temu_package_length_cm", "10", timestamp),
                    ("temu_package_width_cm", "5", timestamp),
                    ("temu_package_height_cm", "1", timestamp),
                    ("temu_1688_excel_path", "", timestamp),
                    ("temu_batch_limit", "", timestamp),
                    ("temu_start_skc", "", timestamp),
                    ("temu_append_sku_suffix", "true", timestamp),
                    ("temu_add_model_info", "false", timestamp),
                    ("temu_model_index", "2", timestamp),
                ],
            )
        else:
            timestamp = now_text()
            defaults = {
                "collection_mode": "1688",
                "enable_external_collection": "false",
                "onebound_key": "",
                "onebound_secret": "",
                "1688_cookie": "",
                "1688_cookie_path": "data/1688_cookies.json",
                "script_dir": str(SCRIPT_SOURCE_DIR),
                "miaoshou_default_suggested_price_usd": "60",
                "upload_image_source": "",
                "cos_region": "",
                "cos_bucket": "",
                "cos_prefix": "",
                "executor_mode": "local_python",
                "executor_server_url": "http://127.0.0.1:8000",
                "executor_bind_code": "",
                "executor_download_url": "",
                "executor_version": "0.1.0",
                "executor_poll_seconds": "5",
                "executor_heartbeat_timeout": "60",
                "executor_task_scope": "manual",
                "upload_fill_skc": "true",
                "upload_skc_missing_policy": "pause",
                "upload_auto_submit": "false",
                "upload_error_policy": "skip",
                "upload_save_screenshots": "false",
                "upload_save_html": "false",
                "upload_trace": "off",
                "upload_step_delay_ms": "500",
                "temu_shop_account": "",
                "temu_site": "美国站",
                "temu_product_template": "",
                "temu_size_category": "",
                "temu_size_template": "",
                "temu_warehouse_template": "",
                "temu_logistics_template": "",
                "temu_ship_days": "9",
                "temu_declare_markup": "239.0",
                "temu_default_weight_g": "350",
                "temu_default_stock": "999",
                "temu_package_length_cm": "10",
                "temu_package_width_cm": "5",
                "temu_package_height_cm": "1",
                "temu_1688_excel_path": "",
                "temu_batch_limit": "",
                "temu_start_skc": "",
                "temu_append_sku_suffix": "true",
                "temu_add_model_info": "false",
                "temu_model_index": "2",
            }
            for key, value in defaults.items():
                exists = db.execute("SELECT 1 FROM app_settings WHERE key = ?", (key,)).fetchone()
                if not exists:
                    db.execute("INSERT INTO app_settings (key, value, updated_at) VALUES (?, ?, ?)", (key, value, timestamp))
        prompt_count = db.execute("SELECT COUNT(*) AS total FROM prompt_templates").fetchone()["total"]
        corrupt_prompt_count = db.execute(
            """
            SELECT COUNT(*) AS total FROM prompt_templates
            WHERE name LIKE '%???%' OR category LIKE '%???%' OR prompt_type LIKE '%???%' OR usage LIKE '%???%' OR content LIKE '%???%' OR status LIKE '%???%'
            """
        ).fetchone()["total"]
        if prompt_count and corrupt_prompt_count:
            db.execute("DELETE FROM prompt_templates")
            prompt_count = 0
        if prompt_count == 0:
            timestamp = now_text()
            db.executemany(
                "INSERT INTO prompt_templates (name, category, prompt_type, usage, content, status, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                [(*template, timestamp) for template in DEFAULT_PROMPT_TEMPLATES],
            )


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/")
def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/image-proxy")
def image_proxy(url: str) -> Response:
    parsed = urllib.parse.urlparse(url)
    allowed_hosts = {"cbu01.alicdn.com", "cbu02.alicdn.com", "cbu03.alicdn.com", "img.alicdn.com"}
    if parsed.scheme not in {"http", "https"} or parsed.netloc not in allowed_hosts:
        raise HTTPException(status_code=400, detail="不支持的图片域名")
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "Referer": "https://detail.1688.com/",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            content = response.read()
            content_type = response.headers.get("Content-Type", "image/jpeg")
    except urllib.error.HTTPError as exc:
        raise HTTPException(status_code=exc.code, detail="图片代理请求失败") from exc
    except urllib.error.URLError as exc:
        raise HTTPException(status_code=502, detail=f"图片代理连接失败：{exc.reason}") from exc
    return Response(content=content, media_type=content_type, headers={"Cache-Control": "public, max-age=86400"})


def fetch_external_image(url: str) -> tuple[bytes, str]:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("unsupported image url")
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "Referer": "https://detail.1688.com/",
        },
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=25) as response:
        content_type = response.headers.get("Content-Type", "image/jpeg")
        return response.read(), content_type


def save_product_main_image_from_url(product_id: int, image_url: str) -> str:
    if not image_url:
        return ""
    try:
        content, content_type = fetch_external_image(image_url)
    except (urllib.error.URLError, TimeoutError, ValueError):
        return ""
    extension = ".jpg"
    if "png" in content_type:
        extension = ".png"
    elif "webp" in content_type:
        extension = ".webp"
    product_dir = IMAGE_DIR / str(product_id)
    product_dir.mkdir(parents=True, exist_ok=True)
    target = product_dir / f"main{extension}"
    for old_file in product_dir.glob("main.*"):
        old_file.unlink(missing_ok=True)
    target.write_bytes(content)
    return f"/images/{product_id}/{target.name}"


def image_extension_from_content_type(content_type: str, fallback_url: str = "") -> str:
    if "png" in content_type:
        return ".png"
    if "webp" in content_type:
        return ".webp"
    if "gif" in content_type:
        return ".gif"
    suffix = Path(urllib.parse.urlparse(fallback_url).path).suffix.lower()
    return suffix if suffix in {".jpg", ".jpeg", ".png", ".webp", ".gif"} else ".jpg"


def save_processed_image_from_url(product_id: int, image_url: str) -> str:
    content, content_type = fetch_external_image(image_url)
    extension = image_extension_from_content_type(content_type, image_url)
    product_dir = IMAGE_DIR / str(product_id)
    product_dir.mkdir(parents=True, exist_ok=True)
    target = product_dir / f"processed{extension}"
    for old_file in product_dir.glob("processed.*"):
        old_file.unlink(missing_ok=True)
    target.write_bytes(content)
    return f"/images/{product_id}/{target.name}"


def image_task_from_row(row: sqlite3.Row) -> ImageTask:
    return ImageTask(**dict(row))


def image_preview_url(image_url: str) -> str:
    clean_url = str(image_url or "").strip()
    if clean_url.startswith("http"):
        return f"/api/image-proxy?url={urllib.parse.quote(clean_url, safe='')}"
    return clean_url


def add_image_option(options: list[ImageOption], seen: set[str], label: str, url: str, kind: str, color: str = "", size: str = "", sku_id: str = "") -> None:
    clean_url = str(url or "").strip()
    dedupe_key = "::".join([kind, clean_url, str(color or ""), str(size or "")])
    if not clean_url or dedupe_key in seen:
        return
    if clean_url.startswith("http") and not re.search(r"\.(jpg|jpeg|png|webp|gif)(\?|$)", clean_url, re.I):
        return
    seen.add(dedupe_key)
    options.append(ImageOption(label=label, url=clean_url, kind=kind, preview_url=image_preview_url(clean_url), color=color, size=size, sku_id=sku_id))


def build_product_image_options(product_id: int, main_image: str = "", source_url: str = "") -> list[ImageOption]:
    options: list[ImageOption] = []
    seen: set[str] = set()
    add_image_option(options, seen, "商品主图", main_image, "main_image")
    product_dir = IMAGE_DIR / str(product_id)
    if product_dir.exists():
        for image_path in sorted(product_dir.iterdir(), key=lambda item: item.stat().st_mtime, reverse=True):
            if image_path.is_file() and image_path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
                add_image_option(options, seen, f"本地图片：{image_path.name}", f"/images/{product_id}/{image_path.name}", "local_file")
    if source_url.startswith("http"):
        add_image_option(options, seen, "处理字段站外链接", source_url, "source_url")
    with connect() as db:
        sku_images = db.execute(
            """
            SELECT sku_id, color, size, image_url, source FROM product_sku_images
            WHERE product_id = ? AND image_url != ''
            ORDER BY sort_order, id
            """,
            (product_id,),
        ).fetchall()
        for row in sku_images:
            parts = [part for part in [row["color"], row["size"]] if part]
            label = "详情图" + (f"：{' / '.join(parts)}" if parts else "")
            add_image_option(options, seen, label, row["image_url"], row["source"] or "detail_image", row["color"], row["size"], row["sku_id"])
        product = db.execute("SELECT title FROM products WHERE id = ?", (product_id,)).fetchone()
        if product:
            rows = db.execute(
                """
                SELECT source, image_url FROM collection_items
                WHERE image_url != '' AND (source_url = ? OR title = ?)
                ORDER BY id DESC LIMIT 12
                """,
                (source_url, product["title"]),
            ).fetchall()
            for row in rows:
                add_image_option(options, seen, f"采集图：{row['source']}", row["image_url"], "collection_image")
    return options


def color_image_assignment_from_row(row: sqlite3.Row) -> ColorImageAssignment:
    return ColorImageAssignment(
        color=row["color"],
        image_url=row["image_url"],
        preview_url=image_preview_url(row["image_url"]),
        source=row["source"],
        sort_order=int(row["sort_order"]),
        is_auto=bool(row["is_auto"]),
        confidence=float(row["confidence"] or 0),
    )


def list_color_image_assignments(product_id: int) -> list[ColorImageAssignment]:
    with connect() as db:
        rows = db.execute(
            """
            SELECT * FROM product_color_image_assignments
            WHERE product_id = ?
            ORDER BY color, sort_order, id
            """,
            (product_id,),
        ).fetchall()
    return [color_image_assignment_from_row(row) for row in rows]


def detail_image_assignment_from_row(row: sqlite3.Row) -> DetailImageAssignment:
    image_url = row["image_url"] or ""
    return DetailImageAssignment(
        image_url=image_url,
        preview_url=image_preview_url(image_url) if image_url else "",
        source=row["source"],
        sort_order=int(row["sort_order"]),
    )


def list_detail_image_assignments(product_id: int) -> list[DetailImageAssignment]:
    with connect() as db:
        rows = db.execute(
            """
            SELECT * FROM product_detail_image_assignments
            WHERE product_id = ?
            ORDER BY sort_order, id
            """,
            (product_id,),
        ).fetchall()
    return [detail_image_assignment_from_row(row) for row in rows]


def image_identity_server(url: str) -> str:
    clean_url = str(url or "").strip()
    if not clean_url:
        return ""
    parsed = urllib.parse.urlsplit(clean_url)
    if parsed.scheme and parsed.netloc:
        return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))
    return clean_url.split("?", 1)[0]


def normalize_color_alias(value: object) -> str:
    return re.sub(r"[\s\-_【】\[\]（）(){}:：,，/\\|;；]+", "", str(value or "").strip().lower())


COLOR_ALIAS_MAP = {normalize_color_alias(alias): color for alias, color in COLOR_ALIAS_ENTRIES}


def resolve_known_color(value: str) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    normalized = normalize_color_alias(text)
    if normalized in COLOR_ALIAS_MAP:
        return COLOR_ALIAS_MAP[normalized]
    for part in re.split(r"[\r\n,，、/]+", text):
        color = COLOR_ALIAS_MAP.get(normalize_color_alias(part))
        if color:
            return color
    for alias, color in COLOR_ALIAS_MAP.items():
        if alias and alias in normalized:
            return color
    return ""


def clean_color_label(value: str) -> str:
    text = str(value or "").strip()
    match = re.search(r"颜色[:：]([^;/\\|]+)", text)
    if match:
        text = match.group(1)
    text = text.replace("（", "(").replace("）", ")").strip()
    return resolve_known_color(text)


def safe_path_segment(value: str, fallback: str = "item") -> str:
    text = str(value or "").strip() or fallback
    text = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", text)
    text = re.sub(r"\s+", "_", text).strip(" ._")
    return text[:80] or fallback


def contains_cjk(value: str) -> bool:
    return bool(re.search(r"[\u3400-\u9fff]", str(value or "")))


def english_title_fallback(source_title: str) -> str:
    text = str(source_title or "").lower()
    parts: list[str] = []
    if any(keyword in text for keyword in ["牛仔", "denim", "jean"]):
        parts.append("Denim")
    if any(keyword in text for keyword in ["短裤", "short"]):
        parts.append("Shorts")
    elif any(keyword in text for keyword in ["裤", "pant"]):
        parts.append("Pants")
    else:
        parts.append("Fashion Item")
    if any(keyword in text for keyword in ["女", "女士", "women", "ladies"]):
        parts.insert(0, "Women's")
    if any(keyword in text for keyword in ["高腰", "high waist", "high-waist"]):
        parts.append("High Waist")
    if any(keyword in text for keyword in ["宽松", "loose"]):
        parts.append("Loose Fit")
    if any(keyword in text for keyword in ["夏", "summer"]):
        parts.append("Summer")
    title = " ".join(dict.fromkeys(part for part in parts if part)).strip()
    if len(title) < 18:
        title = f"{title} Casual Everyday Bottoms"
    return title[:120]


def valid_english_title(value: str) -> bool:
    text = str(value or "").strip()
    return bool(text) and not contains_cjk(text)


def local_image_path_from_url(image_url: str) -> Path | None:
    clean_url = str(image_url or "").strip()
    if not clean_url.startswith("/images/"):
        return None
    relative_path = clean_url.removeprefix("/images/").split("?", 1)[0]
    candidate = (IMAGE_DIR / relative_path).resolve()
    try:
        candidate.relative_to(IMAGE_DIR.resolve())
    except ValueError:
        return None
    return candidate if candidate.is_file() else None


def materialize_image_for_rpa(image_url: str, target: Path) -> bool:
    local_path = local_image_path_from_url(image_url)
    target.parent.mkdir(parents=True, exist_ok=True)
    if local_path:
        shutil.copyfile(local_path, target)
        return True
    if str(image_url or "").startswith("http"):
        try:
            content, _content_type = fetch_external_image(image_url)
        except (urllib.error.URLError, TimeoutError, ValueError):
            return False
        target.write_bytes(content)
        return True
    return False


def extract_json_object(text: str) -> dict[str, object]:
    try:
        parsed = json.loads(text)
        return parsed if isinstance(parsed, dict) else {}
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        return {}
    try:
        parsed = json.loads(match.group(0))
        return parsed if isinstance(parsed, dict) else {}
    except json.JSONDecodeError:
        return {}


def get_vision_api_config() -> sqlite3.Row | None:
    with connect() as db:
        return db.execute("SELECT * FROM api_configs WHERE key = 'vision'").fetchone()


def normalize_chat_completions_endpoint(base_url: str) -> str:
    endpoint = (base_url or "https://ark.cn-beijing.volces.com/api/v3").strip().rstrip("/")
    if endpoint.endswith("/chat/completions"):
        return endpoint
    if endpoint.endswith("/responses"):
        endpoint = endpoint[: -len("/responses")]
    return f"{endpoint}/chat/completions"


def normalize_color_text(value: object) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"[\s\-_【】\[\]（）(){}:：,，/\\|]+", "", text)
    return text


def resolve_matched_color(candidate: str, colors: list[str]) -> str:
    candidate_text = str(candidate or "").strip()
    if not candidate_text:
        return ""
    if candidate_text in colors:
        return candidate_text
    normalized_candidate = normalize_color_text(candidate_text)
    if not normalized_candidate:
        return ""
    for color in colors:
        if normalize_color_text(color) == normalized_candidate:
            return color
    for color in colors:
        normalized_color = normalize_color_text(color)
        if normalized_candidate and normalized_candidate in normalized_color:
            return color
    for color in colors:
        normalized_color = normalize_color_text(color)
        if normalized_color and normalized_color in normalized_candidate:
            return color
    return ""


def active_prompt_template(prompt_type: str, usage: str = "") -> str:
    enabled_status = chr(0x542f) + chr(0x7528) + chr(0x4e2d)
    clauses = ["prompt_type = ?", "status = ?"]
    params: list[object] = [prompt_type, enabled_status]
    if usage:
        clauses.append("usage = ?")
        params.append(usage)
    with connect() as db:
        row = db.execute(
            f"SELECT content FROM prompt_templates WHERE {' AND '.join(clauses)} ORDER BY id DESC LIMIT 1",
            params,
        ).fetchone()
    return row["content"] if row else ""


def active_title_prompt_template() -> str:
    title_prompt_type = chr(0x6807) + chr(0x9898) + chr(0x63d0) + chr(0x793a) + chr(0x8bcd)
    title_usage = chr(0x6807) + chr(0x9898) + chr(0x751f) + chr(0x6210)
    enabled_status = chr(0x542f) + chr(0x7528) + chr(0x4e2d)
    with connect() as db:
        row = db.execute(
            """
            SELECT content FROM prompt_templates
            WHERE status = ? AND prompt_type = ? AND usage = ?
            ORDER BY id DESC LIMIT 1
            """,
            (enabled_status, title_prompt_type, title_usage),
        ).fetchone()
        if not row:
            row = db.execute(
                """
                SELECT content FROM prompt_templates
                WHERE status = ? AND content LIKE '%{orig_title}%' AND content LIKE '%{attrs_text}%'
                ORDER BY id DESC LIMIT 1
                """,
                (enabled_status,),
            ).fetchone()
    return row["content"] if row else ""


def render_title_prompt(template: str, item: ProcessingItem) -> str:
    attrs = [
        f"SKC: {item.skc}",
        f"Color: {item.color}",
        f"Size: {item.size}",
        f"SKU Code: {item.sku_code}",
        f"Source URL: {item.source_url}",
    ]
    attrs_text = "\n".join(part for part in attrs if not part.endswith(": "))
    prompt = template or ""
    replacements = {
        "orig_title": item.title,
        "attrs_text": attrs_text,
        "skc": item.skc,
        "color": item.color,
        "size": item.size,
        "sku_code": item.sku_code,
        "source_url": item.source_url,
    }
    for key, value in replacements.items():
        prompt = prompt.replace("{" + key + "}", str(value or ""))
    if "{orig_title}" not in template and "{attrs_text}" not in template:
        prompt = f"{prompt}\n\nSource title: {item.title}\nAttributes:\n{attrs_text}".strip()
    return prompt


def extract_title_from_model_response(response_text: str, fallback_source_title: str) -> str:
    text = str(response_text or "").strip().strip("` ")
    if text.startswith("json"):
        text = text[4:].strip()
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            title = str(parsed.get("title_en") or parsed.get("english_title") or parsed.get("title") or "").strip()
            if title:
                return title[:120]
    except Exception:
        pass
    return text.strip('\"??')[:120] or english_title_fallback(fallback_source_title)


def image_url_for_vision(image_url: str) -> str:
    clean_url = str(image_url or "").strip()
    if clean_url.startswith(("http://", "https://", "data:image/")):
        return clean_url
    if clean_url.startswith("/images/"):
        relative_path = clean_url.removeprefix("/images/").replace("/", os.sep)
        image_path = (IMAGE_DIR / relative_path).resolve()
        if not str(image_path).startswith(str(IMAGE_DIR.resolve())) or not image_path.is_file():
            raise HTTPException(status_code=400, detail=f"本地图片不存在，无法视觉识别：{clean_url}")
        mime_type = mimetypes.guess_type(str(image_path))[0] or "image/jpeg"
        return f"data:{mime_type};base64,{base64.b64encode(image_path.read_bytes()).decode('ascii')}"
    raise HTTPException(status_code=400, detail=f"豆包视觉识别只支持 http/https 或本地 /images 图片：{clean_url}")


def call_doubao_vision_color(image_url: str, colors: list[str]) -> dict[str, object]:
    config = get_vision_api_config()
    if not config or not config["enabled"] or not config["api_key"]:
        raise HTTPException(status_code=400, detail="豆包视觉识别 API 未配置或未启用")
    endpoint = normalize_chat_completions_endpoint(config["base_url"] or "https://ark.cn-beijing.volces.com/api/v3")
    model = config["model"] or "doubao-1.5-vision-pro-32k"
    color_json = json.dumps(colors, ensure_ascii=False)
    prompt_template = active_prompt_template("图片识别提示词", "颜色分图")
    if not prompt_template:
        prompt_template = next((item[4] for item in DEFAULT_PROMPT_TEMPLATES if item[2] == "图片识别提示词" and item[3] == "颜色分图"), "")
    prompt = prompt_template.replace("{color_json}", color_json).strip()

    body = json.dumps(
        {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url_for_vision(image_url)}},
                    ],
                }
            ],
            "temperature": 0,
            "max_tokens": 300,
        },
        ensure_ascii=False,
    ).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {config['api_key']}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise HTTPException(status_code=502, detail=f"豆包视觉识别失败：{exc.code} {detail}") from exc
    except urllib.error.URLError as exc:
        raise HTTPException(status_code=502, detail=f"豆包视觉识别连接失败：{exc.reason}") from exc
    content = (((payload.get("choices") or [{}])[0].get("message") or {}).get("content") or "").strip()
    result = extract_json_object(content)
    matched_color = resolve_matched_color(str(result.get("matched_color") or "").strip(), colors)
    return {
        "matched_color": matched_color,
        "confidence": to_float(result.get("confidence"), 0),
        "is_product_image": bool(result.get("is_product_image", True)),
        "reason": str(result.get("reason") or ""),
        "raw": payload,
    }


def get_or_create_vision_match(product_id: int, option: ImageOption, colors: list[str], allow_api: bool) -> dict[str, object] | None:
    identity = image_identity_server(option.url)
    if not identity:
        return None
    with connect() as db:
        cached = db.execute(
            "SELECT * FROM product_image_vision_cache WHERE product_id = ? AND image_identity = ?",
            (product_id, identity),
        ).fetchone()
    if cached:
        try:
            cached_raw = json.loads(cached["raw_json"] or "{}")
        except json.JSONDecodeError:
            cached_raw = {}
        if cached_raw.get("cache_version") == VISION_CACHE_VERSION:
            return {"matched_color": cached["matched_color"], "confidence": float(cached["confidence"] or 0), "is_product_image": bool(cached["is_product_image"]), "status": cached["status"]}
    if not allow_api:
        return None
    result = call_doubao_vision_color(option.url, colors)
    result["cache_version"] = VISION_CACHE_VERSION
    timestamp = now_text()
    with connect() as db:
        db.execute(
            """
            INSERT INTO product_image_vision_cache
            (product_id, image_identity, image_url, matched_color, confidence, is_product_image, status, provider, raw_json, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'doubao', ?, ?, ?)
            ON CONFLICT(product_id, image_identity) DO UPDATE SET
              image_url=excluded.image_url, matched_color=excluded.matched_color, confidence=excluded.confidence,
              is_product_image=excluded.is_product_image, status=excluded.status, provider=excluded.provider,
              raw_json=excluded.raw_json, updated_at=excluded.updated_at
            """,
            (
                product_id,
                identity,
                option.url,
                result["matched_color"],
                result["confidence"],
                1 if result["is_product_image"] else 0,
                "matched" if result["matched_color"] else "unmatched",
                json.dumps(result, ensure_ascii=False),
                timestamp,
                timestamp,
            ),
        )
        db.commit()
    return result


def unique_options_for_assignment(options: list[ImageOption]) -> list[ImageOption]:
    seen: set[str] = set()
    unique_options: list[ImageOption] = []
    for option in options:
        key = image_identity_server(option.url)
        if not key or key in seen:
            continue
        seen.add(key)
        unique_options.append(option)
    return unique_options


def auto_assign_color_images(payload: AutoAssignColorImagesPayload) -> AutoAssignColorImagesResult:
    if payload.use_vision and not payload.user_confirmed_vision:
        raise HTTPException(status_code=409, detail="图片识别会调用视觉 API 并可能产生费用，请先确认后再执行")
    count_per_color = max(1, min(int(payload.count_per_color or 3), 10))
    with connect() as db:
        product = db.execute("SELECT * FROM products WHERE id = ?", (payload.product_id,)).fetchone()
        override = db.execute("SELECT source_url FROM processing_overrides WHERE product_id = ?", (payload.product_id,)).fetchone()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    source_url = override["source_url"] if override and override["source_url"] else ""
    image_options = build_product_image_options(payload.product_id, product["main_image"] or "", source_url)
    sku_options = unique_options_for_assignment([option for option in image_options if option.kind == "detail_sku_image" and option.color])
    supplement_options = unique_options_for_assignment([
        option for option in image_options
        if option.kind in {"detail_desc_image", "detail_main_image", "collection_image", "main_image"}
    ])
    colors = sorted({clean_color_label(option.color) for option in sku_options if clean_color_label(option.color)})
    if not colors:
        return AutoAssignColorImagesResult(product_id=payload.product_id, count_per_color=count_per_color, assigned_count=0, colors={})
    vision_by_color: dict[str, list[tuple[ImageOption, float]]] = {color: [] for color in colors}
    if payload.use_vision and colors:
        for option in supplement_options[:40]:
            match = get_or_create_vision_match(payload.product_id, option, colors, payload.user_confirmed_vision)
            if not match or not match.get("is_product_image"):
                continue
            matched_color = str(match.get("matched_color") or "")
            confidence = float(match.get("confidence") or 0)
            if matched_color in vision_by_color and confidence >= 0.75:
                vision_by_color[matched_color].append((option, confidence))
    timestamp = now_text()
    assigned_by_color: dict[str, list[tuple[ImageOption, float]]] = {}
    used_global: set[str] = set()
    for color in colors:
        direct = [option for option in sku_options if clean_color_label(option.color) == color]
        picked: list[tuple[ImageOption, float]] = []
        used_local: set[str] = set()
        for option in direct:
            key = image_identity_server(option.url)
            if key and key not in used_local:
                picked.append((option, 0.98))
                used_local.add(key)
            if len(picked) >= count_per_color:
                break
        candidate_supplements = vision_by_color.get(color) if payload.use_vision else []
        if not candidate_supplements:
            candidate_supplements = [(option, 0.55) for option in supplement_options]
        for option, confidence in candidate_supplements:
            key = image_identity_server(option.url)
            if not key or key in used_local or key in used_global:
                continue
            picked.append((option, confidence))
            used_local.add(key)
            if len(picked) >= count_per_color:
                break
        for option, _confidence in picked:
            key = image_identity_server(option.url)
            if key:
                used_global.add(key)
        assigned_by_color[color] = picked[:count_per_color]
    with connect() as db:
        db.execute("DELETE FROM product_color_image_assignments WHERE product_id = ?", (payload.product_id,))
        assigned_count = 0
        for color, picked in assigned_by_color.items():
            for sort_order, (option, confidence) in enumerate(picked):
                db.execute(
                    """
                    INSERT INTO product_color_image_assignments
                    (product_id, color, image_url, source, sort_order, is_auto, confidence, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, 1, ?, ?, ?)
                    """,
                    (payload.product_id, color, option.url, option.kind, sort_order, confidence, timestamp, timestamp),
                )
                assigned_count += 1
        db.commit()
    return AutoAssignColorImagesResult(
        product_id=payload.product_id,
        count_per_color=count_per_color,
        assigned_count=assigned_count,
        colors={color: len(picked) for color, picked in assigned_by_color.items()},
    )


def save_manual_color_image_assignment(payload: ManualColorImageAssignmentPayload) -> list[ColorImageAssignment]:
    color = str(payload.color or "").strip()
    image_url = str(payload.image_url or "").strip()
    slot_index = max(0, min(4, int(payload.slot_index or 0)))
    if not color:
        raise HTTPException(status_code=400, detail="颜色不能为空")
    with connect() as db:
        product = db.execute("SELECT id FROM products WHERE id = ?", (payload.product_id,)).fetchone()
        if not product:
            raise HTTPException(status_code=404, detail="商品不存在")
        timestamp = now_text()
        db.execute(
            "DELETE FROM product_color_image_assignments WHERE product_id = ? AND color = ? AND sort_order = ?",
            (payload.product_id, color, slot_index),
        )
        if image_url:
            db.execute(
                """
                INSERT INTO product_color_image_assignments
                (product_id, color, image_url, source, sort_order, is_auto, confidence, created_at, updated_at)
                VALUES (?, ?, ?, 'manual_drag', ?, 0, 1, ?, ?)
                """,
                (payload.product_id, color, image_url, slot_index, timestamp, timestamp),
            )
        db.commit()
    return list_color_image_assignments(payload.product_id)


def save_detail_image_slot(product_id: int, slot_index: int, image_url: str) -> list[DetailImageAssignment]:
    clean_url = str(image_url or "").strip()
    safe_slot_index = max(0, min(19, int(slot_index or 0)))
    with connect() as db:
        product = db.execute("SELECT id FROM products WHERE id = ?", (product_id,)).fetchone()
        if not product:
            raise HTTPException(status_code=404, detail="商品不存在")
        timestamp = now_text()
        db.execute(
            "DELETE FROM product_detail_image_assignments WHERE product_id = ? AND sort_order = ?",
            (product_id, safe_slot_index),
        )
        db.execute(
            """
            INSERT INTO product_detail_image_assignments
            (product_id, image_url, source, sort_order, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (product_id, clean_url, 'manual_drag' if clean_url else 'manual_clear', safe_slot_index, timestamp, timestamp),
        )
        db.commit()
    return list_detail_image_assignments(product_id)


def save_manual_detail_image_assignment(payload: ManualDetailImageAssignmentPayload) -> list[DetailImageAssignment]:
    return save_detail_image_slot(payload.product_id, payload.slot_index, payload.image_url)


def normalize_image_dedupe_key(image_url: str) -> str:
    clean_url = str(image_url or "").strip()
    if not clean_url:
        return ""
    parsed = urllib.parse.urlsplit(clean_url)
    if parsed.scheme and parsed.netloc:
        return urllib.parse.urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path, "", ""))
    return clean_url.replace("\\", "/").strip().lower()


def dedupe_processing_images(product_ids: list[int]) -> DedupeProcessingImagesResult:
    safe_ids = [int(product_id) for product_id in product_ids if int(product_id) > 0]
    if not safe_ids:
        raise HTTPException(status_code=400, detail="请选择要去重的商品")
    scanned_count = 0
    detail_removed_count = 0
    color_removed_count = 0
    with connect() as db:
        for product_id in safe_ids:
            seen: set[str] = set()
            detail_rows = db.execute(
                "SELECT id, image_url FROM product_detail_image_assignments WHERE product_id = ? AND image_url != '' ORDER BY sort_order, id",
                (product_id,),
            ).fetchall()
            color_rows = db.execute(
                "SELECT id, image_url FROM product_color_image_assignments WHERE product_id = ? AND image_url != '' ORDER BY color, sort_order, id",
                (product_id,),
            ).fetchall()
            for row in list(detail_rows) + list(color_rows):
                dedupe_key = normalize_image_dedupe_key(row["image_url"])
                if dedupe_key:
                    scanned_count += 1
                    seen.add(dedupe_key)
            duplicate_detail_ids: list[int] = []
            duplicate_color_ids: list[int] = []
            seen.clear()
            for row in detail_rows:
                dedupe_key = normalize_image_dedupe_key(row["image_url"])
                if not dedupe_key:
                    continue
                if dedupe_key in seen:
                    duplicate_detail_ids.append(int(row["id"]))
                else:
                    seen.add(dedupe_key)
            for row in color_rows:
                dedupe_key = normalize_image_dedupe_key(row["image_url"])
                if not dedupe_key:
                    continue
                if dedupe_key in seen:
                    duplicate_color_ids.append(int(row["id"]))
                else:
                    seen.add(dedupe_key)
            if duplicate_detail_ids:
                placeholders = ",".join("?" for _ in duplicate_detail_ids)
                db.execute(f"DELETE FROM product_detail_image_assignments WHERE id IN ({placeholders})", duplicate_detail_ids)
                detail_removed_count += len(duplicate_detail_ids)
            if duplicate_color_ids:
                placeholders = ",".join("?" for _ in duplicate_color_ids)
                db.execute(f"DELETE FROM product_color_image_assignments WHERE id IN ({placeholders})", duplicate_color_ids)
                color_removed_count += len(duplicate_color_ids)
    removed_count = detail_removed_count + color_removed_count
    return DedupeProcessingImagesResult(
        product_count=len(safe_ids),
        scanned_count=scanned_count,
        removed_count=removed_count,
        detail_removed_count=detail_removed_count,
        color_removed_count=color_removed_count,
    )


def get_image_api_config() -> sqlite3.Row | None:
    with connect() as db:
        return db.execute("SELECT * FROM api_configs WHERE key = 'image'").fetchone()


def nanobanana_submit(api_key: str, image_url: str, prompt: str, size: str = "1344x1792", aspect_ratio: str = "3:4") -> str:
    body = json.dumps({"key": api_key, "prompt": prompt, "size": size, "aspectRatio": aspect_ratio, "urls": [image_url]}).encode("utf-8")
    request = urllib.request.Request(NANOBANANA_SUBMIT_URL, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise HTTPException(status_code=502, detail=f"图生图提交失败：{exc.code} {detail}") from exc
    except urllib.error.URLError as exc:
        raise HTTPException(status_code=502, detail=f"图生图连接失败：{exc.reason}") from exc
    except TimeoutError as exc:
        raise HTTPException(status_code=504, detail="图生图提交超时") from exc
    task_id = (payload.get("data") or {}).get("id")
    if not task_id:
        raise HTTPException(status_code=502, detail=f"图生图提交失败：服务商未返回任务 ID，返回：{payload.get('msg') or payload.get('message') or payload.get('code')}")
    return str(task_id)


def nanobanana_query(api_key: str, task_id: str) -> dict[str, object]:
    query = urllib.parse.urlencode({"key": api_key, "id": task_id})
    request = urllib.request.Request(f"{NANOBANANA_DETAIL_URL}?{query}", headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise HTTPException(status_code=502, detail=f"图生图查询失败：{exc.code} {detail}") from exc
    except urllib.error.URLError as exc:
        raise HTTPException(status_code=502, detail=f"图生图查询连接失败：{exc.reason}") from exc
    except TimeoutError as exc:
        raise HTTPException(status_code=504, detail="图生图查询超时") from exc
    data = payload.get("data") or {}
    status_code = data.get("status")
    result_urls = data.get("result") or []
    if isinstance(result_urls, str):
        result_urls = [result_urls]
    if status_code == 2:
        return {"status": "completed", "result_urls": [url for url in result_urls if url], "note": "图生图已完成"}
    if status_code == 3:
        return {"status": "failed", "result_urls": [], "note": data.get("message") or "图生图任务失败"}
    return {"status": "processing", "result_urls": [], "note": f"图生图处理中，服务商状态：{status_code}"}


def default_english_title(title: str) -> str:
    return f"{title} for Temu listing"


def create_processing_override_for_import(db: sqlite3.Connection, product_id: int, product: ProductPayload, source_url: str, total_cost: float) -> None:
    declared_price = round(float(total_cost) + 239, 2)
    db.execute(
        """
        INSERT INTO processing_overrides (
            product_id, english_title, color, size, sku_code, declared_price,
            weight_g, length_cm, width_cm, height_cm, source_url, stock, ship_days, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(product_id) DO UPDATE SET
            english_title = excluded.english_title,
            sku_code = excluded.sku_code,
            declared_price = excluded.declared_price,
            source_url = excluded.source_url,
            updated_at = excluded.updated_at
        """,
        (
            product_id,
            default_english_title(product.title),
            "pending",
            "pending",
            f"{product.skc}-COLOR-SIZE",
            declared_price,
            350,
            15,
            10,
            2,
            source_url,
            999,
            9,
            now_text(),
        ),
    )


@app.get("/api/products", response_model=list[Product])
def list_products(q: str = "", status: str = "", image: str = "") -> list[Product]:
    keyword = f"%{q.strip()}%"
    clauses: list[str] = []
    params: list[object] = []
    if q.strip():
        clauses.append("(title LIKE ? OR skc LIKE ? OR sku_summary LIKE ?)")
        params.extend([keyword, keyword, keyword])
    if status.strip():
        clauses.append("status = ?")
        params.append(status.strip())
    if image == "has":
        clauses.append("main_image IS NOT NULL AND main_image != ''")
    elif image == "missing":
        clauses.append("(main_image IS NULL OR main_image = '')")
    where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    with connect() as db:
        rows = db.execute(f"SELECT * FROM products {where_sql} ORDER BY id DESC", params).fetchall()
    return [product_from_row(row) for row in rows]


@app.get("/api/dashboard")
def dashboard() -> dict[str, int]:
    with connect() as db:
        product_count = db.execute("SELECT COUNT(*) AS total FROM products").fetchone()["total"]
        missing_images = db.execute("SELECT COUNT(*) AS total FROM products WHERE main_image IS NULL OR main_image = ''").fetchone()["total"]
        ready_products = product_count - missing_images
        task_count = db.execute("SELECT COUNT(*) AS total FROM upload_tasks").fetchone()["total"]
        latest_ready_tasks = db.execute("SELECT COUNT(*) AS total FROM upload_tasks WHERE status IN ('export_ready', 'rpa_success')").fetchone()["total"]
    return {
        "product_count": product_count,
        "ready_products": ready_products,
        "missing_images": missing_images,
        "task_count": task_count,
        "ready_tasks": latest_ready_tasks,
    }


@app.get("/api/system/status")
def system_status() -> dict[str, object]:
    upload = upload_preflight()
    collection = collection_preflight()
    script_dir = configured_script_dir()
    cos = cos_preflight()
    checklist = [
        {"key": "database", "label": "本地数据库", "ok": DB_PATH.exists(), "action": "无需处理" if DB_PATH.exists() else "启动应用会自动创建数据库"},
        {"key": "image_dir", "label": "图片目录", "ok": IMAGE_DIR.exists(), "action": "无需处理" if IMAGE_DIR.exists() else "创建 data/images 目录"},
        {"key": "safe_rpa", "label": "真实 RPA 安全", "ok": get_setting_value("enable_real_rpa", "false") != "true", "action": "默认关闭，安全" if get_setting_value("enable_real_rpa", "false") != "true" else "确认要真实上货后再保持开启"},
        {"key": "safe_collection", "label": "外部采集安全", "ok": get_setting_value("enable_external_collection", "false") != "true", "action": "默认关闭，安全" if get_setting_value("enable_external_collection", "false") != "true" else "确认要执行外部采集后再保持开启"},
        {"key": "upload_preflight", "label": "上货预检", "ok": bool(upload["ready"]), "action": "脚本和图片目录就绪" if upload["ready"] else "检查店小秘脚本目录和图片目录"},
        {"key": "executor", "label": "本地执行器", "ok": bool(get_setting_value("executor_mode", "local_python")), "action": f"模式：{get_setting_value('executor_mode', 'local_python')}，版本：{get_setting_value('executor_version', '0.1.0')}"},
        {"key": "fill_skc", "label": "自动填写 SKC", "ok": get_setting_value("upload_fill_skc", "true") == "true", "action": "上货流程会填写商品 SKC" if get_setting_value("upload_fill_skc", "true") == "true" else "当前关闭，可能导致 SKC 空缺"},
        {"key": "collector_1688", "label": "1688 采集", "ok": bool(collection["1688"]["configured"]), "action": "万邦 API/Cookie 已配置" if collection["1688"]["configured"] else "如需 1688 真实采集，优先填写万邦 Key/Secret"},
    ]
    return {
        "database": str(DB_PATH),
        "database_exists": DB_PATH.exists(),
        "image_dir": str(IMAGE_DIR),
        "image_dir_exists": IMAGE_DIR.exists(),
        "enable_real_rpa": get_setting_value("enable_real_rpa", "false"),
        "enable_external_collection": get_setting_value("enable_external_collection", "false"),
        "collection_mode": get_setting_value("collection_mode", "1688"),
        "executor": {
            "mode": get_setting_value("executor_mode", "local_python"),
            "server_url": get_setting_value("executor_server_url", "http://127.0.0.1:8000"),
            "download_url": get_setting_value("executor_download_url", ""),
            "version": get_setting_value("executor_version", "0.1.0"),
            "poll_seconds": get_setting_value("executor_poll_seconds", "5"),
            "task_scope": get_setting_value("executor_task_scope", "manual"),
        },
        "upload_flow": {
            "fill_skc": get_setting_value("upload_fill_skc", "true"),
            "skc_missing_policy": get_setting_value("upload_skc_missing_policy", "pause"),
            "auto_submit": get_setting_value("upload_auto_submit", "false"),
            "error_policy": get_setting_value("upload_error_policy", "skip"),
            "save_screenshots": get_setting_value("upload_save_screenshots", "false"),
            "save_html": get_setting_value("upload_save_html", "false"),
            "trace": get_setting_value("upload_trace", "off"),
            "step_delay_ms": get_setting_value("upload_step_delay_ms", "500"),
        },
        "script_dir": str(script_dir),
        "script_dir_exists": script_dir.exists(),
        "cos_preflight": cos,
        "upload_preflight": upload,
        "collection_preflight": collection,
        "checklist": checklist,
    }


@app.post("/api/products", response_model=Product)
def create_product(payload: ProductPayload) -> Product:
    total_cost, estimated_profit, gross_margin = recalc(payload)
    timestamp = now_text()
    try:
        with connect() as db:
            cursor = db.execute(
                """
                INSERT INTO products (
                    title, skc, sku_summary, purchase_price, first_mile, platform_cost,
                    total_cost, estimated_profit, gross_margin, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload.title,
                    payload.skc,
                    payload.sku_summary,
                    payload.purchase_price,
                    payload.first_mile,
                    payload.platform_cost,
                    total_cost,
                    estimated_profit,
                    gross_margin,
                    payload.status,
                    timestamp,
                    timestamp,
                ),
            )
            row = db.execute("SELECT * FROM products WHERE id = ?", (cursor.lastrowid,)).fetchone()
    except sqlite3.IntegrityError as exc:
        raise HTTPException(status_code=409, detail="SKC 已存在") from exc
    return product_from_row(row)


@app.put("/api/products/{product_id}", response_model=Product)
def update_product(product_id: int, payload: ProductPayload) -> Product:
    total_cost, estimated_profit, gross_margin = recalc(payload)
    try:
        with connect() as db:
            result = db.execute(
                """
                UPDATE products
                SET title = ?, skc = ?, sku_summary = ?, purchase_price = ?, first_mile = ?,
                    platform_cost = ?, total_cost = ?, estimated_profit = ?, gross_margin = ?,
                    status = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    payload.title,
                    payload.skc,
                    payload.sku_summary,
                    payload.purchase_price,
                    payload.first_mile,
                    payload.platform_cost,
                    total_cost,
                    estimated_profit,
                    gross_margin,
                    payload.status,
                    now_text(),
                    product_id,
                ),
            )
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="商品不存在")
            row = db.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    except sqlite3.IntegrityError as exc:
        raise HTTPException(status_code=409, detail="SKC 已存在") from exc
    return product_from_row(row)


@app.post("/api/products/{product_id}/image", response_model=Product)
def upload_product_image(product_id: int, image: UploadFile = File(...)) -> Product:
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="请上传图片文件")
    suffix = Path(image.filename or "main.jpg").suffix.lower() or ".jpg"
    product_dir = IMAGE_DIR / str(product_id)
    product_dir.mkdir(parents=True, exist_ok=True)
    target = product_dir / f"main{suffix}"
    for old_file in product_dir.glob("main.*"):
        old_file.unlink(missing_ok=True)
    with target.open("wb") as file:
        shutil.copyfileobj(image.file, file)
    image_path = f"/images/{product_id}/{target.name}"
    with connect() as db:
        result = db.execute(
            "UPDATE products SET main_image = ?, status = ?, updated_at = ? WHERE id = ?",
            (image_path, "利润正常", now_text(), product_id),
        )
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="商品不存在")
        row = db.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    return product_from_row(row)


def write_placeholder_image(product_id: int, skc: str, title: str) -> str:
    product_dir = IMAGE_DIR / str(product_id)
    product_dir.mkdir(parents=True, exist_ok=True)
    target = product_dir / "main.svg"
    safe_skc = escape(skc[:32])
    safe_title = escape(title[:42])
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="1200" viewBox="0 0 900 1200">
  <defs>
    <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stop-color="#fff7ed"/>
      <stop offset="1" stop-color="#ffedd5"/>
    </linearGradient>
  </defs>
  <rect width="900" height="1200" fill="url(#bg)"/>
  <rect x="90" y="150" width="720" height="900" rx="48" fill="#ffffff" stroke="#fed7aa" stroke-width="8"/>
  <text x="450" y="460" text-anchor="middle" font-family="Arial, sans-serif" font-size="54" font-weight="700" fill="#c2410c">上货助手</text>
  <text x="450" y="550" text-anchor="middle" font-family="Arial, sans-serif" font-size="40" fill="#7c2d12">内部占位主图</text>
  <text x="450" y="660" text-anchor="middle" font-family="Arial, sans-serif" font-size="34" fill="#111827">{safe_skc}</text>
  <text x="450" y="735" text-anchor="middle" font-family="Arial, sans-serif" font-size="28" fill="#6b7280">{safe_title}</text>
  <text x="450" y="910" text-anchor="middle" font-family="Arial, sans-serif" font-size="24" fill="#9ca3af">仅用于本地 MVP 闭环验证，请替换真实商品图后再真实上货</text>
</svg>
"""
    for old_file in product_dir.glob("main.*"):
        old_file.unlink(missing_ok=True)
    target.write_text(svg, encoding="utf-8")
    return f"/images/{product_id}/{target.name}"


@app.post("/api/products/images/placeholders")
def generate_missing_image_placeholders() -> dict[str, object]:
    raise HTTPException(status_code=410, detail="本地占位主图功能已移除，请上传真实商品图")


@app.post("/api/products/images/process")
def process_product_image(payload: ProcessImagePayload) -> ImageTask:
    with connect() as db:
        product = db.execute("SELECT * FROM products WHERE id = ?", (payload.product_id,)).fetchone()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    processing_item = get_processing_item(payload.product_id)
    image_options = build_product_image_options(payload.product_id, product["main_image"] or "", processing_item.source_url.strip())
    selected_image = payload.source_image.strip() or (image_options[0].url if image_options else "")
    allowed_images = {option.url for option in image_options}
    if not selected_image:
        raise HTTPException(status_code=400, detail="商品没有可用于图生图的图片")
    if selected_image not in allowed_images:
        raise HTTPException(status_code=400, detail="请选择当前商品关联的图片进行图生图")
    if selected_image.startswith("/images/"):
        source_path = IMAGE_DIR / selected_image.removeprefix("/images/")
        if not source_path.exists():
            raise HTTPException(status_code=404, detail="所选本地图片文件不存在")
        raise HTTPException(status_code=400, detail="图生图 API 需要公网图片 URL；请选择采集图或处理字段里的站外图片链接。")
    if not selected_image.startswith("http"):
        raise HTTPException(status_code=400, detail="所选图片不是公网 URL，不能提交图生图")
    image_api = get_image_api_config()
    if not image_api or not image_api["enabled"] or not image_api["api_key"]:
        raise HTTPException(status_code=400, detail="图生图 API 未配置：请在设置中心填写 Nano Banana API Key")
    prompt = DEFAULT_IMAGE_PROMPT
    task_id = nanobanana_submit(image_api["api_key"], selected_image, prompt)
    timestamp = now_text()
    with connect() as db:
        cursor = db.execute(
            """
            INSERT INTO image_tasks (product_id, provider, task_id, status, source_image, prompt, note, created_at, updated_at)
            VALUES (?, 'nanobanana', ?, 'submitted', ?, ?, ?, ?, ?)
            """,
            (payload.product_id, task_id, selected_image, prompt, "已提交 Nano Banana 图生图任务", timestamp, timestamp),
        )
        row = db.execute("SELECT * FROM image_tasks WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return image_task_from_row(row)


@app.get("/api/products/{product_id}/image-tasks", response_model=list[ImageTask])
def list_product_image_tasks(product_id: int) -> list[ImageTask]:
    with connect() as db:
        rows = db.execute("SELECT * FROM image_tasks WHERE product_id = ? ORDER BY id DESC", (product_id,)).fetchall()
    return [image_task_from_row(row) for row in rows]


@app.post("/api/image-tasks/{task_row_id}/refresh", response_model=ImageTask)
def refresh_image_task(task_row_id: int) -> ImageTask:
    image_api = get_image_api_config()
    if not image_api or not image_api["enabled"] or not image_api["api_key"]:
        raise HTTPException(status_code=400, detail="图生图 API 未配置：请在设置中心填写 Nano Banana API Key")
    with connect() as db:
        task = db.execute("SELECT * FROM image_tasks WHERE id = ?", (task_row_id,)).fetchone()
    if not task:
        raise HTTPException(status_code=404, detail="图生图任务不存在")
    if task["status"] == "completed" and task["local_path"]:
        return image_task_from_row(task)
    result = nanobanana_query(image_api["api_key"], task["task_id"])
    status = str(result["status"])
    result_urls = result["result_urls"]
    result_url = result_urls[0] if result_urls else task["result_url"]
    local_path = task["local_path"]
    note = str(result["note"])
    if status == "completed" and result_url:
        try:
            local_path = save_processed_image_from_url(task["product_id"], result_url)
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            status = "download_failed"
            note = f"图生图完成，但下载结果图失败：{exc}"
    with connect() as db:
        db.execute(
            "UPDATE image_tasks SET status = ?, result_url = ?, local_path = ?, note = ?, updated_at = ? WHERE id = ?",
            (status, result_url, local_path, note, now_text(), task_row_id),
        )
        row = db.execute("SELECT * FROM image_tasks WHERE id = ?", (task_row_id,)).fetchone()
    return image_task_from_row(row)


@app.post("/api/products/bulk/status")
def update_products_status(payload: ProductBulkStatusPayload) -> dict[str, int]:
    if not payload.ids:
        return {"updated_count": 0}
    placeholders = ",".join("?" for _ in payload.ids)
    with connect() as db:
        result = db.execute(
            f"UPDATE products SET status = ?, updated_at = ? WHERE id IN ({placeholders})",
            [payload.status, now_text(), *payload.ids],
        )
    return {"updated_count": result.rowcount}


@app.post("/api/products/bulk/delete")
def delete_products_bulk(payload: CollectionBulkPayload) -> dict[str, int]:
    deleted = 0
    for product_id in payload.ids:
        try:
            delete_product(product_id)
            deleted += 1
        except HTTPException:
            continue
    return {"deleted_count": deleted}


@app.post("/api/dev/cleanup-test-data")
def cleanup_test_data() -> dict[str, int]:
    patterns = ["%smoke test%", "%example.local%", "%测试%", "%????????%"]
    deleted_products = 0
    deleted_collection_items = 0
    deleted_collection_tasks = 0
    with connect() as db:
        product_rows = db.execute(
            """
            SELECT id FROM products
            WHERE lower(title) LIKE ? OR title LIKE ? OR title LIKE ? OR title LIKE ?
            """,
            patterns,
        ).fetchall()
        product_ids = [row["id"] for row in product_rows]
        for product_id in product_ids:
            db.execute("DELETE FROM processing_overrides WHERE product_id = ?", (product_id,))
            result = db.execute("DELETE FROM products WHERE id = ?", (product_id,))
            deleted_products += result.rowcount
        deleted_collection_items = db.execute(
            """
            DELETE FROM collection_items
            WHERE lower(title) LIKE ? OR source_url LIKE ? OR title LIKE ? OR title LIKE ?
            """,
            patterns,
        ).rowcount
        deleted_collection_tasks = db.execute(
            """
            DELETE FROM collection_tasks
            WHERE lower(keyword) LIKE ? OR keyword LIKE ? OR keyword LIKE ? OR keyword LIKE ?
            """,
            patterns,
        ).rowcount
    for product_id in product_ids:
        product_dir = IMAGE_DIR / str(product_id)
        if product_dir.exists():
            shutil.rmtree(product_dir)
    return {
        "deleted_products": deleted_products,
        "deleted_collection_items": deleted_collection_items,
        "deleted_collection_tasks": deleted_collection_tasks,
    }










def get_setting_value(key: str, default: str = "") -> str:
    with connect() as db:
        row = db.execute("SELECT value FROM app_settings WHERE key = ?", (key,)).fetchone()
    return row["value"] if row else default


def write_run_log(task_id: int, content: str) -> str:
    log_dir = DATA_DIR / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"upload_task_{task_id}.log"
    log_path.write_text(content, encoding="utf-8")
    return str(log_path)


def processing_item_issues(item: ProcessingItem) -> list[str]:
    issues: list[str] = []
    colors = item_colors(item)
    if item.image_status != "has_main_image":
        issues.append("缺少主图")
    if not item.english_title.strip():
        issues.append("英文标题为空")
    elif contains_cjk(item.english_title):
        issues.append("英文标题包含中文")
    if not colors:
        issues.append("颜色为空")
    elif item.color.strip().lower() == "pending":
        issues.append("颜色待确认")
    if not item.size.strip():
        issues.append("尺码为空")
    elif item.size.strip().lower() == "pending":
        issues.append("尺码待确认")
    elif not item_supported_upload_sizes(item):
        issues.append("无 RPA 支持尺码")
    if not item.sku_code.strip():
        issues.append("SKU Code 为空")
    elif "COLOR-SIZE" in item.sku_code.upper():
        issues.append("SKU Code 使用默认占位")
    if item.declared_price <= 0:
        issues.append("申报价必须大于 0")
    if item.weight_g <= 0:
        issues.append("重量必须大于 0")
    if item.length_cm <= 0 or item.width_cm <= 0 or item.height_cm <= 0:
        issues.append("尺寸必须大于 0")
    if item.stock <= 0:
        issues.append("库存必须大于 0")
    if item.ship_days <= 0:
        issues.append("发货时效必须大于 0")
    for color, image_count in item_color_image_counts(item).items():
        if image_count < 3:
            issues.append(f"{color} 颜色图不足 3 张")
    return issues


def processing_item_warnings(item: ProcessingItem) -> list[str]:
    warnings: list[str] = []
    if not item.source_url.strip():
        warnings.append("站外链接为空")
    return warnings


def upload_item_diagnostics(items: list[ProcessingItem]) -> list[dict[str, object]]:
    diagnostics: list[dict[str, object]] = []
    for item in items:
        issues = processing_item_issues(item)
        diagnostics.append(
            {
                "product_id": item.product_id,
                "skc": item.skc,
                "title": item.title,
                "ready": not issues,
                "issues": issues,
                "warnings": processing_item_warnings(item),
            }
        )
    return diagnostics


def upload_preflight_summary(items: list[ProcessingItem]) -> dict[str, object]:
    diagnostics = upload_item_diagnostics(items)
    blocked_items = [item for item in diagnostics if not item["ready"]]
    issue_counts: dict[str, int] = {}
    warning_counts: dict[str, int] = {}
    for item in blocked_items:
        for issue in item["issues"]:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
    for item in diagnostics:
        for warning in item["warnings"]:
            warning_counts[warning] = warning_counts.get(warning, 0) + 1
    return {
        "total_count": len(items),
        "ready_count": len(items) - len(blocked_items),
        "blocked_count": len(blocked_items),
        "issue_counts": issue_counts,
        "warning_counts": warning_counts,
        "blocked_items": blocked_items,
        "warning_items": [item for item in diagnostics if item["warnings"]],
    }


def item_sizes(item: ProcessingItem) -> list[str]:
    values = [part.strip().upper() for part in re.split(r"[,，/、\s-]+", item.size or "") if part.strip()]
    return values or [str(item.size or "").strip()]


def item_supported_upload_sizes(item: ProcessingItem) -> list[str]:
    return [size for size in item_sizes(item) if size in RPA_ALLOWED_UPLOAD_SIZES]


def item_unsupported_upload_sizes(item: ProcessingItem) -> list[str]:
    return [size for size in item_sizes(item) if size and size not in RPA_ALLOWED_UPLOAD_SIZES]


def item_colors(item: ProcessingItem) -> list[str]:
    colors: list[str] = []
    for value in re.split(r"[,，/、\n]+", item.color or ""):
        color = clean_color_label(value)
        if color and color not in colors:
            colors.append(color)
    for assignment in item.color_image_assignments:
        color = clean_color_label(assignment.color)
        if color and color not in colors:
            colors.append(color)
    for option in item.image_options:
        color = clean_color_label(option.color)
        if color and color not in colors:
            colors.append(color)
    return colors


def color_upload_images(item: ProcessingItem, color: str) -> list[str]:
    clean_color = clean_color_label(color)
    if not clean_color:
        return []
    assigned = sorted(
        [assignment for assignment in item.color_image_assignments if clean_color_label(assignment.color) == clean_color],
        key=lambda assignment: assignment.sort_order,
    )
    urls = [assignment.image_url for assignment in assigned if assignment.image_url]
    if item.main_image:
        urls.append(item.main_image)
    for option in item.image_options:
        option_color = clean_color_label(option.color)
        if option.url and (option_color == clean_color or not option_color):
            urls.append(option.url)
    unique_urls: list[str] = []
    seen: set[str] = set()
    for url in urls:
        identity = image_identity_server(url)
        if identity and identity not in seen:
            seen.add(identity)
            unique_urls.append(url)
    return unique_urls[:3]


def item_upload_images(item: ProcessingItem) -> list[str]:
    colors = item_colors(item)
    if not colors:
        return []
    return color_upload_images(item, colors[0])


def item_color_image_counts(item: ProcessingItem) -> dict[str, int]:
    return {color: len(color_upload_images(item, color)) for color in item_colors(item)}


def first_public_image_url(item: ProcessingItem) -> str:
    for image_url in item_upload_images(item):
        if str(image_url or "").startswith("http"):
            return image_url
    return ""


def first_public_or_blank(item: ProcessingItem) -> str:
    return first_public_image_url(item)


def prepare_rpa_sku_images(items: list[ProcessingItem]) -> dict[str, object]:
    target_root = configured_rpa_sku_image_dir()
    target_root.mkdir(parents=True, exist_ok=True)
    prepared: list[dict[str, object]] = []
    missing: list[dict[str, str]] = []
    for item in items:
        for color in item_colors(item):
            safe_color = safe_path_segment(color, "Color")
            product_dir = target_root / safe_path_segment(item.skc, f"product_{item.product_id}") / safe_color
            if product_dir.exists():
                for old_file in product_dir.iterdir():
                    if old_file.is_file() and old_file.suffix.lower() in RPA_IMAGE_EXTENSIONS:
                        old_file.unlink(missing_ok=True)
            urls = color_upload_images(item, color)
            written = 0
            for index, image_url in enumerate(urls, start=1):
                target = product_dir / f"{index}.jpg"
                if materialize_image_for_rpa(image_url, target):
                    written += 1
            if written >= 3:
                prepared.append({"skc": item.skc, "color": color, "count": written, "dir": str(product_dir)})
            else:
                missing.append({"skc": item.skc, "color": color, "reason": f"仅生成 {written} 张 RPA 本地图片"})
    return {"root": str(target_root), "prepared_count": len(prepared), "missing_count": len(missing), "prepared": prepared, "missing": missing}


def miaoshou_rows(items: list[ProcessingItem]) -> list[list[object]]:
    rows: list[list[object]] = []
    for item in items:
        sizes = item_supported_upload_sizes(item)
        if not sizes:
            continue
        colors = item_colors(item)
        suggested_price = get_setting_value("miaoshou_default_suggested_price_usd", "60").strip() or "60"
        for color in colors:
            material_image = next((url for url in color_upload_images(item, color) if str(url or "").startswith("http")), "")
            for size in sizes:
                sku_code = f"{item.skc}-{safe_path_segment(color, 'COLOR')}-{safe_path_segment(size, 'SIZE')}"
                rows.append([
                    item.title,
                    item.english_title,
                    "",
                    item.skc,
                    "颜色",
                    color,
                    "尺码",
                    size,
                    "",
                    f"{float(item.declared_price):.2f}",
                    sku_code,
                    str(item.length_cm),
                    str(item.width_cm),
                    str(item.height_cm),
                    str(item.weight_g),
                    "",
                    "",
                    item.source_url,
                    "",
                    material_image,
                    "",
                    "",
                    "",
                    suggested_price,
                    str(item.stock),
                    str(item.ship_days),
                ])
    return rows


def upload_operation_settings_snapshot() -> dict[str, object]:
    return {
        "executor": {
            "mode": get_setting_value("executor_mode", "local_python"),
            "server_url": get_setting_value("executor_server_url", "http://127.0.0.1:8000"),
            "download_url": get_setting_value("executor_download_url", ""),
            "version": get_setting_value("executor_version", "0.1.0"),
            "poll_seconds": get_setting_value("executor_poll_seconds", "5"),
            "heartbeat_timeout": get_setting_value("executor_heartbeat_timeout", "60"),
            "task_scope": get_setting_value("executor_task_scope", "manual"),
        },
        "temu": {
            "shop_account": get_setting_value("temu_shop_account", ""),
            "site": get_setting_value("temu_site", "美国站"),
            "product_template": get_setting_value("temu_product_template", ""),
            "size_category": get_setting_value("temu_size_category", ""),
            "size_template": get_setting_value("temu_size_template", ""),
            "warehouse_template": get_setting_value("temu_warehouse_template", ""),
            "logistics_template": get_setting_value("temu_logistics_template", ""),
            "ship_days": get_setting_value("temu_ship_days", "9"),
            "declare_markup": get_setting_value("temu_declare_markup", "239.0"),
            "default_weight_g": get_setting_value("temu_default_weight_g", "350"),
            "default_stock": get_setting_value("temu_default_stock", "999"),
            "package_size_cm": {
                "length": get_setting_value("temu_package_length_cm", "10"),
                "width": get_setting_value("temu_package_width_cm", "5"),
                "height": get_setting_value("temu_package_height_cm", "1"),
            },
            "excel_path": get_setting_value("temu_1688_excel_path", ""),
            "batch_limit": get_setting_value("temu_batch_limit", ""),
            "start_skc": get_setting_value("temu_start_skc", ""),
            "append_sku_suffix": get_setting_value("temu_append_sku_suffix", "true"),
            "add_model_info": get_setting_value("temu_add_model_info", "false"),
            "model_index": get_setting_value("temu_model_index", "2"),
        },
        "flow": {
            "fill_skc": get_setting_value("upload_fill_skc", "true"),
            "skc_missing_policy": get_setting_value("upload_skc_missing_policy", "pause"),
            "auto_submit": get_setting_value("upload_auto_submit", "false"),
            "error_policy": get_setting_value("upload_error_policy", "skip"),
            "save_screenshots": get_setting_value("upload_save_screenshots", "false"),
            "save_html": get_setting_value("upload_save_html", "false"),
            "trace": get_setting_value("upload_trace", "off"),
            "step_delay_ms": get_setting_value("upload_step_delay_ms", "500"),
        },
    }


def upload_operation_settings_summary(settings: dict[str, object]) -> str:
    flow = settings.get("flow", {}) if isinstance(settings.get("flow"), dict) else {}
    executor = settings.get("executor", {}) if isinstance(settings.get("executor"), dict) else {}
    temu = settings.get("temu", {}) if isinstance(settings.get("temu"), dict) else {}
    return (
        f"执行器={executor.get('mode', '-')}; "
        f"店铺={temu.get('shop_account', '-') or '-'}; 起始SKC={temu.get('start_skc', '-') or '-'}; "
        f"SKC={'自动填写' if flow.get('fill_skc') == 'true' else '不填写'}; "
        f"缺SKC策略={flow.get('skc_missing_policy', '-')}; "
        f"自动提交={'开启' if flow.get('auto_submit') == 'true' else '关闭'}; "
        f"遇错={flow.get('error_policy', '-')}; Trace={flow.get('trace', '-')}"
    )


def write_task_manifest(task_id: int, task_type: str, status: str, export_path: str, items: list[ProcessingItem], run_log: str = "") -> str:
    manifest_dir = DATA_DIR / "logs"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_dir / f"upload_task_{task_id}.json"
    settings_snapshot = upload_operation_settings_snapshot()
    payload = {
        "task_id": task_id,
        "task_type": task_type,
        "status": status,
        "export_path": export_path,
        "run_log": run_log,
        "created_at": now_text(),
        "settings": settings_snapshot,
        "settings_summary": upload_operation_settings_summary(settings_snapshot),
        "preflight": upload_preflight_summary(items),
        "rpa_images": prepare_rpa_sku_images([item for item in items if not processing_item_issues(item)]),
        "items": [item.model_dump() for item in items],
    }
    manifest_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(manifest_path)


def upload_task_from_row(row: sqlite3.Row) -> UploadTask:
    return UploadTask(**dict(row))


def publish_record_from_row(row: sqlite3.Row) -> PublishRecord:
    return PublishRecord(**dict(row))


def build_processing_items() -> list[ProcessingItem]:
    with connect() as db:
        rows = db.execute(
            """
            SELECT p.*, o.english_title AS override_english_title, o.color AS override_color,
                   o.size AS override_size, o.sku_code AS override_sku_code,
                   o.declared_price AS override_declared_price, o.weight_g AS override_weight_g,
                   o.length_cm AS override_length_cm, o.width_cm AS override_width_cm,
                   o.height_cm AS override_height_cm, o.source_url AS override_source_url,
                   o.stock AS override_stock, o.ship_days AS override_ship_days,
                   d.status AS detail_status, d.note AS detail_note
            FROM products p
            LEFT JOIN processing_overrides o ON o.product_id = p.id
            LEFT JOIN product_detail_snapshots d ON d.product_id = p.id
            ORDER BY p.id DESC
            """
        ).fetchall()
    items: list[ProcessingItem] = []
    for row in rows:
        title = row["title"]
        skc = row["skc"]
        has_image = bool(row["main_image"])
        default_declared_price = round(float(row["total_cost"]) + 239, 2)
        source_url = row["override_source_url"] or ""
        items.append(
            ProcessingItem(
                product_id=row["id"],
                title=title,
                skc=skc,
                english_title=row["override_english_title"] if valid_english_title(row["override_english_title"] or "") else english_title_fallback(title),
                color=clean_color_label(row["override_color"] or ""),
                size=row["override_size"] or "pending",
                sku_code=row["override_sku_code"] or f"{skc}-COLOR-SIZE",
                declared_price=float(row["override_declared_price"] or default_declared_price),
                weight_g=int(row["override_weight_g"] or 350),
                length_cm=int(row["override_length_cm"] or 15),
                width_cm=int(row["override_width_cm"] or 10),
                height_cm=int(row["override_height_cm"] or 2),
                source_url=source_url,
                main_image=row["main_image"] or "",
                image_options=build_product_image_options(row["id"], row["main_image"] or "", source_url),
                color_image_assignments=list_color_image_assignments(row["id"]),
                detail_image_assignments=list_detail_image_assignments(row["id"]),
                detail_status=row["detail_status"] or "",
                detail_note=row["detail_note"] or "",
                image_status="has_main_image" if has_image else "missing_main_image",
                stock=int(row["override_stock"] or 999),
                ship_days=int(row["override_ship_days"] or 9),
                status="ready_to_export" if has_image else "needs_image",
            )
        )
    return items


def get_processing_item(product_id: int) -> ProcessingItem:
    for item in build_processing_items():
        if item.product_id == product_id:
            return item
    raise HTTPException(status_code=404, detail="商品不存在")


def increment_skc_value(start_skc: str, offset: int) -> str:
    clean_skc = str(start_skc or "").strip()
    match = re.search(r"(\d+)$", clean_skc)
    if not match:
        return clean_skc if offset == 0 else f"{clean_skc}-{offset + 1}"
    number_text = match.group(1)
    prefix = clean_skc[:match.start(1)]
    return f"{prefix}{int(number_text) + offset:0{len(number_text)}d}"


def ensure_unique_skc(db: sqlite3.Connection, desired_skc: str, product_id: int) -> str:
    clean_skc = str(desired_skc or "").strip()
    if not clean_skc:
        return clean_skc
    candidate = clean_skc
    suffix = 2
    while db.execute("SELECT 1 FROM products WHERE skc = ? AND id != ?", (candidate, product_id)).fetchone():
        candidate = f"{clean_skc}-{suffix}"
        suffix += 1
    return candidate


def save_processing_override(product_id: int, payload: ProcessingItemPayload) -> ProcessingItem:
    timestamp = now_text()
    with connect() as db:
        product = db.execute("SELECT id FROM products WHERE id = ?", (product_id,)).fetchone()
        if not product:
            raise HTTPException(status_code=404, detail="商品不存在")
        db.execute(
            """
            INSERT INTO processing_overrides (
                product_id, english_title, color, size, sku_code, declared_price,
                weight_g, length_cm, width_cm, height_cm, source_url, stock, ship_days, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(product_id) DO UPDATE SET
                english_title = excluded.english_title,
                color = excluded.color,
                size = excluded.size,
                sku_code = excluded.sku_code,
                declared_price = excluded.declared_price,
                weight_g = excluded.weight_g,
                length_cm = excluded.length_cm,
                width_cm = excluded.width_cm,
                height_cm = excluded.height_cm,
                source_url = excluded.source_url,
                stock = excluded.stock,
                ship_days = excluded.ship_days,
                updated_at = excluded.updated_at
            """,
            (
                product_id,
                payload.english_title,
                payload.color,
                payload.size,
                payload.sku_code,
                payload.declared_price,
                payload.weight_g,
                payload.length_cm,
                payload.width_cm,
                payload.height_cm,
                payload.source_url,
                payload.stock,
                payload.ship_days,
                timestamp,
            ),
        )
    return get_processing_item(product_id)




def api_config_from_row(row: sqlite3.Row) -> ApiConfig:
    data = dict(row)
    data["enabled"] = bool(data["enabled"])
    return ApiConfig(**data)


def setting_from_row(row: sqlite3.Row) -> AppSetting:
    return AppSetting(**dict(row))


def prompt_from_row(row: sqlite3.Row) -> PromptTemplate:
    return PromptTemplate(**dict(row))


@app.get("/api/config/apis", response_model=list[ApiConfig])
def list_api_configs() -> list[ApiConfig]:
    with connect() as db:
        rows = db.execute("SELECT * FROM api_configs ORDER BY key").fetchall()
    return [api_config_from_row(row) for row in rows]


@app.put("/api/config/apis/{config_key}", response_model=ApiConfig)
def save_api_config(config_key: str, payload: ApiConfig) -> ApiConfig:
    timestamp = now_text()
    with connect() as db:
        db.execute(
            """
            INSERT INTO api_configs (key, name, enabled, base_url, model, api_key, usage, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET name=excluded.name, enabled=excluded.enabled, base_url=excluded.base_url,
            model=excluded.model, api_key=excluded.api_key, usage=excluded.usage, updated_at=excluded.updated_at
            """,
            (config_key, payload.name, int(payload.enabled), payload.base_url, payload.model, payload.api_key, payload.usage, timestamp),
        )
        row = db.execute("SELECT * FROM api_configs WHERE key = ?", (config_key,)).fetchone()
    return api_config_from_row(row)


@app.get("/api/settings", response_model=list[AppSetting])
def list_settings() -> list[AppSetting]:
    with connect() as db:
        rows = db.execute("SELECT * FROM app_settings ORDER BY key").fetchall()
    return [setting_from_row(row) for row in rows]


@app.put("/api/settings", response_model=list[AppSetting])
def save_settings(payload: list[AppSetting]) -> list[AppSetting]:
    timestamp = now_text()
    with connect() as db:
        for item in payload:
            db.execute(
                """
                INSERT INTO app_settings (key, value, updated_at) VALUES (?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at
                """,
                (item.key, item.value, timestamp),
            )
        rows = db.execute("SELECT * FROM app_settings ORDER BY key").fetchall()
    return [setting_from_row(row) for row in rows]


@app.get("/api/prompts", response_model=list[PromptTemplate])
def list_prompts() -> list[PromptTemplate]:
    with connect() as db:
        rows = db.execute("SELECT * FROM prompt_templates ORDER BY id DESC").fetchall()
    return [prompt_from_row(row) for row in rows]


@app.post("/api/prompts", response_model=PromptTemplate)
def create_prompt(payload: PromptTemplatePayload) -> PromptTemplate:
    timestamp = now_text()
    with connect() as db:
        cursor = db.execute(
            """
            INSERT INTO prompt_templates (name, category, prompt_type, usage, content, status, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (payload.name, payload.category, payload.prompt_type, payload.usage, payload.content, payload.status, timestamp),
        )
        row = db.execute("SELECT * FROM prompt_templates WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return prompt_from_row(row)


@app.put("/api/prompts/{prompt_id}", response_model=PromptTemplate)
def update_prompt(prompt_id: int, payload: PromptTemplatePayload) -> PromptTemplate:
    with connect() as db:
        result = db.execute(
            """
            UPDATE prompt_templates SET name=?, category=?, prompt_type=?, usage=?, content=?, status=?, updated_at=? WHERE id=?
            """,
            (payload.name, payload.category, payload.prompt_type, payload.usage, payload.content, payload.status, now_text(), prompt_id),
        )
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="prompt not found")
        row = db.execute("SELECT * FROM prompt_templates WHERE id = ?", (prompt_id,)).fetchone()
    return prompt_from_row(row)


@app.delete("/api/prompts/{prompt_id}")
def delete_prompt(prompt_id: int) -> dict[str, bool]:
    with connect() as db:
        result = db.execute("DELETE FROM prompt_templates WHERE id = ?", (prompt_id,))
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="prompt not found")
    return {"ok": True}


@app.post("/api/export/miaoshou")
def export_miaoshou() -> dict[str, str]:
    export_dir = DATA_DIR / "export"
    export_dir.mkdir(parents=True, exist_ok=True)
    filename = f"miaoshou_upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    target = export_dir / filename
    items = build_processing_items()
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Miaoshou Upload"
    sheet.append(MIAOSHOU_COLUMNS)
    for row in miaoshou_rows(items):
        sheet.append(row)
    for column_cells in sheet.columns:
        max_length = max(len(str(cell.value or "")) for cell in column_cells)
        sheet.column_dimensions[column_cells[0].column_letter].width = min(max(max_length + 2, 10), 36)
    workbook.save(target)
    image_result = prepare_rpa_sku_images(items)
    return {"path": str(target), "filename": filename, "download_url": f"/api/export/miaoshou/{filename}", "rpa_image_dir": str(image_result["root"])}


@app.get("/api/export/miaoshou/{filename}")
def download_miaoshou_export(filename: str) -> FileResponse:
    export_dir = (DATA_DIR / "export").resolve()
    target = (export_dir / filename).resolve()
    if target.parent != export_dir or not target.name.startswith("miaoshou_upload_") or target.suffix != ".xlsx":
        raise HTTPException(status_code=400, detail="Invalid export filename")
    if not target.exists():
        raise HTTPException(status_code=404, detail="Export file not found")
    return FileResponse(target, filename=target.name)


@app.get("/api/upload/preflight")
def upload_preflight() -> dict[str, object]:
    scripts = ["export_miaoshou_xlsx.py", "test_sku_feishu.py", "rpa_upload.py", "pipeline.py"]
    script_dir = configured_script_dir()
    script_status = {name: (script_dir / name).exists() for name in scripts}
    latest_exports = sorted((DATA_DIR / "export").glob("miaoshou_upload_*.xlsx"), key=lambda item: item.stat().st_mtime, reverse=True) if (DATA_DIR / "export").exists() else []
    image_root = DATA_DIR / "images"
    items = build_processing_items()
    item_summary = upload_preflight_summary(items)
    rpa_image_result = prepare_rpa_sku_images([item for item in items if not processing_item_issues(item)])
    cos = cos_preflight()
    infra_ready = all(script_status.values()) and image_root.exists() and script_dir.exists()
    return {
        "script_dir": str(script_dir),
        "script_dir_exists": script_dir.exists(),
        "scripts": script_status,
        "latest_export": str(latest_exports[0]) if latest_exports else "",
        "image_dir": str(image_root),
        "image_dir_exists": image_root.exists(),
        "rpa_image_dir": str(rpa_image_result["root"]),
        "rpa_images": rpa_image_result,
        "cos": cos,
        "infra_ready": infra_ready,
        "items": item_summary,
        "command_preview": display_upload_rpa_command(str(latest_exports[0]) if latest_exports else "<export_path>"),
        "ready": infra_ready and item_summary["total_count"] > 0 and item_summary["blocked_count"] == 0 and int(rpa_image_result["missing_count"]) == 0,
    }


@app.get("/api/upload-tasks", response_model=list[UploadTask])
def list_upload_tasks() -> list[UploadTask]:
    with connect() as db:
        rows = db.execute("SELECT * FROM upload_tasks ORDER BY id DESC").fetchall()
    return [upload_task_from_row(row) for row in rows]


@app.delete("/api/upload-tasks/{task_id}")
def delete_upload_task(task_id: int) -> dict[str, bool]:
    with connect() as db:
        result = db.execute("DELETE FROM upload_tasks WHERE id = ?", (task_id,))
    log_path = DATA_DIR / "logs" / f"upload_task_{task_id}.log"
    manifest_path = DATA_DIR / "logs" / f"upload_task_{task_id}.json"
    log_path.unlink(missing_ok=True)
    manifest_path.unlink(missing_ok=True)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="任务不存在")
    return {"ok": True}


@app.post("/api/upload-tasks/clear")
def clear_upload_tasks() -> dict[str, int]:
    with connect() as db:
        count = db.execute("SELECT COUNT(*) AS total FROM upload_tasks").fetchone()["total"]
        db.execute("DELETE FROM upload_tasks")
        db.execute("DELETE FROM publish_records")
    return {"deleted_count": count}


@app.post("/api/upload-tasks", response_model=UploadTask)
def create_upload_task() -> UploadTask:
    export = export_miaoshou()
    items = build_processing_items()
    item_summary = upload_preflight_summary(items)
    success_count = int(item_summary["ready_count"])
    failed_count = int(item_summary["blocked_count"])
    status = "export_ready" if failed_count == 0 else "needs_review"
    timestamp = now_text()
    settings_snapshot = upload_operation_settings_snapshot()
    settings_summary = upload_operation_settings_summary(settings_snapshot)
    with connect() as db:
        cursor = db.execute(
            """
            INSERT INTO upload_tasks (name, status, total_count, success_count, failed_count, export_path, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (f"\u4e0a\u8d27\u4efb\u52a1 {timestamp}", status, len(items), success_count, failed_count, export["path"], timestamp, timestamp),
        )
        db.execute("DELETE FROM publish_records")
        for item in items:
            issues = processing_item_issues(item)
            if not issues:
                db.execute(
                    "INSERT INTO publish_records (result, skc, title, reason, created_at) VALUES (?, ?, ?, ?, ?)",
                    ("\u6210\u529f", item.skc, item.title, "", timestamp),
                )
            else:
                db.execute(
                    "INSERT INTO publish_records (result, skc, title, reason, created_at) VALUES (?, ?, ?, ?, ?)",
                    ("\u5931\u8d25", item.skc, item.title, "；".join(issues), timestamp),
                )
        manifest_path = write_task_manifest(cursor.lastrowid, "create", status, export["path"], items)
        db.execute("UPDATE upload_tasks SET run_log = ? WHERE id = ?", (f"设置：{settings_summary}；Manifest: {manifest_path}", cursor.lastrowid))
        row = db.execute("SELECT * FROM upload_tasks WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return upload_task_from_row(row)




@app.post("/api/upload-tasks/run", response_model=UploadTask)
def run_upload_task() -> UploadTask:
    mode = "real"
    preflight = upload_preflight()
    export = export_miaoshou()
    items = build_processing_items()
    diagnostics = upload_item_diagnostics(items)
    blocked_items = [item for item in diagnostics if not item["ready"]]
    timestamp = now_text()
    real_enabled = get_setting_value("enable_real_rpa", "false").lower() == "true"
    script_dir = configured_script_dir()
    command = upload_rpa_command(export["path"])
    status = "blocked"
    run_log = ""
    stdout_text = ""
    if not real_enabled:
        status = "blocked"
        run_log = "Real RPA blocked: enable_real_rpa is false in settings."
    elif blocked_items:
        status = "needs_review"
        run_log = f"Real RPA blocked: {len(blocked_items)} products need review. SKC: {', '.join(str(item['skc']) for item in blocked_items)}"
    elif not preflight["ready"]:
        status = "needs_review"
        run_log = "Real RPA blocked: preflight failed."
    else:
        try:
            completed = subprocess.run(
                command,
                cwd=script_dir,
                capture_output=True,
                text=True,
                timeout=60 * 60,
                check=False,
            )
            stdout_text = (completed.stdout or "") + "\n" + (completed.stderr or "")
            failure_markers = [
                "导入提交失败",
                "已停止后续上图",
                "未获取到待检测的产品货号",
                "超时仍未就绪",
                "完成：成功 0 个",
            ]
            has_failure_marker = any(marker in stdout_text for marker in failure_markers)
            status = "rpa_success" if completed.returncode == 0 and not has_failure_marker else "rpa_failed"
            run_log = f"Real RPA finished with code {completed.returncode}. CWD: {script_dir}. Command: {' '.join(command)}"
            if has_failure_marker:
                run_log += " Failure marker detected in RPA output."
        except Exception as exc:
            status = "rpa_failed"
            run_log = f"Real RPA exception: {exc}"
            stdout_text = repr(exc)
    failed_count = len(blocked_items)
    success_count = len(items) - failed_count
    with connect() as db:
        cursor = db.execute(
            """
            INSERT INTO upload_tasks (name, status, total_count, success_count, failed_count, export_path, run_log, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (f"正式上货 {timestamp}", status, len(items), success_count, failed_count, export["path"], run_log, timestamp, timestamp),
        )
        task_id = cursor.lastrowid
        log_path = write_run_log(task_id, run_log + "\n\n" + stdout_text)
        manifest_path = write_task_manifest(task_id, mode, status, export["path"], items, run_log)
        db.execute("UPDATE upload_tasks SET run_log = ? WHERE id = ?", (run_log + f" Log: {log_path} Manifest: {manifest_path}", task_id))
        db.execute("DELETE FROM publish_records")
        for item in items:
            issues = processing_item_issues(item)
            if issues:
                db.execute(
                    "INSERT INTO publish_records (result, skc, title, reason, created_at) VALUES (?, ?, ?, ?, ?)",
                    ("Failed", item.skc, item.title, "; ".join(issues), timestamp),
                )
            else:
                db.execute(
                    "INSERT INTO publish_records (result, skc, title, reason, created_at) VALUES (?, ?, ?, ?, ?)",
                    ("Success", item.skc, item.title, "Run checked", timestamp),
                )
        row = db.execute("SELECT * FROM upload_tasks WHERE id = ?", (task_id,)).fetchone()
    return upload_task_from_row(row)






@app.post("/api/products/images/batch")
def batch_upload_product_images(images: list[UploadFile] = File(...)) -> dict[str, object]:
    updated: list[str] = []
    unmatched: list[str] = []
    with connect() as db:
        products = db.execute("SELECT id, skc FROM products").fetchall()
        product_by_skc = {row["skc"].lower(): row for row in products}
        for image in images:
            filename = image.filename or ""
            stem = Path(filename).stem.lower()
            matched = None
            for skc, row in product_by_skc.items():
                if skc in stem:
                    matched = row
                    break
            if not matched:
                unmatched.append(filename)
                continue
            suffix = Path(filename).suffix.lower() or ".jpg"
            product_dir = IMAGE_DIR / str(matched["id"])
            product_dir.mkdir(parents=True, exist_ok=True)
            target = product_dir / f"main{suffix}"
            for old_file in product_dir.glob("main.*"):
                old_file.unlink(missing_ok=True)
            with target.open("wb") as file:
                shutil.copyfileobj(image.file, file)
            image_path = f"/images/{matched['id']}/{target.name}"
            db.execute(
                "UPDATE products SET main_image = ?, status = ?, updated_at = ? WHERE id = ?",
                (image_path, "ok", now_text(), matched["id"]),
            )
            updated.append(matched["skc"])
    return {"updated": updated, "unmatched": unmatched, "updated_count": len(updated), "unmatched_count": len(unmatched)}


@app.get("/api/upload-tasks/{task_id}/log")
def get_upload_task_log(task_id: int) -> dict[str, str]:
    log_path = DATA_DIR / "logs" / f"upload_task_{task_id}.log"
    if not log_path.exists():
        return {"path": str(log_path), "content": ""}
    return {"path": str(log_path), "content": log_path.read_text(encoding="utf-8", errors="replace")}


@app.get("/api/upload-tasks/{task_id}/manifest")
def get_upload_task_manifest(task_id: int) -> dict[str, object]:
    manifest_path = DATA_DIR / "logs" / f"upload_task_{task_id}.json"
    if not manifest_path.exists():
        return {"path": str(manifest_path), "content": {}}
    return {"path": str(manifest_path), "content": json.loads(manifest_path.read_text(encoding="utf-8"))}


@app.get("/api/products/missing-images", response_model=list[Product])
def list_missing_image_products() -> list[Product]:
    with connect() as db:
        rows = db.execute("SELECT * FROM products WHERE main_image IS NULL OR main_image = '' ORDER BY id DESC").fetchall()
    return [product_from_row(row) for row in rows]


@app.get("/api/publish-records", response_model=list[PublishRecord])
def list_publish_records(result: str = "", q: str = "") -> list[PublishRecord]:
    clauses: list[str] = []
    params: list[object] = []
    if result.strip():
        clauses.append("result = ?")
        params.append(result.strip())
    if q.strip():
        keyword = f"%{q.strip()}%"
        clauses.append("(skc LIKE ? OR title LIKE ? OR reason LIKE ?)")
        params.extend([keyword, keyword, keyword])
    where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    with connect() as db:
        rows = db.execute(f"SELECT id, result, skc, title, reason, created_at FROM publish_records {where_sql} ORDER BY id DESC", params).fetchall()
    return [publish_record_from_row(row) for row in rows]


@app.get("/api/processing-items", response_model=list[ProcessingItem])
def list_processing_items() -> list[ProcessingItem]:
    return build_processing_items()


@app.put("/api/processing-items/bulk", response_model=list[ProcessingItem])
def update_processing_items_bulk(payload: ProcessingBulkPayload) -> list[ProcessingItem]:
    if not payload.ids:
        raise HTTPException(status_code=400, detail="请选择要批量编辑的商品")
    ordered_ids = [int(product_id) for product_id in payload.ids]
    start_skc = payload.start_skc.strip()
    if start_skc:
        timestamp = now_text()
        with connect() as db:
            for index, product_id in enumerate(ordered_ids):
                desired_skc = increment_skc_value(start_skc, index)
                skc = ensure_unique_skc(db, desired_skc, product_id)
                db.execute("UPDATE products SET skc = ?, updated_at = ? WHERE id = ?", (skc, timestamp, product_id))
    return [save_processing_override(product_id, payload.fields) for product_id in ordered_ids]


@app.post("/api/processing-items/auto-assign-color-images", response_model=AutoAssignColorImagesResult)
def auto_assign_processing_color_images(payload: AutoAssignColorImagesPayload) -> AutoAssignColorImagesResult:
    return auto_assign_color_images(payload)


@app.post("/api/processing-items/color-image-assignment", response_model=list[ColorImageAssignment])
def manual_assign_processing_color_image(payload: ManualColorImageAssignmentPayload) -> list[ColorImageAssignment]:
    return save_manual_color_image_assignment(payload)


@app.post("/api/processing-items/detail-image-assignment", response_model=list[DetailImageAssignment])
def manual_assign_processing_detail_image(payload: ManualDetailImageAssignmentPayload) -> list[DetailImageAssignment]:
    return save_manual_detail_image_assignment(payload)


@app.post("/api/processing-items/dedupe-images", response_model=DedupeProcessingImagesResult)
def dedupe_processing_item_images(payload: DedupeProcessingImagesPayload) -> DedupeProcessingImagesResult:
    return dedupe_processing_images(payload.ids)


@app.delete("/api/processing-items/{product_id}/detail-images/{slot_index}", response_model=list[DetailImageAssignment])
def clear_processing_detail_image(product_id: int, slot_index: int) -> list[DetailImageAssignment]:
    return save_detail_image_slot(product_id, slot_index, "")


@app.post("/api/processing-items/generate-title", response_model=ProcessingItem)
def generate_processing_title(payload: GenerateTitlePayload) -> ProcessingItem:
    item = get_processing_item(payload.product_id)
    with connect() as db:
        deepseek = db.execute("SELECT * FROM api_configs WHERE key = 'deepseek'").fetchone()
    if deepseek and deepseek["enabled"] and deepseek["api_key"]:
        title_template = active_prompt_template("标题提示词", "标题生成") or active_prompt_template("标题提示词")
        if title_template:
            system_prompt = "You are a product title copywriting assistant. Follow the user's prompt exactly. Return only the requested result."
            user_prompt = render_title_prompt(title_template, item)
        else:
            system_prompt = "You are a Temu ecommerce listing assistant. Generate one concise, natural English product title. Return only the title, no quotes, no explanation."
            user_prompt = (
                f"Source title: {item.title}\n"
                f"SKC: {item.skc}\n"
                f"Color: {item.color}\n"
                f"Size: {item.size}\n"
                "Requirements: English only, under 120 characters, no brand names unless present, no exaggerated claims."
            )
        generated_title = call_openai_compatible_chat(
            deepseek["base_url"] or "https://api.deepseek.com",
            deepseek["api_key"],
            deepseek["model"] or "deepseek-chat",
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        generated_title = extract_title_from_model_response(generated_title, item.title)
        if not valid_english_title(generated_title):
            generated_title = english_title_fallback(item.title)
    else:
        generated_title = english_title_fallback(item.title)
    updated = save_processing_override(
        payload.product_id,
        ProcessingItemPayload(
            english_title=generated_title,
            color=item.color,
            size=item.size,
            sku_code=item.sku_code,
            declared_price=item.declared_price,
            weight_g=item.weight_g,
            length_cm=item.length_cm,
            width_cm=item.width_cm,
            height_cm=item.height_cm,
            source_url=item.source_url,
            stock=item.stock,
            ship_days=item.ship_days,
        ),
    )
    updated.english_title = f"{updated.english_title}"
    return updated


@app.put("/api/processing-items/{product_id}", response_model=ProcessingItem)
def update_processing_item(product_id: int, payload: ProcessingItemPayload) -> ProcessingItem:
    return save_processing_override(product_id, payload)


@app.get("/api/collection-items", response_model=list[CollectionItem])
def list_collection_items(q: str = "", source: str = "", status: str = "", min_price: float = 0, max_price: float = 0, sort: str = "newest") -> list[CollectionItem]:
    clauses: list[str] = []
    params: list[object] = []
    if q.strip():
        keyword = f"%{q.strip()}%"
        clauses.append("(title LIKE ? OR source LIKE ?)")
        params.extend([keyword, keyword])
    if source.strip():
        clauses.append("source = ?")
        params.append(source.strip())
    if status.strip():
        clauses.append("status = ?")
        params.append(status.strip())
    if min_price:
        clauses.append("price >= ?")
        params.append(min_price)
    if max_price:
        clauses.append("price <= ?")
        params.append(max_price)
    order_by = {
        "sales_desc": "sales DESC, id DESC",
        "price_asc": "price ASC, id DESC",
        "price_desc": "price DESC, id DESC",
        "newest": "id DESC",
    }.get(sort, "id DESC")
    where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    with connect() as db:
        rows = db.execute(f"SELECT * FROM collection_items {where_sql} ORDER BY {order_by}", params).fetchall()
    return [collection_item_from_row(row) for row in rows]


@app.get("/api/collection-tasks", response_model=list[CollectionTask])
def list_collection_tasks() -> list[CollectionTask]:
    with connect() as db:
        rows = db.execute("SELECT * FROM collection_tasks ORDER BY id DESC").fetchall()
    return [collection_task_from_row(row) for row in rows]


@app.post("/api/collection-tasks/clear")
def clear_collection_tasks() -> dict[str, int]:
    with connect() as db:
        count = db.execute("SELECT COUNT(*) AS total FROM collection_tasks").fetchone()["total"]
        db.execute("DELETE FROM collection_tasks")
    return {"deleted_count": count}


@app.get("/api/collection/preflight")
def get_collection_preflight() -> dict[str, object]:
    return collection_preflight()


@app.get("/api/collection-tasks/{task_id}/request")
def get_collection_task_request(task_id: int) -> dict[str, object]:
    with connect() as db:
        row = db.execute("SELECT * FROM collection_tasks WHERE id = ?", (task_id,)).fetchone()
        if row and row["mode"] == "1688":
            request_path = ensure_collection_request(row)
            db.execute("UPDATE collection_tasks SET request_path = ?, updated_at = ? WHERE id = ?", (request_path, now_text(), task_id))
            row = db.execute("SELECT * FROM collection_tasks WHERE id = ?", (task_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="采集任务不存在")
    request_path = row["request_path"]
    if not request_path:
        return {"path": "", "content": {}}
    target = Path(request_path)
    if not target.exists():
        return {"path": request_path, "content": {}}
    return {"path": request_path, "content": json.loads(target.read_text(encoding="utf-8"))}


@app.post("/api/collection-tasks/{task_id}/execute", response_model=CollectionTask)
def execute_collection_task(task_id: int) -> CollectionTask:
    with connect() as db:
        row = db.execute("SELECT * FROM collection_tasks WHERE id = ?", (task_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="采集任务不存在")
        if row["mode"] != "1688":
            raise HTTPException(status_code=400, detail="只有 1688 外部采集任务可以执行")
        if row["status"] not in {"external_pending", "blocked", "executed_stub", "empty", "failed"}:
            raise HTTPException(status_code=400, detail="当前状态不允许重复执行，请新建外部采集任务或使用回填结果")
        if row["mode"] == "1688":
            payload = CollectionTaskPayload(
                keyword=row["keyword"],
                source=row["source"],
                mode=row["mode"],
                collector=row["collector"],
                target_count=row["target_count"],
                min_price=row["min_price"],
                max_price=row["max_price"],
                blacklist=row["blacklist"],
            )
            try:
                provider = "万邦 API" if get_setting_value("onebound_key") and get_setting_value("onebound_secret") else "1688 Cookie"
                rows = run_onebound_1688_search(payload) if provider == "万邦 API" else run_1688_public_search(payload)
                imported, skipped = insert_collection_rows_with_db(db, normalize_collection_rows(rows), row["source"])
                status = "completed" if imported else "empty"
                note = f"{provider} 真实采集已执行，解析 {len(rows)} 条，写入 {imported} 条，跳过重复/无标题 {skipped} 条。"
            except HTTPException as exc:
                status = "failed"
                imported = 0
                note = str(exc.detail)
            db.execute("UPDATE collection_tasks SET status = ?, collector = ?, note = ?, result_count = ?, updated_at = ? WHERE id = ?", (status, "1688_public_search", note, imported, now_text(), task_id))
            updated = db.execute("SELECT * FROM collection_tasks WHERE id = ?", (task_id,)).fetchone()
            return collection_task_from_row(updated)
        db.execute(
            "UPDATE collection_tasks SET status = ?, note = ?, result_count = ?, updated_at = ? WHERE id = ?",
            ("failed", "本地模拟采集已移除；仅支持 1688 / 万邦 API 真实采集或文件导入。", 0, now_text(), task_id),
        )
        updated = db.execute("SELECT * FROM collection_tasks WHERE id = ?", (task_id,)).fetchone()
    return collection_task_from_row(updated)


@app.post("/api/collection-tasks", response_model=CollectionTask)
def create_collection_task(payload: CollectionTaskPayload) -> CollectionTask:
    keyword = payload.keyword.strip()
    if not keyword:
        raise HTTPException(status_code=400, detail="请输入采集关键词")
    target_count = max(1, min(int(payload.target_count or 1), 50))
    min_price = max(float(payload.min_price or 0), 0)
    max_price = max(float(payload.max_price or 0), 0)
    if max_price and min_price > max_price:
        raise HTTPException(status_code=400, detail="最低价不能高于最高价")
    timestamp = now_text()
    mode, collector, note = resolve_collector(payload)
    with connect() as db:
        cursor = db.execute(
            """
            INSERT INTO collection_tasks (keyword, source, mode, collector, target_count, min_price, max_price, blacklist, status, note, request_path, result_count, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (keyword, payload.source, mode, collector, target_count, min_price, max_price, payload.blacklist, "running", note, "", 0, timestamp, timestamp),
        )
        task_id = cursor.lastrowid
        result = run_collector(payload, task_id)
        request_path = write_collection_request(task_id, payload, result.mode, result.collector) if result.mode == "1688" else ""
        created, skipped = insert_collection_candidates_with_db(db, result.candidates)
        status = "external_pending" if request_path else ("completed" if created else "empty")
        note = result.note if request_path else f"{result.note} 写入 {created} 条，跳过重复 {skipped} 条。".strip()
        db.execute("UPDATE collection_tasks SET mode = ?, collector = ?, status = ?, note = ?, request_path = ?, result_count = ?, updated_at = ? WHERE id = ?", (result.mode, result.collector, status, note, request_path, created, now_text(), task_id))
        row = db.execute("SELECT * FROM collection_tasks WHERE id = ?", (task_id,)).fetchone()
    task = collection_task_from_row(row)
    if task.mode == "1688" and task.status == "external_pending":
        return execute_collection_task(task.id)
    return task


@app.post("/api/collection-items", response_model=CollectionItem)
def create_collection_item(payload: CollectionItemPayload) -> CollectionItem:
    with connect() as db:
        cursor = db.execute(
            """
            INSERT INTO collection_items (title, source, source_url, image_url, price, sales, image_count, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?)
            """,
            (payload.title, payload.source, payload.source_url, payload.image_url, payload.price, payload.sales, payload.image_count, now_text()),
        )
        row = db.execute("SELECT * FROM collection_items WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return collection_item_from_row(row)


@app.post("/api/collection-items/import-file", response_model=CollectionImportResult)
def import_collection_file(source: str = Form("外部文件"), file: UploadFile = File(...)) -> CollectionImportResult:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".csv", ".xlsx", ".xlsm", ".json"}:
        raise HTTPException(status_code=400, detail="仅支持 CSV / XLSX / JSON 文件")
    import_dir = DATA_DIR / "imports"
    import_dir.mkdir(parents=True, exist_ok=True)
    safe_name = f"collection_{datetime.now().strftime('%Y%m%d_%H%M%S')}{suffix}"
    target = import_dir / safe_name
    with target.open("wb") as output:
        shutil.copyfileobj(file.file, output)
    rows = parse_collection_rows(target)
    imported, skipped = insert_collection_rows(rows, source)
    return CollectionImportResult(imported_count=imported, skipped_count=skipped, source=source, filename=file.filename or safe_name)


@app.post("/api/collection-tasks/{task_id}/import-result", response_model=CollectionTask)
def import_collection_task_result(task_id: int, file: UploadFile = File(...)) -> CollectionTask:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".csv", ".xlsx", ".xlsm", ".json"}:
        raise HTTPException(status_code=400, detail="仅支持 CSV / XLSX / JSON 文件")
    with connect() as db:
        task = db.execute("SELECT * FROM collection_tasks WHERE id = ?", (task_id,)).fetchone()
    if not task:
        raise HTTPException(status_code=404, detail="采集任务不存在")
    import_dir = DATA_DIR / "collection_results"
    import_dir.mkdir(parents=True, exist_ok=True)
    target = import_dir / f"collection_task_{task_id}_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}{suffix}"
    with target.open("wb") as output:
        shutil.copyfileobj(file.file, output)
    rows = parse_collection_rows(target)
    imported, skipped = insert_collection_rows(rows, task["source"])
    status = "completed" if imported else "empty"
    note = f"已从外部结果文件回填 {imported} 条候选，跳过 {skipped} 条。文件：{target}"
    with connect() as db:
        db.execute(
            "UPDATE collection_tasks SET status = ?, note = ?, result_count = ?, updated_at = ? WHERE id = ?",
            (status, note, imported, now_text(), task_id),
        )
        updated = db.execute("SELECT * FROM collection_tasks WHERE id = ?", (task_id,)).fetchone()
    return collection_task_from_row(updated)


@app.get("/api/collection-items/import-template")
def download_collection_import_template() -> FileResponse:
    template_dir = DATA_DIR / "templates"
    template_dir.mkdir(parents=True, exist_ok=True)
    target = template_dir / "collection_import_template.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "采集候选导入"
    sheet.append(["title", "source", "url", "image_url", "price", "sales", "image_count"])
    sheet.append(["示例 牛仔短裤 高腰显瘦", "1688", "https://example.com/item/1", "https://example.com/image.jpg", 29.8, 1200, 12])
    workbook.save(target)
    return FileResponse(target, filename=target.name)


@app.post("/api/collection-items/import", response_model=list[Product])
def import_collection_items(payload: ImportCollectionPayload) -> list[Product]:
    if not payload.ids:
        raise HTTPException(status_code=400, detail="select collection items first")
    imported: list[Product] = []
    with connect() as db:
        rows = db.execute(
            f"SELECT * FROM collection_items WHERE id IN ({','.join(['?'] * len(payload.ids))})",
            payload.ids,
        ).fetchall()
        if not rows:
            raise HTTPException(status_code=404, detail="collection item not found")
        for row in rows:
            skc = f"DS{datetime.now().strftime('%y%m%d')}{row['id']:03d}"
            suffix = 1
            base_skc = skc
            while db.execute("SELECT 1 FROM products WHERE skc = ?", (skc,)).fetchone():
                suffix += 1
                skc = f"{base_skc}-{suffix}"
            has_collection_image = bool(row["image_url"])
            item = ProductPayload(
                title=row["title"],
                skc=skc,
                sku_summary="pending",
                purchase_price=float(row["price"]),
                first_mile=28.0,
                platform_cost=6.5,
                status="待处理" if has_collection_image else "pending_main_image",
            )
            total_cost, estimated_profit, gross_margin = recalc(item)
            timestamp = now_text()
            cursor = db.execute(
                """
                INSERT INTO products (
                    title, skc, sku_summary, purchase_price, first_mile, platform_cost,
                    total_cost, estimated_profit, gross_margin, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item.title,
                    item.skc,
                    item.sku_summary,
                    item.purchase_price,
                    item.first_mile,
                    item.platform_cost,
                    total_cost,
                    estimated_profit,
                    gross_margin,
                    item.status,
                    timestamp,
                    timestamp,
                ),
            )
            product_id = cursor.lastrowid
            main_image = save_product_main_image_from_url(product_id, row["image_url"])
            if main_image:
                db.execute("UPDATE products SET main_image = ?, status = ?, updated_at = ? WHERE id = ?", (main_image, "待处理", now_text(), product_id))
            image_source_url = row["image_url"] or row["source_url"]
            create_processing_override_for_import(db, product_id, item, image_source_url, total_cost)
            if row["source_url"]:
                try_enrich_product_from_onebound_detail(db, product_id, row["source_url"])
            db.execute("UPDATE collection_items SET selected = 1, status = 'imported' WHERE id = ?", (row["id"],))
            product_row = db.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
            imported.append(product_from_row(product_row))
    return imported


@app.post("/api/collection-items/skip")
def skip_collection_items(payload: CollectionBulkPayload) -> dict[str, int]:
    if not payload.ids:
        return {"updated_count": 0}
    placeholders = ",".join("?" for _ in payload.ids)
    with connect() as db:
        result = db.execute(f"UPDATE collection_items SET status = 'skipped' WHERE id IN ({placeholders}) AND status != 'imported'", payload.ids)
    return {"updated_count": result.rowcount}


@app.post("/api/collection-items/delete")
def delete_collection_items(payload: CollectionBulkPayload) -> dict[str, int]:
    if not payload.ids:
        return {"deleted_count": 0}
    placeholders = ",".join("?" for _ in payload.ids)
    with connect() as db:
        result = db.execute(f"DELETE FROM collection_items WHERE id IN ({placeholders})", payload.ids)
    return {"deleted_count": result.rowcount}


@app.delete("/api/products/{product_id}")
def delete_product(product_id: int) -> dict[str, bool]:
    with connect() as db:
        db.execute("DELETE FROM processing_overrides WHERE product_id = ?", (product_id,))
        result = db.execute("DELETE FROM products WHERE id = ?", (product_id,))
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="商品不存在")
    product_dir = IMAGE_DIR / str(product_id)
    if product_dir.exists():
        shutil.rmtree(product_dir)
    return {"ok": True}
