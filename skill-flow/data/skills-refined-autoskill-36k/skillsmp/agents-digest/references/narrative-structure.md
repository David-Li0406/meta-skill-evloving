# Narrative Structure

Digest formats and templates for readable agent work summaries.

## Narrative Principles

1. **Story arc** - setup, implementation, outcome
2. **Code snippets** - highlights, not dumps
3. **Decisions** - why, not just what
4. **Outcomes** - tests, deployment, blockers

## Daily Digest Template

```markdown
# Agent Activity — {Date}

{for each project with activity}

## {Project}

**Agent:** {agent}
**Duration:** {total_duration}
**Confidence:** {avg_confidence}/10

### {Task Title}

{Brief task description}

**Approach:**
{Key decisions, 1-2 sentences}

**Implementation:**
```{language}
{relevant code snippet, 10-15 lines}
```

**Verification:**
{test status, deployment status}

{if blockers}
**Blockers:**
- {blocker description}
{endif}

---

{next project}
```

## Weekly Roundup Template

```markdown
# Weekly Agent Activity — {Week Range}

## Summary

- **Total sessions:** {count}
- **Projects:** {project_list}
- **Total duration:** {hours}h
- **Average confidence:** {avg}/10

{for each project}

## {Project}

**Sessions:** {count}
**Duration:** {hours}h
**Confidence:** {avg}/10

### Features Completed

- {feature 1} (confidence: {n}/10)
- {feature 2} (confidence: {n}/10)

### Code Changes

- {files_changed} files
- +{lines_added} -{lines_removed} lines
- {commits_count} commits

### Highlights

{1-2 notable achievements or code snippets}

{next project}
```

## Code Snippet Extraction

```typescript
// Extract relevant snippet from file
const extractSnippet = (filePath: string, commit: string): string => {
  const diff = execSync(`git show ${commit} -- ${filePath}`).toString();
  const added = diff.split("\n").filter(line => line.startsWith("+"));

  // Get function context
  const snippet = added.slice(0, 15).join("\n");  // First 15 lines
  return snippet;
};
```

## Section Ordering

1. **Overview** - summary stats
2. **By Project** - group related work
3. **Chronological** - within each project
4. **Code Last** - snippets after narrative

## Formatting Rules

- **Headings:** H2 for projects, H3 for tasks
- **Code blocks:** Always specify language
- **Links:** Internal refs to full logs
- **Confidence:** Always show (X/10)
- **Duration:** Human-readable (3h 15m, not 11700s)
