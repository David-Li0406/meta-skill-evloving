# Claude 4.5 Optimization Guide

Specific prompt engineering techniques for Claude 4.5, Sonnet 4.5, Haiku 4.5, and Opus 4.5 models.

## Core 4.5 Principles

Claude 4.5 models differ significantly from Claude 3 and earlier versions. They require more explicit instructions but reward precision with superior results.

### Be Explicit with Instructions

**Why:** Claude 4.5 requires clear, specific instructions rather than implicit expectations.

**Before (Claude 3 style - vague):**
```
Improve this code for performance.
```

**After (Claude 4.5 style - explicit):**
```xml
<objective>
Analyze the code and improve performance. Focus on:
1. Reducing algorithmic complexity (prioritize big-O improvements)
2. Eliminating redundant operations
3. Optimizing data structures
4. Reducing memory allocation

Output format:
- List of 3-5 specific inefficiencies found (with line numbers)
- Explanation of each inefficiency
- Optimized code (complete, functional, tested mentally)
- Benchmark estimate (expected performance improvement %)
</objective>
```

**Key difference:** Claude 4.5 processes explicit instructions literally and precisely, while earlier models would "fill in the gaps" with assumptions.

### Add Contextual Motivation

Explain WHY the task matters to help Claude 4.5 prioritize correctly.

**Pattern:**
```xml
<context>
[What is the background?]
[Why does this matter?]
[What are the consequences of error?]
</context>

<objective>
[The specific task]
</objective>

<instructions>
[Step-by-step guidance]
</instructions>
```

**Example:**
```xml
<context>
Medical diagnosis automation requires extreme accuracy. Hallucinated medical information could lead to patient harm. This system must only make claims supported by peer-reviewed research.
</context>

<objective>
Analyze these symptoms against the knowledge base and identify most likely diagnoses with confidence scores.
</objective>

<instructions>
1. For each symptom, find supporting research
2. Only reference peer-reviewed sources
3. If information is not in the knowledge base, state explicitly
4. Output confidence for each diagnosis (low/medium/high)
5. Flag any claims lacking strong evidence
</instructions>

<knowledge_base>
{{MEDICAL_RESEARCH}}
</knowledge_base>
```

### Pay Attention to Examples

Claude 4.5 mimics patterns in examples with high precision. Poor examples teach bad behaviors.

**Bad example (inconsistent style):**
```xml
<examples>
<example>
<input>List the top 3 benefits</input>
<output>
- Benefit one
- Benefit two
- Benefit three
</output>
</example>

<example>
<input>What are the advantages?</input>
<output>
Advantage 1: Description
Advantage 2: Description
</output>
</example>
</examples>
```

**Good example (consistent structure):**
```xml
<examples>
<example>
<input>List the top 3 benefits of cloud computing</input>
<output>
1. **Scalability**: Resources automatically adjust to demand
2. **Cost efficiency**: Pay only for resources used
3. **Reliability**: Built-in redundancy ensures uptime
</output>
</example>

<example>
<input>List the top 3 benefits of containerization</input>
<output>
1. **Portability**: Run consistently across environments
2. **Efficiency**: Lower overhead than VMs
3. **Isolation**: Security boundaries between containers
</output>
</example>
</examples>
```

Claude 4.5 will replicate this exact structure for new inputs.

---

## Advanced 4.5 Capabilities

### Long-Horizon Reasoning

Claude 4.5 excels at multi-step tasks across extended context, with exceptional state tracking.

**Pattern for long tasks:**
```xml
<instructions>
This is a complex, multi-step task. Work systematically and maintain focus on incremental progress.

Key approach:
- Make steady advances on a few things at a time (not everything at once)
- Track state explicitly as you progress
- Verify each step before moving forward
- Save intermediate results regularly

Do not attempt to solve everything at once. Instead:
1. Break the task into phases
2. Complete each phase fully
3. Document what's been done before moving on
</instructions>

<progress_tracking>
Current phase: 1/5
Completed: [tracking file or explicit listing]
Next: [what's coming]
Blockers: [any issues]
</progress_tracking>
```

### Context Awareness and Multi-Window Workflows

Claude 4.5 knows its remaining token budget and can manage context across multiple windows.

**Pattern for multi-window tasks:**
```xml
<context_note>
Your context window will be automatically compacted as it approaches its limit, allowing you to continue working indefinitely from where you left off. Do not artificially stop work due to token concerns. Instead:

1. As context fills up, save detailed progress to external storage
2. Include state, completed work, and next steps
3. Continue from saved state in next window

Important: You can always resume. Never stop early.
</context_note>

<state_management>
Save to progress.json at regular intervals:
{
  "phase": "current phase number",
  "completed": ["item1", "item2"],
  "in_progress": "current work",
  "next_steps": ["step1", "step2"],
  "blockers": ["issue1"],
  "token_usage_estimate": "for next window"
}
</state_management>
```

