# Attribution Formats Reference

Complete reference for Claude Code attribution formatting in commits and pull requests.

## Overview

Claude Code adds attribution to git commits and pull requests to acknowledge AI assistance. These are configured separately in `.claude/settings.local.json`:

```json
{
  "attribution": {
    "commit": "Commit attribution string",
    "pr": "Pull request attribution string"
  }
}
```

## Commit Attribution

### Format Specification

Commit attribution uses git trailers, which are key-value pairs at the end of commit messages.

**Standard git trailer format:**
```
Trailer-Name: Value
```

**Claude Code default:**
```
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Components

**1. Trailer Key:** `Co-Authored-By`
- Standard git trailer for acknowledging co-authors
- Recognized by GitHub and other platforms
- Can be any valid git trailer key

**2. Name:** `Claude Sonnet 4.5`
- Identifies the AI assistant
- Can include model version
- Can be customized to any name

**3. Email:** `<noreply@anthropic.com>`
- Email address in angle brackets
- Required for git trailer format
- Can be customized

### Example Formats

**Default (with model):**
```
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Custom name (with model):**
```
Co-Authored-By: Big Dawg Sonnet 4.5 <noreply@anthropic.com>
```

**Custom name (without model):**
```
Co-Authored-By: Big Dawg <noreply@anthropic.com>
```

**With custom message:**
```
Generated with AI assistance

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Multiple lines:**
```
This commit was created with AI assistance.
See https://claude.com/claude-code for details.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Custom trailer:**
```
AI-Assisted-By: Claude <noreply@anthropic.com>
```

**No attribution:**
```
""
```
(Empty string removes commit attribution entirely)

### How It Appears

Commit messages show the trailer at the end:

```
Add user authentication feature

Implement OAuth2 flow with JWT tokens.
Added middleware for protected routes.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

GitHub and GitLab recognize `Co-Authored-By` trailers and:
- Display co-authors on the commit
- Credit co-authors in contribution graphs
- Link to user profiles (if email is associated with an account)

---

## Pull Request Attribution

### Format Specification

PR attribution is plain text added to the PR description.

**Claude Code default:**
```
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### Components

**1. Indicator:** `🤖` (emoji)
- Visual indicator of AI generation
- Optional, can use any text or emoji

**2. Message:** `Generated with`
- Descriptive text
- Can be customized to any message

**3. Link:** `[Claude Code](https://claude.com/claude-code)`
- Markdown-formatted link
- Optional, can be plain text or removed

### Example Formats

**Default:**
```
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**Custom message:**
```
🤖 Generated with ✨ Style ✨ and [Claude Code](https://claude.com/claude-code)
```

**With custom name:**
```
🤖 Generated with [Big Dawg](https://claude.com/claude-code)
```

**Simple text:**
```
Created with Claude Code
```

**Detailed attribution:**
```
This pull request was created with AI assistance from Claude Code.
Learn more at https://claude.com/claude-code
```

**No emoji:**
```
Generated with [Claude Code](https://claude.com/claude-code)
```

**No link:**
```
🤖 Generated with Claude Code
```

**No attribution:**
```
""
```
(Empty string removes PR attribution entirely)

### How It Appears

PR descriptions show the attribution at the end:

```
## Summary
- Add user authentication
- Implement OAuth2 flow
- Add protected route middleware

## Testing
- Manual testing completed
- Unit tests passing

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## Configuration in settings.local.json

### Full Structure

```json
{
  "attribution": {
    "commit": "Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>",
    "pr": "🤖 Generated with [Claude Code](https://claude.com/claude-code)"
  }
}
```

### Setting Individual Fields

**Update commit only:**
```json
{
  "attribution": {
    "commit": "Co-Authored-By: Big Dawg <noreply@anthropic.com>",
    "pr": "🤖 Generated with [Claude Code](https://claude.com/claude-code)"
  }
}
```

**Update PR only:**
```json
{
  "attribution": {
    "commit": "Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>",
    "pr": "Created with AI assistance"
  }
}
```

**Remove commit attribution:**
```json
{
  "attribution": {
    "commit": "",
    "pr": "🤖 Generated with [Claude Code](https://claude.com/claude-code)"
  }
}
```

**Remove PR attribution:**
```json
{
  "attribution": {
    "commit": "Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>",
    "pr": ""
  }
}
```

**Remove both:**
```json
{
  "attribution": {
    "commit": "",
    "pr": ""
  }
}
```

---

## Common Customization Patterns

### 1. Personalized AI Name

Give Claude a custom name while keeping the format:

**Commit:**
```
Co-Authored-By: My AI Assistant Sonnet 4.5 <noreply@anthropic.com>
```

**PR:**
```
🤖 Generated with [My AI Assistant](https://claude.com/claude-code)
```

### 2. Minimal Attribution

Keep it simple without details:

**Commit:**
```
Co-Authored-By: AI <noreply@anthropic.com>
```

**PR:**
```
AI-generated
```

### 3. Detailed Attribution

Provide more context:

**Commit:**
```
This work was created with AI assistance from Claude Code.
For more information, visit https://claude.com/claude-code

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**PR:**
```
This pull request was generated with AI assistance.
Tool: Claude Code
Model: Claude Sonnet 4.5
Learn more: https://claude.com/claude-code
```

### 4. Professional Style

Formal, corporate-friendly attribution:

**Commit:**
```
Co-Authored-By: Claude Code Assistant <noreply@anthropic.com>
```

**PR:**
```
Generated using Claude Code AI assistant
```

### 5. Fun/Casual Style

Playful, personality-driven attribution:

**Commit:**
```
Co-Authored-By: Big Dawg 🐕 <noreply@anthropic.com>
```

**PR:**
```
✨ Crafted with care by Big Dawg and [Claude Code](https://claude.com/claude-code) ✨
```

### 6. Company-Specific

Align with company conventions:

**Commit:**
```
Co-Authored-By: AI Assistant <ai@company.com>
```

**PR:**
```
Generated with Company AI Assistant powered by Claude Code
```

---

## Escaping and Special Characters

### In JSON Configuration

When configuring in JSON, escape special characters:

**Quotes:**
```json
{
  "commit": "Co-Authored-By: \"The AI\" <ai@example.com>"
}
```

**Newlines:**
```json
{
  "commit": "AI-generated content\n\nCo-Authored-By: Claude <noreply@anthropic.com>"
}
```

**Backslashes:**
```json
{
  "pr": "Generated with [Claude](https://claude.com\\path)"
}
```

### In Git Trailers

Git trailers support multi-line values with continuation:

```
Co-Authored-By: Claude Sonnet 4.5
  <noreply@anthropic.com>
```

But simpler to keep on one line:
```
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

## Validation Rules

### Commit Attribution

**Valid:**
- Git trailer format: `Key: Value`
- Email in angle brackets if included
- Multiple lines allowed
- Empty string allowed

**Invalid:**
- Malformed email (missing brackets)
- Invalid git trailer syntax
- Null value (use empty string instead)

**Examples:**

✅ Valid:
```
Co-Authored-By: Claude <noreply@anthropic.com>
```

✅ Valid (no email):
```
Generated with AI
```

❌ Invalid:
```
Co-Authored-By: Claude noreply@anthropic.com  // Missing brackets
```

### PR Attribution

**Valid:**
- Any plain text
- Markdown formatting
- Emojis
- Links
- Multiple lines
- Empty string

**Invalid:**
- Null value (use empty string instead)

**Examples:**

✅ Valid:
```
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

✅ Valid:
```
Created with AI
```

✅ Valid (markdown):
```
## AI Attribution
Generated with Claude Code
```

---

## Backwards Compatibility

### Deprecated: includeCoAuthoredBy

Older Claude Code versions used `includeCoAuthoredBy` boolean:

```json
{
  "includeCoAuthoredBy": true
}
```

**Migration:**
- `"includeCoAuthoredBy": true` → Use default attribution
- `"includeCoAuthoredBy": false` → Set `commit: ""` and `pr: ""`

The `attribution` setting takes precedence if both are present.

---

## Best Practices

1. **Be Consistent:** Use the same style across your projects
2. **Keep It Simple:** Don't over-complicate the attribution
3. **Respect Standards:** Use `Co-Authored-By` for git trailers
4. **Test Visibility:** Check how attribution appears on your Git platform
5. **Consider Audience:** Adjust formality based on project context
6. **Update Sparingly:** Don't change attribution frequently
7. **Document Choices:** If using custom attribution, document why

---

## Platform-Specific Notes

### GitHub
- Recognizes `Co-Authored-By` trailer
- Shows co-authors on commit page
- Credits co-authors in contribution graphs
- Links email to GitHub account if registered

### GitLab
- Supports `Co-Authored-By` trailer
- Shows co-authors on commit details
- Links to user profile if email matches

### Bitbucket
- Displays git trailers in commit message
- Does not parse `Co-Authored-By` specially

### Git
- Git trailers are standard git feature
- `git interpret-trailers` command parses them
- Preserved across git operations (rebase, cherry-pick, etc.)
