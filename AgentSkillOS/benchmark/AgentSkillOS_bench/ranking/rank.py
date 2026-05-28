#!/usr/bin/env python3
"""
Multi-Method Bradley-Terry Ranking — rank N methods via pairwise LLM judging.

Runs all C(n,2) pairwise comparisons (both orderings) using the same LLM judge
as compare.py, then fits a Bradley-Terry model to produce standardized scores.

Usage:
    # Rank three methods
    python -m benchmark.AgentSkillOS_bench.ranking.rank --runs results/run1:GPT4 results/run2:Claude results/run3:Gemini

    # Filter to a category or single task
    python -m benchmark.AgentSkillOS_bench.ranking.rank --runs results/run1 results/run2 results/run3 --category creative_design
    python -m benchmark.AgentSkillOS_bench.ranking.rank --runs results/run1 results/run2 results/run3 --task creative_design_task1

    # Control concurrency and save results
    python -m benchmark.AgentSkillOS_bench.ranking.rank --runs results/run1 results/run2 results/run3 --concurrency 5 --output ranking.json
"""
import argparse
import asyncio
import json
import sys
from datetime import datetime
from itertools import combinations
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from .checkpoint import CheckpointStore
from .compare import (
    _flip_preference,
    _get_task_category,
    _single_comparison,
    collect_evaluator_paths,
    discover_shared_tasks,
    load_task_prompt,
)


# ---------------------------------------------------------------------------
# CLI argument parsing
# ---------------------------------------------------------------------------

def parse_run_spec(spec: str) -> Tuple[Path, str]:
    """Parse 'path:label' spec. Label defaults to directory basename."""
    if ":" in spec:
        path_str, label = spec.rsplit(":", 1)
    else:
        path_str, label = spec, None
    path = Path(path_str)
    if label is None:
        label = path.name
    return path, label


# ---------------------------------------------------------------------------
# Comparison unit generation and execution
# ---------------------------------------------------------------------------

def discover_shared_tasks_multi(
    runs: List[Path],
    i: int,
    j: int,
    tasks_dir: Path,
    task_id: Optional[str] = None,
    category: Optional[str] = None,
) -> Tuple[List[str], Dict[str, Path], Dict[str, Path]]:
    """Find tasks shared between run[i] and run[j].

    Returns (shared_task_ids, map_i, map_j) where the maps go from
    task_id to the actual directory path in each run.
    """
    shared, map_i, map_j = discover_shared_tasks(runs[i], runs[j], tasks_dir, task_id=task_id, category=category)
    return shared, map_i, map_j