**For multi-context workflows:**
```xml
<first_window_instructions>
Set up the framework:
1. Create test structure
2. Define architecture
3. Plan implementation
4. Save plan to files
5. Commit plan to git

Do NOT implement yet - prepare the ground.
</first_window_instructions>

<subsequent_window_instructions>
1. Check progress files and git log
2. Run existing tests
3. Implement next set of features
4. Maintain test coverage
5. Commit regularly
</subsequent_window_instructions>
```

---

## Output Control

### Communication Style

Claude 4.5 is more direct and concise by default. Adjust as needed.

**For concise responses (default):**
```xml
<communication_style>
Be direct and concise. Skip verbose summaries unless explicitly requested.
Report what was accomplished with facts, not self-congratulation.
</communication_style>
```

**For verbose responses (when needed):**
```xml
<communication_style>
Provide detailed updates after each step. Explain:
- What was accomplished
- Why this approach was taken
- What will be done next
- Any blockers or decisions needed
</communication_style>
```

### Format Control

Style influences output format. Match your prompt style to desired output.

**For markdown-heavy output (default):**
```xml
<instructions>
Your response may include markdown, bullet points, code blocks as appropriate.
Use bold, italics, and formatting liberally.
```

**For prose-only output:**
```xml
<instructions>
Write in clear, flowing prose using complete paragraphs.
Avoid markdown formatting, bullet points, and excessive structure.
Use standard paragraph breaks for organization.
Incorporate lists naturally into sentences rather than as separate items.
</instructions>
```

**For technical documentation:**
```xml
<instructions>
Use markdown headers (###, ####) for section organization.
Use inline code for technical terms and commands.
Use code blocks (```language```) for examples.
Use tables for structured data comparison.
Minimize other formatting to keep focus on content.
</instructions>
```

### Tool Usage Direction

Claude 4.5 requires explicit action-oriented instructions, not suggestions.

**Vague (may get suggestions only):**
```
Can you improve this code?
```

**Explicit (gets implementation):**
```xml
<instructions>
Improve this code by:
1. Reducing algorithmic complexity
2. Optimizing memory usage
3. Adding error handling

Implement all improvements directly. Do not suggest - execute.
Output the complete, improved code.
</instructions>
```

**Control action defaults:**
```xml
<default_behavior>
By default, implement changes directly rather than only suggesting them.
If intent is unclear, infer the most useful action and proceed.
Use tools to discover any missing details rather than guessing.
</default_behavior>
```

Or for conservative approach:
```xml
<default_behavior>
Do not jump into implementation unless explicitly instructed.
When intent is ambiguous, provide information and recommendations first.
Only make edits when clearly requested.
</default_behavior>
```

---

## Tool and Model-Specific Guidance

### Parallel Tool Calling

Claude 4.5 (especially Sonnet 4.5) is very aggressive with parallel execution.

**For maximum parallelization:**
```xml
<parallel_execution>
Call multiple independent tools in parallel. Do not:
- Use placeholders or guess parameters
- Make sequential calls when parallel is possible

Do:
- Read 3 files in parallel (not one by one)
- Run multiple searches simultaneously
- Execute multiple shell commands together
</parallel_execution>
```

**To reduce parallelization:**
```xml
<execution_strategy>
Execute operations sequentially with brief pauses between each step.
Ensure each step completes and is verified before the next begins.
</execution_strategy>
```

### Extended Thinking Sensitivity

When extended thinking is DISABLED, Claude 4.5 is sensitive to the word "think".

**Replace "think" with:**
- "consider"
- "evaluate"
- "believe"
- "assess"
- "determine"
- "reason about"

**Before (problematic):**
```
Think about the problem and suggest solutions.
```

**After (better):**
```
Consider the problem and suggest solutions.
```

### With Extended Thinking Enabled

Leverage thinking for complex tasks:
```xml
<thinking_guidance>
After receiving tool results, carefully reflect on their quality.
Use your thinking to:
1. Plan next steps
2. Consider alternative approaches
3. Identify potential issues
4. Decide on best action

Then proceed with the optimal next step.
</thinking_guidance>
```

### Subagent Orchestration

Claude 4.5 can naturally delegate to subagents without explicit prompting.

