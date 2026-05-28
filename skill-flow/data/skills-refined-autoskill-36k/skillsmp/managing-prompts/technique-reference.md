# Technique Reference

Indexed prompt engineering techniques for fast lookup and application.

## Technique Index by Use Case

### When: Need to improve clarity
- **Explicit instructions** - Use imperative voice, specific requirements
- **Contextual motivation** - Explain why requirements matter
- **Success criteria** - Define measurable goals
- **Output format specification** - Precise structure definition

### When: Need to reduce hallucinations
- **Uncertainty permission** - "If unsure, say so"
- **Quote-grounding** - Extract quotes before analysis
- **Citation requirement** - Every claim needs source
- **Knowledge restriction** - "Use ONLY provided materials"
- **Chain-of-thought verification** - Expose reasoning to catch errors

### When: Need to improve consistency
- **Structured Outputs** - API-enforced JSON schema for guaranteed format compliance
- **Precise format specification** - JSON schema or XML structure (prompt-based)
- **Response prefilling** - Start assistant message with format
- **Multishot prompting** - 3-5 diverse examples
- **Fixed knowledge base grounding** - RAG with vetted sources
- **Sequential task chaining** - Break into focused steps
- **Prompt chaining** - Multi-prompt workflows with XML handoffs

### When: Need better reasoning
- **Extended thinking** - Enable internal reasoning with output requirements (See: extended-thinking-implementation.md)
- **Basic CoT** - "Think step-by-step" (minimal)
- **Guided CoT** - "First analyze X, then Y, finally Z" (moderate)
- **Structured CoT** - `<thinking>` + `<answer>` tags with verification (most effective)
- **Multi-round verification** - Chain multiple prompts for review and refinement

### When: Need better structure
- **XML tags** - Separate components (`<instructions>`, `<data>`, `<examples>`)
- **Hierarchical nesting** - Organize complex data
- **Document structuring** - `<document>` tags with metadata
- **Consistent naming** - Reference tags explicitly

### When: Need to optimize context
- **Prompt caching** - Cache static content ≥1024 tokens
- **Document placement** - Long docs (20K+) at beginning
- **Quote-grounding** - Filter to relevant sections only
- **Information density** - Bullets, tables, code over prose
- **Prompt chaining** - Split into sequential subtasks
- **Template variables** - {{VARIABLE}} for reusable patterns

### When: Need security/safety
- **Input pre-screening** - Filter jailbreak attempts
- **Prompt leak protection** - Separate system/user, output filtering
- **Jailbreak resistance** - Ethical boundaries, adversarial pattern recognition
- **Output sanitization** - Remove sensitive data from responses

### When: Need character consistency
- **Detailed role definition** - Identity, capabilities, boundaries
- **Scenario-based guidance** - Handle different interaction types
- **Reference standards** - Ground in frameworks (ISO, NIST)
- **Response prefilling** - Reinforce persona from first token
- **Capability boundaries** - Explicit can/cannot lists

### When: Need role/persona consistency
- **Role prompting** - Set expert identity via system prompt (legal analyst, CFO, scientist)
- **Detailed role definition** - Capabilities, boundaries, perspective
- **Response prefilling** - Reinforce role with character tag `[ROLE_NAME]`
- **Scenario preparation** - List common situations and expected responses
- **Capability boundaries** - Explicit "I can" and "I cannot" statements

