from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, List

from modify_csv import modify_csv_inplace
from utils import compute_context, load_json


def _ensure_list(v):
    if v is None:
        return None
    if isinstance(v, list):
        return v
    return [v]


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply CSV changes described in plan.json")
    parser.add_argument("--plan", required=True, help="Path to plan.json")
    args = parser.parse_args()

    plan_path = Path(args.plan).expanduser().resolve()
    plan = load_json(plan_path)
    ctx = compute_context(plan, plan_path)

    changes = plan.get("csv_changes", []) or []
    if not changes:
        print("No csv_changes in plan. Nothing to do.")
        return

    for idx, change in enumerate(changes):
        rel_file = str(change.get("file") or "Boundary.csv")
        csv_path = ctx.sample_dir / rel_file

        column = str(change["column"])
        value = change.get("value")

        start_time = change.get("start_time")
        end_time = change.get("end_time")
        match_time = _ensure_list(change.get("match_time"))
        row_index = _ensure_list(change.get("row_index"))

        print(f"[{idx}] Modifying {csv_path} column={column} value={value}")
        modified, preview = modify_csv_inplace(
            csv_path=csv_path,
            column=column,
            value=str(value),
            start_time=str(start_time) if start_time else None,
            end_time=str(end_time) if end_time else None,
            match_time=[str(x) for x in match_time] if match_time else None,
            row_index=[int(x) for x in row_index] if row_index else None,
        )
        print(f"  rows_modified: {modified}")
        print(f"  old_values_preview: {preview}")

    print("Done.")


if __name__ == "__main__":
    main()