**Let it orchestrate naturally:**
```xml
<instructions>
If you recognize that delegating to a specialized subagent would improve results, do so.
Claude will automatically recognize when subtasks benefit from fresh context.
</instructions>
```

**For conservative delegation:**
```xml
<instructions>
Only delegate to subagents when the task clearly benefits from a separate agent with fresh context.
Most tasks should be handled directly in this context.
</instructions>
```

---

## Research and Analysis

### Structured Research Approach

Claude 4.5 excels at complex research with structured methodology.

```xml
<research_approach>
For complex research tasks:

1. **Define success criteria**: What constitutes a complete answer?

2. **Develop hypotheses**: What competing theories exist?

3. **Search systematically**:
   - Use multiple search strategies
   - Gather data from different sources
   - Track confidence levels
   - Note gaps in information

4. **Synthesize findings**:
   - Compare sources
   - Identify consensus vs disagreement
   - Estimate confidence in conclusions

5. **Self-critique**:
   - Have I covered all angles?
   - Are my sources reliable?
   - What could I have missed?

6. **Maintain records**:
   - Save research notes
   - Track hypotheses evolution
   - Document sources
</research_approach>
```

### Vision and Image Processing

Claude Opus 4.5 has improved vision capabilities.

**For best results with images:**
```xml
<image_processing>
When analyzing images:
1. Describe what you see in detail
2. Extract structured data from visual elements
3. For complex images, request cropping to zoom into specific regions
4. For multiple images, provide comprehensive cross-image analysis
</image_processing>
```

**Crop tool optimization:**
- Provide Claude with a crop tool or skill to "zoom" into specific regions of images
- Consistent performance uplift on image evaluations when Claude can focus on relevant areas
- Allows detailed analysis of specific image regions
- Particularly effective for complex images with multiple elements
- Reference: Anthropic cookbook provides crop tool implementation examples

---

## Code and Development

### Avoid Overengineering

Claude 4.5 can be overly clever. Control this:

```xml
<simplicity_guidance>
Avoid over-engineering. Only make changes that are directly requested or clearly necessary.

Do NOT:
- Add features beyond what was asked
- Refactor surrounding code
- Create "helper" utilities for one-time operations
- Build in flexibility for hypothetical future needs
- Add error handling for impossible scenarios

Do:
- Implement exactly what was requested
- Keep solutions minimal
- Follow existing patterns
- Trust framework guarantees at boundaries
</simplicity_guidance>
```

### Code Exploration Requirement

Always read code before proposing changes:

```xml
<code_review_protocol>
ALWAYS read relevant files before proposing edits.
Do NOT:
- Speculate about code you haven't inspected
- Make assumptions about style or structure
- Propose changes without verification

Do:
- Open and inspect all referenced files
- Understand existing patterns and conventions
- Match the codebase style
- Verify assumptions by reading code
</code_review_protocol>
```

### Minimize Hallucinations

Investigate before answering:

```xml
<investigation_protocol>
Never speculate about code you have not opened.

When user references a specific file:
1. MUST read the file first
2. MUST verify facts before answering
3. MUST investigate relevant code

Only answer questions about code you have examined.
Provide grounded, hallucination-free answers.
</investigation_protocol>
```

---

## Model Selection and Alternatives

Sometimes prompt engineering isn't the answer. Consider model selection:

```xml
<model_selection_guidance>
When to choose different Claude models:

- **Haiku 4.5**: Fast, simple tasks, high throughput needed
- **Sonnet 4.5**: Balanced (speed/intelligence), recommended for most tasks
- **Opus 4.5**: Complex reasoning, multi-step tasks, highest quality

When prompt engineering won't help:
- If task requires fundamentally different capabilities
- If you're at the quality limit of the model
- If latency requirements demand a faster model
- If cost constraints require efficiency

Consider changing model rather than endlessly tuning prompts.
</model_selection_guidance>
```

---

## Performance Optimization Checklist

Before deploying a Claude 4.5 prompt:

- [ ] **Explicitness**: Are instructions specific enough (not vague)?
- [ ] **Motivation**: Is context provided for why the task matters?
- [ ] **Examples**: Are examples consistent with desired output style?
- [ ] **Format**: Does prompt style match desired output format?
- [ ] **Action**: Are instructions action-oriented (do X, not "can you X")?
- [ ] **Complexity**: Is solution minimal, not over-engineered?
- [ ] **Validation**: Do I read code before proposing edits?
- [ ] **Investigation**: Do I verify facts before answering?
- [ ] **Parallelization**: Are independent operations parallelized?
- [ ] **Fallback**: Do I have model selection criteria if this doesn't work?

