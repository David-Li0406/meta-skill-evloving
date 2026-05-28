# pattern discovery

git-native pattern extraction from mature convex projects. discovers and scores projects, extracts patterns, integrates into loop Phase 0.

## overview

dynamically discover "most mature" convex projects in `~/Developer/`, score by commits/tests/quality, extract patterns for TDD, file structure, schema, commit style, and imports. works even with just 1 project.

## architecture

```
~/.loop/
├── discovered-projects.json    # scored projects
└── patterns/
    ├── file-structure.md
    ├── test-patterns.md
    ├── convex-schema.md
    ├── commit-style.md
    └── import-patterns.md
```

## maturity scoring

**0-100 point scale**:

| category | points | criteria |
|----------|--------|----------|
| commit activity | 0-30 | commits in last 3 months |
| test coverage | 0-30 | number of test files |
| code quality | 0-20 | turbo, prettier, eslint, vitest, playwright |
| documentation | 0-10 | README, CONTRIBUTING |
| recency | 0-10 | days since last commit |

**thresholds**:
- **50+**: mature, extract all patterns
- **30-49**: developing, use selectively
- **< 30**: immature, skip

## usage

### discover projects

```bash
cd ~/Developer/skills/skills/loop/scripts

# discover all convex projects
./discover-projects.sh

# custom base directory
./discover-projects.sh /path/to/projects

# outputs to ~/.loop/discovered-projects.json
```

### extract patterns

```bash
# extract from projects scoring 50+
./extract-patterns.sh

# custom minimum score
./extract-patterns.sh ~/.loop/discovered-projects.json ~/.loop/patterns 40
```

### integrated bootstrap

```bash
# enhanced Phase 0 bootstrap with patterns
./bootstrap-with-patterns.sh

# or from loop skill context
source scripts/bootstrap-with-patterns.sh
```

## pattern types

### 1. file structure

```bash
./scripts/extract-file-structure.sh
```

extracts:
- root structure
- turborepo layout (apps/, packages/)
- convex directory organization
- test file locations

**output**: `~/.loop/patterns/file-structure.md`

### 2. test patterns

```bash
./scripts/extract-test-patterns.sh
```

extracts:
- test file naming (*.test.ts vs *.spec.ts)
- test location (co-located vs __tests__/)
- convex-test patterns
- react testing library patterns

**output**: `~/.loop/patterns/test-patterns.md`

### 3. convex schema

```bash
./scripts/extract-convex-schema.sh
```

extracts:
- schema structure
- index patterns
- auth patterns (clerk)
- field types and validators

**output**: `~/.loop/patterns/convex-schema.md`

### 4. commit style

```bash
./scripts/extract-commit-style.sh
```

extracts:
- commit message prefixes
- conventional commits usage
- imperative mood patterns
- your personal style from AGENTS.md

**output**: `~/.loop/patterns/commit-style.md`

### 5. import patterns

```bash
./scripts/extract-import-patterns.sh
```

