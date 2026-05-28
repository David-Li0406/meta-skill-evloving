---
name: technical-blog-writing
description: Use this skill when you want to write technical blog posts that explain system internals, architecture, implementation details, or technical concepts with citations.
---

# Technical Blog Writing Skill

Write technical blog posts that explain system internals, architecture, and implementation details.

## When to Use

- Explaining system internals or implementation details
- Source code analysis and walkthrough
- Comparing different implementations or approaches
- Doc-driven architecture/comparison posts (no source code in scope)

## Document Structure

```markdown
# [Topic] Deep Dive

Brief intro + why it matters.
> **Code Version**: Based on [project] `vX.Y.Z` tag (or commit id for external repos).

## 1. Introduction (problem + scope)
## 2. Background / Prerequisites
## 3-N. Core Content (by data flow, not code structure)
## N+1. Comparison / Trade-offs
## N+2. Code Index (files, functions, line numbers)
## References
```

**Key guidelines**:
- Chapter 1 = Introduction + Navigation only, no implementation details
- Organize content by data flow, not by code components
- Use `> ⏭️ If reading first time, skip to §X, return here when needed.`

---

## Core Principles

### 1. Progressive Explanation
- Start with the problem, not the solution
- Build concepts layer by layer
- Explain "why" not just "what"

### 2. Concept-First
- **Never use undefined terms**: Define before use
- **Add concept sections**: Create §X.Y.1 to introduce concepts before implementation
- **Use navigation hints**: `> ⏭️ If unfamiliar with X, see §Y first`

### 3. Big Picture First
- Start with unified visual overview before details
- Use comparison diagrams/tables for 2+ approaches
- Show complete flow in one diagram

### 4. Balanced Comparison
- Analyze BOTH sides; don't cherry-pick
- Use comparison tables for similar concepts
- Identify what's truly different vs. equivalent

### 5. Design Decision Explanation
- What problem does it solve?
- What alternatives exist?
- What trade-offs?

### 6. Concrete Examples
- 1-2 practical examples per major section
- Show input → process → output
- Use real data for abstract concepts (e.g., inverted index with actual words)

### 7. Terminology Accuracy
- Verify terms via source code or official docs
- Define domain-specific terms when introducing
- Don't assume terms are interchangeable