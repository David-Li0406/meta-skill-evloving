#!/usr/bin/env python3
"""
Upload a single file to Lsky Pro via the REST API and print the returned URLs.

Requirements:
    pip install requests
Environment variables:
    LSKY_BASE_URL   Base API URL, default: https://lsky.xueguo.us/api/v1
    LSKY_TOKEN      Personal access token (without the Bearer prefix)
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError as exc:  # pragma: no cover - dependency check
    raise SystemExit("Missing dependency: pip install requests") from exc


def build_headers(token: str | None) -> dict[str, str]:
    headers = {"Accept": "application/json"}
    if token:
        token = token.strip()
        if not token.lower().startswith("bearer "):
            token = f"Bearer {token}"
        headers["Authorization"] = token
    return headers


def upload(
    file_path: Path,
    base_url: str,
    headers: dict[str, str],
    name: str | None = None,
    album_id: str | None = None,
    strategy_id: str | None = None,
    permission: int | None = None,
) -> dict[str, Any]:
    url = f"{base_url.rstrip('/')}/upload"
    data: dict[str, str] = {}
    if name:
        data["name"] = name
    if album_id:
        data["album_id"] = str(album_id)
    if strategy_id:
        data["strategy_id"] = str(strategy_id)
    if permission is not None:
        data["permission"] = str(permission)

    mime_type, _ = mimetypes.guess_type(file_path.name)
    files = {
        "file": (
            file_path.name,
            file_path.open("rb"),
            mime_type or "application/octet-stream",
        )
    }
    try:
        response = requests.post(
            url,
            headers=headers,
            data=data,
            files=files,
            timeout=120,
        )
    finally:
        files["file"][1].close()
    response.raise_for_status()
    payload = response.json()
    if not payload.get("status"):
        message = payload.get("message") or "Upload failed"
        raise SystemExit(f"Lsky API error: {message}")
    return payload


def pretty_print(payload: dict[str, Any]) -> None:
    data = payload.get("data", {})
    links = data.get("links", {})

    print("Upload succeeded.")
    if "url" in links:
        print(f"URL: {links['url']}")
    if "markdown" in links:
        print(f"Markdown: {links['markdown']}")
    if "delete_url" in links:
        print(f"Delete URL: {links['delete_url']}")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upload an image/file to Lsky Pro.")
    parser.add_argument("file", type=Path, help="Local file path to upload")
    parser.add_argument(
        "--base-url",
        default=os.getenv("LSKY_BASE_URL", "https://lsky.xueguo.us/api/v1"),
        help="Base API URL (default: %(default)s or env LSKY_BASE_URL)",
    )
    parser.add_argument(
        "--token",
        default=os.getenv("LSKY_TOKEN"),
        help="API token without Bearer prefix (default: env LSKY_TOKEN)",
    )
    parser.add_argument("--name", help="Optional custom filename to display")
    parser.add_argument("--album-id", help="Album ID to upload into")
    parser.add_argument("--strategy-id", help="Storage strategy ID")
    parser.add_argument(
        "--permission",
        type=int,
        choices=[0, 1],
        help="0=public, 1=private (refer to your Lsky settings)",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    file_path: Path = args.file
    if not file_path.is_file():
        raise SystemExit(f"File not found: {file_path}")

    token = args.token
    if not token:
        raise SystemExit("Missing API token. Provide --token or set LSKY_TOKEN.")

    payload = upload(
        file_path=file_path,
        base_url=args.base_url,
        headers=build_headers(token),
        name=args.name,
        album_id=args.album_id,
        strategy_id=args.strategy_id,
        permission=args.permission,
    )
    pretty_print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
