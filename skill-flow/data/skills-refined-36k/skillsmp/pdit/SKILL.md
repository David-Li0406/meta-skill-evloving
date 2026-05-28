---
name: pdit
description: "Collaborate with users running pdit, an interactive Python editor with inline execution results. Use when user mentions pdit, runs 'uv run pdit', or is doing collaborative Python development where they see live execution output in a browser."
---

# pdit Collaboration

pdit is an interactive Python editor with inline execution results. The user sees a browser-based
split-pane interface: code editor (left) and streaming execution results (right).

## User's Environment

**Starting pdit:**

pdit runs using `uv run --with` so it's available without modifying the project:

```bash
uv run --with git+https://github.com/vangberg/pdit@dist pdit script.py
```

**Note:** The `@dist` branch contains pre-built frontend assets, so no Node.js or build step is needed.

**Upgrading pdit:**

Since pdit is run with `--with`, it will fetch the latest version each time. To force a fresh fetch:

```bash
uv cache clean pdit
```

**IMPORTANT: Run with `run_in_background: true` in the Bash tool so you can continue editing.**

Options:

- `--port 9000` - Use different port (default: 8888)
- `--no-browser` - Don't auto-open browser

Server runs on `localhost:8888`, browser opens automatically.

**Exporting to HTML:**

```bash
uv run --with git+https://github.com/vangberg/pdit@dist pdit --export script.py
```

This executes the script and generates `script.html` - a self-contained HTML file that can be opened in any browser without a server.

**What the user sees:**

- Left pane: CodeMirror Python editor with syntax highlighting
- Right pane: Execution results grouped by source lines
- Top bar: RUN CURRENT, RUN ALL, SAVE buttons

**User shortcuts:**
| Action | Mac | Windows/Linux |
|--------|-----|---------------|
| Execute selection/current | Cmd+Enter | Ctrl+Enter |
| Execute all | Cmd+Shift+Enter | Ctrl+Shift+Enter |
| Save | Cmd+S | Ctrl+S |

## Code Style

**Write simple, top-level exploratory code** - like a Jupyter notebook, not a production module.

- Prefer flat, sequential statements over functions and classes
- Each line/expression shows its result inline - take advantage of this
- Avoid unnecessary abstractions, loops, or defensive code
- Focus on data exploration: load, inspect, transform, visualize

```python
import pandas as pd

df = pd.read_csv("data.csv")
df.head()
df.shape
df.describe()
df["price"].mean()
df[df["price"] > 100]
```

## Execution Model

- **Stateful**: Variables persist across executions (like Jupyter kernel)
- **Streaming**: Results appear as each statement completes via SSE
- **Line-grouped**: Results display next to the code that produced them
- **Reset**: User can reset namespace to clear all variables

## Collaboration Workflow

**File watching enabled**: When you edit the Python file, changes appear
in the user's editor automatically.

**Validate before the user sees it:**

- Run the script yourself with `uv run script.py` before presenting to user
- Fix any errors or warnings so output is clean
- User should see working code, not debug your mistakes

**Recommended workflow:**

1. Write/edit the `.py` file
2. Run `uv run script.py` to validate - fix any errors
3. User sees clean code and runs with Cmd+Enter

**When user shares output:**

- Results show stdout, stderr, and expression values
- Errors include full tracebacks
- Results are associated with specific line ranges

## API (if needed)

```
POST /api/execute-script  - Execute code (SSE streaming)
POST /api/reset           - Reset namespace
GET  /api/read-file       - Read file from disk
POST /api/save-file       - Save file to disk
GET  /api/health          - Health check
```

## Markdown Cells

pdit supports markdown cells for documentation and explanations in top-level docstring

```python
"""
# Data Analysis
This section loads and explores the dataset
"""

import pandas as pd
df = pd.read_csv("data.csv")
df.head()

"""
## Summary Statistics
Let's look at the distribution of values
"""

df.describe()
```

**Usage:**

