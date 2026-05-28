from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set


def _read_header(path: Path) -> List[str]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
    if not header:
        raise ValueError(f"Empty header: {path}")
    return header


def _find_col_index(header: List[str], name: str) -> Optional[int]:
    for i, h in enumerate(header):
        if h == name:
            return i
    # case-insensitive TIME support could be added, but keep strict for data columns
    return None


def _find_latest_backup(after_path: Path) -> Optional[Path]:
    # Prefer explicit last_backup file if exists
    last_backup_txt = after_path.parent / f"{after_path.name}.last_backup.txt"
    if last_backup_txt.exists():
        try:
            p = Path(last_backup_txt.read_text(encoding="utf-8").strip())
            if p.exists():
                return p
        except Exception:
            pass

    # Fallback to glob
    pattern = f"{after_path.name}.before_*.csv"
    candidates = list(after_path.parent.glob(pattern))
    if not candidates:
        return None
    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0]


def _load_rows(path: Path, key_col: str = "TIME") -> Tuple[List[str], Dict[str, List[str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if not header:
            raise ValueError(f"Empty header: {path}")
        key_idx = None
        for i, h in enumerate(header):
            if h.strip().lower() == key_col.strip().lower():
                key_idx = i
                break

        rows: Dict[str, List[str]] = {}
        data_row_idx = 0
        dup_counter: Dict[str, int] = {}
        for row in reader:
            data_row_idx += 1
            # normalize length
            if len(row) < len(header):
                row = row + [""] * (len(header) - len(row))
            elif len(row) > len(header):
                row = row[: len(header)]

            if key_idx is None:
                key = str(data_row_idx)  # fallback to row number
            else:
                key_raw = row[key_idx]
                key = key_raw
                if key in rows:
                    # disambiguate duplicates
                    dup_counter[key] = dup_counter.get(key, 1) + 1
                    key = f"{key_raw}__dup{dup_counter[key]}"
            rows[key] = row
    return header, rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Diff Boundary.csv before/after (auto-find latest backup)")
    parser.add_argument("--boundary-file", required=True, help="Path to current Boundary.csv (after)")
    parser.add_argument("--before-file", default=None, help="Optional explicit before file (backup)")
    parser.add_argument("--key-col", default="TIME", help="Key column for alignment (default TIME). If missing, use row number.")
    parser.add_argument("--column", default=None, help="If provided, only diff this column")
    parser.add_argument("--max-diffs", type=int, default=200, help="Max diff rows to print/write (default 200)")
    args = parser.parse_args()

    after_path = Path(args.boundary_file).expanduser().resolve()
    if not after_path.exists():
        raise FileNotFoundError(f"boundary-file not found: {after_path}")

    if args.before_file:
        before_path = Path(args.before_file).expanduser().resolve()
    else:
        before_path = _find_latest_backup(after_path)  # may be None

    if not before_path or not before_path.exists():
        raise FileNotFoundError(
            "找不到 before 文件（备份）。请先运行 modify_boundary.py 生成备份，"
            "或用 --before-file 显式指定。"
        )

    before_header, before_rows = _load_rows(before_path, key_col=args.key_col)
    after_header, after_rows = _load_rows(after_path, key_col=args.key_col)

    if before_header != after_header:
        # still allow but warn; align by name intersection
        pass

    # Determine columns to compare
    if args.column:
        cols = [args.column]
    else:
        # compare all columns (excluding key-col if present)
        cols = [c for c in after_header if c.strip().lower() != args.key_col.strip().lower()]

    # Build col index maps
    b_idx = {c: _find_col_index(before_header, c) for c in cols}
    a_idx = {c: _find_col_index(after_header, c) for c in cols}
    for c in cols:
        if b_idx[c] is None or a_idx[c] is None:
            raise ValueError(f"Column not found in both files: {c}")

    before_keys = set(before_rows.keys())
    after_keys = set(after_rows.keys())

    added = sorted(list(after_keys - before_keys))
    removed = sorted(list(before_keys - after_keys))
    common = sorted(list(before_keys & after_keys))

    diffs: List[Tuple[str, str, str, str]] = []
    changed_keys: Set[str] = set()

    for key in common:
        b_row = before_rows[key]
        a_row = after_rows[key]
        for c in cols:
            bi = b_idx[c]
            ai = a_idx[c]
            b_val = b_row[bi] if bi is not None else ""
            a_val = a_row[ai] if ai is not None else ""
            if b_val != a_val:
                diffs.append((key, c, b_val, a_val))
                changed_keys.add(key)

    # Write report files next to after_path
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    md_path = after_path.parent / f"diff_Boundary_{ts}.md"
    csv_path = after_path.parent / f"diff_Boundary_{ts}.csv"

    # Markdown report
    lines: List[str] = []
    lines.append("# Boundary.csv 差异报告\n")
    lines.append(f"- before: `{before_path}`")
    lines.append(f"- after:  `{after_path}`")
    lines.append(f"- key_col: `{args.key_col}`")
    lines.append(f"- columns: `{', '.join(cols)}`")
    lines.append("")
    lines.append("## 统计\n")
    lines.append(f"- common_rows: {len(common)}")
    lines.append(f"- changed_rows: {len(changed_keys)}")
    lines.append(f"- changed_cells: {len(diffs)}")
    lines.append(f"- added_rows: {len(added)}")
    lines.append(f"- removed_rows: {len(removed)}")
    lines.append("")

    show_diffs = diffs[: args.max_diffs]
    lines.append(f"## 变更明细（最多 {args.max_diffs} 条）\n")
    lines.append("| key | column | before | after |")
    lines.append("|---|---|---|---|")
    for key, col, b, a in show_diffs:
        # escape pipes minimally
        b2 = b.replace("|", "\\|")
        a2 = a.replace("|", "\\|")
        lines.append(f"| `{key}` | `{col}` | `{b2}` | `{a2}` |")

    md_path.write_text("\n".join(lines), encoding="utf-8")

    # CSV diff
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["key", "column", "before", "after"])
        for row in show_diffs:
            w.writerow(list(row))

    print("OK")
    print(f"before: {before_path}")
    print(f"after:  {after_path}")
    print(f"changed_rows: {len(changed_keys)}")
    print(f"changed_cells: {len(diffs)}")
    print(f"report_md: {md_path}")
    print(f"report_csv: {csv_path}")

    # Also print first few diffs to console
    for key, col, b, a in show_diffs[:20]:
        print(f"DIFF key={key} col={col}: {b} -> {a}")


if __name__ == "__main__":
    main()
