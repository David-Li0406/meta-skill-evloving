import argparse
import hashlib
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse

from playwright.sync_api import sync_playwright

try:
    from markdownify import markdownify as _markdownify  # type: ignore
except Exception:  # pragma: no cover
    _markdownify = None

try:
    from bs4 import BeautifulSoup  # type: ignore
except Exception:  # pragma: no cover
    BeautifulSoup = None


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha1(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def safe_segment(s: str) -> str:
    s = s.strip()
    s = re.sub(r"[<>:\"/\\\\|?*]", "_", s)
    s = re.sub(r"\s+", " ", s).strip()
    if not s:
        return "_"
    return s[:120]


def query_suffix(query: str) -> str:
    if not query:
        return ""
    compact = query.replace("&", "_").replace("=", "-")
    compact = re.sub(r"[^A-Za-z0-9._-]", "_", compact)
    compact = compact[:80].strip("_")
    if not compact:
        compact = "q"
    return f"__{compact}__{sha1(query)[:10]}"


def normalize_url(raw_url: str) -> str:
    parsed = urlparse(raw_url)
    # Drop fragments to avoid duplicate pages
    parsed = parsed._replace(fragment="")
    return urlunparse(parsed)


def same_origin(a: str, b: str) -> bool:
    pa, pb = urlparse(a), urlparse(b)
    return (pa.scheme, pa.netloc) == (pb.scheme, pb.netloc)

def looks_like_sso_login_url(url: str) -> bool:
    u = (url or "").lower()
    return (
        "login.microsoftonline.com" in u
        or "login.live.com" in u
        or "sts.windows.net" in u
        or "/oauth2/authorize" in u
    )


def try_auto_select_account(page, account_hint: Optional[str]) -> bool:
    """
    Best-effort click of a saved Microsoft account tile.
    This does NOT enter passwords or bypass MFA; it only clicks an existing account.
    """
    try:
        # If the caller gave a hint (email/name), try text match first.
        if account_hint:
            try:
                loc = page.get_by_text(account_hint, exact=False)
                if loc.count() > 0:
                    loc.first.click()
                    return True
            except Exception:
                pass

        # Common Microsoft account chooser tiles.
        selectors = [
            "div[data-test-id='account-chooser-item']",
            "div[data-test-id='accountTile']",
            "#tilesHolder div[role='button']",
            "div[role='button'][data-test-id]",
        ]
        for sel in selectors:
            try:
                loc = page.locator(sel)
                if loc.count() > 0:
                    loc.first.click()
                    return True
            except Exception:
                continue
    except Exception:
        return False
    return False


def is_mod_url_view(url: str) -> bool:
    try:
        p = urlparse(url)
        return p.path.lower() == "/mod/url/view.php"
    except Exception:
        return False


def ensure_forceview(url: str) -> str:
    try:
        p = urlparse(url)
        if p.path.lower() != "/mod/url/view.php":
            return url
        q = dict(parse_qsl(p.query, keep_blank_values=True))
        if q.get("forceview") == "1":
            return url
        q["forceview"] = "1"
        new_q = urlencode(q, doseq=True)
        return urlunparse((p.scheme, p.netloc, p.path, p.params, new_q, p.fragment))
    except Exception:
        return url


def is_probably_download(url: str) -> bool:
    p = urlparse(url)
    path = (p.path or "").lower()
    if path == "/mod/resource/view.php":
        # Moodle "Resource" module usually serves a file (often via redirect).
        return True
    if "/pluginfile.php/" in path:
        return True
    ext = Path(path).suffix
    return ext in {
        ".pdf",
        ".doc",
        ".docx",
        ".ppt",
        ".pptx",
        ".xls",
        ".xlsx",
        ".csv",
        ".zip",
        ".rar",
        ".7z",
        ".txt",
        ".png",
        ".jpg",
        ".jpeg",
    }

def looks_like_cloudflare_block(body_text: str) -> bool:
    t = (body_text or "").lower()
    # English
    if "verify you are human" in t:
        return True
    if "attention required" in t and "cloudflare" in t:
        return True
    if "cloudflare" in t and "security" in t:
        return True
    if "ray id" in t and "cloudflare" in t:
        return True
    # Chinese (common Cloudflare Turnstile interstitial)
    if "验证您是真人" in body_text:
        return True
    if "请完成以下操作" in body_text and "验证" in body_text:
        return True
    if "需要先检查您的连接的安全性" in body_text:
        return True
    if "性能和安全由cloudflare提供" in body_text.lower():
        return True
    if "ray id" in t and ("性能和安全" in body_text or "cloudflare" in t):
        return True
    return False


def looks_like_cloudflare_url(url: str) -> bool:
    u = (url or "").lower()
    return "/cdn-cgi/" in u or "challenge-platform" in u


def local_html_path(out_dir: Path, url: str) -> Path:
    p = urlparse(url)
    domain = safe_segment(p.netloc)
    parts = [safe_segment(seg) for seg in (p.path or "/").split("/") if seg]
    if not parts:
        parts = ["root"]
    base = parts[-1]
    parent = out_dir / domain / Path(*parts[:-1])
    suffix = query_suffix(p.query)
    filename = safe_segment(base) + suffix + ".html"
    return parent / filename


def local_md_path(out_dir: Path, url: str) -> Path:
    return local_html_path(out_dir, url).with_suffix(".md")


def local_text_path(html_path: Path) -> Path:
    return html_path.with_suffix(".txt")


def local_meta_path(html_path: Path) -> Path:
    return html_path.with_suffix(".meta.json")


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def default_storage_state_path() -> Path:
    home = Path(os.path.expanduser("~"))
    # User-level config (avoid putting auth state in the Obsidian vault / iCloud)
    return home / ".codex" / "state" / "moodle_storage_state.json"

def default_user_data_dir() -> Path:
    home = Path(os.path.expanduser("~"))
    # Persistent browser profile (cookies/cache). User-level, not in the vault.
    return home / ".codex" / "state" / "moodle_profile"


@dataclass(frozen=True)
class SavedPage:
    url: str
    html_path: Path
    text_path: Path
    md_path: Path


def extract_links(page) -> list[str]:
    """
    Returns raw link targets (href + iframe src).

    NOTE: Extracting from the full document (a[href]) also captures global Moodle
    header/footer links (notifications, other courses, etc.), which can explode
    the crawl queue. Prefer the main content region when present.
    """

    selectors = [
        "#region-main",
        "#region-main-box",
        "#page-content",
        "main",
        "body",
    ]

    def _extract(selector: str) -> list[str]:
        hrefs = page.eval_on_selector_all(
            f"{selector} a[href]",
            "els => els.map(e => e.getAttribute('href')).filter(Boolean)",
        )
        srcs = page.eval_on_selector_all(
            f"{selector} iframe[src]",
            "els => els.map(e => e.getAttribute('src')).filter(Boolean)",
        )
        raw: list[str] = []
        raw.extend([str(x) for x in (hrefs or [])])
        raw.extend([str(x) for x in (srcs or [])])
        return raw

    for sel in selectors:
        try:
            if page.query_selector(sel) is None:
                continue
            links = _extract(sel)
            if links:
                return links
        except Exception:
            continue
    return []


def write_index_entry(index_file: Path, item: dict) -> None:
    ensure_parent(index_file)
    with index_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")


def save_page(page, out_dir: Path, url: str, index_file: Path, *, fmt: str) -> SavedPage:
    html_path = local_html_path(out_dir, url)
    md_path = local_md_path(out_dir, url)
    ensure_parent(html_path)
    # Moodle pages contain lots of global chrome (header/footer/notifications) that
    # is noisy and changes frequently. Prefer saving the main content region when
    # present to keep mirrors stable and incremental-friendly.
    content = page.evaluate(
        """() => {
  const selectors = ['#region-main', '#region-main-box', '#page-content', 'main', 'body'];
  for (const sel of selectors) {
    const el = document.querySelector(sel);
    if (el) {
      const html = el.outerHTML || '';
      const text = el.innerText || '';
      if (html || text) return { selector: sel, html, text };
    }
  }
  return { selector: 'body', html: document.documentElement?.outerHTML || '', text: document.body?.innerText || '' };
}"""
    ) or {}
    html = str(content.get("html") or "")
    title = page.title() or ""
    text = str(content.get("text") or "")

    if fmt in {"html+md", "html"}:
        html_path.write_text(html, encoding="utf-8")
    text_path = local_text_path(html_path)
    # Always keep a plain text version for fast grep/search.
    text_path.write_text(text, encoding="utf-8")

    md = ""
    if fmt in {"html+md", "md"} and _markdownify is not None:
        md = html_to_markdown(html)
        md_path.write_text(md, encoding="utf-8")

    meta = {
        "url": url,
        "fetched_at_utc": utc_now_iso(),
        "title": title,
        "html": str(html_path) if fmt in {"html+md", "html"} else None,
        "text": str(text_path),
        "md": str(md_path) if fmt in {"html+md", "md"} else None,
    }
    local_meta_path(html_path).write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    write_index_entry(
        index_file,
        {
            "url": url,
            "kind": "page",
            "title": title,
            "html": str(html_path) if fmt in {"html+md", "html"} else None,
            "text": str(text_path),
            "md": str(md_path) if fmt in {"html+md", "md"} else None,
            "fetched_at_utc": meta["fetched_at_utc"],
        },
    )
    return SavedPage(url=url, html_path=html_path, text_path=text_path, md_path=md_path)


def html_to_markdown(html: str) -> str:
    if _markdownify is None:
        return ""
    # Keep a predictable, Obsidian-friendly result; preserve links.
    return _markdownify(html, heading_style="ATX")


def rewrite_markdown_links(
    md: str,
    page_url: str,
    out_dir: Path,
    *,
    allow_url: callable,
    attachment_mapper: callable,
) -> str:
    """
    Rewrites inline markdown links/images to point at local mirrored files.
    - Internal Moodle pages => local .md path
    - Downloadable resources => local attachment path
    """

    def repl(m: re.Match) -> str:
        label = m.group(1)
        target = m.group(2)
        # Leave mailto/tel/anchors untouched
        if target.startswith(("mailto:", "tel:", "#")):
            return m.group(0)
        abs_url = normalize_url(urljoin(page_url, target))
        if allow_url(abs_url):
            if is_probably_download(abs_url):
                local_path = attachment_mapper(abs_url)
                if local_path is None:
                    return m.group(0)
                rel = os.path.relpath(local_path, start=local_md_path(out_dir, page_url).parent)
                rel = rel.replace("\\", "/")
                return f"[{label}]({rel})"
            # internal html page
            local_target = local_md_path(out_dir, abs_url)
            rel = os.path.relpath(local_target, start=local_md_path(out_dir, page_url).parent)
            rel = rel.replace("\\", "/")
            return f"[{label}]({rel})"
        return m.group(0)

    # Links: [text](url)
    md = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, md)
    # Images: ![alt](url)
    md = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", lambda m: "!" + repl(m), md)
    return md


