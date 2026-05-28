#!/usr/bin/env python3
"""
Batch download *open-access* papers (PDF and/or full-text XML) from public APIs.

This script is designed to be compliant:
- It only downloads PDFs when an explicit open-access PDF URL is provided by OA
  discovery services (e.g., Unpaywall/OpenAlex) or when the user supplies a direct URL.
- It does NOT bypass paywalls, library proxies, or anti-bot protections.

Supported identifiers per line:
- DOI (e.g., 10.1186/s12859-024-05748-z) or https://doi.org/<doi>
- PMID (digits)
- PMCID (e.g., PMC11010298)
- arXiv id (e.g., 2101.01234 or arXiv:2101.01234v2)
- Direct URL (http/https)

Outputs:
- Downloaded files under --out
- A JSONL manifest (download_manifest.jsonl) with resolution and hashes

Examples:
  export UNPAYWALL_EMAIL="you@lab.edu"
  python scripts/fetch_open_access_papers.py --input papers.txt --out oa_papers --format both
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Optional
from urllib.parse import quote, urljoin, urlparse

import requests


DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$", re.IGNORECASE)
PMCID_RE = re.compile(r"^PMC\d+$", re.IGNORECASE)
ARXIV_RE = re.compile(r"^(?:arXiv:)?(\d{4}\.\d{4,5})(v\d+)?$", re.IGNORECASE)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_stem(text: str, max_len: int = 120) -> str:
    s = text.strip()
    s = re.sub(r"^https?://(dx\.)?doi\.org/", "", s, flags=re.IGNORECASE)
    s = re.sub(r"[^\w.\-]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    if not s:
        s = "paper"
    return s[:max_len]


def is_probably_pdf(first_bytes: bytes) -> bool:
    # Some servers may prepend whitespace/newlines before the PDF header.
    return first_bytes.lstrip().startswith(b"%PDF")


def is_probably_html(first_bytes: bytes) -> bool:
    head = first_bytes.lstrip().lower()
    return head.startswith(b"<!doctype html") or head.startswith(b"<html") or head.startswith(b"<head") or head.startswith(
        b"<script"
    )


@dataclass
class ResolveResult:
    kind: str  # pdf/xml
    url: str
    via: str  # unpaywall/openalex/europepmc/arxiv/url
    meta: dict[str, Any]


def http_get_json(url: str, *, user_agent: str, timeout_s: int) -> dict[str, Any]:
    r = requests.get(url, timeout=timeout_s, headers={"User-Agent": user_agent})
    r.raise_for_status()
    return r.json()


def _should_prefer_wget(url: str) -> bool:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if host == "ftp.ncbi.nlm.nih.gov" and "/pub/pmc/oa_package/" in (parsed.path or ""):
        return shutil.which("wget") is not None
    return False


def _download_with_wget(
    url: str,
    out_path: Path,
    *,
    overwrite: bool,
    timeout_s: int,
    max_bytes: int = 0,
    max_seconds: int = 0,
) -> dict[str, Any]:
    if out_path.exists() and not overwrite:
        return {"status": "skipped_exists"}

    tmp_path = out_path.with_suffix(out_path.suffix + ".part")
    if tmp_path.exists() and overwrite:
        tmp_path.unlink()

    cmd = [
        "wget",
        "--continue",
        "--max-redirect=20",
        f"--timeout={int(timeout_s)}",
        "--tries=2",
        "-O",
        str(tmp_path),
        url,
    ]

    try:
        completed = subprocess.run(
            cmd,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=(int(max_seconds) if max_seconds else None),
        )
    except subprocess.TimeoutExpired:
        bytes_written = tmp_path.stat().st_size if tmp_path.exists() else 0
        return {"status": "timeout_total", "bytes_written": bytes_written, "max_seconds": max_seconds, "kept_partial": True}

    if not tmp_path.exists():
        return {"status": "wget_error"}

    if completed.returncode != 0:
        bytes_written = tmp_path.stat().st_size if tmp_path.exists() else 0
        return {
            "status": "wget_error",
            "returncode": int(completed.returncode),
            "bytes_written": bytes_written,
            "kept_partial": True,
        }

    size = tmp_path.stat().st_size
    if max_bytes and size > max_bytes:
        try:
            tmp_path.unlink(missing_ok=True)
        except Exception:
            pass
        return {"status": "too_large", "bytes_written": size, "max_bytes": max_bytes}

    # Refuse obvious HTML "challenge"/landing pages.
    try:
        with tmp_path.open("rb") as f:
            head = f.read(512)
    except Exception:
        head = b""
    if head and is_probably_html(head):
        try:
            tmp_path.unlink(missing_ok=True)
        except Exception:
            pass
        return {"status": "not_file"}

    tmp_path.replace(out_path)
    return {"status": "downloaded", "http_status": 200}


def resolve_europepmc_record(query: str, *, user_agent: str, timeout_s: int) -> Optional[dict[str, Any]]:
    url = (
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
        f"?query={quote(query)}&format=json&pageSize=1"
    )
    data = http_get_json(url, user_agent=user_agent, timeout_s=timeout_s)
    hit_count = int(data.get("hitCount") or 0)
    if hit_count <= 0:
        return None
    results = (((data.get("resultList") or {}).get("result")) or [])
    if not results:
        return None
    return results[0]


def resolve_fulltext_xml_url(pmcid: str) -> str:
    # Europe PMC provides JATS XML for OA articles available in PMC.
    # Example: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11010298/fullTextXML
    return f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"


def resolve_unpaywall_pdf(doi: str, *, email: str, user_agent: str, timeout_s: int) -> Optional[ResolveResult]:
    url = f"https://api.unpaywall.org/v2/{quote(doi)}?email={quote(email)}"
    try:
        data = http_get_json(url, user_agent=user_agent, timeout_s=timeout_s)
    except requests.HTTPError as e:
        return None

    if not data.get("is_oa"):
        return None

    def pick_pdf(loc: dict[str, Any]) -> Optional[str]:
        return loc.get("url_for_pdf") or None

    best = data.get("best_oa_location") or {}
    pdf_url = pick_pdf(best)
    if not pdf_url:
        for loc in (data.get("oa_locations") or []):
            pdf_url = pick_pdf(loc or {})
            if pdf_url:
                break

    if not pdf_url:
        # As a last resort, sometimes a "url" is a direct PDF. Only accept obvious PDFs here.
        candidate = best.get("url")
        if isinstance(candidate, str) and candidate.lower().endswith(".pdf"):
            pdf_url = candidate

    if not pdf_url:
        return None

    meta = {
        "is_oa": data.get("is_oa"),
        "oa_status": data.get("oa_status"),
        "best_oa_location": {
            "host_type": best.get("host_type"),
            "license": best.get("license"),
            "url": best.get("url"),
            "url_for_pdf": best.get("url_for_pdf"),
        },
    }
    return ResolveResult(kind="pdf", url=pdf_url, via="unpaywall", meta=meta)


def resolve_openalex_pdf(doi: str, *, user_agent: str, timeout_s: int) -> Optional[ResolveResult]:
    # OpenAlex does not require an API key. It sometimes provides pdf_url locations.
    url = f"https://api.openalex.org/works/https://doi.org/{quote(doi)}"
    try:
        data = http_get_json(url, user_agent=user_agent, timeout_s=timeout_s)
    except requests.HTTPError:
        return None

    open_access = data.get("open_access") or {}
    if not open_access.get("is_oa"):
        return None

    pdf_url = None
    for loc in (data.get("locations") or []):
        if not isinstance(loc, dict):
            continue
        candidate = loc.get("pdf_url")
        if isinstance(candidate, str) and candidate:
            pdf_url = candidate
            break

    if not pdf_url:
        primary = data.get("primary_location") or {}
        candidate = primary.get("pdf_url")
        if isinstance(candidate, str) and candidate:
            pdf_url = candidate

    if not pdf_url:
        return None

    meta = {
        "open_access": open_access,
        "primary_location": data.get("primary_location"),
    }
    return ResolveResult(kind="pdf", url=pdf_url, via="openalex", meta=meta)


def resolve_openalex_landing(doi: str, *, user_agent: str, timeout_s: int) -> Optional[str]:
    url = f"https://api.openalex.org/works/https://doi.org/{quote(doi)}"
    try:
        data = http_get_json(url, user_agent=user_agent, timeout_s=timeout_s)
    except requests.HTTPError:
        return None
    primary = data.get("primary_location") or {}
    landing = primary.get("landing_page_url")
    return landing if isinstance(landing, str) and landing else None


def resolve_arxiv_pdf(arxiv_id: str) -> ResolveResult:
    # arXiv PDF link is stable.
    clean = arxiv_id
    if clean.lower().startswith("arxiv:"):
        clean = clean.split(":", 1)[1]
    m = ARXIV_RE.match(clean)
    if not m:
        raise ValueError(f"Invalid arXiv id: {arxiv_id}")
    base = m.group(1) + (m.group(2) or "")
    url = f"https://arxiv.org/pdf/{base}.pdf"
    return ResolveResult(kind="pdf", url=url, via="arxiv", meta={})


def download_pdf(
    url: str,
    out_path: Path,
    *,
    user_agent: str,
    timeout_s: int,
    overwrite: bool,
    max_bytes: int = 0,
    max_seconds: int = 0,
) -> dict[str, Any]:
    if out_path.exists() and not overwrite:
        return {"status": "skipped_exists"}

    tmp_path = out_path.with_suffix(out_path.suffix + ".part")
    if tmp_path.exists():
        tmp_path.unlink()

    started = time.time()
    with requests.get(url, stream=True, timeout=timeout_s, headers={"User-Agent": user_agent}, allow_redirects=True) as r:
        status = r.status_code
        if status != 200:
            return {"status": "http_error", "http_status": status}

        try:
            content_len = int((r.headers.get("content-length") or "").strip() or "0")
        except Exception:
            content_len = 0
        if max_bytes and content_len and content_len > max_bytes:
            return {"status": "too_large", "content_length": content_len, "max_bytes": max_bytes, "http_status": status}

        it = r.iter_content(chunk_size=1024 * 64)
        first = next(it, b"")
        if not first:
            return {"status": "empty_response"}

        if max_seconds and (time.time() - started) > max_seconds:
            return {"status": "timeout_total", "bytes_written": 0, "max_seconds": max_seconds, "http_status": status}

        if not is_probably_pdf(first):
            # Some hosts return HTML landing pages. Refuse to save as PDF.
            return {"status": "not_pdf"}

        with tmp_path.open("wb") as f:
            f.write(first)
            written = len(first)
            for chunk in it:
                if chunk:
                    written += len(chunk)
                    if max_bytes and written > max_bytes:
                        try:
                            tmp_path.unlink(missing_ok=True)
                        except Exception:
                            pass
                        return {"status": "too_large", "bytes_written": written, "max_bytes": max_bytes, "http_status": status}
                    if max_seconds and (time.time() - started) > max_seconds:
                        try:
                            tmp_path.unlink(missing_ok=True)
                        except Exception:
                            pass
                        return {"status": "timeout_total", "bytes_written": written, "max_seconds": max_seconds, "http_status": status}
                    f.write(chunk)

    tmp_path.replace(out_path)
    return {"status": "downloaded", "http_status": 200}


def download_text(url: str, out_path: Path, *, user_agent: str, timeout_s: int, overwrite: bool) -> dict[str, Any]:
    if out_path.exists() and not overwrite:
        return {"status": "skipped_exists"}
    r = requests.get(url, timeout=timeout_s, headers={"User-Agent": user_agent})
    if r.status_code != 200:
        return {"status": "http_error", "http_status": r.status_code}
    out_path.write_text(r.text, encoding="utf-8")
    return {"status": "downloaded", "http_status": 200}


def download_binary(
    url: str,
    out_path: Path,
    *,
    user_agent: str,
    timeout_s: int,
    overwrite: bool,
    max_bytes: int = 0,
    max_seconds: int = 0,
) -> dict[str, Any]:
    if _should_prefer_wget(url):
        return _download_with_wget(
            url,
            out_path,
            overwrite=overwrite,
            timeout_s=timeout_s,
            max_bytes=max_bytes,
            max_seconds=max_seconds,
        )

    if out_path.exists() and not overwrite:
        return {"status": "skipped_exists"}

    tmp_path = out_path.with_suffix(out_path.suffix + ".part")
    if tmp_path.exists():
        tmp_path.unlink()

    started = time.time()
    with requests.get(url, stream=True, timeout=timeout_s, headers={"User-Agent": user_agent}, allow_redirects=True) as r:
        status = r.status_code
        if status != 200:
            return {"status": "http_error", "http_status": status}

        try:
            content_len = int((r.headers.get("content-length") or "").strip() or "0")
        except Exception:
            content_len = 0
        if max_bytes and content_len and content_len > max_bytes:
            return {"status": "too_large", "content_length": content_len, "max_bytes": max_bytes, "http_status": status}

        it = r.iter_content(chunk_size=1024 * 64)
        first = next(it, b"")
        if not first:
            return {"status": "empty_response"}

        content_type = (r.headers.get("content-type") or "").lower()
        if "text/html" in content_type or is_probably_html(first):
            return {"status": "not_file"}

        with tmp_path.open("wb") as f:
            f.write(first)
            written = len(first)
            for chunk in it:
                if chunk:
                    written += len(chunk)
                    if max_bytes and written > max_bytes:
                        try:
                            tmp_path.unlink(missing_ok=True)
                        except Exception:
                            pass
                        return {"status": "too_large", "bytes_written": written, "max_bytes": max_bytes, "http_status": status}
                    if max_seconds and (time.time() - started) > max_seconds:
                        try:
                            tmp_path.unlink(missing_ok=True)
                        except Exception:
                            pass
                        return {"status": "timeout_total", "bytes_written": written, "max_seconds": max_seconds, "http_status": status}
                    f.write(chunk)

    tmp_path.replace(out_path)
    return {"status": "downloaded", "http_status": 200}


def springer_esm_base_for_doi(doi: str) -> str:
    # Works for many Springer/BMC OA supplementary assets.
    doi_enc = quote(doi, safe="")
    return f"https://static-content.springer.com/esm/art%3A{doi_enc}/MediaObjects/"


def extract_supplementary_hrefs_from_jats(xml_text: str) -> list[str]:
    blocks = re.findall(r"<supplementary-material\b[\s\S]*?</supplementary-material>", xml_text, flags=re.IGNORECASE)
    hrefs: list[str] = []
    for block in blocks:
        hrefs.extend(re.findall(r'xlink:href="([^"]+)"', block))
    # De-duplicate while preserving order
    seen: set[str] = set()
    out: list[str] = []
    for h in hrefs:
        if h and h not in seen:
            seen.add(h)
            out.append(h)
    return out


def filename_from_url(url_or_path: str) -> str:
    parsed = urlparse(url_or_path)
    name = Path(parsed.path).name if parsed.scheme else Path(url_or_path).name
    return safe_stem(name, max_len=180)


def looks_like_file_link(url_or_path: str) -> bool:
    exts = (
        ".zip",
        ".pdf",
        ".csv",
        ".tsv",
        ".txt",
        ".xlsx",
        ".xls",
        ".doc",
        ".docx",
        ".rtf",
        ".fa",
        ".fasta",
        ".json",
        ".xml",
        ".tif",
        ".tiff",
        ".png",
        ".jpg",
        ".jpeg",
        ".svg",
    )
    parsed = urlparse(url_or_path)
    path = parsed.path if parsed.scheme else url_or_path
    return any(path.lower().endswith(ext) for ext in exts)


def pmc_instance_bin_base(pmcid: str) -> Optional[str]:
    # PMC "bin" downloads typically use /articles/instance/<digits>/bin/<file>
    m = re.match(r"^PMC(\d+)$", pmcid, flags=re.IGNORECASE)
    if not m:
        return None
    digits = m.group(1)
    return f"https://pmc.ncbi.nlm.nih.gov/articles/instance/{digits}/bin/"


def resolve_pmc_oa_package_url(pmcid: str, *, user_agent: str, timeout_s: int) -> Optional[str]:
    # Official NCBI endpoint for PMC Open Access subset packages.
    # Example: https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id=PMC11010298
    url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id={quote(pmcid)}"
    r = requests.get(url, timeout=timeout_s, headers={"User-Agent": user_agent})
    if r.status_code != 200:
        return None
    # Prefer tar.gz (oa_package). NCBI returns a tiny XML payload; parse hrefs robustly.
    hrefs = re.findall(r'href=[\'"]([^\'"]+)[\'"]', r.text, flags=re.IGNORECASE)
    for href in hrefs:
        if "/pub/pmc/oa_package/" in href and (href.endswith(".tar.gz") or href.endswith(".tgz")):
            if href.startswith("ftp://"):
                return href.replace("ftp://", "https://", 1)
            if href.startswith("http://"):
                return href.replace("http://", "https://", 1)
            return href

    # Fallback: some responses may not quote the URL the way we expect.
    m = re.search(
        r"(?:ftp|https?)://ftp\.ncbi\.nlm\.nih\.gov/pub/pmc/oa_package/\S+?\.(?:tar\.gz|tgz)",
        r.text,
        flags=re.IGNORECASE,
    )
    if not m:
        return None
    href = m.group(0)
    return href.replace("ftp://", "https://", 1).replace("http://", "https://", 1)


def extract_selected_from_pmc_tar(
    tar_gz_path: Path,
    *,
    out_pdf_path: Path,
    supp_dir: Path,
    overwrite: bool,
) -> dict[str, Any]:
    extracted_pdf = False
    extracted_supp = 0
    pdf_candidates: list[tuple[int, tarfile.TarInfo]] = []
    chosen_pdf_member: Optional[tarfile.TarInfo] = None

    # Supplementary-like file extensions we care about.
    supp_exts = (
        ".zip",
        ".csv",
        ".tsv",
        ".txt",
        ".xlsx",
        ".xls",
        ".doc",
        ".docx",
        ".rtf",
        ".fa",
        ".fasta",
        ".json",
        ".pdf",  # supplementary PDFs (mmc*.pdf) should land in supp_dir
    )

    with tarfile.open(tar_gz_path, mode="r:gz") as tf:
        members = [m for m in tf.getmembers() if m.isfile()]
        for m in members:
            name = Path(m.name).name
            if name.lower().endswith(".pdf"):
                pdf_candidates.append((m.size, m))

        # Choose the largest PDF as the main article PDF (heuristic).
        pdf_candidates.sort(key=lambda x: x[0], reverse=True)
        if pdf_candidates:
            chosen_pdf_member = pdf_candidates[0][1]
            if overwrite or not out_pdf_path.exists():
                f = tf.extractfile(chosen_pdf_member)
                if f is not None:
                    tmp_path = out_pdf_path.with_suffix(out_pdf_path.suffix + ".part")
                    if tmp_path.exists():
                        tmp_path.unlink()
                    with tmp_path.open("wb") as out_f:
                        out_f.write(f.read())
                    tmp_path.replace(out_pdf_path)
                    extracted_pdf = True

        # Extract supplementary-like assets by extension into supp_dir (flat).
        supp_dir.mkdir(parents=True, exist_ok=True)
        for m in members:
            name = Path(m.name).name
            if not any(name.lower().endswith(ext) for ext in supp_exts):
                continue
            # Skip the (largest) main PDF member to avoid duplication in supp_dir.
            if chosen_pdf_member and m.name == chosen_pdf_member.name:
                continue

            out_path = supp_dir / safe_stem(name, max_len=180)
            if out_path.exists() and not overwrite:
                continue
            f = tf.extractfile(m)
            if f is None:
                continue
            tmp_path = out_path.with_suffix(out_path.suffix + ".part")
            if tmp_path.exists():
                tmp_path.unlink()
            with tmp_path.open("wb") as out_f:
                out_f.write(f.read())
            tmp_path.replace(out_path)
            extracted_supp += 1

    return {"extracted_pdf": extracted_pdf, "extracted_supp_files": extracted_supp, "pdf_candidates": len(pdf_candidates)}


class _LinkExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        if tag.lower() != "a":
            return
        for k, v in attrs:
            if k.lower() == "href" and v:
                self.links.append(v)


def extract_candidate_supp_links_from_html(html_text: str, base_url: str) -> list[str]:
    parser = _LinkExtractor()
    try:
        parser.feed(html_text)
    except Exception:
        return []

    keywords = (
        "supplement",
        "supporting",
        "additional",
        "moesm",
        "esm",
        "suppl",
        "source-data",
        "source_data",
    )
    exts = (
        ".zip",
        ".pdf",
        ".csv",
        ".tsv",
        ".txt",
        ".xlsx",
        ".xls",
        ".doc",
        ".docx",
        ".rtf",
        ".fa",
        ".fasta",
        ".json",
        ".xml",
        ".tif",
        ".tiff",
        ".png",
        ".jpg",
        ".jpeg",
        ".svg",
    )

    out: list[str] = []
    seen: set[str] = set()
    for href in parser.links:
        abs_url = urljoin(base_url, href)
        low = abs_url.lower()
        if abs_url in seen:
            continue
        seen.add(abs_url)
        if any(k in low for k in keywords) or any(low.endswith(ext) for ext in exts):
            out.append(abs_url)
    return out

def classify_identifier(raw: str) -> tuple[str, str]:
    s = raw.strip()
    if not s:
        return ("empty", s)

    # URL
    if s.lower().startswith(("http://", "https://")):
        # DOI URL?
        doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", s, flags=re.IGNORECASE)
        if DOI_RE.match(doi):
            return ("doi", doi)
        return ("url", s)

    if PMCID_RE.match(s):
        return ("pmcid", s.upper())

    if s.isdigit():
        return ("pmid", s)

    if DOI_RE.match(s):
        return ("doi", s)

    if ARXIV_RE.match(s):
        return ("arxiv", s)

    return ("unknown", s)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help="Path to a txt file (one id per line).")
    parser.add_argument("--out", type=str, default="oa_papers", help="Output directory.")
    parser.add_argument("--format", choices=["pdf", "xml", "both"], default="pdf", help="What to download.")
    parser.add_argument("--unpaywall-email", type=str, default=os.environ.get("UNPAYWALL_EMAIL", ""), help="Email for Unpaywall.")
    parser.add_argument("--user-agent", type=str, default="oa-fetcher/0.1 (+contact via UNPAYWALL_EMAIL)", help="HTTP User-Agent.")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between items (seconds).")
    parser.add_argument("--timeout", type=int, default=40, help="HTTP timeout (seconds).")
    parser.add_argument("--max-file-mb", type=int, default=0, help="Abort a single binary download if larger than this (0 disables).")
    parser.add_argument(
        "--max-file-seconds",
        type=int,
        default=0,
        help="Abort a single binary download if it exceeds this wall-clock time budget (0 disables).",
    )
    parser.add_argument(
        "--resume",
        action=argparse.BooleanOptionalAction,
        default=True,
        help=(
            "Resume from an existing download_manifest.jsonl by skipping ids that already have a completed entry. "
            "Failed/transient attempts (timeouts, wget errors, 5xx/429) are retried. Disable with --no-resume."
        ),
    )
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files.")
    parser.add_argument("--supplementary", action="store_true", help="Try to download supplementary files (OA only).")
    parser.add_argument(
        "--no-pmc-oa-package",
        dest="pmc_oa_package",
        action="store_false",
        help="Disable downloading PMC Open Access tar.gz packages (recommended to keep on for supplementary).",
    )
    parser.set_defaults(pmc_oa_package=True)
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = out_dir / "download_manifest.jsonl"

    ids: list[str] = []
    if args.input:
        p = Path(args.input)
        if not p.exists():
            print(f"Input not found: {p}", file=sys.stderr)
            return 2
        for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            ids.append(line)
    else:
        print("Provide --input with one id per line.", file=sys.stderr)
        return 2

    want_pdf = args.format in ("pdf", "both")
    want_xml = args.format in ("xml", "both")

    user_agent = args.user_agent
    if "(+contact" in user_agent and args.unpaywall_email:
        user_agent = user_agent.replace("UNPAYWALL_EMAIL", args.unpaywall_email)

    max_bytes = int(args.max_file_mb) * 1024 * 1024 if int(args.max_file_mb) > 0 else 0
    max_seconds = int(args.max_file_seconds) if int(args.max_file_seconds) > 0 else 0

    # Resume support: skip ids that already have a non-retriable manifest entry.
    already_done: set[str] = set()
    if args.resume and (not args.overwrite) and manifest_path.exists():
        last_by_input: dict[str, dict[str, Any]] = {}
        for line in manifest_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            raw = str(rec.get("input") or "").strip()
            if not raw:
                continue
            last_by_input[raw] = rec

        def _needs_retry(rec: dict[str, Any]) -> bool:
            if rec.get("error"):
                return True
            for a in (rec.get("actions") or []):
                if not isinstance(a, dict):
                    continue
                dl = a.get("download")
                if isinstance(dl, dict):
                    st = str(dl.get("status") or "")
                    if st in ("timeout_total", "wget_error", "empty_response"):
                        return True
                    if st == "http_error":
                        try:
                            code = int(dl.get("http_status") or 0)
                        except Exception:
                            code = 0
                        if code in (429, 500, 502, 503, 504):
                            return True
                else:
                    # For older manifest entries that used top-level status.
                    st = str(a.get("status") or "")
                    if st in ("timeout_total", "wget_error", "empty_response"):
                        return True
            return False

        for raw, rec in last_by_input.items():
            if not _needs_retry(rec):
                already_done.add(raw)

    total_ids = len(ids)
    for i, raw in enumerate(ids, start=1):
        if i == 1 or (i % 25 == 0) or (i == total_ids):
            print(f"[progress] {i}/{total_ids}: {raw}", file=sys.stderr, flush=True)
        if raw in already_done:
            continue
        id_type, value = classify_identifier(raw)
        stem = safe_stem(value)
        resolved_doi: Optional[str] = value if id_type == "doi" else None
        resolved_landing: Optional[str] = None
        downloaded_xml_path: Optional[Path] = None
        resolved_pmcid: Optional[str] = value if id_type == "pmcid" else None
        extracted_from_pmc_package = False
        pdf_ok = False

        entry: dict[str, Any] = {
            "retrieved_at": utc_now_iso(),
            "input": raw,
            "id_type": id_type,
            "normalized": value,
            "actions": [],
        }

        try:
            # Resolve PDF (OA only)
            if want_pdf:
                pdf_result: Optional[ResolveResult] = None

                if id_type == "arxiv":
                    pdf_result = resolve_arxiv_pdf(value)
                elif id_type == "doi":
                    if args.unpaywall_email:
                        pdf_result = resolve_unpaywall_pdf(
                            value, email=args.unpaywall_email, user_agent=user_agent, timeout_s=args.timeout
                        )
                    if not pdf_result:
                        pdf_result = resolve_openalex_pdf(value, user_agent=user_agent, timeout_s=args.timeout)
                    resolved_landing = resolve_openalex_landing(value, user_agent=user_agent, timeout_s=args.timeout)
                elif id_type in ("pmid", "pmcid"):
                    # Try to map to DOI via Europe PMC, then use OA resolvers.
                    query = f"EXT_ID:{value}" if id_type == "pmid" else f"PMCID:{value}"
                    try:
                        rec = resolve_europepmc_record(query, user_agent=user_agent, timeout_s=args.timeout)
                    except Exception:
                        rec = None
                    doi = (rec or {}).get("doi")
                    if isinstance(doi, str) and DOI_RE.match(doi):
                        resolved_doi = doi
                        if args.unpaywall_email:
                            pdf_result = resolve_unpaywall_pdf(
                                doi, email=args.unpaywall_email, user_agent=user_agent, timeout_s=args.timeout
                            )
                        if not pdf_result:
                            pdf_result = resolve_openalex_pdf(doi, user_agent=user_agent, timeout_s=args.timeout)
                        resolved_landing = resolve_openalex_landing(doi, user_agent=user_agent, timeout_s=args.timeout)
                elif id_type == "url":
                    pdf_result = ResolveResult(kind="pdf", url=value, via="url", meta={})

                if pdf_result:
                    pdf_path = out_dir / f"{stem}.pdf"
                    dl = download_pdf(
                        pdf_result.url,
                        pdf_path,
                        user_agent=user_agent,
                        timeout_s=args.timeout,
                        overwrite=args.overwrite,
                        max_bytes=max_bytes,
                        max_seconds=max_seconds,
                    )
                    action = {
                        "kind": "pdf",
                        "via": pdf_result.via,
                        "url": pdf_result.url,
                        "download": dl,
                        "meta": pdf_result.meta,
                    }
                    if dl.get("status") == "downloaded":
                        action["path"] = str(pdf_path)
                        action["sha256"] = sha256_file(pdf_path)
                    pdf_ok = dl.get("status") in ("downloaded", "skipped_exists") and pdf_path.exists()
                    entry["actions"].append(action)
                else:
                    entry["actions"].append({"kind": "pdf", "status": "no_oa_pdf_found"})

            # Resolve full-text XML (Europe PMC; OA in PMC)
            if want_xml:
                pmcid: Optional[str] = None
                rec: Optional[dict[str, Any]] = None
                if id_type == "pmcid":
                    # Fast-path: when the input is a PMCID, directly try Europe PMC fullTextXML.
                    # Avoid an extra "search" round-trip (PMCID:...) per item for large-scale runs.
                    pmcid = value
                elif id_type == "pmid":
                    rec = resolve_europepmc_record(f"EXT_ID:{value}", user_agent=user_agent, timeout_s=args.timeout)
                    pmcid = (rec or {}).get("pmcid")
                elif id_type == "doi":
                    rec = resolve_europepmc_record(f"DOI:{value}", user_agent=user_agent, timeout_s=args.timeout)
                    pmcid = (rec or {}).get("pmcid")
                    doi = (rec or {}).get("doi")
                    if isinstance(doi, str) and DOI_RE.match(doi):
                        resolved_doi = doi

                if isinstance(pmcid, str) and PMCID_RE.match(pmcid):
                    resolved_pmcid = pmcid
                    # Only attempt XML when Europe PMC/PMC indicates OA (except when input is already a PMCID).
                    if id_type == "pmcid":
                        is_oa = True
                        in_pmc = True
                    else:
                        is_oa = (rec or {}).get("isOpenAccess") == "Y"
                        in_pmc = (rec or {}).get("inPMC") == "Y"

                    if is_oa and in_pmc:
                        xml_url = resolve_fulltext_xml_url(pmcid)
                        xml_path = out_dir / f"{stem}.xml"
                        dl = download_text(
                            xml_url,
                            xml_path,
                            user_agent=user_agent,
                            timeout_s=args.timeout,
                            overwrite=args.overwrite,
                        )
                        action = {
                            "kind": "xml",
                            "via": "europepmc",
                            "url": xml_url,
                            "download": dl,
                            "meta": {"pmcid": pmcid, "pmid": (rec or {}).get("pmid"), "doi": (rec or {}).get("doi")},
                        }
                        if dl.get("status") == "downloaded":
                            action["path"] = str(xml_path)
                            action["sha256"] = sha256_file(xml_path)
                            downloaded_xml_path = xml_path
                        elif dl.get("status") == "skipped_exists" and xml_path.exists():
                            action["path"] = str(xml_path)
                            downloaded_xml_path = xml_path
                        entry["actions"].append(action)
                    else:
                        entry["actions"].append(
                            {"kind": "xml", "status": "not_open_access_in_pmc", "pmcid": pmcid, "meta": rec or {}}
                        )
                else:
                    entry["actions"].append({"kind": "xml", "status": "no_pmcid_found"})

            # Supplementary download (OA only; best-effort)
            if args.supplementary:
                supp_dir = out_dir / "supplementary" / stem
                supp_dir.mkdir(parents=True, exist_ok=True)

                supp_hrefs: list[str] = []
                supp_failed = False
                supp_links_found = False
                has_suppl_flag = str((rec or {}).get("hasSuppl") or "").strip().upper() == "Y"
                if (not downloaded_xml_path) and (out_dir / f"{stem}.xml").exists():
                    downloaded_xml_path = out_dir / f"{stem}.xml"
                if downloaded_xml_path and downloaded_xml_path.exists():
                    xml_text = downloaded_xml_path.read_text(encoding="utf-8", errors="ignore")
                    supp_hrefs = [h for h in extract_supplementary_hrefs_from_jats(xml_text) if looks_like_file_link(h)]

                # Fallback: scrape landing page for obvious supplementary links (best-effort; may be blocked by some hosts)
                if not supp_hrefs and resolved_landing:
                    try:
                        r = requests.get(resolved_landing, timeout=args.timeout, headers={"User-Agent": user_agent})
                        if r.status_code == 200 and "text/html" in (r.headers.get("content-type") or "").lower():
                            supp_hrefs = [u for u in extract_candidate_supp_links_from_html(r.text, resolved_landing) if looks_like_file_link(u)]
                    except Exception:
                        supp_hrefs = []

                if not supp_hrefs:
                    # Important: when the record indicates supplementary exists (or the user explicitly requested it),
                    # JATS may still omit direct file links. Prefer the official PMC OA package fallback in that case.
                    if has_suppl_flag:
                        supp_failed = True
                    entry["actions"].append({"kind": "supplementary", "status": "no_supp_links_found"})
                else:
                    supp_links_found = True
                    for href in supp_hrefs:
                        candidates: list[str] = []
                        if href.lower().startswith(("http://", "https://")):
                            candidates.append(href)
                        else:
                            if resolved_doi:
                                candidates.append(springer_esm_base_for_doi(resolved_doi) + quote(href, safe="/._-"))
                            if resolved_pmcid:
                                base = pmc_instance_bin_base(resolved_pmcid)
                                if base:
                                    candidates.append(base + quote(href, safe="/._-"))

                        if not candidates:
                            supp_failed = True
                            entry["actions"].append({"kind": "supplementary", "href": href, "status": "no_candidate_url"})
                            continue

                        name = filename_from_url(href)
                        out_path = supp_dir / name

                        last_dl: dict[str, Any] = {"status": "not_attempted"}
                        selected_url: Optional[str] = None
                        for cand in candidates:
                            selected_url = cand
                            last_dl = download_binary(
                                cand,
                                out_path,
                                user_agent=user_agent,
                                timeout_s=args.timeout,
                                overwrite=args.overwrite,
                                max_bytes=max_bytes,
                                max_seconds=max_seconds,
                            )
                            if last_dl.get("status") in ("downloaded", "skipped_exists"):
                                break
                        if last_dl.get("status") not in ("downloaded", "skipped_exists"):
                            supp_failed = True

                        action = {
                            "kind": "supplementary",
                            "via": "jats_or_html",
                            "href": href,
                            "candidates": candidates,
                            "url": selected_url,
                            "download": last_dl,
                        }
                        if last_dl.get("status") in ("downloaded", "skipped_exists") and out_path.exists():
                            action["path"] = str(out_path)
                            action["sha256"] = sha256_file(out_path)
                        entry["actions"].append(action)

                # If the paper is in PMC Open Access subset, prefer the official OA package for robust PDF/supp retrieval.
                if args.pmc_oa_package and resolved_pmcid:
                    need_pmc_package = (want_pdf and not pdf_ok) or (args.supplementary and (supp_failed or (has_suppl_flag and not supp_links_found)))
                    if not need_pmc_package:
                        entry["actions"].append(
                            {"kind": "pmc_oa_package", "status": "skipped_not_needed", "pmcid": resolved_pmcid}
                        )
                    else:
                        pkg_dir = out_dir / "pmc_oa_packages"
                        pkg_dir.mkdir(parents=True, exist_ok=True)
                        pkg_url = resolve_pmc_oa_package_url(resolved_pmcid, user_agent=user_agent, timeout_s=args.timeout)
                        if pkg_url:
                            pkg_path = pkg_dir / f"{stem}.tar.gz"
                            dl = download_binary(
                                pkg_url,
                                pkg_path,
                                user_agent=user_agent,
                                timeout_s=args.timeout,
                                overwrite=args.overwrite,
                                max_bytes=max_bytes,
                                max_seconds=max_seconds,
                            )
                            pkg_action: dict[str, Any] = {
                                "kind": "pmc_oa_package",
                                "via": "ncbi_oa_fcgi",
                                "url": pkg_url,
                                "download": dl,
                                "pmcid": resolved_pmcid,
                            }
                            if dl.get("status") in ("downloaded", "skipped_exists") and pkg_path.exists():
                                pkg_action["path"] = str(pkg_path)
                                pkg_action["sha256"] = sha256_file(pkg_path)
                                # Extract selected content (PDF + supplementary-like files).
                                try:
                                    extract_info = extract_selected_from_pmc_tar(
                                        pkg_path,
                                        out_pdf_path=out_dir / f"{stem}.pdf",
                                        supp_dir=supp_dir,
                                        overwrite=args.overwrite,
                                    )
                                    pkg_action["extract"] = extract_info
                                    extracted_from_pmc_package = True
                                except Exception as e:
                                    pkg_action["extract_error"] = repr(e)
                            entry["actions"].append(pkg_action)
                        else:
                            entry["actions"].append(
                                {"kind": "pmc_oa_package", "status": "no_oa_package_found", "pmcid": resolved_pmcid}
                            )

        except Exception as e:
            entry["error"] = repr(e)

        with manifest_path.open("a", encoding="utf-8") as mf:
            mf.write(json.dumps(entry, ensure_ascii=False) + "\n")

        if i < len(ids):
            time.sleep(max(0.0, float(args.delay)))

    print(f"Done. Manifest: {manifest_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
