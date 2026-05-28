# GPT-5.2 Model Guide

## 1. Introduction

GPT-5.2 is the newest flagship model for enterprise and agentic workloads, designed to deliver higher accuracy, stronger instruction following, and more disciplined execution across complex workflows. Building on GPT-5.1, GPT-5.2 improves token efficiency on medium-to-complex tasks, produces cleaner formatting with less unnecessary verbosity, and shows clear gains in structured reasoning, tool grounding, and multimodal understanding.

GPT-5.2 is especially well-suited for production agents that prioritize reliability, evaluability, and consistent behavior. It performs strongly across coding, document analysis, finance, and multi-tool agentic scenarios, often matching or exceeding leading models on task completion. At the same time, it remains prompt-sensitive and highly steerable in tone, verbosity, and output shape, making explicit prompting an important part of successful deployments.

This guide focuses on prompt patterns and migration practices that maximize performance in real production systems. These recommendations are drawn from internal testing and customer feedback, where small changes to prompt structure, verbosity constraints, and reasoning settings often translate into large gains in correctness, latency, and developer trust.

## 2. Key Behavioral Differences

Compared with previous generation models (e.g. GPT-5 and GPT-5.1), GPT-5.2 delivers:

- More deliberate scaffolding: builds clearer plans and intermediate structure by default; benefits from explicit scope and verbosity constraints
- Generally lower verbosity: more concise and task-focused, though still prompt-sensitive and preference needs to be articulated in the prompt
- Stronger instruction adherence: less drift from user intent; improved formatting and rationale presentation
- Tool efficiency trade-offs: takes additional tool actions in interactive flows compared with GPT-5.1, can be further optimized via prompting
- Conservative grounding bias: tends to favor correctness and explicit reasoning; ambiguity handling improves with clarification prompts

This guide focuses on prompting GPT-5.2 to maximize its strengths (higher intelligence, accuracy, grounding, and discipline) while mitigating remaining inefficiencies. Existing GPT-5/GPT-5.1 prompting guidance largely carries over and remains applicable.

## 3. Prompting Patterns

Adapt the following themes into your prompts for better steer on GPT-5.2.

### 3.1 Controlling Verbosity and Output Shape

Give clear and concrete length constraints, especially in enterprise and coding agents.

### 3.2 Preventing Scope Drift

GPT-5.2 is stronger at structured code but may produce more code than minimal UX specs and design systems require. To stay within scope, explicitly forbid extra features and uncontrolled styling.

```
<design_and_scope_constraints>
- Explore any existing design systems and understand them first.
- Stay focused on what the user requests; avoid unrelated tangents.
- New patterns, abstractions, or refactors are fine when they improve code health.
- Style aligned to the design system at hand.
- If any instruction is ambiguous, choose the simplest valid interpretation.
</design_and_scope_constraints>
```

For design system enforcement, balance consistency with improvement—new patterns are acceptable when they benefit the codebase.

### 3.3 Long-Context and Recall

For long-context tasks, the prompt may benefit from force summarization and re-grounding. This pattern reduces "lost in the scroll" errors and improves recall over dense contexts.

```
<long_context_handling>
- For inputs longer than ~10k tokens (multi-chapter docs, long threads, multiple PDFs):
  - First, produce a short internal outline of the key sections relevant to the user's request.
  - Re-state the user's constraints explicitly (e.g., jurisdiction, date range, product, team) before answering.
  - In your answer, anchor claims to sections ("In the 'Data Retention' section...") rather than speaking generically.
- If the answer depends on fine details (dates, thresholds, clauses), quote or paraphrase them.
</long_context_handling>
```

### 3.4 Handling Ambiguity and Hallucination Risk

Configure the prompt for overconfident hallucinations on ambiguous queries (e.g., unclear requirements, missing constraints, or questions that need fresh data but no tools are called).

You can add a short self-check step for high-risk outputs:

```
<high_risk_self_check>
Before finalizing an answer in legal, financial, compliance, or safety-sensitive contexts:
- Briefly re-scan your own answer for:
  - Unstated assumptions,
  - Specific numbers or claims not grounded in context,
  - Overly strong language ("always," "guaranteed," etc.).
- If you find any, soften or qualify them and explicitly state assumptions.
</high_risk_self_check>
```

## 4. Compaction (Extending Effective Context)

For long-running, tool-heavy workflows that exceed the standard context window, GPT-5.2 with Reasoning supports response compaction via the `/responses/compact` endpoint. Compaction performs a loss-aware compression pass over prior conversation state, returning encrypted, opaque items that preserve task-relevant information while dramatically reducing token footprint. This allows the model to continue reasoning across extended workflows without hitting context limits.

When to use compaction:

- Multi-step agent flows with many tool calls
- Long conversations where earlier turns must be retained
- Iterative reasoning beyond the maximum context window

Key properties:

- Produces opaque, encrypted items (internal logic may evolve)
- Designed for continuation, not inspection
- Compatible with GPT-5.2 and Responses API
- Safe to run repeatedly in long sessions

Endpoint:

```
POST https://api.openai.com/v1/responses/compact
```

Runs a compaction pass over a conversation and returns a compacted response object. Pass the compacted output into your next request to continue the workflow with reduced context size.

Best practices:

- Monitor context usage and plan ahead to avoid hitting context window limits
- Compact after major milestones (e.g., tool-heavy phases), not every turn
- Keep prompts functionally identical when resuming to avoid behavior drift
- Treat compacted items as opaque; don't parse or depend on internals

## 5. Agentic Steerability and User Updates

