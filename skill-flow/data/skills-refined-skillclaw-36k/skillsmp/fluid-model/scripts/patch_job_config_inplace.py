from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from utils import compute_context, dump_json, load_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Patch batch job-config IN PLACE based on plan.json")
    parser.add_argument("--plan", required=True, help="Path to plan.json")
    args = parser.parse_args()

    plan_path = Path(args.plan).expanduser().resolve()
    plan = load_json(plan_path)
    ctx = compute_context(plan, plan_path)

    payload = load_json(ctx.job_config_path)
    if not isinstance(payload, dict):
        raise ValueError("job-config 必须是 JSON object（包含 defaults / jobs）")

    jobs = payload.get("jobs")
    if not isinstance(jobs, list) or not jobs:
        raise ValueError("job-config 缺少 jobs 列表或为空")
    if not (0 <= ctx.job_index < len(jobs)):
        raise ValueError(f"job_index 越界: {ctx.job_index} (jobs={len(jobs)})")

    job = jobs[ctx.job_index]
    if not isinstance(job, dict):
        raise ValueError(f"jobs[{ctx.job_index}] 不是对象")

    # Create run dir + output dir (must be new folder)
    ctx.run_dir.mkdir(parents=True, exist_ok=True)
    ctx.output_dir.mkdir(parents=True, exist_ok=True)

    # Backup current job-config for traceability
    backup_path = ctx.run_dir / "job_config_backup.json"
    shutil.copy2(ctx.job_config_path, backup_path)

    # Patch sample_dir/output to ABSOLUTE paths
    job["sample_dir"] = str(ctx.sample_dir)
    job["output"] = str(ctx.output_dir)

    # Patch name for traceability
    base_name = str(job.get("name") or f"job_{ctx.job_index}")
    job["name"] = f"{base_name}_第{ctx.sample_id}个算例_{ctx.run_tag}"

    # Apply overrides to defaults
    overrides = plan.get("overrides", {}) or {}
    if overrides:
        defaults = payload.get("defaults")
        if not isinstance(defaults, dict):
            defaults = {}
            payload["defaults"] = defaults
        for k, v in overrides.items():
            defaults[k] = v

    # Write back IN PLACE (atomic via temp)
    tmp_path = ctx.job_config_path.with_suffix(ctx.job_config_path.suffix + ".tmp")
    dump_json(tmp_path, payload)
    tmp_path.replace(ctx.job_config_path)

    patched_copy = ctx.run_dir / "job_config_patched.json"
    shutil.copy2(ctx.job_config_path, patched_copy)
    plan_copy = ctx.run_dir / "plan.json"
    shutil.copy2(plan_path, plan_copy)

    print("OK")
    print(f"Patched job-config: {ctx.job_config_path}")
    print(f"Backup saved:       {backup_path}")
    print(f"Patched copy:       {patched_copy}")
    print(f"Output dir:         {ctx.output_dir}")


if __name__ == "__main__":
    main()
