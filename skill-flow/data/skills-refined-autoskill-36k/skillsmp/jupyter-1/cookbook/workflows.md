# Workflows Cookbook

Common notebook workflows and recipes.

---

## Full Edit-Execute-Verify Cycle

**Problem**: Need to edit code, run it, and verify outputs without switching to browser.

**Solution**:
```bash
# 1. Inspect current state
nb.py inspect notebook.ipynb

# 2. Edit cell (use NotebookEdit tool in Claude)

# 3. Execute and save outputs
nb.py execute notebook.ipynb -i

# 4. View outputs
nb.py show notebook.ipynb --output-only

# 5. If errors, check specific cell
nb.py show notebook.ipynb -c 5 -o
```

**Tip**: Use `-i` (in-place) to save outputs back to the file for persistence.

---

## Execute Specific Cell Range

**Problem**: Only want to run cells 3-7 after editing one of them.

**Solution**:
```bash
# Execute cells 3 through 7
nb.py execute notebook.ipynb -c 3-7 -i

# View just those outputs
nb.py show notebook.ipynb -c 3-7 --output-only
```

**Tip**: Cell indices are 0-based. Use `inspect` to see the cell list first.

---

## Prepare Notebook for Git Commit

**Problem**: Want to commit notebook without bloated outputs.

**Solution**:
```bash
# Validate syntax
validate.py notebook.ipynb

# Clear all outputs
nb.py clear notebook.ipynb

# Now safe to commit
git add notebook.ipynb
```

**Tip**: Consider adding a pre-commit hook that runs `clear` automatically.

---

## Convert Notebook to Python Script

**Problem**: Want to extract pure Python code for production use.

**Solution**:
```bash
# Convert to .py file
nb.py convert notebook.ipynb --to py -o script.py
```

**Tip**: The output includes cell markers as comments for reference.

---

## Generate HTML Report

**Problem**: Need to share notebook as static HTML.

**Solution**:
```bash
# First ensure outputs are current
nb.py execute notebook.ipynb -i

# Then convert to HTML
nb.py convert notebook.ipynb --to html -o report.html
```

**Tip**: For PDF, use `--to pdf` but requires additional system dependencies.

---

## Debug Import Errors

**Problem**: Notebook fails on imports, need to identify missing packages.

**Solution**:
```bash
# Execute just the import cells
nb.py execute notebook.ipynb -c 0-2 --allow-errors

# Check the error
nb.py show notebook.ipynb -c 0-2 -o
```

**Tip**: The error output will show `ModuleNotFoundError` with the missing package name.

---

## Incremental Execution

**Problem**: Notebook takes long to run, want to execute incrementally.

**Solution**:
```bash
# Execute in batches
nb.py execute notebook.ipynb -c 0-5 -i
nb.py show notebook.ipynb -c 5 -o

# If good, continue
nb.py execute notebook.ipynb -c 6-10 -i
nb.py show notebook.ipynb -c 10 -o
```

**Tip**: Use `--allow-errors` if you want to continue past failures.

---

## Extract Code from Notebook

**Problem**: Want to see only the code cells, not markdown.

**Solution**:
```bash
# Show only code cells
nb.py show notebook.ipynb -t code
```

**Tip**: Use `-t markdown` to show only markdown cells.

---

## Check Notebook Health

**Problem**: Want to verify notebook is well-formed before sharing.

**Solution**:
```bash
# Quick syntax validation
validate.py notebook.ipynb

# Check if all cells have been executed
validate.py notebook.ipynb --require-outputs
```

**Tip**: Fix syntax errors before execution to avoid cryptic kernel errors.

---

## View Raw Output Data

**Problem**: Need to see the actual JSON structure of outputs (for debugging display issues).

**Solution**:
```bash
# Show raw output data
nb.py show notebook.ipynb -c 5 -o --raw
```

**Tip**: Raw mode shows the full MIME type data including base64-encoded images.

---

## Find Cells Containing Pattern

**Problem**: Need to find which cells define a function or import a specific module.

**Solution**:
```bash
# Find cells importing pandas
nb.py grep "import pandas" notebook.ipynb

# Find function definitions (case-insensitive regex)
nb.py grep -i "def.*process" notebook.ipynb

# Show full cell context around matches
nb.py grep -C "class.*Model" notebook.ipynb

# Get just cell indices (for piping to execute)
nb.py grep --cells-only "TODO" notebook.ipynb
```

**Tip**: Use `--cells-only` output with `-c` flag: `nb.py execute notebook.ipynb -c $(nb.py grep --cells-only "import" notebook.ipynb)`

---

## Extract Images from Notebook

**Problem**: Need to save matplotlib plots or other images from notebook outputs.

**Solution**:
```bash
# Save all images from outputs to a directory
nb.py show notebook.ipynb -o --save-images ./images/

# Save images after executing
nb.py execute notebook.ipynb --save-images ./outputs/

# Extract images from specific cells only
nb.py show notebook.ipynb -c 5,10-12 -o --save-images ./figures/
```

**Tip**: Images are saved as `cell_N_output_M.png` (or `.jpg`, `.svg`). Supports PNG, JPEG, and SVG formats.
