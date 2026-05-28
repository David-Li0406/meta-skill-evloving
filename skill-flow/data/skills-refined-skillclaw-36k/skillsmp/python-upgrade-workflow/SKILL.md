---
name: python-upgrade-workflow
description: Step-by-step workflow for safely upgrading Python dependencies using major package managers (uv, poetry, pipenv, pip).
---

# Workflow: `python-upgrade-workflow`

This skill guides you through the process of safely upgrading Python dependencies. It automatically detects the package manager in use (`uv`, `poetry`, `pipenv`, or `pip`) and provides specific steps for each.

## Prerequisites

Before starting, ensure:

- [ ] The relevant package manager is installed and available in the PATH (`uv`, `poetry`, `pipenv`, or `pip`).
- [ ] A dependency definition file exists (`pyproject.toml`, `Pipfile`, or `requirements.txt`).
- [ ] A test suite (e.g., `pytest`) is configured and passing in the current state.

## Steps

### 1. Preparation & Detection

1.  **Detect Package Manager**:
    - Check for lockfiles/definition files to identify the tool:
      - `uv.lock` -> **uv**
      - `poetry.lock` or `[tool.poetry]` in `pyproject.toml` -> **poetry**
      - `Pipfile.lock` or `Pipfile` -> **pipenv**
      - `requirements.txt` -> **pip**
    - _Note_: If multiple exist, prefer the one with a lockfile or strictly follow the project's contribution guidelines.

2.  **Health Check (Baseline)**:
    - **uv**: `uv lock --check`
    - **poetry**: `poetry check`
    - **pipenv**: `pipenv check`
    - **pip**: `pip check`
    - **All**: Run the test suite (e.g., `pytest`) to confirm tests pass before any changes.
    - _Verification_: Do not proceed if the baseline is broken.

3.  **Back up Lockfile**:
    - **uv**: `cp uv.lock uv.lock.bak`
    - **poetry**: `cp poetry.lock poetry.lock.bak`
    - **pipenv**: `cp Pipfile.lock Pipfile.lock.bak`
    - **pip**: `cp requirements.txt requirements.txt.bak`
    - _Verification_: Check that the backup file exists.

### 2. Execution (Upgrade)

Choose **Option A** (Full Upgrade) or **Option B** (Targeted Upgrade).

#### Option A: Full Upgrade (All dependencies)

- **uv**:
  - Run `uv lock --upgrade`
  - Run `uv sync`
- **poetry**:
  - Run `poetry update`
- **pipenv**:
  - Run `pipenv update`
- **pip**:
  - Run `pip list --outdated --format=freeze` to see what will be upgraded.
  - Run `pip install --upgrade -r requirements.txt` (if packages are unpinned) OR upgrade packages individually.
  - Run `pip freeze > requirements.txt`
  - _Warning_: `pip freeze` usually removes comments from `requirements.txt`.

#### Option B: Targeted Upgrade (Specific package)

Replace `<package_name>` with the desired package.

- **uv**:
  - Run `uv lock --upgrade-package <package_name>`
  - Run `uv sync`
- **poetry**:
  - Run `poetry update <package_name>`
- **pipenv**:
  - Run `pipenv update <package_name>`
- **pip**:
  - Run `pip install --upgrade <package_name>`
  - Run `pip freeze > requirements.txt`

_Verification_: Check that the lockfile (or `requirements.txt`) has been modified.

### 3. Validation & Inspection

1.  **Consistency Check**:
    - **uv**: `uv lock --check`
    - **poetry**: `poetry check`
    - **pipenv**: `pipenv check`
    - **pip**: `pip check`

2.  **Inspect Changes**:
    - **uv**: `uv tree --depth 1`
    - **poetry**: `poetry show --tree` (or just `poetry show`)
    - **pipenv**: `pipenv graph`
    - **pip**: `pip freeze` (compare with backup)

3.  **Run Tests**:
    - Run the test suite again.
    - _Verification_: Ensure all tests pass with the upgraded dependencies.

### 4. Finalization

1.  **Cleanup**:
    - If tests pass, remove the backup: `rm <lockfile>.bak`.
    - _Verification_: Backup file is removed.

2.  **Commit Changes**:
    - Commit the lockfile and definition file (e.g., `uv.lock` & `pyproject.toml`, `poetry.lock` & `pyproject.toml`, etc.).
    - Message suggestion: "chore(deps): upgrade dependencies" or "chore(deps): upgrade <package_name>"

## Rollback / Failure Handling

If validation fails:

1.  **Restore Lockfile**:
    - `mv <lockfile>.bak <lockfile>` (e.g., `mv uv.lock.bak uv.lock`)
2.  **Sync Environment** (Restore original state):
    - **uv**: `uv sync`
    - **poetry**: `poetry install`
    - **pipenv**: `pipenv sync`
    - **pip**: `pip install -r requirements.txt`
3.  **Report Failure**:
    - Provide test failure logs.
    - List attempted upgrades.
