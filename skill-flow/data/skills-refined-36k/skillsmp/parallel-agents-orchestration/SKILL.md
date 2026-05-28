---
name: Parallel Agents Orchestration
description: Dispatch concurrent agent workflows for independent problems
version: 1.0.0
source: Adapted from obra/superpowers with FrankX orchestration patterns
---

# Parallel Agents Orchestration

## When to Use Parallel Agents

Use this pattern when you have **multiple independent problems** that:
- Don't share state or dependencies
- Can be understood without context from others
- Won't interfere with each other
- Would benefit from parallel investigation

**Good candidates:**
- Multiple test failures in different files
- Unrelated subsystems broken independently
- Research tasks across different domains
- Code reviews of separate modules

**NOT good candidates:**
- Failures that might be related (fix one, fix others)
- Tasks requiring sequential context
- Shared state modifications

## The Parallel Dispatch Pattern

### Step 1: Analyze and Group

```
Problem: 6 failing tests across 3 domains

Analysis:
├── Authentication (auth.test.ts)
│   ├── Login failure
│   └── Session expiry
├── Products API (products.test.ts)
│   ├── List filtering
│   └── Price calculation
└── UI Components (components.test.ts)
    ├── Modal rendering
    └── Form validation

These are INDEPENDENT - parallel dispatch appropriate.
```

### Step 2: Create Focused Agent Tasks

Each agent gets:
1. **Specific scope** - One domain only
2. **Full context** - All info needed
3. **Clear constraints** - What NOT to change
4. **Expected output** - What to deliver

```typescript
// Agent 1: Authentication
const authTask = {
  domain: "Authentication",
  files: ["src/auth/", "tests/auth.test.ts"],
  failures: ["Login failure", "Session expiry"],
  constraints: "Don't modify product or UI code",
  deliverable: "Fixed tests with explanation"
};

// Agent 2: Products API
const productsTask = {
  domain: "Products API",
  files: ["src/api/products/", "tests/products.test.ts"],
  failures: ["List filtering", "Price calculation"],
  constraints: "Don't modify auth or UI code",
  deliverable: "Fixed tests with explanation"
};

// Agent 3: UI Components
const uiTask = {
  domain: "UI Components",
  files: ["src/components/", "tests/components.test.ts"],
  failures: ["Modal rendering", "Form validation"],
  constraints: "Don't modify auth or API code",
  deliverable: "Fixed tests with explanation"
};
```

### Step 3: Dispatch Concurrently

Using Claude Code's Task tool:

```typescript
// In Claude Code, dispatch multiple agents in ONE message
// This runs them concurrently

<Task: "Fix auth tests" agent="code-fixer">
  Investigate and fix authentication test failures in tests/auth.test.ts.
  Focus ONLY on auth domain. Do not modify product or UI code.
  Return: Summary of root cause and fix applied.
</Task>

<Task: "Fix products tests" agent="code-fixer">
  Investigate and fix products API test failures in tests/products.test.ts.
  Focus ONLY on products domain. Do not modify auth or UI code.
  Return: Summary of root cause and fix applied.
</Task>

<Task: "Fix UI tests" agent="code-fixer">
  Investigate and fix UI component test failures in tests/components.test.ts.
  Focus ONLY on UI domain. Do not modify auth or API code.
  Return: Summary of root cause and fix applied.
</Task>
```

### Step 4: Synthesize Results

After all agents complete:

1. **Review summaries** - Understand each fix
2. **Check for conflicts** - Any overlapping changes?
3. **Run full test suite** - Verify all fixes work together
4. **Commit atomically** - One commit per domain or all together

## FrankX Orchestration Patterns

### Content Pipeline Parallel Dispatch

```
Task: Publish new blog post

Parallel Agents:
├── SEO Agent
│   ├── Keyword optimization
│   ├── Meta description
│   └── Schema markup
├── Social Agent
│   ├── Twitter thread
│   ├── LinkedIn post
│   └── Instagram caption
└── Email Agent
    ├── Newsletter segment
    └── Welcome sequence update

Synthesis: Coordinate publish timing
```

### Multi-Domain Research

```
Task: Research AI agent frameworks

Parallel Agents:
├── LangGraph Research
│   └── Patterns, examples, best practices
├── Claude SDK Research
│   └── Patterns, examples, best practices
├── OpenAI AgentKit Research
│   └── Patterns, examples, best practices
└── Oracle ADK Research
    └── Patterns, examples, best practices

Synthesis: Comparison matrix, recommendations
```

### Codebase Analysis

```
Task: Comprehensive code review

Parallel Agents:
├── Security Analyst
│   └── Vulnerabilities, OWASP
├── Performance Analyst
│   └── Bottlenecks, optimizations
├── Accessibility Analyst
│   └── WCAG compliance
└── Code Quality Analyst
    └── Patterns, DRY, complexity

Synthesis: Prioritized action items
```

## Agent Prompt Template

```markdown
## Task: [Specific Domain Problem]

### Context
[All information the agent needs]

### Scope
- Files to examine: [list]
- Files to modify: [list]
- Domain boundaries: [what's in/out]

### Constraints
- DO NOT modify: [list of off-limits areas]
- DO NOT introduce: [breaking changes, new dependencies, etc.]
- MUST follow: [coding standards, patterns]

### Expected Output
1. Root cause analysis (2-3 sentences)
2. Fix applied (file paths and summary)
3. Verification steps taken
4. Any concerns or recommendations

### Success Criteria
- [Specific test passes]
- [No regressions]
- [Clean implementation]
```

## Anti-Patterns

| Bad Practice | Why It Fails |
|--------------|--------------|
| Vague scope | Agent changes wrong files |
| Missing context | Agent asks questions or guesses |
| No constraints | Agents conflict with each other |
| Coupled tasks | Agents duplicate work or conflict |
| No synthesis | Fixes don't integrate properly |

## Real Example

```
Input: 6 test failures across 3 files

Sequential approach: ~45 minutes
- Investigate each failure one by one
- Context switching between domains
- Waiting for each fix before next

Parallel approach: ~15 minutes
- 3 agents work simultaneously
- Each focuses on one domain
- Synthesis adds 5 minutes
- 3x faster overall

Result: 6 failures fixed, 0 conflicts, 3x speedup
```

## When to Use This Skill

- Multiple independent failures to fix
- Research across several domains
- Code reviews of separate modules
- Content creation across platforms
- Any task naturally decomposable into parallel work

## Related Skills

- `implementation-planning` - Plan parallel execution
- `systematic-debugging` - Each agent uses this
- `test-driven-development` - Verify fixes with tests
