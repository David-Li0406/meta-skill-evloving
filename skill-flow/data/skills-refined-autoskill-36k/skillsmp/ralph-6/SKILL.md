---
name: ralph
description: Ralph - Long-Running Task Agent. Autonomous AI that works through PRD tasks iteratively, with access to full ACT ecosystem knowledge across all 7 codebases.
---

# Ralph Agent - Ecosystem-Wide Task Automation

Long-running AI agent that works through PRD tasks autonomously using the "Ralph Wiggum" methodology, with access to all ACT ecosystem knowledge.

## When to Use
- Large features requiring multiple implementation steps
- Batch processing across multiple codebases
- Overnight/background task completion
- Content generation from ecosystem activity
- Complex migrations or cross-project refactors

## Quick Start

```bash
# 1. Create PRD
./ralph/create-prd.sh my-project

# 2. Edit ralph/prd.json with your tasks

# 3. Run Ralph
./ralph/ralph.sh
```

## Ecosystem Knowledge Access

Ralph has access to ALL 7 ACT codebases:

| Project | Path | Focus |
|---------|------|-------|
| Global Infrastructure | `/Users/benknight/act-global-infrastructure` | Automation, skills, MCPs |
| JusticeHub | `/Users/benknight/Code/JusticeHub` | Youth justice platform |
| Empathy Ledger | `/Users/benknight/Code/empathy-ledger-v2` | Ethical storytelling |
| ACT Farm | `/Users/benknight/Code/ACT Farm/act-farm` | Land & conservation |
| The Harvest | `/Users/benknight/Code/The Harvest Website` | CSA & community |
| Goods on Country | `/Users/benknight/Code/Goods Asset Register` | Circular economy |
| ACT Placemat | `/Users/benknight/Code/ACT Placemat` | Hub website |

## PRD Types

### 1. Single-Project PRD (Standard)
```json
{
  "project": "JusticeHub",
  "features": [
    {
      "id": "feature-id",
      "priority": 1,
      "title": "Feature Title",
      "project_path": "/Users/benknight/Code/JusticeHub",
      "passes": false
    }
  ]
}
```

### 2. Cross-Ecosystem PRD
```json
{
  "project": "ACT Ecosystem",
  "type": "cross-ecosystem",
  "features": [
    {
      "id": "shared-component",
      "priority": 1,
      "title": "Implement shared auth across projects",
      "affected_projects": [
        "/Users/benknight/Code/JusticeHub",
        "/Users/benknight/Code/empathy-ledger-v2"
      ],
      "passes": false
    }
  ]
}
```

### 3. Content Generation PRD
```json
{
  "project": "Content Publishing",
  "type": "content",
  "features": [
    {
      "id": "new-year-posts",
      "priority": 1,
      "title": "Generate 5 New Year social posts",
      "content_type": "social",
      "target_accounts": ["LinkedIn (Company)", "LinkedIn (Personal)"],
      "sources": ["ecosystem-highlights", "ralph-completions", "sprint-milestones"],
      "passes": false
    }
  ]
}
```

## Knowledge Sources

When generating content or making decisions, Ralph can access:

### 1. Brand Guidelines
Invoke `act-brand-alignment` skill for:
- Voice/tone guidelines
- Project descriptions
- Visual language
- LCAA methodology

### 2. Sprint Data
Query Notion databases:
- Sprint Tracking: `2d5ebcf9-81cf-8151-873d-d14f21b48333`
- Deployments: `2d6ebcf9-81cf-81d1-a72e-c9180830a54e`
- Velocity Metrics: `2d6ebcf9-81cf-8123-939f-fab96227b3da`

### 3. Codebase Insights
Scan all projects for:
- Recent commits and releases
- README changes
- Test coverage
- Documentation updates

### 4. CRM Context
Invoke `ghl-crm-advisor` skill for:
- Pipeline patterns
- Contact context
- Campaign history

## Content Generation Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  1. GATHER ECOSYSTEM CONTEXT                                 │
│                                                              │
│  • Scan ralph/progress.txt for completions                   │
│  • Query Notion for sprint milestones                        │
│  • Check git logs across all 7 repos                         │
│  • Review brand-core.md for voice                            │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────────┐
│  2. GENERATE CONTENT                                         │
│                                                              │
│  • Apply act-brand-alignment voice                           │
│  • Format for target platforms                               │
│  • Add appropriate hashtags                                  │
│  • Include relevant stats/metrics                            │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────────┐
│  3. CREATE IN NOTION                                         │
│                                                              │
│  • Write to Content Hub database                             │
│  • Set status: "Story in Development"                        │
│  • Select Target Accounts                                    │
│  • Mark PRD feature as passes: true                          │
└─────────────────────────────────────────────────────────────┘
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `MAX_ITERATIONS` | 10 | Max loops before stopping |
| `PROJECT_DIR` | `$(pwd)` | Working directory |
| `PRD_FILE` | `ralph/prd.json` | PRD location |
| `AGENT_CMD` | `claude` | Agent command |

## How It Works

1. Reads PRD, finds highest priority `passes: false` task
2. Spawns Claude agent to implement ONE feature
3. Agent commits work, updates PRD to `passes: true`
4. Logs progress to `ralph/progress.txt`
5. Repeats until all tasks complete or max iterations

## Signal Tokens

Agent outputs these to control flow:
- `<promise>ITERATION_DONE</promise>` - Task complete, continue
- `<promise>COMPLETE</promise>` - All tasks done, stop

## Post-Completion Hooks

After Ralph completes a feature, optionally:

1. **Auto-generate announcement post**
   ```bash
   node .claude/skills/content-publisher/references/post-template.mjs \
     --title "Shipped: $FEATURE_TITLE" \
     --content "$FEATURE_DESCRIPTION"
   ```

2. **Update sprint tracking**
   ```bash
   node scripts/sync-github-notion.mjs
   ```

3. **Publish to social**
   ```bash
   node scripts/sync-content-to-ghl.mjs
   ```

## References

| Need | Reference |
|------|-----------|
| Main runner script | `ralph/ralph.sh` |
| PRD template | `ralph/prd.json` |
| Progress log | `ralph/progress.txt` |
| Content generator | `.claude/skills/content-publisher/references/post-template.mjs` |
| Brand guidelines | `.claude/skills/act-brand-alignment/SKILL.md` |
