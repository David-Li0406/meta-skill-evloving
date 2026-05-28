from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import List

from utils import compute_context, load_json


def _read_csv_header(csv_path: Path) -> List[str]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
    if not header:
        raise ValueError(f"CSV 表头为空: {csv_path}")
    return header


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate plan.json for fluid-model predictions")
    parser.add_argument("--plan", required=True, help="Path to plan.json")
    args = parser.parse_args()

    plan_path = Path(args.plan).expanduser().resolve()
    if not plan_path.exists():
        raise FileNotFoundError(f"plan.json 不存在: {plan_path}")

    plan = load_json(plan_path)
    ctx = compute_context(plan, plan_path)

    if not ctx.sample_dir.is_dir():
        raise FileNotFoundError(f"算例目录不存在: {ctx.sample_dir} (sample_id={ctx.sample_id})")

    if not ctx.job_config_path.is_file():
        raise FileNotFoundError(f"job_config_path 不存在: {ctx.job_config_path}")

    payload = load_json(ctx.job_config_path)
    jobs = payload.get("jobs") if isinstance(payload, dict) else None
    if not isinstance(jobs, list) or not jobs:
        raise ValueError("job-config 缺少 jobs 列表或为空")
    if not (0 <= ctx.job_index < len(jobs)):
        raise ValueError(f"job_index={ctx.job_index} 越界，jobs 长度={len(jobs)}")

    changes = plan.get("csv_changes", []) or []
    if not isinstance(changes, list):
        raise ValueError("csv_changes 必须是数组")

    for idx, change in enumerate(changes):
        if not isinstance(change, dict):
            raise ValueError(f"csv_changes[{idx}] 必须是对象")
        rel_file = str(change.get("file") or "Boundary.csv")
        column = change.get("column")
        if not column:
            raise ValueError(f"csv_changes[{idx}] 缺少 column")

        csv_path = ctx.sample_dir / rel_file
        if not csv_path.is_file():
            raise FileNotFoundError(f"csv_changes[{idx}] 文件不存在: {csv_path}")

        header = _read_csv_header(csv_path)
        if column not in header:
            raise ValueError(f"csv_changes[{idx}] 列不存在: {column} in {csv_path}")

        if change.get("start_time") or change.get("end_time") or change.get("match_time"):
            if not any(h.strip().lower() == "time" for h in header):
                raise ValueError(f"{csv_path} 缺少 TIME 列，无法使用 start_time/end_time/match_time")

    if ctx.run_dir.exists() and any(ctx.run_dir.iterdir()):
        raise FileExistsError(f"run_dir 已存在且非空: {ctx.run_dir}. 请更换 run_tag 以保证输出到新文件夹。")

    print("OK")
    print(f"sample_id: {ctx.sample_id}")
    print(f"sample_dir: {ctx.sample_dir}")
    print(f"job_config_path: {ctx.job_config_path}")
    print(f"run_dir: {ctx.run_dir}")
    print(f"output_dir: {ctx.output_dir}")


if __name__ == "__main__":
    main()
