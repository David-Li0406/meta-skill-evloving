---
name: git_commit
description: 作業終了後に不要な一時ファイルを削除し、gitにコミットする
---

# Commit and Cleanup

This skill handles the cleanup of temporary files and committing changes to the git repository.

## Instructions

1. **Identify Temporary Files**:
    * Look for loose python scripts in the root directory (e.g., `temp.py`, `test_adhoc.py`).
    * Look for generated artifacts that shouldn't be committed (logs, plots in unexpected places).
    * *Always* ask for confirmation before deleting a file unless it is a standard temporary artifact you just created.

2. **Clean Up**:
    * Delete the identified confirmed files.
    * Clean up standard cache directories:

        ```bash
        find . -maxdepth 4 -name "__pycache__" -type d -exec rm -rf {} +
        find . -maxdepth 4 -name ".pytest_cache" -type d -exec rm -rf {} +
        rm -rf .ruff_cache .pytest-ipython
        ```

3. **Git Status**:
    * Run `git status` to see what has changed.

4. **Commit**:
    * Add relevant files: `git add <files>`
    * Generate a concise but descriptive commit message following conventional commits if possible.
    * Commit: `git commit -m "message"`

## Best Practices

- Do not add `__pycache__`, `.vscode`, `.idea`, etc., to the commit (ensure `.gitignore` is respected).
* If the `git status` output is huge, do not use `git add .` blindly.
