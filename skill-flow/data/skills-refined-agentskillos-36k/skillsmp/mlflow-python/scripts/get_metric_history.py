# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "mlflow>=2.9.0",
#     "pandas>=2.0",
#     "tabulate>=0.9.0",
# ]
# ///
"""Retrieve metric history (time-series data) for a run.

ADR: 2025-12-12-mlflow-python-skill

This script retrieves the full history of logged metrics for a run,
which is a Python API-only feature (not available via CLI).

Usage:
    uv run scripts/get_metric_history.py --run-id abc123 --metrics sharpe_ratio
    uv run scripts/get_metric_history.py --run-id abc123 --metrics sharpe_ratio,cumulative_return
    uv run scripts/get_metric_history.py --run-id abc123 --all
"""

from __future__ import annotations

import argparse
import sys

import mlflow
import pandas as pd
from tabulate import tabulate


def get_metric_history(run_id: str, metric_name: str) -> pd.DataFrame:
    """Get the full history of a metric for a run.

    Args:
        run_id: MLflow run ID
        metric_name: Name of the metric

    Returns:
        DataFrame with timestamp, step, and value columns.
    """
    client = mlflow.tracking.MlflowClient()

    try:
        history = client.get_metric_history(run_id, metric_name)
    except Exception as e:
        print(f"Error getting metric '{metric_name}': {e}", file=sys.stderr)
        return pd.DataFrame()

    if not history:
        return pd.DataFrame()

    data = [
        {
            "metric": metric_name,
            "timestamp": pd.Timestamp(m.timestamp, unit="ms"),
            "step": m.step,
            "value": m.value,
        }
        for m in history
    ]

    return pd.DataFrame(data)


def get_all_metrics(run_id: str) -> list[str]:
    """Get all metric names for a run.

    Args:
        run_id: MLflow run ID

    Returns:
        List of metric names.
    """
    client = mlflow.tracking.MlflowClient()
    run = client.get_run(run_id)
    return list(run.data.metrics.keys())


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Get metric history for an MLflow run")
    parser.add_argument(
        "--run-id",
        "-r",
        required=True,
        help="MLflow run ID",
    )
    parser.add_argument(
        "--metrics",
        "-m",
        help="Comma-separated list of metrics to retrieve",
    )
    parser.add_argument(
        "--all",
        "-a",
        action="store_true",
        help="Retrieve history for all metrics",
    )
    parser.add_argument(
        "--format",
        choices=["table", "csv", "json"],
        default="table",
        help="Output format",
    )

    args = parser.parse_args()

    if not args.metrics and not args.all:
        print("Error: Must specify --metrics or --all", file=sys.stderr)
        return 1

    # Get metric names
    if args.all:
        metric_names = get_all_metrics(args.run_id)
        if not metric_names:
            print(f"No metrics found for run {args.run_id}")
            return 0
        print(f"Found {len(metric_names)} metrics: {', '.join(metric_names)}")
    else:
        metric_names = [m.strip() for m in args.metrics.split(",")]

    # Collect all metric histories
    all_data = []
    for metric_name in metric_names:
        df = get_metric_history(args.run_id, metric_name)
        if not df.empty:
            all_data.append(df)

    if not all_data:
        print("No metric history found")
        return 0

    combined = pd.concat(all_data, ignore_index=True)
    combined = combined.sort_values(["metric", "step"])

    # Output
    if args.format == "table":
        print(tabulate(combined, headers="keys", tablefmt="simple", showindex=False))
    elif args.format == "csv":
        print(combined.to_csv(index=False))
    elif args.format == "json":
        print(combined.to_json(orient="records", indent=2))

    print(f"\nTotal: {len(combined)} data points across {len(metric_names)} metrics")

    return 0


if __name__ == "__main__":
    sys.exit(main())
