---
name: planz
description: Multi-agent intelligence workflow for prompt understanding, clarification, and planning. Coordinates Research, Survey, and Plan agents to transform vague user intent into actionable roadmaps.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite, AskUserQuestion
user-invocable: true
---

# Inference Planz Skill

This skill enables a sophisticated multi-agent workflow for understanding user prompts, gathering clarifications, and producing production-grade implementation plans.

## How It Works

### Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    INFERENCE PLANZ PIPELINE                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 0: INPUT NORMALIZATION                                      │
│ - Trim whitespace, remove trigger prefix                         │
│ - Detect language and tone                                       │
│ - Extract: entities, constraints, objectives, deliverables       │
│ - Create structured context object                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: RESEARCH AGENT                                           │
│ Purpose: Deep research and thinking on user intent               │
│ Output:                                                          │
│   - Intent summary                                               │
│   - Assumptions inferred                                         │
│   - Key unknowns                                                 │
│   - Constraints detected                                         │
│   - Approach options (A, B, C with tradeoffs)                    │
│   - Risks and mitigations                                        │
│   - Success criteria                                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: SURVEY AGENT                                             │
│ Purpose: Generate clarification questions                        │
│ Inputs: Original prompt + Research synthesis                     │
│ Output: Multiple-choice survey (5-10 questions)                  │
│   - Each question: 3-7 options (A, B, C, D, etc.)               │
│   - Include "Other" when appropriate                             │
│   - Covers: goal, user, format, scope, constraints, timeline     │
│   - Final confirmation question                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: PLAN AGENT                                               │
│ Purpose: Create actionable roadmap                               │
│ Inputs: Original prompt + Research + Survey questions            │
│ Output (provisional until survey answered):                      │
│   - Project overview                                             │
│   - Milestones and phases                                        │
│   - Detailed task breakdown                                      │
│   - Interfaces and contracts                                     │
│   - Data structures                                              │
│   - Failure modes and recovery                                   │
│   - Test plan                                                    │
│   - Definition of Done                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FINAL OUTPUT COMPOSITION                                         │
│ 1. Inference Planz Summary                                       │
│ 2. Research Synthesis                                            │
│ 3. Clarification Survey                                          │
│ 4. Provisional Roadmap Plan                                      │
│ 5. Proceed Question                                              │
└─────────────────────────────────────────────────────────────────┘
```

## Agent Specifications

### Research Agent

**Objective**: Perform deep research and thinking on what the user is truly asking

**Prompt Template**:
```
You are a Research Agent analyzing a user's request. Your job is to deeply understand their intent and provide structured analysis.

User Request: {user_prompt}

Analyze this request and provide:

1. **Intent Summary**: What is the user truly trying to accomplish?

2. **Assumptions Inferred**: What assumptions can we reasonably make?

3. **Key Unknowns**: What critical information is missing?

4. **Constraints Detected**: What limitations or requirements are implied?

5. **Recommended Approaches**:
   - **Option A**: [Description] - Tradeoffs: [pros/cons]
   - **Option B**: [Description] - Tradeoffs: [pros/cons]
   - **Option C**: [Description] - Tradeoffs: [pros/cons]

6. **Risks and Mitigations**: What could go wrong and how to prevent it?

7. **Success Criteria**: How do we know when this is done well?

