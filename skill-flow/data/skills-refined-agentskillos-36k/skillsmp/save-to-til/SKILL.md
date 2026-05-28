---
name: save-to-til
description: Use when the user wants to add a new TIL (Today I Learned) entry to their TIL repository. Automatically analyzes existing TIL patterns and creates a new entry following the repository's conventions.
---

You are helping the user create a new TIL entry in their repository (use the current working directory `$WORKDIR`).

## Step 1: Analyze Existing Patterns

Before creating any TIL, you MUST first explore the repository to understand:

1. **Directory Structure**: Check how TILs are organized (by topic/category)
2. **File Naming Conventions**: Observe naming patterns (lowercase, hyphens, descriptive)
3. **Writing Style**: Review existing TILs to understand the format

Use Glob and Read tools to examine:
- A few existing TIL files in different directories
- The overall directory structure
- Common formatting patterns

## Step 2: Create the TIL File

Based on your analysis, create a new TIL following these conventions:

### File Naming
- Use **lowercase** with **hyphens** for spaces
- Be descriptive and specific
- Place in appropriate category directory (or create new one if needed)

### Content Format
- Use **H2 headers** (`## Title`) for the main title
- Keep content **concise and practical**
- Use **code blocks** for commands or code
- Use **bold text** for key points
- Include relevant context or prerequisites

### Typical Structure
```markdown
## Title

Brief description if needed.

### Section 1
Content with code blocks:
```bash
command here
```

### Section 2
More content...
```

## Step 3: Confirm Creation

After creating the file, inform the user of:
- File path created
- Brief summary of what was documented

## Step 4: Git Commit and Push

After creating the TIL entry, follow this git workflow:

1. **Check git status** to see what changed
2. **Add the new file** to staging
3. **Create a commit** with a concise message (format defined in `claude.md`)
4. **Push to remote** repository

The commit message format is:
```
<topic>: <brief description>

Examples:
- golang: add defer usage notes
- docker: document network mode firewall setup
- react: fix useEffect hook pattern

**DO NOT** add `Co-Authored-By` or any other trailers - keep commits concise.
```

## Important Notes

- **ALWAYS explore first** - Never assume conventions without checking
- **Match existing style** - Blend in with the repository's patterns
- **Be concise** - TILs should be quick reads
- **Focus on action** - Document practical, usable information
- **Update readme.md** when creating a new category folder (see `claude.md`)
