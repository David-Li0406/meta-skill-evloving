# Notebooks

This directory contains Jupyter notebooks for interactive development and exploration of the cmm-ai-automation package.

## Getting Started

### Starting JupyterLab

From the project root, run:

```bash
uv run jupyter lab notebooks/
```

Or to start from the current directory:

```bash
cd notebooks
uv run jupyter lab
```

### Starting Classic Jupyter Notebook

```bash
uv run jupyter notebook notebooks/
```

### Using with Just

You can also add a justfile target for convenience (optional).

## Tips

- The `example.ipynb` notebook provides a starting template
- All notebook checkpoints (`.ipynb_checkpoints/`) are already gitignored
- Use relative paths from notebooks to access data: `../data/`
- The package is installed in editable mode, so changes to source code are automatically available