async def run_all_comparisons(
    runs: List[Path],
    labels: List[str],
    tasks_dir: Path,
    task_id: Optional[str] = None,
    category: Optional[str] = None,
    concurrency: int = 3,
    checkpoint_store: Optional[CheckpointStore] = None,
) -> Tuple[np.ndarray, List[Dict[str, Any]]]:
    """Run all C(n,2) pairwise comparisons in both orderings.

    Returns:
        wins: float matrix of shape (n, n), wins[i][j] = wins of i over j
        details: list of per-comparison detail dicts
    """
    n = len(runs)
    wins = np.zeros((n, n), dtype=float)
    details: List[Dict[str, Any]] = []

    # Build comparison units: (i, j, task_id, direction)
    # Also collect per-run task_id -> actual directory mappings.
    # run_task_maps[run_idx][task_id] -> actual directory Path
    run_task_maps: Dict[int, Dict[str, Path]] = {}
    units: List[Tuple[int, int, str, str]] = []
    for i_idx, j_idx in combinations(range(n), 2):
        shared, map_i, map_j = discover_shared_tasks_multi(
            runs, i_idx, j_idx, tasks_dir, task_id=task_id, category=category,
        )
        # Merge maps (later calls for the same run_idx just add more entries)
        run_task_maps.setdefault(i_idx, {}).update(map_i)
        run_task_maps.setdefault(j_idx, {}).update(map_j)
        for tid in shared:
            units.append((i_idx, j_idx, tid, "fwd"))
            units.append((i_idx, j_idx, tid, "rev"))

    if not units:
        print("No comparison units found -- check that runs share tasks.")
        return wins, details

    # Split into cached and pending based on checkpoint
    cached_results: List[Dict[str, Any]] = []
    pending_units: List[Tuple[int, int, str, str]] = []
    label_to_idx = {label: idx for idx, label in enumerate(labels)}

    for unit in units:
        i_idx, j_idx, tid, direction = unit
        if checkpoint_store is not None:
            ck_key = CheckpointStore.make_rank_key(labels[i_idx], labels[j_idx], tid, direction)
            cached = checkpoint_store.load(ck_key)
            if cached is not None and "result_detail" in cached:
                # Reconstruct the result dict from the checkpoint
                rd = cached["result_detail"]
                pref = rd.get("raw_preference", "error")
                # Resolve i_idx/j_idx from labels stored in checkpoint
                ck_label_i = cached.get("label_i", labels[i_idx])
                ck_label_j = cached.get("label_j", labels[j_idx])
                ck_i = label_to_idx.get(ck_label_i, i_idx)
                ck_j = label_to_idx.get(ck_label_j, j_idx)
                ck_dir = cached.get("direction", direction)

                if ck_dir == "fwd":
                    winner_idx = ck_i if pref == "A" else (ck_j if pref == "B" else None)
                else:
                    winner_idx = ck_j if pref == "A" else (ck_i if pref == "B" else None)

                cached_results.append({
                    "i": ck_i,
                    "j": ck_j,
                    "task_id": tid,
                    "direction": ck_dir,
                    "raw_preference": pref,
                    "winner_idx": winner_idx,
                    "reason": rd.get("reason", ""),
                })
                continue
        pending_units.append(unit)

    total = len(units)
    cached_count = len(cached_results)
    pending_count = len(pending_units)
    print(f"\nTotal comparison units: {total} ({total // 2} tasks x 2 orderings)")
    if cached_count > 0:
        print(f"  Cached: {cached_count}, Pending: {pending_count}")
    print(f"Concurrency: {concurrency}\n")

    semaphore = asyncio.Semaphore(concurrency)
    completed = 0

    async def _run_unit(
        i_idx: int, j_idx: int, tid: str, direction: str,
    ) -> Dict[str, Any]:
        nonlocal completed
        async with semaphore:
            task_prompt = load_task_prompt(tasks_dir, tid)

            # Resolve actual task directories via the maps
            dir_i = run_task_maps[i_idx][tid]
            dir_j = run_task_maps[j_idx][tid]

            if direction == "fwd":
                ws_a = dir_i / "workspace"
                ws_b = dir_j / "workspace"
            else:  # rev
                ws_a = dir_j / "workspace"
                ws_b = dir_i / "workspace"

            ev_paths = collect_evaluator_paths(tasks_dir, tid, workspace=ws_a)
            ev_paths |= collect_evaluator_paths(tasks_dir, tid, workspace=ws_b)

            result = await _single_comparison(tid, task_prompt, ws_a, ws_b, ev_paths)
            pref = result["preference"]  # "A", "B", "tie", or "error"

            # Map LLM preference back to method indices
            if direction == "fwd":
                # A = i, B = j
                winner_idx = i_idx if pref == "A" else (j_idx if pref == "B" else None)
            else:
                # A = j, B = i
                winner_idx = j_idx if pref == "A" else (i_idx if pref == "B" else None)

            detail = {
                "i": i_idx,
                "j": j_idx,
                "task_id": tid,
                "direction": direction,
                "raw_preference": pref,
                "winner_idx": winner_idx,
                "reason": result["reason"],
            }

            # Persist checkpoint immediately
            if checkpoint_store is not None:
                ck_key = CheckpointStore.make_rank_key(labels[i_idx], labels[j_idx], tid, direction)
                checkpoint_store.save(ck_key, {
                    "label_i": labels[i_idx],
                    "label_j": labels[j_idx],
                    "task_id": tid,
                    "direction": direction,
                    "result_detail": {
                        "raw_preference": pref,
                        "reason": result["reason"],
                    },
                })

            completed += 1
            dir_label = f"{labels[i_idx]} vs {labels[j_idx]}" if direction == "fwd" else f"{labels[j_idx]} vs {labels[i_idx]}"
            icon = {"A": "<-A", "B": "B->", "tie": "==", "error": "!!"}.get(pref, "??")
            print(f"  [{completed}/{pending_count}] {tid} ({dir_label}) [{icon}] {pref} -- {result['reason'][:60]}")

            return detail

    pending_results = await asyncio.gather(
        *[_run_unit(i_idx, j_idx, tid, d) for i_idx, j_idx, tid, d in pending_units]
    )

    all_results = list(cached_results) + list(pending_results)

    for r in all_results:
        i_idx, j_idx = r["i"], r["j"]
        pref = r["raw_preference"]
        winner = r["winner_idx"]

        if pref == "tie":
            wins[i_idx][j_idx] += 0.5
            wins[j_idx][i_idx] += 0.5
        elif winner is not None:
            loser = j_idx if winner == i_idx else i_idx
            wins[winner][loser] += 1.0

        details.append(r)

    return wins, details


