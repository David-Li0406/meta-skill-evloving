#!/usr/bin/env python3
"""
Optimize DSPy programs with custom metrics and examples.

This script runs DSPy optimization with teleprompters, evaluates performance
against a metric, and saves the optimized program.

Usage:
    python optimize-dspy.py --module <module_name> --metric <metric_name> --examples <examples_file>
    python optimize-dspy.py --module reasoner --metric accuracy --examples train.jsonl

Options:
    --module: Name of the DSPy module to optimize
    --metric: Name of the metric function to use
    --examples: Path to examples file (JSONL format)
    --teleprompter: Teleprompter to use (default: bootstrap)
    --max-trials: Maximum number of optimization trials (default: 10)
    --output: Output file path for optimized program
"""

import argparse
import json
import pickle
import sys
from pathlib import Path

try:
    import dspy
except ImportError:
    print("Error: dspy is not installed. Install with: pip install dspy-ai")
    sys.exit(1)


def load_examples(file_path: Path):
    """Load examples from a JSONL file."""
    examples = []
    with open(file_path, "r") as f:
        for line in f:
            if line.strip():
                examples.append(json.loads(line))
    return examples


def optimize_module(
    module_name: str,
    metric_name: str,
    examples_file: Path,
    teleprompter_name: str,
    max_trials: int,
    output: Path,
):
    """Optimize a DSPy module with the specified metric."""
    print(f"Optimizing module: {module_name}")
    print(f"Metric: {metric_name}")
    print(f"Examples file: {examples_file}")
    print(f"Teleprompter: {teleprompter_name}")
    print(f"Max trials: {max_trials}")

    # Load examples
    try:
        examples = load_examples(examples_file)
        print(f"Loaded {len(examples)} examples")
    except Exception as e:
        print(f"Error loading examples: {e}")
        sys.exit(1)

    # Import the module dynamically
    try:
        if module_name == "reasoner":
            from agentic_fleet.dspy_modules.reasoner import DSPyReasoner
            module = DSPyReasoner()
        else:
            print(f"Error: Unknown module '{module_name}'")
            sys.exit(1)
    except ImportError as e:
        print(f"Error importing module: {e}")
        sys.exit(1)

    # Define metric function
    def accuracy_metric(example, pred, trace=None):
        """Default accuracy metric."""
        return example.output == pred.output

    # Use custom metric if provided
    if metric_name != "accuracy":
        # In a real implementation, you'd load custom metrics from a module
        print(f"Warning: Using default accuracy metric (custom metric '{metric_name}' not implemented)")
        metric = accuracy_metric
    else:
        metric = accuracy_metric

    # Select teleprompter
    teleprompters = {
        "bootstrap": dspy.BootstrapFewShot,
        "cot": dspy.ChainOfThought,
        "knn": dspy.KNNFewShot,
    }

    if teleprompter_name not in teleprompters:
        print(f"Error: Unknown teleprompter '{teleprompter_name}'")
        sys.exit(1)

    teleprompter_class = teleprompters[teleprompter_name]

    # Create teleprompter with metric
    try:
        teleprompter = teleprompter_class(metric=metric, max_labeled_demos=max_trials)
    except Exception as e:
        print(f"Error creating teleprompter: {e}")
        sys.exit(1)

    # Optimize the module
    try:
        print("Optimizing...")
        optimized = teleprompter.compile(module, trainset=examples)
        print("Optimization successful!")
    except Exception as e:
        print(f"Optimization failed: {e}")
        sys.exit(1)

    # Ensure output directory exists
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)

        # Save optimized module
        try:
            with open(output, "wb") as f:
                pickle.dump(optimized, f)
            print(f"Saved optimized module to: {output}")
        except Exception as e:
            print(f"Error saving optimized module: {e}")
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Optimize DSPy programs")
    parser.add_argument("--module", required=True, help="Name of the DSPy module to optimize")
    parser.add_argument("--metric", default="accuracy", help="Name of the metric function")
    parser.add_argument("--examples", required=True, help="Path to examples file (JSONL)")
    parser.add_argument("--teleprompter", default="bootstrap", help="Teleprompter to use")
    parser.add_argument("--max-trials", type=int, default=10, help="Maximum optimization trials")
    parser.add_argument("--output", help="Output file path for optimized program")

    args = parser.parse_args()

    output = Path(args.output) if args.output else None
    optimize_module(
        args.module,
        args.metric,
        Path(args.examples),
        args.teleprompter,
        args.max_trials,
        output,
    )


if __name__ == "__main__":
    main()
