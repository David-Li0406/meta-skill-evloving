from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path


def check_playwright() -> tuple[bool, str]:
    try:
        import playwright  # noqa: F401
        from playwright.sync_api import sync_playwright  # noqa: F401
    except Exception as e:
        return False, f"Playwright import failed: {type(e).__name__}: {e}"
    return True, "Playwright import OK"


def check_browsers() -> tuple[bool, str]:
    localapp = os.environ.get("LOCALAPPDATA")
    if not localapp:
        return False, "LOCALAPPDATA not set; cannot locate ms-playwright cache"
    base = Path(localapp) / "ms-playwright"
    if not base.exists():
        return False, f"Playwright browsers not found at {base} (run: python -m playwright install)"
    chromium = [p for p in base.iterdir() if p.is_dir() and p.name.lower().startswith("chromium")]
    if not chromium:
        return False, f"No chromium browser found in {base} (run: python -m playwright install)"
    return True, f"Browsers OK ({len(chromium)} chromium dirs under {base})"


def check_cdp(url: str) -> tuple[bool, str]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "codex-cli"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode("utf-8"))
        browser = data.get("Browser")
        ws = data.get("webSocketDebuggerUrl")
        return True, f"CDP OK: {browser} ({ws})"
    except Exception as e:
        return False, f"CDP not reachable at {url}: {type(e).__name__}: {e}"


def main() -> int:
    print(f"Python: {sys.version.split()[0]}")

    ok, msg = check_playwright()
    print(f"Playwright: {'OK' if ok else 'FAIL'} - {msg}")
    if not ok:
        print("Install: pip install playwright")
        return 2

    ok2, msg2 = check_browsers()
    print(f"Browsers: {'OK' if ok2 else 'FAIL'} - {msg2}")
    if not ok2:
        print("Install browsers: python -m playwright install")

    cdp_url = os.environ.get("CDP_URL", "http://127.0.0.1:9222/json/version")
    ok3, msg3 = check_cdp(cdp_url)
    print(f"CDP: {'OK' if ok3 else 'WARN'} - {msg3}")
    if not ok3:
        print("Start Chrome CDP: .\\scripts\\start_chrome_cdp.ps1")

    return 0 if ok and ok2 else 1


if __name__ == "__main__":
    raise SystemExit(main())
