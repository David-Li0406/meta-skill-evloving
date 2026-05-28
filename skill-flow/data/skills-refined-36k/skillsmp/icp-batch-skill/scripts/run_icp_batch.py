#!/usr/bin/env python3
"""
Batch ICP query workflow with cache-first strategy.

Steps:
- Extract domains from workbook (default: domains.xlsx, column named '链接').
- Load cache file (icp_results.csv) to reuse successes (status_code=200, code=1).
- Call API for missing/failed entries using AppCode auth.
- Rewrite cache, write success summary, and append two columns (备案主体/备案号) to workbook.
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

import openpyxl
import requests


DOMAIN_PATTERN = re.compile(r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def extract_domains(workbook_path: Path, link_header: str = "链接") -> List[str]:
    wb = openpyxl.load_workbook(workbook_path, data_only=True, read_only=True)
    ws = wb.active
    rows = ws.iter_rows(values_only=True)
    try:
        header = next(rows)
    except StopIteration:
        return []

    # Locate column
    col_idx = None
    for idx, val in enumerate(header):
        if val == link_header:
            col_idx = idx
            break
    if col_idx is None:
        col_idx = 0  # fallback to first column

    seen = set()
    domains: List[str] = []
    for row in rows:
        if col_idx >= len(row):
            continue
        cell_val = row[col_idx]
        if cell_val is None:
            continue
        text = str(cell_val).strip()
        m = DOMAIN_PATTERN.search(text)
        domain = m.group(0).lower() if m else text.lower()
        if domain not in seen:
            seen.add(domain)
            domains.append(domain)
    return domains


def load_cache(cache_path: Path) -> Dict[str, Dict[str, str]]:
    if not cache_path.exists():
        return {}
    import csv

    with cache_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {row["domain"]: row for row in reader if "domain" in row}


def parse_success(body: str):
    try:
        data = json.loads(body)
    except Exception:
        return None
    if not isinstance(data, dict) or data.get("code") != 1:
        return None
    return data.get("data") or {}


def call_api(domain: str, appcode: str, host: str, path: str, session: requests.Session):
    url = f"{host}{path}"
    resp = session.get(url, params={"domain": domain}, headers={"Authorization": f"APPCODE {appcode}"}, timeout=10)
    return {
        "domain": domain,
        "status_code": str(resp.status_code),
        "error_header": resp.headers.get("X-Ca-Error-Message", ""),
        "body": resp.text,
    }


def rewrite_cache(cache_path: Path, all_domains: List[str], rows_by_domain: Dict[str, Dict[str, str]]):
    import csv

    fieldnames = ["domain", "status_code", "error_header", "body"]
    with cache_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for dom in all_domains:
            row = rows_by_domain.get(dom)
            if row:
                writer.writerow(row)


def write_success(success_path: Path, rows_by_domain: Dict[str, Dict[str, str]]):
    import csv

    fieldnames = ["domain", "icp_name", "icp_num", "sitename", "service", "status"]
    parsed = []
    for row in rows_by_domain.values():
        if row.get("status_code") != "200":
            continue
        data = parse_success(row.get("body", ""))
            
        if not data:
            continue
        parsed.append({
            "domain": data.get("domain", ""),
            "icp_name": data.get("icp_name", ""),
            "icp_num": data.get("icp_num", ""),
            "sitename": data.get("sitename", ""),
            "service": data.get("service", ""),
            "status": data.get("status", ""),
        })

    with success_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(parsed)


def update_workbook(workbook_path: Path, success_rows: Dict[str, Tuple[str, str]], link_header: str = "链接"):
    wb = openpyxl.load_workbook(workbook_path)
    ws = wb.active

    max_col = ws.max_column
    subject_col = max_col + 1
    num_col = max_col + 2
    ws.cell(row=1, column=subject_col, value="备案主体")
    ws.cell(row=1, column=num_col, value="备案号")

    # locate column index again
    header_row = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1))]
    col_idx = None
    for idx, val in enumerate(header_row):
        if val == link_header:
            col_idx = idx
            break
    if col_idx is None:
        col_idx = 0

    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        cell_val = row[col_idx].value
        if cell_val is None:
            continue
        text = str(cell_val).strip()
        m = DOMAIN_PATTERN.search(text)
        domain = m.group(0).lower() if m else text.lower()
        info = success_rows.get(domain)
        if not info:
            continue
        ws.cell(row=row[0].row, column=subject_col, value=info[0])
        ws.cell(row=row[0].row, column=num_col, value=info[1])

    wb.save(workbook_path)


def main():
    parser = argparse.ArgumentParser(description="Batch ICP query with cache-first strategy")
    parser.add_argument("--workbook", default="domains.xlsx", help="Workbook to process")
    parser.add_argument("--cache", default="icp_results.csv", help="Cache file path")
    parser.add_argument("--success", default="icp_success.csv", help="Parsed success output")
    parser.add_argument("--host", default="https://domainicp.market.alicloudapi.com", help="API host")
    parser.add_argument("--path", default="/do", help="API path")
    parser.add_argument("--appcode", default=os.getenv("APP_CODE"), help="AppCode (or set APP_CODE env)")
    parser.add_argument("--sleep", type=float, default=0.1, help="Sleep between API calls (seconds)")
    args = parser.parse_args()

    if not args.appcode:
        sys.exit("APP_CODE not provided. Set env APP_CODE or --appcode")

    workbook_path = Path(args.workbook)
    cache_path = Path(args.cache)
    success_path = Path(args.success)

    domains = extract_domains(workbook_path)
    print(f"domains extracted: {len(domains)}")

    cache = load_cache(cache_path)

    to_call = []
    for dom in domains:
        row = cache.get(dom)
        if not row:
            to_call.append(dom)
            continue
        if row.get("status_code") != "200":
            to_call.append(dom)
            continue
        if not parse_success(row.get("body", "")):
            to_call.append(dom)

    print(f"need api calls: {len(to_call)}")

    sess = requests.Session()
    for dom in to_call:
        try:
            cache[dom] = call_api(dom, args.appcode, args.host, args.path, sess)
        except Exception as e:
            cache[dom] = {
                "domain": dom,
                "status_code": "-1",
                "error_header": type(e).__name__,
                "body": str(e),
            }
        time.sleep(args.sleep)

    # rewrite cache in domain order
    rewrite_cache(cache_path, domains, cache)

    # build success map
    success_map: Dict[str, Tuple[str, str]] = {}
    for dom, row in cache.items():
        if row.get("status_code") != "200":
            continue
        data = parse_success(row.get("body", ""))
        if not data:
            continue
        success_map[dom] = (data.get("icp_name", ""), data.get("icp_num", ""))

    # write success csv
    write_success(success_path, cache)

    # update workbook columns
    update_workbook(workbook_path, success_map)

    print(f"done. cache={cache_path} success={success_path} workbook updated={workbook_path}")


if __name__ == "__main__":
    main()
