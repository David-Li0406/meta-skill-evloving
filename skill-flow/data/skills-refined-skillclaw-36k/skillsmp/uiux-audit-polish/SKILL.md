---
name: UI/UX Audit & Polish
description: Tools and workflows to enforce "Calm Luxury" aesthetics and Design System compliance.
---

# 💎 UI/UX Audit & Polish Skill

This skill operationalizes the standards defined in `Agent/UI-UX-designer-glowglitch.md`. It is the **Quality Gate** for all frontend changes.

## 🎯 When to Use
- **After every UI change**: Run the token scanner.
- **New Component Creation**: Verify against "Calm Luxury" physics.
- **Refactoring**: When cleaning up "legacy" styles.

## 🛠️ Toolbelt

### 1. The Token Scanner (Automated)
Detects "Visual Noise" (hardcoded values) that breaks the design system.

```bash
node .agent/skills/ui-ux-audit/scripts/scan-token-violations.js <target_directory_or_file>
```

**Common Violations & Fixes:**

| Violation Type | Detected Pattern | The "Calm Luxury" Fix |
|:---:|:---:|:---:|
| **Borders** | `border`, `border-gray-200` | Remove border. Use `bg-white/5` or shadow. |
| **Radius** | `rounded-md`, `rounded-lg` | **ALWAYS** `rounded-none`. |
| **Spacing** | `mt-[13px]`, `gap-3` | Use fluid spacing: `mt-4`, `gap-4`. |
| **Colors** | `#F3F4F6`, `bg-gray-100` | Use semantic tokens: `bg-primary/5`. |

### 2. The "White Glove" Inspection (Manual)
Agents must explicitly verify these points before marking a task as done.

#### 🏗️ Architecture
- [ ] **Zero Radius**: Are corners checking out? (Exceptions: Pills/Circles).
- [ ] **No Borders**: defined boundaries should be created by *contrast* and *spacing*, not lines.
- [ ] **Stacking**: Are generic `z-index` values avoided? Use `z-[10]`, `z-[50]`.

#### ⚡ Interaction Physics
- [ ] **Hover**: Is it instant? (No `transition-all duration-500` for hover colors).
- [ ] **Feedback**: Do buttons click? (Active states).

## 🚀 Workflows

### Workflow A: The "Polish" Pass
Use this when asked to "Audit" or "Fix" a specific component.

1. **Scan**: Run `scan-token-violations.js` on the file.
2. **Refactor**: Replace hardcoded values with `tokens`.
3. **Verify**: Check the "White Glove" list.

### Workflow B: The "Calm Luxury" Retrofit
Use this when updating legacy components.

1. **Strip**: Remove all `shadow-*`, `rounded-*`, and `border-*` classes.
2. **Rebuild**: Apply `rounded-none`, `backdrop-blur`, and `bg-black/80`.
3. **Assess**: Does it look premium? if not, increase whitespace (`p-4` -> `p-6`).

## 🧠 Design Philosophy
> **"We don't shout; we whisper."**
> Avoid high-contrast borders. Use subtle variation in background opacity to define shape.
