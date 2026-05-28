---
name: create-business-requirements-documents
description: Use this skill when you need to create Business Requirements Documents (BRD) and Product Requirements Documents (PRD) following the SDD methodology to define business needs and product features.
---

# Skill body

## Purpose

Create **Business Requirements Documents (BRD)** and **Product Requirements Documents (PRD)** as part of the SDD workflow. The BRD defines high-level business needs and objectives, while the PRD translates these into specific product features and user requirements.

### Layers
- **BRD**: Layer 1 (Entry point - no upstream dependencies)
- **PRD**: Layer 2 (Requires completed BRD)

### Downstream Artifacts
- **BRD**: PRD (Layer 2), EARS (Layer 3), BDD (Layer 4), ADR (Layer 5)
- **PRD**: EARS (Layer 3), BDD (Layer 4), ADR (Layer 5)

## Prerequisites

### Upstream Artifact Verification (CRITICAL)

**Before creating these documents, you MUST:**

1. **List existing upstream artifacts**:
   ```bash
   ls docs/BRD/ docs/PRD/ docs/EARS/ docs/BDD/ docs/ADR/ docs/SYS/ docs/REQ/ 2>/dev/null
   ```

2. **Reference only existing documents** in traceability tags.
3. **Use `null`** only when upstream artifact type genuinely doesn't exist.
4. **NEVER use placeholders** like `BRD-XXX` or `TBD`.
5. **Do NOT create missing upstream artifacts** - skip functionality instead.

### Required Readings
Before creating a BRD or PRD, read:
1. **Shared Standards**: `.claude/skills/doc-flow/SHARED_CONTENT.md`
2. **Templates**: 
   - For BRD: `ai_dev_flow/BRD/BRD-TEMPLATE.md`
   - For PRD: `ai_dev_flow/PRD/PRD-TEMPLATE.md`
3. **Creation Rules**: 
   - For BRD: `ai_dev_flow/BRD/BRD_CREATION_RULES.md`
   - For PRD: `ai_dev_flow/PRD/PRD_CREATION_RULES.md`
4. **Validation Rules**: 
   - For BRD: `ai_dev_flow/BRD/BRD_VALIDATION_RULES.md`
   - For PRD: `ai_dev_flow/PRD/PRD_VALIDATION_RULES.md`

## When to Use This Skill

Use this skill when:
- Starting a new project and need to define business needs (BRD).
- Have completed the BRD and need to define product features and user requirements (PRD).
- Translating business needs into product specifications and establishing KPIs and success metrics.

## Document Structure

### BRD Specific Guidance
- **Sections**: Follow the structure outlined in the BRD template, ensuring to include all required sections.

### PRD Specific Guidance
- **Sections**: PRD documents require exactly **21 numbered sections** (1-21). See the PRD template for complete structure.

### Pre-Flight Check (MANDATORY for BRD)
Before creating ANY BRD section, confirm:
1. ✅ Read `ai_dev_flow/ID_NAMING_STANDARDS.md` - Element Type Codes table.
2. ✅ Element ID format: `BRD.{DOC_NUM}.{ELEM_TYPE}.{SEQ}` (4 segments, dots).

**Common Element Types**:
| Code | Type | Example |
|------|------|---------|
| 01 | Functional Requirement | BRD.02.01.01 |
| 06 | Acceptance Criteria | BRD.02.06.01 |
| 23 | Business Objective | BRD.02.23.01 |
| 32 | Architecture Topic | BRD.02.32.01 |

> ⚠️ **Removed Patterns**: Do NOT use `AC-XXX`, `FR-XXX`, `BC-XXX`, `BO-XXX` formats.