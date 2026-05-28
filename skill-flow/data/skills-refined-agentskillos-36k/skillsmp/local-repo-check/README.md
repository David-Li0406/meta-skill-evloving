# local-repo-check Skill

Scans local Git repositories to verify implementation status of components/features.

## Overview

This skill checks local repositories for code evidence to determine if a component is actually implemented. It searches for:

1. **Source files** - Code matching the component name
2. **Test files** - Tests for the component
3. **Git history** - Commits and branches related to the component

## Status Levels

| Status | Evidence Required |
|--------|-------------------|
| Complete | Code + tests found on main branch |
| In Progress | Code found but no tests, or feature branch exists |
| Unknown | No code evidence found |

## When to Use

- Directly: `/local-repo-check authentication`
- Automatically invoked by `/project-status` when repos are configured

## Prerequisites

Repository configuration in `.entourage/repos.json`:

```json
{
  "repos": [
    {
      "name": "my-project",
      "github": "my-org/my-project",
      "mainBranch": "main"
    }
  ]
}
```

Optional path mapping in `.entourage/paths.local.json` (gitignored):

```json
{
  "my-project": "~/code/my-project"
}
```

## Auto-Discovery

When `paths.local.json` is missing or incomplete, the skill automatically discovers repository paths using git remote URL matching.

### How It Works

1. **Reads `repos.json`** to get the list of repos with their `github` fields (e.g., `"my-org/my-project"`)
2. **Scans common locations** for git repositories:
   - Sibling directories (`../*/`)
   - `~/code/*`, `~/dev/*`, `~/projects/*`, `~/src/*`
3. **Matches by git remote** - compares each directory's `origin` remote URL against the expected GitHub path
4. **Offers to save** discovered paths to `paths.local.json` for faster future scans

### Why Git Remote Matching?

Unlike directory name matching, git remote validation:
- Works when repos are cloned with different names
- Distinguishes forks from originals
- Never confuses similarly-named but unrelated repos

### Performance

- **With paths.local.json**: ~100ms (just file reads)
- **With auto-discovery**: ~1 second (filesystem scan + git checks)

To optimize repeated scans, save discovered paths when prompted.

## Testing the Skill

### Running Evaluations

1. Navigate to your context database:
   ```bash
   cd ~/my-context   # or ~/other-context
   ```

2. Start Claude Code with the plugin:
   ```bash
   claude --plugin-dir ~/your-plugin
   ```

3. Test directly:
   ```
   /local-repo-check authentication
   /local-repo-check user-dashboard payments
   ```

### Example Test Queries

| Test Case | Query |
|-----------|-------|
| Single component | `/local-repo-check auth` |
| Multiple components | `/local-repo-check auth dashboard payments` |
| Non-existent component | `/local-repo-check nonexistent-feature` |

### Expected Output Format

```markdown
## Repository Scan: auth

| Repository | Evidence | Status | Confidence |
|------------|----------|--------|------------|
| my-project | Code + tests on main | Complete | High |

### Scan Details

**my-project:**
- File found: `src/auth/AuthProvider.tsx`
- Test found: `src/auth/__tests__/AuthProvider.test.tsx`
- Git status: On main branch, last commit 2 days ago
```

## Naming Convention Search

The skill searches for files using multiple naming conventions:
- Original: `UserAuth`
- snake_case: `user_auth`
- kebab-case: `user-auth`
- lowercase: `userauth`

## Error Handling

| Error | Behavior |
|-------|----------|
| Repository not found | Reports error, continues with other repos |
| Git command fails | Falls back to file existence checks |
| No repos configured | Returns "No repository configuration found" message |

## Evaluation Logs

This skill is typically invoked by `/project-status`. Evaluation logs are stored with project-status results:

```
~/my-context/evaluations/project-status/
~/other-context/evaluations/project-status/
```

## Test Cases

See `evaluations/evaluation.json` for the full test suite covering:
- File existence checks
- Test file detection
- Git history analysis
- Multiple naming conventions
- Error scenarios
