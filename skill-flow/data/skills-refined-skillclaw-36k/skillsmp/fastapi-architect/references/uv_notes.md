# uv Notes (reference)

Common workflow:
- `uv sync` to create/update the environment from `pyproject.toml` (and lock when applicable).
- `uv add <pkg>` to add dependencies.
- `uv run <cmd>` to run commands in the managed environment.

Docker pattern:
- Copy `pyproject.toml` (+ `uv.lock` if present).
- `uv sync --frozen --no-install-project` for caching layers.
