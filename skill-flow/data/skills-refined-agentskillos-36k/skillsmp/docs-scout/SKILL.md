---
name: docs-scout
description: Find the most relevant framework and library documentation pages for implementing a feature correctly. Use when you need official API references, version-specific guidance, or examples from documentation.
---

# Docs Scout

Documentation scout to find the exact documentation pages needed to implement a feature correctly.

**Role**: Documentation finder
**Purpose**: Find official docs needed during implementation
**Current year**: 2026 (use for search queries)

## Tool Requirements

**Required tools**: WebSearch, FetchUrl (WebFetch)

**Degradation strategy** (if tools unavailable):
```
Web tools not available. Please visit these URLs manually:

1. Framework docs:
   - React: https://react.dev
   - Next.js: https://nextjs.org/docs
   - Express: https://expressjs.com
   - Django: https://docs.djangoproject.com

2. Check package versions:
   cat package.json | grep '"<package>"'

3. GitHub source:
   https://github.com/<owner>/<repo>/tree/main/src
```

## Search Strategy

### 1. Identify dependencies (quick scan)
- Check package.json, pyproject.toml, Cargo.toml, etc.
- Note framework and major library versions
- Version matters - docs change between versions

### 2. Find primary framework docs
- Go to official docs site first
- Find the specific section for this feature
- Look for guides, tutorials, API reference

### 3. Find library-specific docs
- Each major dependency may have relevant docs
- Focus on integration points with the framework

### 4. Look for examples
- Official examples/recipes
- GitHub repo examples folders
- Starter templates

### 5. Dive into source when docs fall short
```bash
# Search library source for specific API
gh search code "useEffect cleanup" --repo facebook/react --json path -L 5

# Check for known issues
gh search issues "error message" --repo facebook/react --json title,url -L 5
```

## WebFetch Strategy

Do not just link - extract the relevant parts:

```
WebFetch: https://nextjs.org/docs/app/api-reference/functions/cookies
Prompt: "Extract the API signature, key parameters, and usage examples for cookies()"
```

## Source Quality Signals

When citing GitHub sources, prefer:
- Official repos (org matches package name)
- Recent activity (pushed within 6 months)
- Source over forks
- Relevant paths: `src/`, `packages/`, `lib/`
- Closed issues with solutions over open issues

## Output Format

```markdown
## Documentation for [Feature]

### Primary Framework
- **[Framework] [Version]**
  - [Topic](url) - [what it covers]
    > Key excerpt or API signature

### Libraries
- **[Library]**
  - [Relevant page](url) - [why needed]

### Source References
- `[repo]/[path]` - [what it reveals that docs don't]
  > Key code snippet

### Known Issues
- [Issue title](url) - [relevance, workaround if any]

### Examples
- [Example](url) - [what it demonstrates]

### API Quick Reference
```[language]
// Key API signatures extracted from docs
```

### Version Notes
- [Any version-specific caveats]
```

## Rules

- Version-specific docs when possible (e.g., Next.js 14 vs 15)
- Extract key info inline - do not just link
- Prioritize official docs over third-party tutorials
- Source dive when docs are insufficient - cite file:line
- Check GitHub issues for known problems with the feature
- Include API signatures for quick reference
- Note breaking changes if upgrading
- Skip generic "getting started" - focus on the specific feature
- Keep code snippets to <10 lines

## Verification

````bash
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
if [ -z "$REPO_ROOT" ]; then
  echo "Error: Set REPO_ROOT=/absolute/path/to/repo"
  exit 1
fi

ls "$REPO_ROOT/.factory/skills/docs-scout/SKILL.md"
# Expected: file exists, exit code 0
````
