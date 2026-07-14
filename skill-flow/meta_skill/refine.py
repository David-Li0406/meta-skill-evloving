"""Refiner meta-agent: Claude Code reads the trajectories and rewrites the meta-skill.

Mirrors the meta-harness "automated harness evolution" step: feed the current
meta-skill SKILL.md plus the management decision log, evaluation report,
credit-assignment attribution, and metric history to Claude Code (Opus,
subscription auth), and have it return a full revised SKILL.md.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

from meta_skill.metaskill import MetaSkill, parse_meta_skill

_SKILL_BLOCK = re.compile(r"```(?:skill-?md|markdown)?\s*\n(?P<body>.*?)\n```", re.DOTALL)


def _build_prompt(meta: MetaSkill, decision_log: dict, eval_report: dict,
                  attribution: dict, history: list[dict]) -> str:
    retr = eval_report.get("retrieval", {}).get("metrics", {})
    execm = eval_report.get("execution", {}).get("metrics", {})
    # Compact, bounded per-task attribution (the full decision log can be ~30K
    # entries — too large for the CLI). Keep one short line per failed task.
    compact = []
    for r in attribution.get("records", []):
        if not r.get("task_failed"):
            continue
        miss = [g for g in r.get("gt_attribution", []) if not g.get("found")]
        compact.append({
            "task": r.get("task"), "reward": r.get("reward"),
            "recall": r.get("retrieval_recall"),
            "lost_gt": [{"gt": g.get("gt"), "blamed": g.get("blamed_stage"),
                         "why": g.get("explanation", "")[:80]} for g in miss[:3]],
        })
    compact = compact[:12]
    return f"""You are evolving a **meta-skill**: a SKILL.md that defines a method for \
MANAGING a large agent skill library (clustering near-duplicates, LLM-merging \
clusters, LLM-quality-filtering). The goal of the library is to make the RIGHT \
skill findable for each downstream task. Your job: rewrite the SKILL.md so the \
next run improves the metrics — chiefly keeping ground-truth skills retrievable.

## Current meta-skill (SKILL.md)
```skill-md
{meta.raw}
```

## This iteration's results
Retrieval metrics: {json.dumps(retr)}
Execution (SkillsBench reward): {json.dumps(execm)}
Decision-log summary: {json.dumps(decision_log.get("summary", {}))}
Credit assignment (which pipeline stage caused failures):
{json.dumps(attribution.get("stage_blame", {}))} blamed; {json.dumps(attribution.get("stage_credit", {}))} credited.
Top blamed stage: {attribution.get("summary", {}).get("top_blamed_stage")}

## Failed tasks (compact: which GT skill was lost and why)
{json.dumps(compact, indent=1)}

## Metric history (oldest→newest)
{json.dumps(history)}

## Instructions
Analyze WHY ground-truth skills were lost (dropped by the filter? merged into a \
vague skill? kept but not retrieved?). Then rewrite the ENTIRE SKILL.md to fix \
the dominant failure mode. You may change: the `params` (e.g. `eps`, \
`max_group_size`, filter strictness), the playbook prose, and the embedded \
`merge`/`filter` PROMPT blocks (keep the `<!-- PROMPT: name -->` / \
`<!-- END PROMPT: name -->` fences and any `{{{{ jinja }}}}` variables intact). \
Keep the same YAML frontmatter keys.

Return ONLY the new SKILL.md inside one ```skill-md fenced block. No other text."""


def _call_claude(prompt: str, model: str = "opus", timeout: int = 600) -> str:
    import shutil

    env = dict(os.environ)
    env.pop("ANTHROPIC_API_KEY", None)  # force subscription auth
    env.pop("ANTHROPIC_AUTH_TOKEN", None)
    # `claude` is often a shell function; resolve the real binary for subprocess.
    claude = (env.get("CLAUDE_CODE_EXECPATH")
              or shutil.which("claude")
              or str(Path.home() / ".local/bin/claude"))
    with tempfile.TemporaryDirectory() as cwd:  # clean cwd: no CLAUDE.md pickup
        proc = subprocess.run(
            [claude, "-p", "--model", model, "--permission-mode", "bypassPermissions"],
            input=prompt, capture_output=True, text=True, env=env, cwd=cwd,
            timeout=timeout,
        )
    if proc.returncode != 0:
        raise RuntimeError(f"claude CLI failed ({proc.returncode}): {proc.stderr[:500]}")
    return proc.stdout


def _extract_skill_md(text: str) -> str:
    m = _SKILL_BLOCK.search(text)
    body = m.group("body") if m else text
    body = body.strip()
    if not body.startswith("---"):
        raise ValueError("refiner output is not a valid SKILL.md (no frontmatter)")
    return body


def refine(meta: MetaSkill, decision_log: dict, eval_report: dict,
           attribution: dict, history: list[dict], out_path: Path,
           model: str = "opus") -> MetaSkill:
    """Invoke Claude Code to produce the next meta-skill; write + return it."""
    prompt = _build_prompt(meta, decision_log, eval_report, attribution, history)
    if len(prompt) > 60000:  # hard safety cap for the CLI
        prompt = prompt[:60000] + "\n\n[truncated]\n\nReturn ONLY the new SKILL.md in one ```skill-md block."
    raw = _call_claude(prompt, model=model)
    skill_md = _extract_skill_md(raw)
    new_meta = parse_meta_skill(skill_md)  # validates it round-trips
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(skill_md, encoding="utf-8")
    return new_meta