Be concise but thorough. Focus on actionable insights.
```

### Survey Agent

**Objective**: Generate targeted multiple-choice questions for INTERACTIVE clarification

## ⚠️ CRITICAL REQUIREMENT: USE AskUserQuestion TOOL ⚠️

**The Survey Agent generates JSON. YOU MUST then CALL the `AskUserQuestion` tool.**

❌ **NEVER** output text-based surveys like "Type 1C 2D 3A..."
❌ **NEVER** display A) B) C) D) options as plain text
✅ **ALWAYS** call `AskUserQuestion` tool to render interactive clickable options

**Output Format**: The Survey Agent outputs structured JSON that MUST BE PARSED and used to CALL `AskUserQuestion` tool for an interactive user experience.

**Interactive Survey Features**:
- 🚨 **Accept All ✅**: First question MUST be "✅ Accept All Recommended" to skip survey and proceed with intelligent defaults
- 🎯 **Recommended Answers**: Each question marks the best option with `✅` emoji at START of label for **GREEN text**
- 🟢 **Green Styling**: The `✅` emoji renders as green text in Claude Code terminal
- 🖱️ **Clickable Options**: Users select options via buttons/chips instead of typing "1B 2D 3A"
- 📝 **Descriptions**: Each option includes a brief explanation of implications
- 🔄 **Batched Questions**: Questions presented in groups of 4 (AskUserQuestion tool limit)
- ✅ **Other Option**: Automatically provided for custom user input

**Accept All Feature** (MUST be presented FIRST before any other questions):
```json
{
  "question": "Research complete! Would you like to accept all recommended defaults or review each question?",
  "header": "Quick Start",
  "multiSelect": false,
  "options": [
    { "label": "✅ Accept All Recommended", "description": "Skip survey, use intelligent defaults based on research synthesis" },
    { "label": "Review each question", "description": "Answer questions individually to customize the plan" }
  ]
}
```
**CRITICAL**: The first option MUST have the `✅` emoji at the START of the label for **GREEN text** styling.
If user selects "✅ Accept All Recommended": Skip remaining questions, auto-select all recommended options, proceed to Plan Agent.

**Prompt Template**:
```
You are a Survey Agent creating clarification questions. Use the research synthesis to generate targeted questions that will unblock planning.

User Request: {user_prompt}

Research Synthesis:
{research_synthesis}

