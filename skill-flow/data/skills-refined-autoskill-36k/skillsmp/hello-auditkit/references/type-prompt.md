# Prompt Audit Rules

> **Inherits**: All rules from `rules-universal.md`
> **Execution Required**: Execute each check table below. Output evidence for each category.
> **Source**: Based on Latest GPT Prompting Guide (openai-cookbook/examples/gpt-5)

## Table of Contents

- [Overview](#overview)
- [Structure Validation](#structure-validation)
- [Content Quality](#content-quality)
- [LLM Prompting Best Practices](#llm-prompting-best-practices)
- [Prompt Compliance Checks](#prompt-compliance-checks)
- [LLM-Specific Warnings](#llm-specific-warnings)
- [Common Issues](#common-issues)

---

## Overview

**Applies to**:
- Standalone LLM prompts, system prompts, instruction text
- **Any text content** (pasted directly or from any file, regardless of filename)
- Default rule file for unrecognized content types

**Key focus areas**:
- Verbosity constraints (explicit length limits)
- Scope boundaries (prevent feature creep)
- Output format specification (structured extraction)
- Ambiguity handling (clarification strategy)
- High-risk self-check (verification steps)

> **Dynamic Verification**: Before auditing, fetch latest GPT prompting guides per Step 0 in SKILL.md. Cross-validate built-in checks below against the latest guide and apply any new practices.

---

## Structure Validation

> **Pre-Check Required**: Before flagging any "missing" element, first verify if the intent is already conveyed through examples, context, or patterns that AI can infer from. Only flag if AI cannot reasonably infer the expected behavior.

| Check | Requirement | Severity |
|-------|-------------|----------|
| Verbosity constraints | Output length guidance present (explicit limits OR demonstrative examples OR context AI can infer from) | Severe only if AI cannot infer |
| Scope boundaries | Boundaries conveyed (explicit "do not" list OR clear context/examples showing scope) | Severe only if AI cannot infer |
| Ambiguity handling | Instructions for unclear cases | Warning |
| Output format | Specified structure/format with schema | Warning |
| Grounding | "Based on context" hedging for uncertain claims | Warning |
| Self-check steps | Verification for high-risk outputs | Info |

---

## Content Quality

### Good Prompt Patterns

```markdown
# Explicit verbosity constraints
Default: 3-6 sentences or ≤5 bullets.
Simple questions: ≤2 sentences.
Complex tasks: 1 overview + ≤5 tagged bullets (What, Where, Risk, Next, Open).

# Scope discipline
Implement EXACTLY and ONLY what requested.
Do NOT add: extra features, uncontrolled styling, new UI elements.
Forbidden: inventing elements not in requirements.

# Ambiguity handling
If unclear: provide 1-3 precise clarifying questions OR 2-3 interpretations with assumption labels.

# Output format with schema
Return JSON: { "status": "success|error", "result": {...}, "errors": [] }
Required fields: status, result. Optional: errors.

# Grounding
Based on the provided context, [conclusion].
Never fabricate specific numbers, line numbers, or external references.

# High-risk self-check
Before outputting legal/financial/security content:
- Re-scan for unstated assumptions
- Verify no ungrounded specifics
- Check for overstatements
```

### Bad Prompt Patterns

> **Fix Approach**: Before suggesting "Add X", first check if existing examples/context already convey the intent. Prefer MODIFY over ADD.

| Pattern | Problem | Fix Approach |
|---------|---------|--------------|
| "Do it well" | Vague, non-actionable | Clarify criteria (modify existing text) |
| No length guidance AND no examples | Unbounded verbosity | First check if examples imply length; if not, add minimal guidance |
| No scope indication AND no context | Feature creep risk | First check if context implies scope; if not, clarify boundaries |
| Absolute claims | No grounding | Add hedging language |
| "Be helpful" | Too generic | Specify concrete behaviors |
| "Handle errors" | Undefined | Specify error types |

---

## LLM Prompting Best Practices

> **Source**: Latest GPT Prompting Guide from [openai-cookbook/examples/gpt-5](https://github.com/openai/openai-cookbook/tree/main/examples/gpt-5)

### Core Principles

1. **Explicit over implicit**: Articulate preferences clearly, don't assume AI knows your style
2. **Constraint-driven**: Use explicit scope, verbosity, format constraints
3. **Verification-oriented**: Add self-check steps for high-risk outputs
4. **Minimal interpretation**: "If ambiguous, choose simplest valid interpretation"
5. **Scope discipline**: "Implement EXACTLY and ONLY what requested"

### Verbosity Control (Critical)

| Context | Constraint | Example |
|---------|------------|---------|
| Simple yes/no | ≤2 sentences | "Answer in ≤2 sentences" |
| Default responses | 3-6 sentences or ≤5 bullets | "Respond in 3-6 sentences" |
| Complex tasks | 1 overview + ≤5 tagged bullets | "Overview + bullets: What, Where, Risk, Next, Open" |
| Long-form content | Explicit word/section limits | "≤500 words, 3 sections max" |
| Enterprise/coding agents | Strict limits | "Default ≤5 bullets, simple ≤2 sentences" |

### Scope Discipline (Critical)

**Prevent feature creep with explicit constraints:**

```markdown
# REQUIRED scope constraints
- Implement EXACTLY and ONLY what requested
- Do NOT add: extra features, uncontrolled styling, new UI elements
- Do NOT invent elements not in requirements
- Do NOT expand problem surface area
- Respect design system constraints
```

| Check | Requirement | Severity |
|-------|-------------|----------|
| Explicit "do not" list | Forbidden actions listed | Severe |
| Scope boundaries | What IS and IS NOT in scope | Severe |
| Feature creep prevention | "Only what requested" | Warning |
| Design system respect | No uncontrolled additions | Warning |

### Long-Context Handling (>10k tokens)

| Step | Action | Purpose |
|------|--------|---------|
| 1 | Produce internal outline of key sections | Navigate large input |
| 2 | Re-state user constraints before answering | Prevent drift |
| 3 | Anchor claims to specific sections with quotes | Grounding |
| 4 | Break into phases if necessary | Manage complexity |

### Ambiguity & Hallucination Prevention

| Strategy | Implementation | Severity |
|----------|----------------|----------|
| Clarification | Ask 1-3 precise questions OR present 2-3 interpretations with assumption labels | Warning |
| Hedging | "Based on the provided context..." | Warning |
| No fabrication | Never fabricate exact figures, line numbers, external references | Severe |
| Missing data | Set missing fields to null rather than guessing | Warning |
| Grounding | Reference specific sections/quotes | Warning |
| Uncertainty | Use general terms when specifics may have changed | Info |

### High-Risk Self-Check

**For legal, financial, compliance, or security-sensitive content:**

```markdown
Before outputting, re-scan answer for:
- Unstated assumptions
- Ungrounded specific numbers
- Overstatements or absolute claims
- Missing caveats or disclaimers
```

| Check | Requirement | Severity |
|-------|-------------|----------|
| Self-check instruction | Present for high-risk domains | Warning |
| Assumption disclosure | Unstated assumptions flagged | Warning |
| Grounded specifics | No fabricated numbers | Severe |
| Appropriate hedging | No overstatements | Warning |

### Tool Usage Guidelines

| Guideline | Severity |
|-----------|----------|
| Prefer tools over internal knowledge for fresh/user-specific data | Warning |
| Parallelize independent read operations | Info |
| After writes, restate: what changed, where, validation performed | Warning |
| Explicit tool selection criteria | Info |

### Agentic Updates

| Rule | Requirement | Severity |
|------|-------------|----------|
| Brief updates | 1-2 sentences only | Warning |
| Major phases only | Not routine tool calls | Warning |
| Concrete outcomes | Each update has specific result | Warning |
| No narration | Avoid "thinking out loud" | Info |
| No task expansion | Do NOT expand beyond user request; flag optional work | Severe |
| No rephrasing | Do NOT rephrase user's request unless it changes semantics | Warning |

### Structured Extraction

| Check | Requirement | Severity |
|-------|-------------|----------|
| Schema provided | Always provide JSON shape/structure | Severe |
| Field distinction | Required vs optional marked | Warning |
| Null handling | Missing → null, not guessed | Warning |
| Array bounds | Min/max items specified | Info |
| Re-scan before return | Check for missed fields | Info |
| Multi-doc extraction | Serialize by document with stable IDs | Info |

### Freedom Level Matching

| Task Type | Freedom | Constraint Style | Issue if Mismatch |
|-----------|---------|------------------|-------------------|
| Creative/flexible | High | Guidelines only | Warning if over-constrained |
| Code generation | Medium | Patterns + flexibility | Warning if too rigid |
| Data extraction | Low | Strict schema | Severe if unstructured |
| Safety-critical | Very Low | Explicit scripts | Severe if too loose |

### Web Search & Research Rules (GPT-5.2)

> **Source**: GPT-5.2 Prompting Guide - Comprehensive Web Research Agent specification
>
> **Applies to**: Prompts that involve web search, research, or information gathering

#### Factuality Requirements (Non-Negotiable)

| Scenario | Requirement | Severity |
|----------|-------------|----------|
| Time-sensitive topics | MUST browse web (news, prices, laws, product specs, rankings) | Severe |
| Updated/niche topics | MUST browse (weather, exchange rates, standards, software libraries) | Severe |
| Travel/recommendations | MUST browse for current information | Warning |
| Uncertain terminology | MUST browse to verify | Warning |
| News queries | Prioritize recent events; compare publish dates explicitly | Warning |

#### Citation Requirements

| Check | Requirement | Severity |
|-------|-------------|----------|
| Citations present | Required after each paragraph with web-derived claims | Severe |
| No fabricated citations | Never invent citations | Severe |
| Multiple sources | Use multiple sources for key claims | Warning |
| Primary sources | Prioritize primary sources and quality outlets | Warning |

#### Research Methodology

| Check | Requirement | Severity |
|-------|-------------|----------|
| Multiple targeted searches | Start with multiple searches; use parallel when helpful | Warning |
| Follow-up searches | Add targeted follow-ups to fill gaps, resolve disagreements | Warning |
| Recent updates check | Check for recent updates on time-sensitive topics | Warning |
| Sufficient coverage | Gather sufficient coverage for comparisons and tradeoffs | Warning |
| Continue until complete | Iterate until additional searching unlikely to change answer | Warning |
| Evidence-based | If evidence thin, continue searching rather than guessing | Severe |

**Stop conditions** (all must be true):
- User's question and every subpart answered
- Concrete examples and high-value adjacent material found
- Sufficient sources for core claims located

#### Writing Guidelines (Research Output)

| Check | Requirement | Severity |
|-------|-------------|----------|
| Direct start | Start answering immediately, no preamble | Warning |
| Comprehensive | Answer every query part; detailed unless simplistic request | Warning |
| Simple language | Full sentences, short words, concrete verbs, active voice | Info |
| Readable formatting | Markdown, section labels, bullets, tables for comparisons | Warning |
| No follow-up questions | Do NOT add follow-up questions unless explicitly requested | Warning |

#### Value-Add Behavior

| Check | Requirement | Severity |
|-------|-------------|----------|
| Concrete examples | Named entities, mechanisms, case examples, specific numbers/dates | Warning |
| Not overly brief | Include relevant, well-sourced material supporting user goals | Warning |
| Adjacent material | Add adjacent well-researched material when it helps | Info |
| Completeness pass | Answer all subparts, include explanation + concrete detail | Warning |

#### Handling Inability to Comply

| Check | Requirement | Severity |
|-------|-------------|----------|
| No blunt refusal | Don't lead with refusal if partial help available | Warning |
| Deliver what's possible | First deliver what's safe and possible | Warning |
| State limitations | Clearly state limitations after delivering help | Warning |
| Suggest next steps | If unverifiable, explain what was verified, suggest next steps | Info |

---

## Prompt Compliance Checks

> **Execution Required**: For prompts targeting modern LLMs (GPT-5+, Claude, Gemini, etc.), verify these checks.

### XML Structure Enforcement (GPT-5.2 MANDATORY)

> **Source**: GPT-5.2 Prompting Guide - XML tags are the recommended method to enforce output structure.
>
> **CRITICAL**: This is a **strict audit rule**. Prompts without XML tags for critical constraints will experience format drift in multi-turn/agentic scenarios.

| Check | Requirement | Severity |
|-------|-------------|----------|
| Has XML tags for verbosity | `<output_verbosity_spec>` wraps length constraints | Severe |
| Has XML tags for scope | `<design_and_scope_constraints>` wraps boundaries | Severe |
| Has XML tags for extraction | `<extraction_spec>` wraps schema (if extraction task) | Severe |
| Has XML tags for updates | `<user_updates_spec>` wraps agent communication rules (if agentic) | Severe |
| Has XML tags for uncertainty | `<uncertainty_and_ambiguity>` wraps hallucination prevention (if factual) | Severe |
| Has XML tags for tools | `<tool_usage_rules>` wraps tool invocation rules (if tool-using) | Warning |
| Has XML tags for long-context | `<long_context_handling>` wraps recall rules (if >10k tokens) | Warning |
| Has XML tags for self-check | `<high_risk_self_check>` wraps validation (if high-risk) | Warning |

**Audit execution**:
1. Identify prompt type: agentic, extraction, factual, tool-using, long-context, high-risk
2. For each applicable type, check if corresponding XML tags are present
3. If XML tags missing → Flag with severity per table above
4. **Exception**: Simple single-turn prompts without structured output may skip XML tags

**Example of proper XML structure**:
```xml
<output_verbosity_spec>
Default: 3-6 sentences or ≤5 bullets.
Simple questions: ≤2 sentences.
Complex tasks: 1 overview + ≤5 tagged bullets.
</output_verbosity_spec>

<design_and_scope_constraints>
Implement EXACTLY and ONLY what requested.
Do NOT add: extra features, uncontrolled styling, new UI elements.
</design_and_scope_constraints>

<uncertainty_and_ambiguity>
If unclear: provide 1-3 clarifying questions OR 2-3 interpretations with assumption labels.
Never fabricate exact figures, line numbers, or external references.
</uncertainty_and_ambiguity>
```

### Verbosity Compliance

| Check | Requirement | Severity |
|-------|-------------|----------|
| Has explicit length limit | "≤N sentences/bullets/words" | Severe |
| Default verbosity defined | What to do without specific request | Warning |
| Complex task structure | Tagged bullets for multi-part | Info |

### Scope Compliance

| Check | Requirement | Severity |
|-------|-------------|----------|
| Has "do not" constraints | Explicit forbidden actions | Severe |
| Scope boundaries clear | What IS and IS NOT in scope | Severe |
| Feature creep prevention | "Only what requested" or equivalent | Warning |

### Grounding Compliance

| Check | Requirement | Severity |
|-------|-------------|----------|
| No absolute claims | Uses hedging language | Warning |
| No fabrication instruction | "Never fabricate..." | Severe |
| Context anchoring | "Based on provided context" | Warning |

### Self-Check Compliance (High-Risk Only)

| Check | Requirement | Severity |
|-------|-------------|----------|
| Has verification step | Re-scan instruction | Warning |
| Assumption check | Flag unstated assumptions | Info |
| Overstatement check | Avoid absolute claims | Info |

### Output Format Compliance

| Check | Requirement | Severity |
|-------|-------------|----------|
| Schema provided | JSON structure or format spec | Warning |
| Required/optional marked | Field requirements clear | Info |
| Null handling defined | What to do with missing data | Info |

---

## LLM-Specific Warnings

> **Source**: Latest troubleshooting and optimization guides from [openai-cookbook/examples/gpt-5](https://github.com/openai/openai-cookbook/tree/main/examples/gpt-5)

### Official Warnings (From Troubleshooting Guide)

| Issue | Official Warning | Severity |
|-------|-----------------|----------|
| Filler phrases | Modern LLMs treat "Take a deep breath", "You are a world-class expert" as noise | Warning |
| Contradictory instructions | More damaging to reasoning models (wastes reasoning tokens reconciling) | Severe |
| No clear completion definition | Causes overthinking - model keeps exploring without stop condition | Warning |
| Maximize language | "Analyze everything", "Be thorough" causes over-tool-calling | Warning |
| Overly deferential | In agentic settings, may need persistence instructions | Warning |

### API Parameters Reference

> **Note**: When prompts include parameter recommendations, verify against official values from the latest documentation.

| Parameter | Valid Values | Purpose |
|-----------|-------------|---------|
| reasoning_effort | none \| minimal \| low \| medium \| high \| xhigh | Controls thinking depth |
| verbosity | API parameter | Controls final answer length (separate from thinking) |

**GPT 5.2 Migration**:
- GPT-4o/4.1 → GPT-5.2: Use `reasoning_effort: none`
- GPT-5 → GPT-5.2: Keep same effort value
- GPT-5.1 → GPT-5.2: Keep existing choice

**Response Compression** (GPT 5.2): For long agentic workflows, use `/responses/compact` endpoint for multi-step workflows, long conversations, or iterative reasoning exceeding max context.

---

## Conversational/Multi-Phase Prompt Rules

> **Applies to**: Prompts with multiple phases, user interaction loops, or conditional execution.
> **Core principle**: AI tends to "help more" without explicit constraints. Multi-phase prompts need stronger control than single-turn prompts.
> **Source**: GPT-5 Prompting Guide - Scope Discipline & Verbosity Control

### Critical Checks

| Check | Why Critical | Severity |
|-------|--------------|----------|
| Critical constraints at TOP | Scattered rules get selectively followed | Severe |
| Explicit stop conditions | Vague stop language allows AI to continue | Severe |
| Scope drift prevention | AI tends to add unrequested features | Severe |
| Phase gate conditions | AI may skip phases without explicit triggers | Severe |
| Constraint centralization | Distributed rules = weaker enforcement | Severe |
| Stop condition strength | Soft vs strong stop language | Severe |
| Prohibition language strength | Weak vs strong prohibition language | Warning |

### Key Principle

The root cause of multi-phase prompt failures is usually: **critical constraints buried in middle of document + soft prohibition language**.

**Fix approach**: Move critical constraints to a dedicated block at TOP, use strong prohibition language.

### Constraint Centralization Check

> **Source**: GPT-5 Guide - "Scope discipline: Implement EXACTLY and ONLY what requested"

**Why this matters**: When critical rules are scattered across a document, AI may:
- Selectively follow some rules while ignoring others
- Lose track of constraints as context grows
- Prioritize later instructions over earlier ones

| Pattern | Risk Level | Fix |
|---------|------------|-----|
| All critical rules in dedicated block at TOP | Low | Good |
| Critical rules in 2-3 locations | Medium | Consolidate |
| Critical rules scattered (>3 locations) | High | Must consolidate |
| Critical rules only at BOTTOM | Very High | Move to TOP |

**Audit execution**:
1. Identify all prohibition/constraint statements
2. Map their locations in document
3. If >3 locations → Flag as "Scattered constraints" (Severe)
4. If critical rules not in first 20% of document → Flag as "Constraints not at TOP" (Severe)

### Stop Condition Strength Check

> **Source**: GPT-5 Guide - "Explicit stop conditions prevent overthinking"

| Strength | GPT Guide Pattern | Effectiveness |
|----------|-------------------|---------------|
| Strong | Explicit stop + prohibition of continuation (e.g., "Stop here. Do NOT continue.") | High |
| Medium | Stop instruction without prohibition (e.g., "Stop and wait for user.") | Medium |
| Weak | Implicit wait or vague language (e.g., "then wait for...") | Low - AI may continue |
| None | No stop instruction | Very Low |

**Audit execution**:
1. For each phase transition, check if stop condition exists
2. Evaluate stop condition strength based on GPT Guide patterns
3. If Weak or None at critical gates → Flag as "Weak stop condition" (Severe)

### Length vs Control Paradox

> **Source**: GPT-5 Guide - "Verbosity constraints" + "Scope discipline"

**Critical insight**: Longer prompts ≠ better control. Often the opposite.

| Symptom | Likely Cause | Fix Priority |
|---------|--------------|--------------|
| Longer version has weaker enforcement | Removed centralized rules, added scattered content | Restore centralized block |
| More detailed but less compliant | Diluted critical constraints with explanations | DELETE explanations, keep constraints |
| Added examples but lost control | Examples without constraints | Add constraints, not just examples |

**Audit execution**:
1. If auditing a "v2" or "updated" version, compare with original if available
2. Check if critical constraint blocks were removed or diluted
3. If constraints were scattered → Flag as "Constraint dilution" (Severe)

### Prohibition Language Audit

> **Source**: GPT-5 Guide - "Do NOT add: extra features, uncontrolled styling..."

| Strength | GPT Guide Pattern | When to Use |
|----------|-------------------|-------------|
| Strong | "Do NOT", "NEVER", "MUST NOT" | Critical constraints |
| Medium | "don't", "avoid", "should not" | Preferences |
| Weak | "try not to", "prefer not" | Suggestions only |
| None | Implicit expectation | Not for constraints |

**Audit execution**:
1. Extract all prohibition statements
2. Classify by strength based on GPT Guide patterns
3. If critical constraints use weak language → Flag as "Weak prohibition language" (Warning)
4. If no strong prohibitions for scope control → Flag as "Missing scope constraints" (Severe)

---

## Common Issues

### Should Flag

> **Pre-Check**: Before flagging, verify that the issue cannot be resolved by AI inference from existing examples/context.

| Issue | Severity | Principle | Pre-Check |
|-------|----------|-----------|-----------|
| Contradictory instructions | Fatal | - | Always flag |
| Impossible constraints | Fatal | - | Always flag |
| Missing critical context | Fatal | - | Always flag |
| No verbosity guidance AND no demonstrative examples | Severe | Verbosity Control | Only if AI cannot infer from examples |
| No scope indication AND no contextual boundaries | Severe | Scope Discipline | Only if AI cannot infer from context |
| No "do not" constraints AND ambiguous scope | Severe | Scope Discipline | Only if AI cannot infer boundaries |
| Ambiguous output format for structured tasks | Severe | Structured Extraction | Check if examples show format |
| No error handling instructions | Severe | - | Check if obvious from context |
| Fabrication allowed (no grounding) | Severe | Hallucination Prevention | Always flag for factual tasks |
| Vague instructions ("do it well") | Warning | Explicit over Implicit | Check if examples clarify |
| Missing examples for complex tasks | Warning | - | Only if truly complex |
| No hedging guidance for uncertain cases | Warning | Grounding | Check context |
| Overly long without structure | Warning | Long-Context Handling | - |
| No self-check for high-risk content | Warning | High-Risk Self-Check | - |
| Absolute claims without hedging | Warning | Grounding | - |

### Should NOT Flag

| Pattern | Reason |
|---------|--------|
| Simple prompts without constraints | Not needed for simple tasks |
| Style preferences | Design choice |
| Reasonable interpretation choices | Valid |
| Missing optional elements | Optional |
| No self-check for low-risk content | Not required |
| **No explicit constraints BUT demonstrative examples exist** | AI can infer from examples |
| **No explicit rules BUT context clearly implies behavior** | AI capability - can infer from context |
| **Original design conveys intent through structure/examples** | Redundant to add explicit rules |

---

## Audit Checklist

### Fatal
- [ ] No contradictory instructions
- [ ] No impossible constraints
- [ ] Critical context present

### Severe (Critical)
- [ ] Verbosity constraints specified (explicit length limits)
- [ ] Scope boundaries defined (what IS and IS NOT in scope)
- [ ] "Do not" constraints present (forbidden actions)
- [ ] Output format clear (schema for structured tasks)
- [ ] No fabrication instruction (grounding)
- [ ] Error handling addressed
- [ ] **XML tags for verbosity** (`<output_verbosity_spec>`) - GPT-5.2+
- [ ] **XML tags for scope** (`<design_and_scope_constraints>`) - GPT-5.2+
- [ ] **XML tags for extraction** (`<extraction_spec>`) - if extraction task
- [ ] **XML tags for updates** (`<user_updates_spec>`) - if agentic/multi-phase
- [ ] **XML tags for uncertainty** (`<uncertainty_and_ambiguity>`) - if factual task

### Warnings
- [ ] Instructions are specific, not vague
- [ ] Examples provided for complex tasks
- [ ] Hedging guidance for uncertain cases
- [ ] Well-structured if long (outline for >10k tokens)
- [ ] Self-check for high-risk content
- [ ] No absolute claims without hedging
- [ ] XML tags for tools (`<tool_usage_rules>`) - if tool-using
- [ ] XML tags for long-context (`<long_context_handling>`) - if >10k tokens
- [ ] XML tags for self-check (`<high_risk_self_check>`) - if high-risk

### Info
- [ ] Could benefit from more examples
- [ ] Could add self-check steps
- [ ] Could specify output more precisely
- [ ] Could add tagged bullets for complex tasks
