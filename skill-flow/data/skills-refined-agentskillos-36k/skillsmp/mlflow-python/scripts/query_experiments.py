# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "mlflow>=2.9.0",
#     "pandas>=2.0",
#     "tabulate>=0.9.0",
# ]
# ///
"""Query MLflow experiments and runs with DataFrame output.

ADR: 2025-12-12-mlflow-python-skill

This script replaces CLI-based `mlflow experiments search` and `mlflow runs list`
with Python API calls that return DataFrames for easier filtering and analysis.

Usage:
    uv run scripts/query_experiments.py experiments
    uv run scripts/query_experiments.py runs --experiment "crypto-backtests"
    uv run scripts/query_experiments.py runs --experiment "crypto-backtests" --filter "metrics.sharpe_ratio > 1.5"
    uv run scripts/query_experiments.py runs --experiment "crypto-backtests" --order-by "metrics.sharpe_ratio DESC"
"""

from __future__ import annotations

import argparse
import sys

import mlflow
import pandas as pd
from tabulate import tabulate


def list_experiments(show_deleted: bool = False) -> pd.DataFrame:
    """List all MLflow experiments.

    Returns DataFrame with experiment_id, name, artifact_location, lifecycle_stage.
    """
    client = mlflow.tracking.MlflowClient()
    experiments = client.search_experiments()

    if not show_deleted:
        experiments = [e for e in experiments if e.lifecycle_stage == "active"]

    data = [
        {
            "experiment_id": e.experiment_id,
            "name": e.name,
            "artifact_location": e.artifact_location,
            "lifecycle_stage": e.lifecycle_stage,
        }
        for e in experiments
    ]

    return pd.DataFrame(data)


def search_runs(
    experiment_name: str,
    filter_string: str | None = None,
    order_by: list[str] | None = None,
    max_results: int = 100,
) -> pd.DataFrame:
    """Search runs in an experiment with optional filtering.

    Args:
        experiment_name: Name of the experiment to search
        filter_string: SQL-like filter (e.g., "metrics.sharpe_ratio > 1.5")
        order_by: List of columns to order by (e.g., ["metrics.sharpe_ratio DESC"])
        max_results: Maximum number of runs to return

    Returns:
        DataFrame with run info, params, and metrics.
    """
    # Get experiment by name
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        print(f"Experiment '{experiment_name}' not found", file=sys.stderr)
        return pd.DataFrame()

    # Search runs
    runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        filter_string=filter_string or "",
        order_by=order_by,
        max_results=max_results,
    )

    return runs


def format_runs_output(df: pd.DataFrame, columns: list[str] | None = None) -> str:
    """Format runs DataFrame for display.

    Args:
        df: Runs DataFrame from search_runs
        columns: Specific columns to display (default: key columns)

    Returns:
        Formatted table string.
    """
    if df.empty:
        return "No runs found"

    # Default columns to show
    if columns is None:
        # Find metric and param columns
        metric_cols = [c for c in df.columns if c.startswith("metrics.")]
        param_cols = [c for c in df.columns if c.startswith("params.")]

        # Show key columns first, then metrics, then params
        base_cols = ["run_id", "run_name", "status", "start_time"]
        columns = [c for c in base_cols if c in df.columns]
        columns.extend(sorted(metric_cols)[:5])  # Top 5 metrics
        columns.extend(sorted(param_cols)[:3])  # Top 3 params

    # Filter to existing columns
    columns = [c for c in columns if c in df.columns]

    return tabulate(df[columns], headers="keys", tablefmt="simple", showindex=False)


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Query MLflow experiments and runs")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # experiments subcommand
    exp_parser = subparsers.add_parser("experiments", help="List all experiments")
    exp_parser.add_argument(
        "--show-deleted",
        action="store_true",
        help="Include deleted experiments",
    )
    exp_parser.add_argument(
        "--format",
        choices=["table", "csv", "json"],
        default="table",
        help="Output format",
    )

    # runs subcommand
    runs_parser = subparsers.add_parser("runs", help="Search runs in an experiment")
    runs_parser.add_argument(
        "--experiment",
        "-e",
        required=True,
        help="Experiment name to search",
    )
    runs_parser.add_argument(
        "--filter",
        "-f",
        help="SQL-like filter (e.g., 'metrics.sharpe_ratio > 1.5')",
    )
    runs_parser.add_argument(
        "--order-by",
        "-o",
        help="Order by clause (e.g., 'metrics.sharpe_ratio DESC')",
    )
    runs_parser.add_argument(
        "--max-results",
        type=int,
        default=100,
        help="Maximum number of runs (default: 100)",
    )
    runs_parser.add_argument(
        "--columns",
        "-c",
        help="Comma-separated list of columns to display",
    )
    runs_parser.add_argument(
        "--format",
        choices=["table", "csv", "json"],
        default="table",
        help="Output format",
    )

    args = parser.parse_args()

    if args.command == "experiments":
        df = list_experiments(show_deleted=args.show_deleted)
        if args.format == "table":
            print(tabulate(df, headers="keys", tablefmt="simple", showindex=False))
        elif args.format == "csv":
            print(df.to_csv(index=False))
        elif args.format == "json":
            print(df.to_json(orient="records", indent=2))

    elif args.command == "runs":
        order_by = [args.order_by] if args.order_by else None
        df = search_runs(
            experiment_name=args.experiment,
            filter_string=args.filter,
            order_by=order_by,
            max_results=args.max_results,
        )

        if df.empty:
            print("No runs found")
            return 0

        columns = args.columns.split(",") if args.columns else None

        if args.format == "table":
            print(format_runs_output(df, columns=columns))
        elif args.format == "csv":
            if columns:
                df = df[[c for c in columns if c in df.columns]]
            print(df.to_csv(index=False))
        elif args.format == "json":
            if columns:
                df = df[[c for c in columns if c in df.columns]]
            print(df.to_json(orient="records", indent=2))

        print(f"\nTotal: {len(df)} runs")

    return 0


if __name__ == "__main__":
    sys.exit(main())
