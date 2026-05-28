# Issue Management Framework Reference

This skill generates GitHub issues from spec documents.

## Issue Types & Hierarchy

```
Initiative (months)
├── Feature (weeks)
│   └── Task (days)
└── Bug (varies)
```

## Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Initiative | `[Area] Initiative name` | `[Auth] User authentication system` |
| Feature | `[Component] Feature verb-noun` | `[Login] Add OAuth support` |
| Task | `Verb specific action` | `Create login form component` |

## Labels

- `type:initiative`, `type:feature`, `type:task`, `type:bug`
- `priority:critical`, `priority:high`, `priority:medium`, `priority:low`
- `status:backlog`, `status:ready`, `status:in-progress`, `status:blocked`

## This Skill's Role

Automates issue draft generation from spec documents:

1. Extracts content from specs
2. Applies appropriate templates
3. Generates properly-formatted issue drafts
4. Creates helper scripts for issue creation

## Requirements

- GitHub CLI (`gh`) installed and authenticated
- Optional: `gh sub-issue` extension for hierarchy: `gh extension install yahsan2/gh-sub-issue`
