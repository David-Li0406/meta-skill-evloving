# Prompt Chaining Patterns

multi-step workflows that break complex tasks into manageable subtasks, with handoffs via XML.

## why chain prompts

| benefit | explanation |
|---------|-------------|
| accuracy | each subtask gets full attention |
| clarity | simpler prompts, clearer outputs |
| traceability | pinpoint issues in specific steps |
| parallelization | independent subtasks can run concurrently |
| iteration | refine one step without redoing others |

> "Each link in the chain gets Claude's full attention!"
> — anthropic/chain-prompts

## core patterns

### content pipeline

**flow**: Research → Outline → Draft → Edit → Format

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Research │───▶│ Outline  │───▶│  Draft   │───▶│  Edit    │───▶│ Format   │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
```

**use case**: blog posts, documentation, reports

**prompt 1: research**
```xml
<role>Research assistant</role>
<topic>{{TOPIC}}</topic>
<instructions>
Gather key facts, statistics, and sources about the topic.
Output structured research notes.
</instructions>
<output_format>
<research>
  <key_facts>[list]</key_facts>
  <statistics>[with sources]</statistics>
  <sources>[urls]</sources>
</research>
</output_format>
```

**prompt 2: outline**
```xml
<role>Content strategist</role>
<research>{{RESEARCH_OUTPUT}}</research>
<instructions>
Create a logical outline with sections and key points.
</instructions>
<output_format>
<outline>
  <section title="...">
    <point>...</point>
  </section>
</outline>
</output_format>
```

**prompt 3: draft**
```xml
<role>Content writer</role>
<outline>{{OUTLINE_OUTPUT}}</outline>
<research>{{RESEARCH_OUTPUT}}</research>
<instructions>
Write the full draft following the outline.
Use research for supporting evidence.
</instructions>
```

### data processing

**flow**: Extract → Transform → Analyze → Visualize

```
┌──────────┐    ┌───────────┐    ┌──────────┐    ┌───────────┐
│ Extract  │───▶│ Transform │───▶│ Analyze  │───▶│ Visualize │
└──────────┘    └───────────┘    └──────────┘    └───────────┘
```

**use case**: log analysis, data migration, reporting

**prompt 1: extract**
```xml
<role>Data extraction specialist</role>
<raw_data>{{RAW_INPUT}}</raw_data>
<instructions>
Extract structured data from the raw input.
Handle missing fields gracefully.
</instructions>
<output_format>
{
  "records": [
    {"field1": "value", "field2": "value"}
  ],
  "extraction_notes": "any issues encountered"
}
</output_format>
```

**prompt 2: transform**
```xml
<role>Data engineer</role>
<extracted_data>{{EXTRACTED_OUTPUT}}</extracted_data>
<transformation_rules>
- Normalize dates to ISO 8601
- Convert currencies to USD
- Deduplicate by ID
</transformation_rules>
<instructions>
Apply transformation rules to the extracted data.
</instructions>
```

### decision making

**flow**: Gather info → List options → Analyze each → Recommend

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌───────────┐
│  Gather  │───▶│  List    │───▶│ Analyze  │───▶│ Recommend │
└──────────┘    └──────────┘    └──────────┘    └───────────┘
```

**use case**: vendor selection, architecture decisions, strategic planning

**prompt 1: gather**
```xml
<role>Research analyst</role>
<decision_context>{{CONTEXT}}</decision_context>
<instructions>
Identify all relevant factors for this decision:
- Constraints
- Requirements (must-have vs nice-to-have)
- Stakeholders and their priorities
- Success criteria
</instructions>
```

**prompt 2: list options**
```xml
<role>Strategic planner</role>
<context>{{GATHERED_INFO}}</context>
<instructions>
Generate 3-5 distinct options for addressing this decision.
Include at least one unconventional option.
</instructions>
```

**prompt 3: analyze**
```xml
<role>Decision analyst</role>
<options>{{OPTIONS_LIST}}</options>
<criteria>{{SUCCESS_CRITERIA}}</criteria>
<instructions>
For each option:
1. Score against criteria (1-10)
2. List pros and cons
3. Identify risks
4. Estimate effort/cost
</instructions>
```

**prompt 4: recommend**
```xml
<role>Executive advisor</role>
<analysis>{{ANALYSIS_OUTPUT}}</analysis>
<instructions>
Based on the analysis, make a clear recommendation.
Explain your reasoning.
Provide a decision framework if close call.
</instructions>
```

### self-correction

