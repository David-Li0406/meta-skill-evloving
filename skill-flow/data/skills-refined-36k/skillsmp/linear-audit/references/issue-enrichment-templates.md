# Issue Enrichment Templates

Templates for enriching Linear issues with codebase context, diagrams, and agent-ready prompts.

---

## Output Contract: Two Comments Per Issue

Each enriched issue gets two Linear comments with hidden markers:

1. **Analysis + Diagrams**: `<!-- issue-context:analysis -->`
2. **Agent Prompt**: `<!-- issue-context:agent-prompt -->`

If markers exist, update or add delta comment instead of reposting.

---

## Comment 1: Analysis + Diagrams

```markdown
<!-- issue-context:analysis -->
## Analysis: [Issue Title]

### Summary
[1-2 sentence overview of the issue and approach]

### Recent Progress
[Git history findings - what's been done, who worked on it, related commits]

### Architecture Map
```mermaid
flowchart TD
  [relevant architecture diagram - 5-15 nodes max]
```

### Data Flow
```mermaid
flowchart LR
  [data flow diagram]
```

### Implementation Notes
**Files to modify:**
1. `path/to/file.ts:line` - [what changes needed]
2. `path/to/file.tsx:line` - [what changes needed]

**Pattern to follow:**
[Reference existing code pattern with file:line - MUST have read the file first]

**Scope / Non-goals:**
- [Explicitly list what is out of scope]

**Dependencies/Blockers:**
[Any related issues, prerequisites, or blockers]

### Open Questions
- [Any missing requirements or ambiguous behavior]
```

---

## Comment 2: Agent Prompt

### Bugfix Template (Minimal)

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

### Feature Template (Full)

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

### Refactor Template (Safety-Oriented)

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

### Infra / Migration Template

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

---

## Decision Tree: Enrichment Depth

```
How complex is the issue?
├── Simple (bug fix, single file)
│   ├── Phase 1: quick issue analysis
│   ├── Phase 2: git blame on specific file
│   ├── Skip: diagrams (not needed)
│   └── Output: minimal agent prompt (bugfix template)
├── Moderate (feature, 2-5 files)
│   ├── All phases 1-5
│   ├── Phase 4: 1 architecture diagram
│   └── Output: full analysis + agent prompt (feature template)
├── Complex (architecture, cross-cutting)
│   ├── All phases 1-5
│   ├── Phase 4: 2-3 diagrams (arch, flow, state)
│   └── Output: detailed analysis + rich agent prompt
└── Epic/Infrastructure
    ├── Fetch parent/child issues
    ├── All phases with extended git audit
    ├── Phase 4: system-level diagrams
    └── Output: comprehensive spec (infra template)
```

## Decision Tree: Template Selection

```
What kind of work?
├── Bugfix or regression
│   └── Bugfix template (minimal repro + suspected root)
├── Feature or enhancement
│   └── Feature template (acceptance criteria + integration points)
├── Refactor or cleanup
│   └── Refactor template (invariants + coverage plan)
└── Infra or migration
    └── Infra template (rollback + risk checklist)
```

## Decision Tree: Diagram Selection

```
What does the issue touch?
├── Data transformation
│   └── Sequence diagram (flow of data)
├── Component interaction
│   └── Flowchart (component boundaries)
├── State changes
│   └── State diagram (transitions)
├── System architecture
│   └── C4/layer diagram (dependencies)
├── API changes
│   └── Sequence + entity diagram
└── Multiple areas
    └── Combine relevant diagrams (max 3)
```

---

## Quality Checklist

- [ ] URLs use workspace slug (not team prefix)
- [ ] git audit done - recent progress documented
- [ ] files actually read - patterns verified, not guessed
- [ ] diagrams digestible - 5-15 nodes each
- [ ] file paths correct - verified paths exist
- [ ] line numbers accurate - referenced after reading
- [ ] XML well-formed - valid structure, CDATA for code
- [ ] mermaid renders - tested syntax
- [ ] comment markers included and idempotent
- [ ] prompt includes acceptance criteria and validation commands
- [ ] open questions captured if blockers remain

---

## Posting to Linear

```bash
# Post analysis + diagrams comment
linear comment create -i $ISSUE_ID -b "$ANALYSIS_COMMENT" --workspace luke-labs

# Post agent prompt comment
linear comment create -i $ISSUE_ID -b "$AGENT_PROMPT_COMMENT" --workspace luke-labs

# Verify posted
linear comment list $ISSUE_ID --workspace luke-labs

# Find existing issue-context comments
linear comment list $ISSUE_ID --json --workspace luke-labs | jq -r '.[].body' | rg "issue-context:"
```

---

## Concrete Values

| value | meaning | source |
|-------|---------|--------|
| diagram nodes | 5-15 | readable without overwhelming |
| max diagrams per issue | 3 | avoid information overload |
| git history window | 4 weeks | sufficient recent context |
| comment marker format | `<!-- issue-context:X -->` | idempotency tag |
| enrichment time | ~15 min | typical for moderate issue |
