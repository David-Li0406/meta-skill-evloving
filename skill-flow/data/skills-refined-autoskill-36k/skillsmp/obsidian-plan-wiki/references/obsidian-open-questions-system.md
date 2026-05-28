# Obsidian Open Questions System

Handoff document for agents maintaining the open questions tracking system.

## Overview

Track open questions across documentation using Obsidian-compatible hidden comments with author tags and block references for direct navigation.

## Format Specification

### Basic Format
```markdown
%% [ ] 🙋‍♂️: human-written question or note %% ^q-unique-id

%% [ ] 🤖: agent-generated question %% ^q-unique-id

%% [x] 🤖: resolved question → answer %% ^q-unique-id
```

### Author Tags & Conversation Threading

Questions are conversation threads. The **LAST emoji** determines whose turn it is:

| Last emoji in thread | Whose turn |
|---------------------|------------|
| 🤖 | **Human** needs to respond |
| 🙋‍♂️ | **Agent** should pick up |
| `[x]` | **Done** - nobody needs to act |

**Example thread:**
```
%% [ ] 🤖: Should we cache this? 🙋‍♂️ yes but limit size 🤖: what limit? %% ^q-cache
```
Last emoji is 🤖 → Human's turn to answer "what limit?"

**Simple cases:**
- `🤖: question` → Human answers
- `🙋‍♂️: task` → Agent actions
- `🤖: q? 🙋‍♂️: answer` → Agent picks up (human answered)
- `🤖: q? 🙋‍♂️: done 🤖: followup?` → Human answers followup

### Block ID Convention
Format: `^q-{scope}-{descriptor}`

Examples:
- `^q-history-dedupe` (history provider, deduplication question)
- `^q-prefs-hotkeys` (preferences, hotkeys question)
- `^q-sign-approval` (code signing, approval question)

## Critical: Blank Lines Required

**Each question MUST be separated by a blank line.** Obsidian treats consecutive lines as a single block — only the LAST block ID works.

### WRONG (only `^q-two` works)
```markdown
%% [ ] 🤖: First question %% ^q-one
%% [ ] 🤖: Second question %% ^q-two
```

### CORRECT (both work)
```markdown
%% [ ] 🤖: First question %% ^q-one

%% [ ] 🤖: Second question %% ^q-two
```

## Dataview Auto-Index

The index page at `docs/open-questions.md` uses Dataview JS to auto-generate links:

```dataviewjs
const pages = dv.pages('"workstreams" or "reference"');
const results = [];

// Find the LAST emoji in the text to determine whose turn it is
function getLastResponder(text) {
  const emojis = [...text.matchAll(/🙋‍♂️|🤖/g)];
  if (emojis.length === 0) return null;
  return emojis[emojis.length - 1][0];
}

// Skip documentation files that contain examples, not real questions
const ignored = ['obsidian-open-questions-system', 'AGENTS'];

for (const page of pages) {
  if (ignored.some(pattern => page.file.path.includes(pattern))) continue;
  const content = await dv.io.load(page.file.path);
  const lines = content.split('\n');

  lines.forEach((line, idx) => {
    const match = line.match(/%% \[ \] (🙋‍♂️|🤖): (.+?) %% \^(q-[\w-]+)/);
    if (match) {
      const starter = match[1];
      const question = match[2];
      const blockId = match[3];
      // Last emoji in the full text (starter + question content) determines whose turn
      const fullText = starter + ': ' + question;
      const lastResponder = getLastResponder(fullText);
      results.push({ page, starter, question, blockId, line: idx + 1, lastResponder });
    }
  });
}

// Group by whose turn it is (based on LAST responder)
// Last was 🤖 → Human needs to answer
// Last was 🙋‍♂️ → Agent needs to pick up
const needsHuman = results.filter(r => r.lastResponder === '🤖');
const needsAgent = results.filter(r => r.lastResponder === '🙋‍♂️');

if (needsHuman.length > 0) {
  dv.header(3, "🤖 Last: Needs Human Response");
  dv.list(needsHuman.map(r =>
    `[[${r.page.file.path}#^${r.blockId}|${r.page.file.name}]] - ${r.question}`
  ));
}

