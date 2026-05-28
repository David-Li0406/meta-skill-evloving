# Token Reduction Strategies

Detailed techniques for minimizing token usage while maintaining code quality and Claude's effectiveness.

## Understanding Token Consumption

### What Are Tokens?

Tokens are chunks of text (roughly 4 characters or 0.75 words). Every interaction has:

- **Input tokens**: Your prompts + file contents + context
- **Output tokens**: Claude's responses + generated code
- **System tokens**: Instructions, loaded skills, conversation history

### Token Estimation

| Content | Approximate Tokens |
|---------|-------------------|
| 1 English word | ~1.3 tokens |
| 1 line of code | 10-20 tokens |
| 100 lines of code | 1,000-2,000 tokens |
| Typical source file | 500-3,000 tokens |
| Large file (1000+ lines) | 5,000-15,000 tokens |
| npm install output | 500-2,000 tokens |
| Test run output | 1,000-5,000 tokens |

### High-Cost Operations

| Operation | Token Impact | Frequency Risk |
|-----------|--------------|----------------|
| Reading large files | Very High | Common |
| Glob entire directories | High | Common |
| Verbose tool outputs | High | Medium |
| Long conversations | Cumulative | Always |
| Repeated file reads | High | Very Common |

## Context Management

### The Context Budget

Think of context as a budget:

```
Total context: 200,000 tokens

Allocated:
- System prompt: ~5,000 tokens (fixed)
- Loaded skills: ~2,000 tokens (variable)
- Conversation history: ~80,000 tokens (growing)
- Response buffer: ~40,000 tokens (reserved)
- Available for work: ~73,000 tokens
```

### Context Growth Pattern

| Turn | Cumulative Context | Notes |
|------|-------------------|-------|
| 1 | 5,000 | System + first exchange |
| 5 | 15,000 | Light conversation |
| 10 | 35,000 | Some file reads |
| 15 | 60,000 | Normal development |
| 20 | 85,000 | Consider /compact |
| 25 | 120,000 | Compact now |
| 30+ | 150,000+ | Performance degradation |

### Preventing Context Bloat

1. **Plan file reads**: Know what you need before reading
2. **Use targeted searches**: Grep before glob
3. **Request summaries**: Not full outputs
4. **Compact regularly**: Don't wait for warnings
5. **Clear when done**: Start fresh for new tasks

## File Reading Optimization

### The File Reading Tax

Every file read adds to context. A typical React component:

```typescript
// UserCard.tsx - ~50 lines
// Estimated: 300-500 tokens
```

Reading 10 such files: 3,000-5,000 tokens

Reading an entire src/ folder: potentially 50,000+ tokens

### Read Selectively

**Pattern 1: Specific files only**
```
> @src/api/users.ts @src/types/user.ts
> Add pagination to getUserAll
```

**Pattern 2: Line ranges**
```
> @src/api/users.ts:45-80
> This function needs error handling
```

**Pattern 3: Function extraction**
```
> Show me only the getUserById function from @src/api/users.ts
```

### Grep Before Read

**Wasteful:**
```
> Find where AuthService is used and show me the code
[Claude reads 20 files to find 5 usages]
```

**Efficient:**
```
> grep "AuthService" in src/
[Gets file list: 5 files]

> @src/auth.ts @src/middleware/auth.ts
> Show me how AuthService is instantiated
```

### Avoid Directory Globs

| Request | Token Impact | Better Alternative |
|---------|--------------|-------------------|
| `@src/` | Very High | Specific files |
| `@components/` | High | `@components/UserCard.tsx` |
| `@**/*.ts` | Extreme | Grep + specific reads |

## Prompt Optimization

### Concise Prompting

**Verbose (wasteful):**
```
> I was wondering if you could perhaps take a look at the authentication
> system and maybe help me understand why users are sometimes getting
> logged out unexpectedly. I think it might be related to token expiration
> but I'm not entirely sure. Could you investigate and let me know what
> you find?
```
(~80 tokens)

**Concise (efficient):**
```
> Debug unexpected logouts in @src/auth/.
> Suspect: token expiration. Check refresh logic.
```
(~20 tokens)

### Eliminate Fluff

| Wasteful | Efficient |
|----------|-----------|
| "Could you please" | (just ask) |
| "I was wondering if" | (just ask) |
| "I want you to" | (just state task) |
| "As you can see" | (assume context) |
| "Let me explain" | (just explain) |

### Use Structured Formats

