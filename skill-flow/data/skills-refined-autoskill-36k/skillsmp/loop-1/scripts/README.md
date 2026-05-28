# Pattern Discovery Scripts

bash scripts for discovering and extracting patterns from Convex projects.

## scripts

### discover-projects.sh

finds all Convex projects and scores them by maturity.

```bash
./discover-projects.sh [base_dir]

# default: ~/Developer
# output: ~/.loop/discovered-projects.json
```

**scoring**:
- commit activity (0-30)
- test coverage (0-30)
- code quality (0-20)
- documentation (0-10)
- recency (0-10)

### extract-patterns.sh

orchestrates pattern extraction from top-scoring projects.

```bash
./extract-patterns.sh [discovery_file] [output_dir] [min_score]

# defaults:
# discovery_file: ~/.loop/discovered-projects.json
# output_dir: ~/.loop/patterns
# min_score: 50
```

runs all pattern extractors and outputs markdown files.

### extract-file-structure.sh

extracts directory layout patterns.

```bash
echo "/path/to/project1 /path/to/project2" | ./extract-file-structure.sh
```

### extract-test-patterns.sh

extracts test naming and structure patterns.

```bash
echo "/path/to/project1 /path/to/project2" | ./extract-test-patterns.sh
```

### extract-convex-schema.sh

extracts Convex schema patterns.

```bash
echo "/path/to/project1 /path/to/project2" | ./extract-convex-schema.sh
```

### extract-commit-style.sh

extracts commit message patterns.

```bash
echo "/path/to/project1 /path/to/project2" | ./extract-commit-style.sh
```

### extract-import-patterns.sh

extracts import/export patterns.

```bash
echo "/path/to/project1 /path/to/project2" | ./extract-import-patterns.sh
```

### bootstrap-with-patterns.sh

enhanced Phase 0 bootstrap with pattern integration.

```bash
./bootstrap-with-patterns.sh [project_root]

# or source it
source ./bootstrap-with-patterns.sh
```

## quick start

```bash
# first time setup
./discover-projects.sh && ./extract-patterns.sh

# verify
ls -lh ~/.loop/patterns/

# use in loop Phase 0 (automatic)
# patterns load when you bootstrap any Convex project
```

## output

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

### pattern files

each pattern extractor outputs markdown:
- structured by project
- includes common patterns section
- code examples
- best practices

## dependencies

**none** - pure bash + git

uses standard unix tools:
- find
- grep (or rg if available)
- git
- jq (optional, has fallback)

## maintenance

### refresh patterns

```bash
# weekly or after major project changes
./discover-projects.sh && ./extract-patterns.sh
```

### lower threshold

```bash
# extract from less mature projects
./extract-patterns.sh ~/.loop/discovered-projects.json ~/.loop/patterns 30
```

### single project

```bash
# extract from specific project
./discover-projects.sh /Users/luke/Developer/myproject
./extract-patterns.sh ~/.loop/discovered-projects.json ~/.loop/patterns 0
```

## see also

- [../references/pattern-discovery.md](../references/pattern-discovery.md) - full documentation
- [../references/pattern-discovery-quickstart.md](../references/pattern-discovery-quickstart.md) - usage guide
- [../SKILL.md](../SKILL.md) - loop skill with Phase 0 integration
