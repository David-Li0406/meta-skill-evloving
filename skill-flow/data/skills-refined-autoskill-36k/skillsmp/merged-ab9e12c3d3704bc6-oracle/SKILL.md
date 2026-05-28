---
name: oracle
description: Use this skill when the user asks to 'ask the oracle', 'get a second opinion', 'consult oracle', 'deep analysis', or when facing difficult bugs, reviewing critical code, designing complex refactors, or needing architectural analysis.
---

# Oracle - Second Opinion Model

Invokes OpenAI's GPT-5.2 reasoning model via Codex for complex analysis tasks. It excels at debugging, code review, architecture analysis, and finding better solutions.

**Prerequisite:** Codex CLI installed and authenticated (`codex login`).

**Trade-offs:** Slower and more expensive than the main agent, but significantly better at complex reasoning. Use deliberately, not for every task.

## Invocation

Use `codex exec --profile oracle` to run the reasoning model:

```bash
codex exec --profile oracle "<task with optional @file references>"
```

### Example Prompts

```bash
# Security review
codex exec --profile oracle "Review @src/auth/jwt.ts for security vulnerabilities. Provide specific fixes."

# Debugging
codex exec --profile oracle "Analyze @src/components/DataFetcher.tsx to find why the memory leak occurs. The component fetches data but doesn't clean up properly on unmount."

# Architecture analysis
codex exec --profile oracle "Analyze how @src/services/payment.ts and @src/services/order.ts interact. Propose a refactoring plan that maintains backward compatibility."

# Complex bug investigation
codex exec --profile oracle "Bug: Users intermittently see stale data after updates. Related files: @src/api/update.ts @src/cache/invalidation.ts @src/hooks/useData.ts. Identify race conditions or cache invalidation issues and provide a fix."
```

## Workflow

1. **Gather context first**: Identify relevant files and the specific problem.
2. **Formulate a focused prompt**: Include file references with `@`.
3. **Invoke the oracle**: Run `codex exec --profile oracle "prompt"`.
4. **Act on the analysis**: Implement recommendations from the oracle's response.

## Best Practices

- **Use `@` syntax for files**: Include relevant files directly in the prompt.
- **Provide full context**: Include error messages, reproduction steps, and constraints.
- **Ask specific questions**: Request actionable output, such as "Provide specific fixes" instead of vague queries.
- **Chain with main agent**: Use oracle for analysis, main agent for implementation.

## Continuing Conversations

Use `codex exec resume SESSION_ID` to continue until satisfied. The session ID is returned from the initial invocation.

```bash
# Initial analysis (returns session ID)
codex exec --profile oracle "Review @src/auth/jwt.ts for security vulnerabilities"
# Output includes: Session ID: abc123...

# Continue with follow-up questions using the session ID
codex exec resume abc123 "Also check for timing attacks in the token validation"
```

| Argument | Description |
| -------- | ----------- |
| `SESSION_ID` | Session ID returned from the initial invocation |
| `PROMPT` | Follow-up instruction to send after resuming |

## Rules

- Use the oracle for complex problems that require deep reasoning.
- Keep prompts focused - one problem per invocation.
- Include file references with `@` syntax for relevant code.
- Request specific, actionable output.
- Oracle is read-only; use the main agent to implement changes.