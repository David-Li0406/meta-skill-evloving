---
name: prompt-driven-development
description: Transform rough ideas into detailed design documents with implementation plans. Use when a user wants to develop an idea into a complete specification, create a design document from a concept, plan a feature implementation, or mentions "PDD", "prompt-driven development", "idea to design", "design doc from idea", or wants to systematically refine requirements before building. Guides through requirements clarification, research, detailed design, and implementation planning.
---

# Prompt-Driven Development

Transform rough ideas into detailed designs with implementation plans through systematic requirements clarification, research, and iterative refinement.

## Parameters

- **rough_idea** (required): The initial concept to develop. Accept via:
  - Direct text input
  - File path to a local file
  - URL to a resource
- **project_dir** (optional, default: `.sop/planning`): Base directory for all project files

**Constraints:**
- Ask for all required parameters upfront in a single prompt
- Confirm successful acquisition before proceeding
- Never overwrite an existing project directory - ask for a new path if it exists

## Workflow

### Step 1: Create Project Structure

Create the directory structure:
```
{project_dir}/
├── rough-idea.md          # Original concept
├── idea-honing.md         # Requirements Q&A
├── research/              # Research findings
├── design/                # Design documents
│   └── detailed-design.md
├── implementation/        # Implementation plans
│   └── plan.md
└── summary.md             # Final summary
```

Prompt user to add files to context: `/context add {project_dir}/**/*.md`

### Step 2: Initial Process Planning

Ask user preference:
- Start with requirements clarification (default)
- Start with preliminary research
- Provide additional context first

Explain the process is iterative - they can move between steps as needed. Wait for explicit direction before proceeding.

### Step 3: Requirements Clarification

**Critical constraints:**
- Ask ONE question at a time, wait for response
- Never pre-populate answers or list multiple questions
- Follow this exact process per question:
  1. Formulate question
  2. Append to `idea-honing.md`
  3. Present to user
  4. Wait for complete response (may require dialogue)
  5. Record answer to `idea-honing.md`
  6. Formulate next question

Cover: edge cases, user experience, technical constraints, success criteria. Offer research when questions arise that need investigation.

See [references/templates.md](references/templates.md) for idea-honing format.

### Step 4: Research

1. Identify areas needing research
2. Propose research plan to user, ask for:
   - Additional topics
   - Specific resources to check
   - Areas where user has expertise
3. Document findings in `{project_dir}/research/` (one file per topic)
4. Include mermaid diagrams for architectures and data flows
5. Link to sources and references
6. Check in periodically with user on findings
7. Offer to return to requirements if new questions emerge

### Step 5: Iteration Checkpoint

Summarize current state and ask user:
- Proceed to detailed design?
- Return to requirements clarification?
- Conduct additional research?

Support iterating as many times as needed. Never proceed to design without explicit confirmation.

### Step 6: Create Detailed Design

Create `{project_dir}/design/detailed-design.md` with sections:
- Overview
- Detailed Requirements (consolidated from idea-honing)
- Architecture Overview (with mermaid diagrams)
- Components and Interfaces
- Data Models
- Error Handling
- Testing Strategy
- Appendices (Technology Choices, Research Findings, Alternatives)

See [references/templates.md](references/templates.md) for detailed design template.

Review with user and iterate. Offer to return to earlier steps if gaps emerge.

### Step 7: Develop Implementation Plan

Create `{project_dir}/implementation/plan.md`:
- Checklist at top for tracking progress
- Numbered steps, each with:
  - Clear objective
  - Implementation guidance
  - Test requirements
  - Integration with previous work
  - **Demo** - explicit description of demoable functionality

**Key principle:** Each step must result in working, demoable functionality. Prioritize test-driven development and early core functionality.

See [references/templates.md](references/templates.md) for implementation plan template.

### Step 8: Summarize Results

Create `{project_dir}/summary.md`:
- List all artifacts created
- Overview of design and implementation plan
- Suggested next steps
- Areas needing refinement

Present summary to user.

## Troubleshooting

**Requirements stall:** Suggest moving to different aspect, provide examples, summarize progress, or conduct research.

**Research limitations:** Document gaps, suggest alternatives, ask user for context, continue with available info.

**Design complexity:** Break into smaller components, focus on core first, suggest phased approach.
