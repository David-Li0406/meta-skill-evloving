---
name: latex-posters
description: Use this skill when you need to create professional research posters in LaTeX for conferences, academic events, or public engagement, ensuring effective visual communication through layout design and figure integration.
---

# LaTeX Research Posters

## Overview

Research posters are a critical medium for scientific communication at conferences, symposia, and academic events. This skill provides comprehensive guidance for creating professional, visually appealing research posters using LaTeX packages such as beamerposter, tikzposter, or baposter. Generate publication-quality posters with proper layout, typography, color schemes, and visual hierarchy.

## When to Use This Skill

This skill should be used when:
- Creating research posters for conferences, symposia, or poster sessions.
- Designing academic posters for university events or thesis defenses.
- Preparing visual summaries of research for public engagement.
- Converting scientific papers into poster format.
- Creating template posters for research groups or departments.
- Designing posters that comply with specific conference size requirements (A0, A1, 36×48", etc.).
- Building posters with complex multi-column layouts.
- Integrating figures, tables, equations, and citations in poster format.

## Visual Enhancement with Scientific Schematics

**⚠️ MANDATORY: Every research poster MUST include at least 2-3 AI-generated figures using the scientific-schematics skill.**

Before finalizing any poster:
1. Generate a minimum of TWO schematics or diagrams.
2. Target 3-4 figures for comprehensive posters (methodology flowchart, key results visualization, conceptual framework).
3. Figures should occupy 40-50% of the poster area.

**How to generate figures:**
- Use the **scientific-schematics** skill to generate AI-powered publication-quality diagrams.
- Describe your desired diagram in natural language.
- Nano Banana Pro will automatically generate, review, and refine the schematic.

**How to generate schematics:**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

## Critical Considerations

### Content Overflow Prevention

**⚠️ POSTERS MUST NOT HAVE TEXT OR CONTENT CUT OFF AT EDGES.**

**Common Overflow Problems:**
1. Title/footer text extending beyond page boundaries.
2. Too many sections crammed into available space.
3. Figures placed too close to edges.
4. Text blocks exceeding column widths.

**Prevention Rules:**
- Limit content sections to a maximum of 5-6 for A0 posters.

### Font Requirements

**⚠️ ALL text within AI-generated visualizations MUST be poster-readable.**

When generating graphics for posters, ensure that font size specifications are included in every prompt. Poster graphics should be designed for visibility from 4-6 feet away.

### Standard Workflow

1. Plan all visual elements needed (title, intro, methods, results, conclusions).
2. Generate each element using scientific-schematics or Nano Banana Pro.
3. Assemble generated images in the LaTeX template.
4. Add text content around the visuals.

**Target: 60-70% of poster area should be AI-generated visuals, 30-40% text.**