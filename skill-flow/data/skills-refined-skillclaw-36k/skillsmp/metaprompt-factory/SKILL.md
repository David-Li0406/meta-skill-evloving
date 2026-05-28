---
name: metaprompt-factory
description: This skill should be used when generating structured metaprompts for repeatable tasks. Triggers include "create a metaprompt for X", "generate a review prompt", "make a prompt template", or when building prompts for copilot, Codex, or other AI tools.
---

# metaprompt-factory

generate structured XML metaprompts for repeatable AI tasks. adapts to domain, enforces quality gates, cites sources.

## philosophy

> "a metaprompt is a reusable product spec for an AI worker"

| principle | application |
|-----------|-------------|
| make implicit explicit | encode assumptions, boundaries, constraints |
| separate data from instructions | use XML tags to delineate context vs directives |
| optimize for repeatability | generalize across similar tasks |
| source-grounded claims | cite official docs for technical claims |
| multishot > zero-shot | 3-5 diverse examples dramatically improve output |

## when to use

| use | skip |
|-----|------|
| repeatable AI tasks | one-off questions |
| copilot prompts | simple commands |
| Codex review prompts | ad-hoc exploration |
| PR audit templates | conversational tasks |
| domain-specific workflows | research queries |
| tasks needing structured output | free-form generation |

## decision tree: prompt structure

```
What kind of task?
├── Classification/Categorization
│   ├── Use multishot with 3-5 diverse examples
│   ├── Wrap examples in <example></example> tags
│   └── Include edge cases in examples
├── Analysis (code review, document review)
│   ├── Use XML to separate <document> from <instructions>
│   ├── Request structured output with specific sections
│   └── Add <output_format> tag with example structure
├── Generation (content, code)
│   ├── Define role/persona in system prompt
│   ├── Provide <formatting_example> for style
│   └── Use prefill to guide output structure
├── Multi-step reasoning
│   ├── Use chain-of-thought: <thinking> then <answer>
│   ├── Break into subtasks, chain prompts
│   └── Consider self-correction loop
└── Validation/Review
    ├── Generate → Review → Refine pattern
    ├── Use graded rubric (A-F or 1-10)
    └── Request specific improvement suggestions
```

## decision tree: complexity level

```
How complex is the task?
├── Simple (single transformation)
│   ├── Zero-shot or 1 example sufficient
│   ├── Direct instructions, minimal structure
│   └── ~50-100 tokens prompt
├── Moderate (multiple considerations)
│   ├── 3-5 multishot examples
│   ├── XML structure for clarity
│   ├── Explicit output format
│   └── ~200-500 tokens prompt
├── Complex (multi-step, high-stakes)
│   ├── Chain prompts (break into subtasks)
│   ├── Self-correction loop (generate → review → refine)
│   ├── Comprehensive examples with edge cases
│   └── ~500-1000+ tokens prompt
└── Autonomous (agent workflows)
    ├── Full XML structure with all sections
    ├── Failure modes documented
    ├── Verification steps included
    └── Tool integration specified
```

## concrete patterns (from Anthropic docs)

### XML tag patterns

| tag | purpose | source |
|-----|---------|--------|
| `<instructions>` | separate directives from data | [Use XML tags](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags) |
| `<example>` / `<examples>` | multishot learning | [Multishot prompting](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting) |
| `<document>` / `<data>` | input content | [Use XML tags](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags) |
| `<thinking>` | chain-of-thought reasoning | [Chain of thought](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought) |
| `<answer>` | final response after thinking | [Chain of thought](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought) |
| `<output_format>` | structure specification | [Use XML tags](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags) |
| `<formatting_example>` | style reference | [Use XML tags](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags) |
| `<feedback>` | review/critique content | [Chain complex prompts](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-prompts) |
| `<summary>` | condensed output | [Chain complex prompts](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-prompts) |

### multishot guidelines

| guideline | value | source |
|-----------|-------|--------|
| minimum examples | 3 | [Multishot prompting](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting) |
| recommended examples | 3-5 | [Multishot prompting](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting) |
| more examples = | better performance | [Multishot prompting](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting) |
| example qualities | relevant, diverse, clear | [Multishot prompting](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting) |

### chain prompt patterns

| pattern | use case | source |
|---------|----------|--------|
| content pipeline | Research → Outline → Draft → Edit → Format | [Chain complex prompts](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-prompts) |
| data processing | Extract → Transform → Analyze → Visualize | [Chain complex prompts](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-prompts) |
| decision making | Gather info → List options → Analyze → Recommend | [Chain complex prompts](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-prompts) |
| self-correction | Generate → Review → Refine → Re-review | [Chain complex prompts](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-prompts) |

## workflow

### 1. intake

gather minimal viable inputs:

```yaml
target_task: what the prompt should accomplish
domain: coding | review | ops | research | classification
outputs: expected deliverables (structured format)
tooling: copilot | codex | claude-api
```

### 2. classify complexity

use decision tree above to determine:
- simple → direct prompt
- moderate → XML structure + multishot
- complex → chained prompts
- autonomous → full metaprompt

### 3. select pattern

| domain | recommended pattern |
|--------|---------------------|
| code review | analysis + self-correction |
| classification | multishot (3-5 examples) |
| content generation | role + formatting_example |
| data extraction | XML structure + output_format |
| decision support | chain: gather → analyze → recommend |

### 4. structure metaprompt

```xml
<?xml version="1.0" encoding="UTF-8"?>
<metaprompt name="{name}" version="1.0">
  <role>
    <!-- who is the AI in this context? -->
  </role>

  <context>
    <!-- background, constraints, assumptions -->
  </context>

  <instructions>
    <!-- numbered steps, clear directives -->
  </instructions>

  <examples>
    <example>
      <input>...</input>
      <output>...</output>
    </example>
    <!-- 3-5 diverse examples -->
  </examples>

  <output_format>
    <!-- exact structure expected -->
  </output_format>

  <failure_modes>
    <!-- what can go wrong, how to handle -->
  </failure_modes>
</metaprompt>
```

