---
name: intent-start
description: Start a new intent with spec-driven development. Use when the user wants to begin working on a new feature, bug fix, or task and needs to document the problem, solution, and requirements.
user-invocable: true
---

# Intent Start

You are helping the user start a new intent using spec-driven development.

## Workflow

1. Ask the user: "What are you working on?" (brief description)
2. Based on their answer, suggest a folder name in format: `YYYY-MM-DD-{repository-name}-{intent-description}` (use today's date)
   - Get repository name from: `basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $(pwd)`
   - Format example: `2026-01-20-ai-code-skills-add-dark-mode`
3. Ask these questions to build the spec:
   - "What problem does this solve?"
   - "What's the proposed solution?"
   - "What are the key requirements?" (list 3-5 items)
   - "What are the acceptance criteria?" (how do we know it's done?)
   - "What's the implementation plan?" (break down into 3-7 concrete steps)

4. **Explore the codebase** to identify relevant code:
   - Search for files related to the feature/bug being worked on
   - Identify key entry points, functions, or components that will be modified
   - Find related tests or documentation
   - Note any dependencies or connected modules

5. Create the folder structure:
   ```
   ~/.claude-intents/in-progress/YYYY-MM-DD-{repository-name}-{intent-description}/
   ├── spec.md
   └── notes.md
   ```

6. Write **spec.md** with this structure:
   ```markdown
   # [Intent Title]

   **Date Started:** YYYY-MM-DD
   **Status:** In Progress

   ## Problem
   [Problem statement]

   ## Solution
   [Proposed solution]

   ## Requirements
   - [ ] Requirement 1
   - [ ] Requirement 2
   - [ ] Requirement 3

   ## Acceptance Criteria
   - [ ] Criteria 1
   - [ ] Criteria 2

   ## Implementation Plan
   1. [Step 1]
   2. [Step 2]
   3. [Step 3]
   4. [Step 4]
   5. [Step 5]

   ## Relevant Code

   ### Key Files
   | File | Purpose |
   |------|---------|
   | `path/to/file.ts:42` | Brief description of relevance |
   | `path/to/another.ts:15-30` | Brief description of relevance |

   ### Code Snippets
   <!-- Include key code snippets that are central to this intent -->

   **[filename.ts:line]** - Description
   ```typescript
   // Relevant code snippet
   ```

   ## Architecture (Optional)
   <!-- Include Mermaid diagrams when they help visualize: -->
   <!-- - Data flow between components -->
   <!-- - State transitions -->
   <!-- - Sequence of operations -->
   <!-- - System architecture changes -->

   ```mermaid
   flowchart TD
       A[Component A] --> B[Component B]
       B --> C[Component C]
   ```

   ## Notes
   [Any additional context]
   ```

7. Write **notes.md** with:
   ```markdown
   # Development Notes

   ## YYYY-MM-DD - Intent Started
   - Created spec
   - [Any initial notes from the conversation]
   ```

8. Create a todo list using TodoWrite tool:
   - Convert each step from the implementation plan into a todo item
   - Set all items to "pending" status
   - Use the imperative form for content (e.g., "Implement feature X")
   - Use the present continuous form for activeForm (e.g., "Implementing feature X")
   - This helps track progress throughout the intent lifecycle

9. Confirm intent creation and show the path

## Important Notes

- **Intents folder:** All intents are stored in `~/.claude-intents/`
- **Repository name:** Get from git using: `basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $(pwd)`
- If not in a git repo, use the current folder name as repository name
- Use today's date for folder name
- Keep folder name lowercase with hyphens
- Create `~/.claude-intents/in-progress/` directory if it doesn't exist
- Since intents are stored outside the repo (in `~/.claude-intents`), no gitignore changes are needed

## Code Context Guidelines

When documenting relevant code:

- **Use relative paths** from the repository root (e.g., `src/components/Button.tsx:42`)
- **Include line numbers** for specific functions or sections (e.g., `:42` or `:15-30` for ranges)
- **Keep snippets focused** - only include the most relevant 5-15 lines, not entire files
- **Prioritize entry points** - document where the change begins (handlers, API endpoints, etc.)

## Mermaid Chart Guidelines

Include Mermaid diagrams when they help visualize:

- **Flowcharts** - for complex logic or decision trees
- **Sequence diagrams** - for multi-component interactions or API flows
- **State diagrams** - for state machine changes
- **Entity relationships** - for data model changes

Skip diagrams for:

- Simple, linear implementations
- Single-file changes
- Bug fixes with obvious flow

Supported diagram types:

```text
flowchart TD    - Top-down flowchart
sequenceDiagram - Interaction between components
stateDiagram-v2 - State transitions
erDiagram       - Entity relationships
classDiagram    - Class structures
```
