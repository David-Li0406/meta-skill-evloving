# File Organization & Directory Structure

**Purpose**: Guide to organizing files in Qara's directory structure - where to save what, when, and why.

**Last Updated**: 2025-11-19

---

## Directory Overview

```
~/.claude/
├── skills/          # Domain expertise packages (PERMANENT)
├── history/         # Permanent valuable outputs (PERMANENT)
├── scratchpad/      # Temporary working files (TEMPORARY)
├── bin/             # CLI tools and scripts (PERMANENT)
├── agents/          # Agent configurations (PERMANENT)
├── .env             # Environment variables (PERMANENT, PRIVATE)
```

---

## The Two Key Directories

### `history/` - PERMANENT
**What**: Valuable work to keep forever
**When**: Output has lasting value
**Examples**: Research findings, learnings, session logs

### `scratchpad/` - TEMPORARY
**What**: Working files, drafts, experiments
**When**: Temporary or exploratory work
**Examples**: Quick tests, draft outputs, throwaway code

---

## Detailed Directory Guide

### `~/claude/skills/` - Domain Expertise

**What Goes Here:**
- Skill packages with SKILL.md files
- Workflows and procedures
- Reference documentation
- Templates and assets
- CLI tools specific to skill domain

**Structure:**
```
skills/
├── CORE/                 # Core identity and infrastructure
├── brightdata/           # Web scraping with Bright Data
├── system-create-skill/  # Skill creation tooling
└── [domain-skills]/      # Your custom skills
```

**Never Put Here:**
- Output files
- Temporary work
- One-off scripts
- Data files

---

### `~/.claude/history/` - Permanent Outputs

**What Goes Here:**
- **Learnings**: Problem-solving narratives
- **Research**: Analysis and investigations
- **Sessions**: Work logs and summaries
- **Execution**: Command outputs
- **Upgrades**: Architectural changes

**Structure:**
```
history/
├── raw-outputs/          # Event logs (JSONL)
│   └── YYYY-MM/
│       └── YYYY-MM-DD_all-events.jsonl
│
├── learnings/            # Problem-solving narratives
│   └── YYYY-MM/
│       └── YYYY-MM-DD-HHMMSS_LEARNING_description.md
│
├── sessions/             # Work logs
│   └── YYYY-MM/
│       └── YYYY-MM-DD-HHMMSS_SESSION_description.md
│
├── research/             # Investigations
│   └── YYYY-MM-DD_topic/
│       ├── analysis.md
│       ├── findings.md
│       └── sources.md
│
├── execution/            # Command outputs
│   └── YYYY-MM/
│       └── YYYY-MM-DD-HHMMSS_command-name.txt
│
└── upgrades/             # Architectural changes
    ├── deprecated/
    │   └── YYYY-MM-DD_upgrade-name/
    └── YYYY-MM-DD_upgrade-description.md
```

**When to Save:**
- ✅ Output has lasting value
- ✅ Might need to reference later
- ✅ Documents learning/progress
- ✅ Research findings
- ✅ Important decisions

**When NOT to Save:**
- ❌ Temporary/throwaway work
- ❌ Easily reproducible
- ❌ Still drafting
- ❌ Experiments

---

### `~/.claude/scratchpad/` - Temporary Work

**What Goes Here:**
- Draft outputs before finalization
- Quick tests and experiments
- Temporary data files
- One-off requests
- Work in progress

**Structure:**
```
scratchpad/
├── YYYY-MM-DD/          # Date-based folders
│   ├── test-*.ts
│   ├── draft-*.md
│   └── temp-*.json
└── active/              # Current work
    └── wip-*.md
```

**When to Use:**
- 🧪 Experimenting with code
- 📝 Drafting content
- 🔬 Testing ideas
- ⚡ Quick throwaway work

**Cleanup:**
```bash
# Delete scratchpad older than 7 days
find ~/.claude/scratchpad -type f -mtime +7 -delete
```

---

### `~/.claude/bin/` - CLI Tools

**What Goes Here:**
- Reusable CLI tools
- System-wide scripts
- API wrappers (CLI-First pattern)

**Structure:**
```
bin/
├── llcli/               # Limitless CLI
│   ├── llcli.ts
│   ├── package.json
│   └── README.md
└── [other-tools]/
```

**Requirements:**
- Must be executable (`chmod +x`)
- Must have shebang (`#!/usr/bin/env bun`)
- Must have --help
- Must have README

---

## Decision Tree: Where to Save?

