#!/usr/bin/env python3
"""
Pairwise Comparative Evaluation — compare outputs from two benchmark runs.

Sends task prompt + artifacts from both runs to an LLM judge, which decides
which run produced the better result for each task.

Usage:
    # Compare two runs (all shared tasks)
    python -m benchmark.AgentSkillOS_bench.ranking.compare --run-a results/run_A --run-b results/run_B

    # Compare a specific task
    python -m benchmark.AgentSkillOS_bench.ranking.compare --run-a results/run_A --run-b results/run_B --task creative_design_task1

    # Compare a category
    python -m benchmark.AgentSkillOS_bench.ranking.compare --run-a results/run_A --run-b results/run_B --category creative_design

    # Save results
    python -m benchmark.AgentSkillOS_bench.ranking.compare --run-a results/run_A --run-b results/run_B --output comparison.json
"""
import argparse
import asyncio
import gc
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import uuid4

from .checkpoint import CheckpointStore
from ..utils.file_converters import render_to_images, get_video_metadata_summary, get_file_metadata_summary, RENDERS_DIR_NAME, resize_safe_image
from ..utils.llm_clients import query_claude_code

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# File extensions considered as evaluable artifacts
_VISUAL_EXTENSIONS = {".pdf", ".pptx", ".docx", ".html", ".htm"}
_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}
_VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".webm"}
_TEXT_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".c", ".cpp", ".h",
    ".css", ".scss", ".json", ".csv", ".xml", ".yaml", ".yml", ".toml",
    ".md", ".txt", ".sh", ".bash", ".sql", ".r", ".go", ".rs", ".rb",
    ".php", ".swift", ".kt", ".scala", ".lua", ".pl", ".ex", ".exs",
    ".svelte", ".vue",
}
MAX_TEXT_CHARS = 5000
MAX_IMAGES_PER_SIDE = 30

COMPARE_SYSTEM_PROMPT = """\
You are an impartial evaluation expert. You will receive a task description and the output artifacts from two different systems (A and B).
Compare them holistically across dimensions you consider important — such as quality, completeness, correctness, and aesthetics — and decide which one is better.

## Output Format
Output ONLY a single JSON object. No other text, no markdown.
{"preference": "A", "reason": "Brief justification"}

The value of preference must be "A", "B", or "tie"."""


# ---------------------------------------------------------------------------
# Task discovery helpers
# ---------------------------------------------------------------------------

def _build_task_id_map(run_dir: Path, tasks_dir: Path) -> Dict[str, Path]:
    """Build a mapping from task_id to actual task directory.

    Supports both plain ``{task_id}/workspace`` and timestamped
    ``{timestamp}-{mode}-{task_id}-{hash}/workspace`` layouts.
    """
    known_task_ids = sorted(
        [p.stem for p in tasks_dir.glob("*.json")],
        key=lambda x: -len(x),
    )
    mapping: Dict[str, Path] = {}
    for p in run_dir.iterdir():
        if not p.is_dir() or not (p / "workspace").is_dir():
            continue
        dir_name = p.name
        # Direct match
        if (tasks_dir / f"{dir_name}.json").exists():
            mapping[dir_name] = p
            continue
        # Substring match against known task_ids (longest first)
        for tid in known_task_ids:
            if tid in dir_name:
                mapping[tid] = p
                break
    return mapping


