#!/usr/bin/env python3
"""
Parallel downloader for Europe PMC fullTextXML by PMCID.

Use this when you already have a PMCID list filtered to OA + inPMC (e.g. from
`discover_epmc_pmcids_fast.py`) and you want to speed up large-scale XML pulls.

Compliance:
- Downloads only from the official Europe PMC API endpoint:
    https://www.ebi.ac.uk/europepmc/webservices/rest/{PMCID}/fullTextXML
- Does not bypass paywalls or use non-compliant sources.

Outputs:
- <out>/<PMCID>.xml
- <out>/download_manifest.jsonl (append-only; schema compatible with
  `fetch_open_access_papers.py`, but only emits the `xml` action)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import requests


PMCID_RE = re.compile(r"^PMC\d+$", re.IGNORECASE)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_pmcid(raw: str) -> Optional[str]:
    s = (raw or "").strip()
    if not s or s.startswith("#"):
        return None
    if s.upper().startswith("PMCID:"):
        s = s.split(":", 1)[1].strip()
    s = s.upper()
    if not PMCID_RE.match(s):
        return None
    return s


def fulltext_xml_url(pmcid: str) -> str:
    return f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"


@dataclass
class DownloadOutcome:
    pmcid: str
    entry: dict[str, Any]
    status: str


def download_one(
    pmcid: str,
    *,
    out_dir: Path,
    timeout_s: int,
    retries: int,
    overwrite: bool,
    user_agent: str,
) -> DownloadOutcome:
    url = fulltext_xml_url(pmcid)
    xml_path = out_dir / f"{pmcid}.xml"
    tmp_path = xml_path.with_suffix(xml_path.suffix + ".part")

    entry: dict[str, Any] = {
        "retrieved_at": utc_now_iso(),
        "input": pmcid,
        "id_type": "pmcid",
        "normalized": pmcid,
        "actions": [],
    }

    if xml_path.exists() and not overwrite:
        entry["actions"].append(
            {
                "kind": "xml",
                "via": "europepmc",
                "url": url,
                "download": {"status": "skipped_exists"},
                "meta": {"pmcid": pmcid, "pmid": None, "doi": None},
                "path": str(xml_path),
            }
        )
        return DownloadOutcome(pmcid=pmcid, entry=entry, status="skipped_exists")

    last_dl: dict[str, Any] = {"status": "not_attempted"}
    last_err: str = ""

    for attempt in range(int(retries) + 1):
        try:
            if tmp_path.exists():
                tmp_path.unlink()
        except Exception:
            pass

        try:
            r = requests.get(url, timeout=timeout_s, headers={"User-Agent": user_agent}, allow_redirects=True)
            http_status = int(r.status_code)

            if http_status == 200:
                content = r.content
                if not content:
                    last_dl = {"status": "empty_response", "http_status": http_status}
                else:
                    tmp_path.write_bytes(content)
                    tmp_path.replace(xml_path)
                    last_dl = {"status": "downloaded", "http_status": http_status}
                break

            last_dl = {"status": "http_error", "http_status": http_status}

            # Retry on rate limiting / transient server errors.
            if http_status in (429, 500, 502, 503, 504) and attempt < int(retries):
                backoff = min(60.0, (2.0**attempt) + random.random())
                time.sleep(backoff)
                continue
            break

        except requests.RequestException as e:
            last_err = repr(e)
            last_dl = {"status": "exception", "error": last_err}
            if attempt < int(retries):
                backoff = min(60.0, (2.0**attempt) + random.random())
                time.sleep(backoff)
                continue
            break
        except Exception as e:
            last_err = repr(e)
            last_dl = {"status": "exception", "error": last_err}
            break

    action: dict[str, Any] = {
        "kind": "xml",
        "via": "europepmc",
        "url": url,
        "download": last_dl,
        "meta": {"pmcid": pmcid, "pmid": None, "doi": None},
    }
    if last_dl.get("status") in ("downloaded", "skipped_exists") and xml_path.exists():
        action["path"] = str(xml_path)
        if last_dl.get("status") == "downloaded":
            try:
                action["sha256"] = sha256_file(xml_path)
            except Exception:
                pass
    entry["actions"].append(action)

    if last_dl.get("status") == "downloaded":
        status = "downloaded"
    else:
        status = str(last_dl.get("status") or "unknown")
    if status == "http_error":
        status = f"http_{last_dl.get('http_status')}"
    if status == "exception" and last_err:
        status = "exception"
    return DownloadOutcome(pmcid=pmcid, entry=entry, status=status)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Text file with one PMCID per line (e.g. PMC123...).")
    ap.add_argument("--out", required=True, help="Output directory (writes <PMCID>.xml + download_manifest.jsonl).")
    ap.add_argument("--workers", type=int, default=8, help="Concurrent workers (default: 8).")
    ap.add_argument("--timeout", type=int, default=45, help="HTTP timeout seconds (default: 45).")
    ap.add_argument("--retries", type=int, default=2, help="Retries on transient errors (default: 2).")
    ap.add_argument("--delay", type=float, default=0.0, help="Optional delay after each completed item (seconds).")
    ap.add_argument("--overwrite", action="store_true", help="Overwrite existing XML files.")
    ap.add_argument(
        "--user-agent",
        type=str,
        default="epmc-fulltextxml-parallel/0.1 (+contact via docs pipeline)",
        help="HTTP User-Agent string.",
    )
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = out_dir / "download_manifest.jsonl"

    raw_lines = Path(args.input).read_text(encoding="utf-8", errors="ignore").splitlines()
    pmcids: list[str] = []
    seen: set[str] = set()
    for line in raw_lines:
        pmcid = normalize_pmcid(line)
        if not pmcid or pmcid in seen:
            continue
        seen.add(pmcid)
        pmcids.append(pmcid)

    if not pmcids:
        print("No valid PMCIDs found in input.", file=sys.stderr)
        return 2

    total = len(pmcids)
    counts: dict[str, int] = {}

    started = time.time()
    print(f"Downloading {total} Europe PMC fullTextXML files into: {out_dir}", file=sys.stderr)
    print(f"Manifest: {manifest_path}", file=sys.stderr)

    with manifest_path.open("a", encoding="utf-8") as mf:
        with ThreadPoolExecutor(max_workers=max(1, int(args.workers))) as ex:
            futs = [
                ex.submit(
                    download_one,
                    pmcid,
                    out_dir=out_dir,
                    timeout_s=int(args.timeout),
                    retries=int(args.retries),
                    overwrite=bool(args.overwrite),
                    user_agent=str(args.user_agent),
                )
                for pmcid in pmcids
            ]

            done_n = 0
            for fut in as_completed(futs):
                try:
                    outcome = fut.result()
                except Exception as e:
                    # Should be rare; keep manifest auditable.
                    done_n += 1
                    st = "worker_exception"
                    counts[st] = counts.get(st, 0) + 1
                    entry = {
                        "retrieved_at": utc_now_iso(),
                        "input": "",
                        "id_type": "pmcid",
                        "normalized": "",
                        "actions": [],
                        "error": repr(e),
                    }
                    mf.write(json.dumps(entry, ensure_ascii=False) + "\n")
                else:
                    done_n += 1
                    counts[outcome.status] = counts.get(outcome.status, 0) + 1
                    mf.write(json.dumps(outcome.entry, ensure_ascii=False) + "\n")

                if done_n % 50 == 0 or done_n == total:
                    elapsed = max(1e-6, time.time() - started)
                    rate = done_n / elapsed
                    top = sorted(counts.items(), key=lambda x: (-x[1], x[0]))[:8]
                    top_s = ", ".join([f"{k}={v}" for k, v in top])
                    print(f"[{done_n}/{total}] {rate:.2f} items/s | {top_s}", file=sys.stderr)

                if args.delay:
                    time.sleep(max(0.0, float(args.delay)))

    print("Done.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

