---
name: run-notebooks-and-pre-deploy-checks
description: Use this skill to execute all project notebooks and perform pre-deployment checks to ensure everything is functioning correctly before deployment.
---

# Skill body

## Overview

This skill combines the execution of all Jupyter notebooks in a project with essential pre-deployment checks, ensuring that both code and deployment configurations are error-free.

## Instructions

### Step 1: Run All Notebooks

1. **Find Notebooks**:
    - Search for all `.ipynb` files in the project/workspace.
    - Exclude `.ipynb_checkpoints`.

2. **Execute Sequentially**:
    - Iterate through the list of notebooks.
    - For each notebook, execute it using a command line tool that runs the kernel.
    - **Recommended Tool**: `jupyter nbconvert --to notebook --execute --inplace <notebook.ipynb>` or `pytest --nbmake <notebook.ipynb>`.
    - **CRITICAL**: Wait for one notebook to finish before starting the next to conserve memory.

3. **Report**:
    - Track pass/fail status for each notebook.
    - If a notebook fails, log the error and continue (default behavior).
    - Provide a summary report at the end.

### Step 2: Pre-Deployment Checks

1. **Environment Check**:
    - Ensure the current directory is the root of a git worktree.
    - Check for the existence of the `main` directory.
    - Verify that `scripts/pre-deploy-check.sh` exists.

    **Commands**:
    ```bash
    git worktree list
    ls -la main/scripts/pre-deploy-check.sh
    ```

2. **Execute Pre-Deployment Script**:
    - Run the pre-deployment checks by executing `scripts/pre-deploy-check.sh`.

    **Commands**:
    ```bash
    cd main
    ./scripts/pre-deploy-check.sh
    ```

3. **Error Analysis**:
    - Analyze errors from the following checks:
        - Backend tests (`pytest`)
        - Frontend linting (`npm run lint`)
        - Frontend tests (`npm run test:run`)
        - CDK Synth (`npx cdk synth`)

4. **Propose Fixes**:
    - Based on the error analysis, provide specific suggestions for fixes.

5. **Implement Fixes**:
    - Upon user approval, implement the proposed fixes and re-run the pre-deployment checks.

### Conclusion

This skill ensures that all notebooks are executed and that the project is ready for deployment by performing necessary checks and providing actionable feedback on any issues encountered.