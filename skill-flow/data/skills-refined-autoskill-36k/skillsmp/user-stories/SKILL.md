---
name: user-stories
description: User Stories skill for the ikigai project
---

# User Stories

## Description

Format specification for writing user stories that document terminal interactions.

## Format

Each user story is a single markdown file with the following structure:

### Title (H1)

The name of the user story.

### Description (H2)

A brief 2-4 sentence overview of what the user story demonstrates.

### Transcript (H2)

A `text` code block showing the terminal output exactly as it appears to the user.

- Use `>` prefix for user input
- Model responses appear without prefix
- Tool calls and results are shown as the user sees them

```text
> user input here

model response here
```

### Walkthrough (H2)

A numbered list explaining step-by-step what happens during the interaction. Keep descriptions concise. Reference detailed JSON in the Reference section using markdown links:

```markdown
2. Client builds request (see [Request A](#request-a))
```

### Multiple Transcript Blocks

If the story uses `/clear` or `/rewind` to change history, use multiple transcript/walkthrough pairs interleaved:

```markdown
## Transcript

```text
> first interaction
```

## Walkthrough

1. Step one
2. Step two

## Transcript

```text
> /clear
> second interaction after clear
```

## Walkthrough

1. Clear command resets history
2. New interaction begins
```

### Reference (H2)

Full JSON payloads referenced in the walkthrough. Use H3 headings with anchor-friendly names:

```markdown
## Reference

### Request A

```json
{ ... full JSON ... }
```

### Response A

```json
{ ... full JSON ... }
```
```

## Output Location

User stories are stored in `cdd/user-stories/`:

```
cdd/
├── README.md           # High-level description of release features
├── user-stories/
│   ├── README.md       # Index/overview of user stories
│   ├── story-1.md      # Individual user story (user actions and system responses)
│   ├── story-2.md
│   └── ...
└── ...                 # Other files/directories (ignored by this skill)
```

**Note:** The `cdd/` directory may contain other files and directories beyond those listed above. This skill only works with `cdd/user-stories/` and may reference `cdd/README.md`. Other content is permitted and will be ignored.

- `cdd/README.md` - High-level description of release features
- `cdd/user-stories/README.md` - Index/overview with brief descriptions
- Individual story files - User actions and system responses with transcript and walkthrough

Update the README.md as you add user stories to keep the overview current.

## Rules

- One user story per document
- Assume empty message history at start (only system prompt exists)
- Keep model responses short - long responses make discussion harder
- Show exactly what the user sees in transcripts
- Put implementation details (JSON payloads) in Reference section
- Use sequential naming for references: Request A, Response A, Request B, etc.
