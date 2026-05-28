---
name: iso-13485-certification
description: Use this skill when you need assistance preparing ISO 13485 certification documentation for medical device Quality Management Systems, including gap analysis, document creation, and compliance checks.
---

# ISO 13485 Certification Documentation Assistant

## Overview

This skill helps medical device manufacturers prepare comprehensive documentation for ISO 13485:2016 certification. It provides tools, templates, references, and guidance to create, review, and gap-analyze all required Quality Management System (QMS) documentation.

**What this skill provides:**
- Gap analysis of existing documentation
- Templates for all mandatory documents
- Comprehensive requirements guidance
- Step-by-step documentation creation
- Identification of missing documentation
- Compliance checklists

**When to use this skill:**
- Starting the ISO 13485 certification process
- Conducting gap analysis against ISO 13485
- Creating or updating QMS documentation
- Preparing for certification audit
- Transitioning from FDA QSR to QMSR
- Harmonizing with EU MDR requirements

## Core Workflow

### 1. Assess Current State (Gap Analysis)

**When to start here:** User has existing documentation and needs to identify gaps.

**Process:**

1. **Collect existing documentation:**
   - Ask the user to provide a directory of current QMS documents.
   - Documents can be in any format (.txt, .md, .doc, .docx, .pdf).
   - Include any procedures, manuals, work instructions, and forms.

2. **Run gap analysis script:**
   ```bash
   python scripts/gap_analyzer.py --docs-dir <path_to_docs> --output gap-report.json
   ```

3. **Review results:**
   - Identify which of the 31 required procedures are present.
   - Identify missing key documents (Quality Manual, Medical Device File, etc.).
   - Calculate compliance percentage.
   - Prioritize missing documentation.

4. **Present findings to user:**
   - Summarize existing documentation.
   - Clearly list missing documents.
   - Provide a prioritized action plan.
   - Estimate effort required to complete documentation.