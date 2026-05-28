---
name: plan-module
description: Creates a comprehensive multi-step implementation plan for a new module. Asks discovery questions first, then generates numbered markdown files in docs/ with detailed requirements. Use when asked to "plan a module", "create implementation plan", or "plan a feature".
---

# Plan Module Skill

Creates comprehensive, step-by-step implementation plans for new modules through structured discovery questions and detailed documentation.

## Trigger Phrases

Use this skill when the user says:
- "Plan a module for [name]"
- "Create an implementation plan for [name]"
- "Design a new [name] module"
- "I want to develop a [name] module, ask me questions first"
- "Help me plan the [name] feature comprehensively"

## Process Overview

### Phase 1: Discovery Questions

Ask comprehensive questions organized by category to understand requirements fully.

**Question Categories:**

1. **Core Entities**
   - What main entities/tables does this module need?
   - What are the relationships between entities?

2. **Entity Attributes**
   - For each entity, what fields/columns are required?
   - What are the data types and constraints?

3. **Business Rules**
   - What are the business rules and validations?
   - What calculations or automations are needed?

4. **User Workflows**
   - Who are the users (roles)?
   - What actions can each role perform?

5. **Integrations**
   - Does this integrate with existing modules?
   - Are there external APIs involved?

6. **UI/UX Requirements**
   - What pages/views are needed?
   - What should appear on dashboards?

7. **Reports**
   - What reports are required?
   - Should reports be exportable?

8. **Student Portal**
   - Does this need student-facing views?
   - What can students see/do?

**Question Format:**
Use terminal echo commands for questions:
```
pnpm exec echo "CATEGORY NAME

1. Question one?
2. Question two?
...

Answer: "
```

Wait for user to edit the command with answers before continuing.

### Phase 2: Follow-up Questions

Based on initial answers, ask clarifying follow-up questions to fill gaps.

### Phase 3: Plan Overview

Before writing files, present a high-level overview of the planned steps:
- List each step number and title
- Brief description of what each step covers
- Ask for approval before proceeding

### Phase 4: Generate Plan Documents

Create numbered markdown files in `docs/[module-name]/`:

```
docs/[module-name]/
├── 000_index.md           # Overview and summary
├── 001_[first-step].md    # First implementation step
├── 002_[second-step].md   # Second implementation step
└── ...
```

## Document Structure

### Index File (000_index.md)

```markdown
# [Module Name] - Implementation Plan

## Overview
Brief description of the module purpose.

## Features Summary
Table of features with Admin vs User capabilities.

## Implementation Steps
Table linking to each step with description.

## Database Entities
ASCII diagram of entity relationships.

## Directory Structure (Final)
Expected file structure after completion.

## Business Rules
Key business rules table.

## Access Control
Role-based access table.

## Execution Order
Dependencies and recommended order.

## Validation Command
Standard validation commands.
```

### Step Files (001_xxx.md, 002_xxx.md, etc.)

```markdown
# Step NNN: [Step Title]

## Introduction
- Context about this step
- What previous steps completed
- What this step accomplishes

## Context
Background information needed to understand this step.

## Requirements

### 1. [Subsection]
Detailed requirements with tables for:
- Schema definitions (columns, types, constraints)
- API/Actions signatures
- UI component specifications

### 2. [Subsection]
Continue with organized requirements.

## Expected Files
Table of files to create with purposes.

## Validation Criteria
Numbered list of what should work after this step.

## Notes
Additional implementation guidance.
```

## Step Organization Guidelines

### Recommended Step Categories

1. **Database Schema Steps** (usually first)
   - Group related tables together
   - Include enums, relations, indexes

2. **Core Feature CRUD Steps**
   - Repository, Service, Actions
   - Forms and pages
   - One step per major entity group

3. **Advanced Feature Steps**
   - Complex business logic
   - Integrations with other modules

4. **Reports Step**
   - All reporting functionality
   - Export capabilities

5. **Portal Integration Step** (usually last)
   - Student/user-facing views
   - Read-only interfaces

### Step Size Guidelines

- Each step should be completable in one coding session
- Group related functionality (e.g., Books + Authors + Categories together)
- Database schema can be split if complex (3+ steps for large schemas)
- Keep context manageable for Claude Opus 4.5 token limits

## Content Guidelines

### Do Include
- Detailed table schemas with all columns
- Action signatures with parameters
- UI component field specifications
- Business logic pseudocode
- Integration points with existing code
- Validation criteria checklist

### Do NOT Include
- Actual code implementations
- Copy-paste ready code blocks
- Line-by-line instructions
- Specific import statements

### Formatting Standards
- Use tables for structured data (schemas, actions, files)
- Use bullet points for lists
- Use code blocks only for file paths and directory structures
- Include ASCII diagrams for entity relationships

## Final Steps

After generating all files:

1. List all created files
2. Explain how to use the plan
3. Run completion command:
   ```
   pnpm exec echo 'Done'
   ```

## Example Invocation

User: "Plan a module for inventory management, ask me questions first"

Response:
1. Ask discovery questions via terminal
2. Wait for answers
3. Ask follow-up questions
4. Present high-level plan overview
5. Get approval
6. Generate numbered .md files in docs/inventory/
7. Create index file
8. Signal completion
