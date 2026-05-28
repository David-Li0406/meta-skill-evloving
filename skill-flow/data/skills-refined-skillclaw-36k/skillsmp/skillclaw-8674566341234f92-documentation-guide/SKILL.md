---
name: documentation-guide
description: Use this skill when you need comprehensive guidance on project documentation structure, content requirements, and best practices for technical files.
---

# Skill body

## Purpose

This skill provides comprehensive guidance for project documentation, including:
- Document structure and organization
- Content requirements based on project type
- Standards for writing technical documents
- Templates for common document types

## Quick Reference (YAML Compressed Format)

```yaml
# === Project Type → Document Requirements ===
document_matrix:
  #           README  ARCH   API    DB     DEPLOY MIGRATE ADR    CHANGE CONTRIB
  new:        [REQ,   REQ,   if_app, if_app, REQ,   NO,     REC,   REQ,   REC]
  refactor:   [REQ,   REQ,   REQ,    REQ,    REQ,   REQ,    REQ,   REQ,   REC]
  migration:  [REQ,   REQ,   REQ,    REQ,    REQ,   REQ,    REQ,   REQ,   REC]
  maintenance:[REQ,   REC,   REC,    REC,    REC,   NO,     if_app, REQ,   if_app]
  # REQ=Required, REC=Recommended, if_app=If applicable, NO=Not needed

# === Document Pyramid ===
pyramid:
  level_1: "README.md → Entry point, quick overview"
  level_2: "ARCHITECTURE.md → System overview"
  level_3: "API.md, DATABASE.md, DEPLOYMENT.md → Technical details"
  level_4: "ADR/, MIGRATION.md, CHANGELOG.md → Change history"

# === Required Files ===
root_files:
  README.md: {required: true, purpose: "Project overview, quick start"}
  CONTRIBUTING.md: {required: "recommended", purpose: "Contribution guidelines"}
  CHANGELOG.md: {required: "recommended", purpose: "Version history"}
  LICENSE: {required: "for OSS", purpose: "Licensing information"}

docs_structure:
  INDEX.md: "Document index"
  ARCHITECTURE.md: "System architecture"
  API.md: "API documentation"
  DATABASE.md: "Database schema"
  DEPLOYMENT.md: "Deployment guide"
  MIGRATION.md: "Migration plan (if applicable)"
  ADR/: "Architecture decision records"

# === File Naming ===
naming:
  root: "UPPERCASE.md (README.md, CONTRIBUTING.md, CHANGELOG.md)"
  docs: "lowercase-kebab-case.md (getting-started.md, api-reference.md)"

# === Quality Standards ===
quality:
  format:
    language: "English (or project specified)"
    encoding: "UTF-8"
    line_length: "Recommended ≤120 characters"
    diagrams: "Prefer Mermaid, then ASCII Art"
    links: "Use relative paths for internal links"
  maintenance:
    sync: "Update documents when code changes"
    version: "Indicate version and date at the top"
    review: "Include document changes in code reviews"
    periodic: "Check documents for obsolescence quarterly"
```