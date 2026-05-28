from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


SAMPLE_MIN = 1
SAMPLE_MAX = 264


def normalize_sample_id(sample_id: Any) -> str:
    """
    规则：
    - 允许 001–264
    - 用户没说 / 非数字 / 越界 => 默认 '001'
    """
    if sample_id is None:
        return "001"
    try:
        n = int(str(sample_id).strip())
    except Exception:
        return "001"
    if n < SAMPLE_MIN or n > SAMPLE_MAX:
        return "001"
    return f"{n:03d}"


_RUN_TAG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


def ensure_run_tag(tag: str) -> str:
    tag = (tag or "").strip()
    if not tag:
        raise ValueError("plan.json 缺少 run_tag，且 run_tag 不能为空")
    if not _RUN_TAG_RE.fullmatch(tag):
        raise ValueError("run_tag 只能包含字母/数字/点/下划线/连字符，且必须以字母或数字开头。")
    return tag


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@dataclass(frozen=True)
class PlanContext:
    plan_path: Path
    project_root: Path
    sample_id: str
    sample_dir: Path
    job_config_path: Path
    job_index: int
    run_tag: str
    run_dir: Path
    output_basename: str
    output_dir: Path
    summary_md: Path


def compute_context(plan: Dict[str, Any], plan_path: Path) -> PlanContext:
    project_root_raw = plan.get("project_root")
    if not project_root_raw:
        raise ValueError("plan.json 缺少 project_root（项目根目录绝对路径）")
    project_root = Path(str(project_root_raw)).expanduser().resolve()

    sample_id = normalize_sample_id(plan.get("sample_id"))

    # 默认算例目录约定
    sample_dir_override = plan.get("sample_dir_override")
    if sample_dir_override:
        sample_dir = Path(str(sample_dir_override)).expanduser().resolve()
    else:
        sample_dir = project_root / "data" / "dataset" / "mock_test" / f"第{sample_id}个算例"

    job_config_raw = plan.get("job_config_path") or (
        project_root / "real_predict" / "examples" / "batch_jobs_full_value_projection_small.json"
    )
    job_config_path = Path(str(job_config_raw)).expanduser().resolve()

    job_index = int(plan.get("job_index", 0))
    run_tag = ensure_run_tag(plan.get("run_tag"))
    run_dir = project_root / "real_predict" / "examples" / "_runs" / run_tag

    output_basename = "prediction_output"
    if job_config_path.exists():
        payload = load_json(job_config_path)
        jobs = payload.get("jobs") if isinstance(payload, dict) else None
        if isinstance(jobs, list) and 0 <= job_index < len(jobs):
            out_val = jobs[job_index].get("output")
            if isinstance(out_val, str) and out_val.strip():
                output_basename = Path(out_val.strip()).name or output_basename

    output_dir = run_dir / output_basename
    summary_md = run_dir / "summary.md"

    return PlanContext(
        plan_path=plan_path,
        project_root=project_root,
        sample_id=sample_id,
        sample_dir=sample_dir,
        job_config_path=job_config_path,
        job_index=job_index,
        run_tag=run_tag,
        run_dir=run_dir,
        output_basename=output_basename,
        output_dir=output_dir,
        summary_md=summary_md,
    )