### When: Designing for reusability
- **Prompt templates** - `{{VARIABLE}}` placeholders for dynamic content (See: consistency-techniques.md#template-variables)
- **Template variables** - Separate fixed instructions from variable inputs
- **System/user split** - Reusable system prompt with dynamic user messages
- **Technique combinations** - Template with pre-built technique patterns
- **Version control** - Track prompt structure separately from dynamic inputs

### When: Optimizing for Claude 4.5
- **Explicit instructions** - More specific than Claude 3
- **Contextual motivation** - Helps generalization
- **Example quality** - Claude 4.5 examines closely, must be high quality
- **Action framing** - Imperative over suggestion ("Improve this" not "Can you improve?")
- **Summary requests** - Explicit (4.5 less verbose by default)
- **Quality modifiers** - "Give it your all" for creative tasks
- **Parallel execution guidance** - "Run tools in parallel when independent"
- **Context awareness leverage** - Reference token budget explicitly

---

## Quick Technique Lookup Table

| Need | Technique | Pattern | Detailed Reference |
|------|-----------|---------|-------------------|
| Reduce hallucinations | Quote-grounding | Extract quotes → analyze | guardrails-implementation.md#pattern-2 |
| Reduce hallucinations | Uncertainty permission | "If unsure, say 'I don't have enough information'" | guardrails-implementation.md#pattern-1 |
| Reduce hallucinations | Citations | Every claim needs source quote | guardrails-implementation.md#pattern-3 |
| Reduce hallucinations | Knowledge restriction | "Use ONLY provided materials" | guardrails-implementation.md#pattern-4 |
| Improve consistency | Structured Outputs | API-enforced JSON schema | consistency-techniques.md#structured-outputs |
| Improve consistency | Format specification | JSON schema or XML structure | guardrails-implementation.md#pattern-1 |
| Improve consistency | Response prefilling | Start assistant message with format | consistency-techniques.md#prefilling-response |
| Improve consistency | Examples | 3-5 diverse, structurally identical | guardrails-implementation.md#pattern-3 |
| Improve consistency | Knowledge base grounding | RAG with fixed sources | guardrails-implementation.md#pattern-4 |
| Reusability | Prompt Templates | {{VARIABLE}} placeholders for dynamic content | architecture-patterns.md#template-variables |
| Enable reasoning | Extended Thinking | Internal reasoning with output | extended-thinking-implementation.md |
| Enable reasoning | Basic CoT | "Think step-by-step" | architecture-patterns.md#complex-reasoning |
| Enable reasoning | Guided CoT | "First X, then Y, finally Z" | architecture-patterns.md#complex-reasoning |
| Enable reasoning | Structured CoT | `<thinking>` + `<answer>` tags | architecture-patterns.md#complex-reasoning |
| Enable reasoning | Multi-round verification | Chain prompts for review | prompt-chaining-architecture.md#self-correction |
| Add structure | XML tags | `<instructions>`, `<data>`, `<examples>` | architecture-patterns.md |
| Add structure | Document tags | `<document>` with `<source>`, `<content>` | context-optimization.md#document-organization |
| Optimize context | Caching | cache_control for static ≥1024 tokens | context-optimization.md#prompt-caching |
| Optimize context | Document placement | 20K+ docs at beginning | context-optimization.md#document-organization |
| Optimize context | Quote-grounding | Extract relevant quotes first | context-optimization.md#quote-grounding |
| Optimize context | Prompt Chaining | Sequential multi-prompt workflows | prompt-chaining-architecture.md |
| Optimize context | Template variables | {{VARIABLE}} for reusable patterns | architecture-patterns.md#template-variables |
| Set expert identity | Role Prompting | System prompt with expert identity | technique-reference.md#role-prompting |
| Optimize context | Remove redundancy | Delete Claude's existing knowledge | context-optimization.md#context-reduction |
| Prevent jailbreaks | Input screening | Pre-filter adversarial patterns | guardrails-implementation.md#pattern-1 |
| Prevent jailbreaks | Ethical boundaries | Core principles, refusal patterns | guardrails-implementation.md#pattern-3 |
| Prevent prompt leaks | Separate context | System prompt isolation | guardrails-implementation.md#pattern-2 |
| Prevent prompt leaks | Output filtering | Scan for sensitive keywords | guardrails-implementation.md#pattern-2 |
| Maintain character | Role definition | Detailed identity, capabilities | guardrails-implementation.md#pattern-1 |
| Maintain character | Scenario guidance | Handle different interaction types | guardrails-implementation.md#pattern-2 |
| Maintain character | Capability boundaries | Explicit can/cannot | guardrails-implementation.md#pattern-5 |
| Claude 4.5: vague output | Explicit instructions | Specific requirements, action framing | migration-guide.md#pattern-1 |
| Claude 4.5: stops early | Context awareness | "Use full [X] tokens available" | migration-guide.md#pattern-8 |
| Claude 4.5: suggests not implements | Action framing | "Improve this" not "Can you improve?" | migration-guide.md#pattern-5 |
| Claude 4.5: low creativity | Quality modifiers | "Don't hold back. Give it your all." | migration-guide.md#pattern-6 |
| Claude 4.5: no summaries | Explicit summary requests | "Explain what you're doing before next step" | migration-guide.md#pattern-4 |

---

## Technique Application Patterns

### Pattern: Basic Task (Simple, Straightforward)

**Use when:** Single focused task, clear input/output

**Techniques to apply:**
1. Explicit instructions (imperative voice)
2. Output format specification
3. Basic constraints

**Example structure:**
```
[CLEAR OBJECTIVE]

Requirements:
- Requirement 1
- Requirement 2

Output format: [JSON/XML/specific structure]

{{INPUT}}
```

**Skip:** Examples (obvious pattern), CoT (simple logic), XML tags (single component)

---

### Pattern: Complex Analysis (Multi-step, Judgment)

**Use when:** Requires reasoning, tradeoffs, verification

**Techniques to apply:**
1. Explicit instructions + contextual motivation
2. Structured chain-of-thought (`<thinking>` + `<answer>`)
3. 3-5 diverse examples
4. XML tag structure
5. Guardrails (uncertainty permission, citations)

**Example structure:**
```
<role>[Identity]</role>
<context>[Why this matters]</context>
<objective>[Goal with success criteria]</objective>

<instructions>
[Step-by-step with CoT structure]

<thinking>
[Your reasoning process]
</thinking>

<answer>
[Your final response]
</answer>
</instructions>

<examples>
[3-5 diverse examples]
</examples>

<constraints>
[Rules and boundaries]
</constraints>

<data>
{{INPUT}}
</data>
```

**Include:** CoT, examples, XML structure, guardrails

---

### Pattern: High-Stakes Accuracy (Medical, Legal, Financial)

**Use when:** Errors have serious consequences

**Techniques to apply:**
1. Quote-grounding (extract quotes before analysis)
2. Citation requirement (every claim sourced)
3. Knowledge restriction ("use ONLY provided materials")
4. Structured CoT with verification
5. Uncertainty permission explicit
6. Fixed knowledge base if applicable

**Example structure:**
```
<role>[Expert identity with ethical boundaries]</role>

<instructions>
Step 1: Extract relevant quotes
<quotes>
[Exact quotes with sources]
</quotes>

Step 2: Analyze based solely on quotes
<analysis>
[Analysis with inline citations to quotes]
</analysis>

Critical rules:
- Every claim must reference a quote
- If information missing, state: "Source does not provide..."
- Do not infer beyond what's explicitly stated
- Use ONLY provided materials, not general knowledge

Verification checkpoint:
Before finalizing, verify every claim has supporting quote.
</instructions>

<sources>
{{MATERIALS}}
</sources>
```

**Include:** All major guardrails, CoT, citations, verification

---

### Pattern: Agent/Autonomous Workflow

**Use when:** Tool access, iterative process, extended task

**Techniques to apply:**
1. Detailed role definition (capabilities, boundaries)
2. Process methodology (OODA loop, iterative)
3. Tool orchestration guidance (parallel execution)
4. Budget constraints (tool calls, tokens)
5. Termination conditions
6. Quality gates and checkpoints

**Example structure:**
```
<role>[Identity, capabilities, boundaries]</role>
<context>[Operational environment]</context>
<objective>[Mission with success criteria]</objective>

<process>
[Workflow methodology: OODA, iterative]

Quality gates:
- [Checkpoint 1]
- [Checkpoint 2]
</process>

<tool_usage>
Priorities: [Tool ordering]
Optimization: Invoke tools in parallel when independent
Budget: Simple <X calls, Complex <Y calls, Max Z calls
</tool_usage>

<termination_conditions>
- [Condition 1]
- [Condition 2]
- Diminishing returns reached
</termination_conditions>

<output_format>
[Structured deliverable]
</output_format>

<task>
{{ASSIGNMENT}}
</task>
```

**Include:** Role boundaries, process structure, tool guidance, termination

---

### Pattern: Context-Optimized (Large Documents)

**Use when:** Processing 20K+ tokens of source material

**Techniques to apply:**
1. Document placement (long docs at beginning)
2. Document structuring (`<document>` tags with metadata)
3. Quote-grounding (extract relevant sections)
4. Prompt caching (static content)
5. Consider chaining if >100K total

**Example structure:**
```
<documents>
  <document index="1">
    <source>filename.pdf</source>
    <doc_type>type</doc_type>
    <document_content cache_control="ephemeral">
      [20K+ tokens]
    </document_content>
  </document>
</documents>

<instructions>
Step 1: Extract relevant quotes (filter 20K → 2-5K)
<quotes>
[Relevant sections only]
</quotes>

Step 2: Analyze based on quotes
[Analysis]
</instructions>

<question>
{{USER_QUERY}}
</question>
```

**Include:** Document placement, structuring, quote-grounding, caching

---

### Pattern: Multi-Window Workflow (Extended Task)

**Use when:** Task requires >100K tokens to complete

**Techniques to apply:**
1. State file persistence (JSON with progress)
2. Initial vs continuation prompts
3. Context tracking mechanisms
4. Progress reporting
5. Checkpoint strategy

**Initial prompt structure:**
```
<role>[Identity + state tracking responsibility]</role>
<objective>
Long-term: [Overall goal]
This session: [Current focus]
</objective>

<state_management>
Create {{STATE_FILE}} after each milestone:
{
  "progress": {"completed": [], "in_progress": [], "pending": []},
  "findings": {},
  "next_steps": [],
  "context": {}
}
</state_management>

<instructions>
[Task for initial session]

Before completing:
1. Update state file with progress
2. Document findings
3. Outline next steps
</instructions>
```

**Continuation prompt structure:**
```
<state_restoration>
1. Load {{STATE_FILE}}
2. Review progress and findings
3. Identify where to resume
</state_restoration>

<instructions>
[Continue from last checkpoint]

Update state file as you progress.
</instructions>
```

**Include:** State persistence, checkpoint strategy, progress tracking

---

## Technique Combinations

### Combination: High Accuracy + Consistency

**Use:** Critical outputs needing uniform format and zero errors

**Techniques:**
- Quote-grounding (accuracy)
- Citations (accuracy)
- Precise format specification (consistency)
- 3-5 examples (consistency)
- Response prefilling (consistency)
- Structured CoT (accuracy)

---

### Combination: Context Optimization + Caching

**Use:** Large repetitive prompts for cost reduction

**Techniques:**
- Identify static content ≥1024 tokens
- Place cacheable content first (tools → system → messages)
- Add cache_control breakpoints
- Remove redundancy (optimization)
- Use quote-grounding for large docs (optimization)

---

### Combination: Claude 4.5 + Creative Task

**Use:** UI design, content creation, innovative solutions

**Techniques:**
- Explicit instructions (Claude 4.5)
- Contextual motivation (Claude 4.5)
- Quality modifiers: "Give it your all" (Claude 4.5 creative)
- Specific aesthetic direction (creative)
- Request features explicitly (Claude 4.5)
- Examples for format consistency

---

### Combination: Security + Character Maintenance

**Use:** Customer-facing agents with sensitive data access

**Techniques:**
- Detailed role definition (character)
- Ethical boundaries (security + character)
- Scenario guidance (character)
- Input screening (security)
- Output sanitization (security)
- Capability boundaries (character)
- Prompt leak protection (security)

---

## Anti-Pattern Recognition

### Anti-Pattern: Vague Instructions

**Bad:** "Analyze this data"
**Why bad:** No scope, format, or success criteria
**Fix:** Explicit objective, requirements, output format
**Technique:** Explicit instructions + format specification

---

### Anti-Pattern: No Examples for Complex Format

**Bad:** "Output as JSON" (complex nested structure, no example)
**Why bad:** Multiple valid interpretations
**Fix:** Precise schema + 2-3 examples
**Technique:** Multishot prompting + format specification

---

### Anti-Pattern: No Reasoning for Analysis

**Bad:** "Is this code secure? List issues."
**Why bad:** No visible reasoning, can't debug errors
**Fix:** Structured CoT with security checklist
**Technique:** Structured chain-of-thought

---

### Anti-Pattern: Insufficient Guardrails for High-Stakes

**Bad:** "Summarize medical research" (no grounding)
**Why bad:** Hallucination risk in critical domain
**Fix:** Quote-grounding + citations + uncertainty permission
**Technique:** Hallucination prevention stack

---

### Anti-Pattern: Poor Context Efficiency

**Bad:** 100K knowledge base embedded repeatedly
**Why bad:** High cost, no optimization
**Fix:** Cache knowledge base, use RAG retrieval
**Technique:** Prompt caching + selective retrieval

---

### Anti-Pattern: Suggestion Framing (Claude 4.5)

**Bad:** "Can you suggest improvements to this code?"
**Why bad:** Claude 4.5 may suggest instead of implement
**Fix:** "Improve this code by [specifics]. Provide implementation."
**Technique:** Action framing for Claude 4.5

---

## Technique Selection Flowchart

```
START: Designing prompt

Task complexity?
├─ Simple → Basic pattern (instructions + format)
├─ Medium → Add examples (2-3)
└─ Complex → Full pattern (examples + CoT + XML)

Risk level?
├─ Low → Basic guardrails
├─ Medium → Uncertainty permission + examples
├─ High → Quote-grounding + citations
└─ Critical → Full guardrail stack

Context size?
├─ <10K tokens → No optimization needed
├─ 10-50K tokens → Remove redundancy, consider caching
├─ 50-100K tokens → Implement caching, document placement
└─ >100K tokens → Chaining required + optimization

Consistency needs?
├─ Low → Format specification sufficient
├─ Medium → Add 2-3 examples
└─ High → 3-5 examples + prefilling

Reasoning needed?
├─ None → No CoT
├─ Some → Basic or guided CoT
└─ Complex → Structured CoT with verification

Model version?
├─ Claude 3 → Standard techniques
└─ Claude 4.5 → Add: explicit instructions, quality modifiers,
                      action framing, summary requests

Agent workflow?
├─ No → Standard pattern
└─ Yes → Add: role definition, tool guidance, termination conditions

Multiple components?
├─ No → No XML needed
└─ Yes → XML structure for organization

END: Technique stack determined
```

---

## Quick Reference Links

**For detailed implementation:**
- Guardrails: guardrails-implementation.md
- Context optimization: context-optimization.md
- Architecture patterns: architecture-patterns.md
- Claude 4.5 migration: migration-guide.md
- Before/after examples: optimization-strategies.md
- Common issues: analysis-patterns.md
