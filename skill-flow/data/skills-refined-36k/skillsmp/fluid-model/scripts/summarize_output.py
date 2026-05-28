from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Optional, Tuple, List

from utils import compute_context, load_json


def _count_csv_rows_cols(csv_path: Path, max_bytes: int = 200_000_000) -> Tuple[Optional[int], Optional[int]]:
    size = csv_path.stat().st_size
    cols = None
    rows = None
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header:
            cols = len(header)
        if size <= max_bytes:
            rows = sum(1 for _ in reader)
    return rows, cols


def human_size(n: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    x = float(n)
    for u in units:
        if x < 1024 or u == units[-1]:
            return f"{x:.2f}{u}"
        x /= 1024
    return f"{x:.2f}GB"


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize prediction output directory based on plan.json")
    parser.add_argument("--plan", required=True, help="Path to plan.json")
    parser.add_argument("--max-files", type=int, default=2000, help="Max files to list (default 2000)")
    args = parser.parse_args()

    plan_path = Path(args.plan).expanduser().resolve()
    plan = load_json(plan_path)
    ctx = compute_context(plan, plan_path)

    out_dir = ctx.output_dir
    if not out_dir.exists():
        raise FileNotFoundError(f"Output directory not found: {out_dir}")

    files = [p for p in out_dir.rglob("*") if p.is_file()]
    files = sorted(files, key=lambda p: str(p))
    if len(files) > args.max_files:
        files = files[: args.max_files]

    lines: List[str] = []
    lines.append("# 预测输出汇总\n")
    lines.append(f"- run_tag: `{ctx.run_tag}`")
    lines.append(f"- sample_id: `{ctx.sample_id}`")
    lines.append(f"- sample_dir: `{ctx.sample_dir}`")
    lines.append(f"- output_dir: `{out_dir}`")
    lines.append("")

    lines.append("## 文件清单（部分）\n")
    lines.append("| 相对路径 | 大小 | 行数(可选) | 列数(可选) |")
    lines.append("|---|---:|---:|---:|")

    for p in files:
        rel = p.relative_to(out_dir)
        size = human_size(p.stat().st_size)
        rows = cols = None
        if p.suffix.lower() == ".csv":
            rows, cols = _count_csv_rows_cols(p)
        lines.append(f"| `{rel}` | {size} | {rows if rows is not None else ''} | {cols if cols is not None else ''} |")

    ctx.summary_md.parent.mkdir(parents=True, exist_ok=True)
    ctx.summary_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote summary: {ctx.summary_md}")


if __name__ == "__main__":
    main()
