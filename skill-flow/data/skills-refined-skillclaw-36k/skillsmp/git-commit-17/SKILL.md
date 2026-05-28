---
name: git-commit
description: Use when creating Git commits.
---

# Git Commit

## Staged Changes

Run `git status` to see what changes are staged for commit. If there are no staged changes, stage all modified files.

## Title

Create a clear, succinct title that explains what the commit accomplishes. Brief - only the essentials.

**Use imperative mood:** "Add feature" not "Added feature" or "Adds feature"

Good examples:

- Add user authentication
- Fix memory leak in parser
- Update dependencies
- Remove deprecated API endpoints

Avoid overly detailed titles and phrases like "This commit..." or "Changes to..."

## Body

**MOST COMMITS SHOULD HAVE NO BODY. DO NOT ADD A BODY UNLESS ABSOLUTELY NECESSARY.** A title-only commit is almost always better.

**Before adding a body, ask yourself:** Does this body add information that isn't obvious from the title? If the body just expands on what the title already says, delete it.

Bad example:

```
Add writing-markdown skill

- Add SKILL.md with instructions
- Add scripts/resource-paths script
```

The body just restates "Add writing-markdown skill" in more words. Delete the body.

**Only add a body when the title genuinely can't capture important context.** The body must contain non-redundant detail that adds real value.

**Write bodies in markdown.** Use markdown formatting for lists, emphasis, code, etc.

Common patterns (only when a body is truly necessary):

- **Simple context (1-2 sentences):** Explain the "why" or rationale when it's not obvious
- **Bullet list:** List specific changes when there are multiple distinct items
- **Paragraph + bullet list:** Provide context, then list specific changes under a "Changes:" header
- **Multiple sections:** Use headers to organize complex changes (e.g., "Changes:" and "Template-specific changes:")

The title says "what" - the body explains "why" or provides specific details

## Formatting

**YOU MUST use the format script before outputting the final commit message.**

Run the format script with your drafted title and body:

```bash
./format-commit-message.sh --title "Your commit title" --body "Your commit body"
```

## Create Commit

After formatting, create the commit using the formatted message. Use a heredoc to preserve formatting:

```bash
git commit -m "$(cat <<'EOF'
Commit title here

Optional body here.
EOF
)"
```

## Rationalizations

| Thought                            | Reality                           |
| ---------------------------------- | --------------------------------- |
| "I'll provide multiple versions"   | Draft ONE commit message          |
| "I should explain the format"      | Start with the title directly     |
| "I'll introduce the message"       | NO introductory text whatsoever   |
| "This simple change needs context" | Simple changes rarely need bodies |

**REQUIRED:** See [references/examples.md](references/examples.md) for correct formatting.
