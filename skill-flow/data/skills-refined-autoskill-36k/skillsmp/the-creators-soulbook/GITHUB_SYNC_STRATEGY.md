# Soulbook GitHub Sync Strategy

**Local Path**: `.claude-skills/soulbook/`
**GitHub Repo**: `https://github.com/frankxai/Soulbook-`
**Sync Method**: Manual or automated push

---

## Repository Structure Mapping

### GitHub Repo Structure (frankxai/Soulbook-)
```
Soulbook-/
├── README.md                         # Main landing page
├── docs/                             # Documentation
│   ├── onboarding.md
│   ├── life-symphony.md              # Musical metaphor
│   ├── golden-path.md                # Journey metaphor
│   └── 7-pillars.md                  # Architectural metaphor
├── prompts/                          # AI conversation starters
│   ├── energy.md
│   ├── mind.md
│   ├── soul.md
│   ├── craft.md
│   ├── capital.md
│   ├── circle.md
│   └── legacy.md
├── templates/
│   └── obsidian/                     # Obsidian vault template
└── assets/
    └── images/                       # Visuals
```

### Local Structure (.claude-skills/soulbook/)
```
soulbook/
├── SKILL.md                          # Claude Code skill definition
├── soulbook-creator-agent.md         # Agent behavior
├── SETUP.md                          # Setup guide
├── README.md                         # Quick reference
├── SOULBOOK_OVERVIEW.md              # Complete framework
├── 7-pillars/                        # Pillar details
│   ├── SKILL.md
│   ├── energy/
│   ├── mind/
│   ├── soul/
│   ├── craft/
│   ├── capital/
│   ├── circle/
│   └── legacy/
├── life-symphony/                    # Musical metaphor
├── golden-path/                      # Journey metaphor
└── agents/                           # AI agents
    ├── lifesmith/
    └── soul-composer/
```

---

## Sync Strategy

### What Syncs Where

| Local File | GitHub Destination | Purpose |
|------------|-------------------|---------|
| `SOULBOOK_OVERVIEW.md` | `README.md` | Main landing page |
| `7-pillars/SKILL.md` | `docs/7-pillars.md` | Architecture framework |
| `life-symphony/SKILL.md` | `docs/life-symphony.md` | Musical framework |
| `golden-path/SKILL.md` | `docs/golden-path.md` | Journey framework |
| `7-pillars/energy/SKILL.md` | `prompts/energy.md` | Energy pillar content |
| `7-pillars/mind/SKILL.md` | `prompts/mind.md` | Mind pillar content |
| ...etc | ...etc | All pillars |

### What Stays Local Only

These are Claude Code specific and don't sync to GitHub:
- `SKILL.md` (Claude Code skill definition)
- `soulbook-creator-agent.md` (Agent instructions)
- `SETUP.md` (Local setup guide)
- `GITHUB_SYNC_STRATEGY.md` (This file)

---

## Sync Methods

### Method 1: Manual Sync Script

Create a sync script:

```bash
#!/bin/bash
# sync-to-github.sh

# Set paths
LOCAL_SOULBOOK=".claude-skills/soulbook"
GITHUB_REPO="~/repos/Soulbook-"  # Clone repo here first

# Sync main README
cp "$LOCAL_SOULBOOK/SOULBOOK_OVERVIEW.md" "$GITHUB_REPO/README.md"

# Sync frameworks
cp "$LOCAL_SOULBOOK/7-pillars/SKILL.md" "$GITHUB_REPO/docs/7-pillars.md"
cp "$LOCAL_SOULBOOK/life-symphony/SKILL.md" "$GITHUB_REPO/docs/life-symphony.md"
cp "$LOCAL_SOULBOOK/golden-path/SKILL.md" "$GITHUB_REPO/docs/golden-path.md"

# Sync prompts (pillars)
cp "$LOCAL_SOULBOOK/7-pillars/energy/SKILL.md" "$GITHUB_REPO/prompts/energy.md"
cp "$LOCAL_SOULBOOK/7-pillars/mind/SKILL.md" "$GITHUB_REPO/prompts/mind.md"
cp "$LOCAL_SOULBOOK/7-pillars/soul/SKILL.md" "$GITHUB_REPO/prompts/soul.md"
cp "$LOCAL_SOULBOOK/7-pillars/craft/SKILL.md" "$GITHUB_REPO/prompts/craft.md"
cp "$LOCAL_SOULBOOK/7-pillars/capital/SKILL.md" "$GITHUB_REPO/prompts/capital.md"
cp "$LOCAL_SOULBOOK/7-pillars/circle/SKILL.md" "$GITHUB_REPO/prompts/circle.md"
cp "$LOCAL_SOULBOOK/7-pillars/legacy/SKILL.md" "$GITHUB_REPO/prompts/legacy.md"

# Commit and push
cd "$GITHUB_REPO"
git add .
git commit -m "chore: sync from Claude Code soulbook skill"
git push origin main

echo "✅ Sync complete!"
```