def download_file(context, out_dir: Path, url: str, index_file: Path) -> Optional[Path]:
    try:
        def _download_once(request_url: str) -> Optional[Path]:
            current_url = request_url
            resp = context.request.get(current_url, timeout=30_000)
            # Moodle "resource view" often responds with a redirect to pluginfile.php; follow it.
            for _ in range(10):
                status = getattr(resp, "status", None)
                if status in {301, 302, 303, 307, 308}:
                    headers = resp.headers or {}
                    loc = headers.get("location") or headers.get("Location")
                    if not loc:
                        return None
                    current_url = normalize_url(urljoin(current_url, loc))
                    resp = context.request.get(current_url, timeout=30_000)
                    continue
                break

            if not resp.ok:
                return None

            headers = resp.headers or {}
            cd = headers.get("content-disposition") or headers.get("Content-Disposition") or ""
            ct = (headers.get("content-type") or headers.get("Content-Type") or "").lower()
            # Avoid saving HTML pages as "attachments" unless the server provides a real filename.
            if ("text/html" in ct or "text/plain" in ct) and not cd:
                return None

            filename = ""
            m = re.search(r"filename\\*=UTF-8\\'\\'([^;]+)", cd)
            if m:
                filename = m.group(1)
            else:
                m = re.search(r'filename=\"?([^\";]+)\"?', cd)
                if m:
                    filename = m.group(1)
            if filename:
                filename = safe_segment(filename)
            else:
                parsed = urlparse(current_url)
                filename = safe_segment(Path(parsed.path).name) or "download"

            # Ensure extension if Content-Type implies one (best-effort)
            if "." not in filename:
                if "pdf" in ct:
                    filename += ".pdf"
                elif "msword" in ct:
                    filename += ".doc"
                elif "officedocument.wordprocessingml" in ct:
                    filename += ".docx"
                elif "officedocument.presentationml" in ct:
                    filename += ".pptx"
                elif "officedocument.spreadsheetml" in ct:
                    filename += ".xlsx"

            parsed = urlparse(url)
            domain = safe_segment(parsed.netloc)
            files_dir = out_dir / domain / "_attachments"
            ensure_parent(files_dir / "x")

            unique = sha1(url)[:12]
            out_path = files_dir / f"{unique}__{filename}"
            out_path.write_bytes(resp.body())

            write_index_entry(
                index_file,
                {
                    "url": url,
                    "kind": "download",
                    "path": str(out_path),
                    "final_url": current_url if current_url != url else None,
                    "fetched_at_utc": utc_now_iso(),
                },
            )
            return out_path

        # Try a few Moodle-specific query variants for resource links.
        candidates = [url]
        try:
            parsed0 = urlparse(url)
            if parsed0.path.lower() == "/mod/resource/view.php":
                sep = "&" if parsed0.query else "?"
                candidates.extend(
                    [
                        f"{url}{sep}redirect=1",
                        f"{url}{sep}forcedownload=1",
                        f"{url}{sep}redirect=1&forcedownload=1",
                    ]
                )
        except Exception:
            pass

        seen: set[str] = set()
        for c in candidates:
            if c in seen:
                continue
            seen.add(c)
            out = _download_once(c)
            if out is not None:
                return out
        return None
    except Exception:
        return None


