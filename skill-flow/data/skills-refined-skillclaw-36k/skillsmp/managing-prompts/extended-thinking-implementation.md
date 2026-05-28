# Extended Thinking Implementation Guide

Comprehensive guidance for using Claude's extended thinking capabilities for complex reasoning tasks.

## When to Use Extended Thinking

**Best use cases:**
- Complex multi-step reasoning (legal analysis, financial modeling, scientific analysis)
- Tasks requiring significant reflection or verification
- High-stakes decisions requiring careful deliberation
- Tasks where thinking helps verify correctness

**When NOT to use:**
- Simple, straightforward tasks (overhead unnecessary)
- Latency-sensitive applications (thinking increases latency)
- Tasks within capabilities without extended thinking (cost overhead)

## Core Concepts

### Thinking vs Output

**CRITICAL:** Extended thinking ONLY works when you ask Claude to OUTPUT its thinking explicitly.
- Internal thinking that Claude doesn't output: No benefit
- Explicit thinking output: Claude can reference and build on reasoning

**Implementation:** Use `<thinking>` tags in prompt examples or explicitly request thinking blocks.

### Thinking Budget Management

**Minimum allocation:**
- Recommended minimum: 1024 tokens
- Starting point: Set thinking budget 20-30% of max_tokens, adjust based on task complexity

**Example allocation:**
```
max_tokens: 16000
thinking_budget: 5000  # Start here, adjust upward for complex reasoning
```

**Efficiency tip:** Monitor thinking token usage. Simple tasks may need only 1024 tokens; complex analysis may need 10000+.

## Batch Processing Requirement

**CRITICAL CONSTRAINT:** Thinking >32K tokens REQUIRES batch processing to avoid timeouts.

**When this matters:**
- Extended thinking sessions with multiple rounds
- Very complex reasoning tasks
- Deep analysis with extensive verification steps
- Multi-stage problem decomposition

**Batch API implementation:**
```json
{
  "requests": [
    {
      "custom_id": "task-1",
      "params": {
        "model": "claude-opus-4-1",
        "max_tokens": 16000,
        "thinking": {
          "type": "enabled",
          "budget_tokens": 10000
        },
        "messages": [...]
      }
    }
  ]
}
```

## Prompting Strategies with Extended Thinking

### Strategy 1: General Over Prescriptive

**Better:** Provide general instructions and let thinking explore
```
Analyze this legal contract for risks.
```

**Not recommended:** Prescriptive step-by-step with thinking
```
First, think about liability clauses. Then think about payment terms...
```

**Rationale:** Claude's thinking is most effective when given strategic objectives, not micromanaged steps.

### Strategy 2: Thinking Tags in Multishot Examples

**Effective pattern:** Include `<thinking>` tags in your examples to guide thinking patterns.

```
Example:
User: Analyze whether to invest in company X

<thinking>
Let me consider multiple dimensions:
1. Financial health (revenue growth, profitability)
2. Market position (competition, TAM growth)
3. Risks (regulatory, execution, market)
4. Management quality and track record
</thinking>

Investment recommendation: [answer]
```

**Effect:** Claude mimics the thinking structure in your examples.

### Strategy 3: Verification Within Thinking

**Pattern:** Ask Claude to verify its own conclusions within thinking.

```
Solve this complex problem. Within your thinking:
1. Work through the solution
2. Verify your answer independently
3. Check for logical consistency
```

### Strategy 4: Multi-Round Thinking

**For iterative refinement:**

**Round 1:** Initial analysis with thinking
- Use thinking to explore problem
- Generate preliminary answer

**Round 2:** Review and refinement
- Provide your thinking from Round 1
- Ask Claude to critique and refine
- Combine thinking blocks for deeper analysis

## Language and Locale Considerations

**Performance constraint:** Extended thinking performs best in English.

**If using other languages:**
- Expect slightly lower quality reasoning
- Consider providing English examples
- May need additional verification steps
- Claude 4.5 better than earlier models for non-English

## Model-Specific Guidance

### Claude 4.5 with Extended Thinking

**Advantages:**
- Improved instruction following with thinking enabled
- Better at long-horizon reasoning
- Context awareness integrates with thinking

**Implementation:**
```
Include thinking budget awareness in prompt:
"You have extensive thinking budget available for this complex task.
Use it to thoroughly analyze before providing your answer."
```

### Claude 3.5 Sonnet (Earlier Models)

**Note:** Earlier models have less optimized thinking integration.
- May need more explicit structure
- Examples more important
- Verification step especially valuable

## Thinking Block Handling in Multi-Turn Conversations

### Automatic Stripping

**Key behavior:** Claude API automatically strips thinking blocks from previous turns.

**Practical effect:**
- Thinking tokens don't accumulate context window
- You don't need to manually remove thinking blocks
- Safe to include thinking blocks in conversation history
- Token efficient for extended interactions

### When You Must Include Thinking

