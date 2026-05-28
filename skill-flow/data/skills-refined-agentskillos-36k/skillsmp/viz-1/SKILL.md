---
name: viz
description: Data visualization and inspection skill. Use for (1) creating matplotlib/seaborn plots from data files or marimo notebooks, or (2) inspecting DataFrames by showing first N rows, column names, and dtypes. For plots, provide chart type, data context, and styling. For inspection, ask to "show" or "display" the data.
allowed-tools: Read, Glob(/tmp/viz/*), Grep(/tmp/viz/*), Bash(python {SKILL_DIR}/scripts/viz_runner.py:*)
---

# Viz Skill: Data Visualization and Inspection

## Purpose

This skill **directly executes** visualizations. The calling agent provides a visualization spec along with data context, and the skill:
1. Infers the data loading code from the provided context
2. Generates the complete plotting script
3. Executes it via the `viz_runner.py` helper
4. Returns artifact paths for the caller to reference

**Key pattern:**
```
Caller (with data context) → Skill (infers data loading, generates script, executes) → Plot appears
```

The caller does NOT need to write any execution code. The skill handles everything.

## Input Specification

The calling agent should provide:

### Required
- **Visualization spec**: What to plot (chart type, axes, title, special features)

### Data Context (one of these forms)
- **Database + query**: "Data from `/full/path/to/operational_forecast.ddb`, table `forecast`, columns month, members"
- **SQL query**: "Run this SQL: `SELECT * FROM forecast WHERE year >= 2024`"
- **Code snippet**: "Load data like this: `df = pd.read_parquet('/full/path/to/data.parquet')`"
- **File path**: "CSV at `/tmp/data.csv` with columns X, Y, Z"

**CRITICAL: Absolute Paths Required**

The viz_runner.py executes scripts from `/tmp/viz/`, NOT the caller's working directory. All file paths in generated scripts MUST be absolute paths. The calling agent should:
1. Determine the absolute path to any data files before invoking the skill
2. Pass the full absolute path in the data context
3. Never use relative paths like `./data.ddb` or `data.parquet`

Example - WRONG:
```python
con = duckdb.connect('operational_forecast.ddb')  # Will fail!
```

Example - CORRECT:
```python
con = duckdb.connect('/Users/rob/projects/forecast/operational_forecast.ddb')
```

### Optional
- **Suggested ID**: A name hint (e.g., `pop_bar`, `churn_trend`). The runner ensures uniqueness.

## Intent Detection

**Before generating any code, analyze the user's request to determine the appropriate mode.**

### Inspection Mode (use `--show`)
Use when the user wants to **see the data itself**, not a visualization:
- "Show me the dataframe"
- "Display the first N rows"
- "What does the data look like?"
- "Print the data"
- "What columns are in X?"
- "Inspect the data"
- "Let me see the data"

**Action:** Use `--show` flag. Do NOT generate plot code.

### Visualization Mode (generate plot)
Use when the user wants a **chart, graph, or visual representation**:
- "Plot the data"
- "Create a chart of..."
- "Visualize the trend"
- "Show a graph of..."
- "Bar chart showing..."
- "Scatter plot of..."

**Action:** Generate matplotlib/seaborn code and pass via stdin.

### Ambiguous Requests
If unclear (e.g., "show me X over time"), **default to asking** or interpret based on context:
- If the request mentions chart types (bar, line, scatter) → visualization
- If the request is about structure/columns/rows → inspection
- When in doubt, use `--show` first (it's cheaper), then offer to plot

## Artifact Management

All artifacts are managed in `/tmp/viz/` via the helper script.

### Helper: `viz_runner.py`

```bash
python {SKILL_DIR}/scripts/viz_runner.py [--id NAME] [--desc "Description"] << 'EOF'
<generated script>
EOF
```

The runner:
1. Creates `/tmp/viz/` if needed
2. Ensures ID uniqueness (appends `_2`, `_3`, etc. if collision)
3. Injects `plt.savefig('/tmp/viz/<id>.png', dpi=150, bbox_inches='tight')` before `plt.show()`
4. Writes the script to `/tmp/viz/<id>.py`
5. Executes the script
6. Writes metadata to `/tmp/viz/<id>.json`
7. Prints human-readable results to stdout

### Output Format

Terminal output:
```
Plot: pop_bar
  "Bar chart of members by month"
  png: /tmp/viz/pop_bar.png
```

Sidecar JSON (`/tmp/viz/<id>.json`):
```json
{
  "id": "pop_bar",
  "desc": "Bar chart of members by month",
  "png": "/tmp/viz/pop_bar.png",
  "script": "/tmp/viz/pop_bar.py",
  "created": "2025-01-22T11:31:00",
  "pid": 46368
}
```

The caller can then:
- Read the PNG into context to discuss the plot
- Reference the script for modifications
- Look up plots by ID or description via the JSON metadata

### List

To see all available visualizations:

```bash
python {SKILL_DIR}/scripts/viz_runner.py --list
```

Output:
```
ID              Description                          Created
--------------  -----------------------------------  ----------------
pop_bar         Bar chart of members by month        2025-01-22 11:31
churn_trend     Monthly churn rate                   2025-01-22 10:45
test_scatter    -                                    2025-01-22 09:20
```

### Cleanup

To remove all visualization files from `/tmp/viz/`:

```bash
python {SKILL_DIR}/scripts/viz_runner.py --clean
```

Output:
```
Cleaned 12 files from /tmp/viz
```

## Skill Workflow

1. **Infer data loading**: From the provided context, generate Python code to load/create the DataFrame. **Use absolute paths for all file references** - the script runs from `/tmp/viz/`, not the caller's directory.
2. **Generate visualization**: Add matplotlib/seaborn code for the requested plot
3. **Execute via runner** (always include `--desc` with a short summary):
   ```bash
   python {SKILL_DIR}/scripts/viz_runner.py --id suggested_name --desc "Short description of plot" << 'EOF'
   <complete script>
   EOF
   ```
4. **Parse output**: Capture the ID and paths from stdout
5. **Return to caller**: Report final ID and paths. Do NOT read the PNG into context unless the user needs analysis.

## Library Selection

### Use Seaborn When:
- Statistical distributions (histogram + KDE, violin, box plots)
- Regression with confidence intervals
- Categorical comparisons with error bars
- Heatmaps and correlation matrices

### Use Matplotlib When:
- Fine-grained control over appearance
- Time series with date formatting
- Custom annotations and reference lines
- Simple plots without statistical features

### Combine Both:
Use seaborn for the statistical plot, matplotlib for customizations like reference lines.

## Publication Quality Standards

- **Labels**: Descriptive axis labels with units, 12pt+ font
- **Titles**: Clear, informative, 14pt+ font
- **Figure size**: `figsize=(10, 6)` or appropriate aspect ratio
- **Layout**: Always use `tight_layout()` to prevent clipping
- **Grids**: Subtle guidance with `alpha=0.3`
- **Colors**: Colorblind-friendly palettes (viridis, coolwarm, Set2)
- **Transparency**: Alpha for overlapping points
- **Imports**: Inside the script for self-contained execution

## End-to-End Example

**Request from caller:**
```
/viz id=pop_bar
     bar chart showing total_initial_members and total_final_members by month
     with dashed vertical line at history/forecast boundary (Dec 2025 / Jan 2026).
     Data from operational_forecast.ddb, forecast table.
```

**Skill generates and executes:**
```bash
python {SKILL_DIR}/scripts/viz_runner.py --id pop_bar --desc "Bar chart of members by month with forecast boundary" << 'EOF'
import duckdb
import matplotlib.pyplot as plt
import numpy as np

# Load data from DuckDB (MUST use absolute path!)
con = duckdb.connect('/Users/rob/projects/forecast/operational_forecast.ddb', read_only=True)
df = con.execute("""
    SELECT month, total_initial_members, total_final_members
    FROM forecast
    ORDER BY month
""").df()
con.close()

# Create grouped bar chart
fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(df))
width = 0.35

bars1 = ax.bar(x - width/2, df['total_initial_members'], width, label='Initial Members', color='steelblue')
bars2 = ax.bar(x + width/2, df['total_final_members'], width, label='Final Members', color='coral')

# History/forecast boundary
boundary_idx = df[df['month'] == '2025-12'].index[0] + 0.5
ax.axvline(x=boundary_idx, color='gray', linestyle='--', linewidth=1.5, label='Forecast Start')

ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Members', fontsize=12)
ax.set_title('Member Population by Month: Historical vs Forecast', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(df['month'], rotation=45, ha='right')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.show()
EOF
```

**Runner output:**
```
Plot: pop_bar
  "Bar chart of members by month with forecast boundary"
  png: /tmp/viz/pop_bar.png
```

**Skill returns to caller:**
> Plot generated successfully.
> - ID: `pop_bar`
> - Script: `/tmp/viz/pop_bar.py`
> - PNG: `/tmp/viz/pop_bar.png`

## Important: Do NOT Auto-Read PNGs

**Do NOT automatically read the PNG into context after generating a plot.**

Reading images consumes significant context tokens and is usually unnecessary. The plot window opens automatically via `plt.show()`, so the user can already see the visualization.

**Only read the PNG into context when:**
- The user explicitly asks you to analyze or interpret the graph
- The user asks questions about what the graph shows
- You need to learn something from the visual output to answer a question

**Instead of reading the PNG, offer to open it:**
```bash
open /tmp/viz/pop_bar.png  # macOS
```

This displays the image in the system viewer without consuming context tokens.

## Refinement Workflow

When refining an existing plot:

1. Caller provides the existing script path + requested changes
2. Skill reads the script, applies modifications
3. Executes with a new ID (e.g., `pop_bar_2`)
4. Both versions remain available for comparison

## Regeneration

When a user asks to regenerate an existing plot (e.g., after data has changed):

### By ID
Request: "regenerate pop_bar"

Run the saved script directly:
```bash
python /tmp/viz/pop_bar.py
```

The script already contains the hardcoded savefig path, so it overwrites the existing PNG.

### By Description
Request: "regenerate the churn plot"

1. Run `--list` to find matching plot
2. Identify the ID from the description
3. Run `python /tmp/viz/<id>.py`

### Ambiguous Request
Request: "regenerate a plot"

1. Run `--list` to show available plots
2. Ask user which one to regenerate
3. Run the selected script

### Key Point
Regeneration does NOT require `viz_runner.py` - the saved `.py` scripts are self-contained and can be executed directly with `python`.

## Interactive Backend Note

Generated scripts use `plt.show()` which works with the `macosx` backend for interactive display. The injected `savefig()` ensures a PNG copy is always saved before display.

## Marimo Notebook Support

The viz skill can extract data from marimo notebooks and generate plots without modifying the original notebook.

### How It Works

1. **Copy notebook** to `/tmp/viz/<id>.py`
2. **Analyze dependencies** to identify cells needed for target data
3. **Prune unneeded cells** from the copied notebook
4. **Inject plotting code** as a new cell at the end
5. **Execute via subprocess** with `cwd` set to original notebook's directory (so relative paths work)

### CLI Interface

```bash
python {SKILL_DIR}/scripts/viz_runner.py \
    --marimo \
    --notebook /path/to/notebook.nb.py \
    --target-var df_forecast \
    --id forecast_plot \
    --desc "Monthly forecast visualization" \
    << 'EOF'
# Plotting code that uses df_forecast
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(df_forecast['date'], df_forecast['total_final_members'])
plt.show()
EOF
```

### Parameters

- `--marimo`: Enable marimo notebook mode (required)
- `--notebook`: Path to the marimo notebook file (required)
- `--target-var`: Variable to extract from the notebook (required)
- `--target-line`: Optional line number for capturing intermediate state (for mutated variables)
- `--id`: Suggested ID for the visualization (optional)
- `--desc`: Description of the visualization (optional)
- `--show`: Show mode - print dataframe info to console instead of plotting (no stdin required)
- `--rows`: Number of rows to display in show mode (default: 5)

### Dependency Analysis

Marimo notebooks encode dependencies explicitly:
- Cell parameters = variables the cell **reads** (refs)
- Cell return tuple = variables the cell **defines** (defs)

The skill walks backwards from the target variable through the dependency graph to find all required cells.

### Target Line (Advanced)

When a variable is mutated within a cell, use `--target-line` to capture intermediate state:

```python
@app.cell
def _(raw_data):
    df = raw_data.copy()           # line 45
    df = df[df['value'] > 0]       # line 46 - filtered
    df = df.groupby('cat').sum()   # line 47 - aggregated
    return (df,)
```

Use `--target-var df --target-line 46` to capture `df` after filtering but before aggregation.

### Show Mode (Data Inspection)

Use `--show` to print dataframe info to console instead of generating a plot. Useful for quickly inspecting data at a specific point in the notebook pipeline.

```bash
python {SKILL_DIR}/scripts/viz_runner.py \
    --marimo \
    --notebook /path/to/notebook.nb.py \
    --target-var df \
    --show \
    --rows 10
```

Output:
```
Shape: (12345, 5)
Columns: ['date', 'profile_id', 'kind', 'state', 'channel_type']

Dtypes:
date              datetime64[ns]
profile_id                 int64
kind                      object
state                     object
channel_type              object

First 10 rows:
        date  profile_id     kind state channel_type
0 2021-01-01      123456  monthly    CA      organic
1 2021-01-02      123457  monthly    TX         paid
...
```

No stdin (plot code) is required for show mode - it only prints dataframe metadata and contents.

### Example Workflow

**User request:**
> "Plot the member forecast over time from the operational forecast notebook"

**Agent workflow:**
1. Read the notebook to identify candidate variables
2. Ask clarifying questions if multiple candidates exist
3. Execute:

```bash
python {SKILL_DIR}/scripts/viz_runner.py \
    --marimo \
    --notebook /Users/rob/repos/project/forecast.nb.py \
    --target-var df_deliverable \
    --id member_forecast \
    --desc "Historical and forecast members" \
    << 'EOF'
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df_deliverable['date'], df_deliverable['total_final_members'])
ax.set_xlabel('Date')
ax.set_ylabel('Members')
ax.set_title('Member Population Over Time')
plt.tight_layout()
plt.show()
EOF
```

### Important Notes

- The **original notebook is never modified** (read-only access)
- All work happens on a copy in `/tmp/viz/`
- The script runs with the notebook's directory as cwd, so relative file paths work
- Uses `uv run python` if the notebook directory contains `pyproject.toml` or `uv.lock`
