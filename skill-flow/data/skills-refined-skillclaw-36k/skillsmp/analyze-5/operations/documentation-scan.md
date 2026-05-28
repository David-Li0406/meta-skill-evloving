# Documentation Scan

Scan for existing documentation and assess quality.

## Overview

Identify all existing documentation to understand:
- What's already documented
- Quality and completeness of docs
- What documentation is missing
- Where docs are located

---

## Documentation Discovery

### Find Documentation Directories

```bash
# Common documentation directories
ls -la docs/ 2>/dev/null
ls -la documentation/ 2>/dev/null
ls -la doc/ 2>/dev/null
ls -la wiki/ 2>/dev/null
ls -la .docs/ 2>/dev/null
```

### Find Markdown Files

```bash
# Find all markdown files (limiting to avoid noise)
find . -type f -name "*.md" \
  | grep -v -E "node_modules|vendor|\.git|dist|build" \
  | head -30
```

### Common Documentation Files

Look for these standard files:

```bash
# Standard docs
ls -la README.md 2>/dev/null
ls -la CONTRIBUTING.md 2>/dev/null
ls -la CHANGELOG.md 2>/dev/null
ls -la LICENSE 2>/dev/null
ls -la CODE_OF_CONDUCT.md 2>/dev/null
ls -la SECURITY.md 2>/dev/null

# Setup/deployment docs
ls -la INSTALL.md 2>/dev/null
ls -la DEPLOYMENT.md 2>/dev/null
ls -la SETUP.md 2>/dev/null

# Architecture docs
ls -la ARCHITECTURE.md 2>/dev/null
ls -la DESIGN.md 2>/dev/null
ls -la API.md 2>/dev/null
```

---

## Documentation Categories

### README Assessment

Read `README.md` and assess quality:

**Good README includes:**
- Clear project description
- Installation/setup instructions
- Usage examples
- API documentation or links
- Development guide
- Testing instructions
- Deployment guide
- Contributing guidelines
- License information

**Rate as:**
- **Good** - Comprehensive, well-organized, covers all key areas
- **Basic** - Has description and setup, but missing key sections
- **Poor** - Minimal info, outdated, or confusing

### API Documentation

Look for API documentation:

```bash
# OpenAPI/Swagger
find . -name "openapi.yaml" -o -name "openapi.yml" -o -name "swagger.yaml" -o -name "swagger.json" 2>/dev/null

# API doc generators
find . -name "apidoc.json" -o -name ".redocly.yaml" 2>/dev/null

# API docs directories
ls -la docs/api/ 2>/dev/null
ls -la api-docs/ 2>/dev/null
```

**Assessment:**
- **Yes** - OpenAPI spec or comprehensive API docs exist
- **Partial** - Some API docs but incomplete
- **No** - No API documentation found

### Architecture Documentation

Look for architecture diagrams and docs:

```bash
# Architecture docs
find . -name "ARCHITECTURE.md" -o -name "architecture.md" -o -name "DESIGN.md" 2>/dev/null

# Diagram files
find . \( -name "*.drawio" -o -name "*.mermaid" -o -name "*.puml" -o -name "*.svg" \) \
  | grep -i "architecture\|diagram\|flow" 2>/dev/null
```

**Assessment:**
- **Yes** - Architecture docs with diagrams/explanations
- **Partial** - Some architecture info in README
- **No** - No architecture documentation

### Setup/Deployment Documentation

```bash
# Deployment docs
find . -name "DEPLOYMENT.md" -o -name "deployment.md" -o -name "DEPLOY.md" 2>/dev/null

# Infrastructure docs
ls -la infrastructure/README.md 2>/dev/null
ls -la terraform/README.md 2>/dev/null
ls -la .github/workflows/ 2>/dev/null
```

**Assessment:**
- **Yes** - Clear deployment and infrastructure docs
- **Partial** - Basic setup but missing details
- **No** - No deployment documentation

### Developer Documentation

```bash
# Developer guides
find . -name "CONTRIBUTING.md" -o -name "DEVELOPMENT.md" -o -name "dev-guide.md" 2>/dev/null

# Code comments/JSDoc
grep -r "@param\|@returns\|@description" src/ 2>/dev/null | wc -l
```

**Assessment:**
- **Yes** - Developer guide with setup, conventions, workflow
- **Partial** - Some developer info scattered
- **No** - No developer documentation

### Testing Documentation

```bash
# Test docs
find . -name "TESTING.md" -o -name "test-guide.md" 2>/dev/null

# Test README files
find . -path "*/tests/README.md" -o -path "*/test/README.md" 2>/dev/null
```

**Assessment:**
- **Yes** - Testing guide with examples and conventions
- **Partial** - Basic test info in README
- **No** - No testing documentation

### Database Documentation

