---
name: doc-splitter
description: Use this skill to split large documentation (10K+ pages) into focused sub-skills with intelligent routing, ideal for massive doc sites like Godot, AWS, or MSDN.
---

# Documentation Splitter Skill

## Purpose

Single responsibility: Split large documentation sites into multiple focused sub-skills with an optional router skill for intelligent navigation.

## Grounding Checkpoint

Before executing, VERIFY:

- [ ] Total page count is known (run estimation first)
- [ ] Documentation categories are identifiable
- [ ] Target skill size determined (default: 5,000 pages per skill)
- [ ] Router strategy selected (category, size, or hybrid)

**DO NOT split without understanding documentation structure.**

## Uncertainty Escalation

ASK USER instead of guessing when:

- Category boundaries are unclear
- Optimal skill size is uncertain for target use case
- Cross-references between sections complicate splitting
- Router vs flat structure decision needed

**NEVER arbitrarily split - seek user guidance on boundaries.**

## Context Scope

| Context Type | Included | Excluded |
|--------------|----------|----------|
| RELEVANT | Doc structure, categories, page counts | Actual page content |
| PERIPHERAL | Similar large doc examples | Other documentation |
| DISTRACTOR | Content quality concerns | Individual page issues |

## Size Guidelines

| Documentation Size | Recommendation | Strategy |
|-------------------|----------------|----------|
| < 5,000 pages | One skill | No splitting |
| 5,000 - 10,000 pages | Consider splitting | Category-based |
| 10,000 - 30,000 pages | Recommended | Router + Categories |
| 30,000+ pages | Strongly recommended | Router + Categories |

## Workflow Steps

### Step 1: Estimate Documentation Size

```bash
# Quick estimation with skill-seekers
skill-seekers estimate configs/large-docs.json

# Output:
# 📊 ESTIMATION RESULTS
# ✅ Pages Discovered: 28,450
# 📈 Estimated Total: 32,000
# ⏱️  Time Elapsed: 2.1 minutes
# 💡 Recommended: Split into 6-7 sub-skills
```

### Step 2: Analyze Category Structure

```bash
# Identify natural category boundaries
skill-seekers analyze --config configs/large-docs.json --categories

# Output:
# Categories detected:
# - scripting: 8,200 pages
# - 2d: 5,400 pages
# - 3d: 9,100 pages
# - physics: 4,300 pages
# - networking: 2,800 pages
# - editor: 2,200 pages
```

### Step 3: Choose Splitting Strategy

- Based on the analysis, decide on the splitting strategy (category-based, size-based, or hybrid).
- Implement the splitting according to the chosen strategy, ensuring to maintain logical boundaries and user guidance.