**Paragraph form (more tokens):**
```
> I need to add a new feature where users can upload profile pictures.
> The pictures should be validated to make sure they're not too large,
> probably under 5MB. They should be stored in S3 and the user record
> should be updated with the URL. Also add a delete endpoint.
```

**Structured (fewer tokens):**
```
> Add profile picture upload:
> - Max size: 5MB
> - Storage: S3
> - Update user record with URL
> - Add delete endpoint
```

### Reuse @ Mentions

Don't re-explain context:

**Turn 1:**
```
> @src/api/users.ts - Add pagination
```

**Turn 2:**
```
> Now add sorting to the same endpoint
```
(Not: "Now add sorting to the users endpoint in src/api/users.ts")

## Tool Output Management

### Limit Verbose Outputs

**Wasteful:**
```
> Run npm install and show me the output
[Entire npm install log: 1000+ tokens]
```

**Efficient:**
```
> Run npm install, just confirm success or show errors
```

### Request Summaries

```
> Run the tests and give me a summary:
> - Total tests
> - Passed/failed count
> - First 3 failure messages if any
```

### Suppress Known Good Output

```
> Run build. If successful, just say "build passed".
> Only show output on failure.
```

## Conversation Management

### When to /compact

| Signal | Action |
|--------|--------|
| Context > 70% | Compact soon |
| Responses slowing | Compact now |
| Claude forgetting earlier info | Compact |
| Starting new sub-task | Good time to compact |
| After completing milestone | Compact and continue |

### Compact Effectively

**Before compacting, state key context:**
```
> Current state:
> - Working on user auth feature
> - Completed: login endpoint, JWT middleware
> - Next: password reset flow
> - Key file: @src/auth/
>
> /compact
```

This ensures important info survives compression.

### Use /clear Aggressively

When switching tasks, don't preserve irrelevant context:

```
> /clear

Starting: Payment integration
Key files: @src/payments/ @src/types/payment.ts
```

## Batching Techniques

### Batch Similar Operations

**Sequential (expensive):**
```
Turn 1: > Add validation to createUser
Turn 2: > Add validation to updateUser
Turn 3: > Add validation to deleteUser
```
(3 full exchanges, context growing each time)

**Batched (efficient):**
```
> Add input validation to all user endpoints in @src/api/users.ts:
> - createUser: email format, password strength
> - updateUser: partial update support
> - deleteUser: confirm user exists
```
(1 exchange, same result)

### Batch Read-Modify

```
> In @src/api/:
> 1. Add error handling to users.ts
> 2. Add error handling to products.ts
> 3. Add error handling to orders.ts
> Use consistent try-catch with logging
```

### Know When Not to Batch

Don't batch when:
- Changes are complex and interdependent
- You need to verify each step
- Debugging (need to isolate)
- Learning new code (need explanations)

## Subagent Delegation

### Why Subagents Save Tokens

Subagents have separate context:
- Their exploration doesn't bloat your context
- They return summaries, not full explorations
- Can use cheaper models (Haiku)

### Delegation Patterns

**Exploration delegation:**
```
> Use a subagent (Haiku) to find all files that import the Logger class.
> Return: file list with line numbers
```

**Analysis delegation:**
```
> Use a subagent to analyze the database schema in @db/schema.ts.
> Return: table names, key relationships, potential issues
```

### Return Summaries, Not Details

Configure agents to summarize:

```yaml
---
name: explorer
model: haiku
---
You explore and analyze code. Always return:
- Concise summary (max 200 words)
- Key findings as bullet points
- File paths for follow-up

Never return full file contents.
```

## Quick Reference

### Token-Saving Actions

| Action | Savings | Effort |
|--------|---------|--------|
| Grep before read | 50-90% | Low |
| Specific @ mentions | 30-70% | Low |
| Concise prompts | 20-40% | Low |
| Batch operations | 30-50% | Medium |
| Regular /compact | 50-80% | Low |
| Subagent delegation | 40-60% | Medium |

### Token-Wasting Actions

| Action | Extra Cost | Why |
|--------|------------|-----|
| Directory globs | Very High | Reads everything |
| Verbose prompts | 20-50% | Unnecessary words |
| Repeated context | 30-50% | Already in history |
| Full tool outputs | 50-200% | Too much detail |
| No /compact | Cumulative | Context grows forever |

## Checklist

Before any significant task:

- [ ] Identified specific files needed
- [ ] Used grep to narrow scope
- [ ] Written concise prompt
- [ ] Checked current context usage (/cost)
- [ ] Considered if batching applies
- [ ] Planned /compact point