def download_file_via_browser(page, out_dir: Path, url: str, index_file: Path) -> Optional[Path]:
    """
    Fallback downloader that uses the real browser download mechanism.
    This is useful when authenticated downloads require the same Chrome session
    or when APIRequestContext can't fetch the final file reliably.
    """
    try:
        parsed = urlparse(url)
        domain = safe_segment(parsed.netloc)
        files_dir = out_dir / domain / "_attachments"
        ensure_parent(files_dir / "x")

        unique = sha1(url)[:12]
        with page.expect_download(timeout=45_000) as dl_info:
            page.goto(url, timeout=60_000, wait_until="domcontentloaded")
        dl = dl_info.value
        suggested = safe_segment(getattr(dl, "suggested_filename", "") or "") or "download"
        out_path = files_dir / f"{unique}__{suggested}"
        dl.save_as(str(out_path))

        final_url = None
        try:
            final_url = getattr(dl, "url", None)
        except Exception:
            final_url = None

        write_index_entry(
            index_file,
            {
                "url": url,
                "kind": "download",
                "path": str(out_path),
                "final_url": final_url,
                "fetched_at_utc": utc_now_iso(),
            },
        )
        return out_path
    except Exception:
        return None


def download_best_effort(context, page, out_dir: Path, url: str, index_file: Path) -> Optional[Path]:
    out = download_file(context, out_dir=out_dir, url=url, index_file=index_file)
    if out is not None:
        return out
    if page is None:
        return None
    return download_file_via_browser(page, out_dir=out_dir, url=url, index_file=index_file)