### Method 2: Git Worktree (Advanced)

Use git worktree to have both local and GitHub in sync:

```bash
# Clone repo adjacent to FrankX directory
cd ~/
git clone https://github.com/frankxai/Soulbook-.git

# Create symlinks
ln -s ~/Soulbook-/docs ~/FrankX/.claude-skills/soulbook/github-docs
ln -s ~/Soulbook-/prompts ~/FrankX/.claude-skills/soulbook/github-prompts
```

### Method 3: GitHub Actions (Automated)

Set up GitHub Actions to auto-sync when you push to FrankX repo.

---

## Recommended Workflow

### 1. Develop Locally
Work in `.claude-skills/soulbook/` with full Claude Code integration.

### 2. Sync to GitHub Periodically
When major updates are done:

```bash
# Navigate to Soulbook GitHub repo
cd ~/repos/Soulbook-

# Copy updated files
cp ~/FrankX/.claude-skills/soulbook/SOULBOOK_OVERVIEW.md README.md
# ...etc

# Commit and push
git add .
git commit -m "feat: update framework from Claude Code skill"
git push origin main
```

### 3. GitHub is the Public Face
- GitHub repo = Public documentation and templates
- Local `.claude-skills/soulbook/` = Working development + Claude Code functionality

---

## Initial Setup

### Step 1: Clone GitHub Repo

```bash
cd ~/repos  # or wherever you keep repos
git clone https://github.com/frankxai/Soulbook-.git
```

### Step 2: Create Sync Script

Save the script above as `sync-to-github.sh` and make executable:

```bash
chmod +x sync-to-github.sh
```

### Step 3: Do Initial Sync

```bash
./sync-to-github.sh
```

---

## Sync Checklist

Before syncing, verify:

- [ ] All pillar SKILL.md files are complete
- [ ] SOULBOOK_OVERVIEW.md is up to date
- [ ] Life Book frameworks are finalized
- [ ] No sensitive/personal data in files
- [ ] Markdown formatting is clean
- [ ] All links work

---

## Version Control Strategy

### GitHub Repo (Public)
- **Purpose**: Public framework, templates, documentation
- **Audience**: Soulbook users, community
- **Content**: Generic, shareable, polished

### Local Claude Skills (Private)
- **Purpose**: Claude Code integration, agent behavior
- **Audience**: You (Frank) and Claude
- **Content**: Technical, implementation details, agent prompts

---

## Future: Automated Sync

When ready, set up GitHub Action in FrankX repo:

```yaml
# .github/workflows/sync-soulbook.yml
name: Sync Soulbook to GitHub

on:
  push:
    paths:
      - '.claude-skills/soulbook/**'

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Sync files
        run: |
          # Copy files to Soulbook repo
          # Commit and push
```

---

## Summary

**Development Flow:**
1. Edit locally in `.claude-skills/soulbook/`
2. Test with `/soulbook` command
3. When stable, run `./sync-to-github.sh`
4. GitHub repo updates automatically

**Best Practice:**
- Keep local as "dev" version
- GitHub as "production" public version
- Sync only when major milestones complete

---

*Last Updated: 2026-01-14*