- Start with a triple-quoted docstring (`"""..."""`) containing markdown
- Content is rendered as markdown in the output pane
- Supports standard markdown: headers, lists, links, code blocks, etc.
- Great for documenting analysis steps and explaining results

## Matplotlib Plots

**IMPORTANT:** Always wrap matplotlib plotting code in a `plt.ioff()` context manager:

```python
import matplotlib.pyplot as plt

with plt.ioff():
    plt.plot([1, 2, 3], [1, 4, 9])
    plt.title("My Plot")
    plt.show()  # ✅ Standard matplotlib display
```

**Key points:**

- Use `with plt.ioff():` to disable interactive mode
- Use standard `plt.show()` to display plots
- Plots appear inline in the output pane automatically
- The context manager prevents interactive mode issues while capturing plots

## Output Suppression

Append `;` to any expression to suppress its output (iPython/Jupyter convention):

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5));  # Suppressed - no <Figure> output
plt.plot([1, 2, 3], [1, 4, 9])
plt.title("My Plot");  # Suppressed - no Text object output
plt.gca()  # Shows the plot
```

**Works with:**
- Any expression: `expensive_calc();`
- Trailing comments: `plt.figure(); # setup`
- DataFrames, plots, and regular values

**Does not affect:**
- Markdown cells (explicit documentation)
- `print()` statements (stdout is always captured)

## Output Types & Rich Display

pdit renders different output types with appropriate visualizations:

| Badge | Type | Description |
|-------|------|-------------|
| >>> | stdout | print() output |
| err | stderr | Error/warning output |
| !!! | error | Exceptions with traceback |
| md | markdown | Rendered markdown from docstrings |
| df | dataframe | Interactive table (pagination, sort, filter) |
| fig | image | Matplotlib figures |
| htm | html | Rich HTML from _repr_html_() |

### DataFrames

Pandas and Polars DataFrames render as interactive TanStack tables:

```python
import pandas as pd
df = pd.read_csv("sales.csv")
df  # Interactive table with pagination, sorting, filtering
```

### Rich HTML Display (`_repr_html_`)

Objects with a `_repr_html_()` method render as rich HTML. Many libraries support this:

**Plotly** - Interactive charts:
```python
import plotly.express as px
fig = px.scatter(df, x="price", y="sales")
fig  # Interactive Plotly chart
```

**Great Tables** - Formatted tables:
```python
from great_tables import GT
GT(df).fmt_currency("price").fmt_percent("margin")
```

**pandas Styler** - Conditional formatting:
```python
df.style.format({"price": "${:.2f}"}).background_gradient(subset=["sales"])
```

### Custom HTML Widgets

Create your own rich displays by implementing `_repr_html_()`:

```python
class MetricCard:
    def __init__(self, title, value, color="#667eea"):
        self.title = title
        self.value = value
        self.color = color

    def _repr_html_(self):
        return f'''
        <div style="background:{self.color}; padding:16px; border-radius:8px; color:white;">
            <div style="font-size:24px; font-weight:bold;">{self.value}</div>
            <div style="opacity:0.8;">{self.title}</div>
        </div>
        '''

MetricCard("Total Revenue", "$1,234,567")  # Renders as styled card
```

This pattern is powerful for building dashboards and custom visualizations.

## Tips

- Expressions show their values inline - `print()` is rarely needed
- Write intermediate expressions to see values: `df.shape` instead of `print(df.shape)`
- Long-running code streams results as each statement completes
- User has full filesystem and package access (local Python execution)
- Use docstring-style markdown cells to document your analysis
- Always wrap matplotlib plotting code in `with plt.ioff():` and use `plt.show()`
- Use `;` to suppress unwanted output like `plt.figure()` return values

## Dependencies

Since pdit runs from the local uv environment, add packages with `uv add`:

```bash
uv add pandas matplotlib
```

No server restart needed - packages are available immediately in both pdit and `uv run` validation.
