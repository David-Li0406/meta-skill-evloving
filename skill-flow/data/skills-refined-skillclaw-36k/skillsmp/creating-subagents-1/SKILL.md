---
name: creating-subagents
description: Guide for creating effective subagents with concise prompts and skill integration. This skill should be used when users want to create a new subagent, improve existing subagent definitions, or need guidance on subagent architecture. Triggers on "create subagent", "create agent", "new subagent", "improve agent", or "subagent definition".
---

# Creating Subagents

Create specialized, concise subagents that leverage existing skills for task-specific workflows.

## When to Use

- Creating new subagents for specialized tasks
- Improving or refactoring existing subagent definitions
- Validating subagent architecture and design
- Determining optimal tool access for subagents

## Core Principles

### 1. Concise and Focused

Subagent prompts should be **short and directive** - typically 50-200 words. Avoid lengthy explanations.

**Why**: Subagents operate in separate contexts. Verbose prompts waste tokens and reduce effectiveness.

### 2. Leverage Skills, Not Prompts

When subagents need specialized knowledge, **create or reference skills** instead of embedding instructions in the prompt.

**Why**: Skills are reusable, maintainable, and can include bundled resources. Prompts should orchestrate, not educate.

### 3. Single Responsibility

Each subagent should handle **one clear domain** with minimal scope creep.

**Why**: Focused subagents are more predictable and easier to maintain.

## Creation Workflow

### Step 1: Define Purpose

Clearly articulate what the subagent will do:

- What specific task domain does it handle?
- When should it be invoked (proactively or on-demand)?
- What makes this worthy of a separate subagent?

### Step 2: Skill Validation

**Critical step**: Before writing the subagent prompt, determine if a skill should be created.

**Create a skill when**:
- Subagent needs procedural knowledge (multi-step workflows)
- Domain requires reference material (schemas, APIs, templates)
- Task involves reusable assets (scripts, boilerplate code)
- Complexity exceeds ~100 words of instructions

**Use prompt-only when**:
- Task is simple orchestration with existing tools
- Behavior is purely about tool usage patterns
- No specialized domain knowledge required

**If skill needed**: Create the skill first using `Skill(command='creating-skills')`, then reference it in the subagent with Skill() invocations.

### Step 3: Tool Selection

Grant **minimal necessary tools**. Omit the `tools` field only if all tools are genuinely needed.

Common tool patterns:
- **Read-only research**: Read, Grep, Glob
- **Code modification**: Read, Edit, Grep, Glob, Bash
- **Testing**: Bash, Read, Grep
- **Documentation**: Read, Write, Grep, Glob

### Step 4: Choose Color

Select an appropriate color from the color coding system (see `references/color-codes.md`):

- **purple**: Review/audit agents
- **blue**: Implementation/development agents
- **green**: Testing/validation agents
- **yellow**: Documentation agents
- **orange**: Maintenance/refactoring agents
- **red**: Debugging/troubleshooting agents
- **cyan**: Research/analysis agents
- **magenta**: Deployment/operations agents
- **white**: General purpose agents

Choose based on the agent's **primary purpose**.

### Step 5: Craft the Prompt

Use the `Skill(command='crafting-agentic-prompts')` for prompt engineering guidance.

**Structure**:
```markdown
---
name: subagent-name
description: When to invoke this subagent (proactive triggers)
tools: Tool1, Tool2, Tool3
model: inherit  # or sonnet/opus/haiku
color: blue  # See references/color-codes.md for color system
---

[Role: 1 sentence]

[Core instructions: 3-5 directive statements]

[Constraints or workflow if needed: 2-3 lines]

[Skill references: Skill(command='skill-name') if applicable]
```

**Example of concise prompt**:
```markdown
---
name: api-tester
description: Test API endpoints and validate responses. Use proactively after API implementation or when endpoints mentioned.
tools: Bash, Read, Grep
model: inherit
color: green
---

Test API endpoints systematically using curl or HTTPie.

Verify:
- Response status codes match expectations
- Response schemas are valid
- Error handling works correctly
- Authentication flows properly

Invoke Skill(command='api-validation') for schema validation patterns.
```

### Step 6: Location Decision

Choose storage location:

- **Project**: `.claude/agents/` - Task-specific to this codebase
- **User**: `~/.claude/agents/` - Reusable across projects

### Step 7: Create and Test

Create the agent file:

```bash
# For project agents
mkdir -p .claude/agents
# Write agent definition to .claude/agents/agent-name.md

# For user agents
mkdir -p ~/.claude/agents
# Write agent definition to ~/.claude/agents/agent-name.md
```

**Testing approach**:
1. Invoke explicitly: "Use the [name] subagent to..."
2. Test proactive triggering with relevant prompts
3. Verify tool access is sufficient
4. Confirm prompt conciseness delivers results

### Step 8: Iterate

After testing:
- Remove unnecessary instructions
- Add missing constraints if behavior drifts
- Update skill references if domain knowledge grows
- Adjust tool access based on actual usage

## Skill Integration

When subagents need specialized knowledge:

**Invoke skills explicitly**:
```markdown
Invoke Skill(command='crafting-agentic-prompts') for prompt optimization.
Invoke Skill(command='api-security') for authentication patterns.
Invoke Skill(command='database-schema') for table relationships.
```

**Benefits**:
- Skills load on-demand (progressive disclosure)
- Prompts stay lean
- Knowledge stays maintainable
- Skills are reusable across agents

## Anti-Patterns

**Avoid**:
- ❌ Lengthy procedural instructions (create a skill instead)
- ❌ Embedding reference material in prompts (use `references/`)
- ❌ Granting all tools by default (be selective)
- ❌ Creating subagents for one-off tasks (use main thread)
- ❌ Duplicate knowledge across agent and skill

**Prefer**:
- ✅ Short, directive prompts (50-200 words)
- ✅ Skill references for complex workflows
- ✅ Minimal tool access
- ✅ Clear invocation patterns
- ✅ Single source of truth for knowledge

## Validation Checklist

Before finalizing the subagent:

- [ ] Prompt is under 200 words
- [ ] Description clearly states when to invoke
- [ ] Tool list is minimal and justified
- [ ] Color chosen based on primary purpose (see `references/color-codes.md`)
- [ ] Skills created/referenced for complex knowledge
- [ ] Tested with both explicit and proactive invocation
- [ ] No redundant instructions in both prompt and skills
- [ ] Model selection appropriate for task complexity
- [ ] Validated with `scripts/validate_subagent.py`
- [ ] Quality reviewed against `references/subagent-quality-review.md` criteria

## Examples

See `references/subagent-examples.md` for complete examples demonstrating skill integration patterns.

## Resources

### references/

**color-codes.md** - Comprehensive color coding system for categorizing subagents by purpose. Use this to select appropriate colors for subagents.

**subagent-examples.md** - Collection of well-designed subagents showing various patterns, skill integration approaches, and color coding.

**subagent-quality-review.md** - Comprehensive quality review framework with automated validation, scoring rubrics, and approval criteria.
