---
name: add-to-inbox
description: Create a new note in the Obsidian inbox with user-specified content, including project context
license: Apache-2.0
compatibility: opencode
---

## Vault Configuration
Obsidian vault path: "~/Documents/nls"
Inbox location: "01 Inbox"

## Quick Start

1. Determine the current project context (git repo name, working directory)
2. Get the content/idea from the user
3. Generate a descriptive filename based on the content
4. Create a new note in `{vault}/01 Inbox/{filename}.md`
5. Include project context in the note

## Note Template

```markdown
---
created: YYYY-MM-DD HH:mm
project: {project-name}
source: {working-directory}
status: inbox
---

# {Title}

{User-provided content}

## Context

- **Project:** {project-name}
- **Directory:** {working-directory}
- **Created during:** {brief description of what was being worked on}
```

## Process

**Step 1: Gather context**
- Get current date and time from system
- Identify project name from git remote or directory name
- Get current working directory path

**Step 2: Process user input**
- Extract the main idea/content from user's request
- Generate a concise, descriptive title for the note
- Create a filename from the title (lowercase, hyphens, no special chars)

**Step 3: Create the note**
- Build path: `{vault}/01 Inbox/{filename}.md`
- Populate template with gathered information
- Include any additional context the user provides

**Step 4: Confirm creation**
- Verify the file was created successfully
- Report the note location to the user

## Filename Guidelines

- Use lowercase letters and hyphens only
- Keep it concise but descriptive (3-6 words)
- No dates in filename (dates are in frontmatter)
- Examples: `api-rate-limiting-idea.md`, `refactor-auth-module.md`

## Success Criteria

- [ ] Note created in correct inbox path
- [ ] Frontmatter includes project context
- [ ] Content accurately captures user's input
- [ ] Filename is descriptive and properly formatted
