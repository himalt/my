from __future__ import annotations

import os
import webbrowser
from threading import Timer

import uvicorn


def main() -> None:
    host = os.environ.get("UPLOAD_ASSISTANT_HOST", "127.0.0.1")
    port = int(os.environ.get("UPLOAD_ASSISTANT_PORT", "8000"))
    open_browser = os.environ.get("UPLOAD_ASSISTANT_OPEN_BROWSER", "true").lower() in {"1", "true", "yes", "on"}
    browser_url = os.environ.get("UPLOAD_ASSISTANT_BROWSER_URL") or f"http://{host}:{port}"
    if open_browser:
        Timer(1.2, lambda: webbrowser.open(browser_url)).start()
    uvicorn.run("backend.app.main:app", host=host, port=port, reload=False, access_log=False)


if __name__ == "__main__":
    main()
