# Game Systems Doc

AAA-quality Game Design Document creation for casino-farming hybrid games.

## Expertise

This skill provides professional GDD writing covering:

- **System Design Documents**: Detailed mechanic specifications
- **Feature Briefs**: One-pagers for new features
- **Technical Design Docs**: Implementation specifications
- **Economy Documents**: Currency and resource flows
- **Balancing Spreadsheets**: Numbers and formulas
- **Minigame Specs**: Self-contained game documents
- **User Stories**: Player-focused requirements
- **Acceptance Criteria**: Definition of done

## When to Use

Invoke this skill when you need to:

- Create formal game design documentation
- Spec out a new feature or system
- Document minigame mechanics
- Write technical requirements
- Create economy/balance documents
- Prepare handoff docs for development

## Document Templates

### System Design Document

```markdown
# [System Name]

## Overview
Brief description of what this system does.

## Player Goals
What the player is trying to achieve.

## Core Loop
1. Step one
2. Step two
3. Step three

## Mechanics
### Mechanic A
- Description
- Rules
- Edge cases

## UI/UX Requirements
- Screen mockups
- Interaction flows

## Data Model
- Entities
- Relationships

## Success Metrics
- KPIs to track

## Open Questions
- Decisions needed
```

### Feature Brief (One-Pager)

```markdown
# Feature: [Name]

**Goal**: What problem does this solve?
**Players**: Who is this for?
**Core Mechanic**: One sentence description
**Success Looks Like**: Measurable outcome
**Dependencies**: What's needed first
**Risks**: What could go wrong
**Estimate**: T-shirt size (S/M/L/XL)
```

### Minigame Spec

```markdown
# Minigame: [Name]

## Hook
Why players will want to play this.

## Rules
1. How to play
2. Win conditions
3. Lose conditions

## Controls
- Input mapping
- Mobile considerations

## Rewards
- What players earn
- Frequency

## Integration
- Where it appears in main game
- Triggers/unlocks

## Art Requirements
- Asset list
- Animation needs

## Audio Requirements
- SFX list
- Music mood
```

## Documentation Standards

### Writing Style
- Clear, concise language
- Present tense ("The player collects...")
- Active voice
- Numbered lists for sequences
- Bullet points for options

### Visual Aids
- Flowcharts for systems
- Tables for data
- Mockups for UI
- Diagrams for relationships

### Version Control
- Date all documents
- Track changes
- Note authors

## Integration

This skill works alongside:

- `game-concept-advisor` - Ideas to document
- `casino-math-balancer` - Math to spec
- `drizzle-game-schema` - Data models to document

## Usage in Claude Code

```
/game-systems-doc

"Write a GDD for the meta-pot betting system..."
"Create a feature brief for robot companions..."
"Spec out the seasonal farming cycle..."
```
