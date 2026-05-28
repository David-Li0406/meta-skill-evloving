---
title: Use Scripts for Determinism
impact: HIGH
impactDescription: Reliability and token efficiency
tags: anatomy, scripts
---

## Use Scripts for Determinism

**Impact: HIGH**

Use `scripts/` for tasks that require deterministic reliability or complex logic that is prone to hallucination if written as text instructions.

**Incorrect (complex logic in text):**

```markdown
To rotate the PDF, first read the bytes, then look for the rotation matrix... [complex math instructions]
```

**Correct (delegated to script):**

```markdown
To rotate the PDF, run: `scripts/rotate_pdf.py input.pdf output.pdf`
```
