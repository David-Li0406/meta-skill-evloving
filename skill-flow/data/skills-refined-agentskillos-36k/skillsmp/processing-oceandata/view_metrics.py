#!/usr/bin/env python3
"""
View training/validation/test metrics from saved npz files

This script reads metrics saved by ocean_trainer during training and testing,
and displays them in a formatted, easy-to-read manner.

The ocean_trainer saves two types of metric files:
1. final_metrics.npz (after training): Contains valid_metrics and test_metrics
2. test_metrics.npz (after testing): Contains only test_metrics

Usage:
    # View metrics from final_metrics.npz (after training)
    python view_metrics.py --metrics_file logs/pearl_river/10_16/OceanCNN_13_22_08/final_metrics.npz

    # View metrics from test_metrics.npz (after testing)
    python view_metrics.py --metrics_file logs/pearl_river/10_16/OceanCNN_13_22_08/test_metrics.npz

    # View metrics from model directory (auto-detect file)
    python view_metrics.py --model_dir logs/pearl_river/10_16/OceanCNN_13_22_08
"""

import argparse
import numpy as np
from pathlib import Path
from typing import Dict, Any
import sys


def format_metric_value(value: Any) -> str:
    """
    Format metric value for display

    Args:
        value: Metric value (float, int, or other)

    Returns:
        Formatted string
    """
    if isinstance(value, (float, np.floating)):
        # Use scientific notation for very small/large numbers
        if abs(value) < 0.001 or abs(value) > 10000:
            return f"{value:.6e}"
        else:
            return f"{value:.6f}"
    elif isinstance(value, (int, np.integer)):
        return str(value)
    else:
        return str(value)


def print_metrics_dict(metrics: Dict[str, Any], title: str = "Metrics", indent: int = 0):
    """
    Print metrics dictionary in a formatted way

    Args:
        metrics: Dictionary of metrics
        title: Title for this metrics section
        indent: Indentation level
    """
    indent_str = "  " * indent
    print(f"{indent_str}{title}:")
    print(f"{indent_str}{'-' * 60}")

    # Separate loss and other metrics
    loss_metrics = {}
    other_metrics = {}

    for key, value in sorted(metrics.items()):
        if 'loss' in key.lower():
            loss_metrics[key] = value
        else:
            other_metrics[key] = value

    # Print loss metrics first
    if loss_metrics:
        print(f"{indent_str}Loss Metrics:")
        for key, value in loss_metrics.items():
            formatted_value = format_metric_value(value)
            print(f"{indent_str}  {key:25s} = {formatted_value}")

    # Then print other metrics
    if other_metrics:
        if loss_metrics:
            print()  # Add blank line
        print(f"{indent_str}Performance Metrics:")
        for key, value in other_metrics.items():
            formatted_value = format_metric_value(value)
            print(f"{indent_str}  {key:25s} = {formatted_value}")

    print()


def load_and_display_metrics(metrics_file: Path):
    """
    Load and display metrics from npz file

    The ocean_trainer saves metrics in the following format:

    final_metrics.npz (from process() function):
        - Created at line 333-337 in ocean_trainer.py
        - Contains:
            - 'valid_metrics': dict from evaluate(split="valid").to_dict()
            - 'test_metrics': dict from evaluate(split="test").to_dict()

    test_metrics.npz (from test() function):
        - Created at line 359-361 in ocean_trainer.py
        - Contains:
            - 'test_metrics': dict from evaluate(split="test").to_dict()

    Args:
        metrics_file: Path to metrics npz file
    """
    if not metrics_file.exists():
        print(f"Error: Metrics file not found: {metrics_file}")
        sys.exit(1)

    print("=" * 80)
    print(f"Loading metrics from: {metrics_file}")
    print("=" * 80)
    print()

    # Load npz file
    data = np.load(metrics_file, allow_pickle=True)

    # Check what keys are available
    available_keys = data.files
    print(f"Available metrics: {', '.join(available_keys)}")
    print()

    # Display each metrics dictionary
    for key in available_keys:
        value = data[key]

        if isinstance(value, np.ndarray) and value.dtype == object:
            # This is likely a dictionary stored as numpy array
            metrics_dict = value.item()

            if isinstance(metrics_dict, dict):
                # Format the title
                if 'valid' in key:
                    title = "Validation Metrics"
                elif 'test' in key:
                    title = "Test Metrics"
                elif 'train' in key:
                    title = "Training Metrics"
                else:
                    title = key.replace('_', ' ').title()

                print_metrics_dict(metrics_dict, title)
            else:
                print(f"{key}: {metrics_dict}")
                print()
        else:
            print(f"{key}: {value}")
            print()

    print("=" * 80)


def find_metrics_file(model_dir: Path) -> Path:
    """
    Find metrics file in model directory

    Args:
        model_dir: Path to model directory

    Returns:
        Path to metrics file

    Raises:
        FileNotFoundError: If no metrics file found
    """
    # Try final_metrics.npz first (contains both valid and test)
    final_metrics = model_dir / "final_metrics.npz"
    if final_metrics.exists():
        return final_metrics

    # Then try test_metrics.npz
    test_metrics = model_dir / "test_metrics.npz"
    if test_metrics.exists():
        return test_metrics

    raise FileNotFoundError(
        f"No metrics file found in {model_dir}. "
        f"Looked for: final_metrics.npz, test_metrics.npz"
    )


def main():
    parser = argparse.ArgumentParser(
        description='View training/validation/test metrics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # View metrics from specific file
  python view_metrics.py --metrics_file logs/pearl_river/10_16/OceanCNN_13_22_08/final_metrics.npz

  # Auto-detect metrics file in model directory
  python view_metrics.py --model_dir logs/pearl_river/10_16/OceanCNN_13_22_08

Metrics file formats:
  - final_metrics.npz: Saved after training, contains valid_metrics and test_metrics
  - test_metrics.npz: Saved after testing, contains only test_metrics

Metrics typically include:
  - Loss metrics: valid_loss, test_loss
  - Performance metrics: MAE, RMSE, R2, etc. (defined in utils/metrics.py)
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--metrics_file',
        type=str,
        help='Path to metrics npz file (final_metrics.npz or test_metrics.npz)'
    )
    group.add_argument(
        '--model_dir',
        type=str,
        help='Path to model directory (will auto-detect metrics file)'
    )

    args = parser.parse_args()

    # Determine metrics file path
    if args.metrics_file:
        metrics_file = Path(args.metrics_file)
    else:
        model_dir = Path(args.model_dir)
        try:
            metrics_file = find_metrics_file(model_dir)
            print(f"Found metrics file: {metrics_file.name}")
            print()
        except FileNotFoundError as e:
            print(f"Error: {e}")
            sys.exit(1)

    # Load and display metrics
    load_and_display_metrics(metrics_file)


if __name__ == "__main__":
    main()

