# Handler Implementation Patterns

## Table of Contents
- [Basic Handler Structure](#basic-handler-structure)
- [Staged Execution Pattern](#staged-execution-pattern)
- [Error Handling](#error-handling)
- [Model Loading](#model-loading)
- [Visualization Helpers](#visualization-helpers)

## Basic Handler Structure

Every handler follows this pattern:

```python
from runner import ExperimentRunner

def e_example_handler(runner: ExperimentRunner) -> dict:
    """
    E-Example: Description of what this sub-experiment tests.

    Objective: What we're trying to learn
    Protocol: How we'll measure it
    """
    print("=" * 60)
    print("E-Example: Handler Name")
    print("=" * 60)

    # Your experiment code here...

    return {
        "finding": "One-sentence summary of what we learned",
        "metrics": {
            "accuracy": 0.95,
            "loss": 0.1,
        },
        "artifacts": [],  # List of artifact paths
    }
```

## Staged Execution Pattern

For complex handlers, use numbered stages:

```python
def e_p2_1_spatial_analysis(runner: ExperimentRunner) -> dict:
    """E-P2.1: DINOv2 Spatial Feature Analysis"""
    print("=" * 60)
    print("E-P2.1: DINOv2 Spatial Feature Analysis")
    print("=" * 60)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    artifacts = []

    # Stage 1: Data preparation
    print("\n[Stage 1/5] Generating test datasets...")
    train_data, test_data = generate_datasets()
    print(f"  Train: {len(train_data)}, Test: {len(test_data)}")

    # Stage 2: Model loading
    print("\n[Stage 2/5] Loading model...")
    model = load_model(device)
    runner.log_metrics({"e_p2_1/progress": 0.2})

    # Stage 3: Feature extraction
    print("\n[Stage 3/5] Extracting features...")
    features = extract_features(model, train_data)
    runner.log_metrics({"e_p2_1/progress": 0.4})

    # Stage 4: Training/evaluation
    print("\n[Stage 4/5] Training probe...")
    metrics = train_and_evaluate(features, test_data)
    runner.log_metrics({"e_p2_1/progress": 0.8})

    # Stage 5: Visualization and results
    print("\n[Stage 5/5] Creating visualizations...")
    plot_path = create_visualization(metrics, runner)
    artifacts.append(plot_path)
    runner.log_metrics({"e_p2_1/progress": 1.0})

    # Log final metrics
    runner.log_metrics({
        "e_p2_1/accuracy": metrics["accuracy"],
        "e_p2_1/spatial_iou": metrics["spatial_iou"],
    })

    return {
        "finding": f"Spatial IoU: {metrics['spatial_iou']:.3f}, Accuracy: {metrics['accuracy']:.1%}",
        "metrics": metrics,
        "artifacts": artifacts,
    }
```

## Error Handling

### Defensive tensor conversion

```python
def safe_to_numpy(tensor):
    """Safely convert tensor to numpy array."""
    if isinstance(tensor, torch.Tensor):
        return tensor.detach().cpu().numpy()
    return tensor

def safe_to_python(obj):
    """Convert numpy/torch types to Python natives for JSON."""
    import numpy as np

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
```

### Robust model output handling

```python
def extract_features(model, images, device):
    """Extract features with robust output handling."""
    with torch.no_grad():
        output = model.forward_features(images.to(device))

        # Handle different output formats
        if isinstance(output, dict):
            # Try known keys in order of preference
            for key in ['x_norm_patchtokens', 'x_prenorm', 'x_norm', 'last_hidden_state']:
                if key in output:
                    features = output[key]
                    # Remove CLS token if present
                    if features.shape[1] > 256:
                        features = features[:, 1:, :]
                    return features

            # Fallback: find first suitable tensor
            for key, val in output.items():
                if isinstance(val, torch.Tensor) and len(val.shape) == 3:
                    return val[:, 1:, :] if val.shape[1] > 256 else val

            raise ValueError(f"No suitable features found. Keys: {list(output.keys())}")
        else:
            # Tensor output - remove CLS token
            return output[:, 1:, :]
```

### Memory-safe batch processing

```python
def process_in_batches(data, model, batch_size=16):
    """Process data in batches with memory cleanup."""
    results = []

    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]

        with torch.no_grad():
            batch_result = model(batch)
            results.append(batch_result.cpu())

        # Clear GPU memory
        torch.cuda.empty_cache()

    return torch.cat(results, dim=0)
```

## Model Loading

### Standard pattern with caching

```python
def load_dinov2(device):
    """Load DINOv2 model with proper setup."""
    print("  Loading DINOv2-giant model...")
    model = torch.hub.load('facebookresearch/dinov2', 'dinov2_vitg14')
    model = model.to(device)
    model.eval()

    n_params = sum(p.numel() for p in model.parameters())
    print(f"  DINOv2-giant loaded: {n_params / 1e9:.2f}B params")

    return model
```

### Loading with memory constraints

```python
def load_model_efficient(model_name, device):
    """Load model with memory-efficient settings."""
    model = AutoModel.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,  # Use bfloat16
        device_map="auto",  # Automatic device placement
        low_cpu_mem_usage=True,
    )
    model.eval()
    return model
```

## Visualization Helpers

### Creating and saving plots

```python
import io
import matplotlib.pyplot as plt

def save_plot(runner, fig, filename, prefix=""):
    """Save matplotlib figure as artifact."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)

    return runner.results.save_artifact(f"{prefix}{filename}", buf.read())

# Usage
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(losses)
ax.set_xlabel("Epoch")
ax.set_ylabel("Loss")
ax.set_title("Training Progress")
artifact_path = save_plot(runner, fig, "training_loss.png", prefix="e_p2_1_")
```

### Metrics comparison table

```python
def format_metrics_table(metrics, thresholds):
    """Format metrics vs thresholds for findings."""
    lines = ["| Metric | Value | Target | Result |", "|--------|-------|--------|--------|"]

    for name, value in metrics.items():
        if name in thresholds:
            target = thresholds[name]["target"]
            direction = thresholds[name].get("direction", "higher")

            if direction == "higher":
                passed = value >= target
            else:
                passed = value <= target

            result = "Pass" if passed else "Fail"
            lines.append(f"| {name} | {value:.3f} | {target} | {result} |")

    return "\n".join(lines)
```
