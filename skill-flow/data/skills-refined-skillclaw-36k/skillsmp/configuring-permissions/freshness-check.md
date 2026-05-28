# Freshness Check Procedure

## Find State File

```bash
# Works regardless of installation location
find ~/.claude/plugins -path "*/claude-code/skills/configuring-permissions/.state" 2>/dev/null | head -1
```

## Research Queries

Run these searches to find current permission-related issues:

```
site:github.com/anthropics/claude-code issues Skill permissions wildcard glob settings.json
site:github.com/anthropics/claude-code "plugin" "skill" permission allow settings
```

## Update Workflow

1. **Search** — Run research queries above
2. **Fetch** — Read relevant issue pages for details and workarounds
3. **Update SKILL.md Known Issues section** — Add/modify/remove issues based on findings
4. **Update .state** — Record today's date and issues reviewed

## State File Format

```json
{
  "last_evaluated": "YYYY-MM-DD",
  "cc_version_checked": "X.Y.Z or 'latest'",
  "issues_open": ["#6881", "#5140", "#10833", "#14956", "#13344"],
  "issues_fixed": ["#9814", "#8581", "#3107"],
  "issues_closed_other": ["#10093"]
}
```

**Refresh procedure:** Use `gh issue view <number> --repo anthropics/claude-code --json state,title,closedAt` to check each issue.

## Review User Settings

After updating knowledge, check user's current setup:

1. Read `~/.claude/settings.json`
2. Check projects listed in user's CLAUDE.md (Permissions section)
3. Compare against known issues — flag any problematic patterns
4. Suggest fixes if found
