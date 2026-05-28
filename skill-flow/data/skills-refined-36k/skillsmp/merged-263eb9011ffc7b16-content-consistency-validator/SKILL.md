---
name: content-consistency-validator
description: Use this skill to validate messaging consistency across websites, GitHub repositories, and local documentation, generating read-only discrepancy reports to identify conflicts or inconsistencies.
---

# Content Consistency Validator

## Overview

This skill performs comprehensive read-only validation of messaging consistency across three critical content sources:

1. **Website Content** (ANY HTML site: WordPress, Hugo, Astro, Next.js, static HTML, etc.) - **OFFICIAL SOURCE OF TRUTH**
2. **GitHub Repositories** (README files, technical documentation)
3. **Local Documentation** (SOPs, standards, principles, beliefs, training materials, internal docs, procedures)

**CRITICAL: This skill NEVER makes changes.** It only generates detailed discrepancy reports for human review.

## When This Skill Activates

Trigger this skill when you mention:
- "Check consistency"
- "Validate documentation"
- "Audit messaging"
- "Find mixed messaging"
- "Before I update internal docs, check website first"
- "Ensure website matches GitHub"
- "Generate consistency report"

## How It Works

### Phase 1: Source Discovery

1. **Identify Website Sources**
   - Detect and analyze ANY HTML-based website:
     - Static HTML sites
     - Hugo/Astro static site generators
     - Jekyll/GitHub Pages sites
     - WordPress sites
     - Next.js/React sites
     - Vue/Nuxt sites
     - Gatsby sites
     - 11ty/Eleventy sites
     - Docusaurus sites
   - Extract key messaging: taglines, value propositions, feature lists

2. **Identify GitHub Sources**
   - Locate relevant repositories
   - Find README.md, CONTRIBUTING.md, documentation folders
   - Extract project descriptions, feature claims, installation instructions

3. **Identify Local Documentation**
   - Find internal docs, training materials, SOPs
   - Extract procedures, guidelines, technical specifications

### Phase 2: Content Extraction

For each source, extract:
- Core messaging (mission statements, value propositions)
- Feature descriptions
- Version numbers
- URLs and links
- Contact information
- Technical specifications
- Terminology

### Phase 3: Consistency Analysis

Compare content across sources and identify:

**🔴 Critical Discrepancies:**
- Conflicting version numbers
- Different feature lists
- Contradictory technical requirements
- Mismatched contact information

**🟡 Warning-Level Issues:**
- Inconsistent terminology
- Different phrasing of the same concept
- Missing information in one source

**🟢 Informational Notes:**
- Stylistic differences (acceptable)
- Platform-specific variations (expected)

### Phase 4: Generate Discrepancy Report

Create a comprehensive Markdown report with:

```markdown
# Content Consistency Validation Report
Generated: [timestamp]

## Executive Summary
- Total sources analyzed: X
- Critical discrepancies: X
- Warnings: X

## 1. Website vs GitHub Discrepancies
### 🔴 CRITICAL: Version Mismatch
**Website says:** v1.2.0
**GitHub says:** v1.2.1
**Location:**
- Website: /about/index.html:45
- GitHub: README.md:12

## 2. Website vs Local Docs Discrepancies
### 🔴 CRITICAL: Contact Email Mismatch
**Website says:** support@example.com
**Local docs say:** help@example.com

## 3. GitHub vs Local Docs Discrepancies
### 🟡 WARNING: Installation Instructions Differ
**GitHub:** "Run npm install"
**Local docs:** "Use pnpm install"

## 4. Terminology Consistency Issues
| Term Used | Website | GitHub | Local Docs | Recommendation |
|-----------|---------|--------|------------|----------------|
| Plugin/Extension | Plugin | Extension | Plugin | Standardize on "Plugin" |
```

## Best Practices

### Source Priority (Use This When Conflicts Exist)

**Trust Priority Order:**
1. **Website** - Public-facing, most authoritative
2. **GitHub** - Developer-facing, technical accuracy
3. **Local Docs** - Internal-use, lowest priority for public messaging

### When to Run Validation

✅ **Run validation BEFORE:**
- Updating internal documentation
- Creating training materials
- Writing new marketing content

✅ **Run validation AFTER:**
- Website updates
- GitHub README changes

### What This Skill Does NOT Do

❌ Does NOT automatically fix issues  
❌ Does NOT modify any files  
❌ Does NOT make content decisions  
✅ ONLY generates read-only reports for human review  

## Technical Implementation

### Read-Only Tools Used

- `Read` - Reads local files (website, docs, SOPs)
- `WebFetch` - Reads deployed website pages
- `Grep` - Searches for specific terms across files

### Output Format

- Markdown report saved to `consistency-reports/YYYY-MM-DD-HH-MM-SS.md`

## Expected Activation Patterns

**Natural Language Triggers:**
- "Check consistency"
- "Validate documentation"
- "Audit messaging"
- "Find discrepancies"
- "Before I update X, check Y"