# ---------------------------------------------------------------------------
# Bradley-Terry fitting (MM algorithm)
# ---------------------------------------------------------------------------

def fit_bradley_terry(
    wins: np.ndarray,
    alpha: float = 0.1,
    max_iter: int = 1000,
    tol: float = 1e-6,
) -> np.ndarray:
    """Fit Bradley-Terry model using the MM (minorization-maximization) algorithm.

    Args:
        wins: (n, n) matrix where wins[i][j] = number of times i beat j
        alpha: Laplace smoothing -- adds alpha virtual wins for every pair
        max_iter: maximum iterations
        tol: convergence tolerance (max absolute change in log-scores)

    Returns:
        scores: array of length n, centered log-strength parameters
                (higher = better, mean = 0)
    """
    n = wins.shape[0]
    if n < 2:
        return np.zeros(n)

    # Apply Laplace smoothing
    w = wins + alpha
    np.fill_diagonal(w, 0.0)  # diagonal has no self-play; remove spurious alpha
    # Total games between i and j
    n_ij = w + w.T  # n_ij[i][j] = w[i][j] + w[j][i]

    pi = np.ones(n, dtype=float)

    for iteration in range(max_iter):
        pi_old = pi.copy()
        pi_new = np.empty(n, dtype=float)
        for i in range(n):
            w_i = w[i].sum()  # total wins for i
            denom = 0.0
            for j in range(n):
                if j == i:
                    continue
                denom += n_ij[i][j] / (pi_old[i] + pi_old[j])
            if denom > 0:
                pi_new[i] = w_i / denom
            else:
                pi_new[i] = pi_old[i]
        pi = pi_new

        # Normalize so geometric mean = 1
        pi = pi / np.exp(np.mean(np.log(pi)))

        # Check convergence
        log_change = np.max(np.abs(np.log(pi) - np.log(pi_old)))
        if log_change < tol:
            break

    # Return centered log-scores
    scores = np.log(pi) - np.mean(np.log(pi))
    return scores


def scores_to_scale(scores: np.ndarray, lo: float = 0.0, hi: float = 100.0) -> np.ndarray:
    """Linearly rescale scores so that min maps to lo and max maps to hi."""
    s_min, s_max = scores.min(), scores.max()
    if s_max - s_min < 1e-12:
        return np.full_like(scores, (lo + hi) / 2)
    return lo + (scores - s_min) / (s_max - s_min) * (hi - lo)


# ---------------------------------------------------------------------------
# Per-task Bradley-Terry: consolidation, fitting, and aggregation
# ---------------------------------------------------------------------------

