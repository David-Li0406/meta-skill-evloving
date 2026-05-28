---
name: game-concept-design
description: Use this skill when you want to transform vague game ideas into structured design documents, ensuring clarity in gameplay mechanics and player experience.
---

# Skill body

## Overview

This skill provides a structured workflow to convert abstract game concepts into detailed design documents, focusing on gameplay mechanics, player experience, and core decisions.

## Workflow Steps

1. **Define Core Concept**  
   Create a one-sentence description that includes the player, their actions, and the emotional experience.  
   **Format:**  
   ```
   【Who】【What action】【What decisions】【What emotions】
   ```
   **Example:**  
   "Players choose actions from limited cards, surviving through a series of quick decisions."

2. **Set Experience Boundaries**  
   Define the limitations of the target experience:  
   - **Playtime:** Duration of a single play session.  
   - **Complexity:** Is it easy to understand or does it require a tutorial?  
   - **Action Density:** Is the gameplay busy or calm?  
   - **Exclusions:** Clearly outline what the game will not include.

3. **Analyze Reference Games**  
   Break down similar games into elements to determine what to include or exclude:  
   | Aspect | Include | Exclude |
   |--------|---------|---------|
   | Decision Frequency | | |
   | Randomness | | |
   | Persistent Growth | | |
   | Resource Management | | |

4. **Design Experience Curve**  
   Outline the intensity of decisions throughout the game:  
   ```
   Start: Understanding phase (no confusion)
   Mid: Decisions become challenging
   End: Choices require commitment
   ```

5. **Validate Concept**  
   Use a checklist to verify the concept:  
   - [ ] Can the game be explained in 30 seconds?  
   - [ ] Can the fun be described in terms of decisions rather than actions?  
   - [ ] Is there a reason to try again after failure?  
   If there are too many "NO" answers, return to Step 1.

6. **Output Design Document**  
   After completing all steps, generate a Markdown document using a predefined template.

## Output Format

```markdown
# {Game Name} Design Document

## 1. Core Concept
- {Core Concept}

## 2. Experience Boundaries
- Playtime: {Duration}
- Complexity: {Easy/Requires Tutorial}
- Action Density: {Busy/Calm}
- Exclusions: {What is not included}

## 3. Reference Game Analysis
| Aspect | Include | Exclude |
|--------|---------|---------|
| Decision Frequency | | |
| Randomness | | |
| Persistent Growth | | |
| Resource Management | | |

## 4. Experience Curve
- Start: {Description}
- Mid: {Description}
- End: {Description}

## 5. Validation Checklist
- [ ] {Checklist Item}
- [ ] {Checklist Item}
- [ ] {Checklist Item}
```