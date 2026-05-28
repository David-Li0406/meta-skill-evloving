---
name: panel-architecture
description: Best practices for building Panel visualization apps using param.Parameterized classes, reactive binding with pn.bind(), and URL state sync.
---

# Panel Application Architecture

## Core Patterns

### 1. DataHolder for Reactive State

```python
import param
import pandas as pd

class DataHolder(param.Parameterized):
    """Central state container that components watch."""
    selected_id = param.String(default="")
    filtered_df = param.DataFrame()
    is_loaded = param.Boolean(default=False)
```

### 2. Reactive Binding with pn.bind()

```python
# Function called when parameter changes
display = pn.bind(
    self.render_content,
    record_id=self.data_holder.param.selected_id,
    df=self.data_holder.param.filtered_df,
)
pn.Column(display)
```

### 3. Component Pattern

```python
class MyComponent:
    def __init__(self, data_holder, config):
        self.data_holder = data_holder
        self.config = config

    def create(self):
        """Return Panel viewable. Called once or reactively."""
        return pn.bind(self._render, df=self.data_holder.param.filtered_df)

    def _render(self, df):
        # Create and return widget/pane
        ...
```

## URL State Synchronization

### When to Use Each Pattern

| Scenario | Use | Why |
|----------|-----|-----|
| Widget created once | `location.sync()` | Simple, bidirectional |
| Widget in reactive render | One-way sync | Avoids race conditions |
| Multiple syncs updating URL | One-way sync | Prevents widget reversion |

### Native Sync (for static widgets)

```python
def _sync_url_state(self):
    location = pn.state.location
    location.sync(self.my_widget, {'value': 'param_name'})
```

### One-Way Sync (for reactive widgets)

```python
from urllib.parse import parse_qs

def get_url_param(name, default=None):
    query = pn.state.location.search or ""
    params = parse_qs(query.lstrip("?"))
    return params.get(name, [default])[0]

def update_url_param(name, value):
    pn.state.location.update_query(**{name: value})

# Usage
class MyComponent:
    def __init__(self):
        self._initial = get_url_param("my_param")  # Read once

    def create(self):
        widget = pn.widgets.Select(value=self._initial, ...)
        widget.param.watch(
            lambda e: update_url_param("my_param", e.new), "value"
        )
        return widget
```

### Auto-Load on Page Load

```python
def main_layout(self):
    # ... create layout ...

    def _autoload():
        if get_url_param("project"):
            self.load_data()
    pn.state.onload(_autoload)

    return template
```

## Layout Patterns

### Tabulator for DataFrames

```python
table = pn.widgets.Tabulator(
    df,
    selectable=1,
    frozen_columns=["id"],
    header_filters=True,
    height=400,
    sizing_mode="stretch_width",
)

def on_selection(event):
    if event.new:
        data_holder.selected_id = str(df.iloc[event.new[0]]["_id"])

table.param.watch(on_selection, "selection")
```

### Bokeh Scatter with Hover Image

```python
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool

source = ColumnDataSource(df)
p = figure(tools="pan,wheel_zoom,reset,tap")
scatter = p.scatter(x="x", y="y", source=source)

tooltips = '<img src="@image_url{safe}" width="400">'
p.add_tools(HoverTool(tooltips=tooltips, renderers=[scatter]))
```

## Best Practices

1. **Use `pn.bind()` over callbacks** - cleaner, more efficient
2. **Throttle expensive updates**: `slider.param.value_throttled`
3. **Update data sources, don't recreate widgets**
4. **Cache data loading**: `@pn.cache(ttl=3600)`

## Project Structure

```
code/
├── app.py              # Entry point
├── config/             # Configuration (models.py, projects.py)
├── data/               # Data loaders with caching
├── core/               # State management (DataHolder)
├── components/         # UI components
└── utils/              # Helpers (url_state.py)
```

## Running

```bash
# Development
panel serve code/app.py --dev --show

# Production
panel serve code/app.py --allow-websocket-origin=* --port 7860
```