def consolidate_fwd_rev_verdict(
    fwd_pref: Optional[str],
    rev_pref: Optional[str],
) -> Optional[Tuple[str, float]]:
    """Merge fwd and rev results for a single (task, i, j) pair into one verdict.

    Returns:
        ("winner", weight) where winner is "i", "j", or "tie" and weight is 1.0,
        or None if both are errors / missing.

    Merge rules:
        fwd=A rev=A  -> i wins  (fwd has i as A)
        fwd=B rev=B  -> j wins
        tie + tie    -> tie
        A + B (split)-> tie
        win + error  -> use the non-error side
        error+error  -> skip (None)
    """
    def _map_fwd(pref: str) -> str:
        if pref == "A":
            return "i"
        if pref == "B":
            return "j"
        return pref  # "tie" or "error"

    def _map_rev(pref: str) -> str:
        # In rev ordering, A=j and B=i
        if pref == "A":
            return "j"
        if pref == "B":
            return "i"
        return pref

    f = _map_fwd(fwd_pref) if fwd_pref else "error"
    r = _map_rev(rev_pref) if rev_pref else "error"

    if f == "error" and r == "error":
        return None

    if f == "error":
        # Only rev is valid
        if r in ("i", "j"):
            return (r, 1.0)
        return ("tie", 1.0)

    if r == "error":
        # Only fwd is valid
        if f in ("i", "j"):
            return (f, 1.0)
        return ("tie", 1.0)

    # Both valid
    if f == r:
        # Agree
        return (f, 1.0)
    else:
        # Disagree (split) -> tie
        return ("tie", 1.0)


def build_per_task_win_matrices(
    details: List[Dict[str, Any]],
    n: int,
) -> Dict[str, np.ndarray]:
    """Group details by task_id, consolidate fwd/rev, build per-task win matrices.

    Returns:
        dict mapping task_id -> (n, n) win matrix
    """
    from collections import defaultdict

    # Group by (task_id, i, j)
    grouped: Dict[Tuple[str, int, int], Dict[str, str]] = defaultdict(dict)
    for d in details:
        key = (d["task_id"], d["i"], d["j"])
        direction = d["direction"]  # "fwd" or "rev"
        grouped[key][direction] = d["raw_preference"]

    # Build per-task matrices
    task_matrices: Dict[str, np.ndarray] = {}
    for (task_id, i, j), verdicts in grouped.items():
        if task_id not in task_matrices:
            task_matrices[task_id] = np.zeros((n, n), dtype=float)

        result = consolidate_fwd_rev_verdict(
            verdicts.get("fwd"),
            verdicts.get("rev"),
        )
        if result is None:
            continue

        winner, weight = result
        mat = task_matrices[task_id]
        if winner == "i":
            mat[i][j] += weight
        elif winner == "j":
            mat[j][i] += weight
        elif winner == "tie":
            mat[i][j] += 0.5
            mat[j][i] += 0.5

    return task_matrices


def fit_per_task_bt(
    task_matrices: Dict[str, np.ndarray],
    alpha: float = 0.1,
) -> Dict[str, np.ndarray]:
    """Fit Bradley-Terry independently for each task.

    Returns:
        dict mapping task_id -> scaled scores array (0-100)
    """
    per_task_scores: Dict[str, np.ndarray] = {}
    for task_id, wins in task_matrices.items():
        raw = fit_bradley_terry(wins, alpha=alpha)
        scaled = scores_to_scale(raw)
        per_task_scores[task_id] = scaled
    return per_task_scores


