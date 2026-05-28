---
name: document-requirements
description: Use this skill to create structured requirements documents, including Business Requirements Documents (BRD) and Product Requirements Documents (PRD), following the SDD methodology.
---

# Document Requirements

## Purpose

Create structured **Business Requirements Documents (BRD)** and **Product Requirements Documents (PRD)** as part of the SDD workflow. BRDs define high-level business needs and objectives, while PRDs detail product features and user requirements.

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

Before creating a BRD or PRD, read:
- **Shared Standards**: `.claude/skills/doc-flow/SHARED_CONTENT.md`
- **Templates**: `ai_dev_flow/BRD/BRD-TEMPLATE.md`, `ai_dev_flow/PRD/PRD-TEMPLATE.md`
- **Creation Rules**: `ai_dev_flow/BRD/BRD_CREATION_RULES.md`, `ai_dev_flow/PRD/PRD_CREATION_RULES.md`
- **Validation Rules**: `ai_dev_flow/BRD/BRD_VALIDATION_RULES.md`, `ai_dev_flow/PRD/PRD_VALIDATION_RULES.md`

## When to Use This Skill

Use this skill when:
- Starting a new project or feature.
- Defining business requirements and objectives (BRD).
- Translating business needs to product specifications (PRD).
- Establishing KPIs and success metrics (PRD).
- You are at Layer 1 (BRD) or Layer 2 (PRD) of the SDD workflow.

## BRD-Specific Guidance

### Required Sections (18 Total)

1. **Document Control** (MANDATORY - First section):
   - Project Name
   - Document Version
   - Date (YYYY-MM-DD)
   - Document Owner
   - Prepared By
   - Status (Draft, In Review, Approved, Superseded)
   - Document Revision History table

2. **Core Sections**:
   - Executive Summary
   - Business Context
   - Stakeholder Analysis
   - Business Requirements
   - Success Criteria
   - Constraints and Assumptions
   - Architecture Decision Requirements
   - Risk Assessment
   - Traceability
   - Additional content sections (see BRD-TEMPLATE.md for full structure)
   - Glossary
   - Appendices

### PRD-Specific Guidance

### Required Sections (21 Total)

1. **Document Control** (MANDATORY - First section):
   - Status, Version, Date Created, Last Updated
   - Author, Reviewer, Approver
   - BRD Reference
   - SYS-Ready Score and EARS-Ready Score (both >=90%)
   - Template Variant
   - Document Revision History table

2. **Core Sections**:
   - Executive Summary
   - Problem Statement
   - Target Audience & User Personas
   - Success Metrics (KPIs)
   - Goals & Objectives
   - Scope & Requirements
   - User Stories & User Roles
   - Functional Requirements
   - Customer-Facing Content (MANDATORY)
   - Acceptance Criteria
   - Constraints & Assumptions
   - Risk Assessment
   - Success Definition
   - Stakeholders & Communication
   - Implementation Approach
   - Budget & Resources
   - Traceability
   - References
   - EARS Enhancement Appendix
   - Quality Assurance & Testing Strategy

## Creation Process

### Step 1: Determine Document Type

- For **BRD**: Identify if it is a Platform or Feature BRD using the provided questionnaire.
- For **PRD**: Ensure the upstream BRD is completed.

### Step 2: Read Strategy Documents

Read relevant `{project_root}/strategy/` sections to understand business logic.

### Step 3: Select Template

Choose the appropriate template for BRD or PRD.

### Step 4: Reserve ID Number

Check `docs/BRD/` or `docs/PRD/` for the next available ID number.

### Step 5: Create Document Folder and Files

**Folder structure** (DEFAULT - nested folder per document):
1. Create folder: `docs/BRD/BRD-NN_{slug}/` or `docs/PRD/PRD-NN_{slug}/`
2. Create index file: `docs/BRD/BRD-NN_{slug}/BRD-NN.0_index.md` or `docs/PRD/PRD-NN_{slug}/PRD-NN.0_index.md`
3. Create section files: `docs/BRD/BRD-NN_{slug}/BRD-NN.S_{section_type}.md` or `docs/PRD/PRD-NN_{slug}/PRD-NN.S_{section_type}.md`

### Step 6: Complete Document Control Section

Fill all required metadata fields and initialize Document Revision History table.

### Step 7: Complete Core Sections

Fill all required sections following the template structure.

### Step 8: Document Architecture Decision Requirements

List topics needing architectural decisions (do NOT reference specific ADR numbers).

### Step 9: Add Strategy References

In the Traceability section, link to specific `{project_root}/strategy/` sections.

### Step 10: Create/Update Traceability Matrix

**MANDATORY**: Create or update `docs/BRD/BRD-00_TRACEABILITY_MATRIX.md` or `docs/PRD/PRD-00_TRACEABILITY_MATRIX.md`.

### Step 11: Validate Document

Run validation scripts for BRD and PRD.

### Step 12: Commit Changes

Commit the document file and traceability matrix together.

## Validation

### Automated Validation

Run validation scripts specific to BRD and PRD.

### Manual Checklist

- Ensure all required sections are completed.
- Verify document control is at the top.
- Check for broken links and correct tagging.

## Common Pitfalls

1. **Missing dual scores**: Both SYS-Ready and EARS-Ready scores required for PRD.
2. **Incorrect section structure**: Must be exactly 18 sections for BRD and 21 for PRD.
3. **Missing Section 10 content**: Customer-Facing Content is MANDATORY in PRD.
4. **User Stories scope violation**: Section 8 must stay at PRD-level (no EARS/BDD detail).
5. **ADR forward references**: Don't write "See ADR-033" (ADRs don't exist yet).

## Next Skills

After creating a BRD, use **`doc-prd`** to create a Product Requirements Document (Layer 2). After creating a PRD, use **`doc-ears`** to create formal EARS requirements (Layer 3).

## Related Resources

- **Main Guide**: `ai_dev_flow/SPEC_DRIVEN_DEVELOPMENT_GUIDE.md`
- **BRD and PRD Templates**: `ai_dev_flow/BRD/BRD-TEMPLATE.md`, `ai_dev_flow/PRD/PRD-TEMPLATE.md`
- **Validation Rules**: `ai_dev_flow/BRD/BRD_VALIDATION_RULES.md`, `ai_dev_flow/PRD/PRD_VALIDATION_RULES.md`
- **Shared Standards**: `.claude/skills/doc-flow/SHARED_CONTENT.md`