```bash
# Database docs
find . -name "schema.md" -o -name "database.md" -o -name "DATA_MODEL.md" 2>/dev/null

# ER diagrams
find . -name "*er-diagram*" -o -name "*schema-diagram*" 2>/dev/null

# Migration docs
ls -la migrations/README.md 2>/dev/null
ls -la prisma/README.md 2>/dev/null
```

**Assessment:**
- **Yes** - Database schema docs and ER diagrams
- **Partial** - Schema file but no explanatory docs
- **No** - No database documentation

---

## Documentation Tools Detection

Identify if automated documentation tools are configured:

### Code Documentation Generators

```bash
# JSDoc/TypeDoc (JavaScript/TypeScript)
grep -r "typedoc\|jsdoc" package.json 2>/dev/null

# Sphinx (Python)
ls -la docs/conf.py 2>/dev/null

# Javadoc (Java)
grep -r "javadoc" pom.xml build.gradle 2>/dev/null

# RDoc/YARD (Ruby)
ls -la .yardopts 2>/dev/null

# Doxygen (C/C++)
ls -la Doxyfile 2>/dev/null
```

### API Documentation Tools

```bash
# Swagger UI
grep -r "swagger-ui" package.json 2>/dev/null

# Redoc
grep -r "redoc" package.json 2>/dev/null

# Postman collections
find . -name "*.postman_collection.json" 2>/dev/null
```

### Static Site Generators

```bash
# Docusaurus
grep -r "docusaurus" package.json 2>/dev/null
ls -la docusaurus.config.js 2>/dev/null

# VuePress
grep -r "vuepress" package.json 2>/dev/null

# MkDocs
ls -la mkdocs.yml 2>/dev/null

# GitBook
ls -la .gitbook.yaml 2>/dev/null

# Mintlify
ls -la mint.json 2>/dev/null
```

---

## Documentation Quality Checklist

For each category, assess:

- [ ] **Exists** - Documentation files are present
- [ ] **Current** - Docs match current code (check dates)
- [ ] **Complete** - Covers all major features/components
- [ ] **Clear** - Well-written and easy to understand
- [ ] **Examples** - Includes code examples and usage
- [ ] **Maintained** - Recently updated (check git log)

---

## Output Summary

Summarize findings:

```markdown
## Existing Documentation

### README.md
- **Status:** Yes
- **Quality:** Good
- **Coverage:** Installation, usage, API overview, development setup
- **Last Updated:** 2024-01-15
- **Notes:** Comprehensive but missing deployment section

### API Documentation
- **Status:** Partial
- **Type:** Inline JSDoc comments only
- **Coverage:** ~60% of endpoints documented
- **OpenAPI Spec:** No
- **Notes:** Should generate OpenAPI spec

### Architecture Documentation
- **Status:** No
- **Notes:** Architecture decisions are scattered in code comments

### Setup/Deployment Documentation
- **Status:** Yes
- **Files:** DEPLOYMENT.md, infrastructure/README.md
- **Coverage:** AWS deployment, CI/CD, environment setup
- **Quality:** Basic

### Developer Documentation
- **Status:** Partial
- **Files:** CONTRIBUTING.md
- **Coverage:** PR process, code style guide
- **Missing:** Local development setup, debugging guide

### Testing Documentation
- **Status:** No
- **Notes:** No testing guide, test structure undocumented

### Database Documentation
- **Status:** Yes
- **Type:** Prisma schema file with comments
- **Coverage:** All models documented inline
- **ER Diagram:** No
- **Notes:** Should generate ER diagram from schema

### Documentation Tools
- **Configured:** None
- **Recommended:** TypeDoc for code docs, Swagger for API docs
```

---

## Missing Documentation Identification

List what documentation should be created:

**Critical (needed for Step 2):**
- OpenAPI specification for API endpoints
- Architecture overview document
- Database ER diagram

**Important (create during specification):**
- Comprehensive testing guide
- Deployment runbook
- Troubleshooting guide

**Nice-to-have:**
- Code contribution guide
- ADRs (Architecture Decision Records)
- Security documentation

---

## Documentation Metrics

Calculate documentation coverage:

```bash
# Count documented vs undocumented functions (example for JS/TS)
# Total functions
grep -r "function\|const.*=>.*{" src/ | wc -l

# Documented functions (with JSDoc)
grep -B1 "function\|const.*=>" src/ | grep -c "/\*\*"

# Calculate percentage
```

Report as:
- **Code documentation coverage:** ~45% (estimated)
- **API endpoint documentation:** ~60%
- **Feature documentation:** ~30%
- **Overall documentation score:** 4/10

---

## Notes

- Check git history to see when docs were last updated
- Compare doc dates with code changes to identify stale docs
- Look for TODO/FIXME comments in docs indicating incomplete sections
- Verify links in docs aren't broken
