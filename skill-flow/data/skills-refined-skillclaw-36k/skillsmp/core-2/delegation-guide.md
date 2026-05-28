# Delegation & Task Decomposition Guide

**Purpose**: Practical guide for when to delegate work to agents, how to decompose tasks for parallel execution, and the mandatory spotcheck pattern.

**When to read**: Planning to use parallel agents, decomposing complex tasks, or setting up multi-agent workflows.

---

## Table of Contents
1. [When to Delegate](#when-to-delegate)
2. [Task Decomposition](#task-decomposition)
3. [Spotcheck Pattern](#spotcheck-pattern-mandatory)
4. [Launch Patterns](#launch-patterns)
5. [Best Practices](#best-practices)

---

## When to Delegate

### Good Candidates for Parallelization

✅ **Updating multiple files simultaneously**
- Example: Update 5 documentation files with new naming convention
- Pattern: 1 agent per file + 1 spotcheck agent

✅ **Researching multiple topics at once**
- Example: Research 3 different libraries for feature comparison
- Pattern: 1 agent per topic + 1 synthesis agent

✅ **Testing multiple approaches in parallel**
- Example: Try 3 different algorithms to solve problem
- Pattern: 1 agent per approach + 1 comparison agent

✅ **Processing lists/batches**
- Example: Analyze 10 code files for security issues
- Pattern: 1 agent per file (or per batch of 2-3) + 1 spotcheck

✅ **Independent subtasks**
- Example: Create components A, B, C for a feature
- Pattern: 1 agent per component + 1 integration agent

### Poor Candidates for Parallelization

❌ **Sequential dependencies**
- Example: "Build feature A, then use A to build B, then test B"
- Why: Each step depends on previous completion

❌ **Single-file edits**
- Example: "Update line 42 in config.ts"
- Why: No parallelization benefit, overhead not worth it

❌ **Tasks requiring human judgment**
- Example: "Decide which architecture to use"
- Why: Need single coherent decision, not multiple opinions

❌ **Quick one-liners**
- Example: "What's the syntax for async/await?"
- Why: Answer faster than launching agents

---

## Task Decomposition

### Pattern 1: File-Based Decomposition

**Scenario**: Update multiple files with same change

**Decomposition**:
```
Task: Add error logging to 5 API endpoints

Decompose into:
1. Agent 1: Add logging to /api/users.ts
2. Agent 2: Add logging to /api/posts.ts
3. Agent 3: Add logging to /api/comments.ts
4. Agent 4: Add logging to /api/auth.ts
5. Agent 5: Add logging to /api/settings.ts
6. Spotcheck Agent: Verify consistent logging pattern across all files
```

### Pattern 2: Feature-Based Decomposition

**Scenario**: Build multi-component feature

**Decomposition**:
```
Task: Add Settings page to application

Decompose into:
1. Agent 1: Create Settings page component
2. Agent 2: Add Settings route configuration
3. Agent 3: Create Settings API endpoints
4. Agent 4: Add Settings navigation menu item
5. Agent 5: Write Settings page tests
6. Integration Agent: Verify all pieces work together
```

### Pattern 3: Research-Based Decomposition

**Scenario**: Compare multiple options

**Decomposition**:
```
Task: Choose best state management library

Decompose into:
1. Agent 1: Research Zustand (features, pros/cons, examples)
2. Agent 2: Research Jotai (features, pros/cons, examples)
3. Agent 3: Research Redux Toolkit (features, pros/cons, examples)
4. Synthesis Agent: Compare findings, create decision matrix
```

### Pattern 4: Batch-Based Decomposition

**Scenario**: Process large list of items

**Decomposition**:
```
Task: Update 20 component files

Decompose into batches:
Batch 1 (files 1-5): 5 agents + spotcheck
Batch 2 (files 6-10): 5 agents + spotcheck
Batch 3 (files 11-15): 5 agents + spotcheck
Batch 4 (files 16-20): 5 agents + spotcheck
Final spotcheck: Verify consistency across all 20 files
```

---

## Spotcheck Pattern (MANDATORY)

### Why Spotcheck is Critical

- Parallel agents work independently
- No inter-agent communication
- Need verification of consistency
- Catch conflicting changes early

### When Spotcheck is Required

**After ANY parallel agent work** - no exceptions:
- Multi-file updates
- Batch processing
- Parallel research
- Independent subtasks

### What Spotcheck Reviews

**Completeness**:
- [ ] All parallel tasks completed?
- [ ] All files updated as expected?
- [ ] Nothing missed?

**Consistency**:
- [ ] Naming consistent across files?
- [ ] Patterns followed uniformly?
- [ ] No conflicting implementations?

**Quality**:
- [ ] Code style consistent?
- [ ] Tests passing?
- [ ] Documentation updated?

**Requirements**:
- [ ] Original requirements met?
- [ ] Success criteria achieved?
- [ ] Edge cases handled?

### Spotcheck Task Template

```
task({ 
  agent: "agent", 
  task: "SPOTCHECK: Review work from previous [N] agents.
  
  Verify:
  1. All tasks completed successfully
  2. Consistency across [files/components/features]
  3. No conflicting changes
  4. [Specific requirement 1]
  5. [Specific requirement 2]
  
  Report any issues found and recommend fixes."
});
```

---

## Launch Patterns

### Pattern 1: Standard Parallel Execution

**Use case**: Update multiple files with similar changes

```typescript
// SINGLE message with MULTIPLE Task tool calls
await Promise.all([
  task({ 
    agent: "agent", 
    task: "Update navigation.tsx: Add Settings route..." 
  }),
  task({ 
    agent: "agent", 
    task: "Update routes.ts: Register /settings..." 
  }),
  task({ 
    agent: "agent", 
    task: "Update types.ts: Add SettingsPage interface..." 
  }),
  task({ 
    agent: "agent", 
    task: "Update tests.ts: Add settings route test..." 
  }),
  task({ 
    agent: "agent", 
    task: "Update docs.md: Document settings feature..." 
  }),
]);

// Then MANDATORY spotcheck
task({ 
  agent: "agent", 
  task: "SPOTCHECK: Review all 5 updates for consistency..." 
});
```

### Pattern 2: Research & Synthesis

**Use case**: Compare multiple options before deciding

```typescript
// Research phase (parallel)
await Promise.all([
  task({ 
    agent: "agent", 
    task: "Research Library A: Features, pros/cons, examples..." 
  }),
  task({ 
    agent: "agent", 
    task: "Research Library B: Features, pros/cons, examples..." 
  }),
  task({ 
    agent: "agent", 
    task: "Research Library C: Features, pros/cons, examples..." 
  }),
]);

// Synthesis phase (single agent)
task({ 
  agent: "agent", 
  task: "SYNTHESIS: Compare findings, create decision matrix..." 
});
```

### Pattern 3: Batch Processing

**Use case**: Process large number of items

```typescript
// Batch 1 (files 1-5)
await Promise.all([...5 agent tasks...]);
task({ agent: "agent", task: "SPOTCHECK batch 1..." });

// Batch 2 (files 6-10)
await Promise.all([...5 agent tasks...]);
task({ agent: "agent", task: "SPOTCHECK batch 2..." });

// Continue for remaining batches...

// Final spotcheck
task({ 
  agent: "agent", 
  task: "FINAL SPOTCHECK: Verify all batches consistent..." 
});
```

---

## Scalability Guidelines

### Small Tasks (1-3 files)
- **Pattern**: 1 agent per file + spotcheck
- **Total**: 2-4 agents
- **Example**: Update 3 config files

### Medium Tasks (4-10 files)
- **Pattern**: 1 agent per file + spotcheck
- **Total**: 5-11 agents
- **Example**: Add new feature across multiple components

### Large Tasks (11-50 files)
- **Pattern**: Batch into groups of 5-10, spotcheck per batch + final spotcheck
- **Total**: N+2 to N+5 agents (depending on batching)
- **Example**: Global refactoring across codebase

### Very Large Tasks (50+ files)
- **Pattern**: Hierarchical delegation
  - Group into logical units
  - 1 agent per unit + unit spotcheck
  - 1 final synthesis + overall spotcheck
- **Total**: Varies by complexity
- **Example**: Migrate entire codebase to new framework

---

## Best Practices

### ✅ Do

**Launch Aggressively**:
- Use parallel agents liberally
- No artificial limits on agent count
- Better to have spotcheck catch duplicates than miss work

**Provide Full Context**:
- Every agent gets complete picture
- Include file paths, examples, success criteria
- Better too much context than too little

**Always Spotcheck**:
- After ANY parallel work
- No exceptions
- This catches 90% of consistency issues

**Escalate Appropriately**:
- Agents can invoke engineers for technical expertise
- See `agent-guide.md` for escalation patterns

**Document Outcomes**:
- Spotcheck reports issues found
- Clear handoffs between agents
- Track what was accomplished

### ❌ Don't

**Don't: Launch 1 agent for trivial task**
```typescript
// Bad
task({ agent: "agent", task: "Add semicolon to line 42" });

// Good: Just do it yourself
```

**Don't: Forget spotcheck after parallel work**
```typescript
// Bad
await Promise.all([...10 tasks...]);
// Done! (NO - you forgot spotcheck)

// Good
await Promise.all([...10 tasks...]);
task({ agent: "agent", task: "SPOTCHECK..." });
```

**Don't: Give vague instructions**
```typescript
// Bad
task({ agent: "agent", task: "Make it better" });

// Good
task({ 
  agent: "agent", 
  task: "Refactor authentication.ts: Extract token validation to separate function, add error handling for expired tokens, update tests..." 
});
```

**Don't: Skip context sharing**
```typescript
// Bad
task({ agent: "agent", task: "Update the config" });

// Good
task({ 
  agent: "agent", 
  task: "Update config.ts at /path/to/config.ts: Add DATABASE_URL environment variable to config object (line 23), follow existing pattern for API_KEY..." 
});
```

**Don't: Artificially limit parallel agents**
```typescript
// Bad
"I'll only use 3 agents because I don't want to overwhelm the system"

// Good
"I need to update 10 files, so I'll launch 10 agents + 1 spotcheck"
```

**There is NO artificial limit on parallel agents.** Launch as many as the task requires.

---

## Quick Reference

```bash
# DECISION TREE
Simple task → Do it yourself
Multi-file task → Parallel agents + spotcheck
Need expertise → Escalate to engineer (see agent-guide.md)

# PATTERN: N parallel tasks + 1 spotcheck
Agents: Launch as many as needed (no limit)
Context: FULL for each agent
Spotcheck: ALWAYS after parallel work

# DECOMPOSITION
Files: 1 agent per file
Features: 1 agent per component
Research: 1 agent per topic
Batches: Group into manageable chunks

# REMEMBER
- No artificial limits on parallel agents
- Full context for every agent
- Never skip spotcheck
- Escalate when appropriate (see agent-guide.md)
```

---

## Background Tasks

### When to Use Background Execution

Use `run_in_background: true` for:
- Long-running research while continuing other work
- Build/test processes that don't block coding
- Multiple independent investigations

### Pattern: Background Research

```typescript
// Launch research in background
const researchTask = task({
  subagent_type: "researcher",
  prompt: "Deep research on [topic]...",
  run_in_background: true  // Returns immediately with output_file
});

// Continue with other work...
// Read results when needed:
read(researchTask.output_file);
```

### Pattern: Parallel Background Tasks

```typescript
// Launch multiple background tasks
const tasks = [
  task({ ..., run_in_background: true }),
  task({ ..., run_in_background: true }),
  task({ ..., run_in_background: true })
];

// Do other work while they run...

// Check results later
for (const t of tasks) {
  const result = read(t.output_file);
  // Process result
}
```

### Output File Location

Background tasks write to output files. Use `Read` tool or `tail` to check progress:
```bash
tail -f [output_file_path]
```

---

## Agent Resume

### When to Resume

Resume agents when:
- Previous agent produced partial results
- Need to continue a long conversation with context
- Building on previous agent's discoveries

### Pattern: Resume for Follow-up

```typescript
// Initial agent run
const result = task({
  subagent_type: "researcher",
  prompt: "Research authentication libraries",
  description: "Auth research"
});
// result includes agent_id

// Later, resume for follow-up
task({
  subagent_type: "researcher",
  prompt: "Based on your findings, now compare JWT vs session tokens",
  resume: result.agent_id  // Continues with full previous context
});
```

### Pattern: Error Recovery Resume

```typescript
// Agent hit an error or timeout
const result = task({ ... });  // Partial completion

// Resume to continue
task({
  prompt: "Continue from where you left off. Complete the remaining items.",
  resume: result.agent_id
});
```

### Agent ID Storage

Store active agent IDs in `.claude/context/working/agent-state.json` for session recovery:
```json
{
  "active_agents": [
    {"id": "agent-123", "task": "description", "started": "timestamp"}
  ]
}
```

---

## Interactive Queries (AskUserQuestion)

### When to Ask

Use AskUserQuestion when:
- Multiple valid approaches exist
- User preference matters
- Destructive operation needs confirmation
- Requirements are ambiguous

### When NOT to Ask

Skip AskUserQuestion when:
- Reasonable default exists
- Choice has minimal impact
- User already specified preference
- You can make informed decision

### Pattern: Approach Selection

```typescript
AskUserQuestion({
  questions: [{
    question: "Which state management approach should we use?",
    header: "State Mgmt",
    options: [
      { label: "Zustand (Recommended)", description: "Simple, minimal boilerplate" },
      { label: "Redux Toolkit", description: "Full-featured, good DevTools" },
      { label: "Jotai", description: "Atomic, fine-grained updates" }
    ],
    multiSelect: false
  }]
})
```

### Pattern: Feature Selection

```typescript
AskUserQuestion({
  questions: [{
    question: "Which features should we include?",
    header: "Features",
    options: [
      { label: "Authentication", description: "User login/logout" },
      { label: "Authorization", description: "Role-based access" },
      { label: "Audit Logging", description: "Track all actions" },
      { label: "Rate Limiting", description: "Prevent abuse" }
    ],
    multiSelect: true  // Allow multiple selections
  }]
})
```

### Pattern: Confirmation Before Destructive Action

```typescript
AskUserQuestion({
  questions: [{
    question: "This will delete all test data. Proceed?",
    header: "Confirm",
    options: [
      { label: "Yes, delete", description: "Remove all test data permanently" },
      { label: "No, cancel", description: "Keep existing data" }
    ],
    multiSelect: false
  }]
})
```

---

## Technical Parallelization

For Promise.all, Promise.allSettled, and concurrency control patterns, Claude knows these intrinsically. Use standard TypeScript async patterns - no special documentation needed.

---

## Related Documentation

- **agent-guide.md** - Agent hierarchy, roles, and escalation patterns
- **SKILL.md** - Quick delegation reference

---

**Core Mantra**: When in doubt, parallelize. Spotcheck everything. Escalate appropriately.
