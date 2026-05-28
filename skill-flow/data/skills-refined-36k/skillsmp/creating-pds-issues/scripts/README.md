# Creating PDS Issues - Scripts

Helper scripts for the `creating-pds-issues` skill.

## Scripts

### cache-templates.mjs

Fetches and caches NASA-PDS issue templates from the `.github` repository.

**Usage:**
```bash
node scripts/cache-templates.mjs [--force]
```

**Options:**
- `--force` - Force refresh even if cache is recent (< 7 days old)

**What it does:**
- Fetches all issue templates from NASA-PDS/.github repository
- Stores them locally in `resources/templates/`
- Creates a timestamp file to track cache age
- Templates are cached for 7 days to reduce GitHub API calls

**Output:**
Templates are saved to:
- `resources/templates/-bug_report.yml`
- `resources/templates/i-t-bug-report.yml`
- `resources/templates/-feature_request.yml`
- `resources/templates/-vulnerability-issue.yml`
- `resources/templates/task.yml`
- `resources/templates/release-theme.yml`
- `resources/templates/config.yml`
- `resources/templates/.cache-timestamp`

---

### detect-repo.mjs

Detects if the current directory is a NASA-PDS repository.

**Usage:**
```bash
node scripts/detect-repo.mjs
```

**Output (JSON):**
```json
{
  "detected": true,
  "repo": "pds-registry",
  "org": "NASA-PDS",
  "url": "https://github.com/NASA-PDS/pds-registry.git",
  "remote": "origin"
}
```

For forked repositories:
```json
{
  "detected": true,
  "repo": "pds-registry",
  "org": "NASA-PDS",
  "url": "https://github.com/NASA-PDS/pds-registry.git",
  "remote": "upstream",
  "note": "Detected from upstream (origin is a fork)"
}
```

Or if not in a NASA-PDS repo:
```json
{
  "detected": false,
  "reason": "Not in a git repository"
}
```

**What it does:**
- Checks `git remote get-url origin` first
- Falls back to `git remote get-url upstream` if origin doesn't exist
- If origin is a personal fork, checks upstream for NASA-PDS repository
- Parses the URL to extract organization and repository name
- Validates that the organization is `NASA-PDS`
- Handles both HTTPS and SSH remote URLs

---

### create-issue.mjs

Helper script for creating GitHub issues with formatted templates.

**Usage:**
```bash
node scripts/create-issue.mjs <type> <repo> <title> <data.json>
```

**Arguments:**
- `type` - Template type: `bug`, `feature`, `task`, `vulnerability`, `theme`
- `repo` - Repository name (without `NASA-PDS/` prefix)
- `title` - Issue title
- `data.json` - JSON file containing template field data

**Example:**
```bash
node scripts/create-issue.mjs bug pds-registry "Validator fails on nested tables" bug-data.json
```

**Data File Format:**

For bug reports (`bug-data.json`):
```json
{
  "description": "When validating a PDS4 label with nested tables...",
  "expectedBehavior": "Validator should successfully validate...",
  "reproductionSteps": [
    "Create PDS4 label with 3 nested tables",
    "Run: validate my-label.xml",
    "Observe error"
  ],
  "environment": [
    "Version: v1.2.3",
    "OS: macOS 13.0"
  ],
  "version": "v1.2.3",
  "testData": "See attached label file",
  "relatedRequirements": "#123"
}
```

For feature requests:
```json
{
  "personas": "Data Engineer, Node Operator",
  "motivation": "validate labels in CI/CD pipelines without manual intervention",
  "additionalDetails": "This would reduce deployment time from hours to minutes"
}
```

For tasks:
```json
{
  "taskType": "Sub-task",
  "description": "Refactor the validation module to use the new API"
}
```

**What it does:**
- Formats the issue body according to the template structure
- Applies appropriate labels and assignees
- Creates the issue via GitHub CLI (`gh issue create`)
- Returns the issue URL

---

## Prerequisites

All scripts require:
- **Node.js v18+**
- **GitHub CLI (`gh`)** installed and authenticated

Verify prerequisites:
```bash
node --version
gh --version
gh auth status
```

## Development

These scripts are designed to be used by the `creating-pds-issues` skill, but can also be run independently for testing or automation purposes.
