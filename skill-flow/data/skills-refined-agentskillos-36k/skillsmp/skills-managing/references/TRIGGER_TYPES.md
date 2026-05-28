# Trigger Types - Complete Guide

Complete reference for configuring skill triggers in the Antigravity Skill Engine's auto-activation system.

## Table of Contents

- [Keyword Triggers (Explicit)](#keyword-triggers-explicit)
- [Intent Pattern Triggers (Implicit)](#intent-pattern-triggers-implicit)
- [File Path Triggers](#file-path-triggers)
- [Content Pattern Triggers](#content-pattern-triggers)
- [Best Practices Summary](#best-practices-summary)

---

## Keyword Triggers (Explicit)

### How It Works

Case-insensitive substring matching in user's prompt.

### Use For

Topic-based activation where user explicitly mentions the subject.

### Configuration

```json
"intent_keywords": ["layout", "grid", "toolbar", "submission"]
```

### Example

- User prompt: "how does the **layout** system work?"
- Matches: "layout" keyword
- Activates: corresponding skill

### Best Practices

- Use specific, unambiguous terms
- Include common variations ("layout", "layout system", "grid layout")
- Avoid overly generic words ("system", "work", "create")
- Test with real prompts

---

## Intent Pattern Triggers (Implicit)

### How It Works

Regex pattern matching to detect user's intent without explicit keywords.

### Use For

Catching implied intent that keywords might miss.

### Configuration

```json
"intentPatterns": [
  "(add|create|implement).*?(feature|endpoint|route)",
  "(how does|explain|what is).*?(work|function)"
]
```

### Pattern Tips

**Non-greedy matching:**
```regex
(create|add).*?(feature|endpoint)  // .*? = non-greedy, stops at first match
```

**Anchoring:**
```regex
^how does.*work$  // Only match if entire prompt matches
```

### Common Patterns

```regex
# Feature creation
(add|create|implement|build).*?(feature|endpoint|route|service)

# Explanation requests
(how does|how do|explain|what is|describe).*?

# Database work
(add|create|modify|update).*?(table|column|schema|migration)

# Error handling
(fix|handle|catch|debug).*?(error|exception|bug)
```

---

## File Path Triggers

### How It Works

Glob pattern matching against file paths being edited.

### Use For

Activating skills when working on specific file types or directories.

### Configuration

```json
"pathPatterns": [
  "src/services/**/*.ts",
  "src/controllers/**/*.ts"
]
```

### Glob Syntax

| Pattern | Matches |
|---------|---------|
| `*` | Any single path segment |
| `**` | Any number of path segments |
| `*.ts` | Any .ts file in current dir |
| `**/*.ts` | Any .ts file in any subdir |
| `src/{a,b}/**` | src/a or src/b subdirs |

### Best Practices

- Be as specific as possible
- Add exclusions for test files
- Consider monorepo structure

---

## Content Pattern Triggers

### How It Works

Regex matching against file contents.

### Use For

Activating based on what's IN the file, not just filename.

### Configuration

```json
"contentPatterns": [
  "import.*Prisma",
  "PrismaService",
  "export class.*Controller"
]
```

### Common Patterns

```regex
# Prisma/Database
import.*[Pp]risma
PrismaService
\.findMany\(

# Controllers/Routes
export class.*Controller
router\.
app\.(get|post|put|delete)

# React/Components
export.*React\.FC
useState|useEffect
```

### Performance Note

Content matching reads entire file - use sparingly on large files.

---

## Best Practices Summary

### DO:
✅ Use specific, unambiguous keywords
✅ Test all patterns with real examples
✅ Include common variations
✅ Use non-greedy regex: `.*?`
✅ Escape special characters in content patterns
✅ Add exclusions for test files

### DON'T:
❌ Use overly generic keywords ("system", "work")
❌ Make intent patterns too broad (false positives)
❌ Use greedy regex: `.*` instead of `.*?`
❌ Match too broadly in file paths
❌ Forget to test with regex tester (https://regex101.com/)

---

**Related Files:**
- [SKILL.md](../SKILL.md) - Main skill guide
- [SKILL_RULES_REFERENCE.md](SKILL_RULES_REFERENCE.md) - Complete schema
- [PATTERNS_LIBRARY.md](PATTERNS_LIBRARY.md) - Ready-to-use patterns
