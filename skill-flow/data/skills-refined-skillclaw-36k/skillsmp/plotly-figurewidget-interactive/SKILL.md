---
name: plotly-figurewidget-interactive
description: "Fix for Plotly FigureWidget KeyError: 'uid' when updating shapes with sliders. Trigger: interactive Plotly dashboard errors, FigureWidget batch_update issues"
author: Claude Code
date: 2026-01-06
---

# Plotly FigureWidget Interactive Dashboard Fix

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2026-01-06 |
| **Goal** | Create interactive QC dashboard with linked threshold sliders using Plotly FigureWidget |
| **Environment** | Python 3.12, Plotly 6.5.0, ipywidgets 8.1.8, VS Code Jupyter |
| **Status** | Success (after multiple fixes) |

## Context
Building an interactive single-cell QC dashboard with:
- Multiple linked plots (histograms, scatter plots, pie chart)
- Threshold sliders that update all plots simultaneously
- Threshold lines on plots that move with slider values

Encountered multiple issues with Plotly FigureWidget in VS Code environment.

## Verified Workflow

### Working Pattern: Recreate Figure on Update

The most reliable approach for VS Code is to **recreate the entire figure** on each slider change rather than trying to update an existing FigureWidget:

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import ipywidgets as widgets
from IPython.display import display, clear_output

# Set renderer for VS Code compatibility
pio.renderers.default = "notebook"

# Pre-compute data (do this once outside the update function)
hist_data = np.histogram(values, bins=100)
scatter_x = data_x[subsample_mask]
scatter_y = data_y[subsample_mask]

def create_figure(threshold1, threshold2):
    """Create fresh figure with current threshold values."""
    fig = make_subplots(rows=1, cols=2)

    # Add traces
    fig.add_trace(go.Bar(x=hist_data[1][:-1], y=hist_data[0]), row=1, col=1)
    fig.add_trace(go.Scattergl(x=scatter_x, y=scatter_y, mode='markers'), row=1, col=2)

    # Add threshold lines as shapes
    shapes = [
        dict(type='line', x0=threshold1, x1=threshold1, y0=0, y1=1,
             yref='y domain', xref='x', line=dict(color='red', dash='dash'))
    ]
    fig.update_layout(shapes=shapes, height=600, width=1000)

    return fig

# Create sliders
slider1 = widgets.FloatSlider(value=50, min=0, max=100, description='Threshold:')

# Output widget for figure
fig_output = widgets.Output()

def update_dashboard(change=None):
    fig = create_figure(slider1.value, slider2.value)
    with fig_output:
        clear_output(wait=True)
        fig.show()

# Connect sliders
slider1.observe(update_dashboard, names='value')

# Display
display(slider1)
display(fig_output)
update_dashboard()  # Initial render
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| `FigureWidget` + `batch_update()` for shapes | `KeyError: 'uid'` in `_handler_js2py_traceDeltas` | Plotly 6.x bug: don't modify shapes inside `batch_update()` |
| Modify shapes list in place | Same `KeyError: 'uid'` | The bug triggers when ANY shape modification happens during batch sync |
| Update shapes outside `batch_update()` | Shapes update but traces don't sync | Partial fix - shapes work but other updates may lag |
| Just `display(FigureWidget)` in VS Code | Figure doesn't render (blank output) | VS Code renderer issues with FigureWidget |
| `fig.show()` without Output widget | Multiple overlapping figures on each update | Need `clear_output(wait=True)` in Output widget |

## Root Cause Analysis

The `KeyError: 'uid'` error occurs in Plotly 6.x when:
1. FigureWidget is used with interactive updates
2. Shapes are modified (even outside `batch_update()`)
3. The JavaScript-to-Python trace delta sync tries to access a `uid` field that doesn't exist

The bug is in `plotly/basewidget.py:445`:
```python
def _handler_js2py_traceDeltas(self, change):
    for delta in trace_deltas:
        trace_uid = delta["uid"]  # KeyError here when delta lacks 'uid'
```

## Final Parameters

```python
# Plotly configuration for VS Code
import plotly.io as pio
pio.renderers.default = "notebook"  # or "vscode"

# Figure dimensions
fig.update_layout(
    height=700,
    width=1100
)

# Subsample for performance with large datasets
n_points = min(50000, len(data))
```

## Key Insights

- **FigureWidget is fragile**: In Plotly 6.x with VS Code, FigureWidget has multiple rendering and sync issues
- **Recreate > Update**: For interactive dashboards, recreating the entire figure on each update is more reliable than trying to update in place
- **Use Output widget**: Wrap `fig.show()` in `widgets.Output()` with `clear_output(wait=True)` to prevent stacking
- **Pre-compute expensive operations**: Histograms and data subsampling should happen once, not on every update
- **Subsample large datasets**: Scatter plots with >50k points will lag; subsample for interactivity

## Alternative Approaches

If you need true in-place updates (e.g., streaming data):

```python
# Option 1: Use Dash instead of Jupyter widgets
# Option 2: Use Panel library which has better widget support
# Option 3: Downgrade to Plotly 5.x where FigureWidget is more stable
```

## References
- Plotly FigureWidget documentation: https://plotly.com/python/figurewidget/
- Related issue: https://github.com/plotly/plotly.py/issues/3441
- ipywidgets Output widget: https://ipywidgets.readthedocs.io/en/stable/examples/Output%20Widget.html
