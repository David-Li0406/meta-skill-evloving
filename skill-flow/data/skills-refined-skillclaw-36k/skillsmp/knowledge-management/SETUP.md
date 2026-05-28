# Setup Guide: Push to GitHub

## Option 1: Push Existing Repo

```bash
# แตก zip file
unzip knowledge-management-repo.zip -d knowledge-management-skill
cd knowledge-management-skill

# สร้าง repo ใหม่บน GitHub แล้ว push
git remote add origin https://github.com/YOUR_USERNAME/knowledge-management-skill.git
git push -u origin main
```

## Option 2: Create New Repo

```bash
# สร้าง repo ใหม่บน GitHub ก่อน (ไม่ต้อง init README)
# https://github.com/new

# Clone และ copy files
git clone https://github.com/YOUR_USERNAME/knowledge-management-skill.git
cd knowledge-management-skill

# แตก zip แล้ว copy files (ไม่รวม .git)
unzip ../knowledge-management-repo.zip -d ../temp-skill
cp -r ../temp-skill/knowledge-management-repo/* .
rm -rf ../temp-skill

# Commit และ push
git add -A
git commit -m "feat: initial release - Knowledge Management Skill"
git push -u origin main
```

## Option 3: GitHub CLI

```bash
# ใช้ GitHub CLI
cd knowledge-management-skill

gh repo create knowledge-management-skill --public --source=. --push
```

## After Push

### Enable as Skill

```bash
# Clone ไปที่ Claude skills directory
git clone https://github.com/YOUR_USERNAME/claude-km-skill.git ~/.claude/skills/claude-km-skill

# หรือ add เป็น git submodule ใน project
git submodule add https://github.com/YOUR_USERNAME/claude-km-skill.git .claude/skills/claude-km-skill
```

### Share with Team

เพิ่มใน project's `README.md`:

```markdown
## Knowledge Management

This project uses [Claude KM Skill](https://github.com/YOUR_USERNAME/claude-km-skill) for capturing development knowledge.

### Setup

\`\`\`bash
git clone https://github.com/YOUR_USERNAME/claude-km-skill.git ~/.claude/skills/claude-km-skill
~/.claude/skills/claude-km-skill/scripts/init.sh .
\`\`\`
```

## Repository Structure

```
claude-km-skill/
├── .git/                       # Git history
├── .gitignore
├── LICENSE                     # MIT
├── README.md                   # Documentation
├── SKILL.md                    # Skill definition
├── SETUP.md                    # This file
├── AUTO-CAPTURE.md             # Auto-capture documentation
├── hooks.json                  # Hook configurations
├── scripts/
│   ├── init.sh                 # Setup script (with path validation)
│   ├── auto-capture.sh         # Auto session capture
│   ├── ai-capture.sh           # AI-powered capture
│   ├── claude-wrap.sh          # Claude wrapper
│   └── notify.sh               # macOS notification (with input sanitization)
├── references/
│   ├── mem-template.md
│   ├── distill-template.md
│   ├── td-template.md
│   └── improve-workflow.md
└── assets/
    └── commands/
        ├── README.md
        ├── mem.md
        ├── distill.md
        ├── td.md
        ├── improve.md
        ├── commit.md
        ├── focus.md
        ├── recap.md
        └── review.md
```
