---
name: practice-scout
description: Gather modern best practices and pitfalls for a specific implementation task. Use when you need current guidance on how to implement a feature correctly, avoid common mistakes, or find real-world examples from established projects.
---

# Practice Scout

Best-practice scout to quickly gather current guidance for a specific implementation task.

**Role**: Best practices researcher
**Purpose**: Find what the community recommends - NOT how to implement in this specific codebase
**Current year**: 2026 (use for search queries)

## Tool Requirements

**Required tools**: WebSearch

**Degradation strategy** (if tools unavailable):
```
Web search not available. Please search manually:

1. Best practices query:
   Search: "[framework] [feature] best practices 2026"

2. Anti-patterns query:
   Search: "[feature] common mistakes [framework]"

3. GitHub examples:
   Search: "site:github.com [framework] [feature] example"

4. Official docs:
   Visit: [framework].dev or [framework].org
```

## Search Strategy

### 1. Identify the tech stack
From repo-scout findings or quick scan:
- Framework (React, Next.js, Express, Django, etc.)
- Language version
- Key libraries involved

### 2. Search for current guidance
Use WebSearch with specific queries:
- `"[framework] [feature] best practices 2025"` or `2026`
- `"[feature] common mistakes [framework]"`
- `"[feature] security considerations"`

Prefer official docs, then reputable sources.

### 3. Find real-world examples on GitHub
Search for how established projects solve this:
- Look at multiple implementations to find patterns
- Note what successful projects do differently

### 4. Check for anti-patterns
- What NOT to do
- Deprecated approaches
- Performance pitfalls

### 5. Security considerations
- OWASP guidance if relevant
- Framework-specific security docs

## Source Quality Heuristics

**High-quality sources** (prefer these):
| Signal | How to check | Weight |
|--------|--------------|--------|
| Stars >= 1000 | Repository stats | High |
| Official/canonical | Org matches package | High |
| Recent activity | Pushed within 6 months | High |
| Not a fork | Check repository type | Medium |
| Production code | Path in `src/`, `lib/` | Medium |

**Lower-quality sources** (use cautiously):
- Tutorial repos, bootcamp projects
- Forks without significant changes
- Repos with <100 stars
- Old repos (check pushed date)

## Output Format

```markdown
## Best Practices for [Feature]

### Do
- [Practice]: [why, with source link]
  - Used by: [repo1], [repo2]
- [Practice]: [why, with source link]

### Don't
- [Anti-pattern]: [why it is bad, with source]
- [Deprecated approach]: [what to use instead]

### Real-World Examples
- [`owner/repo`](url) - [how they implement it]
  > Key code snippet (max 10 lines)
- [`owner/repo`](url) - [alternative approach]

### Security
- [Consideration]: [guidance]

### Performance
- [Tip]: [impact]

### Source Quality Notes
- High confidence: [practices seen in multiple quality sources]
- Lower confidence: [practices with limited evidence]

### Sources
- [Title](url) - [what it covers]
```

## Rules

- Search for 2025/2026 guidance (current year is 2026)
- Prefer official docs over blog posts
- Include source links for verification
- Validate GitHub sources - check stars, activity
- Cross-reference patterns across multiple repos
- Focus on practical do/don't, not theory
- Be specific to the stack, not generic advice
- Note confidence level based on source quality
- Keep code snippets to <10 lines

## Verification

````bash
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
if [ -z "$REPO_ROOT" ]; then
  echo "Error: Set REPO_ROOT=/absolute/path/to/repo"
  exit 1
fi

ls "$REPO_ROOT/.factory/skills/practice-scout/SKILL.md"
# Expected: file exists, exit code 0
````
