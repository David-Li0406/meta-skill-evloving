# Jupyter Reference

Conceptual information about notebook structure, execution model, and best practices.

## Notebook Structure (nbformat v4)

A `.ipynb` file is JSON with this structure:

```json
{
  "metadata": {
    "kernelspec": {"name": "python3", "display_name": "Python 3"},
    "language_info": {"name": "python", "version": "3.11"}
  },
  "nbformat": 4,
  "nbformat_minor": 5,
  "cells": [...]
}
```

### Cell Types

**Code cells:**
```json
{
  "cell_type": "code",
  "id": "unique-id",
  "source": "print('hello')",
  "metadata": {},
  "execution_count": 1,
  "outputs": [...]
}
```

**Markdown cells:**
```json
{
  "cell_type": "markdown",
  "id": "unique-id",
  "source": "# Heading",
  "metadata": {}
}
```

### Output Types

| Type | Field | Description |
|------|-------|-------------|
| `stream` | `text` | stdout/stderr output |
| `execute_result` | `data` | Return value of last expression |
| `display_data` | `data` | Explicit display (plots, HTML) |
| `error` | `ename`, `evalue`, `traceback` | Exception info |

### Data MIME Types

Common output data formats:
- `text/plain` - Text representation
- `text/html` - HTML (tables, rich output)
- `image/png` - PNG image (base64 encoded)
- `image/svg+xml` - SVG graphics
- `application/json` - JSON data

## Execution Model

### Kernel Lifecycle

1. **Start kernel** - Initialize Python interpreter
2. **Execute cells** - Run code in order, maintain state
3. **Capture outputs** - stdout, stderr, display data
4. **Store results** - Save outputs back to notebook

### Cell Execution Order

- Cells share state - variables persist across cells
- Execution order matters - earlier cells must run first
- "Restart and Run All" ensures clean state

### Common Kernel Names

| Name | Description |
|------|-------------|
| `python3` | Default Python 3 kernel |
| `python` | May be Python 2 or 3 |
| `ir` | R kernel |
| `julia-1.9` | Julia kernel |

## Best Practices

### For Clean Notebooks

1. **Clear outputs before commit** - Keeps diffs manageable
2. **Restart kernel regularly** - Avoid hidden state bugs
3. **Run all cells in order** - Verify notebook works end-to-end
4. **Use markdown headers** - Structure for navigation

### For Reproducibility

1. **Pin dependencies** - Include requirements in first cell
2. **Set random seeds** - For reproducible results
3. **Avoid external state** - Don't depend on prior runs
4. **Document assumptions** - Explain data sources

### Cell Granularity

| Good | Bad |
|------|-----|
| One concept per cell | Giant cells with many operations |
| Imports in first cell | Imports scattered throughout |
| Markdown before code | Code without explanation |
| Small, testable units | Monolithic scripts |

## Anti-Patterns

### State Confusion

```python
# Cell 1
x = 10

# Cell 2
print(x)  # Works if Cell 1 ran

# Cell 3 (user runs this first)
y = x + 1  # NameError: x not defined
```

**Fix:** Restart kernel and "Run All" to verify order-independence.

### Hidden State

```python
# Cell 1
data = load_data()  # Takes 5 minutes

# Cell 2 (modified)
result = process(data)  # Uses stale 'data' from old Cell 1
```

**Fix:** Re-run upstream cells after modifications.

### Output Bloat

```python
# Avoid: Giant outputs that inflate notebook size
df  # Displays entire dataframe

# Better: Limit output
df.head()
df.describe()
```

## Cell Addressing

### By Index (0-based)

```bash
# Show cell 0
uv run nb.py show notebook.ipynb -c 0

# Show cells 2, 3, 4
uv run nb.py show notebook.ipynb -c 2-4

# Show cells 0, 5, 10
uv run nb.py show notebook.ipynb -c 0,5,10
```

### By Cell ID

Each cell has a unique `id` field. Use with `NotebookEdit`:

```python
# NotebookEdit parameters
cell_id = "abc123"  # Targets specific cell
```

## Kernel Management

### Timeout Handling

Long-running cells may timeout. Adjust with `-t`:

```bash
# 10-minute timeout (default: 600s)
uv run nb.py execute notebook.ipynb -t 600

# 1-hour timeout for ML training
uv run nb.py execute notebook.ipynb -t 3600
```

### Kernel Selection

Force a specific kernel:

```bash
uv run nb.py execute notebook.ipynb -k python3
uv run nb.py execute notebook.ipynb -k ir  # R kernel
```

### Error Handling

Continue past failing cells:

```bash
uv run nb.py execute notebook.ipynb --allow-errors
```

## Output Interpretation

### Stream Output

```json
{"output_type": "stream", "name": "stdout", "text": "Hello\n"}
```
Displayed as plain text.

### Execute Result

```json
{
  "output_type": "execute_result",
  "data": {
    "text/plain": "42",
    "text/html": "<b>42</b>"
  }
}
```
`text/plain` shown by default. Use `--raw` for full data.

### Error Output

```json
{
  "output_type": "error",
  "ename": "ValueError",
  "evalue": "invalid literal",
  "traceback": ["..."]
}
```
Traceback is displayed with ANSI codes stripped.
