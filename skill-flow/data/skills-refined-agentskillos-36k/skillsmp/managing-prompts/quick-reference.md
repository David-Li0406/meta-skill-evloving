# Quick Reference Guide

Fast validation checklists, common issues, and rapid decision aids for prompt engineering.

## Quick Validation Checklist

Use this before finalizing any prompt:

```
□ OBJECTIVE
  □ Clear, measurable goal stated
  □ Success criteria defined
  □ Output format specified

□ CLARITY
  □ Instructions explicit (action framing, not suggestion)
  □ No vague terms ("analyze this", "improve it")
  □ Contextual motivation provided (why requirements matter)

□ EXAMPLES (if complex task)
  □ 3-5 diverse examples provided
  □ All examples structurally identical
  □ Cover edge cases
  □ Wrapped in <example> tags

□ REASONING (if multi-step or judgment)
  □ Chain-of-thought enabled
  □ Structured: <thinking> + <answer> tags

□ STRUCTURE (if multiple components)
  □ XML tags separate sections
  □ Hierarchical organization
  □ Consistent tag naming

□ GUARDRAILS (based on risk)
  □ Hallucination prevention (quote-grounding, uncertainty permission)
  □ Consistency enforcement (format spec, examples)
  □ Security measures (if applicable)

□ CONTEXT EFFICIENCY
  □ Static content ≥1024 tokens identified for caching
  □ Long documents (20K+) placed at beginning
  □ No redundant information
  □ Splitting considered if >100K tokens

□ CLAUDE 4.5 OPTIMIZATION
  □ Explicit enough for Claude 4.5
  □ Quality modifiers for creative tasks
  □ Summary requests explicit (4.5 less verbose)
  □ Parallel execution guidance (if tools)
```

## Common Issues: Fast Diagnosis

### Symptom: Inconsistent Outputs

**Likely cause:** No examples or poor format specification

**Quick fix:**
```
Add 3-5 examples + precise format spec:

Output format:
{
  "field1": "type",
  "field2": "type"
}

<examples>
[3-5 structurally identical examples]
</examples>
```

---

### Symptom: Hallucinations/Fabricated Facts

**Likely cause:** No uncertainty permission or grounding

**Quick fix:**
```
Add to prompt:
"If information not present in provided materials, state:
'I don't have enough information about [topic].'

Extract exact quotes before analysis:
<quotes>
[Relevant quotes from source]
</quotes>

<analysis>
[Based solely on quotes above]
</analysis>"
```

---

### Symptom: Output Too Concise (Claude 4.5)

**Likely cause:** Claude 4.5 defaults to brevity

**Quick fix:**
```
Add explicit request:
"Provide detailed explanations. For each point:
- What it is
- Why it matters
- How to address it
- Impact of the change"
```

---

### Symptom: Claude Suggests Instead of Implements

**Likely cause:** Suggestion framing instead of action

**Quick fix:**
```
Change from: "Can you improve this code?"
Change to: "Improve this code by [specific optimizations].
Provide the complete optimized implementation."
```

---

### Symptom: High Token Usage

**Likely cause:** No caching, verbose instructions, full documents

**Quick fix:**
```
1. Identify static content ≥1024 tokens → cache
2. Remove redundant explanations
3. Use quote-grounding instead of full docs
4. Consider prompt chaining if >3 subtasks
```

---

### Symptom: Stops Too Early (Claude 4.5)

**Likely cause:** Claude 4.5 context awareness

**Quick fix:**
```
Add:
"You have [X] tokens available. Use full capacity - don't stop
prematurely. If approaching limits, save state and indicate what
remains for continuation."
```

---

## Fast Decision Trees

### Decision: Add Examples?

```
Task complexity?
├─ Simple (obvious pattern) → 1 example or none
├─ Medium (some variation) → 2-3 examples
└─ Complex (edge cases, nuance) → 3-5 examples

Output format?
├─ Multiple valid interpretations → ADD EXAMPLES
└─ Single obvious interpretation → Optional

Consistency critical?
├─ Yes → ADD 3-5 EXAMPLES
└─ No → Optional
```

---

### Decision: Add Chain-of-Thought?

```
Task type?
├─ Simple lookup/format → No CoT needed
├─ Multi-step analysis → ADD STRUCTURED CoT
├─ Judgment/tradeoffs → ADD GUIDED CoT
└─ Complex reasoning → ADD STRUCTURED CoT

Need to debug?
├─ Yes → ADD CoT (reasoning visible)
└─ No → Optional

High accuracy critical?
├─ Yes → ADD CoT (reduces errors)
└─ No → Optional
```

---

### Decision: Implement Caching?

```
Static content size?
├─ <1024 tokens → No caching benefit
├─ 1024-10K tokens → Consider caching if reused 2+ times
└─ >10K tokens → IMPLEMENT CACHING

Reuse frequency?
├─ One-time → No caching
├─ 2-5 times → Cache if >2K tokens
└─ Many times → IMPLEMENT CACHING

Break-even calculation:
Cache write cost = 1.25x regular
Cache read cost = 0.1x regular
Break-even after ~2 cache hits
```

