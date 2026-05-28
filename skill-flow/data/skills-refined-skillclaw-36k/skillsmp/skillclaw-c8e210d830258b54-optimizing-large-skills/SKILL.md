---
name: optimizing-large-skills
description: Use this skill when you need to reduce the size of a skill file that exceeds 300 lines or contains multiple similar code blocks, ensuring efficient organization and functionality.
---

# Optimizing Large Skills

This skill provides a systematic methodology for reducing skill file size while preserving functionality through separation of concerns and strategic code organization.

## When to Use

**Symptoms that trigger this skill:**
- Skills-eval validation shows "[WARN] Large skill file" warnings
- SKILL.md files exceed 300 lines
- Multiple code blocks (10+) with similar functionality
- Heavy Python implementations inline with markdown
- Functions >20 lines embedded in documentation

**Quick Analysis:**
```bash
# Analyze any skill file for optimization opportunities
python skills/optimizing-large-skills/tools/optimization-patterns.py \
  skills/path/SKILL.md --verbose --generate-plan
```

## Core Pattern: Externalize-Consolidate-Progress

### Transformation Pattern

**Before**: 654-line skill with heavy inline Python implementations  
**After**: ~150-line skill with external tools and references

**Key Changes:**
- Externalize heavy implementations (>20 lines) to dedicated tools
- Consolidate similar functions with parameterization
- Replace code blocks with structured data and tool references
- Implement progressive loading for non-essential content

## Quick Reference

### Size Reduction Strategies

| Strategy                              | Impact           | When to Use                             |
| ------------------------------------- | ---------------- | --------------------------------------- |
| **Externalize Python modules**        | 60-70% reduction | Heavy implementations (>20 lines)       |
| **Consolidate similar functions**     | 15-20% reduction | Repeated patterns with minor variations |
| **Replace code with structured data** | 10-15% reduction | Configuration-driven logic              |
| **Progressive loading patterns**      | 5-10% reduction  | Multi-stage workflows                   |

### File Organization
```
skill-name/
  SKILL.md              # Core documentation (~150-200 lines)
  modules/              # Directory for externalized modules
```