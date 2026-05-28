---
name: skill-manager
description: Manages the dynamic skill learning system. Use when you want to list skills, scan transcripts for patterns, learn preferences, approve/reject candidates, rollback versions, view skill history, or check usage statistics. Trigger phrases include "manage skills", "skill learn", "list skills", "approve skill", "skill stats", "skill history", "rollback skill", "scan patterns", "learn preferences".
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Write
---

# Skill Manager

This skill manages the **dynamic skill learning and generation system**. It enables automatic skill creation from usage patterns, version control, and auto-improvement.

## Core Capabilities

1. **Pattern Observation** - Hooks capture tool usage and prompt patterns
2. **Skill Learning** - Analyze patterns to generate skill candidates
3. **Version Control** - Git-based versioning with rollback
4. **Auto-Improvement** - Automatically enhance skills based on effectiveness

## Commands

All commands use the manage.py CLI:

```bash
python3 ~/.claude/skills/_skill-manager/scripts/manage.py <command> [args]
```

### List All Skills

Show installed skills with status and effectiveness scores:

```bash
python3 ~/.claude/skills/_skill-manager/scripts/manage.py list
```

### Scan Transcripts

Scan Claude transcripts for usage patterns (run before learn):

```bash
python3 ~/.claude/skills/_skill-manager/scripts/manage.py scan
```

### Learn Preferences

Learn user preferences from prompts and update CLAUDE.md:

```bash
python3 ~/.claude/skills/_skill-manager/scripts/manage.py preferences --force
```

### View Captured Prompts

View recent user prompts:

```bash
python3 ~/.claude/skills/_skill-manager/scripts/manage.py prompts [N]
```

### Learn from Patterns

Analyze collected patterns and generate skill candidates:

```bash
python3 ~/.claude/skills/_skill-manager/scripts/manage.py learn
```

### Show Candidates

List pending skill candidates awaiting approval:

```bash
python3 ~/.claude/skills/_skill-manager/scripts/manage.py candidates
```

### Approve a Skill

Approve a candidate skill for use:

```bash
python3 ~/.claude/skills/_skill-manager/scripts/manage.py approve <candidate-id>
```

### Reject a Skill

Reject and remove a candidate skill:

```bash
python3 ~/.claude/skills/_skill-manager/scripts/manage.py reject <candidate-id>
```

### View Skill History

Show version history for a skill:

```bash
python3 ~/.claude/skills/_skill-manager/scripts/manage.py history <skill-name>
```

### Rollback Skill Version

Restore a skill to a previous version:

```bash
python3 ~/.claude/skills/_skill-manager/scripts/manage.py rollback <skill-name> <version>
```

### View Statistics

Show usage analytics and effectiveness metrics:

```bash
python3 ~/.claude/skills/_skill-manager/scripts/manage.py stats
```

### Force Auto-Improvement

Trigger improvement analysis for a specific skill:

```bash
python3 ~/.claude/skills/_skill-manager/scripts/manage.py improve <skill-name>
```

### Refine a Skill

Interactively improve a skill with new patterns:

```bash
python3 ~/.claude/skills/_skill-manager/scripts/manage.py refine <skill-name>
```

## How Pattern Learning Works

### 1. Observation Phase

Hooks automatically capture:
- **Tool sequences** - Which tools are used in what order
- **Domain keywords** - DevOps, security, frontend, etc.
- **Success/failure signals** - Task completion, errors, retries

### 2. Analysis Phase

The learning engine detects:
- **Repeated workflows** - Same tool chains used 2+ times
- **Domain expertise** - Concentration of domain-specific keywords
- **Reusable patterns** - Generalizable processes

### 3. Scoring Phase

Candidates are scored on:
| Factor | Weight | Criteria |
|--------|--------|----------|
| Frequency | 30% | Pattern appears 2+ times |
| Complexity | 20% | 3-7 tool steps optimal |
| Domain clarity | 25% | Clear domain association |
| Distinctiveness | 25% | Different from existing skills |

### 4. Generation Phase

High-scoring patterns become skill packages with:
- `SKILL.md` - Definition with YAML frontmatter
- `skill.meta.json` - Metadata and effectiveness tracking
- `references/` - Extracted documentation
- `scripts/` - Helper utilities (if applicable)
- `CHANGELOG.md` - Version history

## Auto-Improvement System

Skills automatically improve when:
1. **Success rate drops below 70%**
2. **New enhancing patterns detected**
3. **50+ usages since last improvement**
4. **User manually refines skill** (system learns from refinement)

### Improvement Actions

- Add missing tool permissions
- Update reference documentation
- Add error handling for failure cases
- Refine trigger phrases
- Optimize workflow steps

### Confidence-Based Application

| Confidence | Action |
|------------|--------|
| ≥90% | Auto-apply improvement |
| 70-89% | Queue for user approval |
| <70% | Suggest but don't queue |

## Version Control

Each skill is a Git repository supporting:

```bash
# View version history
cd ~/.claude/skills/<skill-name>
git log --oneline

# Compare versions
git diff v1.0.0 v1.1.0

# Rollback
git checkout v1.0.0
```

## Configuration

Edit `~/.claude/skills/.skill-system/config.json`:

```json
{
  "observation": {
    "enabled": true,
    "pattern_retention_days": 90
  },
  "learning": {
    "auto_suggest": true,
    "min_frequency": 2,
    "score_threshold": 0.6
  },
  "improvement": {
    "enabled": true,
    "auto_apply_threshold": 0.9,
    "min_usage_before_improve": 10,
    "success_rate_trigger": 0.7
  }
}
```

## Supported Domains

Pre-configured domain detection:
- **devops** - docker, kubernetes, ci/cd, terraform
- **security** - audit, vulnerability, owasp, encryption
- **data_science** - pandas, numpy, model, tensorflow
- **frontend** - react, vue, css, webpack
- **backend** - api, rest, database, orm
- **git** - merge, rebase, pr, branch

Custom domains can be added in config.

## Data Storage

| Location | Contents | Persistence |
|----------|----------|-------------|
| `.skill-system/patterns/` | Raw observations | 90 days |
| `.skill-system/candidates/` | Pending approvals | Until approved/rejected |
| `.skill-system/config.json` | Configuration | Permanent |
| `<skill-name>/` | Active skills | Git-versioned |

## Example Workflow

1. **Normal usage** - Use Claude Code normally
2. **Scan transcripts** - `manage.py scan` extracts patterns from transcripts
3. **Learn preferences** - `manage.py preferences --force` updates CLAUDE.md with learned rules
4. **Generate candidates** - `manage.py learn` creates skill candidates from patterns
5. **Review candidates** - `manage.py candidates` shows suggestions
6. **Approve** - `manage.py approve docker-compose-helper`
7. **Use skill** - Skill is now active and tracking effectiveness
8. **Auto-improve** - System enhances based on usage data

## Troubleshooting

### Hooks not capturing

Check hooks are registered:
```bash
cat ~/.claude/settings.local.json | grep -A5 hooks
```

### No candidates generated

Ensure sufficient pattern data:
```bash
wc -l ~/.claude/skills/.skill-system/patterns/*.jsonl
```

### Skill not improving

Check effectiveness metrics:
```bash
cat ~/.claude/skills/<skill-name>/skill.meta.json | jq .effectiveness
```
