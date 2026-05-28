# Prompt Chaining Architecture

Breaking complex tasks into sequential prompts for accuracy, clarity, and traceability. Distinct from chain-of-thought reasoning within a single prompt.

## When to Use Prompt Chaining

**Prompt chaining is better when:**
- Task has multiple distinct phases (research → analysis → synthesis)
- Each phase needs Claude's full attention
- Outputs from one phase feed into next phase
- Task is complex enough that a single prompt becomes unwieldy
- Debugging specific phases is important

**Don't chain when:**
- Task is simple and self-contained
- Phases are tightly interdependent
- Output quality more important than process clarity

**Key insight:** "Each link in the chain gets Claude's full attention" - single-prompt CoT may cause Claude to drop details midway.

## Chaining vs Chain-of-Thought (CoT)

| Aspect | CoT (Single Prompt) | Prompt Chaining (Multi-Prompt) |
|--------|-------------------|-------------------------------|
| **Mechanism** | Reasoning within one prompt | Sequential prompts |
| **Context** | All previous reasoning available | New context per prompt |
| **Use case** | Reasoning accuracy | Phase separation, debugging |
| **Latency** | Single API call | Multiple API calls |
| **Best for** | <20K tokens, simple reasoning | >50K tokens, multi-phase |

## Core Architecture

### Three Chaining Patterns

#### Pattern 1: Linear Sequential

```
Prompt 1 → Output 1
   ↓
Prompt 2 (uses Output 1) → Output 2
   ↓
Prompt 3 (uses Output 2) → Output 3
```

**Use cases:**
- Research → Outline → Draft → Edit → Publish
- Extract → Transform → Load → Visualize
- Analyze → Interpret → Recommend → Justify

**Advantage:** Each phase optimized independently
**Disadvantage:** Serial execution (slower)

#### Pattern 2: Parallel Independent

```
         ┌→ Prompt 1 → Output 1 ↘
Input ---|→ Prompt 2 → Output 2 |→ Synthesis → Final Output
         └→ Prompt 3 → Output 3 ↗
```

**Use cases:**
- Analyze from multiple perspectives (legal, business, technical)
- Compare multiple options simultaneously
- Parallel data processing

**Advantage:** Faster (parallel execution)
**Disadvantage:** Requires synthesis step

#### Pattern 3: Hierarchical Orchestration

```
Lead Agent (planning) → Delegates to:
├─ Subagent A (deep research)
├─ Subagent B (alternative analysis)
└─ Subagent C (verification)
     ↓
Lead Agent (synthesis)
```

**Use cases:**
- Complex research tasks
- Multi-perspective analysis
- Verification workflows

**Advantage:** Specialized subagent focus
**Disadvantage:** Orchestration overhead

## Structuring Handoffs Between Prompts

### XML-Based Handoff Pattern

**Effective structure for passing data between prompts:**

```
Prompt 1 Output:
<research>
<finding>
  <source>Article: XYZ</source>
  <key_point>Main finding text</key_point>
  <confidence>high</confidence>
</finding>
</research>

Prompt 2 Input:
<task>Analyze and synthesize research findings</task>
<research_input>
[paste Prompt 1 output here]
</research_input>
```

**Benefits:**
- Clear structure for data passing
- Machine-readable handoff
- Easy to validate completeness
- Enables reliable parsing

### Template Variables for Reuse

```
Prompt template:
Analyze this {{document_type}} document:

<document>
{{document_content}}
</document>

Focus on: {{analysis_focus}}
```

**For chaining:**
- Generate analysis in first prompt
- Use output in {{analysis_result}} in second prompt
- Maintain consistency across chain

## Advanced Patterns

### Pattern 4: Self-Correction Chain

**Claude reviews its own work:**

```
Prompt 1: Generate initial solution
   ↓
Prompt 2: Review and critique (given Prompt 1 output)
   ↓
Prompt 3: Refine based on critique
   ↓
[Repeat if quality insufficient]
```

**Example use case:**
```
Phase 1: Draft report
Phase 2: "Review this report for accuracy and completeness.
          Point out any gaps or errors."
Phase 3: "Using the feedback, improve the report."
```

**Quality improvement:** Often catches errors that wouldn't appear in single pass

### Pattern 5: Escalation Chain

**Route to specialized prompts based on complexity:**

```
Prompt 1: Classify complexity level
   ↓
If simple → Prompt 2A (simple handler)
If complex → Prompt 2B (expert handler)
If uncertain → Prompt 2C (verification)
```

**Use case:** Support systems, decision trees

### Pattern 6: Verification Loop

**Verify accuracy before proceeding:**

```
Prompt 1: Generate answer
   ↓
Prompt 2: "Verify this answer independently.
          Do you get the same result?
          List any discrepancies."
   ↓
If verified: Use answer
If discrepancies: Go back to Prompt 1 with feedback
```

## Deciding: Chain or Single Prompt?

**Use chaining if:**
- Output is >5,000 tokens
- Task has 3+ distinct phases
- You need independent optimization per phase
- Debugging specific phases is important
- Multi-agent approach helps (parallel research, different perspectives)

