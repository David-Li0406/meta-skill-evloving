---
name: feature-workflow
description: Structured workflow for implementing new features with planning, clarification, and documentation. Use when implementing new features, making significant changes, or when the user requests a feature that requires planning and multiple implementation steps. Triggers on feature requests, multi-step implementations, or when explicit planning is beneficial.
---

# Feature Workflow

Follow this workflow for new features or significant changes.

## Steps

1. **Research**: Understand the codebase, requirements, and constraints
   - Check existing patterns and implementations for similar functionality
   - Review related tests to understand expected behavior
   - Identify dependencies and potential side effects

2. **Plan**: Create initial plan with clear, actionable steps
   - Create a markdown feature file in `docs/features/` named `YYYY-MM-DD-HHMM_FEATURE_NAME.md`
   - Use `date +%Y-%m-%d-%H%M` for timestamp (e.g., `docs/features/2025-11-26-1530_AUTHENTICATION.md`)

3. **Present Summary**: Present brief plan to user
   - Use `question_tool`: "Go to clarifying"
   - If user adds context/feedback: immediately update feature file
   - Continue showing prompt until user confirms
   - Only proceed to Clarify after confirmation

4. **Clarify**: Ask questions to ensure complete understanding (REQUIRED if ANY ambiguity exists)
   - Ask ALL questions at once in a single `question_tool` call with multiple questions
   - Use `question_tool` when options can be predefined; plain text otherwise
   - If answers reveal new ambiguities: ask follow-up questions (again, all at once)
   - When to ask: architecture, file structure, user-facing changes, breaking changes, major patterns
   - When NOT to ask: minor implementation details
   - NEVER skip if uncertain - defaulting to assumption is unacceptable
   - After ALL clarifying questions resolved: update feature file with decisions, then go to **Confirm**

5. **Confirm**: Present final plan summary
   - Use `question_tool`: "Implement this plan"
   - If user confirms with no changes: proceed to implementation
   - If user provides changes/details: update feature file and ask "Implement this plan" again
   - Any plan modification requires re-confirmation before implementation

6. **Implement**: Execute plan incrementally
   - Follow code style and architecture guidelines
   - Write tests alongside implementation
   - Make incremental commits for major milestones if working on large features

7. **Validate**: Run all quality gates in order
   - If any gate fails: fix issues and re-run all gates from the beginning

8. **Update Feature File**: Sync feature file with any discussions, decisions, or changes not yet documented

9. **Complete**: After all quality gates pass
   - Summarize changes made
   - Ask about committing (see Version Control in AGENTS.md)
