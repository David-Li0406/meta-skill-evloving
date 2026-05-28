---
name: restructure-issue
description: Restructure existing GitHub issue to clarify problem definition
---

Restructure existing GitHub issue $ARGUMENTS to clarify problem definition

## Purpose

Transform vague/incomplete issues into format that `/work-on-issue` can work with effectively. Focus on problem clarity, not implementation.

## Process

1. Fetch issue details:
   - `gh issue view $ARGUMENTS --json title,body,comments`
2. Check completeness: problem definition, reproduction steps (bug), expected/actual behavior (bug), background/purpose (feature), environment info
3. Use AskUserQuestion for missing info
4. Create structured body using templates below
5. Improve title: `バグがある` → `[Bug] ログイン時に認証エラー`, `機能追加` → `[Feature] ダークモード対応`
6. Show to user for confirmation
7. Update issue (execute commands sequentially):
```bash
gh issue edit $ARGUMENTS --title "new title"
gh issue edit $ARGUMENTS --body "$(cat <<'EOF'
[new body]
EOF
)"
```
8. Show issue URL and suggest `/work-on-issue $ARGUMENTS`

## Templates

Use structure-issue templates (Bug/Feature/Enhancement sections), then append:
```
---
<details>
<summary>元の issue 内容</summary>
[original body]
</details>
```

## Notes

- Focus on problem definition, not implementation
- Preserve original content in collapsed section
- Respect original author's intent
- For issues under discussion, suggest changes in comment first
