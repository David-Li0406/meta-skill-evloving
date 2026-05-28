---
name: prompt-engineer
description: >
  Best-practice prompt engineering using research-backed patterns. Handles: transforming
  rough prompts into production-ready, debugging prompt issues, creating new prompts
  from scratch. ALWAYS researches via subagents (keeps main context clean). Triggers on:
  "improve prompt", "fix prompt", "create prompt", "prompt not working", "write a prompt for",
  "optimize prompt", "/prompt".
degree-of-freedom: medium
allowed-tools: Task, Read, Write, Edit, Glob, Grep, WebSearch, mcp__Ref__*, mcp__mcp-server-firecrawl__*, AskUserQuestion
---

@.claude/shared-imports/CoD_Σ.md

# Unified Prompt Engineering Skill

## Purpose

Transform, debug, or create production-ready prompts using research-backed patterns and mandatory subagent research. Achieves high-quality prompts through:

1. **Research** (via subagents) - External patterns, docs, best practices
2. **Analysis** - Diagnose issues or requirements
3. **Design** - Apply optimal patterns
4. **Validation** (via subagents) - Test and iterate
5. **Production** - Output production-ready prompt

**Announce at start:** "I'm using the prompt-engineer skill to create/improve your prompt."

---

## Quick Reference

| Mode | When to Use | Research Focus | Output |
|------|-------------|----------------|--------|
| **Transform** | Rough prompt → Production | Pattern matching, best practices | Optimized prompt |
| **Debug** | Prompt not working | Root cause analysis | Fixed prompt + diagnosis |
| **Create** | New prompt from requirements | Domain research, examples | New prompt from scratch |

---

## Workflow Files (Progressive Disclosure)

**Mode-Specific Workflows:**
- @.claude/skills/prompt-engineer/workflows/analyze.md - Analyze prompt/requirements
- @.claude/skills/prompt-engineer/workflows/research.md - Subagent research delegation
- @.claude/skills/prompt-engineer/workflows/design.md - Pattern selection + structuring
- @.claude/skills/prompt-engineer/workflows/validate.md - Parallel testing
- @.claude/skills/prompt-engineer/workflows/iterate.md - Refinement loop

**Pattern Library:**
- @.claude/skills/prompt-engineer/patterns/meta-prompting.md - Conductor-Expert
- @.claude/skills/prompt-engineer/patterns/react-pattern.md - Reasoning + Acting
- @.claude/skills/prompt-engineer/patterns/self-refine.md - Iterative improvement

**Templates:**
- @.claude/skills/prompt-engineer/templates/system-prompt.md - System prompt structure
- @.claude/skills/prompt-engineer/templates/agent-prompt.md - Subagent definition
- @.claude/skills/prompt-engineer/templates/task-prompt.md - Task-specific prompt

---

## Step 1: Detect Mode

**Pattern Matching:**

```
Mode_Patterns := {
  transform: ["improve", "optimize", "make better", "refine", "enhance"],
  debug: ["not working", "failing", "broken", "fix", "wrong output", "issues"],
  create: ["create", "write", "generate", "build", "new prompt"]
}
```

**Detection Logic:**
```
IF user_message contains Mode_Patterns.debug keywords:
  mode := "debug"
ELSE IF user_message contains Mode_Patterns.create keywords:
  mode := "create"
ELSE:
  mode := "transform"  # Default

PROCEED to Step 2 with detected mode
```

---

## Step 2: Analyze Input

### Transform Mode
**Analyze existing prompt for:**
- Structure (sections, formatting)
- Clarity (ambiguous language)
- Completeness (missing elements)
- Examples (presence/quality)
- Claude-specific (XML, thinking blocks)

### Debug Mode
**Diagnose issues:**
- Expected vs actual output
- Error patterns
- Missing context
- Instruction clarity
- Edge case handling

### Create Mode
**Extract requirements:**
- Task type (system, task, agent)
- Domain (technical, creative, analytical)
- Inputs/outputs expected
- Constraints/limitations
- Quality criteria

---

