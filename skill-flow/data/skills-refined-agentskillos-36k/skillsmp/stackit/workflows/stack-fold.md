# Workflow: Intelligent Branch Folding (`/stack-fold`)

This workflow guides the LLM through analyzing a branch stack and recommending branches to fold (squash) into their parents to maintain stack health and PR quality.

## Objectives
- Identify "too granular" branches (e.g., small typo fixes, minor adjustments).
- Combine them with their parent branches to reduce PR noise.
- Ensure safety by respecting locks, freezes, and scope boundaries.

## Steps

### 1. Gather Context
Fetch the complete metadata for the current stack:
```bash
command stackit info --stack --json --no-interactive
```

### 2. Identify Candidates
Analyze the JSON output to find folding candidates.

**Criteria for a "Good" Fold Candidate:**
- **Granularity:** The branch has few commits (often just 1) and small diff stats (few files changed, few lines added/deleted).
- **Descriptiveness:** The commit message suggests a minor fix or follow-up (e.g., "fix typo", "address review feedback", "tweak styles").
- **Safety:**
    - `is_locked`: Must be `false`.
    - `is_frozen`: Must be `false`.
    - `scope`: Must match the parent's scope (folding across scopes is forbidden).
    - **Target Parent:** The parent branch must also not be locked or frozen.

### 3. Detailed Analysis (Optional but Recommended)
For high-confidence candidates, verify the actual changes to ensure they are safe to merge into the parent:
```bash
command stackit info <branch-name> --diff --no-interactive
```

### 4. Propose a Fold Plan
Present your findings to the user. For each recommendation, include:
- **Branch to fold:** The name of the granular branch.
- **Target parent:** The branch it will be folded into.
- **Reasoning:** Why this branch is a good candidate (e.g., "It's a single-line typo fix").
- **Impact:** What the combined commit message or PR might look like.

### 5. Execute Fold
Wait for user confirmation. If confirmed, perform the fold:
```bash
# Fold branch into parent (keeps parent name)
command stackit checkout <branch-to-fold> --no-interactive
command stackit fold --no-interactive
```

### 6. Post-Fold Cleanup
After folding, ensure the stack is healthy:
```bash
command stackit restack --no-interactive
```

## Safety Constraints
- **Never fold into trunk** unless explicitly requested by the user.
- **Never fold locked or frozen branches.**
- **Never fold across different scopes.**
- If you are unsure if a fold is appropriate, ask the user for clarification.
