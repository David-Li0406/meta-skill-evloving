# Python Performance Best Practices

A comprehensive, AI-agent-optimized guide to Python >=3.11 performance optimization. Contains 45 rules across 9 categories, prioritized by impact.

## Overview

This skill provides performance optimization guidelines for Python applications targeting Python 3.11 and later. The rules are organized by impact level, from critical I/O and async patterns to incremental runtime optimizations.

## Structure

```
python-best-practices/
├── SKILL.md              # Quick reference with all rules
├── AGENTS.md             # Compiled comprehensive guide
├── metadata.json         # Version and references
├── README.md             # This file
└── rules/
    ├── _sections.md      # Category definitions
    ├── io-*.md           # I/O pattern rules (CRITICAL)
    ├── async-*.md        # Async concurrency rules (CRITICAL)
    ├── mem-*.md          # Memory management rules (HIGH)
    ├── ds-*.md           # Data structure rules (HIGH)
    ├── algo-*.md         # Algorithm efficiency rules (MEDIUM-HIGH)
    ├── conc-*.md         # Concurrency model rules (MEDIUM)
    ├── serial-*.md       # Serialization rules (MEDIUM)
    ├── cache-*.md        # Caching rules (LOW-MEDIUM)
    └── runtime-*.md      # Runtime tuning rules (LOW)
```

## Getting Started

```bash
# Install dependencies
pnpm install

# Build AGENTS.md from rules
pnpm build

# Validate skill structure
pnpm validate
```

## Creating a New Rule

1. Identify the category from the prefix table below
2. Create a new file: `rules/{prefix}-{descriptive-name}.md`
3. Use the template structure with YAML frontmatter
4. Run validation to check formatting

### Prefix Reference

| Prefix | Category | Impact |
|--------|----------|--------|
| `io-` | I/O Patterns | CRITICAL |
| `async-` | Async Concurrency | CRITICAL |
| `mem-` | Memory Management | HIGH |
| `ds-` | Data Structures | HIGH |
| `algo-` | Algorithm Efficiency | MEDIUM-HIGH |
| `conc-` | Concurrency Model | MEDIUM |
| `serial-` | Serialization | MEDIUM |
| `cache-` | Caching and Memoization | LOW-MEDIUM |
| `runtime-` | Runtime Tuning | LOW |

## Rule File Structure

```markdown
---
title: Rule Title Here
impact: CRITICAL|HIGH|MEDIUM-HIGH|MEDIUM|LOW-MEDIUM|LOW
impactDescription: Quantified impact (e.g., "2-10× improvement")
tags: prefix, technique, related-concepts
---

## Rule Title Here

Brief explanation of WHY this matters (1-3 sentences).

**Incorrect (what's wrong):**

\`\`\`python
# Bad example with comments explaining the cost
\`\`\`

**Correct (what's right):**

\`\`\`python
# Good example with minimal diff from incorrect
\`\`\`

Reference: [Source](url)
```

## File Naming Convention

Rules follow the pattern: `{prefix}-{descriptive-name}.md`

- Prefix must match one of the categories in `_sections.md`
- Use lowercase with hyphens for multi-word names
- Keep names concise but descriptive

Examples:
- `async-gather-independent-operations.md`
- `mem-slots-dataclass.md`
- `ds-set-for-membership.md`

## Impact Levels

| Level | Description | Examples |
|-------|-------------|----------|
| CRITICAL | Architectural issues causing 2-10× slowdown | Waterfalls, blocking I/O |
| HIGH | Significant memory or performance impact | Wrong data structures, memory leaks |
| MEDIUM-HIGH | Notable improvement in common scenarios | Algorithm complexity |
| MEDIUM | Moderate gains for specific use cases | Concurrency model, serialization |
| LOW-MEDIUM | Incremental improvements | Caching, memoization |
| LOW | Micro-optimizations for hot paths | Interpreter settings |

## Scripts

```bash
# Build AGENTS.md from individual rules
pnpm build
# or: node ../../plugins/dev-skill/scripts/build-agents-md.js .

# Validate skill structure and content
pnpm validate
# or: node ../../plugins/dev-skill/scripts/validate-skill.js .

# Validate sections only (for incremental development)
pnpm validate:sections
# or: node ../../plugins/dev-skill/scripts/validate-skill.js . --sections-only
```

## Contributing

1. Read existing rules to understand the style
2. Follow the rule template exactly
3. Ensure examples are production-realistic
4. Quantify impact where possible
5. Run validation before submitting

## Acknowledgments

This skill draws from the official Python documentation, PEP 8, the Python Performance Tips wiki, and community best practices. Special thanks to the CPython core developers for continuous interpreter optimizations.
