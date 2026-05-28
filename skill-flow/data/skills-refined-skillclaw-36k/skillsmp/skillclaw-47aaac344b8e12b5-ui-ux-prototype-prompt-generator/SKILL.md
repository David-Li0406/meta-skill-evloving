---
name: ui-ux-prototype-prompt-generator
description: Use this skill when you need to generate detailed, structured prompts for creating UI/UX prototypes, ensuring adherence to various design systems and comprehensive documentation.
---

# Skill body

## Overview

Generate comprehensive, production-ready prompts for UI/UX prototype creation. Transform user requirements into detailed technical specifications that include design systems, color palettes, component specifications, layout structures, and implementation guidelines. Output prompts are structured for optimal consumption by AI tools or human developers building HTML/CSS/React prototypes.

## When to Use This Skill

Use this skill when:
- Creating detailed design briefs for web or mobile applications.
- Generating structured prompts for AI-assisted UI design.
- Documenting UI specifications across multiple design systems.
- Building design handoff documentation for development teams.
- Prototyping mobile apps with specific design system constraints.
- Generating comprehensive design documentation from high-level concepts.

**Trigger phrases:**
- "Create a prototype prompt for [app description]"
- "Design a mobile app for [use case]"
- "Generate UI specifications for [feature]"
- "Build a design brief for [application type]"
- "Create design documentation for [platform]"

## Supported Design Systems

This skill generates prompts compatible with:

| Design System         | Platform                | Best For                                   |
|-----------------------|------------------------|--------------------------------------------|
| **WeChat Work**       | Enterprise messaging    | Internal enterprise apps, workflow tools   |
| **iOS Native (HIG)**  | Apple platforms        | Consumer iOS apps, native experiences     |
| **Material Design 3** | Android, Web           | Cross-platform apps, Google ecosystem      |
| **Ant Design Mobile** | Mobile web, Hybrid     | Admin panels, data-heavy mobile apps       |

**Automatic adaptation**: Prompts adjust component names, interaction patterns, and visual styles based on selected design system.

## Workflow

### Step 1: Gather Requirements

Begin by collecting essential information from the user. Ask targeted questions to understand:

- **Application Type & Purpose:** What kind of application? (e.g., enterprise tool, e-commerce, social media, dashboard)
- **Target Platform & Context:** iOS, Android, Web, or cross-platform? Device type?
- **Design Preferences:** Design style, brand colors, and any design references?
- **Feature Requirements:** Key pages, navigation structure, data to display, and user interactions?
- **Content & Data:** Actual content, empty states, error states, and specific business logic?
- **Technical Constraints:** Framework preference, CSS approach, image assets, and CDN dependencies?

**Ask questions incrementally** (2-3 at a time) to avoid overwhelming the user. Many details can be inferred from context or filled with sensible defaults.

### Step 2: Structure the Prompt

Generate a comprehensive prompt based on the gathered requirements, ensuring it aligns with the selected design system and includes all necessary specifications for development.