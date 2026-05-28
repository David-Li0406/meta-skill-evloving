---
name: pptx-posters
description: Use this skill when you need to create research posters in HTML/CSS format that can be exported to PDF or PPTX, specifically when the user requests a PowerPoint format.
---

# PPTX Research Posters (HTML-Based)

## Overview

**⚠️ USE THIS SKILL ONLY WHEN USER EXPLICITLY REQUESTS PPTX/POWERPOINT POSTER FORMAT.**

For standard research posters, use the **latex-posters** skill instead, which provides better typographic control and is the default for academic conferences.

This skill creates research posters using HTML/CSS, which can then be exported to PDF or converted to PowerPoint format. The web-based approach offers:
- Modern, responsive layouts
- Easy integration of AI-generated visuals
- Quick iteration and preview in browser
- Export to PDF via browser print function
- Conversion to PPTX if specifically needed

## When to Use This Skill

**ONLY use this skill when:**
- User explicitly requests "PPTX poster", "PowerPoint poster", or "PPT poster"
- User specifically asks for HTML-based poster
- User needs to edit poster in PowerPoint after creation
- LaTeX is not available or user requests non-LaTeX solution

**DO NOT use this skill when:**
- User asks for a "poster" without specifying format → Use latex-posters
- User asks for "research poster" or "conference poster" → Use latex-posters
- User mentions LaTeX, tikzposter, beamerposter, or baposter → Use latex-posters

## AI-Powered Visual Element Generation

**STANDARD WORKFLOW: Generate ALL major visual elements using AI before creating the HTML poster.**

This is the recommended approach for creating visually compelling posters:
1. Plan all visual elements needed (hero image, intro, methods, results, conclusions)
2. Generate each element using scientific-schematics or Nano Banana Pro
3. Assemble generated images in the HTML template
4. Add text content around the visuals

**Target: 60-70% of poster area should be AI-generated visuals, 30-40% text.**

### CRITICAL: Poster-Size Font Requirements

**⚠️ ALL text within AI-generated visualizations MUST be poster-readable.**

When generating graphics for posters, you MUST include font size specifications in EVERY prompt. Poster graphics are viewed from 4-6 feet away, so text must be LARGE.