### 5. parameterize

extract variables for reuse:

```xml
<parameters>
  <param name="document" type="string" required="true">
    The document to analyze
  </param>
  <param name="format" type="enum" values="json,yaml,text" default="json">
    Output format
  </param>
</parameters>
```

### 6. validate

check against rubric:

| dimension | check | pass criteria |
|-----------|-------|---------------|
| clarity | roles explicit, I/O unambiguous | no ambiguous pronouns |
| completeness | workflow + failure modes + output spec | all sections present |
| groundedness | technical claims cited or marked "proposed" | no phantom APIs |
| reusability | parameters cover variability | works across similar tasks |
| examples | 3-5 diverse, relevant examples | edge cases covered |

## tool integration

| tool | command | purpose |
|------|---------|---------|
| copilot | `copilot -p --model gemini-3-pro` | quick prompt validation |
| codex | `codex exec --model "gpt-5.2-codex xhigh"` | deep prompt execution |
| prompts | `prompts commands export /X` | load prompt templates |
| trails | `trails trail record` | prompt creation persistence |

### trails integration

persist prompt creation for pattern analysis:

```bash
# record prompt creation
trails trail record --agent claude --action completed \
  --task "metaprompt-factory: $PROMPT_NAME - $DOMAIN" \
  --confidence $CONFIDENCE --json -q
```

**trails enables**:
- tracking prompt patterns across domains
- measuring prompt quality over time
- correlating prompts with execution success

### copilot (consult-light)

```bash
cat <<'EOF' | copilot -p --model gemini-3-pro
<context>
{context_packet}
</context>

<instructions>
1. Analyze the provided context
2. Output structured JSON
</instructions>

<output_format>
{field: type, ...}
</output_format>
EOF
```

### codex (consult-deep)

```bash
cat <<'EOF' | codex exec --model "gpt-5.2-codex xhigh"
<role>
Senior code reviewer with expertise in {domain}
</role>

<document>
{code_or_document}
</document>

<instructions>
1. Review for {criteria}
2. Provide actionable feedback
3. Rate severity (high/medium/low)
</instructions>

<output_format>
{
  "issues": [...],
  "summary": "...",
  "score": 1-10
}
</output_format>
EOF
```

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| phantom specifics | inventing APIs, versions, paths | cite source or mark "proposed" |
| policy bloat | too many rules, loses clarity | prioritize top 3-5 rules |
| missing failure modes | no handling for errors | add explicit failure section |
| vague outputs | "generate a response" | specify exact structure with example |
| zero-shot complex tasks | poor accuracy on nuanced work | add 3-5 diverse examples |
| mixing data and instructions | Claude misinterprets boundaries | use XML tags to separate |
| undefined acronyms | confusion, inconsistency | spell out on first use |
| no edge cases in examples | fails on atypical inputs | include boundary examples |

## quality rubric

| dimension | weight | criteria |
|-----------|--------|----------|
| clarity | high | no ambiguous references, explicit I/O |
| examples | high | 3-5 diverse, relevant, edge cases |
| structure | medium | XML tags separate concerns |
| completeness | medium | all sections present |
| groundedness | medium | no invented APIs or paths |
| reusability | low | parameters enable variation |

**scoring:**
- 9-10: production-ready, comprehensive examples, handles edge cases
- 7-8: solid, minor gaps in examples or failure modes
- 5-6: functional but needs more examples or structure
- <5: needs significant rework

## references

- [references/xml-patterns.md](references/xml-patterns.md) - complete XML tag reference with examples
- [references/domain-templates.md](references/domain-templates.md) - templates for coding, review, ops, classification
- [references/chain-patterns.md](references/chain-patterns.md) - multi-step prompt chaining patterns
- [references/domain-modules.md](references/domain-modules.md) - domain-specific prompt modules
- [references/rubric.md](references/rubric.md) - quality scoring rubric
- [references/factory-template.xml](references/factory-template.xml) - base metaprompt template

## examples

### classification prompt

```xml
<role>
Customer feedback analyst for a B2B SaaS product.
</role>

<instructions>
Analyze feedback and categorize issues. Use categories:
UI/UX, Performance, Feature Request, Integration, Pricing, Other.
Rate sentiment (Positive/Neutral/Negative) and priority (High/Medium/Low).
</instructions>

<examples>
<example>
<input>The new dashboard is a mess! It takes forever to load, and I can't find the export button. Fix this ASAP!</input>
<output>
Category: UI/UX, Performance
Sentiment: Negative
Priority: High
</output>
</example>
<example>
<input>Love the Salesforce integration! But it'd be great if you could add Hubspot too.</input>
<output>
Category: Integration, Feature Request
Sentiment: Positive
Priority: Medium
</output>
</example>
</examples>

<data>
{{FEEDBACK}}
</data>
```

### code review prompt

```xml
<role>
Senior engineer reviewing pull request for security and performance.
</role>

<document>
{{PR_DIFF}}
</document>

<instructions>
1. Identify security vulnerabilities (OWASP top 10)
2. Flag performance concerns (N+1 queries, memory leaks)
3. Check for test coverage gaps
4. Rate each issue: severity (high/medium/low), effort (small/medium/large)
</instructions>

<output_format>
{
  "security_issues": [{"description": "", "severity": "", "line": 0}],
  "performance_issues": [{"description": "", "severity": "", "line": 0}],
  "test_gaps": [""],
  "overall_rating": "approve | request_changes | comment",
  "summary": ""
}
</output_format>
```
