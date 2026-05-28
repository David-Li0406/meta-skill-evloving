---
name: "feature-continue"
description: "Resume work on existing feature clone"
---

Continues work on an existing feature clone with proper context analysis.


## Feature description from user input
"$ARGUMENTS"

### Feature Description Validation
If empty or missing: "Error: Feature description is required. Please provide a detailed description of the feature you want to continue implementing."

## Process

### Step 1: Search for Existing Clone
List existing clones in _clones/ directory and try to match the feature description:
```bash
ls -1 _clones/
```

If found → Continue to Step 4 (navigate)
If not found → Continue to Step 2

### Step 2: Check for Remote Branch
Check if a remote feature branch exists that matches the description:
```bash
git fetch --prune
git branch -a | grep "remotes/origin/feature"
```

If found → Continue to Step 3
If not found → Exit with error message:
- Tell user: "Feature branch not found locally or remotely"
- Suggest: "Use the create-clone skill to create a new feature clone: /create-clone <feature-description>"
- Exit the skill

### Step 3: Clone from Remote
Create the local clone from the remote branch:
```bash
REPO_URL=$(git config --get remote.origin.url)
mkdir -p _clones
git clone -b FEATURE_BRANCH_NAME "$REPO_URL" _clones/FEATURE_BRANCH_NAME

# Setup development environment
cd _clones/FEATURE_BRANCH_NAME
bash ~/.claude/scripts/setup_project_env.sh
```

After cloning → Continue to Step 4

### Step 4: Navigate to Feature Clone
```bash
cd _clones/FEATURE_NAME
```

### Step 5: Sync with Main
Run the sync skill to commit and push.

### Step 6: Run Feature Loop
Run the feature-loop-scheme skill to execute the full development workflow.