```
Is this valuable long-term?
│
├─ YES → history/
│  │
│  ├─ Problem-solving narrative? → history/learnings/
│  ├─ Research/analysis? → history/research/
│  ├─ Work summary? → history/sessions/
│  ├─ Command output? → history/execution/
│  └─ Architectural change? → history/upgrades/
│
└─ NO → scratchpad/
   │
   ├─ Draft/WIP? → scratchpad/active/
   ├─ Test/experiment? → scratchpad/YYYY-MM-DD/
   └─ Throwaway? → scratchpad/temp/
```

---

## File Naming Conventions

### History Files

**Learnings:**
```
YYYY-MM-DD-HHMMSS_LEARNING_short-description.md
2025-11-19-143000_LEARNING_typescript-async-patterns.md
```

**Sessions:**
```
YYYY-MM-DD-HHMMSS_SESSION_short-description.md
2025-11-19-140000_SESSION_content-population-work.md
```

**Research:**
```
YYYY-MM-DD_topic/
2025-11-19_api-strategy-analysis/
```

### Scratchpad Files

**Date-based:**
```
YYYY-MM-DD/
  test-feature.ts
  draft-doc.md
  temp-data.json
```

**Active work:**
```
active/
  wip-blog-post.md
  draft-proposal.md
```

---

## Verification Gates

### Before Saving to history/

Ask:
- [ ] Will I reference this in 1+ months?
- [ ] Does it document learning/progress?
- [ ] Is it research findings?
- [ ] Is it a reusable asset?
- [ ] Is it complete (not draft)?

**If 2+ YES → history/**
**Otherwise → scratchpad/**

### Before Deleting from scratchpad/

Ask:
- [ ] Is this truly temporary?
- [ ] Is it easily reproducible?
- [ ] No lasting value?
- [ ] More than 7 days old?

**If all YES → Safe to delete**

---

## Backup Strategy

### Auto-Backed Up (in git)
- ✅ `skills/` - Part of repo
- ✅ `bin/` - Part of repo
- ✅ `history/` - Should be in repo
- ✅ `.env` - Gitignored (but backup separately)

### Not Backed Up
- ❌ `scratchpad/` - Gitignored (by design)

### Manual Backup
```bash
# Backup environment variables
cp ~/.claude/.env ~/.claude/backups/env-$(date +%Y-%m-%d).bak

# Backup scratchpad (if needed)
tar -czf scratchpad-backup.tar.gz ~/.claude/scratchpad/
```

---

## Cleanup Maintenance

### Weekly Cleanup

```bash
# Review scratchpad
ls -lh ~/.claude/scratchpad/

# Delete old date folders (>7 days)
find ~/.claude/scratchpad -type d -name "20*" -mtime +7 -exec rm -rf {} +

# Review active work
ls -lh ~/.claude/scratchpad/active/
```

### Monthly Review

```bash
# Review history size
du -sh ~/.claude/history/*

# Archive old raw-outputs (>3 months)
tar -czf raw-outputs-archive-$(date +%Y-%m).tar.gz \
  ~/.claude/history/raw-outputs/YYYY-MM/
```

---

## Quick Reference

### Where to Save

```
Permanent valuable work → history/
  ├─ Learning → history/learnings/
  ├─ Research → history/research/
  └─ Session logs → history/sessions/

Temporary work → scratchpad/
  ├─ Drafts → scratchpad/active/
  ├─ Tests → scratchpad/YYYY-MM-DD/
  └─ Throwaway → scratchpad/temp/

CLI tools → bin/
  └─ Reusable scripts → bin/toolname/

Skills → skills/
  └─ Domain packages → skills/domain-name/
```

### Common Patterns

```bash
# Save learning
~/.claude/history/learnings/YYYY-MM/YYYY-MM-DD-HHMMSS_LEARNING_topic.md

# Draft in scratchpad
~/.claude/scratchpad/active/wip-document.md

# Finalize to history
mv ~/.claude/scratchpad/active/wip-document.md \
   ~/.claude/history/sessions/YYYY-MM/YYYY-MM-DD-HHMMSS_SESSION_topic.md

# Create CLI tool
~/.claude/bin/toolname/toolname.ts
```

---

## Related Documentation

- **CONSTITUTION.md** - History system architecture
- **security-protocols.md** - What to never commit
- **git-update-repo.md** - Committing organized files

---

**Key Takeaways:**
1. `history/` = permanent, valuable
2. `scratchpad/` = temporary, experimental
3. Use date-based naming for files
4. Clean scratchpad weekly
5. Verify before moving to history
6. Keep `bin/` for reusable tools
