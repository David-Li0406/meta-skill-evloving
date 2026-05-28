---
name: dx-maintainability-reviewer
description: Evaluate how easy it is for new engineers to work in a codebase. Use when assessing code quality, onboarding friction, or technical debt. Triggers on "code quality", "maintainability", "developer experience", "DX review", "onboarding", "cognitive load", "code smell", "refactoring", "tech debt".
---

# DX & Maintainability Reviewer

Evaluate how easy it is for a new engineer to understand, modify, and work in this codebase. Focus on cognitive load, clarity, and sustainable development practices.

## Core Principle

> "Any fool can write code that a computer can understand. Good programmers write code that humans can understand." — Martin Fowler

## When to Use

- Onboarding new team members
- Reviewing code quality after feature work
- Assessing technical debt before sprints
- Evaluating codebases during due diligence
- Planning refactoring efforts
- Improving team velocity

## Review Workflow

### Step 1: First Impressions (New Engineer Simulation)

Approach the codebase as a new engineer would:

```
Questions a new engineer asks:
1. What does this project do? (README)
2. How do I run it locally? (Setup docs)
3. Where is the code for X? (Project structure)
4. How do I make a change? (Contribution guide)
5. What patterns should I follow? (Conventions)
6. Who do I ask for help? (Team/ownership)
```

Time yourself:
- [ ] Can find entry point in < 2 minutes?
- [ ] Can run locally in < 15 minutes?
- [ ] Can understand main flow in < 1 hour?

### Step 2: Structural Analysis

```bash
# Project structure overview
tree -L 3 -d --noreport

# File count by type
find . -type f -name "*.ts" | wc -l

# Largest files (complexity indicators)
find . -name "*.ts" -exec wc -l {} \; | sort -rn | head -20

# Most changed files (hotspots)
git log --pretty=format: --name-only | sort | uniq -c | sort -rn | head -20
```

### Step 3: Code Complexity Scan

```bash
# Long files (>500 lines)
find . -name "*.ts" -exec sh -c 'wc -l "$1" | awk "\$1 > 500 {print}"' _ {} \;

# Long functions (rough heuristic)
grep -rn "function\|async\|=>" --include="*.ts" -A 100 | head -200

# Deep nesting (many closing braces together)
grep -rn "}}}\|}}}}" --include="*.ts"

# TODO/FIXME/HACK count
grep -rn "TODO\|FIXME\|HACK\|XXX" --include="*.ts" | wc -l
```

### Step 4: Execute Checklist

See [CHECKLIST.md](CHECKLIST.md) for the complete maintainability checklist.
See [PATTERNS.md](PATTERNS.md) for common code smells and fixes.

## Output Format

### A) Developer Experience Score

```
┌─────────────────────────────────────────────────────────────┐
│                  DX SCORECARD                                │
├─────────────────────────────────────────────────────────────┤
│ Category              │ Score │ Notes                       │
├───────────────────────┼───────┼─────────────────────────────┤
│ Setup & Onboarding    │ [/10] │ [brief note]                │
│ Code Organization     │ [/10] │ [brief note]                │
│ Naming & Readability  │ [/10] │ [brief note]                │
│ Documentation         │ [/10] │ [brief note]                │
│ Testing               │ [/10] │ [brief note]                │
│ Error Messages        │ [/10] │ [brief note]                │
│ Tooling & Automation  │ [/10] │ [brief note]                │
├───────────────────────┼───────┼─────────────────────────────┤
│ OVERALL DX SCORE      │ [/70] │ [EXCELLENT/GOOD/FAIR/POOR]  │
└─────────────────────────────────────────────────────────────┘
```

### B) Cognitive Load Hotspots

Areas that require excessive mental effort to understand:

```
### :red_circle: HIGH COGNITIVE LOAD: [filename]

**Location:** `path/to/file.ts`
**Lines:** [count]
**Complexity indicators:**
- [indicator 1]
- [indicator 2]

**Why it's hard to understand:**
[Explanation]

**Suggested improvement:**
[Concrete suggestion]
```

Cognitive load causes:
| Cause | Example |
|-------|---------|
| **Length** | 1000+ line files, 100+ line functions |
| **Nesting** | 4+ levels of indentation |
| **Abstraction** | Excessive indirection, "magic" |
| **Coupling** | Changes here require changes everywhere |
| **Naming** | Unclear or misleading names |
| **Inconsistency** | Different patterns for same thing |

### C) Naming & Structure Problems

```
### NAMING: [Problem Title]

**Location:** `path/to/file.ts:123`
**Current:** `[current name]`
**Problem:** [Why it's confusing]
**Suggested:** `[better name]`
```

```
### STRUCTURE: [Problem Title]

**Location:** `path/to/directory/`
**Problem:** [What's wrong with structure]
**Suggested:** [Better organization]
```

