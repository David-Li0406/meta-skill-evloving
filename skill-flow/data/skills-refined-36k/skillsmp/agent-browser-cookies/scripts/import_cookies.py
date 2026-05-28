#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse


def run_agent_browser(args: list[str]) -> None:
    subprocess.run(["agent-browser", *args], check=True)


def load_cookies(file_path: Path) -> list[dict]:
    raw = file_path.read_text(encoding="utf-8")
    data = json.loads(raw)
    # Accept either raw agent-browser JSON or wrapped export payload.
    if "data" in data and isinstance(data["data"], dict) and "cookies" in data["data"]:
        return data["data"]["cookies"] or []
    if "cookies" in data:
        return data["cookies"] or []
    return []


def domain_matches(cookie_domain: str, host: str) -> bool:
    cookie_domain = cookie_domain.lstrip(".").lower()
    host = host.lower()
    return host == cookie_domain or host.endswith(f".{cookie_domain}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Import agent-browser cookies into a session.")
    parser.add_argument("--session", required=True, help="Session name to import into.")
    parser.add_argument("--file", required=True, help="Cookie JSON file path.")
    parser.add_argument(
        "--base-url",
        required=True,
        help="Base URL to open before setting cookies (determines origin).",
    )
    args = parser.parse_args()

    base_url = args.base_url
    host = urlparse(base_url).hostname
    if not host:
        print("Invalid --base-url, missing hostname.", file=sys.stderr)
        return 1

    cookie_file = Path(args.file).expanduser().resolve()
    if not cookie_file.exists():
        print(f"Cookie file not found: {cookie_file}", file=sys.stderr)
        return 1

    cookies = load_cookies(cookie_file)
    filtered = [c for c in cookies if domain_matches(c.get("domain", ""), host)]

    # Ensure origin exists before setting cookies.
    run_agent_browser(["open", base_url, "--session", args.session])

    for cookie in filtered:
        name = cookie.get("name")
        value = cookie.get("value", "")
        if not name:
            continue
        run_agent_browser(["cookies", "set", name, value, "--session", args.session])

    print(f"Applied {len(filtered)} cookies to session '{args.session}' for host '{host}'.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
