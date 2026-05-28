---
name: local-repo-check
description: Verify implementation status by scanning local Git repositories for code, tests, and commit history. Use when checking if a feature is actually implemented.
---

## Purpose

Scan local Git repositories to verify implementation status of components/features. Returns evidence-based status levels.

## When to Use

- Directly invoked: `/local-repo-check authentication`
- Checking if a component has code in the codebase
- Verifying implementation claims against actual code
- Determining "In Progress" vs "Complete" status
- When invoked by other skills (like `/project-status`)

## Input

Component or feature name(s) to verify. Examples:
- `/local-repo-check authentication`
- `/local-repo-check user-dashboard payments`

---

## Repository Configuration

Before scanning, look for repository configuration:

### Step 1: Check for Config Files

Use the Read tool to check if these files exist in the current working directory:
- `.entourage/repos.json` - shared repo metadata (name, mainBranch, github)
- `.entourage/paths.local.json` - personal local filesystem paths

### Step 2: Parse repos.json

If the file exists, it contains a `repos` array. Each repo has:
- `name`: Human-readable identifier
- `mainBranch`: Branch name for "shipped" status (default: "main")

Example `.entourage/repos.json`:
```json
{
  "repos": [
    {
      "name": "my-web-app",
      "mainBranch": "main",
      "github": "my-org/my-web-app"
    }
  ]
}
```

### Step 3: Parse paths.local.json

If the file exists, it contains a mapping of repo names to local paths:

Example `.entourage/paths.local.json`:
```json
{
  "my-web-app": "~/Documents/code/my-web-app"
}
```

### Step 4: Merge Configurations

For each repo in `repos.json`:
1. Look up the path by repo `name` in `paths.local.json`
2. If path found: proceed with expansion and verification
3. If path not found: mark as needing discovery

### Step 5: Auto-Discovery (Fallback)

**Only run this step if some repos are missing paths.**

For repos without configured paths, use the discovery script to find them:

```bash
echo '{"repos":[{"name":"repo-name","github":"org/repo"}]}' | /path/to/plugin/scripts/discover-repos.sh
```

The script searches:
- Sibling directories (`../*/`)
- Common locations: `~/code/*`, `~/dev/*`, `~/projects/*`, `~/src/*`

**Matching:** Uses git remote URL validation (not directory name), so it correctly identifies repos even if cloned with different names.

**If repos are discovered:**
1. Use the discovered paths for scanning
2. After completing the scan, offer to save the discovered paths:
   ```
   Discovered local paths for: repo-a, repo-b
   Save to .entourage/paths.local.json? [y/N]
   ```
3. If user confirms, write paths.local.json (creates if needed, merges with existing)

**If repos cannot be found:**
- Report: "Repository 'name' not found locally. Clone from github.com/org/repo or configure path in .entourage/paths.local.json"
- Continue with other repos

### Step 6: Expand Paths

Replace `~` with the user's home directory using Bash:
```bash
echo ~/path/to/repo
```

### Step 7: Verify Access

For each repo with a configured path, confirm the path exists:
```bash
test -d "/expanded/path" && echo "exists" || echo "missing"
```

---

## Scanning Workflow

For each component/feature being queried, perform these checks against each configured repository:

### 1. File Existence Check

Use Glob to find files matching the component name. Convert the component name to multiple naming conventions and search for each:

**Naming Convention Conversion:**
- Original: Use the component name as provided (e.g., `UserAuth`)
- snake_case: Convert to lowercase with underscores (e.g., `user_auth`)
- kebab-case: Convert to lowercase with hyphens (e.g., `user-auth`)
- lowercase: Simple lowercase (e.g., `userauth`)

**Search patterns (run all four):**
```
**/*UserAuth*        (original)
**/*user_auth*       (snake_case)
**/*user-auth*       (kebab-case)
**/*userauth*        (lowercase)
```

### 2. Test File Detection

Search for test files using the same naming convention conversions:
```
**/*ComponentName*.test.*
**/*ComponentName*.spec.*
**/*component_name*.test.*
**/*component_name*.spec.*
**/*component-name*.test.*
**/*component-name*.spec.*
**/test*/*ComponentName*
**/test*/*component_name*
**/__tests__/*ComponentName*
**/__tests__/*component_name*
```

### 3. Git History Analysis

Check recent commits mentioning the component:
```bash
cd /path/to/repo && git log --oneline --all --since="3 months ago" --grep="ComponentName" | head -20
```

Check for feature branches:
```bash
cd /path/to/repo && git branch -a | grep -i "component"
```

Check if component code is on main branch:
```bash
cd /path/to/repo && git log main --oneline -- "**/ComponentName*" | head -5
```

### 4. Migration/Schema Detection (for database components)

Look for migration files:
```
**/migrations/*component*
**/db/*component*
```

---

## Evidence Synthesis

Apply this decision tree to determine component status:

```
1. Code + tests found + on main branch?
   YES -> Status: Done (High confidence)

2. Code + tests found (any branch)?
   YES -> Status: Done (Medium confidence)

3. Code found but no tests?
   YES -> Status: In Progress (Medium confidence)

4. Feature branch exists with commits?
   YES -> Status: In Progress (Low confidence)

5. No code evidence found?
   -> Status: Unknown
```

---

## Error Handling

### Repository Not Found
If a configured repo path doesn't exist:
- Report in output: "Repository 'name' not accessible at path"
- Continue with other repos
- Don't fail the entire scan

### Git Command Failures
If git commands fail (not a git repo, permissions):
- Report: "Could not access git history for 'name'"
- Fall back to file existence checks only

### Path Expansion Failures
If `~` expansion fails:
- Try `$HOME/rest/of/path` as fallback
- Report: "Could not expand path for 'name'"

---

## Output Format

### With Repository Configuration

```
## Repository Scan: [Component Name]

| Repository | Evidence | Status | Confidence |
|------------|----------|--------|------------|
| [repo-name] | [Brief evidence summary] | Done/In Progress/Unknown | High/Med/Low |

### Scan Details

**[repo-name]:**
- File found: `path/to/file.tsx`
- Test found: `path/to/file.test.tsx`
- Git status: On main branch, last commit X days ago
```

### Without Repository Configuration

```
## Repository Scan

No repository configuration found. Create `.entourage/repos.json` to enable code scanning.

See the plugin README for configuration instructions.
```

### Multiple Components

When checking multiple components, output a summary table followed by details for each:

```
## Repository Scan Summary

| Component | Status | Source | Confidence |
|-----------|--------|--------|------------|
| auth | Done | entourage-web | High |
| dashboard | In Progress | entourage-web | Medium |
| payments | Unknown | - | - |

### Details

[Per-component scan details...]
```

## Example

**Query:** `/local-repo-check clerk-auth`

**Output:**

```
## Repository Scan: clerk-auth

| Repository | Evidence | Status | Confidence |
|------------|----------|--------|------------|
| entourage-web | Code + tests on main | Done | High |

### Scan Details

**entourage-web:**
- File found: `src/auth/ClerkProvider.tsx`
- Test found: `src/auth/__tests__/ClerkProvider.test.tsx`
- Git status: On main branch, last commit 2 days ago
- Related commits: "Add Clerk authentication provider" (abc1234)
```

---

## After Output

This skill returns results to the calling context (usually `/project-status`). **Do not stop execution.**
Continue with the next step in the workflow or TODO list.
