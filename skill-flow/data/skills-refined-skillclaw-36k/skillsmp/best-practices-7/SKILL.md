---
name: best-practices
description: Project-specific best practices - auto-loads based on detected project type
---

# Best Practices Skill

Comprehensive best practices with **40+ rules per framework**. Auto-activates based on project type and **auto-audits codebase** for violations.

## Activation Triggers

This skill activates automatically when:
- Working in a detected project type (React, Go, Flutter, FastAPI, Kotlin Spring)
- Writing or reviewing code
- Optimizing performance
- `/feature-dev` is invoked

## How It Works

1. **Auto-detect** project type (vite.config, go.mod, pubspec.yaml, build.gradle.kts with spring-webflux, etc.)
2. **Load** appropriate rules from templates directory (see paths below)
3. **Scan codebase** for anti-pattern violations using Grep
4. **Generate TodoWrite items** for detected issues
5. **Apply** rules throughout the session

## Template Locations

Templates are located at `${CLAUDE_PLUGIN_ROOT}/plugins/best-practices/skills/best-practices/templates/`. Each template is a directory containing `SKILL.md` with the full ruleset.

**Base Path**: `${CLAUDE_PLUGIN_ROOT}/plugins/best-practices/skills/best-practices/templates`

| Project Type | Template Path |
|-------------|---------------|
| react-vite | `${CLAUDE_PLUGIN_ROOT}/plugins/best-practices/skills/best-practices/templates/react-vite/SKILL.md` |
| nextjs | `${CLAUDE_PLUGIN_ROOT}/plugins/best-practices/skills/best-practices/templates/nextjs/SKILL.md` |
| go-gin | `${CLAUDE_PLUGIN_ROOT}/plugins/best-practices/skills/best-practices/templates/go-gin/SKILL.md` |
| flutter | `${CLAUDE_PLUGIN_ROOT}/plugins/best-practices/skills/best-practices/templates/flutter/SKILL.md` |
| python-fastapi | `${CLAUDE_PLUGIN_ROOT}/plugins/best-practices/skills/best-practices/templates/python-fastapi/SKILL.md` |
| kotlin-multiplatform | `${CLAUDE_PLUGIN_ROOT}/plugins/best-practices/skills/best-practices/templates/kotlin-multiplatform/SKILL.md` |
| kotlin-spring | `${CLAUDE_PLUGIN_ROOT}/plugins/best-practices/skills/best-practices/templates/kotlin-spring/SKILL.md` |

**To load rules**: Read the appropriate template SKILL.md using the full path above. The `${CLAUDE_PLUGIN_ROOT}` variable resolves to the plugin installation directory.

## Auto-Audit Mode

**IMPORTANT**: After loading rules, you MUST scan the codebase for violations using Grep.

### Quick Scan Patterns (MANDATORY)

For **React/Vite/Next.js** projects, scan for these CRITICAL patterns:

```bash
# Barrel file imports (CRITICAL)
Grep: pattern="from ['\"']@/components['\"]" glob="*.tsx,*.ts"

# Lodash full import (CRITICAL)
Grep: pattern="from ['\"']lodash['\"]" glob="*.tsx,*.ts"

# Inline style objects (HIGH)
Grep: pattern="style=\{\{" glob="*.tsx"
```

For **Go/Gin** projects:

```bash
# Ignored errors (CRITICAL)
Grep: pattern="json\.(Unmarshal|Marshal)\([^)]+\)$" glob="*.go"

# Unwrapped error returns (HIGH)
Grep: pattern="return nil, err$" glob="*.go"
```

For **Kotlin Multiplatform** projects:

```bash
# GlobalScope usage (CRITICAL)
Grep: pattern="GlobalScope\.(launch|async)" glob="*.kt"

# MutableStateFlow without asStateFlow (CRITICAL)
Grep: pattern="val.*MutableStateFlow" glob="*.kt"

# Missing @Immutable/@Stable annotations (HIGH)
Grep: pattern="data class.*\(" glob="*.kt"
```

For **Kotlin Spring** (Coroutines + WebFlux) projects:

```bash
# GlobalScope usage (CRITICAL)
Grep: pattern="GlobalScope\.(launch|async)" glob="*.kt"

# Blocking calls in suspend functions (CRITICAL)
Grep: pattern="Thread\.sleep" glob="*.kt"

# JDBC instead of R2DBC (CRITICAL)
Grep: pattern="JdbcTemplate|spring-boot-starter-jdbc" glob="*.kt,*.gradle.kts"

# Catching CancellationException (HIGH)
Grep: pattern="catch.*Exception\)" glob="*.kt"

# runBlocking in tests (MEDIUM)
Grep: pattern="runBlocking" glob="*Test.kt"
```

### Audit Workflow

1. **Run Grep** for each critical pattern above
2. **Report findings** with file:line format
3. **Group by severity**: 🔴 CRITICAL → 🟠 HIGH → 🟡 MEDIUM
4. **Create TodoWrite items** for CRITICAL and HIGH violations
5. **Show summary**: `💡 Fix with: /feature-workflow "fix: best-practice violations"`

### Skip Audit

Use `--no-audit` flag to load rules without scanning.

### Example Output

```
🔍 Detecting project type...
📁 Found: vite.config.ts

✅ best-practices loaded
Project: react-vite | Rules: 45+

🔎 Scanning codebase...
📂 Scanned: 127 files in 342ms

⚠️ Found 12 violations:

🔴 CRITICAL (2):
  ❌ [bundle-optimization] Barrel file imports
     src/components/index.ts:1

🟠 HIGH (5):
  ❌ [rerender-prevention] Missing useMemo
     src/hooks/useData.ts:23

📋 7 items added to TodoWrite

💡 Fix with: /feature-workflow "fix: best-practice violations"
```

### Filtering by Severity

Use `--severity` to report only violations at or above a threshold:
```bash
/best-practices:best-practices --severity HIGH
```

## Templates Available

| Project Type | Rules | Categories |
|-------------|-------|------------|
| react-vite | 45+ | 5 |
| nextjs | 45+ | 5 |
| go-gin | 48 | 8 |
| flutter | 42 | 8 |
| python-fastapi | 48 | 8 |
| kotlin-multiplatform | 44 | 8 |
| kotlin-spring | 48 | 8 |

See "Template Locations" section above for full paths.

## Rule Structure

Each template includes:
- **Priority levels**: CRITICAL → HIGH → MEDIUM → LOW
- **Rule prefixes**: For easy reference (e.g., `err-wrap`, `async-block`)
- **Quick Reference**: All rules at a glance
- **Examples**: Incorrect vs correct patterns

## React/Next.js Integration

For React/Next.js projects, best practices **extend `/vercel-react-best-practices`**:

```
/vercel-react-best-practices  ← Primary (45 Vercel rules)
     ↓
best-practices templates      ← Framework-specific additions
```

