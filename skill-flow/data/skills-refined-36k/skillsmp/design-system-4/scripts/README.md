# Design System Scripts

Helper scripts for the design-system skill.

## find-hardcoded-colors.sh

Scans the codebase for hardcoded Tailwind color classes that should use CSS variables instead.

### Usage

```bash
# From project root
bash .agent/skills/design-system/scripts/find-hardcoded-colors.sh

# Or specify a directory
bash .agent/skills/design-system/scripts/find-hardcoded-colors.sh src/components
```

### What it finds

| Pattern | Example | Should Be |
|---------|---------|-----------|
| `bg-slate-*` | `bg-slate-900` | `bg-card` |
| `text-gray-*` | `text-gray-500` | `text-muted-foreground` |
| `border-zinc-*` | `border-zinc-700` | `border-border` |
| Hex colors | `#1e293b` | CSS variable |
| `dark:` prefix | `dark:bg-gray-900` | CSS variable with `:root` and `[data-theme="light"]` |

### Next Steps

After finding violations:
1. Replace with semantic CSS variables from globals.css
2. Ensure both light and dark variants exist
3. Test in both themes