---

### Decision: Split Prompt?

```
Subtask count?
├─ 1-2 subtasks → Single prompt
├─ 3+ distinct subtasks → CONSIDER SPLITTING
└─ 5+ subtasks → SPLIT INTO CHAIN

Token usage?
├─ <50K → Single prompt fine
├─ 50-100K → Consider splitting
├─ 100-200K → SPLIT RECOMMENDED
└─ >200K → MUST SPLIT

Subtasks independent?
├─ Yes → PARALLEL PROMPTS
└─ No → SEQUENTIAL CHAIN

Each subtask needs full attention?
├─ Yes → SPLIT
└─ No → Single prompt acceptable
```

---

## Severity Assessment Guide

### Critical (Must fix immediately)
- Invalid YAML syntax
- No objective specified
- Vague objective causing hallucinations
- Missing guardrails for high-stakes tasks
- >200K tokens (won't fit in context)

### Major (Fix soon)
- No examples for complex tasks
- Missing chain-of-thought for reasoning
- Poor XML structure (confusing sections)
- No caching despite 10K+ static tokens
- Inconsistent output format
- Suggestion framing instead of action (Claude 4.5)

### Minor (Consider fixing)
- Could be more specific
- Slightly verbose
- Missing quality modifiers for creative tasks
- No parallel execution guidance
- Could benefit from better examples

---

## Technique Selection Matrix

### For Hallucination Prevention

| Risk Level | Technique | Implementation |
|------------|-----------|----------------|
| Low | Basic uncertainty permission | "If unsure, say so" |
| Medium | Quote-grounding | Extract quotes → analyze |
| High | Citations required | Every claim needs source |
| Critical | Knowledge restriction + citations | "Use ONLY provided materials" + quotes |

### For Consistency

| Need | Technique | Implementation |
|------|-----------|----------------|
| Format consistency | Precise spec + prefilling | JSON schema + start response |
| Content consistency | 3-5 examples | Diverse, identical structure |
| Approach consistency | Workflow specification | Numbered steps, checkpoints |
| Team consistency | Template variables | {{VARIABLE}} for reusability |

### For Quality Improvement

| Issue | Technique | Implementation |
|-------|-----------|----------------|
| Errors in reasoning | Structured CoT | <thinking> + <answer> tags |
| Missing edge cases | 3-5 diverse examples | Cover variations |
| Vague outputs | Explicit requirements | Numbered list, specific criteria |
| Low creativity (Claude 4.5) | Quality modifiers | "Give it your all" |

---

## Context Optimization Quick Wins

### Immediate Actions (5 minutes)

1. **Remove Claude's existing knowledge**
   - Delete: Python basics, standard libraries, common patterns
   - Keep: Domain-specific, proprietary knowledge

2. **Identify cacheable content**
   - Static instructions >1024 tokens → mark for caching
   - Large knowledge bases >10K → cache
   - Tool definitions >2K → cache

3. **Check document placement**
   - Long documents (20K+) → move to beginning
   - Wrap in <document> tags with metadata

### Medium Effort (15-30 minutes)

4. **Implement caching**
   - Add cache_control breakpoints
   - Place static content first
   - Test cache hit rate

5. **Convert prose to bullets/tables**
   - Replace paragraphs with concise lists
   - Use tables for comparisons
   - Code blocks instead of descriptions

6. **Consolidate examples**
   - Remove redundant examples
   - Keep only diverse, essential ones

### Major Refactor (1-2 hours)

7. **Split into chained prompts**
   - Identify distinct subtasks (3+)
   - Design handoff structure (XML)
   - Implement sequential chain

8. **Use quote-grounding**
   - Extract relevant quotes first
   - Analyze based on quotes only
   - Reduces 50K docs → 2-5K quotes

---

## Output Format Selection

### Analysis Report
**Use when:** Evaluating existing prompt
**Load:** output-formats.md#analysis-report
**Size:** ~80 lines XML template

### Optimization Report
**Use when:** Improving prompt efficiency/quality
**Load:** output-formats.md#optimization-report
**Size:** ~50 lines XML template

### Extraction Decision
**Use when:** Deciding if logic should become prompt/script
**Load:** output-formats.md#extraction-decision
**Size:** ~60 lines XML template

---

## Fast Pattern Lookup

### Need hallucination prevention?
→ guardrails-implementation.md#hallucination-prevention

### Need consistency enforcement?
→ guardrails-implementation.md#consistency-enforcement

### Need to optimize context?
→ context-optimization.md (see table of contents)

### Need before/after examples?
→ optimization-strategies.md (11 examples)

### Need to migrate Claude 3→4.5?
→ migration-guide.md#migration-patterns

### Need architecture template?
→ architecture-patterns.md (5 pattern types)

### Need to decide extraction?
→ extraction-decision-guide.md#decision-tree

### Need common issue examples?
→ analysis-patterns.md#common-prompt-issues

---

## Token Counting Quick Reference

**Estimation:**
- English: ~4 chars/token
- Code: ~3-3.5 chars/token
- JSON/XML: ~3.5-4 chars/token

**Limits:**
- Standard: 200K tokens
- Sonnet 4/4.5: Up to 1M tokens (beta)
- Premium pricing: >200K (2x input, 1.5x output)

**Quick calculation:**
- 1K tokens ≈ 750 words ≈ 4KB text
- 10K tokens ≈ 7,500 words ≈ 40KB text
- 100K tokens ≈ 75,000 words ≈ 400KB text

---

## Workflow Selection Guide

**User asks to analyze a prompt:** → Workflow 1 (Analysis)

**User asks to create a prompt:** → Workflow 2 (Creation)

**User asks to optimize/improve a prompt:** → Workflow 3 (Optimization)

**User mentions Claude 3 or outdated patterns:** → Workflow 4 (Migration)

**User asks if logic should be a prompt:** → Workflow 5 (Extraction Decision)

**User has hallucination issues:** → Load guardrails-implementation.md#hallucination-prevention

**User has high token usage:** → Load context-optimization.md

**User needs specific technique:** → Load technique-reference.md

**User wants examples:** → Load optimization-strategies.md or architecture-patterns.md

---

## Technique Engineering Progression

**Suggested Order (Broad → Specialized):**

Start with techniques that address broad effectiveness, then apply specialized techniques:

1. **Clarity & Directness** (Broadest impact)
   - Explicit instructions
   - Clear success criteria
   - Contextual motivation

2. **Examples** (Multi-shot prompting)
   - 3-5 diverse examples
   - Structurally identical
   - Covers edge cases

3. **Reasoning** (Chain-of-thought)
   - Basic CoT: "Think step-by-step"
   - Guided CoT: "First X, then Y"
   - Structured CoT: `<thinking>` tags

4. **Structure** (XML tags)
   - Separate components
   - Hierarchical organization
   - Consistent naming

5. **Role** (System prompts)
   - Identity definition
   - Expertise framing
   - Boundary clarification

6. **Format Control** (Prefilling)
   - Skip preambles
   - Enforce structure
   - Role reinforcement

7. **Multi-prompt** (Prompt chaining)
   - Complex workflows
   - Sequential subtasks
   - Orchestration patterns

8. **Long context** (Optimization)
   - Document placement
   - Quote-grounding
   - Information density

**Decision Framework:**
```
Simple task?
├─ Yes → Step 1-2 sufficient
└─ No → Continue to step 3

Needs reasoning?
├─ Yes → Add step 3 (CoT)
└─ No → Skip to step 4

Multiple components?
├─ Yes → Add step 4 (XML)
└─ No → Skip to step 5

Role important?
├─ Yes → Add step 5 (Role)
└─ No → Skip to step 6

Format critical?
├─ Yes → Add step 6 (Prefilling)
└─ No → Skip to step 7

Complex workflow?
├─ Yes → Add step 7 (Chaining)
└─ No → Stop

Very large context?
├─ Yes → Add step 8 (Optimization)
└─ No → Complete
```

**When to Break Order:**
- Critical security → Move guardrails to step 2
- Low latency requirement → Skip steps 6-8
- Hallucination risk → Add guardrails early
- Budget-sensitive → Add optimization early

---

## Prompt Improver (Claude Console Tool)

**What It Does:**
Automatically enhances prompts through 4-step iterative improvement process.

**4-Step Process:**

1. **Example Identification**
   - Extracts existing examples
   - Identifies patterns

2. **Initial Draft**
   - Creates structured template
   - Adds XML organization
   - Clear section separation

3. **Chain-of-Thought Refinement**
   - Adds detailed reasoning instructions
   - Step-by-step guidance
   - Verification patterns

4. **Example Enhancement**
   - Updates examples to match new structure
   - Demonstrates reasoning explicitly
   - Improves clarity

**What You Get:**
- Detailed chain-of-thought instructions
- XML tag organization
- Standardized example formatting
- Strategic prefills for guidance

**When to Use:**
✓ Complex tasks requiring detailed reasoning
✓ Situations where accuracy > speed
✓ Current outputs need significant improvement
✓ Want systematic enhancement

✗ Latency-sensitive applications (produces longer responses)
✗ Cost-sensitive applications (more thorough = more tokens)
✗ Simple tasks (overkill)

**Implementation:**

```
Before: Basic prompt
After: Structured template with:
  - Explicit reasoning instructions
  - XML tags for organization
  - Enhanced examples
  - Prefilled guidance

Trade-off: Longer but more accurate responses
```

**Test Case Generator:**
Need examples? Use Test Case Generator to:
1. Generate sample inputs
2. Get Claude's responses
3. Edit to match ideal outputs
4. Add polished examples to prompt

**Accessing Prompt Improver:**
- Available in Claude Console
- Works with all Claude models
- Compatible with extended thinking models
- Select prompt → "Improve prompt" button

**Example Workflow:**
```
1. Start with basic classification prompt
2. Run Prompt Improver
3. Add your feedback: "Results too basic for expert audience"
4. Improver generates enhanced version with:
   - Step-by-step analysis instructions
   - Structured output sections
   - Multi-level reasoning examples
5. Review and refine as needed
```
