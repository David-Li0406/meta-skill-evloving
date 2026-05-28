# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "mlflow>=2.9.0",
# ]
# ///
"""Create a new MLflow experiment with metadata.

ADR: 2025-12-12-mlflow-python-skill

This script creates MLflow experiments with optional description and tags.

Usage:
    uv run scripts/create_experiment.py --name "crypto-backtests-2025"
    uv run scripts/create_experiment.py --name "crypto-backtests-2025" --description "Q1 2025 cryptocurrency trading strategy backtests"
    uv run scripts/create_experiment.py --name "crypto-backtests-2025" --tags '{"team": "quant", "asset_class": "crypto"}'
"""

from __future__ import annotations

import argparse
import json
import sys

import mlflow


def create_experiment(
    name: str,
    description: str | None = None,
    tags: dict[str, str] | None = None,
    artifact_location: str | None = None,
) -> str:
    """Create a new MLflow experiment.

    Args:
        name: Experiment name (must be unique)
        description: Optional description
        tags: Optional tags dict
        artifact_location: Optional artifact storage location

    Returns:
        Experiment ID.
    """
    # Check if experiment already exists
    existing = mlflow.get_experiment_by_name(name)
    if existing is not None:
        print(f"Experiment '{name}' already exists with ID: {existing.experiment_id}")
        return existing.experiment_id

    # Create experiment
    experiment_id = mlflow.create_experiment(
        name=name,
        artifact_location=artifact_location,
        tags=tags,
    )

    # Set description as a tag if provided (MLflow stores description in tags)
    if description:
        client = mlflow.tracking.MlflowClient()
        client.set_experiment_tag(experiment_id, "mlflow.note.content", description)

    return experiment_id


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Create a new MLflow experiment")
    parser.add_argument(
        "--name",
        "-n",
        required=True,
        help="Experiment name (must be unique)",
    )
    parser.add_argument(
        "--description",
        "-d",
        help="Experiment description",
    )
    parser.add_argument(
        "--tags",
        "-t",
        help="Tags as JSON string (e.g., '{\"team\": \"quant\"}')",
    )
    parser.add_argument(
        "--artifact-location",
        help="Artifact storage location (default: MLflow server default)",
    )

    args = parser.parse_args()

    # Parse tags if provided
    tags = None
    if args.tags:
        try:
            tags = json.loads(args.tags)
        except json.JSONDecodeError as e:
            print(f"Error parsing --tags JSON: {e}", file=sys.stderr)
            return 1

    # Create experiment
    experiment_id = create_experiment(
        name=args.name,
        description=args.description,
        tags=tags,
        artifact_location=args.artifact_location,
    )

    print("Experiment created:")
    print(f"  Name: {args.name}")
    print(f"  ID: {experiment_id}")
    if args.description:
        print(f"  Description: {args.description}")
    if tags:
        print(f"  Tags: {tags}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
