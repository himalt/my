from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "1688_cookies.json"
USER_DATA_DIR = ROOT / "data" / "browser_profiles" / "1688"


def main() -> int:
    parser = argparse.ArgumentParser(description="Open 1688 login page and save local cookies for upload-assistant.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Cookie JSON output path")
    parser.add_argument("--timeout", type=int, default=300, help="Seconds to wait for manual login")
    args = parser.parse_args()

    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    USER_DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("正在打开 1688 登录页。请在弹出的浏览器里完成登录。")
    print("登录成功后不用复制 Cookie，脚本会自动保存到：", output)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch_persistent_context(
            str(USER_DATA_DIR),
            headless=False,
            viewport={"width": 1280, "height": 900},
            locale="zh-CN",
        )
        page = browser.new_page()
        page.goto("https://www.1688.com", wait_until="domcontentloaded", timeout=60000)

        deadline = args.timeout * 1000
        try:
            page.wait_for_function(
                """
                () => document.cookie.includes('memberId=')
                  || document.cookie.includes('_m_h5_tk=')
                  || document.cookie.includes('cookie2=')
                  || document.cookie.includes('unb=')
                """,
                timeout=deadline,
            )
        except PlaywrightTimeoutError:
            cookies = browser.cookies()
            browser.close()
            if not cookies:
                print("等待登录超时，且未读取到 Cookie。", file=sys.stderr)
                return 1
            output.write_text(json.dumps(cookies, ensure_ascii=False, indent=2), encoding="utf-8")
            print("等待登录超时，但已保存当前 Cookie。若采集失败，请重新运行脚本登录。")
            return 0

        page.goto("https://s.1688.com/selloffer/offer_search.htm?keywords=%E7%89%9B%E4%BB%94%E7%9F%AD%E8%A3%A4", wait_until="domcontentloaded", timeout=60000)
        cookies = browser.cookies()
        browser.close()

    output.write_text(json.dumps(cookies, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"已保存 {len(cookies)} 条 Cookie：{output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
