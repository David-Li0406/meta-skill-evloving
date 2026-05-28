# Repository Analysis & Exploration (Repomix)

*Expert Skill for Codebase Intelligence*

## Overview
Using **Repomix** (formerly known as `repomix` or `repomix-cli`) is the gold standard for packing a repository into a single, token-optimized file for LLM analysis.

## Core Commands

### 1. Remote Repository Analysis
```bash
npx repomix@latest --remote <owner/repo> --output /tmp/repo-pack.xml
```

### 2. Local Directory Analysis
```bash
npx repomix@latest [path/to/dir] --output repomix-output.xml
```

## 2026 Optimized Workflow

### Step 1: Pack with Compression
For large repositories (>500 files), always use compression to save 70%+ tokens.
```bash
npx repomix@latest --compress --output /tmp/compressed-pack.xml
```

### Step 2: Intelligent Search (Grep)
Instead of reading the whole XML, search for specific architectural patterns.
```bash
# Find all Use Cases
grep -n "UseCase" /tmp/repo-pack.xml

# Find Domain Entities
grep -n "class .*Entity" /tmp/repo-pack.xml
```

## Metrics and Evaluation
- **Token Count**: Repomix provides an estimated token count. Use this to decide if you need to further filter the include/exclude patterns.
- **Security Check**: Repomix automatically excludes `.env`, `node_modules`, and secret keys.

## Integration with Architect-Pro
When refactoring a system, use Repomix to get a holistic view of the existing "spaghetti" code before applying Clean Architecture or DDD patterns.
