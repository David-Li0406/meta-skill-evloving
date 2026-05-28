# Universal Audit Rules

> **Dual Application**: These rules serve as both:
> 1. **Audit standards** for checking other skills
> 2. **Quality standards** that audited content should follow
>
> Key principles audited content should follow: AI Executor Awareness, Conciseness, LLM Wording Patterns, and necessity-based content (see `methodology-core.md`).

## Table of Contents

- [AI Executor Awareness](#ai-executor-awareness)
- [Content-Based Audit Principle](#content-based-audit-principle)
- [Universal Prompt Quality Rules](#universal-prompt-quality-rules)
- [Universal Size Thresholds](#universal-size-thresholds)
- [Universal Format Rules](#universal-format-rules)
- [Internationalization Rules](#internationalization-rules)
- [Universal Should Flag](#universal-should-flag)
- [Universal Should NOT Flag](#universal-should-not-flag)

---

## AI Executor Awareness

> **Rationale**: See `methodology-core.md` → AI Capability Model

### Core Principle

AI executors have contextual understanding and can infer from common sense and context.

### Audit Checks

| Check | Guideline | Severity |
|-------|-----------|----------|
| Avoid over-specification | Don't specify what AI can infer | Warning |
| Trust AI judgment | Guidelines over rigid rules for flexible tasks | Info |
| No redundant explanations | Don't explain concepts AI already knows | Warning |

**Threshold**: If <30% would misunderstand → AI can handle it, don't flag.

---

## Content-Based Audit Principle

**Audit is based on CONTENT user provides, NOT limited to specific system paths.**

User may:
- Provide files copied to any location for review
- Paste content directly
- Point to any directory structure

**Focus on**: Content quality itself
**Path/location checks**: Informational only (marked as "Info (advisory)")

---

## Universal Prompt Quality Rules

> **Execution Required**: For ALL content containing AI instructions, verify each check below.
> **Detailed guidance**: See `type-prompt.md` → LLM Prompting Best Practices
> **Dynamic Verification**: Execute Step 0 in SKILL.md to fetch and cross-validate against latest GPT guides.

**Applies to**: Prompts, Memory files, Skill bodies, Command bodies, Agent bodies, Hook prompts

### Pre-Check: Intent Already Conveyed?

**CRITICAL**: Before flagging any "missing" element, first verify if the intent is already conveyed:

| Check | Question | If YES → | If NO → |
|-------|----------|----------|---------|
| Demonstrative examples | Does the content have examples that imply the expected behavior/format? | NOT an issue (AI can infer) | Continue to rule check |
| Contextual clarity | Can AI infer the expected behavior from surrounding context? | NOT an issue (AI capability) | Continue to rule check |
| Threshold test | Would <30% misunderstand without explicit constraint? | NOT an issue (below threshold) | Continue to rule check |

**Only flag as issue if ALL pre-checks answer NO.**

### LLM Prompting Best Practices

| Check | Requirement | Severity | Applies To | Pre-Check |
|-------|-------------|----------|------------|-----------|
| Verbosity constraints | Output length guidance (explicit limits OR demonstrative examples) | Severe only if AI cannot infer | All prompts | Check if examples imply length |
| Scope boundaries | Boundaries conveyed (explicit "do not" OR clear context) | Severe only if AI cannot infer | All instructions | Check if context implies scope |
| No fabrication | "Never fabricate..." instruction for factual content | Severe | Data extraction | Always required for factual tasks |
| Ambiguity handling | Instructions for unclear cases (clarify OR interpret) | Warning | Complex tasks | - |
| No AI-known content | Don't explain standard concepts | Warning | All | - |
| Grounding | "Based on context" for uncertain claims | Warning | Data extraction | - |
| Self-check | Verification step for high-risk outputs | Warning | Legal/financial/security | - |
| Output schema | JSON structure or format specification | Warning | Structured output | Check if examples show format |
| Tool preference | Prefer tools over internal knowledge for fresh/user-specific data | Warning | Tool-using content | - |
| Tool parallelization | Parallelize independent read operations | Info | Tool-using content | - |
| Write confirmation | After writes, restate: what changed, where, validation performed | Warning | Tool-using content | - |
| Agentic updates | Brief updates (1-2 sentences) at major phases only, concrete outcomes | Warning | Agent/agentic content | - |
| No task expansion | Don't expand beyond user request; flag optional work | Warning | Agent/agentic content | - |
| Long-context outline | For >10k tokens: internal outline, constraint restatement, section refs with quotes | Warning | Long content | - |
| Structured null handling | Missing fields → null, not guessed; re-scan before return | Warning | Structured output | - |

### Freedom Level Matching

| Task Type | Expected Constraint Level | Issue if Mismatch |
|-----------|---------------------------|-------------------|
| Fragile/deterministic ops | Specific scripts | Severe if too loose |
| Data extraction | Strict schema | Severe if unstructured |
| Creative/flexible tasks | Guidelines only | Warning if over-constrained |
| Code generation | Patterns + flexibility | Warning if too rigid |
| Conversational/multi-phase | Strong constraints + explicit gates | Severe if rules scattered or gates missing |

> **Note**: For conversational/multi-phase content, see `type-prompt.md` → Conversational/Multi-Phase Prompt Rules for detailed checks.

### Conciseness Principle

| Check | Requirement | Severity |
|-------|-------------|----------|
| Single source of truth | Info in ONE place only | Warning |
| No duplication | Not in body AND references | Warning |
| Prefer examples | Over lengthy explanations | Info |
| Remove AI-known | Don't explain common concepts | Warning |

### Trigger Condition Placement

| Content Type | Trigger Location | Body Contains |
|--------------|------------------|---------------|
| Skill | description field | Implementation |
| Agent | description field | Instructions |
| Command | description field | Task instructions |
| Hook | matcher config | Action logic |

**Issue**: Trigger conditions in body instead of description → Severe

---

## Numbering & Order Rules

> **Execution Required**: Extract actual numbers from content and verify.

### Numbering Validation

| Check | Requirement | Severity |
|-------|-------------|----------|
| Sequential numbering | No gaps (1,2,3 not 1,2,4) | Warning |
| Consistent format | Same style (R1/R2 OR 1.1/1.2) | Warning |
| Referenced numbers exist | All referenced R1, Step 2 etc. exist | Severe |
| No duplicate numbers | Each number used once | Warning |
| Hierarchical consistency | 1.1, 1.2 under section 1 | Warning |

### Order Validation

| Check | Requirement | Severity |
|-------|-------------|----------|
| Section order logical | Prerequisites before dependents | Warning |
| Heading hierarchy | H1→H2→H3 (no skipping) | Warning |
| TOC matches content | TOC order = section order | Warning |
| Priority order | High priority items first | Info |
| Chronological flow | Steps in execution order | Warning |

---

## Reference Integrity Rules

> **Execution Required**: Extract ALL references from content (file refs, anchor links, numbered refs) and verify each exists.

### Reference Accuracy

| Check | Requirement | Severity |
|-------|-------------|----------|
| Named references exist | All `@file`, `skill-name` exist | Severe |
| Numbered references exist | All R1, Step 2, etc. defined | Severe |
| Anchor links valid | All #section-name anchors resolve | Warning |
| Cross-file refs valid | References to other files exist | Severe |
| No orphan references | No undefined references | Warning |

### Reference Consistency

| Check | Requirement | Severity |
|-------|-------------|----------|
| Same ref = same format | Consistent reference style | Warning |
| Bidirectional integrity | If A refs B, B should ref A (if needed) | Info |
| No circular references | A→B→C→A pattern | Fatal |
| No conflicting references | Same name != different targets | Severe |

---

## Diagram & Flowchart Rules

> **Execution Required**: If diagrams exist, verify each node has text description and all paths have endpoints.

### Directory Tree Verification

Before reporting "tree incomplete" or "missing files": re-read and fully parse the tree structure to confirm. ASCII tree characters can cause parsing errors on first scan.

### Diagram-Text Consistency

| Check | Requirement | Severity |
|-------|-------------|----------|
| Node names match text | Diagram nodes = text descriptions | Severe |
| Flow paths match rules | Diagram paths = documented flow | Severe |
| All paths documented | Every diagram path has description | Warning |
| No undocumented nodes | Every node explained | Warning |
| Conditions match | Decision conditions consistent | Severe |

### Flowchart Logic Validation

| Check | Requirement | Severity |
|-------|-------------|----------|
| All paths have endpoints | No hanging branches | Fatal |
| No infinite loops | All loops have exit conditions | Fatal |
| Decision completeness | All decision branches handled | Severe |
| Start/end nodes present | Clear entry and exit points | Warning |
| Consistent notation | Same symbols throughout | Info |

### Mermaid/Diagram Syntax

| Check | Requirement | Severity |
|-------|-------------|----------|
| Valid syntax | Renders without error | Severe |
| Node IDs match references | Referenced nodes exist | Severe |
| Edge labels clear | Conditions readable | Info |

---

## Language Expression Rules

> **Execution Required**: Scan for ambiguity patterns listed below. Flag if found without condition/context.

### Clarity & Precision

| Check | Requirement | Severity |
|-------|-------------|----------|
| Clear wording | No ambiguous phrases | Warning |
| Fluent expression | Grammatically correct | Warning |
| No typos | Scan for spelling errors in identifiers, headings, key terms | Info |
| No redundancy | No unnecessary repetition | Warning |
| Consistent verb tense | Same tense throughout | Info |

### Ambiguity Detection

| Check | Requirement | Severity |
|-------|-------------|----------|
| Vague quantifiers/timing | Must be specific or have context | Warning |
| Undefined criteria | "appropriate/suitable" needs definition | Warning |
| Incomplete enumerations | "etc." should have examples or be exhaustive | Info |

### Terminology Consistency

| Check | Requirement | Severity |
|-------|-------------|----------|
| Same concept = same term | One term per concept | Warning |
| Defined domain terms | Technical terms explained | Info |
| Consistent verb forms | Same verbs for same actions | Warning |
| Consistent formatting | Same style for same elements | Warning |

### Wording Patterns (LLM Best Practices)

> **Source**: Latest GPT Prompting Guide from [openai-cookbook/examples/gpt-5](https://github.com/openai/openai-cookbook/tree/main/examples/gpt-5)
>
> **Version Policy**: Always use the **latest version** as authoritative source. When multiple versions exist, prefer the highest version number (e.g., gpt-5.2 over gpt-5.1 over gpt-5).

#### Recommended Wording Patterns (from GPT Guide)

| Pattern | GPT Guide Recommended Wording | Purpose | Severity if Missing |
|---------|-------------------------------|---------|---------------------|
| Verbosity constraint | "≤N sentences", "≤N bullets", "≤N words" | Explicit length control | Warning |
| Scope constraint | "EXACTLY and ONLY what requested" | Prevent feature creep | Warning |
| Prohibition list | "Do NOT: [specific items]" | Clear boundaries | Warning |
| Context grounding | "Based on provided context" | Prevent hallucination | Warning |
| No fabrication | "Never fabricate exact figures, line numbers, or external references" | Factual accuracy | Severe |
| Ambiguity handling | "1-3 clarifying questions OR 2-3 interpretations with assumption labels" | Handle uncertainty | Warning |
| Completion definition | Explicit stop condition or "done when" criteria | Prevent overthinking | Warning |
| Strong stop condition | Explicit stop + prohibition of continuation | Enforce phase gates | Severe |
| Centralized constraints | All critical rules in dedicated block at TOP | Prevent selective compliance | Severe |

#### XML Tags for Structured Output (GPT-5.2 MANDATORY)

> **Source**: GPT-5.2 Prompting Guide - XML tags enforce output structure and prevent format drift in agentic/multi-turn scenarios.

**CRITICAL**: For prompts targeting GPT-5+ or agentic workflows, XML tags are the **recommended method** to enforce output structure. Without XML tags, output format compliance degrades significantly in multi-turn conversations.

| XML Tag | Purpose | When Required | Severity if Missing |
|---------|---------|---------------|---------------------|
| `<output_verbosity_spec>` | Controls length and format | All prompts with verbosity requirements | Severe |
| `<design_and_scope_constraints>` | Prevents feature creep | All prompts with scope boundaries | Severe |
| `<long_context_handling>` | Improves recall on dense inputs | Prompts handling >10k tokens | Warning |
| `<uncertainty_and_ambiguity>` | Mitigates hallucination | Factual/extraction tasks | Severe |
| `<high_risk_self_check>` | Pre-finalization validation | Legal/financial/security content | Warning |
| `<user_updates_spec>` | Structures agent communication | Agentic/multi-phase prompts | Severe |
| `<tool_usage_rules>` | Governs tool invocation | Tool-using prompts | Warning |
| `<extraction_spec>` | Enforces structured data output | Data extraction tasks | Severe |
| `<web_search_rules>` | Directs research behavior | Research/search tasks | Warning |

**Audit execution**:
1. Check if prompt has structured output requirements
2. If YES → Verify XML tags are used to enforce structure
3. If XML tags missing for critical constraints → Flag as "Missing XML structure enforcement" (Severe)
4. For agentic/multi-phase prompts without XML tags → Flag as "Format drift risk" (Severe)

#### GPT-5.2 Behavioral Characteristics (Audit Awareness)

> **Source**: GPT-5.2 Prompting Guide - Key Behavioral Differences

**When auditing prompts for GPT-5.2+, be aware of these characteristics:**

| Characteristic | Implication for Audit | Severity if Not Addressed |
|----------------|----------------------|---------------------------|
| More deliberate scaffolding | Benefits from explicit scope and verbosity constraints | Severe if missing |
| Generally lower verbosity | More concise by default; still needs explicit preferences | Warning |
| Stronger instruction adherence | Less drift from user intent; improved formatting | Info (positive) |
| Tool efficiency trade-offs | May take additional tool actions; optimize via prompting | Warning |
| Conservative grounding bias | Favors correctness; ambiguity handling improves with clarification prompts | Warning |

**Audit checks for GPT-5.2 optimization:**

| Check | Requirement | Severity |
|-------|-------------|----------|
| Explicit preferences | Articulate style preferences clearly (don't assume AI knows) | Warning |
| Design system exploration | Include "Explore existing design systems" instruction | Warning |
| No task expansion | Include "Do NOT expand beyond user request" | Severe |
| No rephrasing | Include "Do NOT rephrase user's request unless semantics change" | Warning |
| Style alignment | Include "Style aligned to design system at hand" | Warning |

#### Wording Anti-Patterns (GPT Guide Official Warnings)

| Anti-Pattern | Examples | Why Problematic | Severity |
|--------------|----------|-----------------|----------|
| Filler phrases | "Take a deep breath", "You are a world-class expert" | Modern LLMs treat as noise | Warning |
| Vague verbosity | "Be concise", "Keep it short" | No measurable constraint | Warning |
| Absolute claims | "Always", "Never", "Guaranteed" (without qualification) | Lacks grounding | Warning |
| Maximize language | "Analyze everything", "Be thorough" | Causes overthinking/over-tool-calling | Warning |
| Contradictory instructions | Conflicting rules in same prompt | Reasoning models waste tokens reconciling | Severe |
| Scattered constraints | Critical rules in >3 locations | Selectively followed, weaker enforcement | Severe |
| Weak prohibition language | Soft language for critical constraints | Less effective than strong prohibitions | Warning |
| Soft stop conditions | Vague wait language without explicit stop | AI may continue despite instruction | Warning |

**Audit approach**: Check if instructions use GPT Guide recommended wording patterns. Flag when vague, absolute, or anti-pattern language is used where qualified language is appropriate.

---

## Security & Compliance Rules

> **Execution Required**: Search for hardcoded paths, secrets, API keys. Check scripts for injection vulnerabilities.

### Security Checks

| Check | Requirement | Severity |
|-------|-------------|----------|
| No hardcoded secrets | Use env variables | Severe |
| No exposed credentials | API keys, passwords protected | Severe |
| Path traversal prevention | Sanitize file paths | Severe |
| Input validation rules | Validate user input | Warning |
| Command injection prevention | Sanitize shell inputs | Severe |

### Compliance Checks

| Check | Requirement | Severity |
|-------|-------------|----------|
| Data handling rules | Privacy requirements documented | Warning |
| Error disclosure | No sensitive info in errors | Warning |
| Audit trail | Actions logged appropriately | Info |
| Access control | Permissions documented | Warning |

---

## Structure & Organization Rules

> **Execution Required**: Verify TOC-content match by comparing actual entries.

### Section Structure

| Check | Requirement | Severity |
|-------|-------------|----------|
| TOC present (>100 lines) | Table of contents for navigation | Info |
| TOC-content match | Every TOC entry has corresponding heading | Warning |
| Logical grouping | Related content together | Warning |
| Clear boundaries | Sections clearly separated | Info |
| No orphan sections | All sections integrated | Warning |

### Rule Organization

| Check | Requirement | Severity |
|-------|-------------|----------|
| Single source of truth | Rule defined in one place | Warning |
| No scattered rules | Same rule not in >3 files | Warning |
| No semantic duplicates | No rules with same meaning but different wording | Warning |
| Proper categorization | Rules in correct sections | Warning |
| Level-appropriate | Global vs local rules correct | Warning |

### Template Compliance

| Check | Requirement | Severity |
|-------|-------------|----------|
| Required sections present | All mandatory sections exist | Severe |
| Section order correct | Sections in expected order | Warning |
| Consistent formatting | Same format across similar files | Warning |

---

## Universal Size Thresholds

> Based on official Agent Skills specification (agentskills.io/specification)

### SKILL.md Body (Official Requirement)

| Range | Status | Severity |
|-------|--------|----------|
| ≤500 lines | Ideal | - |
| 500-550 (≤10% over) | **NOT an issue** | - |
| 550-625 (10-25% over) | Info only | Info |
| >625 lines | Should optimize | Warning |

> **Source**: "Keep your main `SKILL.md` under 500 lines. Move detailed reference material to separate files."

### Reference Files (No Official Limit)

**Official guidance**: "Keep individual reference files focused. Agents load these on demand, so smaller files mean less use of context."

**Audit approach**: No hardcoded line limit. Evaluate based on content nature:
- Does content have indivisible integrity? (e.g., professional knowledge that cannot be split without functional risk)
- Would splitting cause loading omissions?
- Is there obvious redundancy that can be trimmed?

**Only flag if**: Content has clear redundancy or can be split without functional impact.

### Component Summary

| Component | Limit | Notes |
|-----------|-------|-------|
| L1 Metadata | ~100 words | Permanent context cost |
| L2 Body (SKILL.md) | <500 lines | Official requirement |
| L3 References | **No limit** | Evaluate by content nature |
| L4 Scripts | No limit | Runtime only |

---

## Universal Format Rules

### Frontmatter Validation

| Field | Rule | Severity |
|-------|------|----------|
| Required fields | Must be present and non-empty | Fatal/Severe |
| name | kebab-case, appropriate length | Warning |
| description | Include trigger conditions, concise | Severe |
| Valid YAML | Parseable, correct syntax | Fatal |

### Markdown Structure

| Check | Rule | Severity |
|-------|------|----------|
| Heading hierarchy | H1→H2→H3 (no skipping) | Warning |
| Table format | Valid markdown tables | Warning |
| Code blocks | Proper language tags | Info |
| Links | Valid internal/external links | Warning |

### Naming Conventions

| Element | Convention | Severity |
|---------|------------|----------|
| Directories | kebab-case | Warning |
| Files | kebab-case (except SKILL.md) | Warning |
| No spaces | Use hyphens instead | Severe |
| No special chars | Letters, numbers, hyphens only | Severe |
| File encoding | UTF-8 without BOM | Warning |

---

## Internationalization Rules

### When i18n is Declared

**Applies when**: Content has any language/locale configuration

| Check | Guideline | Severity |
|-------|-----------|----------|
| No hardcoded user-facing text | Use variables/templates | Warning |
| No fixed language output examples | Use `{example_output}` placeholders | Warning |
| Language-agnostic rules | Rules shouldn't assume specific language | Info |
| BCP 47 language tags | Standard format like `zh-CN`, `en-US` | Warning |

### Hardcoded Content Exceptions

**Do NOT flag:**
- License/copyright notices
- Technical terms (API, JSON, etc.)
- Code examples showing syntax (not content)
- Variable/function names
- Log messages for debugging
- **Official documentation/specification/standard content** (API parameters, protocol values, format definitions)
- **Necessary prohibition rules** ("Do NOT" lists for scope control, security constraints)
- **Necessary clarifying examples** (when rule is ambiguous without example)

> **Key principle**: See `methodology-core.md` → "When ADD is Necessary" for full criteria.

---

## Universal Should Flag

### Fatal Issues (Blocks Execution)

- Contradictory rules (A vs NOT A) — **Warning**: Particularly damaging for modern reasoning models (wastes reasoning tokens attempting to reconcile)
- Impossible conditions
- Circular references (A→B→C→A)
- Missing required fields
- Invalid syntax (JSON, YAML, etc.)
- Referenced files/components don't exist

### Severe Issues (Major Impact)

- Hardcoded absolute paths (should use relative paths or environment variables)
- Missing trigger conditions in descriptions
- ≥60% executor error rate
- Core workflow in wrong location
- Security vulnerabilities (injection, secrets)
- Invalid tool/model/event names

### Warnings (Suboptimal)

- SKILL.md body >625 lines (applies to SKILL.md only, not references)
- Missing "when to read" for references
- Vague instructions ("do it well")
- Inconsistent terminology without explanation
- Missing error handling
- Non-kebab-case naming

### Info (Suggestions)

- SKILL.md body 550-625 lines (10-25% over)
- Could benefit from examples
- Minor style variations
- Optional fields missing
- Optimization opportunities

---

## Universal Should NOT Flag

### AI Inference Capability

**CRITICAL**: Do NOT flag as issues when AI can infer correct behavior:

| Pattern | Reason | Example |
|---------|--------|---------|
| No explicit constraints BUT demonstrative examples exist | AI can infer from examples | Examples show 3-5 bullet format → AI understands length expectation |
| No explicit rules BUT context clearly implies behavior | AI capability | "Engineering bid" context → AI understands data should come from provided materials |
| Original design conveys intent through structure/examples | Redundant to add explicit rules | Structured example output → implies format requirements |
| Placeholder patterns indicate expected behavior | AI understands placeholder semantics | `{{content from materials}}` → AI knows to extract, not fabricate |

### Size Tolerance

- ≤10% over recommended → **NOT an issue**
- 504/500 lines → **NOT an issue** (only 0.8% over)
- 520/500 lines → **NOT an issue** (only 4% over)

### Design Choices

- Different directory naming (commands/ vs cmds/)
- Different file organization
- Style variations within specification
- Platform-specific patterns (Claude vs Codex)
- Using different valid approaches

### Intentional Content

- License/copyright notices
- Brand identifiers
- Fixed header/footer in output
- Technical specifications
- Code examples demonstrating syntax

### AI Capability

- Content AI can infer from context
- Standard terminology without definition
- Common patterns without explanation
- Obvious constraints

### Optional Elements

- Missing optional fields
- Missing README.md
- Missing version field
- Additional helper directories

---

## Severity Decision Matrix

### Quick Reference

| Condition | Severity |
|-----------|----------|
| Cannot execute at all | Fatal |
| ≥60% serious errors | Severe |
| ≥3 conflicting interpretations | Severe |
| ≥40% misunderstand | Warning |
| ≥20% failure in common cases | Warning |
| ≥30% improvement possible, <10% cost | Info |
| <10% over recommended | NOT an issue |
| AI can infer | NOT an issue |
| Design choice | NOT an issue |

### Verification Questions

Before flagging ANY issue:

1. **Concrete impact?** Can you describe specific failure?
2. **In scope?** Within design boundaries?
3. **Flaw or choice?** Can find reasonable rationale?
4. **Meets threshold?** Above quantified threshold?

If ANY answer is NO → Discard the issue
