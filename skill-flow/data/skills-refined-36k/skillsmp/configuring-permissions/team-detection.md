# Team vs Solo Project Detection

## Check Contributor Count

```bash
git shortlog -sne --all | head -10
```

## Decision Flow

```dot
digraph team_detection {
    "Modifying project .claude/ settings?" [shape=diamond];
    "Multiple contributors?" [shape=diamond];
    "Project CLAUDE.md has 'minimize-permission-prompts'?" [shape=diamond];
    "Proceed with user-level only" [shape=box];
    "Ask user: 'This affects team. Proceed?'" [shape=box];
    "Auto-configure based on enabled plugins" [shape=box];
    "Apply changes" [shape=box];

    "Modifying project .claude/ settings?" -> "Multiple contributors?" [label="yes"];
    "Modifying project .claude/ settings?" -> "Apply changes" [label="no"];
    "Multiple contributors?" -> "Project CLAUDE.md has 'minimize-permission-prompts'?" [label="yes"];
    "Multiple contributors?" -> "Apply changes" [label="no (solo)"];
    "Project CLAUDE.md has 'minimize-permission-prompts'?" -> "Auto-configure based on enabled plugins" [label="yes"];
    "Project CLAUDE.md has 'minimize-permission-prompts'?" -> "Ask user: 'This affects team. Proceed?'" [label="no"];
    "Ask user: 'This affects team. Proceed?'" -> "Apply changes" [label="approved"];
    "Ask user: 'This affects team. Proceed?'" -> "Proceed with user-level only" [label="declined"];
    "Auto-configure based on enabled plugins" -> "Apply changes";
}
```

## Project Preference

Add to project CLAUDE.md to enable auto-configuration:

```markdown
## Permissions
* minimize-permission-prompts: true
```

## Auto-Configuration Logic

When `minimize-permission-prompts: true` is set:

1. Read `.claude/settings.json` for `enabledPlugins`
2. Generate `Skill(plugin-name:*)` pattern for each enabled plugin
3. Add to `.claude/settings.local.json` (or committed settings if team shares)
4. Remember: `Skill(*)` doesn't work in project settings — must list individually

## Why This Matters

- User-level `Skill(*)` doesn't help teammates
- Team projects need project-level permissions
- Without this check, you might configure only for one user while breaking team workflow