extracts:
- convex function imports
- react component imports
- path aliases (@/*, @/components/*)
- barrel exports

**output**: `~/.loop/patterns/import-patterns.md`

### 6. lint patterns

```bash
./scripts/extract-lint-patterns.sh
```

extracts:
- Biome configuration
- ESLint configuration (.eslintrc.*, eslint.config.js)
- Rules and plugins

**output**: `~/.loop/patterns/lint-patterns.md`

## integration with loop

### Phase 0 enhancement

replace standard bootstrap in loop SKILL.md with:

```bash
# Enhanced Phase 0 with pattern discovery
source scripts/bootstrap-with-patterns.sh
```

**behavior**:
1. runs standard project detection
2. if convex project, checks for patterns
3. if patterns missing/stale, discovers and extracts
4. shows pattern summary inline
5. continues with standard bootstrap

### pattern lifecycle

| age | action |
|-----|--------|
| < 7 days | use cached patterns |
| 7-30 days | warn stale, use cached |
| > 30 days | auto-refresh on next bootstrap |

### graceful degradation

- **no patterns**: continues with standard bootstrap
- **no projects**: creates empty patterns (no errors)
- **single project**: extracts from that project (min score 0)
- **discovery fails**: logs warning, continues

## storage format

### discovered-projects.json

```json
[
  {
    "name": "arbor-xyz",
    "path": "/Users/luke/Developer/arbor/arbor-xyz",
    "score": 85,
    "metadata": {
      "commits_total": 450,
      "commits_3mo": 120,
      "test_files": 45,
      "convex_functions": 23,
      "last_commit": "2025-12-17 10:23:45 -0800",
      "days_since_commit": 1,
      "has_turbo": true,
      "has_tests": true,
      "has_vitest": true,
      "has_playwright": true
    }
  }
]
```

### pattern markdown

each pattern file:
```markdown
# Pattern Name

Extracted from mature Convex projects on 2025-12-18

## project-name-1

### Category
[extracted content]

## project-name-2

### Category
[extracted content]

## Common Patterns

[synthesized patterns across projects]
```

## examples

### Example 1: fresh workspace

```bash
# first time running
./discover-projects.sh
# 🔍 Discovering Convex projects...
# 📊 Found 5 Convex projects, scoring maturity...
# ✅ Discovery complete

./extract-patterns.sh
# 🎯 Extracting patterns from projects (min score: 50)...
# 📁 Analyzing 3 projects...
# ✅ Pattern extraction complete!

# patterns now available at ~/.loop/patterns/
```

### Example 2: loop integration

```bash
# in loop Phase 0
./scripts/bootstrap-with-patterns.sh

# === Pattern-Enhanced Bootstrap ===
# === Project Detection ===
# Project type: convex
# 
# === Pattern Discovery Check ===
# ✅ Fresh patterns found (< 7 days old)
# Patterns available:
# file-structure.md
# test-patterns.md
# convex-schema.md
# commit-style.md
# import-patterns.md
# 
# === Project Patterns Summary ===
# 📁 File Structure Pattern:
# [shows common structure]
# 
# [continues with standard bootstrap...]
```

### Example 3: single project

```bash
# only one convex project exists
./discover-projects.sh
# 📊 Found 1 Convex projects, scoring maturity...

./extract-patterns.sh ~/.loop/discovered-projects.json ~/.loop/patterns 0
# 🎯 Extracting patterns from projects (min score: 0)...
# 📁 Analyzing 1 projects...
# ✅ Pattern extraction complete!

# still generates useful patterns from that one project
```

## maintenance

### refresh patterns

```bash
# manual refresh
rm -rf ~/.loop/patterns
./discover-projects.sh && ./extract-patterns.sh

# or just re-run discovery
./discover-projects.sh && ./extract-patterns.sh
```

### inspect discovery

```bash
# view all discovered projects
cat ~/.loop/discovered-projects.json | jq '.'

# view top 3 by score
cat ~/.loop/discovered-projects.json | jq 'sort_by(.score) | reverse | .[0:3]'

# view projects with tests
cat ~/.loop/discovered-projects.json | jq '.[] | select(.metadata.has_tests == true)'
```

### debug patterns

```bash
# check pattern age
ls -lh ~/.loop/patterns/

# view specific pattern
cat ~/.loop/patterns/commit-style.md

# re-extract single pattern type
./scripts/extract-test-patterns.sh "$(cat ~/.loop/discovered-projects.json | jq -r '.[].path' | tr '\n' ' ')" > ~/.loop/patterns/test-patterns.md
```

## philosophy

**git-native**: no external databases, no APIs, pure git/fs operations

**zero-config**: works out of the box, discovers your workspace

**graceful**: never blocks, degrades to standard bootstrap

**fresh**: auto-refreshes stale patterns

**extensible**: add new pattern extractors easily

## anti-patterns

- **don't** run discovery on every bootstrap (use cached)
- **don't** require patterns to exist (graceful fallback)
- **don't** hard-code project paths (discover dynamically)
- **don't** fail on missing projects (work with 0 or 1)
- **don't** depend on external tools (pure bash/git)

## future enhancements

- extract CI/CD patterns from .github/workflows
- extract monorepo config patterns (turbo.json)
- extract middleware patterns from convex/http.ts
- ML-based pattern similarity scoring
- cross-project dependency analysis
