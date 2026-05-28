from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from modify_csv import modify_csv_inplace


def make_backup(src: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = src.with_name(f"{src.name}.before_{ts}.csv")
    shutil.copy2(src, backup)
    # 记录最新备份，方便 diff 脚本定位
    (src.parent / f"{src.name}.last_backup.txt").write_text(str(backup), encoding="utf-8")
    return backup


def parse_multi_arg(value: Optional[str]) -> Optional[List[str]]:
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    # 允许逗号分隔
    parts = [p.strip() for p in value.split(",") if p.strip()]
    return parts or None


def parse_int_list(value: Optional[str]) -> Optional[List[int]]:
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    parts = [p.strip() for p in value.split(",") if p.strip()]
    out: List[int] = []
    for p in parts:
        out.append(int(p))
    return out or None


def main() -> None:
    parser = argparse.ArgumentParser(description="Modify Boundary.csv column values (Windows-friendly)")
    parser.add_argument("--boundary-file", required=True, help="Path to Boundary.csv (relative or absolute)")
    parser.add_argument("--column", required=True, help="Target column name, e.g. T_001:SNQ")
    parser.add_argument("--value", required=True, help="New value (number or string)")
    parser.add_argument("--time-col", default="TIME", help="Time column name (default TIME)")
    parser.add_argument("--start-time", default=None, help="Start time (optional, requires TIME column)")
    parser.add_argument("--end-time", default=None, help="End time (optional, requires TIME column)")
    parser.add_argument("--match-time", default=None, help="Exact TIME values to modify (comma-separated), requires TIME column")
    parser.add_argument("--row-index", default=None, help="Data row indexes to modify (1=first data row, comma-separated)")

    args = parser.parse_args()

    boundary_path = Path(args.boundary_file).expanduser().resolve()
    if not boundary_path.exists():
        raise FileNotFoundError(f"Boundary file not found: {boundary_path}")

    backup = make_backup(boundary_path)

    match_time = parse_multi_arg(args.match_time)
    row_index = parse_int_list(args.row_index)

    modified, preview = modify_csv_inplace(
        csv_path=boundary_path,
        column=args.column,
        value=str(args.value),
        time_col=args.time_col,
        start_time=args.start_time,
        end_time=args.end_time,
        match_time=match_time,
        row_index=row_index,
    )

    print("OK")
    print(f"boundary_file: {boundary_path}")
    print(f"backup_file:   {backup}")
    print(f"column:        {args.column}")
    print(f"value:         {args.value}")
    if row_index:
        print(f"row_index:     {row_index}")
    if match_time:
        print(f"match_time:    {match_time}")
    if args.start_time or args.end_time:
        print(f"time_range:    {args.start_time or ''} ~ {args.end_time or ''}")
    print(f"rows_modified: {modified}")
    print(f"old_preview:   {preview}")


if __name__ == "__main__":
    main()
