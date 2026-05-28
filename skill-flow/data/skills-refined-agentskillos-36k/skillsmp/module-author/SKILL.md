---
name: module-author
description: Generates module README.md with exercise planning table for CopilotTraining workshop modules. Researches URLs to understand new capabilities and creates strategic content outline. Use exercise-author skill to implement individual exercises.
---

# Module Author Skill

Generate module README.md with exercise planning for CopilotTraining workshop modules. This skill focuses on **module strategy and planning**—the exercise-author skill handles tactical implementation.

---

## When to Use This Skill

- Creating a new training module from scratch
- Updating module content when GitHub releases new capabilities
- Researching and planning exercises for a specific feature

**Invocation examples:**
- "Create module 7 on MCP servers using https://github.blog/mcp-announcement"
- "Update module 4 about custom instructions with https://docs.github.com/copilot/customizing"
- "Research https://code.visualstudio.com/docs/copilot/agents and create module 8"

---

## Core Module Design Principles

### Three Essential Goals

Every module must deliver on these three goals:

1. **Teach one capability** — Each module = one GitHub Copilot feature or technique
2. **Hands-on practice** — At least one exercise (typically 2-3) to let readers see/touch/use it
3. **Persona relevance** — Show why this matters to each persona type in a compelling way

### Single-File Structure (README.md)

Each module README.md (~100-150 lines) contains:

1. **Story So Far** — Progression from previous modules
2. **Why This Matters** — Relevance to ALL personas (Sarah, David, Marcus, Elena, Rafael)
3. **What You'll Learn** — Brief capability overview
4. **📋 Exercise Planning Table** — Detailed exercise specifications
5. **What This Feature Does** — Technical overview
6. **Next Up** — Preview of next module

**Exercise files are generated separately** by the exercise-author skill using the planning table as input.

---

## Core Principles (from copilot-instructions.md)

Before generating, review `.github/copilot-instructions.md` for:
- Training philosophy (Syntax Wizards → Markdown Whisperers)
- Persona characteristics and voice guidelines
- Metrics requirements (quantifiable improvements)
- Official docs requirements (1-3 GitHub/MS links)
- Emoji vocabulary for consistent visual language
- Section separators (`---` between all major sections)
- Outcome-based language (professionals demonstrating results, not students learning)

---

## URL Research Workflow

### When URL is Provided

If the user provides a URL (blog post, docs page, announcement):

1. **Extract key information:**
   - What capability is being introduced/updated?
   - What problem does it solve?
   - What are the main features or commands?
   - Any code examples or workflows shown?
   - Official documentation links referenced?

2. **Identify persona relevance:**
   - How would Sarah validate this with metrics?
   - How would David use his expertise with this?
   - What workflow friction does this remove for Marcus?
   - How does this affect Elena's testing process?
   - What business value does Rafael see?

3. **Plan exercises:**
   - What hands-on demonstrations would prove the value?
   - What artifacts would learners create?
   - What before/after metrics would be compelling?
   - Which persona should lead each exercise?

4. **Find official docs:**
   - Primary documentation URL
   - Related API/CLI reference
   - Best practices guide

---

## Template Structure

Use [TEMPLATE.md](TEMPLATE.md) as the base structure. The template includes all necessary sections with placeholder text and formatting.

### Key Sections to Fill

**1. Story So Far (2-3 paragraphs)**
- Summarize what was built in 2-3 previous modules
- Explain how those capabilities are currently being used
- Introduce the new challenge this module addresses
- Add Integration Note connecting to specific artifacts from previous module

**2. Why This Matters (All 5 Personas)**
- Write one outcome-focused statement per persona
- Include specific metrics or measurable improvements
- Show how capability delivers value to each role
- See persona voice guidelines in `.github/copilot-instructions.md`

**3. Exercise Planning Table (2-3 exercises)**
- One row per exercise with all columns filled
- Lead persona marked with ⭐, support personas with 🤝
- Problem column: current pain with specific metrics
- Solution column: brief description of what will be built
- Key Metrics column: before→after improvements
- Artifacts column: specific file paths that will be created

**4. What This Feature Does (Technical Overview)**
- 1-2 sentence capability explanation
- Specific use case ("when questions span X files...")
- 3 concrete artifacts learners will build
- 2-3 official documentation links
- Optional callout for critical tools/commands

**5. Next Module Preview**
- One sentence describing next capability
- Quote from a persona teasing the next challenge

---

## Exercise Table Column Specifications

When populating the exercise planning table in TEMPLATE.md:

**# (Exercise Number):**
- Format: `[N.X](exercise-0X.md)` where N = module number
- Links to exercise file (created by exercise-author skill)

**Exercise (Title):**
- Action-oriented, specific outcome
- Example: "Enforcing Review Standards" not "Learn Custom Instructions"

**Lead:**
- Primary persona (one only) with ⭐
- Whose story anchors this exercise

**Support:**
- 1-3 supporting personas with 🤝
- Who collaborates or benefits

