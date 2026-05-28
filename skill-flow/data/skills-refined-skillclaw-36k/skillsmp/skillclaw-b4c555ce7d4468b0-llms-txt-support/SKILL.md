---
name: llms-txt-support
description: Use this skill to detect and utilize llms.txt files for LLM-optimized documentation, ensuring efficient documentation ingestion before scraping a site.
---

# Skill body

## Purpose

Single responsibility: Detect, fetch, and utilize llms.txt files that provide LLM-optimized documentation, enabling 10x faster documentation ingestion.

## Background

The llms.txt standard (https://llmstxt.org/) provides a convention for websites to expose LLM-friendly documentation. Instead of scraping entire sites, check for llms.txt first.

**File hierarchy (check in order):**
1. `llms-full.txt` - Complete documentation (largest)
2. `llms.txt` - Standard documentation
3. `llms-small.txt` - Condensed documentation (smallest)

## Grounding Checkpoint

Before executing, VERIFY:

- [ ] Base URL is accessible
- [ ] Check all three llms.txt variants in order
- [ ] Validate file content is actual documentation (not error page)
- [ ] Confirm file size is reasonable for the documentation scope

**DO NOT assume llms.txt exists. Always probe first.**

## Uncertainty Escalation

ASK USER instead of guessing when:

- Multiple llms.txt variants found - which size to use?
- llms.txt content appears partial or outdated
- File returns but content seems like an error page
- Site has llms.txt but content doesn't match expected documentation

**NEVER assume llms.txt quality without verification.**

## Context Scope

| Context Type | Included | Excluded |
|--------------|----------|----------|
| RELEVANT | Target base URL, llms.txt content | Full site scraping |
| PERIPHERAL | llms.txt spec reference | Other sites' llms.txt |
| DISTRACTOR | Previous scraping attempts | Unrelated documentation |

## Workflow Steps

### Step 1: Detect llms.txt

```bash
# Check for llms.txt variants (in order of preference)
curl -I https://example.com/llms-full.txt
curl -I https://example.com/llms.txt
curl -I https://example.com/llms-small.txt

# Check common alternate locations
curl -I https://example.com/.well-known/llms.txt
curl -I https://docs.example.com/llms.txt
```

### Step 2: Validate Content

```bash
# Fetch and inspect first 100 lines
curl -s https://example.com/llms.txt | head -100

# Check file size
curl -sI https://example.com/llms.txt | grep -i content-length

# Verify it's not an error page
curl -s https://example.com/llms.txt | grep -i "not found\|error\|404" && echo "WARNING: Malformed content detected."
```