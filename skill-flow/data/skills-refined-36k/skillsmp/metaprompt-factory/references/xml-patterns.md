# XML Tag Patterns for Metaprompts

comprehensive reference for structuring prompts with XML tags, based on Anthropic documentation.

## core principles

> "XML tags help Claude parse your prompts more accurately, leading to higher-quality outputs."
> — anthropic/use-xml-tags

| principle | application |
|-----------|-------------|
| consistency | use same tag names throughout, reference them explicitly |
| nesting | `<outer><inner></inner></outer>` for hierarchical content |
| semantic naming | tag names should describe their content |
| no canonical tags | any well-named tag works, no special training |

## standard tags

### input/data tags

```xml
<!-- raw document input -->
<document>
  content to analyze
</document>

<!-- structured data -->
<data>
  {"key": "value"}
</data>

<!-- multiple documents -->
<documents>
  <document id="1">first doc</document>
  <document id="2">second doc</document>
</documents>

<!-- reference material -->
<context>
  background information
</context>

<!-- user-provided content -->
<user_input>
  {{USER_MESSAGE}}
</user_input>
```

### instruction tags

```xml
<!-- primary directives -->
<instructions>
1. First, do X
2. Then, do Y
3. Finally, output Z
</instructions>

<!-- constraints/rules -->
<constraints>
- Must not exceed 500 words
- Must cite sources
- Must use formal tone
</constraints>

<!-- output specification -->
<output_format>
{
  "field1": "type",
  "field2": "type"
}
</output_format>
```

### example tags

```xml
<!-- single example -->
<example>
  <input>user question</input>
  <output>expected response</output>
</example>

<!-- multiple examples (multishot) -->
<examples>
  <example>
    <input>feedback: "App is slow"</input>
    <output>Category: Performance, Sentiment: Negative</output>
  </example>
  <example>
    <input>feedback: "Love the new feature!"</input>
    <output>Category: Feature, Sentiment: Positive</output>
  </example>
  <example>
    <input>feedback: "Pricing seems fair"</input>
    <output>Category: Pricing, Sentiment: Neutral</output>
  </example>
</examples>

<!-- formatting/style example -->
<formatting_example>
  # Q2 Report
  - Revenue: $X
  - Growth: Y%
</formatting_example>
```

### reasoning tags

```xml
<!-- chain-of-thought -->
<thinking>
  Let me analyze this step by step...
  1. First consideration
  2. Second consideration
  3. Conclusion
</thinking>

<answer>
  Final answer based on reasoning
</answer>

<!-- scratchpad for working -->
<scratchpad>
  intermediate calculations
</scratchpad>
```

### review/feedback tags

```xml
<!-- findings from analysis -->
<findings>
1. Issue A: description
2. Issue B: description
</findings>

<!-- recommendations -->
<recommendations>
1. Do X because Y
2. Consider Z for improvement
</recommendations>

<!-- feedback on work -->
<feedback>
  Accuracy: A
  Clarity: B+
  Completeness: B
</feedback>

<!-- summary -->
<summary>
  Brief overview of key points
</summary>
```

## composition patterns

### analysis prompt

```xml
<role>
Expert analyst in {domain}
</role>

<document>
{{CONTENT}}
</document>

<instructions>
1. Analyze for {criteria}
2. Identify {targets}
3. Rate {dimensions}
</instructions>

<output_format>
{structured output spec}
</output_format>
```

### classification prompt

```xml
<role>
{domain} classifier
</role>

<instructions>
Classify the input into: {categories}
Also rate: {additional_dimensions}
</instructions>

<examples>
{3-5 diverse examples covering edge cases}
</examples>

<data>
{{INPUT}}
</data>
```

### generation prompt

```xml
<role>
{persona} creating {content_type}
</role>

<context>
{background, audience, constraints}
</context>

<formatting_example>
{style reference}
</formatting_example>

<instructions>
Generate {output} following the style above.
</instructions>
```

### chain-of-thought prompt

```xml
<role>
{expert} solving {problem_type}
</role>

<problem>
{{PROBLEM}}
</problem>

<instructions>
Think through this step by step in <thinking> tags.
Then provide your final answer in <answer> tags.
</instructions>
```

## nesting patterns

### hierarchical data

```xml
<analysis>
  <section name="security">
    <finding severity="high">SQL injection in line 42</finding>
    <finding severity="medium">Missing input validation</finding>
  </section>
  <section name="performance">
    <finding severity="low">Unoptimized loop</finding>
  </section>
</analysis>
```

### conditional sections

```xml
<output>
  <required>
    always include this
  </required>
  <optional condition="has_errors">
    only include if errors found
  </optional>
</output>
```

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| inconsistent tags | `<doc>` then `<document>` | pick one, use consistently |
| unlabeled sections | mixing data with instructions | wrap each section in appropriate tag |
| deep nesting | `<a><b><c><d>` | flatten to 2-3 levels max |
| generic names | `<data1>`, `<data2>` | use semantic names: `<user_data>`, `<product_data>` |
| missing references | "analyze the document" | "analyze the document in <document> tags" |

## power combinations

### multishot + CoT

```xml
<examples>
  <example>
    <input>...</input>
    <thinking>step by step reasoning</thinking>
    <output>...</output>
  </example>
</examples>
```

### self-correction

```xml
<draft>
{{FIRST_ATTEMPT}}
</draft>

<feedback>
{{REVIEW}}
</feedback>

<instructions>
Revise the draft based on feedback.
</instructions>
```

### role + constraints + examples

```xml
<role>
Senior security engineer
</role>

<constraints>
- Focus on OWASP Top 10
- Severity ratings: critical/high/medium/low
- Must provide remediation for each finding
</constraints>

<examples>
{security review examples}
</examples>
```

## sources

- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-prompts
