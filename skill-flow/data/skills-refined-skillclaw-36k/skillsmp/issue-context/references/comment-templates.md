# Comment Templates

Two comments are generated per issue:
1. **Analysis + Diagrams** - Human-readable with visualizations
2. **Agent Prompt** - Structured XML for coding agents

## Comment 1: Analysis + Diagrams

```markdown
<!-- issue-context:analysis -->
## Analysis: [Issue Title]

### Summary
[1-2 sentence overview of the issue and approach]

### Recent Progress
[Git history findings - what's been done, who worked on it, related commits]

### Architecture Map
[Package/layer dependency diagram from layer CLI]

```mermaid
flowchart TD
  [relevant architecture diagram]
```

### Data Flow
[How data moves through the system for this feature]

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

### Risks / Rollback (if infra)
- [Risk area and rollback plan]

### Sequence Diagram (if interaction-heavy)
```mermaid
sequenceDiagram
  [interaction flow]
```
```

## Comment 2: Agent Prompt

````markdown
<!-- issue-context:agent-prompt -->
## Agent Prompt: [Issue ID]

```xml
<?xml version="1.0" encoding="UTF-8"?>
<agent_prompt issue="[ISSUE_ID]" type="[feature|bugfix|refactor]">

  <context>
    <summary>[One-line summary]</summary>
    <repo>[repo name(s)]</repo>
    <recent_commits>
      <commit hash="abc123">[commit message]</commit>
    </recent_commits>
  </context>

  <acceptance_criteria>
    <item>[Behavior or UI change required]</item>
  </acceptance_criteria>

  <constraints>
    <item>[Invariants or hard rules]</item>
  </constraints>

  <non_goals>
    <item>[Out of scope]</item>
  </non_goals>

  <primary_files>
    <file>[path/to/main/file.ts]</file>
  </primary_files>

  <related_files>
    <file>[path/to/reference/file.ts]</file>
  </related_files>

  <existing_pattern file="[path]" lines="[start-end]">
    <description>[What this pattern shows]</description>
    <code_snippet>
      <![CDATA[
[Actual code snippet - MUST have read the file]
      ]]>
    </code_snippet>
  </existing_pattern>

  <implementation_steps>
    <step order="1" file="[path]">
      <action>[What to do]</action>
      <details>[How to do it, specific guidance]</details>
    </step>
    <step order="2" file="[path]">
      <action>[What to do]</action>
      <details>[How to do it]</details>
    </step>
  </implementation_steps>

  <validation>
    <test>[How to verify the change works]</test>
    <test>[Additional test case]</test>
    <lint>pnpm lint</lint>
    <build>pnpm build</build>
  </validation>

  <open_questions>
    <question>[Clarification needed]</question>
  </open_questions>

  <files_to_modify>
    <file>[path1]</file>
    <file>[path2]</file>
  </files_to_modify>
</agent_prompt>
```
````

## Section Guidelines

### Context Section
- Project name and purpose (1-2 sentences)
- Technology stack
- Domain-specific terminology

### Current State Section
Most critical. Include:
- Relevant completed work with file paths
- Patterns to follow
- Constraints from existing code

### Implementation Steps
Balance specificity with latitude:
- **Specific**: Acceptance criteria, integration points, constraints
- **Open**: Implementation approach, data structures, helpers

### Validation Section
Always include runnable commands:
- Type checking commands
- Test commands
- Build verification

### Open Questions
If any requirements are ambiguous, list them explicitly so the agent can ask.

## Posting

```bash
# Post analysis + diagrams comment
linear comment create -i $ISSUE_ID -b "$ANALYSIS_COMMENT"

# Post agent prompt comment
linear comment create -i $ISSUE_ID -b "$AGENT_PROMPT_COMMENT"

# Verify posted
linear comment list $ISSUE_ID
```
