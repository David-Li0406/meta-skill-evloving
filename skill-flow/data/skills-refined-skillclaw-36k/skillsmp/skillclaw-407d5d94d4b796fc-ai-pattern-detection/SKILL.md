---
name: ai-pattern-detection
description: Use this skill when you need to detect AI-generated writing patterns and suggest more authentic alternatives to enhance the quality of written content.
---

# AI Pattern Detection Skill

## Purpose

Automatically scan content for AI-generated writing patterns and provide authentic alternatives. This skill activates when generating or reviewing text content, ensuring outputs maintain human-like authenticity.

## When This Skill Applies

- Generating any prose, documentation, or written content
- Reviewing or editing existing documents
- User mentions "AI detection", "writing quality", "authentic voice"
- User asks to "make it sound more natural" or "less robotic"
- Creating marketing copy, documentation, or communications

## Detection Categories

### Critical Patterns (Always Flag)

These immediately identify content as AI-generated:

1. **Corporate Buzzwords**: "seamlessly integrates", "cutting-edge", "revolutionary", "next-generation", "comprehensive solution"
2. **Vague Intensifiers**: "dramatically improves", "significantly enhances", "vastly superior"
3. **Formulaic Transitions**: "Moreover,", "Furthermore,", "Additionally,", "In conclusion,"
4. **Performative Language**: "aims to provide", "strives to achieve", "designed to enhance"
5. **Academic Passive**: "It has been observed that...", "It can be argued that..."

### Structural Patterns (Flag When Overused)

1. **Three-item lists**: "reliable, scalable, and secure"
2. **Em-dash overuse**: Multiple em-dashes in a paragraph
3. **Identical paragraph structure**: Topic → 3 points → conclusion repeated
4. **Balanced hedging**: "While X has challenges, it also offers opportunities"

### Contextual Patterns (Check Frequency)

Words acceptable at 1:1000 ratio but problematic at 1:100:
- manifest, revolutionary, next-generation
- robust, scalable, comprehensive
- synergy, leverage, utilize

## Replacement Guidelines

| Instead of | Use |
|-----------|-----|
| "plays a crucial role" | "handles" / "manages" / "does" |
| "seamlessly integrates" | "works with" / "connects to" |
| "cutting-edge" | "new" / "recent" / specific tech name |
| "Moreover," | [just start the next sentence] |
| "comprehensive solution" | [specific description of what it does] |
| "dramatically improves" | [specific metric: "reduces latency by 40%"] |
| "robust" | "handles X requests/second" |