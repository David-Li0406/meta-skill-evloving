---
name: add-token
description: Add a new token to the VibeFunded dashboard. Use when user says "add token", "new token", "add project", or provides a GitHub Issue URL from the vibefunded repo with label "project-submission". Handles updating fetch_data.py, running verification, and updating documentation.
---

# Add Token to VibeFunded Dashboard

Add a new OSS-funded token to the dashboard by updating the data script and verifying it works.

## Required Information

| Field | Description | Example |
|-------|-------------|---------|
| ticker | Token symbol (without $) | `GAS` |
| name | Project name | `Gastown` |
| creator | Creator name | `Steve Yegge` |
| social | X/Twitter URL | `https://x.com/Steve_Yegge` |
| social_handle | X handle | `@Steve_Yegge` |
| project_url | GitHub repo URL | `https://github.com/steveyegge/gastown` |
| bags_url | Bags.fm token page | `https://bags.fm/...` |
| token_mint | Solana mint address | `7pskt3A1Zsjhngazam7vHWjWHnfgiRump916Xj7ABAGS` |
| description | Brief project description | `Multi-agent AI orchestrator...` |
| pair_address | DexScreener pair address | `FiNu5nSFwvjQbAFDESxDxvLhQJa3H7QYBrLUqFRB27v9` |

## Workflow

### 1. Gather Token Information

**If GitHub Issue URL provided:**
- Fetch the issue using `gh issue view <number> --repo vishalsachdev/vibefunded`
- Parse the issue body for required fields

**If no URL provided:**
- Ask user for required fields interactively
- Validate addresses look like valid Solana addresses (32-44 chars, base58)

### 2. Update fetch_data.py

Add entry to the `TOKENS` dict in `scripts/fetch_data.py`:

```python
"TICKER": {
    "name": "Project Name",
    "creator": "Creator Name",
    "social": "https://x.com/handle",
    "social_handle": "@handle",
    "project_url": "https://github.com/owner/repo",
    "bags_url": "https://bags.fm/...",
    "token_mint": "...",
    "description": "Brief description of what the project does.",
    "pair_address": "..."
}
```

Insert alphabetically by ticker to maintain order.

### 3. Verify Token Works

Run the fetch script (earnings will be 0 without API key, but other data should populate):

```bash
python scripts/fetch_data.py
```

Check the output for errors. Verify `data.json` contains the new token with:
- Price data from DexScreener
- GitHub stats (if repo exists)

### 4. Update Documentation

Add the new token to the Current Tokens table in `CLAUDE.md`:

```markdown
| $TICKER | Project Name | Creator Name | github.com/owner/repo |
```

### 5. Commit Changes

Stage and commit with message:
```
Add $TICKER token to dashboard

Added [Project Name] by [Creator] - [brief description]
```

## Validation Checklist

Before completing:
- [ ] Token mint address is valid (check on Solscan if unsure)
- [ ] Pair address returns data from DexScreener
- [ ] GitHub URL is accessible (if provided)
- [ ] Bags.fm URL is correct format
- [ ] Description is concise (1-2 sentences)
- [ ] No duplicate ticker in TOKENS dict