**Problem:**
- Current pain point with specific metrics
- Format: "[Issue]: [time], [count], [rounds/cycles]"
- Example: "Manual reviews: 45 min/review, 8 violations/PR, 3 rounds"

**Solution:**
- Brief description of what will be built
- What capability solves the problem
- Example: "Custom instructions for React standards"

**Key Metrics:**
- Target improvements in shorthand
- Format: "before→after" for each metric
- Example: "45→5 min, 8→0 violations, 3→1 rounds"

---

## Exercise Planning Guidelines

### Step Count Goal: 3 Steps per Exercise

Each exercise specification should assume **~3 steps** in implementation:
- **Ideal**: 3 substantial, clear steps
- **Acceptable**: 2 steps if naturally cohesive, or 4-5 if complexity demands it
- **Consider splitting**: If you plan for more than 5 steps, consider if this should be 2 exercises

---

## Persona Distribution Guidelines

### Balance Across Module

Aim for diverse representation:
- Each persona should lead at least 1 exercise across every 2-3 modules
- Sarah and David typically lead architecture/standards exercises
- Marcus leads infrastructure/workflow exercises
- Elena leads testing/quality exercises
- Rafael leads requirements/analysis exercises

### Supporting Cast Selection

Choose support personas based on realistic collaboration:
- **Sarah + David** — Architecture and standards alignment
- **Marcus + Elena** — Testing infrastructure and automation
- **Sarah + Marcus** — Standards enforcement in CI/CD
- **Elena + Sarah** — Quality standards and review processes
- **Rafael + [any]** — Business requirements meet technical implementation

---

## Module Continuity Patterns

### Story So Far
- Summarize 2-3 previous modules in brief paragraphs
- Explain what capabilities were added and how they're being used
- Introduce the new challenge this module solves
- Add Integration Note showing how this builds on previous artifacts

### Next Module Preview
- One clear sentence about next capability
- Quote from a persona that teases the upcoming challenge
- Shows progression of complexity or integration

---

## Usage Guide

### 1. Research Phase (If URL Provided)

```bash
# User provides URL for research
"@module-author Create module 7 on MCP servers using https://github.blog/mcp-announcement"
```

**Research workflow:**
1. Read the provided URL content
2. Extract key capabilities and features
3. Identify how each persona would use this
4. Note official documentation links
5. Plan exercises that demonstrate value

### 2. Generate README.md

Using [TEMPLATE.md](TEMPLATE.md), create:

- **Story So Far** — Connection to previous modules
- **Why This Matters** — Individual statements for ALL 5 personas
- **What You'll Learn** — Brief capability overview
- **📋 Exercise Planning Table** — Detailed specifications for 2-3 exercises
- **What This Feature Does** — Technical overview with official docs
- **Next Up** — Preview of next module

### 3. Validate Against Checklist

- [ ] README.md is ~100-150 lines
- [ ] Story So Far connects to previous module's artifacts
- [ ] Why This Matters includes ALL personas (Sarah, David, Marcus, Elena, Rafael)
- [ ] Exercise planning table includes all required columns
- [ ] Each exercise has:
  - [ ] Clear lead persona (⭐) and support personas (🤝)
  - [ ] Specific problem with current metrics
  - [ ] Brief solution description
  - [ ] Target improvement metrics (before→after format)
  - [ ] Artifacts that will be created
- [ ] "What This Feature Does" includes 2-3 official documentation links
- [ ] Next Up preview included
- [ ] Section separators (`---`) between major sections

---

## Example Invocation

```
@module-author Create Module 4 on custom instructions. Research https://docs.github.com/copilot/customizing-github-copilot/adding-custom-instructions-for-github-copilot

Plan these exercises:
- Sarah enforcing React component standards (saves 40 min/review)
- Marcus automating build validation (saves 28 min/failure)
- Elena generating comprehensive test suites (saves 43 min/suite)
```

**Result:**
- `modules/04-custom-instructions/README.md` with:
  - Story connecting to Module 3's prompt libraries
  - Why This Matters for all 5 personas
  - Exercise planning table with 3 rows (detailed specifications)
  - Technical overview with official docs links
  - Next Up preview to Module 5

**Next steps:**
- User invokes `@exercise-author` to generate `exercise-01.md`, `exercise-02.md`, `exercise-03.md`

---

## Key Benefits of This Approach

**Research Integration:**
- ✅ Learn new capabilities from official sources
- ✅ Identify persona-relevant use cases
- ✅ Find authoritative documentation to reference

**Strategic Planning:**
- ✅ Module-level content strategy separate from exercise implementation
- ✅ Clear specifications for exercise-author to implement
- ✅ Ensures all personas are addressed at planning stage

**Iterative Refinement:**
- ✅ Update module overview without touching exercises
- ✅ Refine individual exercises independently
- ✅ Add new exercises without regenerating README

**Clear Separation:**
- ✅ module-author: Strategy, research, planning (README.md)
- ✅ exercise-author: Tactical implementation (exercise-*.md files)