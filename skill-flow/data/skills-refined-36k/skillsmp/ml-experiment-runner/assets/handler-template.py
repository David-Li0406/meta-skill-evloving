"""
Handler template for ML experiments.

Copy this file and modify for your sub-experiment.
"""

import io
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn

from runner import ExperimentRunner


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================


def safe_to_numpy(tensor: torch.Tensor) -> np.ndarray:
    """Safely convert tensor to numpy array."""
    if isinstance(tensor, torch.Tensor):
        return tensor.detach().cpu().numpy()
    return tensor


def safe_to_python(obj: Any) -> Any:
    """Convert numpy/torch types to Python natives for JSON serialization."""
    if isinstance(obj, dict):
        return {k: safe_to_python(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [safe_to_python(v) for v in obj]
    elif isinstance(obj, torch.Tensor):
        return safe_to_python(obj.detach().cpu().numpy())
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.bool_, np.integer, np.floating)):
        return obj.item()
    return obj


def save_plot(runner: ExperimentRunner, fig: plt.Figure, filename: str) -> str:
    """Save matplotlib figure as artifact and return path."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return runner.results.save_artifact(filename, buf.read())


# =============================================================================
# HANDLER IMPLEMENTATION
# =============================================================================


def e_template_handler(runner: ExperimentRunner) -> dict:
    """
    E-Template: [Description of what this sub-experiment tests]

    Objective: [What we're trying to learn]
    Protocol: [How we'll measure it]
    """
    print("=" * 60)
    print("E-Template: [Handler Name]")
    print("=" * 60)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    artifacts = []
    metrics = {}

    # -------------------------------------------------------------------------
    # Stage 1: Data Preparation
    # -------------------------------------------------------------------------
    print("\n[Stage 1/N] Preparing data...")
    # TODO: Load or generate your data
    # train_data, test_data = load_data()
    # print(f"  Train: {len(train_data)}, Test: {len(test_data)}")

    runner.log_metrics({"e_template/progress": 0.2})

    # -------------------------------------------------------------------------
    # Stage 2: Model Loading
    # -------------------------------------------------------------------------
    print("\n[Stage 2/N] Loading model...")
    # TODO: Load your model
    # model = load_model().to(device)
    # model.eval()

    runner.log_metrics({"e_template/progress": 0.4})

    # -------------------------------------------------------------------------
    # Stage 3: Experiment Execution
    # -------------------------------------------------------------------------
    print("\n[Stage 3/N] Running experiment...")
    # TODO: Your main experiment logic
    # with torch.no_grad():
    #     results = model(test_data)

    runner.log_metrics({"e_template/progress": 0.6})

    # -------------------------------------------------------------------------
    # Stage 4: Metric Calculation
    # -------------------------------------------------------------------------
    print("\n[Stage 4/N] Computing metrics...")
    # TODO: Calculate your metrics
    # metrics["accuracy"] = compute_accuracy(results, labels)
    # metrics["loss"] = compute_loss(results, labels)

    # Example metrics (replace with your actual metrics)
    metrics = {
        "accuracy": 0.95,
        "loss": 0.05,
    }

    # Log metrics to W&B
    for name, value in metrics.items():
        runner.log_metrics({f"e_template/{name}": value})

    runner.log_metrics({"e_template/progress": 0.8})

    # -------------------------------------------------------------------------
    # Stage 5: Visualization and Results
    # -------------------------------------------------------------------------
    print("\n[Stage 5/N] Creating visualizations...")

    # Example: Create a simple plot
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(["Accuracy", "1-Loss"], [metrics["accuracy"], 1 - metrics["loss"]])
    ax.set_ylabel("Value")
    ax.set_title("Experiment Results")
    ax.set_ylim(0, 1)
    plot_path = save_plot(runner, fig, "e_template_results.png")
    artifacts.append(plot_path)

    # Save detailed results as JSON
    results_data = safe_to_python(
        {
            "metrics": metrics,
            "config": {
                "device": str(device),
                # Add your config here
            },
        }
    )
    json_path = runner.results.save_json_artifact("e_template_results.json", results_data)
    artifacts.append(json_path)

    runner.log_metrics({"e_template/progress": 1.0})

    # -------------------------------------------------------------------------
    # Return Results
    # -------------------------------------------------------------------------
    print(f"\n  Accuracy: {metrics['accuracy']:.1%}")
    print(f"  Loss: {metrics['loss']:.4f}")

    return {
        "finding": f"Model achieves {metrics['accuracy']:.1%} accuracy with loss {metrics['loss']:.4f}",
        "metrics": safe_to_python(metrics),
        "artifacts": artifacts,
    }


# =============================================================================
# HANDLER REGISTRATION
# =============================================================================

# In your __init__.py, register this handler:
#
# from .e_template import e_template_handler
#
# def get_handlers() -> dict:
#     return {
#         "e_template": e_template_handler,
#     }
