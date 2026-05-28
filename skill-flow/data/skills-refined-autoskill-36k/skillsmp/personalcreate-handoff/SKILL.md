---
name: personal:create-handoff
description: >
  Write concise handoff documents to transfer work context to another agent session.
  Use when the user asks to hand off or wrap up work for later.
---

# Create Handoff

You are tasked with writing a handoff document to transfer your work context to another session. The handoff must be thorough but **concise**. The goal is to compact and summarize your context without losing any key details.

## Process

### 1. Filepath & Metadata
Use the following information to understand how to create your document:
- Create your file under `.coding-agent/handoffs/ENG-XXXX/YYYY-MM-DD_HH-MM-SS_ENG-ZZZZ_description.md` (create the subdirectory structure if it doesn't already exist), where:
  - YYYY-MM-DD is today's date
  - HH-MM-SS is the hours, minutes and seconds based on the current time, in 24-hour format (i.e. use `13:00` for `1:00 pm`)
  - ENG-XXXX is the ticket number (replace with `general` if no ticket)
  - ENG-ZZZZ is the ticket number (omit if no ticket)
  - description is a brief kebab-case description
- Run the `~/bin/spec-metadata` script to generate all relevant metadata
- Examples:
  - With ticket: `2025-01-08_13-55-22_ENG-2166_create-context-compaction.md`
  - Without ticket: `2025-01-08_13-55-22_create-context-compaction.md`

### 2. Handoff writing
Using the above conventions, write your document. Use the defined filepath and the following YAML frontmatter pattern. Use the metadata gathered in step 1. Structure the document with YAML frontmatter followed by content:

Use the following template structure:
```markdown
---
date: [Current date and time with timezone in ISO format]
git_commit: [Current commit hash]
branch: [Current branch name]
repository: [Repository name]
topic: "[Feature/Task Name] Implementation Strategy"
tags: [implementation, strategy, relevant-component-names]
status: complete
last_updated: [Current date in YYYY-MM-DD format]
type: implementation_strategy
---

# Handoff: ENG-XXXX {very concise description}

## Task(s)
{description of the task(s) that you were working on, along with the status of each (completed, work in progress, planned/discussed). If you are working on an implementation plan, make sure to call out which phase you are on. Make sure to reference the plan document and/or research document(s) you are working from that were provided to you at the beginning of the session, if applicable.}

## Critical References
{List any critical specification documents, architectural decisions, or design docs that must be followed. Include only 2-3 most important file paths. Leave blank if none.}

## Recent changes
{describe recent changes made to the codebase that you made in line:file syntax}

## Learnings
{describe important things that you learned - e.g. patterns, root causes of bugs, or other important pieces of information someone that is picking up your work after you should know. consider listing explicit file paths.}

## Artifacts
{ an exhaustive list of artifacts you produced or updated as filepaths and/or file:line references - e.g. paths to feature documents, implementation plans, etc that should be read in order to resume your work.}

## Action Items & Next Steps
{ a list of action items and next steps for the next agent to accomplish based on your tasks and their statuses}

## Other Notes
{ other notes, references, or useful information - e.g. where relevant sections of the codebase are, where relevant documents are, or other important things you learned that you want to pass on but that don't fall into the above categories}
```

### 3. Approve and Sync
Ask the user to review and approve the document. If they request any changes, make them and ask for approval again.

Once approved, respond with a concise confirmation and include the handoff path, for example:

```
Handoff created and synced! You can resume from this handoff in a new session with:

.coding-agent/handoffs/ENG-2166/2025-01-08_13-44-55_ENG-2166_create-context-compaction.md
```

## Additional Notes & Instructions
- **More information, not less**. This is a guideline that defines the minimum of what a handoff should be. Always feel free to include more information if necessary.
- **Be thorough and precise**. Include both top-level objectives and lower-level details as necessary.
- **Avoid excessive code snippets**. While a brief snippet to describe a key change is important, avoid large code blocks or diffs unless absolutely necessary. Prefer using `path/to/file.ext:line` references that another agent can follow later.