## Step 3: Research (ALWAYS via Subagent)

**CRITICAL:** Research runs in isolated subagent context to keep main context clean (~10K tokens).

### Launch Research Subagent

```python
Task(
    subagent_type="prompt-researcher",
    description="Research for $MODE prompt engineering",
    prompt="""
    Research the following for prompt engineering:

    **Context:**
    - Mode: $MODE
    - Domain: $DOMAIN
    - Task type: $TASK_TYPE

    **Research Tasks:**
    1. Query Ref MCP for relevant library/API documentation
    2. Query Firecrawl for latest prompt engineering patterns
    3. Find examples from prompt-engineering-examples.md
    4. Identify Claude-specific optimizations

    **Return:**
    - Top 3 patterns for this use case
    - Relevant examples (condensed)
    - Key optimizations
    - Pitfalls to avoid

    Maximum 500 tokens in response.
    """
)
```

### Research Sources

| Source | Query For | Tool |
|--------|-----------|------|
| Ref MCP | Library/API docs | mcp__Ref__ref_search_documentation |
| Firecrawl | Latest patterns | mcp__mcp-server-firecrawl__firecrawl_search |
| Internal | prompt-engineering-examples.md | Read |
| Web | Current best practices | WebSearch |

---

## Step 4: Design Prompt

### 4.1 Select Pattern

**Pattern Selection Matrix:**

| Use Case | Primary Pattern | Secondary |
|----------|-----------------|-----------|
| Multi-domain task | Meta-Prompting | ReAct |
| Tool/API usage | ReAct | Plan-Execute |
| Quality-critical | Self-Refine | Meta-Prompting |
| Simple task | None (direct) | - |
| Agent creation | Meta-Prompting | Self-Refine |
| Iterative process | Self-Refine | ReAct |

### 4.2 Apply Claude-Specific Optimizations

**Required Elements:**

```markdown
## Claude Optimizations Checklist

- [ ] **XML Structure**: Use tags for sections (<role>, <instructions>, <format>)
- [ ] **Thinking Blocks**: Add <thinking> for complex reasoning
- [ ] **Prefill**: Use assistant prefill for constrained output
- [ ] **Examples**: Include 2-3 diverse examples
- [ ] **Explicit Format**: Define output structure clearly
- [ ] **Constraints**: List what NOT to do
- [ ] **Context**: Provide necessary background
```

### 4.3 Structure Prompt

**Standard Sections:**

```xml
<role>
Define the persona and expertise
</role>

<context>
Relevant background information
</context>

<instructions>
Step-by-step process to follow
1. First step
2. Second step
3. Continue...
</instructions>

<format>
Expected output structure
</format>

<examples>
<example>
Input: ...
Output: ...
</example>
</examples>

<constraints>
- What NOT to do
- Limitations
</constraints>
```

---

## Step 5: Validate (via Parallel Subagents)

**Launch 3-5 test scenarios in parallel:**

```python
# Happy path test
Task(
    subagent_type="prompt-validator",
    description="Test happy path",
    prompt="""
    Test this prompt with a standard input:

    <prompt>
    $DESIGNED_PROMPT
    </prompt>

    <test_input>
    $HAPPY_PATH_INPUT
    </test_input>

    Evaluate:
    1. Does output match expected format?
    2. Is reasoning sound?
    3. Are all instructions followed?

    Return: PASS/FAIL with reasoning
    """
)

# Edge case test
Task(
    subagent_type="prompt-validator",
    description="Test edge case",
    prompt="... test with edge case input ..."
)

# Adversarial test
Task(
    subagent_type="prompt-validator",
    description="Test adversarial input",
    prompt="... test with challenging input ..."
)
```

**Validation Criteria:**

| Test Type | Pass Criteria |
|-----------|---------------|
| Happy Path | Output matches format, follows instructions |
| Edge Case | Handles gracefully, no crashes |
| Adversarial | Maintains safety, doesn't break |
| Format | Consistent structure across inputs |
| Quality | Meets stated quality criteria |