### D) Missing Documentation

```
┌─────────────────────────────────────────────────────────────┐
│               DOCUMENTATION GAPS                             │
├─────────────────────────────────────────────────────────────┤
│ Document                    │ Status        │ Priority      │
├─────────────────────────────┼───────────────┼───────────────┤
│ README.md                   │ ⚠️ Incomplete │ HIGH          │
│ CONTRIBUTING.md             │ ❌ Missing    │ MEDIUM        │
│ Architecture overview       │ ❌ Missing    │ HIGH          │
│ API documentation           │ ✅ Present    │ -             │
│ Setup guide                 │ ⚠️ Outdated   │ HIGH          │
│ Deployment runbook          │ ❌ Missing    │ CRITICAL      │
│ Incident runbook            │ ❌ Missing    │ HIGH          │
│ ADR (decisions)             │ ❌ Missing    │ MEDIUM        │
└─────────────────────────────┴───────────────┴───────────────┘
```

For each missing critical document:
```
### MISSING: [Document Name]

**Why needed:** [Impact of not having it]
**Should contain:**
- [Section 1]
- [Section 2]
- [Section 3]

**Template:** [Link to template if available]
```

### E) Refactor Opportunities

```
┌─────────────────────────────────────────────────────────────┐
│              REFACTOR OPPORTUNITIES                          │
├──────────────┬──────────────┬────────────────────────────────┤
│ Priority     │ Effort       │ Opportunity                    │
├──────────────┼──────────────┼────────────────────────────────┤
│ HIGH         │ Medium       │ Extract OrderService from...   │
│ HIGH         │ Low          │ Rename confusing variables...  │
│ MEDIUM       │ High         │ Split monolithic file...       │
│ MEDIUM       │ Medium       │ Add error handling pattern...  │
│ LOW          │ Low          │ Remove dead code in...         │
└──────────────┴──────────────┴────────────────────────────────┘
```

For high-priority refactors:
```
### REFACTOR: [Title]

**Location:** `path/to/file.ts`
**Current state:** [What it looks like now]
**Problem:** [Why this needs to change]
**Proposed change:** [What to do]
**Effort:** [Low/Medium/High]
**Risk:** [Low/Medium/High]
**Dependencies:** [What else might need to change]
```

### F) Quick Wins

Changes that significantly improve DX with minimal effort:

```
QUICK WINS (< 1 hour each):
1. [ ] Add missing npm scripts for common tasks
2. [ ] Add .env.example with all required variables
3. [ ] Fix misleading error message in [file]
4. [ ] Add JSDoc to exported function [name]
5. [ ] Delete unused file [path]
```

### G) Summary & Recommendations

```
┌─────────────────────────────────────────────────────────────┐
│                    SUMMARY                                   │
├─────────────────────────────────────────────────────────────┤
│ Overall DX:          [EXCELLENT/GOOD/FAIR/POOR]             │
│ Onboarding time:     [estimate for new engineer]            │
│ Cognitive hotspots:  [count]                                │
│ Missing docs:        [count]                                │
│ Refactor debt:       [estimate: days/weeks]                 │
├─────────────────────────────────────────────────────────────┤
│ TOP 3 PRIORITIES:                                           │
│ 1. [Most impactful improvement]                             │
│ 2. [Second priority]                                        │
│ 3. [Third priority]                                         │
└─────────────────────────────────────────────────────────────┘
```

## Quick Commands

```bash
# Find largest files
find . -name "*.ts" -exec wc -l {} \; | sort -rn | head -10

# Find most complex files (by cyclomatic complexity proxy)
grep -rn "if\|else\|switch\|case\|for\|while\|catch\|&&\|||" --include="*.ts" -c | sort -t: -k2 -rn | head -10

# Find files with most imports (coupling)
grep -rn "^import" --include="*.ts" -c | sort -t: -k2 -rn | head -10

# Find TODO/FIXME
grep -rn "TODO\|FIXME" --include="*.ts" --include="*.tsx"

# Find commented-out code
grep -rn "^[[:space:]]*//.*function\|^[[:space:]]*//.*const\|^[[:space:]]*//.*if" --include="*.ts"

# Find magic numbers
grep -rn "[^a-zA-Z0-9][0-9][0-9][0-9][0-9]*[^a-zA-Z0-9]" --include="*.ts" | grep -v "test\|spec"

# Find any/unknown types (TypeScript)
grep -rn ": any\|as any\|<any>" --include="*.ts"

# Check for consistent naming
grep -rn "camelCase\|snake_case\|PascalCase" --include="*.ts" | head -20
```

## Resources

- [CHECKLIST.md](CHECKLIST.md) - Complete maintainability checklist
- [PATTERNS.md](PATTERNS.md) - Code smells and refactoring patterns
