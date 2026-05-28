---
name: content-consistency-validator
description: Use this skill when you need to validate messaging consistency across a website, GitHub repositories, and local documentation, generating detailed discrepancy reports for review.
---

# Skill body

## Overview

This skill performs comprehensive read-only validation of messaging consistency across three critical content sources:

1. **Website Content** (ANY HTML site: WordPress, Hugo, Astro, Next.js, static HTML, etc.) - **OFFICIAL SOURCE OF TRUTH**
2. **GitHub Repositories** (README files, technical documentation)
3. **Local Documentation** (SOPs, standards, principles, beliefs, training materials, internal docs, procedures)

**CRITICAL: This skill NEVER makes changes.** It only generates detailed discrepancy reports for human review.

## When This Skill Activates

Trigger this skill when you mention:
- "Check consistency between website and GitHub"
- "Validate documentation consistency"
- "Audit messaging across platforms"
- "Find mixed messaging"
- "Before I update internal docs, check website first"
- "Ensure website matches GitHub"
- "Generate consistency report"

## How It Works

### Phase 1: Source Discovery

1. **Identify Website Sources**
   - Detect and analyze ANY HTML-based website:
     - Static HTML sites (index.html, about.html)
     - Hugo/Astro static site generators
     - Jekyll/GitHub Pages sites
     - WordPress sites (wp-content/)
     - Next.js/React sites (build/, out/, .next/)
     - Vue/Nuxt sites (dist/, .nuxt/)
     - Gatsby sites (public/)
     - 11ty/Eleventy sites (_site/)
     - Docusaurus sites (build/)
   - Find marketing pages, landing pages, product descriptions.

2. **Extract Key Messaging**
   - Gather key messaging, features, and versions from each source.

3. **Compare Content**
   - Systematically compare content across sources to identify discrepancies.

4. **Generate Reports**
   - Create a comprehensive Markdown report detailing discrepancies, including:
     - Executive summary with discrepancy counts by severity.
     - Detailed comparison by source pairs (website vs GitHub, etc.).
     - Terminology consistency matrix.
     - Reports saved to consistency-reports/YYYY-MM-DD-HH-MM-SS.md.

## Critical Operating Parameters

- **Temperature: 0.0** - ZERO creativity. Pure factual analysis only.
- **Read-only** - Report discrepancies, never suggest creative fixes.
- **Exact matching** - Report differences precisely as found.
- **No interpretation** - Facts only, no opinions.