def aggregate_per_task_scores(
    per_task_scores: Dict[str, np.ndarray],
    labels: List[str],
    tasks_dir: Path,
) -> Tuple[Dict[str, float], Dict[str, Dict[str, float]]]:
    """Aggregate per-task scores into overall and by-category averages.

    Returns:
        (overall_scores, by_category)
        overall_scores: {method_label: mean_score}
        by_category: {category: {method_label: mean_score}}
    """
    from collections import defaultdict

    n = len(labels)

    # Collect scores per method across all tasks
    all_scores: List[np.ndarray] = list(per_task_scores.values())
    if not all_scores:
        return {l: 0.0 for l in labels}, {}

    # Overall: mean across tasks for each method
    stacked = np.stack(all_scores, axis=0)  # (num_tasks, n)
    overall_means = stacked.mean(axis=0)  # (n,)
    overall_scores = {labels[i]: round(float(overall_means[i]), 2) for i in range(n)}

    # By category
    cat_scores: Dict[str, List[np.ndarray]] = defaultdict(list)
    for task_id, scores in per_task_scores.items():
        cat = _get_task_category(tasks_dir, task_id)
        cat_scores[cat].append(scores)

    by_category: Dict[str, Dict[str, float]] = {}
    for cat in sorted(cat_scores):
        cat_stacked = np.stack(cat_scores[cat], axis=0)
        cat_means = cat_stacked.mean(axis=0)
        by_category[cat] = {labels[i]: round(float(cat_means[i]), 2) for i in range(n)}

    return overall_scores, by_category


def print_per_task_scores_table(
    per_task_scores: Dict[str, np.ndarray],
    labels: List[str],
) -> None:
    """Print a method x task score matrix."""
    if not per_task_scores:
        return

    task_ids = sorted(per_task_scores.keys())
    n = len(labels)

    # Column widths
    task_col_w = max(len(t) for t in task_ids)
    task_col_w = max(task_col_w, 8)
    method_col_w = max(len(l) for l in labels)
    method_col_w = max(method_col_w, 6)

    print(f"\n{'=' * 60}")
    print("PER-TASK SCORES (Bradley-Terry, 0-100)")
    print(f"{'=' * 60}")

    # Header
    header = f"  {'Task':<{task_col_w}}"
    for l in labels:
        header += f"  {l:>{method_col_w}}"
    print(header)
    print(f"  {'-' * task_col_w}" + f"  {'-' * method_col_w}" * n)

    for tid in task_ids:
        scores = per_task_scores[tid]
        row = f"  {tid:<{task_col_w}}"
        for i in range(n):
            row += f"  {scores[i]:>{method_col_w}.1f}"
        print(row)

    print(f"{'=' * 60}")


def print_category_scores_table(
    by_category: Dict[str, Dict[str, float]],
    labels: List[str],
) -> None:
    """Print by-category average scores."""
    if not by_category:
        return

    cat_col_w = max(len(c) for c in by_category)
    cat_col_w = max(cat_col_w, 10)
    method_col_w = max(len(l) for l in labels)
    method_col_w = max(method_col_w, 6)
    n = len(labels)

    print(f"\n{'=' * 60}")
    print("BY-CATEGORY SCORES (mean of per-task BT scores)")
    print(f"{'=' * 60}")

    header = f"  {'Category':<{cat_col_w}}"
    for l in labels:
        header += f"  {l:>{method_col_w}}"
    print(header)
    print(f"  {'-' * cat_col_w}" + f"  {'-' * method_col_w}" * n)

    for cat in sorted(by_category):
        row = f"  {cat:<{cat_col_w}}"
        for l in labels:
            row += f"  {by_category[cat][l]:>{method_col_w}.1f}"
        print(row)

    print(f"{'=' * 60}")


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def print_ranking_table(labels: List[str], scaled: np.ndarray, raw_scores: np.ndarray) -> None:
    """Print a ranked table to console."""
    order = np.argsort(-scaled)  # descending

    max_label_len = max(len(l) for l in labels)
    col_w = max(max_label_len, 6)

    print(f"\n{'=' * 60}")
    print("RANKING (Bradley-Terry)")
    print(f"{'=' * 60}")
    print(f"  {'Rank':<6} {'Method':<{col_w}}  {'Score':>7}  {'Log-Strength':>14}")
    print(f"  {'-' * 6} {'-' * col_w}  {'-' * 7}  {'-' * 14}")
    for rank, idx in enumerate(order, 1):
        print(f"  {rank:<6} {labels[idx]:<{col_w}}  {scaled[idx]:7.2f}  {raw_scores[idx]:>14.4f}")
    print(f"{'=' * 60}")