**flow**: Generate → Review → Refine → Re-review

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌───────────┐
│ Generate │───▶│  Review  │───▶│  Refine  │───▶│ Re-review │
└──────────┘    └──────────┘    └──────────┘    └───────────┘
                     │                              │
                     └───── loop if needed ─────────┘
```

**use case**: high-stakes content, technical accuracy, quality assurance

**prompt 1: generate**
```xml
<role>{{DOMAIN}} expert</role>
<task>{{TASK}}</task>
<instructions>
Complete the task to the best of your ability.
</instructions>
```

**prompt 2: review**
```xml
<role>{{DOMAIN}} reviewer</role>
<work>{{GENERATED_OUTPUT}}</work>
<original_task>{{TASK}}</original_task>
<instructions>
Review this work for:
1. Accuracy
2. Completeness
3. Clarity
4. Adherence to requirements

Grade each dimension A-F.
Provide specific improvement suggestions.
</instructions>
<output_format>
<review>
  <grades>
    <accuracy>B+</accuracy>
    <completeness>A-</completeness>
    ...
  </grades>
  <issues>
    <issue>specific problem</issue>
  </issues>
  <suggestions>
    <suggestion>specific improvement</suggestion>
  </suggestions>
</review>
</output_format>
```

**prompt 3: refine**
```xml
<role>{{DOMAIN}} expert</role>
<original>{{GENERATED_OUTPUT}}</original>
<review>{{REVIEW_OUTPUT}}</review>
<instructions>
Improve the work based on the review feedback.
Address each issue and suggestion.
</instructions>
```

## parallelization

for independent subtasks, run concurrently:

```
                    ┌──────────┐
               ┌───▶│ Task A   │───┐
               │    └──────────┘   │
┌──────────┐   │    ┌──────────┐   │    ┌──────────┐
│  Split   │───┼───▶│ Task B   │───┼───▶│  Merge   │
└──────────┘   │    └──────────┘   │    └──────────┘
               │    ┌──────────┐   │
               └───▶│ Task C   │───┘
                    └──────────┘
```

**example**: analyzing multiple documents

```xml
<!-- split prompt -->
<instructions>
Split the following documents for parallel analysis.
Return a list of document IDs.
</instructions>

<!-- parallel prompts (run concurrently) -->
<document id="1">{{DOC_1}}</document>
<instructions>Analyze this document...</instructions>

<document id="2">{{DOC_2}}</document>
<instructions>Analyze this document...</instructions>

<!-- merge prompt -->
<analyses>{{ALL_ANALYSES}}</analyses>
<instructions>
Synthesize findings across all documents.
Identify common themes and contradictions.
</instructions>
```

## handoff patterns

### XML output → XML input

```xml
<!-- prompt 1 output -->
<findings>
  <finding id="1">issue description</finding>
  <finding id="2">another issue</finding>
</findings>

<!-- prompt 2 input -->
<previous_findings>{{FINDINGS_XML}}</previous_findings>
<instructions>
For each finding in <previous_findings>, suggest a fix.
</instructions>
```

### JSON intermediate format

```xml
<!-- prompt 1 output -->
<output_format>
Return JSON: {"items": [...], "metadata": {...}}
</output_format>

<!-- prompt 2 input -->
<data>{{JSON_OUTPUT}}</data>
<instructions>
Process the items in the data object.
</instructions>
```

### structured summary

```xml
<!-- prompt 1 output -->
<summary>
  <key_points>[3-5 bullet points]</key_points>
  <decision>[conclusion if any]</decision>
  <open_questions>[unresolved items]</open_questions>
</summary>

<!-- prompt 2 input -->
<previous_summary>{{SUMMARY}}</previous_summary>
<instructions>
Continue from where we left off.
Address the open questions.
</instructions>
```

## debugging chains

| symptom | likely cause | fix |
|---------|--------------|-----|
| output doesn't match expected | handoff format mismatch | verify XML/JSON structure |
| information lost between steps | insufficient summary | add more detail to handoff |
| step produces wrong result | too much in one prompt | split into smaller subtasks |
| chain takes too long | sequential when could parallel | identify independent tasks |
| inconsistent quality | no review step | add self-correction loop |

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| monolithic prompt | too much for one call | break into focused subtasks |
| over-chaining | unnecessary steps | combine steps that naturally fit |
| lost context | forgetting earlier info | pass relevant context forward |
| tight coupling | can't modify one step | use clean interfaces (XML tags) |
| no error handling | chain breaks on bad output | add validation between steps |

## sources

- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-prompts
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags
