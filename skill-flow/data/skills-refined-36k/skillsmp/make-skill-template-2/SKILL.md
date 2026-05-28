---
name: make-skill-template
description: 'Template nhanh để tạo skill mới. Copy-paste và fill in blanks, không cần research format.'
---

# Make Skill Template

Quick template để tạo Copilot skill mới. Copy → Paste → Fill blanks → Done.

---

## Quick Start

1. Copy template bên dưới
2. Tạo folder `skills/[your-skill-name]/`
3. Paste vào `SKILL.md`
4. Fill in các `[PLACEHOLDER]`
5. Remove sections không cần

---

## Full Template

```markdown
---
name: [skill-name-lowercase-hyphenated]
description: '[1-2 sentence description. What does it do? When to use?]'
---

# [Skill Title]

> [One-line summary hoặc tagline]

## Khi Nào Sử Dụng

- [Use case 1]
- [Use case 2]
- [Use case 3]

---

## Quick Reference

| [Column 1] | [Column 2] |
|------------|------------|
| [Item] | [Description] |
| [Item] | [Description] |
| [Item] | [Description] |

---

## Core Concepts

### [Concept 1]

[Explanation - 2-3 paragraphs max]

### [Concept 2]

[Explanation - 2-3 paragraphs max]

---

## Examples

### [Example Name]

\`\`\`[language]
[code example]
\`\`\`

---

## Checklist

- [ ] [Step 1]
- [ ] [Step 2]
- [ ] [Step 3]

---

## Common Issues

| Issue | Solution |
|-------|----------|
| [Problem] | [Fix] |
| [Problem] | [Fix] |

---

## References

- [Reference 1](references/ref1.md)
- [External Link](https://example.com)
```

---

## Minimal Template

Cho simple skills:

```markdown
---
name: [skill-name]
description: '[Brief description]'
---

# [Title]

## Khi Nào Sử Dụng

- [Use case]

## Quick Reference

| Item | Description |
|------|-------------|
| [A] | [Details] |

## Example

\`\`\`
[code]
\`\`\`
```

---

## Reference File Template

Khi cần file trong `references/`:

```markdown
# [Topic Name]

> Part of [parent-skill-name] skill

## Overview

[Introduction]

## Details

[Main content]

## Examples

[Code/content examples]

## See Also

- [Related topic](related.md)
```

---

## Frontmatter Rules

```yaml
---
name: must-be-lowercase-with-hyphens  # ✅
name: MySkill                          # ❌
name: my_skill                         # ❌

description: 'Use single quotes for description. End with period.'  # ✅
description: No quotes here            # ❌
description: "Double quotes work but single preferred"  # ⚠️
---
```

---

## Section Priority

| Priority | Sections | Notes |
|----------|----------|-------|
| **Required** | Frontmatter, Khi Nào Sử Dụng, Quick Reference | Always include |
| **Recommended** | Examples, Checklist | Most skills need these |
| **Optional** | Common Issues, References | If applicable |

---

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Skill name | lowercase-hyphen | `ios-mvvm-foundation` |
| Folder | Same as name | `skills/ios-mvvm-foundation/` |
| Main file | SKILL.md | `SKILL.md` (uppercase) |
| References | lowercase-hyphen.md | `animation-guidelines.md` |

---

## File Structure Examples

### Simple Skill
```
skills/git-basics/
└── SKILL.md
```

### Skill with References
```
skills/ios-mvvm-foundation/
├── SKILL.md
└── references/
    ├── animation-guidelines.md
    ├── navigation-patterns.md
    └── testing.md
```

---

## Checklist Khi Tạo Skill

- [ ] Folder name = skill name (lowercase-hyphen)
- [ ] SKILL.md có frontmatter với `name` và `description`
- [ ] Có "Khi Nào Sử Dụng" section
- [ ] Có ít nhất 1 table hoặc list
- [ ] Có ít nhất 1 code example (nếu technical)
- [ ] All links hoạt động
- [ ] Không có placeholder text còn sót

---

## Quick Copy Sections

### Table Template
```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data | Data | Data |
```

### Code Block Template
```markdown
\`\`\`swift
// Swift code here
\`\`\`
```

### Checklist Template
```markdown
- [ ] Item 1
- [ ] Item 2
- [ ] Item 3
```

### Callout Template
```markdown
> **Note**: Important information here.

> **Warning**: Be careful about this.

> **Tip**: Helpful suggestion.
```
