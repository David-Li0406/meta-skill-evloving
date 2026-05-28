---
name: Code Quality & Refactoring
description: Tools to enforce code cleanliness, reduce technical debt, and maintain architectural standards.
---

# 🧹 Code Quality & Refactoring Skill

This skill enforces the standards of the **Code Reviewer** and **JavaScript Pro** agents. It is the **Health Monitor** for your codebase.

## 🎯 When to Use
- **After every Feature Implementation**: Clean up the "construction site".
- **Refactoring Legacy Code**: When touching a file > 3 months old.
- **Before `gated-commit`**: Ensure no blockers exist.

## 🛠️ Toolbelt

### 1. The Quality Scanner (Automated)
Detects "God Components", type safety violations, and leftover debug noise.

```bash
node .agent/skills/code-quality/scripts/scan-quality-metrics.js <target_directory>
```

**Common Violations & Fixes:**

| Violation Type | Detected Pattern | The "Pro" Fix |
|:---:|:---:|:---:|
| **Type Safety** | `any`, `Function` | Use `unknown`, generics, or specific Interfaces. |
| **Debug Noise** | `console.log()` | Remove or use `logger.info()` (only if necessary). |
| **Complexity** | File > 300 lines | **Extract** sub-components to `./components/<Name>/`. |
| **Exports** | Unused export | **Delete** it. Dead code is technical debt. |

### 2. Manual Cleanup Checklist
- [ ] **Comments**: Delete "What" comments. Keep "Why" comments.
- [ ] **Naming**: do variables explain themselves? (`d` vs `durationInMs`).
- [ ] **Imports**: Are imports organized? (Absolute vs Relative).

## 🚀 Workflows

### Workflow A: The "Boy Scout" Pattern
Use this when you are just passing through a file.

1. **Scan**: visually checks for `any` or `console.log`.
2. **Fix**: Apply the "Pro" fix immediately.
3. **Leave**: Do not start a massive refactor unless requested.

### Workflow B: The "Deep Clean"
Use this when assigned a refactoring task.

1. **Measure**: Run `scan-quality-metrics.js` to get a baseline.
2. **Plan**: Identify the top 3 "God Components" to break down.
3. **Execute**: Break them down one by one.
4. **Verify**: Ensure functionality is unchanged (Run Smoke Tests).

## 🧠 Philosophy
> **"If you can't type it, you don't understand it."**
> Avoid shortcuts. `any` is a virus that spreads. Kill it early.