**Exception: Tool use with interleaved thinking**

When combining thinking with tool calls:
- Include the thinking block with tool results
- Required for Claude to maintain reasoning continuity
- Must be preserved exactly (cryptographically signed)

**DO NOT modify thinking blocks when using tools.**

## Combining Extended Thinking with Other Techniques

### Extended Thinking + Chain-of-Thought

**Complementary but different:**
- CoT: Output reasoning step-by-step
- Thinking: Internal reasoning before outputting
- Combined: Thinking for analysis, CoT tags for structure

**Pattern:**
```
User: Solve this problem.
Request thinking budget: 10000 tokens

<thinking>
[Claude explores problem deeply]
</thinking>

[Claude then outputs structured answer with CoT tags if needed]
```

### Extended Thinking + Multishot Examples

**Most effective combination:**

Examples with `<thinking>` tags guide Claude's approach:
```
Example 1:
<thinking>
Analysis of the problem from multiple angles...
</thinking>

Example 2:
<thinking>
Different approach to similar problem...
</thinking>
```

### Extended Thinking + Structured Outputs

**Use Structured Outputs** for guaranteed format compliance:
- Thinking for reasoning quality
- Structured Outputs for format guarantee
- Combine for reasoning + reliability

## Performance Tips

### Token Efficiency

1. **Start conservatively:** Begin with 1024-2048 thinking tokens
2. **Monitor usage:** Check thinking token consumption
3. **Scale up:** Increase budget if reasoning insufficient
4. **Stop when sufficient:** Don't max out thinking unnecessarily

### Quality Over Quantity

**Don't maximize thinking tokens.** Instead:
- Set budget for task complexity
- Monitor reasoning depth
- Increase only if insufficient
- Example: 5000 tokens often better than 16000 for many tasks

### Latency Tradeoffs

**Extended thinking is slower:**
- Simple tasks: 2-5x latency increase
- Complex tasks: More acceptable (deep reasoning = longer time)
- Batch processing: Mitigates latency concern

**Decision:** Use extended thinking for quality-critical tasks, not speed-critical ones.

## Common Patterns

### Pattern 1: Analysis with Verification

```
Task: Analyze this data for anomalies.

Thinking budget: 5000 tokens

Within your thinking:
1. Identify potential anomalies
2. Verify each against expected patterns
3. Check for data quality issues
```

### Pattern 2: Decision Making

```
Task: Should we proceed with project X?

Thinking budget: 8000 tokens

Provide your reasoning within thinking,
then a clear recommendation.
```

### Pattern 3: Error Detection

```
Task: Review this code for bugs.

Thinking budget: 6000 tokens

Use thinking to:
1. Trace execution flow
2. Check boundary conditions
3. Verify error handling
```

## Troubleshooting

### Thinking Not Improving Results

**Possible causes:**
- Thinking budget too small (increase to 5000+)
- Task too simple for thinking (disable for simple tasks)
- Instructions not aligned with thinking (clarify goal)

**Solution:** Increase thinking budget, verify task complexity warrants extended thinking

### Thinking Blocks Not Appearing

**Possible causes:**
- Extended thinking not enabled in API call
- Model doesn't support extended thinking (use Claude 4.5+)
- Thinking budget too small

**Solution:** Verify extended thinking enabled, use supported model

### Excessive Token Usage

**Possible causes:**
- Thinking budget too high
- Model exploring unnecessary directions
- Unstructured task causing exploration

**Solution:** Lower thinking budget, provide more structure, clarify success criteria

## Thinking Blocks and Prompt Caching

When combining extended thinking with prompt caching, thinking blocks have special behavior that affects performance, costs, and cache invalidation.

### Automatic Caching Behavior

**Thinking blocks cannot be explicitly cached:**
- You cannot add `cache_control` directly to thinking blocks
- However, thinking blocks ARE automatically cached alongside other content in subsequent API calls
- This commonly happens during tool use workflows when passing thinking blocks back with tool results

**When thinking blocks get cached:**
- During multi-turn conversations with tool use
- When passing previous assistant responses (including thinking) back to the API
- In agentic workflows where thinking blocks are part of conversation history

**Important:** This caching happens automatically - you don't need to (and cannot) explicitly mark thinking blocks for caching.

### Token Counting with Cached Thinking

**Critical for cost calculation:**
- When thinking blocks are read from cache, they count as input tokens
- Shows up in `cache_read_input_tokens` in the usage response
- Affects both cost and rate limit calculations

**Example:**
```python
# Request 1: Generate thinking
response_1 = client.messages.create(
    model="claude-opus-4-5",
    thinking={"type": "enabled", "budget_tokens": 5000},
    messages=[{"role": "user", "content": "Analyze this complex problem..."}]
)
# Response includes thinking_block_1 (5000 tokens) + output

# Request 2: Continue with tool results (thinking gets cached)
response_2 = client.messages.create(
    model="claude-opus-4-5",
    thinking={"type": "enabled", "budget_tokens": 5000},
    messages=[
        {"role": "user", "content": "Analyze this complex problem..."},
        {"role": "assistant", "content": [
            {"type": "thinking", "thinking": "..."},  # This gets cached
            {"type": "tool_use", "...": "..."}
        ]},
        {"role": "user", "content": [
            {"type": "tool_result", "...": "..."},
            {"type": "text", "text": "", "cache_control": {"type": "ephemeral"}}
        ]}
    ]
)

# response_2.usage will show:
# - cache_read_input_tokens: includes the 5000 thinking tokens
# - Charged at 0.1x rate for cached thinking
```

### Cache Invalidation Patterns

**Cache remains valid when:**
- Only tool results are provided as user messages
- No non-tool-result content added to conversation
- Content before thinking blocks unchanged

**Cache invalidated when:**
- Non-tool-result user content is added (designates new assistant loop)
- All previous thinking blocks are stripped from context
- Any messages following thinking blocks are removed from cache

**Example invalidation:**
```python
# Valid: Tool results only - cache preserved
messages=[
    {"role": "user", "content": "Question"},
    {"role": "assistant", "content": [thinking_block_1, tool_use_1]},
    {"role": "user", "content": [tool_result_1]}  # Cache valid
]

# Invalid: Non-tool-result content - cache invalidated
messages=[
    {"role": "user", "content": "Question"},
    {"role": "assistant", "content": [thinking_block_1, tool_use_1]},
    {"role": "user", "content": [tool_result_1]},
    {"role": "assistant", "content": [thinking_block_2, text_2]},
    {"role": "user", "content": "Follow-up question"}  # All thinking blocks stripped
]
```

### Workflow Example: Tool Use with Thinking

```python
# Request 1: Initial query with thinking
Request 1:
User: "What's the weather in Paris?"
Response: [thinking_block_1: 3000 tokens] + [tool_use block 1]

# Request 2: Tool result (thinking cached)
Request 2:
User: ["What's the weather in Paris?"],
Assistant: [thinking_block_1] + [tool_use block 1],
User: [tool_result_1, cache=True]
Response: [thinking_block_2: 2000 tokens] + [text block 2]

# Usage for Request 2:
{
    "cache_read_input_tokens": 3000,  # thinking_block_1 from cache
    "cache_creation_input_tokens": 1000,  # tool_result_1 cached
    "input_tokens": 20,  # uncached content
    "output_tokens": 2500  # thinking_block_2 (2000) + text (500)
}

# Request 3: Non-tool-result added (thinking stripped)
Request 3:
User: ["What's the weather in Paris?"],
Assistant: [thinking_block_1] + [tool_use block 1],
User: [tool_result_1, cache=True],
Assistant: [thinking_block_2] + [text block 2],
User: [Text response: "Thanks! What about tomorrow?"]

# Result: All thinking blocks (1 and 2) stripped from context
# Cache only includes non-thinking content
# Processed as if thinking blocks were never present
```

### Cost Optimization with Thinking + Caching

**Best practices:**
- Design tool use workflows to maximize tool-result-only turns (preserves thinking cache)
- Account for thinking token costs when calculating cache ROI
- For long-running agentic workflows, consider thinking token accumulation in cache
- Use 1-hour cache TTL for agentic workflows with thinking >5 minutes apart

**Cost example (Claude Opus 4.5):**
```
Scenario: 5-turn conversation with thinking
- Turn 1: Generate 5000 thinking tokens ($0.025)
- Turn 2-5: Cached thinking read 4 times (4 × 5000 × $0.50/MTok = $0.01)
- Total thinking cost: $0.035 vs $0.125 without caching (72% savings)
```

### Integration with Extended Thinking Workflows

**Multi-round thinking with caching:**
1. Initial request with extended thinking enabled
2. Response includes thinking block + tool use
3. Subsequent requests with tool results (thinking cached automatically)
4. Continue pattern for iterative workflows
5. Avoid non-tool-result messages to maintain thinking cache

**Debugging tip:**
- Check `cache_read_input_tokens` to verify thinking blocks are cached
- Monitor cache invalidations to identify non-tool-result insertions
- Use thinking blocks strategically in tool use workflows for cost efficiency

**Reference:** See context-optimization.md for detailed caching strategies and TTL selection

## Decision Tree: Use Extended Thinking?

```
Is task complex? (multi-step reasoning, verification needed)
├─ YES → Does it need quality > speed?
│        ├─ YES → Use extended thinking
│        └─ NO → Skip extended thinking
└─ NO → Skip extended thinking

Will thinking >32K tokens?
├─ YES → Must use batch API
└─ NO → Can use standard API
```

## Next Steps

- See prompt-chaining-architecture.md for breaking thinking into multiple prompts
- See guardrails-implementation.md for combining thinking with safety constraints
- See claude-4-5-optimization.md for Claude 4.5 specific thinking patterns
