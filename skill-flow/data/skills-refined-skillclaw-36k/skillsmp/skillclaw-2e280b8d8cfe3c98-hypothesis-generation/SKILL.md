---
name: hypothesis-generation
description: Use this skill when you need to generate testable hypotheses from observations, design experiments, and explore competing explanations in scientific inquiry across various domains.
---

# Scientific Hypothesis Generation

## Overview

Hypothesis generation is a systematic process for developing testable explanations. Formulate evidence-based hypotheses from observations, design experiments, explore competing explanations, and develop predictions. Apply this skill for scientific inquiry across domains.

## When to Use This Skill

This skill should be used when:
- Developing hypotheses from observations or preliminary data
- Designing experiments to test scientific questions
- Exploring competing explanations for phenomena
- Formulating testable predictions for research
- Conducting literature-based hypothesis generation
- Planning mechanistic studies across scientific domains

## Visual Enhancement with Scientific Schematics

**⚠️ MANDATORY: Every hypothesis generation report MUST include at least 1-2 AI-generated figures using the scientific-schematics skill.**

This is not optional. Hypothesis reports without visual elements are incomplete. Before finalizing any document:
1. Generate at minimum ONE schematic or diagram (e.g., hypothesis framework showing competing explanations).
2. Prefer 2-3 figures for comprehensive reports (mechanistic pathway, experimental design flowchart, prediction decision tree).

**How to generate figures:**
- Use the **scientific-schematics** skill to generate AI-powered publication-quality diagrams.
- Simply describe your desired diagram in natural language.
- Nano Banana Pro will automatically generate, review, and refine the schematic.

**How to generate schematics:**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

The AI will automatically:
- Create publication-quality images with proper formatting.
- Review and refine through multiple iterations.
- Ensure accessibility (colorblind-friendly, high contrast).
- Save outputs in the figures/ directory.

**When to add schematics:**
- Hypothesis framework diagrams showing competing explanations.
- Experimental design flowcharts.
- Mechanistic pathway diagrams.
- Prediction decision trees.
- Causal relationship diagrams.
- Theoretical model visualizations.
- Any complex concept that benefits from visualization.