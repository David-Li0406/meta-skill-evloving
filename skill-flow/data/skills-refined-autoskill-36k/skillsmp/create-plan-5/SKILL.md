---
name: create-plan
description: Create a structured implementation plan for a feature before coding
---

# Create Plan

Create a structured implementation plan before writing any code.

**Usage**: "create plan `<id>-<title>` [details]"

---

## Instructions

When the user asks to create a plan:

### 1. Parse Input

Extract from user request:
- **id**: Short identifier (e.g., `001`, `002`)
- **title**: Kebab-case title (e.g., `qr-code`, `thai-linebreak`)
- **details**: Optional description of what to build

### 2. Create Plan Directory

```bash
mkdir -p plan
```

### 3. Generate Plan File

Create `plan/<id>-<title>.md` using this template:

```markdown
# <id>: <Title in Title Case>

**Branch**: `feature/<id>-<title>`
**Status**: planning

## Objective

<What we're building and why - expand from user's details>

## Steps

### 1. <First Step Name>

- [ ] Task description
- [ ] Task description

> Commit: `<type>(scope): message`

### 2. <Second Step Name>

- [ ] Task description

> Commit: `<type>(scope): message`

## Tests

- [ ] Unit tests for new functionality
- [ ] Integration tests if applicable

## Notes

<Design decisions, risks, dependencies>
```

### 4. Do NOT Implement

**This is planning only.** Do not write any implementation code.

---

## Example

**User**: "create plan 001-qr-code Add QR code generation to templates"

**Create file** `plan/001-qr-code.md`:

```markdown
# 001: QR Code

**Branch**: `feature/001-qr-code`
**Status**: planning

## Objective

Add QR code generation capability to the template engine for embedding QR codes in PDFs.

## Steps

### 1. Add QR Code Library

- [ ] Add `qrcode` crate dependency to pdf-core
- [ ] Create QR generation module with public API

> Commit: `feat(pdf-core): add qr code generation module`

### 2. Template Integration

- [ ] Add QrCode element type to template schema
- [ ] Implement QR rendering in template engine
- [ ] Add positioning and sizing support

> Commit: `feat(template): integrate qr code rendering`

### 3. Documentation

- [ ] Add QR code usage examples
- [ ] Update API documentation

> Commit: `docs: add qr code documentation`

## Tests

- [ ] Unit tests for QR generation functions
- [ ] Integration test with sample PDF template

## Notes

- Using `qrcode` crate for generation
- Default error correction level: Medium
- Support custom size via width/height attributes
```

---

## Commit Types Reference

| Type | Use for |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `refactor` | Code restructure |
| `test` | Adding tests |
| `chore` | Maintenance |

---

## Checklist

Before finishing:
- [ ] Plan file created in `plan/` directory
- [ ] All steps have clear tasks
- [ ] Each step has a commit message
- [ ] Tests section is filled out
- [ ] Status is set to `planning`
- [ ] NO implementation code written
