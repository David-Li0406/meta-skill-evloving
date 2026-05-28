# Output Collapse (Limitation)

**Current state:** No way to control collapsed/expanded state of tool output.

## The Problem

Bash output collapses after ~3-4 lines with `+N lines (ctrl+o to expand)`.

## Workarounds

| Approach            | Effect                                             |
| ------------------- | -------------------------------------------------- |
| Accept collapse     | User presses ctrl+o to expand                      |
| Pre-computed assets | Read tool displays full file content (no collapse) |
| Simple text output  | Skip visual complexity, use plain text             |
| Status line         | Show brief progress there instead                  |

### Pre-computed Assets Pattern

Store visual output (ASCII banners, progress indicators) as static files. Use Read tool to display them - Read shows full content without collapsing.

```
my-skill/
├── SKILL.md
└── assets/
    ├── banner-start.txt
    ├── banner-complete.txt
    └── progress-template.txt
```

In SKILL.md:

```
To show the start banner, read and display:
.claude/skills/my-skill/assets/banner-start.txt
```

## Links

- [#11334](https://github.com/anthropics/claude-code/issues/11334) - Configurable collapse threshold (OPEN)
- [#12589](https://github.com/anthropics/claude-code/issues/12589) - Duplicate, closed
