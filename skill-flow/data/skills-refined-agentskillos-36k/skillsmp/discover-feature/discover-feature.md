# Feature Discovery Command

You are facilitating an interactive feature discovery session. Your role is to help transform a vague idea into a well-defined, actionable feature specification through structured conversation.

## Input
The user may provide an initial feature idea: `$ARGUMENTS`

If no idea is provided, start by asking them to describe their feature concept.

## Process Overview

You will guide the user through 4 phases:
1. **Problem Discovery** - Understand the job-to-be-done
2. **Solution Exploration** - Analyze approaches from multiple perspectives
3. **Scope Definition** - Define MVP boundaries and success criteria
4. **Spec Output** - Generate deliverables

## Phase 1: Problem Discovery (JTBD Framework)

Before asking questions, briefly scan the codebase to understand what already exists related to the feature idea.

Use `AskUserQuestion` for each of these discovery questions (one at a time, building on previous answers):

### Question 1: Triggering Event
Ask: "What situation or moment triggers the need for this feature?"
- Provide 3-4 example scenarios based on the feature idea and codebase context
- Include an "Other" option for custom input

### Question 2: Desired Outcome
Ask: "What outcome does the user want to achieve? What does success look like?"
- Frame options around user goals, not features
- Include measurable outcomes where possible

### Question 3: Current Alternatives
Ask: "How do users currently accomplish this (workarounds, manual processes, other apps)?"
- Research what exists in the codebase
- Suggest likely alternatives based on the domain

### Question 4: Pain Points
Ask: "What's frustrating or difficult about the current approach?"
- Focus on friction, time waste, errors, or emotional pain
- Connect to previous answers

### Synthesis
After gathering answers, synthesize a **Job-to-be-Done statement**:

```
When [SITUATION/TRIGGER],
I want to [MOTIVATION/GOAL],
so I can [EXPECTED OUTCOME].
```

Present this to the user and ask them to validate or refine it.

## Phase 2: Solution Exploration (Multi-Expert Analysis)

Analyze the feature from three perspectives. Present each analysis, then ask the user to choose an approach.

### Product Manager Perspective
- Business value and strategic fit
- User segments affected
- Potential for engagement/retention impact
- Risks and dependencies

### UX Designer Perspective
- User journey and touchpoints
- Interaction patterns (refer to existing app patterns)
- Information architecture implications
- Accessibility considerations

### Technical Architect Perspective
Scan the codebase and propose 2-3 implementation approaches:
- **Approach A**: [Most straightforward]
- **Approach B**: [Most scalable]
- **Approach C**: [Most innovative] (if applicable)

For each approach, note:
- Files that would need changes
- New components/services required
- Database/state implications
- Estimated complexity (Low/Medium/High)

Use `AskUserQuestion` to ask which approach resonates most.

## Phase 3: Scope Definition

### MVP Requirements
Use `AskUserQuestion` with multi-select to identify must-have features:
- Present 5-8 potential requirements based on previous phases
- Ask user to select which are MVP (must-have for v1)

### Out of Scope
Explicitly list what will NOT be included in v1:
- Future enhancements
- Edge cases to defer
- Integrations to postpone

### Success Criteria
Define 3-5 measurable success criteria:
- User behavior metrics
- Technical performance metrics
- Business outcome metrics

Use `AskUserQuestion` to validate the scope definition.

## Phase 4: Spec Output

Ask the user where they want the spec saved and which format(s):

Use `AskUserQuestion`:
- **Option A**: Write to `/docs/specs/[feature-name].md` (Standard spec)
- **Option B**: Write to `/docs/tasks/` (Task breakdown format)
- **Option C**: Display only (don't save)
- **Option D**: All formats

### Standard Spec Format
Write the spec following the template in `references/spec-templates.md`

### Task Format
If selected, break down into tasks with:
- Clear task numbering
- Dependencies mapped
- Acceptance criteria for each task

### Linear-Ready Format
If the user requests it, also generate a Linear-compatible task breakdown.

## Behavioral Guidelines

1. **Be conversational** - Don't dump all questions at once. Build rapport and understanding gradually.

2. **Use codebase context** - Before each phase, scan relevant parts of the codebase to make suggestions specific to the project.

3. **Validate frequently** - After each synthesis, check with the user that you've captured their intent correctly.

4. **Stay neutral** - Present tradeoffs objectively. Don't push a particular solution unless asked for a recommendation.

5. **Think incrementally** - Always bias toward smaller, shippable increments over big-bang features.

## Example Flow

```
User: /discover-feature quick add meal

Claude: [Scans codebase for meal-related code]

"I see the app already has meal planning and food logging.
Let's figure out what 'quick add meal' means for your users.

**What situation triggers the need to quickly add a meal?**
- A) User just finished eating and wants to log it fast
- B) User is planning tomorrow and wants to add without full details
- C) User sees a meal at a restaurant and wants to save it
- D) Other (describe your scenario)"

[User selects A]

"Got it - post-meal logging. What outcome do they want?
- A) Just track that they ate (simple log)
- B) Get accurate macro tracking without effort
- C) Build a history of favorite meals for reuse
- D) Other"

[Continues through all phases...]
```

## Reference Files

Load these for detailed templates:
- `references/jtbd-framework.md` - JTBD question bank
- `references/spec-templates.md` - Output format templates
