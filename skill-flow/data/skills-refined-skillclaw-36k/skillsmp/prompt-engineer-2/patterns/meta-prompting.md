# Meta-Prompting Pattern (Conductor-Expert)

## Overview

A meta-orchestrator dynamically creates and coordinates expert LLM personas to solve complex multi-domain tasks.

**When to Use:**
- Tasks requiring multiple domains of expertise
- Situations where expert types can't be anticipated
- Complex problems needing synthesis of perspectives
- Enterprise-scale task automation

**Community Validation:**
- suzgunmirac/meta-prompting: 1,100+ stars
- Stanford paper: 23 benchmarks improvement
- Production: ZoomInfo 80% time reduction

---

## Architecture

```
User Query → Conductor → Generates Expert Prompts →
Execute Experts → Conductor Synthesizes → Final Output
```

---

## Conductor Prompt Template

```xml
<role>
You are a meta-orchestrator that coordinates expert LLMs to solve complex tasks.
You decompose problems, generate specialized expert prompts, and synthesize results.
</role>

<instructions>
Given a task:
1. Analyze what expertise areas are needed
2. Decompose into subtasks requiring different expertise
3. For each subtask, generate an expert persona and specialized prompt
4. Define the execution workflow
5. After experts complete, synthesize into coherent solution
</instructions>

<task>
{{USER_TASK}}
</task>

<thinking>
First, I'll analyze what expertise areas are needed for this task...
Then, I'll decompose into subtasks...
Finally, I'll coordinate the workflow...
</thinking>

<expert_decomposition>
For each subtask, define:
- Expert role and expertise scope
- Specific instructions for that expert
- Expected output format
- How output feeds into solution
</expert_decomposition>

<workflow>
Define execution order and data flow:
1. Expert A produces X
2. Expert B uses X to produce Y
3. Synthesize X + Y into final output
</workflow>

<output_format>
## Expert 1: [Role]
[Expert prompt here]

## Expert 2: [Role]
[Expert prompt here]

## Synthesis Plan
[How to combine results]
</output_format>
```

---

## Expert Generation Template

```xml
<task>
Create an expert prompt for: {{SUBTASK}}
</task>

<expert_requirements>
The expert should:
- Have clear role definition and expertise scope
- Receive specific instructions for this subtask
- Produce output in defined format for integration
- Include relevant examples if complexity warrants
</expert_requirements>

<format>
<expert_prompt>
<role>You are an expert in [domain] with deep knowledge of [specific areas].</role>

<context>
[Relevant background for this subtask]
</context>

<instructions>
[Specific steps for this expert to follow]
</instructions>

<output_format>
[Expected structure of expert's output]
</output_format>
</expert_prompt>
</format>
```

---

## Synthesis Prompt Template

```xml
<role>
You are synthesizing outputs from multiple experts into a coherent solution.
</role>

<expert_outputs>
## Expert 1: [Role]
{{EXPERT_1_OUTPUT}}

## Expert 2: [Role]
{{EXPERT_2_OUTPUT}}

## Expert 3: [Role]
{{EXPERT_3_OUTPUT}}
</expert_outputs>

<original_task>
{{USER_TASK}}
</original_task>

<instructions>
1. Review each expert's contribution
2. Identify complementary insights
3. Resolve any conflicts between experts
4. Synthesize into unified solution
5. Ensure all aspects of original task addressed
</instructions>

<output_format>
## Synthesized Solution

### Key Insights
[Combined insights from all experts]

### Complete Solution
[Unified answer to original task]

### Expert Attribution
[Which expert contributed what]
</output_format>
```

---

## Implementation Example

```python
# Python pseudo-code for meta-prompting

def meta_prompt(user_task: str) -> str:
    # Step 1: Conductor decomposes task
    decomposition = llm_call(
        CONDUCTOR_PROMPT.format(USER_TASK=user_task)
    )

    # Step 2: Parse expert prompts
    experts = parse_expert_prompts(decomposition)

    # Step 3: Execute each expert (can be parallel)
    expert_outputs = []
    for expert in experts:
        output = llm_call(expert.prompt)
        expert_outputs.append({
            "role": expert.role,
            "output": output
        })

    # Step 4: Synthesize results
    final = llm_call(
        SYNTHESIS_PROMPT.format(
            EXPERT_OUTPUTS=format_outputs(expert_outputs),
            USER_TASK=user_task
        )
    )

    return final
```

---

## Best Practices

1. **Clear expertise boundaries**: Each expert should have non-overlapping domain
2. **Explicit handoffs**: Define exactly what each expert produces
3. **Format consistency**: Experts output in parseable format
4. **Synthesis logic**: Conductor knows how to merge outputs
5. **Iteration support**: Allow conductor to request clarification from experts

---

## When NOT to Use

- Simple, single-domain tasks (overkill)
- Time-critical applications (added latency)
- When expertise areas are well-known (use direct prompts)
- Limited token budget (high overhead)

---

## Version

**Version**: 1.0.0
**Source**: Anthropic's prompt generator, Stanford research
