---
name: source-unifier
description: Use this skill to intelligently merge documentation from multiple sources (websites, GitHub repos, PDFs) while detecting and reporting conflicts between documented and implemented behavior.
---

# Skill body

## Purpose

Single responsibility: Intelligently merge documentation from multiple sources (websites, GitHub repos, PDFs) while detecting and transparently reporting conflicts between documented and implemented behavior.

## Grounding Checkpoint

Before executing, VERIFY:

- [ ] All source URLs/paths are accessible
- [ ] Each source type is correctly identified (docs, GitHub, PDF)
- [ ] Output directory is writable
- [ ] Merge mode is specified (rule-based or AI-enhanced)
- [ ] Conflict resolution strategy is defined

**DO NOT merge without inspecting each source first.**

## Uncertainty Escalation

ASK USER instead of guessing when:

- Conflict severity is unclear (is doc or code authoritative?)
- Multiple valid interpretations of API signature
- Source versions don't match (e.g., v2 docs vs v3 code)
- Merge strategy produces ambiguous results

**NEVER silently resolve conflicts. Always report discrepancies.**

## Context Scope

| Context Type | Included | Excluded |
|--------------|----------|----------|
| RELEVANT | All specified sources, merge config | Unrelated documentation |
| PERIPHERAL | Version history for context | Other projects |
| DISTRACTOR | Previous merge attempts | Unrelated codebases |

## Conflict Types

| Type | Severity | Description | Example |
|------|----------|-------------|---------|
| Missing in code | HIGH | Documented but not implemented | API endpoint in docs, not in code |
| Missing in docs | MEDIUM | Implemented but not documented | Hidden feature in code |
| Signature mismatch | MEDIUM | Different parameters/types | `func(a, b)` vs `func(a, b, c=None)` |
| Description mismatch | LOW | Different explanations | Wording differences |

## Workflow Steps

### Step 1: Verify Sources

```bash
# Test documentation URL
curl -I https://docs.example.com/

# Test GitHub repo
gh repo view owner/repo --json name,description

# Test PDF file
file manual.pdf && pdfinfo manual.pdf
```

### Step 2: Create Unified Configuration

```json
{
  "name": "myframework",
  "description": "Complete framework knowledge from docs + code",
  "merge_mode": "rule-based",
  "conflict_resolution": {
    "missing_in_code": "warn",
    "missing_in_docs": "include"
  }
}
```