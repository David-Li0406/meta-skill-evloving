# Agent Prompts

## Prompt Template

All agents receive the same structure (substitute `{AGENT_NAME}` with ALICE, BOB, or CARL):

```
Read {context_file} for review context, and {diff_file} for the full diff.

Use this review checklist:
{contents of review-dimensions.md}

Review the completed work against PRD requirements. Explore the codebase as needed.

OUTPUT FORMAT IS MANDATORY. Follow exactly:
{agent output format from output-formats.md "Agent Output Format" section}
```

> **Note:** The output format is defined in `output-formats.md` under "Agent Output Format". This is the single source of truth — do not duplicate format rules here.