def discover_shared_tasks(
    run_a: Path,
    run_b: Path,
    tasks_dir: Path,
    task_id: Optional[str] = None,
    category: Optional[str] = None,
) -> Tuple[List[str], Dict[str, Path], Dict[str, Path]]:
    """Find task IDs present in both runs, optionally filtered.

    Returns (shared_task_ids, map_a, map_b) where the maps go from
    task_id to the actual directory path in each run.
    """
    map_a = _build_task_id_map(run_a, tasks_dir)
    map_b = _build_task_id_map(run_b, tasks_dir)
    shared = sorted(set(map_a) & set(map_b))

    if task_id:
        shared = [t for t in shared if t == task_id]

    # Only keep tasks that have a config file
    shared = [t for t in shared if (tasks_dir / f"{t}.json").exists()]

    # Prefer matching JSON category field; if no tasks match, fall back to
    # task_id prefix matching (legacy behavior).
    if category:
        json_matched: List[str] = []
        prefix_matched: List[str] = []
        for t in shared:
            if t.startswith(category + "_"):
                prefix_matched.append(t)
            try:
                with open(tasks_dir / f"{t}.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                continue
            if data.get("category") == category:
                json_matched.append(t)
        shared = sorted(json_matched) if json_matched else sorted(prefix_matched)

    return shared, map_a, map_b


def load_task_prompt(tasks_dir: Path, task_id: str) -> str:
    """Load the task prompt from the task config JSON."""
    config_path = tasks_dir / f"{task_id}.json"
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("prompt", "")


def collect_evaluator_paths(tasks_dir: Path, task_id: str, workspace: Optional[Path] = None) -> Set[str]:
    """Extract all file paths referenced in evaluators' op_args.

    Handles both ``op_args.path`` (file_exists, file_content_check, etc.) and
    ``op_args.directory`` + ``op_args.pattern`` (files_match_pattern).  For the
    latter, *workspace* must be provided so that the directory can be listed and
    filenames matched against the regex pattern.
    """
    config_path = tasks_dir / f"{task_id}.json"
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    paths: Set[str] = set()
    for ev in data.get("evaluators", []):
        op_args = ev.get("op_args", {})

        # --- path-based evaluators (file_exists, file_content_check, ...) ---
        path_val = op_args.get("path")
        if path_val is not None:
            if isinstance(path_val, str):
                paths.add(path_val)
            elif isinstance(path_val, list):
                for p in path_val:
                    if isinstance(p, str):
                        paths.add(p)

        # --- files_match_pattern evaluator ---
        if ev.get("op_func") == "files_match_pattern" and workspace is not None:
            directory = op_args.get("directory", ".")
            pattern = op_args.get("pattern")
            if pattern:
                dir_path = workspace / directory
                if dir_path.is_dir():
                    regex = re.compile(pattern)
                    for f in sorted(dir_path.iterdir()):
                        if f.is_file() and regex.match(f.name):
                            # Store as relative path from workspace
                            rel = str(f.relative_to(workspace))
                            paths.add(rel)

    return paths


# ---------------------------------------------------------------------------
# Artifact discovery and rendering
# ---------------------------------------------------------------------------

def discover_artifacts(workspace: Path, evaluator_paths: Set[str]) -> List[Path]:
    """Discover task deliverable files in a workspace.

    Only includes files referenced by evaluators (via ``evaluator_paths``).
    When an evaluator-referenced file is not at its expected relative path,
    a recursive search of the workspace is used as a fallback.
    """
    found: Dict[str, Path] = {}

    for rel_path in evaluator_paths:
        full = workspace / rel_path
        if full.exists() and full.is_file():
            found[str(full)] = full
        else:
            # Try recursive search by filename
            candidates = list(workspace.rglob(Path(rel_path).name))
            for c in sorted(candidates, key=lambda p: len(p.parts)):
                if c.is_file():
                    found[str(c)] = c
                    break

    return list(found.values())


async def prerender_artifacts(artifacts: List[Path], render_dir: Optional[Path] = None) -> List[Path]:
    """Render visual artifacts (PDF/PPTX/DOCX/HTML/Video) to images.

    Args:
        artifacts: List of artifact file paths to render.
        render_dir: Isolated directory for rendered output.  When ``None``,
                    renders are placed next to the original artifacts (legacy
                    behavior).

    Returns the list of rendered image paths.
    """
    rendered: List[Path] = []
    for artifact in artifacts:
        suffix = artifact.suffix.lower()
        if suffix in (_VISUAL_EXTENSIONS | _VIDEO_EXTENSIONS):
            images = await render_to_images(artifact, out_dir=render_dir)
            rendered.extend(images)
        elif suffix in _IMAGE_EXTENSIONS:
            safe = resize_safe_image(
                artifact,
                out_dir=render_dir or (artifact.parent / RENDERS_DIR_NAME),
            )
            if safe is not None:
                rendered.append(safe)
    return rendered


# ---------------------------------------------------------------------------
# Prompt building
# ---------------------------------------------------------------------------

def _read_text_truncated(path: Path) -> Optional[str]:
    """Read a text file, truncated to MAX_TEXT_CHARS."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        if len(text) > MAX_TEXT_CHARS:
            text = text[:MAX_TEXT_CHARS] + f"\n... [truncated, {len(text)} chars total]"
        return text
    except Exception:
        return None


def build_compare_prompt(
    task_prompt: str,
    artifacts_a: List[Path],
    artifacts_b: List[Path],
    images_a: List[Path],
    images_b: List[Path],
) -> str:
    """Build the comparison prompt for the LLM judge.

    For claude_code backend: image paths are listed as absolute paths for the
    agent to read; text files are embedded inline.
    """
    parts: List[str] = []

    parts.append("## Task Description\n")
    parts.append(task_prompt)
    parts.append("")

    # --- System A ---
    parts.append("## System A Output\n")
    _append_side_artifacts(parts, "A", artifacts_a, images_a)

    # --- System B ---
    parts.append("## System B Output\n")
    _append_side_artifacts(parts, "B", artifacts_b, images_b)

    parts.append("## Evaluation Instructions\n")
    parts.append(
        "Carefully read all files listed above (use the Read tool to read images and text files), "
        "then holistically compare the output quality of A and B.\n"
        "Output ONLY a single JSON: {\"preference\": \"A\" or \"B\" or \"tie\", \"reason\": \"Brief justification\"}"
    )

    return "\n".join(parts)


def _append_side_artifacts(
    parts: List[str],
    label: str,
    artifacts: List[Path],
    images: List[Path],
) -> None:
    """Append artifact descriptions for one side to the prompt parts list."""
    if not artifacts and not images:
        parts.append(f"(System {label} produced no output files)\n")
        return

    # File metadata (video resolution/duration, image size, PDF pages, etc.)
    # Placed before screenshots so the judge has context while reviewing visuals.
    file_metadata: Optional[str] = None
    for artifact in artifacts:
        suffix = artifact.suffix.lower()
        if suffix in _VIDEO_EXTENSIONS:
            metadata = get_video_metadata_summary(artifact)
            if metadata:
                file_metadata = (file_metadata or "") + metadata + "\n"
        if suffix in _IMAGE_EXTENSIONS | _VISUAL_EXTENSIONS:
            metadata = get_file_metadata_summary(artifact)
            if metadata:
                file_metadata = (file_metadata or "") + metadata + "\n"
    if file_metadata:
        parts.append(f"### {label} File Metadata:")
        parts.append(file_metadata)
        parts.append("")

    # Images (rendered screenshots + native images)
    capped_images = images[:MAX_IMAGES_PER_SIDE]
    if capped_images:
        parts.append(f"### {label} Visual Screenshots (read each one):")
        for img in capped_images:
            parts.append(f"  - {img}")
        if len(images) > MAX_IMAGES_PER_SIDE:
            parts.append(f"  ... {len(images)} total, showing first {MAX_IMAGES_PER_SIDE}")
        parts.append("")

    # Text files — embed inline
    text_files = [a for a in artifacts if a.suffix.lower() in _TEXT_EXTENSIONS]
    if text_files:
        parts.append(f"### {label} Text Files:")
        for tf in text_files:
            content = _read_text_truncated(tf)
            if content is not None:
                parts.append(f"**{tf.name}** (`{tf}`):")
                parts.append(f"```\n{content}\n```")
            else:
                parts.append(f"**{tf.name}** — could not read")
        parts.append("")

    # List all artifact paths for reference
    non_text_non_image = [
        a for a in artifacts
        if a.suffix.lower() not in _TEXT_EXTENSIONS
        and a.suffix.lower() not in _IMAGE_EXTENSIONS
    ]
    if non_text_non_image:
        parts.append(f"### {label} Other Files (pre-rendered as screenshots above):")
        for a in non_text_non_image:
            parts.append(f"  - {a}")
        parts.append("")


# ---------------------------------------------------------------------------
# LLM comparison call
# ---------------------------------------------------------------------------

def _parse_preference(response: str) -> Tuple[str, str]:
    """Parse LLM response to extract preference and reason.

    Returns (preference, reason). preference is one of "A", "B", "tie", or "error".
    """
    text = response.strip()
    # Strip markdown code fences
    text = re.sub(r"^```(?:json)?\s*\n?", "", text)
    text = re.sub(r"\n?```\s*$", "", text)

    # Try JSON extraction
    json_match = re.search(r"\{[^{}]*\"preference\"[^{}]*\}", text, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group(0))
            pref = str(data.get("preference", "")).strip().upper()
            reason = str(data.get("reason", ""))
            if pref in ("A", "B", "TIE"):
                return pref.lower() if pref == "TIE" else pref, reason
        except (json.JSONDecodeError, ValueError):
            pass

    # Fallback: balanced brace extraction
    start = text.find("{")
    if start != -1:
        depth = 0
        for i, ch in enumerate(text[start:], start):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    try:
                        data = json.loads(text[start : i + 1])
                        pref = str(data.get("preference", "")).strip().upper()
                        reason = str(data.get("reason", ""))
                        if pref in ("A", "B", "TIE"):
                            return pref.lower() if pref == "TIE" else pref, reason
                    except (json.JSONDecodeError, ValueError):
                        pass
                    break

    # Last resort: regex for preference value
    pref_match = re.search(r'"preference"\s*:\s*"([^"]*)"', text, re.IGNORECASE)
    if pref_match:
        pref = pref_match.group(1).strip().upper()
        if pref in ("A", "B", "TIE"):
            return pref.lower() if pref == "TIE" else pref, text[:200]

    return "error", f"Failed to parse: {text[:300]}"


def _artifact_paths(artifacts: List[Path], workspace: Path) -> List[str]:
    """Convert artifact paths to workspace-relative strings."""
    result = []
    for a in artifacts:
        try:
            result.append(str(a.relative_to(workspace)))
        except ValueError:
            result.append(a.name)
    return result


def _flip_preference(pref: str) -> str:
    """Flip A<->B, leave tie/error unchanged."""
    if pref == "A":
        return "B"
    if pref == "B":
        return "A"
    return pref


async def _single_comparison(
    task_id: str,
    task_prompt: str,
    workspace_a: Path,
    workspace_b: Path,
    evaluator_paths: Set[str],
    max_retries: int = 2,
) -> Dict[str, Any]:
    """Run a single pairwise comparison (one presentation ordering).

    Returns dict with keys: preference, reason.
    Retries up to *max_retries* times when the LLM response cannot be parsed.

    All rendered images are written into an isolated temporary directory so
    that concurrent fwd/rev comparisons on the same workspace pair never
    interfere with each other.
    """
    # Create an isolated sibling temp directory for this comparison's renders
    render_dir = workspace_a.parent / f"_cmp_{uuid4().hex[:12]}"
    render_dir.mkdir(parents=True, exist_ok=True)

    # Discover artifacts
    artifacts_a = discover_artifacts(workspace_a, evaluator_paths)
    artifacts_b = discover_artifacts(workspace_b, evaluator_paths)

    if not artifacts_a and not artifacts_b:
        shutil.rmtree(render_dir, ignore_errors=True)
        return {
            "preference": "tie", "reason": "Both sides have no artifacts",
            "artifacts_a": [], "artifacts_b": [],
            "num_images_a": 0, "num_images_b": 0,
        }

    # Pre-render visual files into isolated subdirectories
    images_a = await prerender_artifacts(artifacts_a, render_dir=render_dir / "a")
    images_b = await prerender_artifacts(artifacts_b, render_dir=render_dir / "b")

    # File info to include in every return value
    file_info = {
        "artifacts_a": _artifact_paths(artifacts_a, workspace_a),
        "artifacts_b": _artifact_paths(artifacts_b, workspace_b),
        "num_images_a": len(images_a),
        "num_images_b": len(images_b),
    }

    # Build prompt
    prompt = build_compare_prompt(task_prompt, artifacts_a, artifacts_b, images_a, images_b)

    last_reason = ""
    try:
        for attempt in range(1, max_retries + 2):  # 1 initial + max_retries retries
            try:
                response = await query_claude_code(
                    prompt=prompt,
                    system=COMPARE_SYSTEM_PROMPT,
                    max_turns=150,
                    model="claude-opus-4-5",
                )
            except Exception as e:
                last_reason = f"LLM call failed: {e}"
                if attempt <= max_retries:
                    print(f"    [retry {attempt}/{max_retries}] {task_id}: LLM call failed, retrying...")
                    continue
                break

            preference, reason = _parse_preference(response)
            if preference != "error":
                return {"preference": preference, "reason": reason, **file_info}

            last_reason = reason
            if attempt <= max_retries:
                print(f"    [retry {attempt}/{max_retries}] {task_id}: parse failed, retrying...")
    finally:
        shutil.rmtree(render_dir, ignore_errors=True)

    return {"preference": "error", "reason": last_reason, **file_info}


async def compare_one_task(
    task_id: str,
    task_prompt: str,
    workspace_a: Path,
    workspace_b: Path,
    evaluator_paths: Set[str],
) -> Dict[str, Any]:
    """Run pairwise comparison in both presentation orders to mitigate position bias.

    Returns dict with ab_order and ba_order results (preferences mapped back
    to the original A/B identity).
    """
    # Order 1: run_a presented as "System A", run_b as "System B"
    result_ab = await _single_comparison(
        task_id, task_prompt, workspace_a, workspace_b, evaluator_paths,
    )

    # Order 2: run_b presented as "System A", run_a as "System B"
    result_ba_raw = await _single_comparison(
        task_id, task_prompt, workspace_b, workspace_a, evaluator_paths,
    )
    # Flip preference back to original identity (swap a/b artifact fields)
    result_ba = {
        "preference": _flip_preference(result_ba_raw["preference"]),
        "reason": result_ba_raw["reason"],
        "artifacts_a": result_ba_raw.get("artifacts_b", []),
        "artifacts_b": result_ba_raw.get("artifacts_a", []),
        "num_images_a": result_ba_raw.get("num_images_b", 0),
        "num_images_b": result_ba_raw.get("num_images_a", 0),
    }

    return {"ab_order": result_ab, "ba_order": result_ba}


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------

def _get_task_category(tasks_dir: Path, task_id: str) -> str:
    """Get category from task config JSON, falling back to task_id prefix."""
    try:
        with open(tasks_dir / f"{task_id}.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        cat = data.get("category", "")
        if cat:
            return cat
    except Exception:
        pass
    parts = task_id.rsplit("_task", 1)
    return parts[0] if len(parts) == 2 else task_id


async def run_comparison(
    run_a: Path,
    run_b: Path,
    tasks_dir: Path,
    task_id: Optional[str] = None,
    category: Optional[str] = None,
    concurrency: int = 3,
    checkpoint_store: Optional[CheckpointStore] = None,
    output_name: str = "",
    label_a: Optional[str] = None,
    label_b: Optional[str] = None,
) -> Dict[str, Any]:
    """Run pairwise comparison across shared tasks."""
    shared, map_a, map_b = discover_shared_tasks(run_a, run_b, tasks_dir, task_id=task_id, category=category)

    if not shared:
        filter_desc = task_id or category or "any"
        print(f"No shared tasks found for filter '{filter_desc}' between the two runs.")
        return {
            "run_a": str(run_a),
            "run_b": str(run_b),
            "timestamp": datetime.now().isoformat(),
            "summary": {"total_comparisons": 0, "a_wins": 0, "b_wins": 0, "ties": 0, "errors": 0},
            "tasks": {},
        }

    run_a_name = run_a.name
    run_b_name = run_b.name

    filter_label = (
        f" [task={task_id}]" if task_id
        else (f" [category={category}]" if category else "")
    )
    print(f"\n{'=' * 60}")
    print(f"PAIRWISE COMPARISON: {len(shared)} task(s){filter_label}")
    print(f"  Run A: {run_a}")
    print(f"  Run B: {run_b}")
    print(f"  Concurrency: {concurrency}")
    print(f"{'=' * 60}\n")

    semaphore = asyncio.Semaphore(concurrency)
    results: Dict[str, Dict[str, Any]] = {}

    async def _compare_one(tid: str) -> Tuple[str, Dict[str, Any]]:
        async with semaphore:
            task_prompt = load_task_prompt(tasks_dir, tid)
            workspace_a = map_a[tid] / "workspace"
            workspace_b = map_b[tid] / "workspace"
            # Collect evaluator paths from both workspaces (files_match_pattern
            # may resolve to different filenames in each workspace).
            ev_paths_a = collect_evaluator_paths(tasks_dir, tid, workspace=workspace_a)
            ev_paths_b = collect_evaluator_paths(tasks_dir, tid, workspace=workspace_b)
            ev_paths = ev_paths_a | ev_paths_b
            icon = {"A": "<-A", "B": "B->", "tie": "==", "error": "!!"}

            # --- AB ordering ---
            ab_key = None
            result_ab = None
            if checkpoint_store is not None:
                if label_a and label_b:
                    ab_key = CheckpointStore.make_rank_key(label_a, label_b, tid, "fwd")
                else:
                    ab_key = CheckpointStore.make_compare_key(run_a_name, run_b_name, tid, "ab", output_name)
                cached_ab = checkpoint_store.load(ab_key)
                if cached_ab is not None:
                    if "result" in cached_ab:
                        result_ab = cached_ab["result"]
                    elif "result_detail" in cached_ab:
                        rd = cached_ab["result_detail"]
                        result_ab = {"preference": rd.get("raw_preference", "error"), "reason": rd.get("reason", "")}

            if result_ab is None:
                print(f"  Comparing: {tid} (ab) ...")
                result_ab = await _single_comparison(
                    tid, task_prompt, workspace_a, workspace_b, ev_paths,
                )
                if checkpoint_store is not None and ab_key is not None:
                    checkpoint_store.save(ab_key, {
                        "run_a": str(run_a), "run_b": str(run_b),
                        "task_id": tid, "ordering": "ab",
                        "result": result_ab,
                    })
            else:
                print(f"  Cached: {tid} (ab)")

            # --- BA ordering ---
            ba_key = None
            result_ba_raw = None
            if checkpoint_store is not None:
                if label_a and label_b:
                    ba_key = CheckpointStore.make_rank_key(label_a, label_b, tid, "rev")
                else:
                    ba_key = CheckpointStore.make_compare_key(run_a_name, run_b_name, tid, "ba", output_name)
                cached_ba = checkpoint_store.load(ba_key)
                if cached_ba is not None:
                    if "result" in cached_ba:
                        result_ba_raw = cached_ba["result"]
                    elif "result_detail" in cached_ba:
                        rd = cached_ba["result_detail"]
                        result_ba_raw = {"preference": rd.get("raw_preference", "error"), "reason": rd.get("reason", "")}

            if result_ba_raw is None:
                print(f"  Comparing: {tid} (ba) ...")
                result_ba_raw = await _single_comparison(
                    tid, task_prompt, workspace_b, workspace_a, ev_paths,
                )
                if checkpoint_store is not None and ba_key is not None:
                    checkpoint_store.save(ba_key, {
                        "run_a": str(run_a), "run_b": str(run_b),
                        "task_id": tid, "ordering": "ba",
                        "result": result_ba_raw,
                    })
            else:
                print(f"  Cached: {tid} (ba)")

            # Flip BA preference back to original identity (swap a/b artifact fields)
            result_ba = {
                "preference": _flip_preference(result_ba_raw["preference"]),
                "reason": result_ba_raw["reason"],
                "artifacts_a": result_ba_raw.get("artifacts_b", []),
                "artifacts_b": result_ba_raw.get("artifacts_a", []),
                "num_images_a": result_ba_raw.get("num_images_b", 0),
                "num_images_b": result_ba_raw.get("num_images_a", 0),
            }

            ab = result_ab
            ba = result_ba
            print(f"    order(A,B) [{icon.get(ab['preference'], '??')}] winner={ab['preference']} -- {ab['reason'][:60]}")
            print(f"    order(B,A) [{icon.get(ba['preference'], '??')}] winner={ba['preference']} -- {ba['reason'][:60]}")
            return tid, {"ab_order": ab, "ba_order": ba}

    task_results = await asyncio.gather(*[_compare_one(tid) for tid in shared])

    for tid, res in task_results:
        results[tid] = res

    # Summarize — each task contributes two comparisons (both orderings)
    all_prefs = []
    category_stats: Dict[str, Dict[str, int]] = {}
    per_task: Dict[str, Dict[str, Any]] = {}

    for tid, r in results.items():
        ab_pref = r["ab_order"]["preference"]
        ba_pref = r["ba_order"]["preference"]
        all_prefs.extend([ab_pref, ba_pref])

        if ab_pref == ba_pref:
            final = ab_pref
        elif "error" in (ab_pref, ba_pref):
            final = [p for p in (ab_pref, ba_pref) if p != "error"][0] if ab_pref != ba_pref else "error"
        else:
            final = "split"

        cat = _get_task_category(tasks_dir, tid)
        per_task[tid] = {"category": cat, "ab": ab_pref, "ba": ba_pref, "final": final}

        if cat not in category_stats:
            category_stats[cat] = {"a_wins": 0, "b_wins": 0, "ties": 0, "errors": 0, "splits": 0, "total_tasks": 0}
        cs = category_stats[cat]
        cs["total_tasks"] += 1
        if final == "A":
            cs["a_wins"] += 1
        elif final == "B":
            cs["b_wins"] += 1
        elif final == "tie":
            cs["ties"] += 1
        elif final == "split":
            cs["splits"] += 1
        else:
            cs["errors"] += 1

    a_wins = sum(1 for p in all_prefs if p == "A")
    b_wins = sum(1 for p in all_prefs if p == "B")
    ties = sum(1 for p in all_prefs if p == "tie")
    errors = sum(1 for p in all_prefs if p == "error")

    output = {
        "run_a": str(run_a),
        "run_b": str(run_b),
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_tasks": len(results),
            "total_comparisons": len(all_prefs),
            "a_wins": a_wins,
            "b_wins": b_wins,
            "ties": ties,
            "errors": errors,
        },
        "by_category": dict(sorted(category_stats.items())),
        "per_task": dict(sorted(per_task.items())),
        "tasks": results,
    }

    # Print summary
    print(f"\n{'=' * 60}")
    print("COMPARISON SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Total comparisons: {len(all_prefs)} ({len(shared)} tasks x 2 orderings)")
    print(f"  A wins: {a_wins}")
    print(f"  B wins: {b_wins}")
    print(f"  Ties:   {ties}")
    if errors:
        print(f"  Errors: {errors}")

    print(f"\n  By category:")
    for cat in sorted(category_stats):
        cs = category_stats[cat]
        print(f"    {cat}: A={cs['a_wins']} B={cs['b_wins']} tie={cs['ties']} split={cs['splits']} err={cs['errors']} (n={cs['total_tasks']})")
    print(f"{'=' * 60}")

    return output


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Pairwise comparative evaluation of two benchmark runs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m benchmark.AgentSkillOS_bench.ranking.compare --run-a results/run_A --run-b results/run_B
  python -m benchmark.AgentSkillOS_bench.ranking.compare --run-a results/run_A --run-b results/run_B --task creative_design_task1
  python -m benchmark.AgentSkillOS_bench.ranking.compare --run-a results/run_A --run-b results/run_B --category creative_design
  python -m benchmark.AgentSkillOS_bench.ranking.compare --run-a results/run_A --run-b results/run_B --output comparison.json
        """,
    )

    parser.add_argument("--run-a", "-a", required=True, help="Path to first run results directory")
    parser.add_argument("--run-b", "-b", required=True, help="Path to second run results directory")
    parser.add_argument("--task", "-t", help="Compare a specific task ID")
    parser.add_argument("--category", "-c", help="Compare all tasks in a category")
    parser.add_argument("--output", "-o", help="Save comparison results to JSON file")
    parser.add_argument("--concurrency", "-n", type=int, default=3, help="Max concurrent LLM calls (default: 3)")
    parser.add_argument(
        "--benchmark", type=str, default="AgentSkillOS_bench",
        help="Benchmark name to resolve tasks directory (default: AgentSkillOS_bench)",
    )
    parser.add_argument(
        "--tasks-dir", type=str, default=None,
        help="Tasks directory (explicit override; takes precedence over --benchmark)",
    )
    parser.add_argument(
        "--checkpoint-dir", type=str, default=None,
        help="Checkpoint directory (default: .checkpoints/rank/)",
    )
    parser.add_argument(
        "--no-cache", action="store_true",
        help="Disable checkpoint caching -- rerun all comparisons from scratch",
    )
    parser.add_argument("--label-a", help="Label for run A (used in cache key to match rank.py cache)")
    parser.add_argument("--label-b", help="Label for run B (used in cache key to match rank.py cache)")

    args = parser.parse_args()

    run_a = Path(args.run_a)
    run_b = Path(args.run_b)
    if args.tasks_dir:
        tasks_dir = Path(args.tasks_dir)
    else:
        from benchmark import get_benchmark
        tasks_dir = get_benchmark(args.benchmark).tasks_dir

    if not run_a.is_dir():
        print(f"Error: Run A directory not found: {run_a}")
        return 1
    if not run_b.is_dir():
        print(f"Error: Run B directory not found: {run_b}")
        return 1

    # Set up checkpoint store
    checkpoint_store = None
    if not args.no_cache:
        ck_dir = Path(args.checkpoint_dir) if args.checkpoint_dir else Path(".checkpoints") / "rank"
        checkpoint_store = CheckpointStore(ck_dir)
        print(f"Checkpoint dir: {ck_dir}")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(run_comparison(
            run_a=run_a,
            run_b=run_b,
            tasks_dir=tasks_dir,
            task_id=args.task,
            category=args.category,
            concurrency=args.concurrency,
            checkpoint_store=checkpoint_store,
            output_name=Path(args.output).name if args.output else "",
            label_a=args.label_a,
            label_b=args.label_b,
        ))
    finally:
        try:
            pending = asyncio.all_tasks(loop)
            for task in pending:
                task.cancel()
            if pending:
                loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.run_until_complete(loop.shutdown_default_executor())
            # Force GC so subprocess transport finalizers run while the
            # loop is still open, then drain any resulting callbacks.
            gc.collect()
            loop.run_until_complete(asyncio.sleep(0))
        finally:
            asyncio.set_event_loop(None)
            loop.close()

    if args.output:
        output_path = Path(args.output)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to: {output_path}")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
