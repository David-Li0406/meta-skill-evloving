# Context-Aware Detection and Tree Injection

## Automatic Hook Execution

Before this skill executes, the **UserPromptSubmit** hook automatically runs and checks the user's query for implementation keywords:

**Keywords**: `implement`, `create`, `add`, `refactor`, `build`, `generate`, `setup`, `initialize`

If ANY of these keywords are detected, the hook:

1. Generates a project structure tree using `get_context_tree.py`
2. Injects the tree into the conversation context with `[CONTEXT-AWARE MODE ACTIVATED]` marker
3. Provides guidance on using the project structure for transformation

## Checking for Context Injection

At the start of execution, check if the conversation context contains:

```text
[CONTEXT-AWARE MODE ACTIVATED]

Project Structure:
```
(project tree)
```

Use this project structure as context for the request: "..."
```

**If Found**: The PROJECT_TREE context is available. Pass this context when invoking the prompt-structurer skill.

**If Not Found**: Either:

- Query didn't contain implementation keywords (no tree needed)
- Hook failed to execute (graceful degradation)
- Project is empty (tree generation skipped)

## Using Context During Transformation

When PROJECT_TREE context is available, you MUST pass it to the transform skill:

```text
Skill tool with skill="pseudo-code-prompting:prompt-structurer"
args="[user query]

PROJECT_TREE:
[tree structure from context]
"
```

This ensures the transformation includes project-specific file paths and architecture-aware suggestions.

## Context-Aware Troubleshooting

**Context not appearing?**

1. Check if query contains implementation keywords
2. Verify hook is configured in `hooks/hooks.json`
3. Check if Python is installed (`python3 --version`)
4. Verify script exists: `hooks/tree/get_context_tree.py`

**Empty project tree?**

The hook gracefully skips tree injection for empty projects and returns `<<PROJECT_EMPTY_NO_STRUCTURE>>`.

## Implementation Requirements

### Context Window Optimization (MANDATORY)

To minimize token usage, you MUST remove intermediate outputs from the conversation flow:

**Keep Only**:

- Original user query (input)
- Final optimized output

**Remove/Don't Store**:

- Transform step output (intermediate)
- Validate step input (redundant with transform output)
- Validate step output (intermediate)
- Optimize step input (redundant with validate output)

**Implementation**: After each step completes, extract only the essential result and pass it to the next step WITHOUT including full tool outputs in subsequent messages.

## Token Savings

By removing intermediate outputs, you save approximately **60-80% of context window usage**.
