---
name: project-notebook-and-deploy-check
description: Use this skill to execute all project notebooks and perform pre-deployment checks to ensure everything is functioning correctly before deployment.
---

# Run Notebooks and Pre-Deployment Checks

This skill executes all `.ipynb` files in the project sequentially and runs essential pre-deployment checks, reporting any errors encountered.

## Instructions

### Step 1: Run All Notebooks

1. **Find Notebooks**:
    * Search for all `.ipynb` files in the project/workspace, excluding `.ipynb_checkpoints`.

2. **Execute Sequentially**:
    * Iterate through the list of notebooks and execute each using a command line tool.
    * **Recommended Tool**: `jupyter nbconvert --to notebook --execute --inplace <notebook.ipynb>` or `pytest --nbmake <notebook.ipynb>`.
    * **CRITICAL**: Wait for one notebook to finish before starting the next to conserve memory.

3. **Report**:
    * Track pass/fail status for each notebook.
    * If a notebook fails, log the error and continue (default behavior).
    * Provide a summary report at the end.

### Step 2: Pre-Deployment Checks

1. **Environment Verification**:
    * Ensure the current directory is the root of a git worktree.
    * Check for the existence of the `main` directory and the `scripts/pre-deploy-check.sh` script.

    **Commands**:
    ```bash
    git worktree list
    ls -la main/scripts/pre-deploy-check.sh
    ```

2. **Execute Pre-Deployment Check Script**:
    * Run `scripts/pre-deploy-check.sh` to validate all necessary checks.

    **Commands**:
    ```bash
    cd main
    ./scripts/pre-deploy-check.sh
    ```

3. **Check Contents**:
    * The script should validate:
        - Backend tests (`pytest`)
        - Frontend linting (`npm run lint`)
        - Frontend tests (`npm run test:run`)
        - CDK Synth (`npx cdk synth`)

4. **Error Analysis**:
    * If errors occur, analyze the type of error and provide suggestions for fixes based on common error patterns.

5. **Fix Suggestions**:
    * Propose specific fixes based on the error type, including code snippets for clarity.

6. **Re-Execution**:
    * After applying fixes, re-run the pre-deployment check script to ensure all checks pass.

7. **Deployment Guidance**:
    * If all checks pass, provide instructions for deploying both frontend and backend components.

## Output Format

### Success Output

```
✅ All checks passed. Ready for deployment.

Next actions:
- [ ] Frontend deployment (git push origin main)
- [ ] Backend deployment (cd cdk && npx cdk deploy --all --context jravan=true)
```

### Error Detection Output

```
🔴 Errors detected during pre-deployment checks.

Next actions:
- [ ] Fix errors
- [ ] Re-run: ./scripts/pre-deploy-check.sh
```

## Notes

- Ensure to run the skill in the correct environment and follow the specified commands for successful execution.
- The skill aims to minimize deployment failures by ensuring all checks are passed before proceeding.