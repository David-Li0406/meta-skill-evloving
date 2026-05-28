from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple, List, Set


def parse_time(time_str: str) -> datetime:
    time_str = (time_str or "").strip()
    if not time_str:
        raise ValueError("Empty time string")
    # 常见格式
    for fmt in [
        "%Y/%m/%d %H:%M",
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S.%f",
    ]:
        try:
            return datetime.strptime(time_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse time: {time_str}")


def _find_col_index(header: List[str], target: str) -> int:
    for i, h in enumerate(header):
        if h == target:
            return i
    raise ValueError(f"Column not found: {target}")


def _find_time_index(header: List[str], time_col: str = "TIME") -> int:
    for i, h in enumerate(header):
        if h.strip().lower() == time_col.strip().lower():
            return i
    raise ValueError(f"{time_col} column not found")


def modify_csv_inplace(
    csv_path: Path,
    column: str,
    value: str,
    *,
    time_col: str = "TIME",
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    match_time: Optional[List[str]] = None,
    row_index: Optional[List[int]] = None,
) -> Tuple[int, List[str]]:
    """
    修改 CSV 某列的值（就地修改）。

    选择规则（优先级从高到低）：
    1) row_index：按数据行序号（1=第一行数据，不含表头）
    2) match_time：按 TIME 精确匹配（需要 TIME 列）
    3) start_time/end_time：按 TIME 范围（需要 TIME 列）
    4) 默认：整列全改（所有数据行）

    返回：
      (rows_modified, old_values_preview[最多5个])
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    start_dt = parse_time(start_time) if start_time else None
    end_dt = parse_time(end_time) if end_time else None

    target_times: Optional[Set[datetime]] = None
    if match_time:
        target_times = set(parse_time(t) for t in match_time if str(t).strip())

    target_rows: Optional[Set[int]] = None
    if row_index:
        target_rows = set(int(x) for x in row_index)

    tmp_path = csv_path.with_suffix(csv_path.suffix + ".tmp")

    old_preview: List[str] = []
    modified = 0

    with csv_path.open("r", encoding="utf-8-sig", newline="") as src, tmp_path.open(
        "w", encoding="utf-8", newline=""
    ) as dst:
        reader = csv.reader(src)
        writer = csv.writer(dst)

        header = next(reader, None)
        if not header:
            raise ValueError(f"Empty header: {csv_path}")

        col_idx = _find_col_index(header, column)

        time_idx = None
        if target_times is not None or start_dt is not None or end_dt is not None:
            time_idx = _find_time_index(header, time_col=time_col)

        writer.writerow(header)

        data_row_idx = 0  # 1-based for data rows
        for row in reader:
            data_row_idx += 1

            # Pad/trim
            if len(row) < len(header):
                row = row + [""] * (len(header) - len(row))
            elif len(row) > len(header):
                row = row[: len(header)]

            apply = True

            if target_rows is not None:
                apply = data_row_idx in target_rows
            elif target_times is not None:
                t = parse_time(row[time_idx].strip())
                apply = t in target_times
            elif time_idx is not None:
                t = parse_time(row[time_idx].strip())
                if start_dt and t < start_dt:
                    apply = False
                if end_dt and t > end_dt:
                    apply = False

            if apply:
                if len(old_preview) < 5:
                    old_preview.append(row[col_idx])
                row[col_idx] = str(value)
                modified += 1

            writer.writerow(row)

    tmp_path.replace(csv_path)
    return modified, old_preview
