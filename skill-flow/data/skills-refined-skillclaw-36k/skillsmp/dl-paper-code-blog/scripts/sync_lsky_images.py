#!/usr/bin/env python3
"""
Upload local image links in a blog Markdown file to Lsky and rewrite the Markdown
to use the returned URLs.

This script is designed to be used *after* you finish drafting a blog post:
  1) You write Markdown with local links like `![](paper/figures/fig_01.png)`.
  2) You run this script.
  3) It uploads missing images (dedup via .lsky_upload_cache.json) and rewrites
     the Markdown to `![](https://lsky...png)`.

Hard rule enforced by default:
  - Do NOT embed full-page renders under `paper/pages/`. Use cropped figures
    under `paper/figures/` (or `paper/front_matter/`) instead.

Auth:
  - Uses env var LSKY_TOKEN (or --token).
  - Base URL defaults to https://lsky.xueguo.us/api/v1 (or env LSKY_BASE_URL).

Dependency:
  - Requires the `lsky-uploader` skill to be installed, because this script
    imports and reuses its upload logic.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def is_url(value: str) -> bool:
    value = value.strip()
    return value.startswith("http://") or value.startswith("https://")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_cache(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"version": 1, "entries": {}}
    # Cache is expected to be UTF-8 JSON, but allow GBK fallback for legacy files.
    for enc in ("utf-8", "utf-8-sig", "gbk"):
        try:
            with path.open("r", encoding=enc) as fh:
                data = json.load(fh)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise
    if "entries" not in data or not isinstance(data["entries"], dict):
        raise ValueError(f"Invalid cache file (missing entries): {path}")
    return data


def save_cache(path: Path, cache: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(cache, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def read_text_guess_encoding(path: Path) -> tuple[str, str]:
    for enc in ("utf-8", "utf-8-sig", "gbk"):
        try:
            return path.read_text(encoding=enc), enc
        except UnicodeDecodeError:
            continue
    raise


def token_from_env_or_args(value: str | None) -> str:
    token = (value or os.environ.get("LSKY_TOKEN") or "").strip()
    if not token:
        raise SystemExit("Missing LSKY_TOKEN. Set env LSKY_TOKEN or pass --token.")
    return token


def base_url_from_env_or_args(value: str | None) -> str:
    return (value or os.environ.get("LSKY_BASE_URL") or "https://lsky.xueguo.us/api/v1").strip()


def load_lsky_uploader_module() -> Any:
    codex_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    module_dir = codex_home / "skills" / "lsky-uploader" / "scripts"
    if not module_dir.is_dir():
        raise SystemExit(
            f"lsky-uploader skill not found at {module_dir}. Install it first and restart Codex."
        )
    sys.path.insert(0, str(module_dir))
    try:
        import upload_image  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise SystemExit(f"Failed to import lsky-uploader module: {exc}") from exc
    return upload_image


@dataclass(frozen=True)
class UploadConfig:
    base_url: str
    token: str
    album_id: str | None
    strategy_id: str | None
    permission: int | None
    use_markdown_link: bool


def parse_link_inner(inner: str) -> tuple[str, str, str]:
    """
    Parse Markdown link inner text: "<path> [optional title...]"
    Returns: (leading_ws, path_token, rest)
    """
    match = re.match(r"^(\s*)(\S+)(.*)$", inner, flags=re.S)
    if not match:
        return "", inner.strip(), ""
    return match.group(1), match.group(2), match.group(3)


def validate_local_image_ref(path_token: str) -> None:
    normalized = path_token.replace("\\", "/")
    if normalized.startswith("paper/pages/") or "/paper/pages/" in normalized:
        raise SystemExit(
            f"Refusing to upload full-page render: {path_token}. "
            "Use cropped images under paper/figures/ instead."
        )


def upload_one(
    uploader: Any,
    file_path: Path,
    config: UploadConfig,
) -> dict[str, Any]:
    payload = uploader.upload(
        file_path=file_path,
        base_url=config.base_url,
        headers=uploader.build_headers(config.token),
        name=None,
        album_id=config.album_id,
        strategy_id=config.strategy_id,
        permission=config.permission,
    )
    data = payload.get("data", {})
    links = data.get("links", {}) if isinstance(data, dict) else {}
    return {"payload": payload, "links": links}


def choose_link(links: dict[str, Any], use_markdown_link: bool) -> str:
    if use_markdown_link and isinstance(links.get("markdown"), str):
        # markdown is like: ![...](URL) - extract URL if possible, else return raw.
        m = re.search(r"\((https?://[^)]+)\)", links["markdown"])
        return m.group(1) if m else links["markdown"]
    if isinstance(links.get("url"), str):
        return links["url"]
    # Fallbacks: pick any https link field.
    for key, value in links.items():
        if isinstance(value, str) and value.startswith("http"):
            return value
    raise SystemExit(f"Upload response missing URL fields: {links}")


def discover_markdown(workspace: Path) -> Path:
    blog_md = workspace / "blog.md"
    if blog_md.is_file():
        return blog_md
    candidates = sorted(workspace.glob("*_blog.md"))
    if len(candidates) == 1:
        return candidates[0]
    raise SystemExit(
        "Unable to auto-detect blog Markdown. Provide --markdown explicitly "
        "(expected blog.md or a single *_blog.md)."
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upload local Markdown images to Lsky and rewrite URLs.")
    parser.add_argument("--workspace", type=Path, default=Path.cwd(), help="Blog workspace root (default: cwd).")
    parser.add_argument("--markdown", type=Path, help="Blog Markdown path to rewrite (default: auto-detect).")
    parser.add_argument(
        "--cache",
        type=Path,
        help="Path to .lsky_upload_cache.json (default: workspace/.lsky_upload_cache.json).",
    )
    parser.add_argument("--token", help="Lsky token (default: env LSKY_TOKEN).")
    parser.add_argument("--base-url", help="Base API URL (default: env LSKY_BASE_URL or https://lsky.xueguo.us/api/v1).")
    parser.add_argument("--album-id", help="Optional album_id to upload into.")
    parser.add_argument("--strategy-id", help="Optional strategy_id to use.")
    parser.add_argument("--permission", type=int, choices=[0, 1], help="0=public, 1=private.")
    parser.add_argument("--use-markdown-link", action="store_true", help="Use links.markdown-derived URL if present.")
    parser.add_argument("--dry-run", action="store_true", help="Do not upload or rewrite; print planned actions.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    workspace: Path = args.workspace.resolve()
    markdown_path: Path = (args.markdown or discover_markdown(workspace)).resolve()
    cache_path: Path = (args.cache or (workspace / ".lsky_upload_cache.json")).resolve()

    if not markdown_path.is_file():
        raise SystemExit(f"Markdown not found: {markdown_path}")

    config = UploadConfig(
        base_url=base_url_from_env_or_args(args.base_url),
        token=token_from_env_or_args(args.token),
        album_id=args.album_id,
        strategy_id=args.strategy_id,
        permission=args.permission,
        use_markdown_link=args.use_markdown_link,
    )

    text, markdown_encoding = read_text_guess_encoding(markdown_path)
    matches = list(IMAGE_PATTERN.finditer(text))
    if not matches:
        print("No Markdown image links found. Nothing to do.")
        return 0

    uploader = load_lsky_uploader_module()
    cache = load_cache(cache_path)
    entries: dict[str, Any] = cache.get("entries", {})

    # Build mapping for local path tokens -> URL
    path_to_url: dict[str, str] = {}
    uploads_needed: list[tuple[str, Path]] = []

    for m in matches:
        inner = m.group(2)
        _, path_token, _ = parse_link_inner(inner)
        if is_url(path_token):
            continue
        validate_local_image_ref(path_token)
        file_path = (workspace / path_token).resolve()
        if not file_path.is_file():
            raise SystemExit(f"Image file not found: {path_token} -> {file_path}")
        digest = sha256_file(file_path)
        cached = entries.get(digest)
        if isinstance(cached, dict) and isinstance(cached.get("url"), str):
            path_to_url[path_token] = cached["url"]
            continue
        uploads_needed.append((path_token, file_path))

    if args.dry_run:
        print(f"Markdown: {markdown_path}")
        print(f"Cache: {cache_path}")
        print(f"Uploads needed: {len(uploads_needed)}")
        for path_token, file_path in uploads_needed[:20]:
            print(f"  - {path_token} -> {file_path}")
        return 0

    # Upload missing
    for path_token, file_path in uploads_needed:
        digest = sha256_file(file_path)
        result = upload_one(uploader, file_path, config)
        links = result["links"] if isinstance(result["links"], dict) else {}
        url = choose_link(links, config.use_markdown_link)
        entries[digest] = {
            "url": url,
            "path": str(file_path),
            "links": links,
        }
        path_to_url[path_token] = url
        print(f"Uploaded: {path_token} -> {url}")

    cache["version"] = cache.get("version", 1)
    cache["entries"] = entries
    save_cache(cache_path, cache)

    # Rewrite Markdown
    def replacer(match: re.Match[str]) -> str:
        alt = match.group(1)
        inner = match.group(2)
        leading, path_token, rest = parse_link_inner(inner)
        if is_url(path_token):
            return match.group(0)
        url = path_to_url.get(path_token)
        if not url:
            return match.group(0)
        return f"![{alt}]({leading}{url}{rest})"

    new_text = IMAGE_PATTERN.sub(replacer, text)
    if new_text != text:
        markdown_path.write_text(new_text, encoding=markdown_encoding)
        print(f"Rewrote Markdown in-place: {markdown_path}")
    else:
        print("No changes made to Markdown (all links already URLs?).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
