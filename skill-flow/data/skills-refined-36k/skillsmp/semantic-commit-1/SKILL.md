---
name: semantic-commit
description: Generate semantic commit messages following conventional commit format for agentconfig.org. Use when creating commits, reviewing staged changes, or when the user asks for help with commit messages.
---

# Semantic Commit

Create clean, semantic git commits following strict commit discipline.

## Commit Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

## Types

| Type | When to Use |
|------|-------------|
| `feat` | New feature or functionality |
| `fix` | Bug fix |
| `docs` | Documentation changes only |
| `style` | Formatting, whitespace (no code logic change) |
| `refactor` | Code restructuring without behavior change |
| `test` | Adding or updating tests |
| `chore` | Maintenance, configs, dependencies |

## Scopes (Project-Specific)

Common scopes for agentconfig.org:
- `file-tree` - FileTree component/visualization
- `cards` - PrimitiveCards component
- `comparison` - ProviderComparison component
- `hero` - Hero section
- `navigation` - Navigation component
- `theme` - ThemeProvider, ThemeToggle, dark/light mode
- `data` - Data files in site/src/data/
- `e2e` - Playwright tests
- `skills` - Skill files in .github/skills/

## Rules

### 1. Atomic Commits
Each commit must represent ONE logical change. If you're tempted to use "and" in your description, split it into multiple commits.

```
# Bad
feat(ui): add file tree component and update navigation

# Good - Two separate commits
feat(file-tree): add collapsible tree node component
fix(navigation): update scroll offset for new header
```

### 2. Minimize Files
Prefer multiple small commits over one large commit. Ask: "Can this be split further?"

### 3. Clear Descriptions
The description should complete: "This commit will..."
- Use imperative mood: "add", "fix", "update" (not "added", "fixes")
- Be specific but concise
- No period at the end

### 4. Pre-Commit Verification

Before committing, verify:
1. `bun run lint` passes
2. `bun run typecheck` passes
3. `bun run test` passes
4. Only intended files are staged
5. No debug code or console.logs (unless intentional)

## Workflow

When asked to commit:

1. **Review changes** with `git status` and `git diff --staged`
2. **Assess scope** - Determine if this should be one or multiple commits
3. **Unstage if needed** - If changes span multiple features, commit separately
4. **Write message** following the format
5. **Verify** - Run lint, typecheck, and tests
6. **Commit** only after verification passes

## Good Examples

```
feat(file-tree): add TreeNode component with expand/collapse
chore(deps): add @radix-ui/react-collapsible
test(navigation): verify smooth scroll to sections
fix(theme): use correct tan background in light mode
refactor(hooks): extract theme logic to useTheme hook
docs(readme): add development setup instructions
```

## Bad Examples

```
update stuff                           # Too vague
feat: add everything                   # Too broad
WIP                                    # Incomplete work
fix(ui): fixed the bug                 # Past tense, vague
feat(tree): Add tree. And cards.       # Multiple changes, period
```

## Multi-File Commits

When changes span multiple areas:
1. Can this be split into separate commits?
2. If not, use the most significant scope
3. List additional changes in the commit body

```
feat(file-tree): add expand/collapse functionality

Also updates:
- TreeNode component styling
- FileTree section layout
```