Generate 5-10 multiple-choice questions covering:
- Primary goal and success metrics
- Target user/audience
- Output format and structure
- Scope boundaries (what's in/out)
- Technical constraints
- Timeline expectations
- Quality bar

Rules:
- Each question must have 2-4 options (AskUserQuestion limit)
- Mark the RECOMMENDED option with `✅` emoji at START of label for **GREEN text**
- Put recommended option FIRST in the options array
- "Other" is automatically provided by the tool
- Include brief descriptions explaining each option
- Avoid open-ended essay questions
- Prioritize questions that unblock planning decisions
- End with a confirmation question

Output as structured JSON for AskUserQuestion:
{
  "questions": [
    {
      "question": "What is the primary goal?",
      "header": "Goal",
      "multiSelect": false,
      "options": [
        { "label": "✅ Build new feature", "description": "Best match based on detected intent" },
        { "label": "Fix existing issue", "description": "Debug and resolve problems" },
        { "label": "Improve/optimize", "description": "Enhance without changing behavior" }
      ]
    }
  ]
}
```

**Example Interactive Survey Flow**:
```
┌──────────────────────────────────────────────────────────────────────────┐
│  Quick Start                                                              │
│  Research complete! Would you like to accept all recommended defaults?    │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────┐         │
│  │ ✅ Accept All Recommended           ← GREEN TEXT            │         │
│  │   Skip survey, proceed with intelligent defaults            │         │
│  └─────────────────────────────────────────────────────────────┘         │
│  ┌─────────────────────────────────────────────────────────────┐         │
│  │ Review each question                                        │         │
│  │   Answer questions individually to customize the plan       │         │
│  └─────────────────────────────────────────────────────────────┘         │
└──────────────────────────────────────────────────────────────────────────┘

(If user selects "Review each question", show individual questions:)

┌────────────────────────────────────────────────────────┐
│  Goal                                                   │
│  What is the primary goal of this project?             │
│                                                         │
│  ┌─────────────────────────────────────────┐           │
│  │ ✅ Build new feature   ← GREEN TEXT    │           │
│  │   Create new functionality from scratch │           │
│  └─────────────────────────────────────────┘           │
│  ┌─────────────────────────────────────────┐           │
│  │ Fix existing issue                      │           │
│  │ Debug and resolve problems              │           │
│  └─────────────────────────────────────────┘           │
│  ┌─────────────────────────────────────────┐           │
│  │ Other                                   │           │
│  │ Provide custom input                    │           │
│  └─────────────────────────────────────────┘           │
└────────────────────────────────────────────────────────┘
```

**IMPORTANT**: The `✅` emoji at the START of the recommended option label renders as **GREEN text** in Claude Code terminal.

### Plan Agent

**Objective**: Create production-grade implementation roadmap

**Prompt Template**:
```
You are a Plan Agent creating an actionable roadmap. The survey has not been answered yet, so create a PROVISIONAL plan with branches for likely outcomes.

User Request: {user_prompt}

Research Synthesis:
{research_synthesis}

Survey Questions:
{survey_questions}

Create a production-grade roadmap with:

1. **Project Overview**: Brief summary of what will be built

2. **Milestones and Phases**: High-level breakdown
   - Phase 1: [Name] - [Description]
   - Phase 2: [Name] - [Description]
   - etc.

3. **Detailed Task Breakdown**: Per phase
   - Task 1.1: [Description] - Size: [small/medium/large]
   - Task 1.2: [Description] - Size: [small/medium/large]
   - etc.

4. **File and Folder Structure**: Proposed layout

5. **Interfaces and Contracts**: Key APIs and data flows

6. **Data Structures**: Core types and schemas

7. **Failure Modes and Recovery**: What could fail and how to handle it

8. **Test Plan**: Testing strategy and key test cases

9. **Definition of Done**: Acceptance criteria

10. **Provisional Branches**: Note where plan might change based on survey answers

Mark this as PROVISIONAL - final plan will be generated after survey responses.
```

## Fallback Behavior

### If Research Agent Fails
- Generate survey using heuristics based on detected keywords
- Questions will be more generic but still useful
- **MUST STILL call `AskUserQuestion` tool** - never fall back to text input

### If Survey Agent Fails
- **CALL `AskUserQuestion` tool** with fallback survey:
  - **Batch 1**: Goal, User, Output, Constraint (4 questions)
  - **Batch 2**: Confirmation question
- Each question includes "" option based on keyword analysis
- Users MUST get clickable options via `AskUserQuestion` tool - **NEVER text input**

⚠️ **Even on failure, ALWAYS use `AskUserQuestion` tool - never ask users to type "1C 2D..."**

### If Plan Agent Fails
- Return skeleton plan structure
- Request survey answers to continue

### Fallback Survey Questions
| Question | Header | Options |
|----------|--------|---------|
| Accept all? | Quick Start | ✅ Accept All Recommended, Review each question |
| Primary goal? | Goal | ✅ Build, Fix, Improve, Refactor |
| Target user? | User | ✅ End users, Developers, Internal, System |
| Deliverable? | Output | ✅ Working code, Docs, Analysis, Prototype |
| Constraint? | Constraint | ✅ Time, Complexity, Dependencies, Resources |
| Correct? | Confirm | ✅ Yes, Mostly, No |

**Note**: All recommended options MUST have `✅` at the START of the label for **GREEN text** styling.

## Usage Examples

### Basic Usage
```
/inference-planz:run Build a user authentication system with OAuth2
```

### Complex Request
```
/inference-planz:run I need to refactor our monolithic API into microservices while maintaining backwards compatibility and adding new features for mobile clients
```

### Empty Prompt
```
/inference-planz:run
```
(Shows domain/goal selection survey)

## Integration Points

- **inference-confidenz**: Adds confidence scoring to agent outputs
- **inference-continuez**: Can auto-proceed on high-confidence steps
- **Ralph Loop**: Compatible for iterative refinement cycles

## Safety Features

- Timeouts prevent runaway processing
- Fallbacks ensure useful output even on failures
- Debug mode for troubleshooting (redacted sensitive data)
- All decisions logged for audit
