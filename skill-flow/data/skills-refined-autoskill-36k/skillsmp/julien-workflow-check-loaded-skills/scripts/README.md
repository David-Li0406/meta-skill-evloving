# Scripts - Check Loaded Skills

## check-loaded-skills.sh

Bash script that checks which Claude Code skills are loaded.

### Usage

```bash
./check-loaded-skills.sh
```

### What it does

1. Lists all global skills from `~/.claude/skills/`
2. Categorizes by author (Hostinger, Anthropic, custom)
3. Checks for project-level skills in `.claude/skills/`
4. Displays counts and formatted output

### Output Sections

- **📦 SKILLS GLOBAUX**: All globally available skills
- **🏢 Skills Hostinger-specific**: Infrastructure skills for srv759970
- **🤖 Skills Anthropic**: Official Anthropic skills
- **📁 SKILLS PROJECT-LEVEL**: Project-specific overrides (if any)

### Requirements

- Bash shell (Git Bash on Windows)
- Access to `~/.claude/skills/` directory
- Read permissions

### Exit Codes

- `0`: Success
- (Script doesn't fail, always shows available info)