**Target**: ≥80% pass rate before production

---

## Step 6: Iterate (Self-Refine Loop)

**If validation score < 80%:**

```
Generate → Reflect → Refine → Validate → [Repeat if needed]
```

**Reflection Prompt:**

```markdown
## Prompt Critique

**Failed Tests:**
- $TEST_1: $REASON
- $TEST_2: $REASON

**Root Causes:**
1. $CAUSE_1
2. $CAUSE_2

**Improvements Needed:**
1. $IMPROVEMENT_1
2. $IMPROVEMENT_2

Apply these improvements while preserving what worked.
```

**Maximum iterations:** 3 (if still failing, flag for human review)

---

## Step 7: Output Production Prompt

**Final Output Structure:**

```markdown
# Production Prompt: $NAME

**Version:** 1.0
**Mode:** $MODE (transform/debug/create)
**Pattern:** $PATTERN_USED
**Validation:** $PASS_RATE%

---

## Prompt

<system>
$SYSTEM_PROMPT
</system>

## Usage Notes

- **When to use:** $USE_CASE
- **Expected inputs:** $INPUT_DESCRIPTION
- **Expected outputs:** $OUTPUT_DESCRIPTION

## Validation Results

| Test | Result | Notes |
|------|--------|-------|
| Happy path | PASS/FAIL | |
| Edge case | PASS/FAIL | |
| Adversarial | PASS/FAIL | |

## Iteration History

| Version | Changes | Improvement |
|---------|---------|-------------|
| 1.0 | Initial | - |
| 1.1 | Added examples | +15% |
```

---

## Quality Gates

| Gate | Requirement | Enforcement |
|------|-------------|-------------|
| Research | Subagent research completed | Task tool invoked |
| Structure | XML tags used | Check formatting |
| Examples | ≥2 examples included | Count examples |
| Validation | ≥80% pass rate | Test results |
| Format | Clear output specification | Format section present |
| Constraints | Negative instructions | Constraints section |

---

## Pattern Quick Reference

### Meta-Prompting (Conductor-Expert)
**Use when:** Multi-domain expertise needed
**Structure:** Conductor analyzes → Generates expert prompts → Synthesizes
**See:** @.claude/skills/prompt-engineer/patterns/meta-prompting.md

### ReAct (Reasoning + Acting)
**Use when:** Tool usage, information gathering
**Structure:** Thought → Action → Observation → Loop
**See:** @.claude/skills/prompt-engineer/patterns/react-pattern.md

### Self-Refine
**Use when:** Quality critical, clear evaluation criteria
**Structure:** Generate → Critique → Refine → Validate
**See:** @.claude/skills/prompt-engineer/patterns/self-refine.md

---

## Common Mistakes

| Mistake | Impact | Prevention |
|---------|--------|------------|
| No research | Reinvent patterns | Always run research subagent |
| Generic prompt | Poor performance | Add domain-specific context |
| Missing examples | Unclear expectations | Include 2-3 diverse examples |
| No validation | Unknown quality | Run test scenarios |
| Skipping XML | Less structured | Use Claude-optimized format |

---

## Integration with Other Skills

**Before prompt-engineer:**
- Requirements clarification (if needed)

**After prompt-engineer:**
- Integration into agent/skill definitions
- Production deployment

**Related:**
- analyze-code: For code-related prompts
- sdd: For specification prompts

---

## Token Efficiency

**Main context target:** ≤10K tokens

**Token budget:**

| Phase | Main Context | Subagent Context |
|-------|--------------|------------------|
| Analysis | 500 | - |
| Research | 100 (delegation) | 2000 |
| Design | 1500 | - |
| Validation | 200 (per test) | 1000 each |
| Output | 1000 | - |
| **Total** | ~3500 | ~5000 |

**Research in subagents keeps main context clean.**

---

## Version

**Version:** 1.0.0
**Last Updated:** 2025-12-30
**Owner:** Claude Code Intelligence Toolkit

**Change Log:**
- v1.0.0 (2025-12-30): Initial unified prompt engineering skill
