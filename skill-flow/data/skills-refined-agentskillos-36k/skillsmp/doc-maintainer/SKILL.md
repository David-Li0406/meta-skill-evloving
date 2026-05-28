---
name: doc-maintainer
description: Auto-updates documentation (README, implementation plans) based on recent code changes.
---

# Document Maintainer

This skill helps you keep project documentation synchronized with the codebase. It analyzes recent git changes and suggests updates to documentation files.

## When to Use

- After completing a significant feature or refactor.
- When `README.md` or `implementation_plan.md` assumes outdated implementation details.
- To verify if documentation reflects the current codebase state.

## Workflow

1.  **Analyze Changes**: Run the analysis script to see what code has changed.
2.  **Review Suggestions**: The script will output a summary of changes and suggest documentation updates.
3.  **Apply Updates**: You (the Agent) should apply the updates to the markdown files using your file editing tools.

## Tools

### Analyze Changes

Run the following script to analyze the git diff and identify impacted documentation:

```bash
python .agent/skills/doc-maintainer/scripts/analyze.py --since HEAD~1
```

*(Note: Adjust `--since` to cover the relevant commit range if needed)*

**Output Format**: Text summary of changes and potential documentation impacts.

**Example**:
```text
--- Doc Impact Analysis (Since HEAD~1) ---
Changed Files (1):
  - src/auth.py

Documentation References:
  📄 README.md mentions:
     -> src/auth.py
```

## Rules

1.  **Truth Source**: The Code is the source of truth. If docs contradict code, fix the docs.
2.  **Conciseness**: Don't narrate the diff; summarize the *impact* on the user or developer.
3.  **Safety**: Do not overwrite `productContext.md` (Requirements) unless the user explicitly requested a requirement change.

## Troubleshooting

If the script fails:
1. Check if you are in the project root.
2. Ensure git is initialized and has commits.

