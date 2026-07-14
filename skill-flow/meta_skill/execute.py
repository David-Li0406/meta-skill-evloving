"""Execution eval: run SkillsBench tasks LOCALLY (Apptainer) with the refined library.

Builds a selector_cache from the refined-pool retrieval (task -> top-k refined
skill keys), points the SkillFlow Claude-Code injection agent at the refined
corpus, and runs the tasks on the local Apptainer backend (no Docker daemon, no
Daytona). The reward therefore reflects the refined library's effect, so it can
be tracked across evolving iterations. Subscription auth (no API key).
"""

from __future__ import annotations

import glob
import json
import os
import re
import subprocess
import time
from pathlib import Path

from meta_skill.data.schema import SkillPool

PROJ = Path("/home/daweili5/meta-skill-evolving/skill-flow")
VENV = "/scratch/daweili5/skill-flow-venv/bin/python"
_RL = ("You've hit your session limit", "You've hit your Sonnet limit",
       '"api_error_status":429', '"error":"rate_limit"')


def _live_oauth_token() -> str | None:
    """Refresh + read the current Claude Code OAuth token.

    The stored OAuth token expires; the CLI only refreshes it when invoked. A
    long setup phase can let it go stale (causing 401 in the agent), so we run a
    trivial `claude` call first to force a refresh, then read the fresh token.
    """
    claude = (os.environ.get("CLAUDE_CODE_EXECPATH")
              or str(Path.home() / ".local/bin/claude"))
    try:
        subprocess.run([claude, "-p", "--model", "haiku", "ok"],
                       capture_output=True, text=True, timeout=120,
                       cwd="/tmp",
                       env={k: v for k, v in os.environ.items()
                            if k not in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")})
    except Exception:  # noqa: BLE001
        pass
    cred = Path.home() / ".claude" / ".credentials.json"
    try:
        return json.loads(cred.read_text())["claudeAiOauth"]["accessToken"]
    except Exception:  # noqa: BLE001
        return None


def _env() -> dict:
    e = dict(os.environ)
    e.update({
        "APPTAINER_CACHEDIR": "/scratch/daweili5/apptainer-cache",
        "HARBOR_APPTAINER_ROOT": "/tmp/harbor-apptainer-metaskill",
        "UV_PROJECT_ENVIRONMENT": "/scratch/daweili5/skill-flow-venv",
        "UV_NO_SYNC": "1", "UV_CACHE_DIR": "/scratch/daweili5/uv-cache",
    })
    tok = _live_oauth_token()
    if tok:  # use the freshest token so long loops survive rotation
        e["CLAUDE_CODE_OAUTH_TOKEN"] = tok
    # force subscription auth for the Claude Code agent
    e.pop("ANTHROPIC_API_KEY", None)
    e.pop("ANTHROPIC_AUTH_TOKEN", None)
    return e


def run_execution_sample(
    refined: SkillPool, tasks, retrieval_per_task: dict, workdir: Path | None,
    agent: str = "claude_code", model: str = "anthropic/claude-sonnet-4-6",
    top_k: int = 5, n_concurrent: int = 2,
) -> dict:
    """Inject refined-library top-k skills and run the tasks via Apptainer."""
    if not tasks:
        return {"per_task": {}, "metrics": {}}
    workdir = Path(workdir or "/scratch/daweili5/meta_skill_smoke/exec")
    corpus_refined = workdir / "corpus_refined"  # written by manage()
    if not corpus_refined.is_dir():
        return {"per_task": {t.id: {"reward": None, "error": "no refined corpus"}
                             for t in tasks}, "metrics": {}}

    # selector_cache: task -> top-k refined skill keys (resolvable by the injector)
    refined_ids = set(refined.ids())
    selector = {t.id: [k for k in retrieval_per_task.get(t.id, {}).get("topk_keys", [])
                       if k in refined_ids][:top_k] for t in tasks}
    sel_path = workdir / "selector_cache.json"
    sel_path.write_text(json.dumps(selector, indent=2), encoding="utf-8")

    jobs_dir = workdir / "evaluation"
    jobs_dir.mkdir(parents=True, exist_ok=True)
    task_ids = [t.id for t in tasks]
    valid: dict[str, float] = {}
    big = len(task_ids) > 8
    max_windows = 30 if big else 1  # throttle only for big batches
    if big:  # finish big batches fast (before token can expire); 8 cores avail
        n_concurrent = max(n_concurrent, 8)

    # Pick up any rewards already on disk (e.g. a resumed run) so we only launch
    # the still-missing tasks.
    valid.update(_collect_valid(jobs_dir, task_ids))

    prev_done = len(valid)
    stagnant = 0
    for w in range(max_windows):
        remaining = [t for t in task_ids if t not in valid]
        if not remaining:
            break
        cfg = {
            "jobs_dir": str(jobs_dir), "model": model, "agent_backend": agent,
            "reasoning_effort": "medium", "selector_cache": str(sel_path),
            "tasks_dir_for_skills": "integration/skillsbench/tasks",
            "corpus_dir": str(corpus_refined),
            "tasks_path": "integration/skillsbench/tasks", "num_runs": 1,
            "environment": {"backend": "apptainer", "n_concurrent": n_concurrent},
            "tasks": {"include_tasks": remaining, "exclude_tasks": []},
            "retry": {"resume": False, "retry_errors": False, "retry_tasks": [],
                      "retry_error_types": ["AgentTimeoutError", "RuntimeError",
                                            "AgentSetupTimeoutError", "VerifierTimeoutError",
                                            "RewardFileNotFoundError"]},
            "job_name": "metaskill-exec",
        }
        cfg_path = workdir / "exec_benchmark.json"
        cfg_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
        log_path = workdir / f"harbor_window_{w}.log"
        try:
            proc = subprocess.run([VENV, "-m", "benchmark.scripts.cli", "run",
                                   "--config", str(cfg_path)],
                                  cwd=PROJ, env=_env(), timeout=14400,
                                  capture_output=True, text=True)
            log_path.write_text((proc.stdout or "")[-20000:] + "\n--- STDERR ---\n"
                                + (proc.stderr or "")[-20000:], encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            log_path.write_text(f"window {w} crashed: {exc}", encoding="utf-8")
        # Re-scan ALL tasks (aggregates across every window run so far).
        valid.update(_collect_valid(jobs_dir, task_ids))
        done = len(valid)
        if done >= len(task_ids):
            break
        # harbor aborts early (~26 tasks/run) AND may rate-limit; keep launching
        # the still-missing tasks while we make progress, sleeping out any cap.
        if _rate_limited(jobs_dir):
            time.sleep(_reset_seconds(jobs_dir))
            stagnant = 0
        elif done <= prev_done:
            stagnant += 1
            if stagnant >= 2:  # two windows, zero new rewards -> real infra wall
                break
        else:
            stagnant = 0
        prev_done = done

    per_task = {t: {"reward": valid.get(t), "injected_skills": selector.get(t, [])}
                for t in task_ids}
    rewards = [r for r in valid.values() if r is not None]
    return {"per_task": per_task, "selector_cache": selector,
            "metrics": {"mean_reward": sum(rewards) / len(rewards) if rewards else None,
                        "n_scored": len(rewards), "n_tasks": len(task_ids)}}


def _collect_valid(jobs_dir: Path, task_ids: list[str]) -> dict[str, float]:
    """Best non-rate-limited reward per task across all job dirs."""
    out: dict[str, float] = {}
    for job in sorted(jobs_dir.glob("metaskill-exec*")):
        for t in task_ids:
            for trial in job.glob(f"{t}__*"):
                ccs = list(trial.glob("**/claude-code.txt"))
                if ccs and any(s in ccs[0].read_text(errors="ignore") for s in _RL):
                    continue
                for rf in trial.glob("**/reward.txt"):
                    try:
                        r = float(rf.read_text().strip())
                        if t not in out or r > out[t]:
                            out[t] = r
                    except Exception:  # noqa: BLE001
                        pass
    return out


def _rate_limited(jobs_dir: Path) -> bool:
    newest = sorted(jobs_dir.glob("metaskill-exec*"))
    if not newest:
        return False
    for cc in newest[-1].glob("*__*/**/claude-code.txt"):
        if any(s in cc.read_text(errors="ignore") for s in _RL):
            return True
    return False


def _reset_seconds(jobs_dir: Path) -> int:
    import datetime as dt
    default = 5 * 3600 + 600
    txt = ""
    for job in reversed(sorted(jobs_dir.glob("metaskill-exec*"))):
        for cc in job.glob("*__*/**/claude-code.txt"):
            t = cc.read_text(errors="ignore")
            if "resets" in t and ('429' in t or "rate_limit" in t):
                txt = t
                break
        if txt:
            break
    m = re.search(r"resets (\d+)(?::(\d+))?\s*(am|pm)\s*\(UTC\)", txt)
    if not m:
        return default
    h = int(m.group(1)) % 12 + (12 if m.group(3) == "pm" else 0)
    now = dt.datetime.utcnow()
    target = now.replace(hour=h, minute=int(m.group(2) or 0), second=0, microsecond=0)
    if target <= now:
        target += dt.timedelta(days=1)
    d = int((target - now).total_seconds())
    return d + 300 if 0 < d <= 6 * 3600 else default