def write_toc(out_dir: Path, index_file: Path) -> None:
    if not index_file.exists():
        return
    items = []
    for line in index_file.read_text(encoding="utf-8").splitlines():
        try:
            items.append(json.loads(line))
        except Exception:
            continue

    pages = [x for x in items if x.get("md") and x.get("url") and x.get("kind") is None]
    pages.sort(key=lambda x: (x.get("title") or "", x.get("url") or ""))

    toc = out_dir / "TOC.md"
    lines = ["# Moodle Mirror TOC", "", f"- Updated (UTC): {utc_now_iso()}", ""]
    for p in pages:
        md_path = Path(p["md"])
        rel = os.path.relpath(md_path, start=toc.parent).replace("\\", "/")
        title = (p.get("title") or md_path.stem).strip()
        lines.append(f"- [{title}]({rel})")
    toc.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="Mirror Moodle pages + attachments locally using Playwright (login once, then crawl)."
    )
    ap.add_argument("--start-url", action="append", required=True, help="Start URL (repeatable).")
    ap.add_argument("--out-dir", required=True, help="Output directory to write mirrored pages.")
    ap.add_argument(
        "--allow-prefix",
        action="append",
        default=[],
        help="Only crawl URLs starting with this prefix (repeatable). Default: same origin as start URLs.",
    )
    ap.add_argument("--max-pages", type=int, default=80, help="Maximum HTML pages to save.")
    ap.add_argument("--max-downloads", type=int, default=120, help="Maximum downloads to fetch.")
    ap.add_argument("--polite-delay-ms", type=int, default=300, help="Delay between navigations.")
    ap.add_argument("--progress-every", type=int, default=10, help="Print progress every N saved pages.")
    ap.add_argument("--max-retries", type=int, default=2, help="Retries per URL on 5xx/timeout.")
    ap.add_argument("--retry-sleep-seconds", type=int, default=10, help="Sleep between retries.")
    ap.add_argument(
        "--resume",
        action="store_true",
        help="Resume by reading existing _index.jsonl and skipping already-saved URLs.",
    )
    ap.add_argument(
        "--no-refresh-start-urls",
        action="store_true",
        help="When resuming, also skip start URLs if already saved (faster, but won't discover newly-added links).",
    )
    ap.add_argument(
        "--update-on-change",
        action="store_true",
        help="If a previously-saved page is revisited (e.g. a start URL), re-save it only if local content differs.",
    )
    ap.add_argument(
        "--block-wait-seconds",
        type=int,
        default=0,
        help="If Cloudflare verification is detected during crawl, wait up to N seconds for you to complete it (headful recommended).",
    )
    ap.add_argument(
        "--networkidle-wait-ms",
        type=int,
        default=0,
        help="After navigation, optionally wait for networkidle up to N ms (0 disables; faster for Moodle).",
    )
    ap.add_argument(
        "--storage-state",
        default=str(default_storage_state_path()),
        help="User-level Playwright storage state JSON path (cookies).",
    )
    ap.add_argument(
        "--user-data-dir",
        default=str(default_user_data_dir()),
        help="User-level persistent browser profile dir (recommended to avoid re-login).",
    )
    ap.add_argument(
        "--persistent",
        action="store_true",
        help="Use a persistent browser profile (like a normal browser profile). Best for SSO/Cloudflare.",
    )
    ap.add_argument(
        "--cdp-url",
        default="",
        help="Connect to an existing Chrome via CDP (e.g. http://127.0.0.1:9222). Overrides --persistent/--login.",
    )
    ap.add_argument(
        "--login",
        action="store_true",
        help="Force interactive login (opens a visible browser and saves storage state).",
    )
    ap.add_argument(
        "--login-wait-seconds",
        type=int,
        default=0,
        help="When --login is set, wait this many seconds for manual login (no stdin prompt).",
    )
    ap.add_argument("--headful", action="store_true", help="Run crawl headful (visible browser).")
    ap.add_argument(
        "--channel",
        choices=["chromium", "chrome", "msedge"],
        default="chrome",
        help="Chromium channel to use (helps with anti-bot checks).",
    )
    ap.add_argument(
        "--format",
        choices=["html+md", "md", "html"],
        default="md",
        help="What to save for each page.",
    )
    ap.add_argument(
        "--rewrite-links",
        action="store_true",
        help="Rewrite internal links in markdown to local mirrored files.",
    )
    ap.add_argument(
        "--login-and-crawl",
        action="store_true",
        help="After interactive login, immediately start crawling in the SAME browser context (reduces Cloudflare/SSO re-checks).",
    )
    ap.add_argument(
        "--pause-on-exit-seconds",
        type=int,
        default=0,
        help="If >0, keep the browser open for this many seconds at the end (headful only).",
    )
    ap.add_argument(
        "--keep-open",
        action="store_true",
        help="Keep the browser open until Ctrl+C (headful only). Useful for Cloudflare/SSO.",
    )
    ap.add_argument(
        "--auto-login",
        action="store_true",
        help="Best-effort auto-click of saved account tiles on Microsoft login pages.",
    )
    ap.add_argument(
        "--auto-login-account",
        default="",
        help="Optional account text/email to click on the Microsoft account chooser page.",
    )

    args = ap.parse_args(argv)

    start_urls = [normalize_url(u) for u in args.start_url]
    start_url_set = set(start_urls)
    allow_prefixes = [normalize_url(p) for p in args.allow_prefix]
    out_dir = Path(args.out_dir).expanduser().resolve()
    storage_state = Path(args.storage_state).expanduser().resolve()
    user_data_dir = Path(args.user_data_dir).expanduser().resolve()
    index_file = out_dir / "_index.jsonl"

    if args.max_pages <= 0:
        raise SystemExit("--max-pages must be > 0")
    if args.max_downloads < 0:
        raise SystemExit("--max-downloads must be >= 0")

    if not allow_prefixes:
        # Default: allow anything within the same origin as the first start url
        allow_prefixes = []

    storage_state.parent.mkdir(parents=True, exist_ok=True)
    user_data_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = None
        context = None
        page = None
        connected_over_cdp = bool(args.cdp_url)

        if args.cdp_url:
            # Connect to an already-running, user-driven Chrome to reduce bot-detection.
            browser = p.chromium.connect_over_cdp(args.cdp_url)
            # Use the first existing context, or create one.
            if browser.contexts:
                context = browser.contexts[0]
            else:
                context = browser.new_context(accept_downloads=True)
            page = context.new_page()

        if args.login:
            if args.persistent:
                context = p.chromium.launch_persistent_context(
                    user_data_dir=str(user_data_dir),
                    headless=False,
                    channel=args.channel,
                    accept_downloads=True,
                )
                page = context.new_page()
            else:
                browser = p.chromium.launch(headless=False, channel=args.channel)
                context = browser.new_context(accept_downloads=True)
                page = context.new_page()
            page.goto(start_urls[0], timeout=60_000)
            print("")
            print("Login required:")
            print("1) Finish logging in in the opened browser window.")
            print("2) Navigate to the course page you want to mirror (optional).")
            if args.login_wait_seconds > 0:
                print(f"3) You have {args.login_wait_seconds}s. This window will auto-save cookies after the timer.")
                end = time.time() + args.login_wait_seconds
                passed = False
                while time.time() < end:
                    remaining = int(end - time.time())
                    try:
                        body = page.evaluate("() => document.body ? document.body.innerText : ''") or ""
                        current_url = page.url
                        if looks_like_cloudflare_block(body) or looks_like_cloudflare_url(current_url):
                            if remaining in {600, 300, 120, 60, 30, 15, 10, 5}:
                                print("  ...still seeing Cloudflare 'Verify you are human' page; please complete it in the browser.")
                        else:
                            passed = True
                            if args.auto_login and looks_like_sso_login_url(current_url):
                                try_auto_select_account(page, args.auto_login_account or None)
                    except Exception:
                        pass
                    if remaining in {600, 300, 120, 60, 30, 15, 10, 5, 4, 3, 2, 1}:
                        print(f"  ...saving in {remaining}s")
                    time.sleep(1)
                if not passed:
                    print("")
                    print("Login wait ended but the page still looks like a Cloudflare verification block.")
                    print("Re-run with a longer --login-wait-seconds and make sure the verification is completed.")
                    try:
                        context.close()
                    finally:
                        if browser is not None:
                            browser.close()
                    return 3
            else:
                print("3) Come back here and press Enter to continue.")
            try:
                if args.login_wait_seconds <= 0:
                    input()
            except EOFError:
                print("No interactive stdin available. Re-run this command in an interactive terminal to complete login.")
                try:
                    context.close()
                finally:
                    if browser is not None:
                        browser.close()
                return 2
            except KeyboardInterrupt:
                try:
                    context.close()
                finally:
                    if browser is not None:
                        browser.close()
                return 130
            # Export storage_state too (handy when not using --persistent later).
            try:
                context.storage_state(path=str(storage_state))
            except Exception:
                pass
            if not args.login_and_crawl:
                context.close()
                if browser is not None:
                    browser.close()
                browser = None
                context = None
                page = None

        # If --login --persistent --login-and-crawl was used, we already have a
        # persistent context from the login step. Don't try to launch a second
        # persistent context pointing at the same user-data-dir (it will fail).
        if browser is None and context is None:
            if args.persistent:
                context = p.chromium.launch_persistent_context(
                    user_data_dir=str(user_data_dir),
                    headless=not args.headful,
                    channel=args.channel,
                    accept_downloads=True,
                )
                page = context.new_page()
                browser = None
            else:
                browser = p.chromium.launch(headless=not args.headful, channel=args.channel)
        if context is None:
            if storage_state.exists():
                context = browser.new_context(storage_state=str(storage_state), accept_downloads=True)
            else:
                context = browser.new_context(accept_downloads=True)
        if page is None:
            page = context.new_page()

        visited: set[str] = set()
        processed: set[str] = set()
        downloaded: set[str] = set()
        queue: list[str] = []
        if args.resume and index_file.exists():
            try:
                for line in index_file.read_text(encoding="utf-8", errors="ignore").splitlines():
                    try:
                        obj = json.loads(line)
                    except Exception:
                        continue
                    u = obj.get("url")
                    kind = obj.get("kind")
                    # Only skip URLs that were successfully processed (saved page or downloaded file).
                    if kind == "download":
                        if isinstance(u, str) and u:
                            nu = normalize_url(u)
                            processed.add(nu)
                            downloaded.add(nu)
                    elif kind in (None, "page", "updated") and obj.get("md"):
                        if isinstance(u, str) and u:
                            processed.add(normalize_url(u))
            except Exception:
                pass
        # Only treat successfully processed URLs as already-visited.
        # This allows re-trying previously "error"/"blocked" URLs on resume.
        visited = set(processed)

        queued: set[str] = set()
        for u in start_urls:
            nu = normalize_url(u)
            queue.append(nu)
            queued.add(nu)

        saved_pages = 0
        saved_downloads = 0

        def allowed(u: str) -> bool:
            u = normalize_url(u)
            if not same_origin(u, start_urls[0]):
                return False
            if allow_prefixes:
                return any(u.startswith(pref) for pref in allow_prefixes)
            return True

        while queue and saved_pages < args.max_pages:
            url = normalize_url(queue.pop(0))
            queued.discard(url)
            # On resume, allow revisiting start URLs for link extraction.
            if url in processed and (url not in start_url_set or args.no_refresh_start_urls):
                continue
            if not allowed(url):
                continue

            visited.add(url)
            try:
                fetch_url = ensure_forceview(url) if is_mod_url_view(url) else url
                # Treat "resource view" and pluginfile URLs as downloads, not pages.
                if is_probably_download(url):
                    if saved_downloads < args.max_downloads and url not in downloaded:
                        out_path = download_best_effort(context, page, out_dir=out_dir, url=url, index_file=index_file)
                        if out_path is not None:
                            saved_downloads += 1
                            downloaded.add(url)
                            if args.progress_every > 0 and (saved_downloads % args.progress_every == 0 or saved_downloads == 1):
                                print(
                                    f"[progress] pages={saved_pages} downloads={saved_downloads} queue={len(queue)} visited={len(visited)} url={url}"
                                )
                    continue

                response = None
                for attempt in range(args.max_retries + 1):
                    try:
                        response = page.goto(fetch_url, timeout=45_000, wait_until="domcontentloaded")
                        if args.networkidle_wait_ms and args.networkidle_wait_ms > 0:
                            try:
                                page.wait_for_load_state("networkidle", timeout=args.networkidle_wait_ms)
                            except Exception:
                                pass
                        if response is not None and response.status >= 500:
                            if attempt < args.max_retries:
                                print(f"[retry] {url} got HTTP {response.status}, retrying in {args.retry_sleep_seconds}s...")
                                time.sleep(max(0, args.retry_sleep_seconds))
                                continue
                            write_index_entry(
                                index_file,
                                {
                                    "url": url,
                                    "kind": "error",
                                    "error": f"HTTP {response.status}",
                                    "time_utc": utc_now_iso(),
                                },
                            )
                            # Skip this URL for now.
                            raise RuntimeError(f"HTTP {response.status}")
                        break
                    except Exception as e:
                        # Some Moodle "resource" links trigger a browser download instead of rendering a page.
                        # In that case, treat it as a successful download rather than a navigation failure.
                        if "Download is starting" in str(e) or "download is starting" in str(e):
                            out_path = download_best_effort(context, page, out_dir=out_dir, url=url, index_file=index_file)
                            if out_path is not None:
                                saved_downloads += 1
                                downloaded.add(url)
                                response = None
                                break
                        if attempt < args.max_retries:
                            print(f"[retry] {url} error {type(e).__name__}, retrying in {args.retry_sleep_seconds}s...")
                            time.sleep(max(0, args.retry_sleep_seconds))
                            continue
                        raise

                # If we got redirected to SSO/login (off-origin), wait for you to complete login in the open Chrome
                # (CDP/persistent modes). Then retry the original URL.
                try:
                    if not same_origin(page.url, start_urls[0]) and looks_like_sso_login_url(page.url):
                        write_index_entry(
                            index_file,
                            {
                                "url": url,
                                "kind": "blocked",
                                "reason": "Redirected to SSO login",
                                "final_url": page.url,
                                "time_utc": utc_now_iso(),
                            },
                        )
                        if args.block_wait_seconds <= 0:
                            break
                        print(f"[auth] SSO login detected. Waiting up to {args.block_wait_seconds}s...")
                        end = time.time() + args.block_wait_seconds
                        while time.time() < end:
                            try:
                                if args.auto_login:
                                    try_auto_select_account(page, args.auto_login_account or None)
                                if same_origin(page.url, start_urls[0]):
                                    break
                            except Exception:
                                pass
                            time.sleep(2)
                        if not same_origin(page.url, start_urls[0]):
                            print("[auth] Still on SSO page; stopping crawl.")
                            break
                        # Now retry original
                        page.goto(url, timeout=45_000, wait_until="domcontentloaded")
                        try:
                            page.wait_for_load_state("networkidle", timeout=15_000)
                        except Exception:
                            pass
                except Exception:
                    pass

                # Detect Cloudflare blocks early; crawling won't work until user clears it.
                try:
                    def is_blocked_now() -> bool:
                        body = page.evaluate("() => document.body ? document.body.innerText : ''") or ""
                        return looks_like_cloudflare_block(body) or looks_like_cloudflare_url(page.url)

                    if is_blocked_now():
                        write_index_entry(
                            index_file,
                            {
                                "url": url,
                                "kind": "blocked",
                                "reason": "Cloudflare verification page detected",
                                "time_utc": utc_now_iso(),
                            },
                        )
                        if args.block_wait_seconds > 0:
                            print(
                                f"[blocked] Cloudflare verification detected. Waiting up to {args.block_wait_seconds}s for manual completion..."
                            )
                            end = time.time() + args.block_wait_seconds
                            while time.time() < end and is_blocked_now():
                                time.sleep(2)
                            if is_blocked_now():
                                print("[blocked] Still blocked after waiting; stopping crawl.")
                                break
                            print("[blocked] Cleared; continuing crawl.")
                        else:
                            # Stop immediately to avoid saving useless pages.
                            break
                except Exception:
                    pass

                saved = None
                should_save = url not in processed
                if (not should_save) and args.update_on_change:
                    try:
                        md_path = local_md_path(out_dir, url)
                        txt_path = local_text_path(local_html_path(out_dir, url))
                        content = page.evaluate(
                            """() => {
  const selectors = ['#region-main', '#region-main-box', '#page-content', 'main', 'body'];
  for (const sel of selectors) {
    const el = document.querySelector(sel);
    if (el) {
      const html = el.outerHTML || '';
      const text = el.innerText || '';
      if (html || text) return { selector: sel, html, text };
    }
  }
  return { selector: 'body', html: document.documentElement?.outerHTML || '', text: document.body?.innerText || '' };
}"""
                        ) or {}
                        new_html = str(content.get("html") or "")
                        new_text = str(content.get("text") or "")
                        new_md = ""
                        if args.format in {"html+md", "md"} and _markdownify is not None:
                            new_md = html_to_markdown(new_html)

                        if md_path.exists() and new_md:
                            old_md = md_path.read_text(encoding="utf-8", errors="ignore")
                            should_save = old_md != new_md
                        elif txt_path.exists():
                            old_txt = txt_path.read_text(encoding="utf-8", errors="ignore")
                            should_save = old_txt != new_text
                        else:
                            should_save = True
                    except Exception:
                        should_save = False

                if should_save:
                    saved = save_page(page, out_dir=out_dir, url=url, index_file=index_file, fmt=args.format)
                    if url in processed:
                        write_index_entry(index_file, {"url": url, "kind": "updated", "time_utc": utc_now_iso()})
                    saved_pages += 1
                if args.progress_every > 0 and saved_pages > 0 and (
                    saved_pages % args.progress_every == 0 or saved_pages == 1
                ):
                    print(f"[progress] pages={saved_pages} downloads={saved_downloads} queue={len(queue)} visited={len(visited)} url={url}")

                # Extract links for crawling
                for raw in extract_links(page):
                    next_url = normalize_url(urljoin(url, raw))
                    if next_url not in visited and next_url not in queued and allowed(next_url):
                        queue.append(next_url)
                        queued.add(next_url)

                # Collect potential downloads (current page only, to stay bounded)
                if saved_downloads < args.max_downloads:
                    # Use scoped extraction to avoid grabbing header/footer noise.
                    for raw in extract_links(page):
                        if saved_downloads >= args.max_downloads:
                            break
                        candidate = normalize_url(urljoin(url, str(raw)))
                        if not allowed(candidate):
                            continue
                        if not is_probably_download(candidate):
                            continue
                        if candidate in downloaded:
                            continue
                        # Do not mark download as visited page; keep it separate
                        out_path = download_best_effort(context, page, out_dir=out_dir, url=candidate, index_file=index_file)
                        if out_path is not None:
                            saved_downloads += 1
                            downloaded.add(candidate)

                # Optionally rewrite markdown links to point to local files
                if (
                    args.rewrite_links
                    and _markdownify is not None
                    and args.format in {"html+md", "md"}
                    and saved is not None
                ):
                    md_path = saved.md_path
                    if not md_path.exists():
                        md = ""
                    else:
                        md = md_path.read_text(encoding="utf-8")

                    def attachment_mapper(u: str) -> Optional[str]:
                        # Ensure the attachment exists; download on demand.
                        # This keeps markdown links stable and offline.
                        out = download_best_effort(context, page, out_dir=out_dir, url=u, index_file=index_file)
                        return str(out) if out else None

                    md2 = rewrite_markdown_links(
                        md,
                        page_url=url,
                        out_dir=out_dir,
                        allow_url=allowed,
                        attachment_mapper=attachment_mapper,
                    )
                    if md2 != md:
                        md_path.write_text(md2, encoding="utf-8")

                time.sleep(max(0, args.polite_delay_ms) / 1000.0)

            except Exception as e:
                write_index_entry(
                    index_file,
                    {
                        "url": url,
                        "kind": "error",
                        "error": f"{type(e).__name__}: {e}",
                        "time_utc": utc_now_iso(),
                    },
                )
                continue

        if args.pause_on_exit_seconds > 0 and args.headful:
            print(f"Pausing {args.pause_on_exit_seconds}s before closing browser...")
            time.sleep(args.pause_on_exit_seconds)
        if args.keep_open and args.headful:
            print("Keeping browser open. Press Ctrl+C in this terminal to exit and close it.")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
        # Cleanup:
        # - In CDP mode we must NOT close the user-driven Chrome instance (it would log you out / lose state).
        #   Just close the tab we opened (best-effort).
        if connected_over_cdp:
            try:
                if page is not None:
                    page.close()
            except Exception:
                pass
        else:
            try:
                context.close()
            finally:
                if browser is not None:
                    browser.close()

    write_toc(out_dir=out_dir, index_file=index_file)

    summary = {
        "start_urls": start_urls,
        "out_dir": str(out_dir),
        "storage_state": str(storage_state),
        "saved_pages": saved_pages,
        "saved_downloads": saved_downloads,
        "index": str(index_file),
        "time_utc": utc_now_iso(),
    }
    ensure_parent(out_dir / "summary.json")
    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
