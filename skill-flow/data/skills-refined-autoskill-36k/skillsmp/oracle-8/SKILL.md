---
name: oracle
description: Ask the oracle (GPT-5.2 with deep reasoning) strategic technical questions. Use for architecture decisions, complex debugging, security analysis, or when you need a second expert opinion. Supports background execution for long-running queries.
allowed-tools: Bash, TaskOutput, KillShell
---

# Oracle - Strategic Technical Advisor

The oracle is a GPT-5.2 reasoning model configured for deep technical analysis. Use it when you need expert-level guidance on complex decisions.

## Capabilities & Restrictions

**Can do:**
- Read files and explore the codebase
- Run shell commands for investigation
- Search the web for current information
- Provide strategic technical advice

**Cannot do (by design):**
- Edit or write files (read-only sandbox)
- Make changes to the codebase
- Execute destructive commands

This makes oracle safe to consult without risk of unintended modifications.

## When to Use Oracle

- **Architecture decisions**: System design, technology choices, scaling strategies
- **Complex debugging**: Multi-system issues, race conditions, performance bottlenecks
- **Security analysis**: Threat modeling, vulnerability assessment, auth patterns
- **Trade-off analysis**: When multiple valid approaches exist and you need to weigh them
- **Code review**: Getting a second opinion on significant implementations
- **Post-implementation review**: Validating decisions after the fact

## How to Invoke

**Script location**: `${CLAUDE_PLUGIN_ROOT}/skills/oracle/scripts/oracle.ts`

### Foreground (quick questions, <30 seconds expected)

Use Bash tool directly:
```bash
bun ${CLAUDE_PLUGIN_ROOT}/skills/oracle/scripts/oracle.ts "What's the best way to implement rate limiting for this API?"
```

### Background (complex questions, longer reasoning)

For questions that require deep reasoning, run in background and poll:

1. **Start the query** with `run_in_background=true`:
   ```bash
   bun ${CLAUDE_PLUGIN_ROOT}/skills/oracle/scripts/oracle.ts "Analyze the security implications of this authentication flow and suggest improvements"
   ```

2. **Continue working** on other tasks while oracle thinks

3. **Poll for status** using TaskOutput with `block=false`:
   - Check periodically if the oracle has finished
   - When status shows completed, retrieve the result

4. **Get result** - for long responses, use tail to avoid context flooding:
   ```bash
   # Get last 100 lines of output
   tail -100 /path/to/output
   ```

## Response Format

Oracle responses follow a tiered structure:

### Essential (Always Present)
- **Bottom Line**: 1-2 sentence direct answer
- **Action Plan**: Numbered concrete next steps
- **Effort Estimate**: Quick (<1h) | Short (1-4h) | Medium (1-2d) | Large (3d+)

### Expanded (When Relevant)
- **Reasoning**: Why this approach over alternatives
- **Trade-offs**: What you gain vs sacrifice
- **Dependencies**: Prerequisites and external factors

### Edge Cases (When Applicable)
- **Escalation Triggers**: When to reconsider
- **Alternatives**: Backup options
- **Gotchas**: Common mistakes to avoid

## Example Questions

Good oracle questions are:
- Specific and contextualized
- About decisions rather than implementations
- Complex enough to benefit from deep reasoning

Examples:
- "Given our PostgreSQL + Redis stack, should we add Elasticsearch for full-text search or use pg_trgm? We have 10M records, 100 QPS expected."
- "This codebase uses a custom event system. Should we migrate to a standard library or continue extending it?"
- "Review this authentication flow for security issues: [paste code]"
