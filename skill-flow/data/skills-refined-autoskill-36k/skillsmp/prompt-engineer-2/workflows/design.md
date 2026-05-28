# Design Workflow

## Purpose

Select optimal pattern and structure the prompt based on analysis and research.

---

## Pattern Selection

### Decision Tree

```
Is task multi-domain?
├── YES → Meta-Prompting
│   └── Does it need tools? → Meta-Prompting + ReAct hybrid
└── NO → Continue...

Does task require tool/API usage?
├── YES → ReAct
│   └── Complex planning needed? → Plan-and-Execute
└── NO → Continue...

Is quality critical with clear criteria?
├── YES → Self-Refine
└── NO → Continue...

Is it a simple, single-step task?
├── YES → Direct prompt (no pattern)
└── NO → Self-Refine (default for complex)
```

### Pattern Summary

| Pattern | Complexity | Token Cost | Quality | Use When |
|---------|------------|------------|---------|----------|
| Direct | Low | Low | Medium | Simple tasks |
| ReAct | Medium | Medium | High | Tool usage |
| Self-Refine | Medium | Medium-High | Very High | Quality matters |
| Meta-Prompting | High | High | Very High | Multi-domain |
| Plan-Execute | High | High | High | Complex goals |

---

## Claude-Specific Optimizations

### XML Structure (Required)

```xml
<role>
Define persona with expertise and perspective
</role>

<context>
Background information the model needs
- Domain context
- Prior state (if any)
- Relevant constraints
</context>

<instructions>
Step-by-step process:
1. First, analyze the input
2. Then, apply logic
3. Finally, format output
</instructions>

<format>
## Output Structure

<section_1>
[Content]
</section_1>

<section_2>
[Content]
</section_2>
</format>

<examples>
<example>
<input>Example input here</input>
<output>Example output here</output>
</example>

<example>
<input>Different example</input>
<output>Different output</output>
</example>
</examples>

<constraints>
- Do NOT include X
- Do NOT exceed Y tokens
- MUST follow format exactly
- NEVER skip sections
</constraints>
```

### Thinking Blocks

**Add when:**
- Multi-step reasoning required
- Decisions need justification
- Complex logic involved

```xml
<thinking_requirement>
Before responding, analyze in <thinking> tags:
1. What are the key elements of the input?
2. What pattern applies here?
3. What edge cases exist?
</thinking_requirement>
```

### Prefill Usage

**For constrained output:**

```python
# In API call
messages = [
    {"role": "user", "content": user_prompt},
    {"role": "assistant", "content": '{"result": '}  # Prefill
]
```

---

## Prompt Assembly

### Section Checklist

- [ ] **Role**: Clear persona (1-3 sentences)
- [ ] **Context**: Background info (as needed)
- [ ] **Instructions**: Numbered steps (3-7 steps)
- [ ] **Format**: Output structure (explicit)
- [ ] **Examples**: 2-3 diverse examples
- [ ] **Constraints**: What NOT to do (3-5 items)

### Length Guidelines

| Prompt Type | Target Length | Max Length |
|-------------|---------------|------------|
| System prompt | 500-1000 tokens | 2000 tokens |
| Task prompt | 200-500 tokens | 1000 tokens |
| Agent prompt | 1000-2000 tokens | 4000 tokens |

### Example Diversity

**Include examples that cover:**
1. **Happy path**: Standard, expected input
2. **Edge case**: Unusual but valid input
3. **Boundary**: At the limits of requirements

---

## Quality Checklist

```markdown
## Design Quality Checklist

### Structure (0-10)
- [ ] Clear role definition (+2)
- [ ] Explicit instructions (+2)
- [ ] Defined output format (+2)
- [ ] 2+ examples (+2)
- [ ] Constraints listed (+2)

### Clarity (0-6)
- [ ] No ambiguous language (+2)
- [ ] Specific, measurable criteria (+2)
- [ ] Logical flow (+2)

### Claude-Specific (0-4)
- [ ] XML tags used (+2)
- [ ] Appropriate thinking blocks (+1)
- [ ] Good section separation (+1)

**Minimum to proceed: 15/20**
```

---

## Pattern Templates

### Direct Prompt Template

```xml
<role>You are a [expertise] that [capability].</role>

<task>
$TASK_DESCRIPTION
</task>

<format>
$OUTPUT_FORMAT
</format>

<example>
Input: $EXAMPLE_INPUT
Output: $EXAMPLE_OUTPUT
</example>
```

### ReAct Template

See: @.claude/skills/prompt-engineer/patterns/react-pattern.md

### Self-Refine Template

See: @.claude/skills/prompt-engineer/patterns/self-refine.md

### Meta-Prompting Template

See: @.claude/skills/prompt-engineer/patterns/meta-prompting.md

---

## Version

**Version**: 1.0.0
