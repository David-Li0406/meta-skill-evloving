# Troubleshooting Cookbook

Common errors and how to fix them.

---

## Kernel Not Found

**Problem**: `RuntimeError: Kernel 'python3' not found`

**Solution**:
```bash
# List available kernels
jupyter kernelspec list

# Install Python kernel if missing
python -m ipykernel install --user

# Or specify a different kernel
nb.py execute notebook.ipynb -k python
```

**Tip**: Kernel names are in the notebook's `metadata.kernelspec.name`. Use `inspect` to check.

---

## Execution Timeout

**Problem**: `CellTimeoutError: Timeout waiting for execute reply`

**Solution**:
```bash
# Increase timeout (default: 600 seconds)
nb.py execute notebook.ipynb -t 3600  # 1 hour

# Or execute long cell separately
nb.py execute notebook.ipynb -c 5 -t 7200  # 2 hours for cell 5
```

**Tip**: Consider breaking long-running cells into smaller chunks.

---

## Cell Execution Failed

**Problem**: Cell raises an exception, execution stops.

**Solution**:
```bash
# Continue past errors
nb.py execute notebook.ipynb --allow-errors -i

# Then inspect failures
nb.py show notebook.ipynb -o | grep -A 20 "Error:"
```

**Tip**: The error output includes the full traceback.

---

## Stale State Issues

**Problem**: Variable defined in cell 10, used in cell 5 after reordering.

**Solution**:
```bash
# Clear all outputs (resets execution order)
nb.py clear notebook.ipynb

# Execute from fresh state
nb.py execute notebook.ipynb -i
```

**Tip**: Always "Run All" to verify notebook works in order.

---

## Import Fails Only in Execution

**Problem**: Package works in terminal but fails in notebook execution.

**Solution**:
```bash
# Check which Python the kernel uses
jupyter kernelspec list --json

# Ensure package is installed in that environment
# For the python3 kernel:
python3 -m pip install missing_package

# Or use a uv-managed environment
uv pip install missing_package
```

**Tip**: The kernel's Python may differ from your shell's Python.

---

## Notebook Won't Parse

**Problem**: `JSONDecodeError: Expecting value`

**Solution**:
```bash
# Check if file is valid JSON
python -c "import json; json.load(open('notebook.ipynb'))"

# If corrupt, try to recover
# Often caused by merge conflicts - look for <<<<<<< markers
grep -n "<<<<<<" notebook.ipynb
```

**Tip**: Use `git show HEAD:notebook.ipynb > backup.ipynb` to recover last committed version.

---

## Output Too Large

**Problem**: Notebook file is huge due to large outputs (dataframes, images).

**Solution**:
```bash
# Clear outputs
nb.py clear notebook.ipynb

# Then re-execute with limited output
# In your code, use:
# df.head() instead of df
# fig.show() with limited points
```

**Tip**: Add `pd.set_option('display.max_rows', 10)` in first cell.

---

## ANSI Codes in Error Output

**Problem**: Tracebacks have unreadable escape sequences.

**Solution**:
The `nb.py show` command automatically strips ANSI codes. If you're still seeing them:

```bash
# The default output is already cleaned
nb.py show notebook.ipynb -c 5 -o

# For raw inspection with codes:
nb.py show notebook.ipynb -c 5 -o --raw
```

**Tip**: ANSI codes are for terminal colors; they're stripped for readability.

---

## Execution Hangs

**Problem**: Cell never completes, no timeout triggered.

**Solution**:
```bash
# Kill any running kernels
jupyter notebook stop 8888

# Or find and kill Python processes
ps aux | grep python | grep jupyter

# Execute with shorter timeout
nb.py execute notebook.ipynb -t 60 -c 5
```

**Tip**: Common causes: infinite loops, waiting for user input, network I/O.

---

## Permission Denied

**Problem**: `PermissionError: [Errno 13] Permission denied`

**Solution**:
```bash
# Check file permissions
ls -la notebook.ipynb

# Fix permissions
chmod 644 notebook.ipynb

# If running as different user, check ownership
chown $USER notebook.ipynb
```

**Tip**: This often happens when notebooks are copied from external sources.

---

## nbclient Not Installed

**Problem**: `ModuleNotFoundError: No module named 'nbclient'`

**Solution**:
The scripts use inline dependencies with `uv run`. If uv isn't handling deps:

```bash
# Ensure uv is installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# The shebang handles the rest automatically
nb.py execute notebook.ipynb
```

**Tip**: For the lightweight `validate.py`, only `nbformat` is needed.
