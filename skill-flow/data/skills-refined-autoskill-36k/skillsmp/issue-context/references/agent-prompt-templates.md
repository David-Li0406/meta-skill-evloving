# Agent Prompt Templates

Use these templates to generate structured, agent-ready prompts. Keep XML valid, include CDATA for code, and prefer short concrete steps.

## General Rules

- include `issue`, `type`, and `repo` attributes when known.
- cite real file paths and line numbers from files you read.
- keep steps small and ordered.
- always include validation commands.
- list open questions explicitly if any requirements are missing.

## Bugfix (Minimal)

```xml
<agent_prompt issue="ISSUE-ID" type="bugfix" repo="repo-name">
  <context>
    <summary>one-line description of the bug</summary>
  </context>
  <bug>
    <symptom>what breaks, where, for whom</symptom>
    <repro>steps to reproduce</repro>
    <expected>expected behavior</expected>
    <actual>current behavior</actual>
  </bug>
  <suspected_root>
    <file>path/to/file.ts</file>
    <hint>function or component to inspect first</hint>
  </suspected_root>
  <implementation_steps>
    <step order="1" file="path/to/file.ts">fix the root cause</step>
    <step order="2" file="path/to/test.ts">add regression test</step>
  </implementation_steps>
  <validation>
    <test>verify --format=summary</test>
    <test>targeted test command</test>
  </validation>
</agent_prompt>
```

## Feature (Full)

```xml
<agent_prompt issue="ISSUE-ID" type="feature" repo="repo-name">
  <context>
    <summary>one-line feature goal</summary>
    <stakeholders>who this is for</stakeholders>
  </context>
  <acceptance_criteria>
    <item>behavior or UI change required</item>
    <item>edge case to cover</item>
  </acceptance_criteria>
  <constraints>
    <item>performance, security, or UX rules</item>
  </constraints>
  <non_goals>
    <item>explicitly out of scope work</item>
  </non_goals>
  <integration_points>
    <item file="path/to/entry.ts">where new behavior is wired</item>
    <item file="path/to/ui.tsx">UI surface to update</item>
  </integration_points>
  <existing_pattern file="path/to/pattern.ts" lines="12-40">
    <description>pattern to follow</description>
    <code_snippet><![CDATA[
// actual snippet from file
    ]]></code_snippet>
  </existing_pattern>
  <implementation_steps>
    <step order="1" file="path/to/schema.ts">update schema/types</step>
    <step order="2" file="path/to/api.ts">add new API behavior</step>
    <step order="3" file="path/to/ui.tsx">update UI</step>
  </implementation_steps>
  <validation>
    <test>verify --format=summary</test>
    <test>targeted test command</test>
  </validation>
  <open_questions>
    <question>clarify acceptance criteria or UI detail</question>
  </open_questions>
</agent_prompt>
```

## Refactor (Safety-Oriented)

```xml
<agent_prompt issue="ISSUE-ID" type="refactor" repo="repo-name">
  <context>
    <summary>what is being refactored and why</summary>
  </context>
  <invariants>
    <item>behavior must not change</item>
    <item>performance baseline preserved</item>
  </invariants>
  <risk>
    <area>where breakage is likely</area>
    <rollback>rollback plan or feature flag</rollback>
  </risk>
  <implementation_steps>
    <step order="1" file="path/to/file.ts">mechanical refactor</step>
    <step order="2" file="path/to/file.ts">cleanup and simplify</step>
  </implementation_steps>
  <validation>
    <test>verify --format=summary</test>
  </validation>
</agent_prompt>
```

## Infra / Migration

```xml
<agent_prompt issue="ISSUE-ID" type="infra" repo="repo-name">
  <context>
    <summary>infra change and motivation</summary>
  </context>
  <migration>
    <step>add new fields or tables</step>
    <backfill>how to backfill or migrate data</backfill>
  </migration>
  <rollout>
    <plan>staged rollout or flag</plan>
    <rollback>revert steps if issues appear</rollback>
  </rollout>
  <monitoring>
    <metric>key metrics to watch</metric>
    <alert>failure signals</alert>
  </monitoring>
  <validation>
    <test>verify --format=summary</test>
  </validation>
</agent_prompt>
```