GPT-5.2 is strong on agentic scaffolding and multi-step execution when prompted well. You can reuse your GPT-5.1 `<user_updates_spec>` and `<solution_persistence>` blocks.

Two key tweaks to further push the performance of GPT-5.2:

- Clamp verbosity of updates (shorter, more focused)
- Make scope discipline explicit (don't expand problem surface area)

Example updated spec:

```
<user_updates_spec>
- Send brief updates (1-2 sentences) only when:
  - You start a new major phase of work, or
  - You discover something that changes the plan.
- Avoid narrating routine tool calls ("reading file...", "running tests...").
- Each update must include at least one concrete outcome ("Found X", "Confirmed Y", "Updated Z").
- Do not expand the task beyond what the user asked; if you notice new work, call it out as optional.
</user_updates_spec>
```

## 6. Tool-Calling and Parallelism

GPT-5.2 improves on 5.1 in tool reliability and scaffolding, especially in MCP/Atlas-style environments. Best practices:

- Describe tools crisply: 1-2 sentences for what they do and when to use them
- Encourage parallelism explicitly for scanning codebases, vector stores, or multi-entity operations
- Require verification steps for high-impact operations (orders, billing, infra changes)

Example tool usage section:

```
<tool_usage_rules>
- Prefer tools over internal knowledge whenever:
  - You need fresh or user-specific data (tickets, orders, configs, logs).
  - You reference specific IDs, URLs, or document titles.
- Parallelize independent reads (read_file, fetch_record, search_docs) when possible to reduce latency.
- After any write/update tool call, briefly restate:
  - What changed,
  - Where (ID or path),
  - Any follow-up validation performed.
</tool_usage_rules>
```

## 7. Structured Extraction, PDF, and Office Workflows

This is an area where GPT-5.2 clearly shows strong improvements. To get the most out of it:

- Always provide a schema or JSON shape for the output. You can use structured outputs for strict schema adherence.
- Distinguish between required and optional fields.
- Ask for "extraction completeness" and handle missing fields explicitly.

Example:

```
<extraction_spec>
You will extract structured data from tables/PDFs/emails into JSON.

- Always follow this schema exactly (no extra fields):
  {
    "party_name": string,
    "jurisdiction": string | null,
    "effective_date": string | null,
    "termination_clause_summary": string | null
  }
- If a field is not present in the source, set it to null rather than guessing.
- Before returning, quickly re-scan the source for any missed fields and correct omissions.
</extraction_spec>
```

For multi-table/multi-file extraction, add guidance to:

- Serialize per-document results separately
- Include a stable ID (filename, contract title, page range)

## 8. Prompt Migration Guide to GPT-5.2

This section helps you migrate prompts and model configs to GPT-5.2 while keeping behavior stable and cost/latency predictable. GPT-5-class models support a `reasoning_effort` knob (none|minimal|low|medium|high|xhigh) that trades off speed/cost vs. deeper reasoning.

Migration mapping (use these default mappings when updating to GPT-5.2):

| Current model | Target model | Target reasoning_effort           | Notes                                                                                                |
| ------------- | ------------ | --------------------------------- | ---------------------------------------------------------------------------------------------------- |
| GPT-4o        | GPT-5.2      | none                              | Treat 4o/4.1 migrations as "fast/low-deliberation" by default; only increase effort if evals regress |
| GPT-4.1       | GPT-5.2      | none                              | Same mapping as GPT-4o to preserve snappy behavior                                                   |
| GPT-5         | GPT-5.2      | same value except minimal -> none | Preserve none/low/medium/high to keep latency/quality profile consistent                             |
| GPT-5.1       | GPT-5.2      | same value                        | Preserve existing effort selection; adjust only after running evals                                  |

Note: default reasoning level for GPT-5 is medium, and for GPT-5.1 and GPT-5.2 is none.

General steps to migrate to a new model:

1. Switch models, don't change prompts yet. Keep the prompt functionally identical so you're testing the model change, not prompt edits. Make one change at a time.
2. Pin reasoning_effort. Explicitly set GPT-5.2 reasoning_effort to match the prior model's latency/depth profile.
3. Run evals for a baseline. After model + effort are aligned, run your eval suite. If results look good, you're ready to ship.
4. If regressions, tune the prompt. Use targeted constraints (verbosity/format/schema, scope discipline) to restore parity or improve.
5. Re-run evals after each small change. Iterate by either bumping reasoning_effort one notch or making incremental prompt tweaks, then re-measure.

GPT-5.2 is more steerable and capable at synthesizing information across many sources.

Best practices:

- Specify the research bar up front: tell the model how you want to perform search, whether to follow second-order leads, resolve contradictions, and include citations. Explicitly state how far to go.
- Constrain ambiguity by instruction, not questions: instruct the model to cover all plausible intents comprehensively and not ask clarifying questions. Require breadth and depth when uncertainty exists.
- Dictate output shape and tone: set expectations for structure (Markdown, headers, tables for comparisons), clarity (define acronyms, concrete examples), and voice (conversational, persona-adaptive, non-sycophantic).

## 9. Conclusion

GPT-5.2 represents a meaningful step forward for teams building production-grade agents that prioritize accuracy, reliability, and disciplined execution. It delivers stronger instruction following, cleaner output, and more consistent behavior across complex, tool-heavy workflows. Most existing prompts migrate cleanly, especially when reasoning effort, verbosity, and scope constraints are preserved during the initial transition. Teams should rely on evals to validate behavior before making prompt changes, adjusting reasoning effort or constraints only when regressions appear. With explicit prompting and measured iteration, GPT-5.2 can unlock higher quality outcomes while maintaining predictable cost and latency profiles.
