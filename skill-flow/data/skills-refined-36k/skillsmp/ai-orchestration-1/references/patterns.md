# AI Orchestration Patterns

## Quick Consensus

```python
# Spawn all 3 for same question
review = ai_review(prompt="Should we use WebSockets or SSE for real-time updates?")

# Fetch and compare
results = {
    "claude": ai_fetch(review.jobs["claude"].job_id, timeout=120),
    "codex": ai_fetch(review.jobs["codex"].job_id, timeout=120),
    "gemini": ai_fetch(review.jobs["gemini"].job_id, timeout=120),
}

# Synthesize: look for agreement, note disagreements
```

## Specialized Perspectives

```python
# Different prompts for different strengths
claude_job = ai_spawn(
    cli="claude",
    prompt="Analyze the architecture implications of using Redis for caching..."
)
codex_job = ai_spawn(
    cli="codex",
    prompt="Review the Redis integration code for bugs and anti-patterns...",
    files=["src/cache/"]
)
gemini_job = ai_spawn(
    cli="gemini",
    prompt="Research Redis caching best practices and common pitfalls..."
)
```

## Security Audit

```python
security_prompt = """
Review src/auth/ for security vulnerabilities.
Focus on: injection, auth bypass, data exposure.
Output: List findings with severity and file:line references.
"""

claude_job = ai_spawn(cli="claude", prompt=security_prompt, files=["src/auth/"])
codex_job = ai_spawn(cli="codex", prompt=security_prompt, files=["src/auth/"])

# Aggregate findings from both
```

## Sequential (When Prompts Depend on Results)

```python
# First, get architecture analysis
arch = ai_call(cli="claude", prompt="Design the auth architecture...")

# Then, use that to get implementation details
impl = ai_call(cli="codex", prompt=f"Given this architecture:\n{arch.content}\n\nList implementation steps...")
```

## Writing Good Prompts

Include:
1. **Clear task description** - what exactly to do
2. **Expected output format** - how to structure the response
3. **Scope boundaries** - what files/areas to focus on
4. **Read-only reminder** (for codex/gemini) - they cannot modify anything

### Good Example

```text
Review the authentication module for security vulnerabilities.

Focus on: src/auth/*.py
Output: List of findings with severity (high/medium/low) and line numbers
Constraints: This is a read-only review - identify issues only
```

### Bad Example

```text
Look at the code and tell me what you think
```
