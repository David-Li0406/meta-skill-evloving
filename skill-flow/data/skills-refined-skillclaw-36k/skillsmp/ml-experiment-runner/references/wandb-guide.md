# W&B Logging Best Practices

## Table of Contents
- [Metric Naming](#metric-naming)
- [Logging Patterns](#logging-patterns)
- [Step Management](#step-management)
- [Artifacts](#artifacts)
- [Common Issues](#common-issues)

## Metric Naming

Use hierarchical, prefixed names for clarity:

```python
# Pattern: <sub_experiment>/<metric_name>
runner.log_metrics({
    "e_p2_1/loss": 0.1,
    "e_p2_1/accuracy": 0.95,
    "e_p2_1/progress": 0.5,
})
```

**Benefits:**
- Groups metrics by sub-experiment in W&B UI
- Avoids collisions between sub-experiments
- Easy to filter and compare

## Logging Patterns

### Progress tracking for long operations

```python
def long_training_loop(runner, epochs=100):
    for epoch in range(epochs):
        loss = train_epoch()

        # Log every N epochs to avoid spam
        if epoch % 10 == 0:
            runner.log_metrics({
                "e_p2_1/epoch": epoch,
                "e_p2_1/loss": loss,
                "e_p2_1/progress": epoch / epochs,
            })
            print(f"    Epoch {epoch}/{epochs}, Loss: {loss:.4f}")
```

### Batch processing progress

```python
def process_dataset(runner, data, batch_size=16):
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        process(batch)

        progress = min(1.0, (i + batch_size) / len(data))
        runner.log_metrics({"e_p2_1/data_progress": progress})
```

### Final metrics summary

```python
# Log final metrics at the end
runner.log_metrics({
    "e_p2_1/final_loss": final_loss,
    "e_p2_1/final_accuracy": final_accuracy,
    "e_p2_1/spatial_iou": spatial_iou,
    "e_p2_1/lpips": lpips,
})
```

## Step Management

### The step conflict problem

W&B expects monotonically increasing steps. When multiple sub-experiments log, conflicts occur:

```
wandb: WARNING Tried to log to step 0 that is less than the current step 85.
```

### Solutions

**Option 1: Let W&B auto-increment (recommended)**
```python
# Don't specify step - W&B handles it
runner.log_metrics({"loss": 0.1})
```

**Option 2: Use sub-experiment offset**
```python
# Each sub-experiment gets a step range
SUB_EXP_STEPS = 1000
step_offset = sub_exp_index * SUB_EXP_STEPS

for epoch in range(100):
    runner.log_metrics({"loss": loss}, step=step_offset + epoch)
```

**Option 3: Use custom x-axis**
```python
# Define metric to use epoch as x-axis
wandb.define_metric("e_p2_1/*", step_metric="e_p2_1/epoch")

runner.log_metrics({
    "e_p2_1/epoch": epoch,
    "e_p2_1/loss": loss,
})
```

## Artifacts

### Saving plots and images

```python
import io
import matplotlib.pyplot as plt

# Create plot
fig, ax = plt.subplots()
ax.plot(losses)
ax.set_title("Training Loss")

# Save to buffer
buf = io.BytesIO()
fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
buf.seek(0)
plt.close(fig)

# Save as artifact
artifact_path = runner.results.save_artifact("loss_plot.png", buf.read())
```

### Saving JSON data

```python
results_data = {
    "metrics": {"accuracy": 0.95, "loss": 0.1},
    "config": {"learning_rate": 0.001},
}

# Convert numpy types first!
clean_data = to_python_types(results_data)
data_path = runner.results.save_json_artifact("results.json", clean_data)
```

### Saving model checkpoints

```python
import tempfile

with tempfile.NamedTemporaryFile(suffix='.pt', delete=False) as f:
    torch.save(model.state_dict(), f.name)
    with open(f.name, 'rb') as checkpoint:
        artifact_path = runner.results.save_artifact(
            "model_checkpoint.pt",
            checkpoint.read()
        )
```

## Common Issues

### Metrics not appearing

**Check:**
1. `runner.log_metrics()` was actually called
2. No exceptions before the log call
3. W&B run is active (check for init errors)

### Step warnings flooding logs

**Fix:** Don't specify step, or use define_metric:
```python
# Remove step parameter
runner.log_metrics({"loss": loss})  # Not: runner.log_metrics({"loss": loss}, step=0)
```

### Large artifacts failing

**Fix:** Chunk large files or use W&B's artifact API directly:
```python
artifact = wandb.Artifact('large-data', type='dataset')
artifact.add_file('large_file.pt')
wandb.log_artifact(artifact)
```