**Use single prompt with CoT if:**
- <20,000 tokens total
- Phases tightly interdependent
- Task naturally sequential
- Latency matters (fewer API calls)

## Orchestration Strategies

### Simple Orchestration (Manual)

```python
# Phase 1: Research
research_output = client.messages.create(
    prompt="Research XYZ..."
)

# Phase 2: Analysis (uses research)
analysis_output = client.messages.create(
    prompt=f"Analyze this research:\n{research_output}"
)

# Phase 3: Synthesis
final_output = client.messages.create(
    prompt=f"Synthesize into report:\n{analysis_output}"
)
```

### Parallel Orchestration

```python
import concurrent.futures

# Run multiple analyses in parallel
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [
        executor.submit(client.messages.create,
                       prompt=f"Analyze from {perspective}..."),
        executor.submit(client.messages.create,
                       prompt=f"Analyze from {perspective}...")
    ]
    results = [f.result() for f in concurrent.futures.as_completed(futures)]

# Synthesize results
final_output = client.messages.create(
    prompt=f"Synthesize these perspectives:\n{results}"
)
```

### Subagent Delegation

```python
# Lead agent orchestrates subagents
subagent_1_output = delegate_to_subagent("task_1", prompt_1)
subagent_2_output = delegate_to_subagent("task_2", prompt_2)
subagent_3_output = delegate_to_subagent("task_3", prompt_3)

# Lead synthesizes
final_output = client.messages.create(
    prompt=f"""
    Synthesize these findings:
    - Perspective 1: {subagent_1_output}
    - Perspective 2: {subagent_2_output}
    - Perspective 3: {subagent_3_output}
    """
)
```

## Common Chaining Workflows

### Research Synthesis Workflow

```
Phase 1: Research collection
  Task: "Research [topic]. Gather key facts, sources, and perspectives."
  Output: Structured findings with citations

Phase 2: Analysis
  Task: "Analyze these findings. Identify patterns and contradictions."
  Output: Analysis framework with key insights

Phase 3: Synthesis
  Task: "Create comprehensive report synthesizing these findings."
  Output: Final report with recommendations
```

### Content Creation Workflow

```
Phase 1: Research & Planning
  Output: Research notes + outline

Phase 2: Draft
  Output: First draft content

Phase 3: Edit & Format
  Output: Polished content

Phase 4: Review
  Output: Quality assessment + feedback

Phase 5: Final refinement
  Output: Publication-ready content
```

### Data Processing Workflow

```
Phase 1: Extract
  → Parse structure, identify fields

Phase 2: Transform
  → Apply business logic, calculations

Phase 3: Load
  → Format for destination system

Phase 4: Validate
  → Verify completeness and accuracy

Phase 5: Report
  → Generate summary of changes
```

## Best Practices

### For Each Prompt in Chain

1. **Clear objective:** State what this prompt accomplishes
2. **Context:** Provide necessary background and previous outputs
3. **Constraints:** Format, length, tone requirements
4. **Output structure:** Exact format for next prompt's input
5. **Success criteria:** How to know if successful

### Handoff Best Practices

- **Include full context:** Don't assume Claude remembers previous calls
- **Structured format:** Use XML or JSON for clear boundaries
- **Explicit connections:** "This is from Phase 1. It shows..."
- **Validation:** Verify output completeness before passing to next prompt
- **Error handling:** What if previous output is incomplete?

### Performance Optimization

- **Parallelize when possible:** Independent phases can run simultaneously
- **Batch processing:** For many chains, consider batch API
- **Cache static content:** Reusable research/context across chains
- **Monitor tokens:** Track total chain token consumption
- **Set timeouts:** Prevent runaway chains with missing outputs

## Troubleshooting Chains

### Problem: Information Lost Between Prompts

**Cause:** Previous output too summarized

**Solution:**
- Pass complete previous output, not summary
- Use structured format to preserve detail
- Verify output includes necessary detail for next phase

### Problem: Inconsistency Across Phases

**Cause:** Each prompt interprets context differently

**Solution:**
- Use consistent terminology in chain
- Provide explicit constraints (tone, format, style)
- Add verification prompt to check consistency

### Problem: Poor Synthesis at End

**Cause:** Synthesis prompt unclear

**Solution:**
- Provide clear synthesis instructions
- Include all inputs explicitly
- Ask Claude to identify contradictions
- Request structured final output

## Examples by Domain

### Legal Analysis Chain
```
1. Extract key clauses
2. Identify risks per clause
3. Compare to standards
4. Generate recommendations
```

### Financial Analysis Chain
```
1. Extract financial metrics
2. Calculate ratios and trends
3. Benchmark against competitors
4. Generate recommendations
```

### Technical Architecture Chain
```
1. Understand requirements
2. Propose multiple architectures
3. Evaluate tradeoffs
4. Recommend approach
5. Create implementation plan
```

## Next Steps

- See extended-thinking-implementation.md for multi-turn chains with thinking
- See architecture-patterns.md for prompt architecture selection
- See optimization-strategies.md for performance tuning across chains
- See guardrails-implementation.md for safety across chained prompts
