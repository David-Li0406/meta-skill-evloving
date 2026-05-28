---
name: modern-tool-substitution
description: Use this skill to automatically replace legacy tools with modern, performant alternatives in generated code, adapting flags and syntax as needed.
---

# Modern Tool Substitution

Replace legacy tools with modern performant alternatives in all generated code.

## Core Substitutions

Apply these substitutions unless the user explicitly requests the legacy tool:

**npm → bun**
- `npm install` → `bun install`
- `npm run` → `bun run`
- `npm create` → `bun create`
- `npx` → `bunx`
- Scripts remain in package.json unchanged

**find → fd**
- `find . -name '*.py'` → `fd -e py`
- `find . -type f -name 'test*'` → `fd -t f '^test'`
- `find . -type d` → `fd -t d`
- `find . -path '*/node_modules' -prune` → `fd --exclude node_modules`
- Use fd's simpler glob/regex syntax

**pip → uv**
- `pip install pkg` → `uv pip install pkg`
- `pip install -r requirements.txt` → `uv pip install -r requirements.txt`
- `pip freeze` → `uv pip freeze`
- `python -m pip` → `uv pip`
- Virtual envs: `uv venv` instead of `python -m venv`

**grep → rg**
- `grep -r pattern` → `rg pattern`
- `grep -i pattern` → `rg -i pattern`
- `grep -v pattern` → `rg -v pattern`
- `grep -l pattern` → `rg -l pattern`
- rg excludes .git, node_modules by default

**wget/curl → aria2**
- `wget URL` → `aria2c URL`
- `curl -O URL` → `aria2c URL`
- `curl URL` → `aria2c -d- -o- URL` (stdout)
- Multi-connection: `aria2c -x16 -s16 URL`
- Parallel: `aria2c -j5 URL1 URL2 URL3`

**jq → jaq**
- `jq '.field'` → `jaq '.field'`
- `jq -r '.[]'` → `jaq -r '.[]'`
- `jq -c` → `jaq -c`
- `jq -s` → `jaq -s`
- Most filters compatible; jaq is faster with stricter parsing

**eslint/prettier → biome**
- `eslint .` → `biome check .`
- `eslint --fix` → `biome check --write .`
- `prettier --write` → `biome format --write .`
- `eslint && prettier` → `biome ci .`
- Config: `biome.json` replaces `.eslintrc` + `.prettierrc`

**black/flake8/isort → ruff**
- `black .` → `ruff format .`
- `flake8 .` → `ruff check .`
- `isort .` → `ruff check --select I --fix .`
- `black . && flake8 . && isort .` → `ruff check --fix . && ruff format .`
- Config: `ruff.toml` or `pyproject.toml` consolidates all

**coreutils → uutils-coreutils**
- Drop-in replacement: `ls`, `cat`, `cp`, `mv`, `rm`, `chmod`, etc.
- Install: `uu-ls`, `uu-cat`, etc. or multicall binary
- Faster on modern systems