if (needsAgent.length > 0) {
  dv.header(3, "🙋‍♂️ Last: Agent Should Pick Up");
  dv.list(needsAgent.map(r =>
    `[[${r.page.file.path}#^${r.blockId}|${r.page.file.name}]] - ${r.question}`
  ));
}
```

### Key Regex Pattern
```javascript
/%% \[ \] (🙋‍♂️|🤖): (.+?) %% \^(q-[\w-]+)/
```

Captures:
1. Author emoji (`🙋‍♂️` or `🤖`)
2. Question text (non-greedy)
3. Block ID (must start with `q-`, then alphanumeric + hyphens)

## Link Format

Use Obsidian's native wikilink with block reference:

```markdown
[[path/to/file#^block-id|Display Text]]
```

Example:
```markdown
[[workstreams/03-command-palette/3.4-history-provider#^q-history-dedupe|3.4-history-provider]]
```

## Common Errors to Avoid

### 1. Block ID Outside Comment
**WRONG:** Block ID after `%%` — Obsidian can't attach it to invisible content
```markdown
%% [ ] 🤖: question %% ^q-id
```
**Actually this works** if the line is isolated (has blank lines before/after).

### 2. Consecutive Questions Without Blank Lines
**WRONG:** Only last block ID works
```markdown
%% [ ] 🤖: Q1 %% ^q-one
%% [ ] 🤖: Q2 %% ^q-two
%% [ ] 🤖: Q3 %% ^q-three
```
**RIGHT:** Each is its own block
```markdown
%% [ ] 🤖: Q1 %% ^q-one

%% [ ] 🤖: Q2 %% ^q-two

%% [ ] 🤖: Q3 %% ^q-three
```

### 3. Obsidian URI with vault= Parameter
**WRONG:** Hardcoded vault name breaks in other vaults
```markdown
[link](obsidian://open?vault=docs&file=path&line=123)
```
**RIGHT:** Use native wikilinks (work in any vault)
```markdown
[[path/to/file#^block-id|text]]
```

### 4. Line Number Links Don't Work
Obsidian doesn't support `&line=123` in URIs. Use block references instead.

### 5. Duplicate Block IDs
Block IDs must be unique across the entire vault. Use descriptive prefixes:
- `^q-history-` for history provider questions
- `^q-prefs-` for preferences questions
- `^q-ext-` for extension questions

## Distinguishing Human vs Agent Questions

**CRITICAL FOR AGENTS:** The emoji tells you WHO WROTE IT, which determines WHO ANSWERS:
- See `🙋‍♂️:` → **You (agent) should action this** (human wrote it for you)
- See `🤖:` → **SKIP this** (you or another agent wrote it, waiting for human)

### Human-written (`🙋‍♂️:`) - AGENTS SHOULD ACTION:
- Casual language, incomplete sentences
- Inline responses (`-> NO`, `-> yes`)
- Personal context ("one of the big things here was...")
- Obsidian wikilinks in the text
- Missing punctuation, abbreviations ("prio")

### Agent-written (`🤖:`) - AGENTS MUST SKIP:
- Formal "Should we X?" pattern
- Complete sentences with proper punctuation
- Parenthetical examples `(e.g., X)`
- Technical but generic phrasing
- Consistent structure

## Adding New Questions

When adding a question to a spec:

1. Choose author tag based on source
2. Create unique block ID with scope prefix
3. Ensure blank line before AND after
4. Verify the regex pattern still matches

```markdown
### Open Questions

%% [ ] 🤖: New question here? %% ^q-scope-descriptor

%% [ ] 🙋‍♂️: personal note about something %% ^q-scope-note
```

## Resolving Questions

Change `[ ]` to `[x]` and add answer after `→`:

```markdown
%% [x] 🤖: Should we use X? → Yes, implemented in PR #123 %% ^q-scope-x
```

The Dataview query only shows `[ ]` (unresolved) questions.

## Requirements

- **Dataview plugin** installed and enabled
- **Enable JavaScript Queries** in Dataview settings
- Questions must match the exact regex pattern
- Block IDs must be valid (alphanumeric + hyphens only)

## Files

| File | Purpose |
|------|---------|
| `docs/open-questions.md` | Auto-generated index (Dataview JS) |
| `docs/CLAUDE.md` | Pointer file (contains only `@AGENTS.md`) |
| `docs/AGENTS.md` | Actual agent instructions including this convention |
| Individual spec files | Contain the actual questions |

## Grep Commands

```bash
# All open questions
grep -rn "%% \[ \]" docs/

# Human only
grep -rn "🙋‍♂️:" docs/

# Agent only
grep -rn "🤖:" docs/

# Find questions missing block IDs
grep -rn "%% \[ \].*%%$" docs/  # Lines ending with %% (no ^id)
```
