---
name: game-concept-and-requirements
description: Use this skill when you want to transform vague game ideas into structured concepts and requirements, or when you need to create a simple prototype to test gameplay hypotheses.
---

# Game Concept and Requirements Skill

This workflow helps in defining game concepts, requirements, and creating a simple prototype to validate gameplay ideas.

## Workflow Overview

The process consists of several steps to transform ideas into structured documents and prototypes.

### Concept Design

1. **One-Sentence Concept**: Refine the game idea into a single sentence that includes who, what action, repeated judgments, and emotional outcomes.
2. **Target Experience Limitation**: Define playtime, complexity, operation density, and what will not be included.
3. **Reference Game Breakdown**: Analyze existing games to extract design intentions.
4. **Experience Intensity Curve**: Design the weight of decisions throughout the gameplay.
5. **Concept Validation**: Self-check the concept with specific yes/no questions.

### Game Requirements Definition

1. **Play Cycle Definition**: Define what players will repeat in a single play session.
2. **Victory and Defeat Conditions**: Clearly state the conditions for winning, losing, and being unable to continue.
3. **Player Actions**: List possible actions in verb form.
4. **Game Element Definition**: Identify the components that can be systematized.
5. **Variable and Value Estimation**: Outline adjustable parameters.
6. **Expected Play Flow**: Simulate a complete play session.

### Single-Screen Prototype Creation

1. **State Design**: Extract player state and resource constraints from the concept design.
2. **Choice Design**: Define 3-5 distinct choices for players.
3. **Implementation**: Create a prototype using any technology (HTML+JS, React, etc.) based on a simple template.
4. **Validation**: Playtest the prototype and ask specific questions to assess if the gameplay hypothesis holds.

## Output Formats

### Concept Document

After completing the concept design steps, generate a Markdown document that includes:

```markdown
# {Game Name} Concept Document

## 1. One-Sentence Concept
- ...

## 2. Target Experience
- Playtime: ...
- Complexity: ...
- ...

## 3. Reference Game Breakdown
| Aspect | Include | Exclude |
|--------|---------|---------|
| ...    |         |         |

## 4. Experience Intensity Curve
- Start: ...
- Mid: ...
- End: ...

## 5. Concept Validation
- [ ] Can I explain the game in 30 seconds?
- ...
```

### Requirements Document

For the requirements definition, the output should be structured as follows:

```markdown
# {Game Name} Requirements Document

## 1. Play Cycle
- ...

## 2. Victory and Defeat Conditions
- ...

## 3. Player Actions
- ...

## 4. Game Elements
### Player
- ...

## 5. Variable Design
| Variable | Range | Initial Value |
|----------|-------|---------------|
| HP       | ...   | ...           |

## 6. Expected Play Flow
### Turn 1
- ...
```

### Prototype Validation

Ensure the prototype meets the following criteria:
- It is a single screen.
- It can be interacted with without instructions.
- Players want to try it multiple times.
- Each cycle completes in 3-5 minutes.

This skill is designed to help you systematically develop and test game concepts, ensuring that your ideas are both structured and validated through practical prototyping.