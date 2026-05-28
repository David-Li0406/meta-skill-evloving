---
name: game-loop-design
description: Core gameplay loop design documentation
category: gamedesign
depends-on: [thermite-integration]
---

# Game Loop Design

## Overview

The core loop is the minute-by-minute experience of playing your game. This skill provides guidance for documenting and designing effective game loops.

## When to Use This Skill

Use when:
- Defining the core gameplay loop
- Mapping the player experience over time
- Designing session structures
- Identifying pacing issues

## Core Loop Template

```markdown
# Core Loop Specification v[X.X]
**Last Updated:** YYYY-MM-DD
**Owners:** [Designers]

## Loop Overview
```
[PRE-GAME] → [SESSION] → [POST-GAME] → [LOOP BACK]
```

## Session Structure

### Pre-Game Phase
**Duration:** [Target time]

**Player Actions:**
1. [Action 1]
2. [Action 2]
3. [Action 3]

**Emotional Beat:** [Feeling player has]

**Objectives:**
- [Goal 1]
- [Goal 2]

---

### Session Start (0:00 - [X:XX])

**State:** Players [enter spawn/start]
**Objectives:** [Initial goals]
**Threats:** [What can hurt players]
**Emotional Beat:** [Feeling]

**Key Events:**
- [X:XX] - [Event 1]
- [Y:YY] - [Event 2]

---

### Early Game ([X:XX] - [Y:YY])

**State:** [Game state description]
**Objectives:** [What players should do]
**Threats:** [What challenges exist]
**Emotional Beat:** [Feeling]

---

### Mid Game ([Y:YY] - [Z:ZZ])

**State:** [Game state description]
**Objectives:** [What players should do]
**Threats:** [What challenges exist]
**Emotional Beat:** [Feeling]

---

### Late Game ([Z:ZZ] - [End])

**State:** [Game state description]
**Objectives:** [Final objectives]
**Threats:** [Maximum challenges]
**Emotional Beat:** [Feeling]

---

### End Game

**Victory Conditions:**
- [Condition 1]
- [Condition 2]

**Defeat Conditions:**
- [Condition 1]
- [Condition 2]

**Rewards:**
- [What players earn]
- [Progression updates]

---

## Post-Game Phase

**Duration:** [Target time]

**Player Actions:**
1. [Action 1]
2. [Action 2]

**Emotional Beat:** [Feeling]

**Session Loop:** [What brings players back]
```

## Loop Design Principles

### Engagement

Keep players engaged by:
- **Immediate action** - Something to do right away
- **Clear goals** - Know what to do next
- **Meaningful choices** - Decisions that matter
- **Feedback** - See results of actions

### Pacing

Create tension through:
- **Buildup** - Escalate towards climax
- **Variation** - Mix fast/slow moments
- **Surprises** - Unexpected events
- **Release** - Tension breaks

### Progression

Enable growth through:
- **Learning** - Skills improve over time
- **Unlocking** - New content available
- **Building** - Accumulate resources
- **Advancing** - Move through content

## Session Flow Diagrams

### Text-Based Flow

```
┌─────────┐
│ LOBBY   │
└────┬────┘
     │
     ▼
┌─────────┐
│ MATCH   │◄──────────────────────┐
└────┬────┘                        │
     │                            │
     ├──────────┬─────────┐      │
     │          │         │      │
     ▼          ▼         ▼      ▼
┌────────┐ ┌───────┐ ┌──────┐ ┌──────┐
│EXPLORE│ │FIGHT  │ │LOOT  │ │OBJ   │
└────────┘ └───────┘ └──────┘ └──────┘
     │          │         │      │
     └──────────┴─────────┴──────┘
                    │
                    ▼
              ┌─────────┐
              │EXTRACT  │
              └─────────┘
                    │
                    ▼
              ┌─────────┐
              │ SUMMARY │
              └────┬────┘
                   │
                   ▼
              ┌─────────┐
              │  LOBBY  │
              └─────────┘
```

## Common Loop Patterns

### Round-Based

Discrete turns with planning phases:
1. Plan phase
2. Execution phase
3. Resolution phase
4. Reward phase

### Real-Time

Continuous action with moments:
1. Constant engagement
2. Peaks and valleys
3. No pausing
4. Immediate feedback

### Session-Based

Complete matches with:
1. Preparation phase
2. Main gameplay
3. Conclusion phase
4. Summary/rewards

## Loop Review Checklist

Before finalizing the core loop:

- [ ] Minute-by-minute flow documented
- [] Session phases defined
- [ ] Emotional beats mapped
- [ ] Pacing is appropriate
- [ ] Engagement maintained
- [ ] Goals are clear
- [ ] Feedback is immediate
- [ ] Win/lose conditions defined
- [ ] Progression tied to loop
- [ ] Technical feasibility confirmed
