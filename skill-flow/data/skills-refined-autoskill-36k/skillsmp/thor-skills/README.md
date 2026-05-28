# THOR Claude Code Skills

Claude Code skills for the THOR APT scanner by Nextron Systems.

## Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/NextronSystems/thor-skill.git
```

### Step 2: Copy to Claude skills directory

```bash
cp -r thor-skill ~/.claude/skills/
```

This copies the skill folder to `~/.claude/skills/thor-skill/`.

## Verify Installation

After installation, ask Claude Code:

> "What Skills are available?"

Claude should list the THOR skills:
- **thor-scan** – Run THOR scans
- **thor-log-analysis** – Interpret THOR results
- **thor-troubleshooting** – Diagnose THOR issues
- **thor-maintenance** – Update/upgrade THOR
- **thor-lens** – THOR Lens forensic timeline viewer (requires v11)
- **thor-db** – Analyze ThorDB for performance tuning

## Skills Overview

| Skill | Use When |
|-------|----------|
| thor-scan | You want to run a scan or need the right command |
| thor-log-analysis | You have results to analyze or triage |
| thor-troubleshooting | THOR is stuck, slow, or failing |
| thor-maintenance | You need to update signatures or upgrade THOR |
| thor-lens | You want to explore forensic timelines in a web UI |
| thor-db | You want to analyze scan timing or find slow rules |

## Requirements

- Claude Code CLI
- THOR v10 (stable) or v11 (TechPreview)
- THOR Lens features require v11 with `--audit-trail` output
