---
name: gdd-creation
description: Game Design Document creation and structure
category: gamedesign
depends-on: []
---

# GDD Creation Skill

## Overview

This skill guides the creation and maintenance of Game Design Documents (GDD). A GDD is the master blueprint for a game, ensuring all team members understand the vision, mechanics, and requirements.

## When to Use This Skill

Use when:
- No GDD exists in the project
- Starting a new game project
- Major feature requires design documentation
- GDD needs updating due to changes
- Preparing for prototype or production

## GDD Document Structure

### Main Document: `docs/design/gdd.md`

```markdown
# Game Design Document - [Project Name]

## Document Info
- **Version:** X.X.X
- **Last Updated:** YYYY-MM-DD
- **Author:** Game Designer Agent
- **Status:** Draft | Review | Approved

---

## 1. Overview

### 1.1 High Concept
One to two sentence summary of the game.

### 1.2 Elevator Pitch
A 30-second pitch that hooks the listener.

### 1.3 Target Audience
- Primary audience: [description]
- Secondary audience: [description]
- Age rating: [ESRB/PEGI rating]

### 1.4 Platforms
- Target platforms: [list]
- Technical constraints: [list]

### 1.5 Unique Selling Points
- USP 1: [description]
- USP 2: [description]
- USP 3: [description]

---

## 2. Core Gameplay

### 2.1 Game Loop
[Minute-by-minute breakdown of player experience]

### 2.2 Core Mechanics
[Primary game systems and rules]

### 2.3 Win/Lose Conditions
- Victory conditions: [list]
- Defeat conditions: [list]
- Draw conditions: [if applicable]

### 2.4 Session Length
- Target session duration: [X minutes]
- Match duration: [Y minutes]
- Expected engagement: [Z hours/week]

---

## 3. Mechanics

### 3.1 Movement
[How players move through the world]

### 3.2 Combat/Interaction
[How players interact with the game world]

### 3.3 Progression
[How players advance/grow]

### 3.4 Special Systems
[Unique mechanics that don't fit elsewhere]

---

## 4. Characters & Classes

### 4.1 Character Archetypes
[List of character types]

### 4.2 Abilities & Skills
[What characters can do]

### 4.3 Stats & Attributes
[Character properties]

### 4.4 Customization
[How players personalize characters]

---

## 5. Weapons & Items

### 5.1 Weapon Categories
[Types of weapons]

### 5.2 Item System
[How items work]

### 5.3 Balance Considerations
[Rock-paper-scissors relationships]

---

## 6. Level Design

### 6.1 Map Layout Principles
[Design philosophy for levels]

### 6.2 Flow Analysis
[How players move through spaces]

### 6.3 Spawn Points
[Where players enter/exit]

### 6.4 Key Locations
[Important places in levels]

---

## 7. UI/UX

### 7.1 HUD Elements
[What's shown on screen]

### 7.2 Menu Flow
[Navigation structure]

### 7.3 Controls
[Input schemes per platform]

### 7.4 Accessibility
[Inclusive design features]

---

## 8. Progression

### 8.1 Leveling System
[How players advance]

### 8.2 Rewards
[What players earn]

### 8.3 Economy
[Currency systems, sinks/faucets]

---

## 9. Multiplayer (if applicable)

### 9.1 Match Structure
[How matches are formed]

### 9.2 Team Balancing
[How teams are composed]

### 9.3 Network Considerations
[Latency handling, sync strategy]

---

## 10. Audio/Visual

### 10.1 Art Style
[Visual direction]

### 10.2 Sound Design
[Audio philosophy]

### 10.3 Music
[Music approach]

---

## 11. Technical Considerations

### 11.1 Platform Constraints
[Technical limitations]

### 11.2 Performance Targets
[FPS, load times, etc.]

### 11.3 Localization
[Language support]

---

## Appendix

### Glossary
[Game-specific terminology]

### References
[Inspiration games, documents]

### Version History
| Version | Date | Changes |
|---------|------|---------|
```

---

## Supporting Artifacts

The GDD is supported by separate documents:

| Artifact | Purpose | Location |
|----------|---------|----------|
| Core Loop Spec | Minute-by-minute gameplay | `docs/design/core_loop.md` |
| Decision Log | Design decisions with rationale | `docs/design/decision_log.md` |
| Open Questions | Unresolved design questions | `docs/design/open_questions.md` |
| Gear Registry | Items, weapons, equipment | `docs/design/gear_registry.md` |
| Map Templates | Level designs | `docs/design/map_templates.md` |
| Economy Model | Currency systems | `docs/design/economy_model.md` |
| Visual Language | Art/UX direction | `docs/design/visual_language.md` |
| Tech Spec | Technical requirements | `docs/design/tech_spec.md` |
| MVD Checklist | Prototype readiness | `docs/design/mvd_checklist.md` |

---

## GDD Creation Workflow

### Step 1: Repository Analysis

Gather context about the project:

```powershell
# Read project files
$readme = Get-Content "README.md" -Raw
$packageJson = Get-Content "package.json" -Raw | ConvertFrom-Json
$prd = Get-Content "prd.json" -Raw | ConvertFrom-Json

# Explore source structure
Get-ChildItem -Path "src/" -Recurse -File
```

Document:
- Project type and genre
- Current implementation status
- Technology stack
- Team size and structure

### Step 2: Research Phase

Use web-search and GitHub MCP:
- Research similar games
- Find reference implementations
- Document inspirations
- Identify best practices

### Step 3: Design Sessions

Use thermite-design skill for structured sessions:
- Boardroom Retreat for core concepts
- Deep Dive for specific domains
- Decision Review for validation

### Step 4: Draft GDD

Create the main GDD document with all sections.

### Step 5: Iterate

Refine through self-iteration and team feedback.

---

## GDD Review Checklist

Before marking GDD as ready:

### Completeness
- [ ] All 11 main sections complete
- [ ] Supporting artifacts created
- [ ] Decision log has initial entries
- [ ] Open questions tracked

### Quality
- [ ] Clear, unambiguous language
- [ ] No contradictions within document
- [ ] All mechanics described in detail
- [ ] Art style is specific

### Usability
- [ ] Table of contents for navigation
- [ ] Cross-references between sections
- [ ] Version history maintained
- [ ] Glossary for game-specific terms

---

## GDD Maintenance

### When to Update

Update GDD when:
- New mechanics are added
- Existing mechanics change significantly
- Balance changes are implemented
- New features are planned
- Team requests clarification

### Version Control

- Use semantic versioning (X.Y.Z)
- Major version: Complete overhauls
- Minor version: Feature additions
- Patch version: Clarifications, small fixes

### Change Log

Maintain a change log in the GDD:

```markdown
## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2025-01-21 | Game Designer | Initial draft |
| 0.2.0 | 2025-01-22 | Game Designer | Added combat section |
```

---

## Common Mistakes to Avoid

| Mistake | Why It's Bad | Fix |
|---------|--------------|-----|
| Too vague | Developers won't know what to build | Be specific with numbers and examples |
| Over-specifying | Stifles creativity, hard to maintain | Focus on what, not how |
| No versioning | Can't track changes | Always version your GDD |
| Ignoring technical constraints | Unrealistic designs | Consult technical team early |
| Writing for AAA scope on indie budget | Unrealistic expectations | Scope appropriately |
| Not updating | Document becomes obsolete | Maintain regularly |