def print_win_matrix(labels: List[str], wins: np.ndarray) -> None:
    """Print the win matrix to console."""
    n = len(labels)
    max_label_len = max(len(l) for l in labels)
    col_w = max(max_label_len, 5)

    print(f"\n{'=' * 60}")
    print("WIN MATRIX (row beat column)")
    print(f"{'=' * 60}")

    # Header row
    header = f"  {'':<{col_w}}"
    for l in labels:
        header += f"  {l:>{col_w}}"
    print(header)
    print(f"  {'-' * col_w}" + f"  {'-' * col_w}" * n)

    for i in range(n):
        row = f"  {labels[i]:<{col_w}}"
        for j in range(n):
            if i == j:
                row += f"  {'--':>{col_w}}"
            else:
                val = wins[i][j]
                if val == int(val):
                    row += f"  {int(val):>{col_w}}"
                else:
                    row += f"  {val:>{col_w}.1f}"
        print(row)
    print(f"{'=' * 60}")


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------

async def run_ranking(
    runs: List[Path],
    labels: List[str],
    tasks_dir: Path,
    task_id: Optional[str] = None,
    category: Optional[str] = None,
    concurrency: int = 3,
    alpha: float = 0.1,
    checkpoint_store: Optional[CheckpointStore] = None,
) -> Dict[str, Any]:
    """Run full ranking pipeline: pairwise comparisons + Bradley-Terry fitting."""
    n = len(runs)
    filter_label = (
        f" [task={task_id}]" if task_id
        else (f" [category={category}]" if category else "")
    )
    print(f"\n{'=' * 60}")
    print(f"MULTI-METHOD RANKING: {n} methods{filter_label}")
    print(f"{'=' * 60}")
    for i, (run, label) in enumerate(zip(runs, labels)):
        print(f"  [{i}] {label}: {run}")
    print(f"{'=' * 60}")

    # Run all pairwise comparisons
    wins, details = await run_all_comparisons(
        runs, labels, tasks_dir,
        task_id=task_id, category=category, concurrency=concurrency,
        checkpoint_store=checkpoint_store,
    )

    # Fit Bradley-Terry
    raw_scores = fit_bradley_terry(wins, alpha=alpha)
    scaled = scores_to_scale(raw_scores)

    # Display global results
    print_ranking_table(labels, scaled, raw_scores)
    print_win_matrix(labels, wins)

    # Build global output
    order = np.argsort(-scaled).tolist()
    ranking = []
    for rank, idx in enumerate(order, 1):
        ranking.append({
            "rank": rank,
            "method": labels[idx],
            "path": str(runs[idx]),
            "score": round(float(scaled[idx]), 2),
            "log_strength": round(float(raw_scores[idx]), 4),
        })

    # --- Per-task Bradley-Terry ---
    tasks_dir_for_cat = tasks_dir
    task_matrices = build_per_task_win_matrices(details, n)
    per_task_scores = fit_per_task_bt(task_matrices, alpha=alpha)
    overall_scores, by_category = aggregate_per_task_scores(
        per_task_scores, labels, tasks_dir_for_cat,
    )

    # Display per-task results
    print_per_task_scores_table(per_task_scores, labels)
    print_category_scores_table(by_category, labels)

    # Per-task BT ranking (by overall mean)
    pt_order = sorted(overall_scores.keys(), key=lambda m: overall_scores[m], reverse=True)
    pt_ranking = []
    for rank_num, method in enumerate(pt_order, 1):
        pt_ranking.append({
            "rank": rank_num,
            "method": method,
            "score": overall_scores[method],
        })

    # Print per-task BT ranking
    print(f"\n{'=' * 60}")
    print("RANKING (Per-Task Bradley-Terry, mean across tasks)")
    print(f"{'=' * 60}")
    max_label_len = max(len(l) for l in labels)
    col_w = max(max_label_len, 6)
    print(f"  {'Rank':<6} {'Method':<{col_w}}  {'Score':>7}")
    print(f"  {'-' * 6} {'-' * col_w}  {'-' * 7}")
    for entry in pt_ranking:
        print(f"  {entry['rank']:<6} {entry['method']:<{col_w}}  {entry['score']:7.2f}")
    print(f"{'=' * 60}")

    # Serialise per-task scores and matrices for JSON
    per_task_scores_json = {
        tid: {labels[i]: round(float(s[i]), 2) for i in range(n)}
        for tid, s in per_task_scores.items()
    }
    per_task_win_matrices_json = {
        tid: mat.tolist() for tid, mat in task_matrices.items()
    }

    per_task_bt = {
        "ranking": pt_ranking,
        "overall_scores": overall_scores,
        "by_category": by_category,
        "per_task_scores": per_task_scores_json,
        "per_task_win_matrices": per_task_win_matrices_json,
    }

    output = {
        "timestamp": datetime.now().isoformat(),
        "methods": [{"label": l, "path": str(p)} for l, p in zip(labels, runs)],
        "ranking": ranking,
        "win_matrix": wins.tolist(),
        "bt_params": {"alpha": alpha},
        "pairwise_details": details,
        "filters": {"task_id": task_id, "category": category},
        "per_task_bt": per_task_bt,
    }

    return output


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Multi-method ranking via pairwise LLM comparison and Bradley-Terry model",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python -m benchmark.AgentSkillOS_bench.ranking.rank --runs results/run1:GPT4 results/run2:Claude results/run3:Gemini
  python -m benchmark.AgentSkillOS_bench.ranking.rank --runs results/run1 results/run2 results/run3 --category creative_design
  python -m benchmark.AgentSkillOS_bench.ranking.rank --runs results/run1 results/run2 --task creative_design_task1 --output ranking.json
        """,
    )

    parser.add_argument(
        "--runs", "-r", nargs="+", required=True,
        help="Run directories in path:label format (label defaults to dirname)",
    )
    parser.add_argument("--task", "-t", help="Rank on a specific task ID only")
    parser.add_argument("--category", "-c", help="Rank on tasks in a category only")
    parser.add_argument("--output", "-o", help="Save ranking results to JSON file")
    parser.add_argument(
        "--concurrency", "-n", type=int, default=3,
        help="Max concurrent LLM calls (default: 3)",
    )
    parser.add_argument(
        "--alpha", type=float, default=0.1,
        help="Laplace smoothing for Bradley-Terry (default: 0.1)",
    )
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

    args = parser.parse_args()

    # Parse run specs
    runs: List[Path] = []
    labels: List[str] = []
    for spec in args.runs:
        path, label = parse_run_spec(spec)
        if not path.is_dir():
            print(f"Error: Run directory not found: {path}")
            return 1
        runs.append(path)
        labels.append(label)

    if len(runs) < 2:
        print("Error: Need at least 2 runs to rank.")
        return 1

    # Check for duplicate labels
    if len(set(labels)) != len(labels):
        print("Error: Duplicate labels detected. Use path:label to assign unique labels.")
        return 1

    if args.tasks_dir:
        tasks_dir = Path(args.tasks_dir)
    else:
        from benchmark import get_benchmark
        tasks_dir = get_benchmark(args.benchmark).tasks_dir

    # Set up checkpoint store
    checkpoint_store = None
    if not args.no_cache:
        ck_dir = Path(args.checkpoint_dir) if args.checkpoint_dir else Path(".checkpoints") / "rank"
        checkpoint_store = CheckpointStore(ck_dir)
        print(f"Checkpoint dir: {ck_dir}")

    result = asyncio.run(run_ranking(
        runs=runs,
        labels=labels,
        tasks_dir=tasks_dir,
        task_id=args.task,
        category=args.category,
        concurrency=args.concurrency,
        alpha=args.alpha,
        checkpoint_store=checkpoint_store,
    ))

    if args.output:
        output_path = Path(args.output)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False, default=str)
        print(f"\nResults saved to: {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
