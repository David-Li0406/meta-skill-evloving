---
name: github-pull-request
description: Generates GitHub pull request (PR) titles and descriptions from code changes. Use when creating PR, updating PR details, generating PR text for chat output, or when the user mentions pull request, PR, merge request, GitHub workflow, "write PR", "generate PR", "prepare PR text", or asks to show/create PR content.
license: Unlicense
---

# GitHub Pull Request

## Step-by-Step Process

1. **Read branch changes**: Carefully analyze all code changes in the current branch compared to the base branch
2. **Review commit history**: Understand the progression of changes and development timeline
3. **Identify main purpose**: Determine the core objective and impact of the changes
4. **Verify branch state**: Check if changes are already pushed to remote or if on default branch
5. **Create/checkout branch**: If needed, create a new branch or ensure working on proper feature branch
6. **Generate PR title**: Create concise, descriptive title (≤50 characters)
7. **Write PR description**: Include summary, motivation, context, and related issues
8. **Push changes**: Ensure all commits are pushed to remote repository
9. **Create or update PR**: Create new pull request or update existing one with generated content

## Language Requirement

- **ALWAYS write the entire PR in English only** - this includes title, description, and all sections
- Never use any other language for PR content

## PR Title Format

- Keep it concise and descriptive (ideally ≤50 characters)
- Use imperative mood (e.g., "Add feature" not "Added feature" or "Adds feature")
- Accurately reflect the main purpose of the changes
- Avoid technical jargon when possible
- Don't include issue numbers in title (use description for that)

### Title Examples

```text
Add dark mode support to theme package
```

```text
Fix input validation in text field component
```

```text
Refactor build configuration for better performance
```

## PR Description Structure

**Important**: Write all sections in English only.

### Required Sections

1. **Summary of Changes**
   - Brief overview of what was modified, added, or removed
   - List key changes using bullet points for clarity
   - Mention affected packages or modules

2. **Motivation and Context**
   - Explain why these changes were necessary
   - Provide background information or problem statement
   - Describe the impact on the project

3. **Related Issues/Tickets** (if applicable)
   - Reference related issues using GitHub syntax: `Fixes #123`, `Closes #456`, `Related to #789`
   - Provide context for issue relationships

### Optional Sections

- **Testing Notes**: How changes were tested or what manual testing is needed
- **Breaking Changes**: Clearly mark and explain any breaking changes
- **Migration Guide**: For breaking changes, provide migration instructions
- **Performance Impact**: For performance-related changes, include metrics

### Description Examples

```markdown
## Summary

This PR adds dark mode support to the theme package:

- Added dark color palette with semantic tokens
- Updated CSS variables for theme switching
- Added theme toggle component
- Updated documentation with usage examples

## Motivation

Users have requested dark mode support to reduce eye strain and improve accessibility. This implementation provides a complete theming solution that other packages can leverage.

## Related Issues

Fixes #42
```

```markdown
## Summary

Fixes input validation bug in the text field component:

- Fixed regex pattern for email validation
- Added edge case handling for empty strings
- Improved error message clarity

## Motivation

The previous email validation was rejecting valid email addresses with special characters. This caused user frustration during form submissions.

## Testing

- Added unit tests for edge cases
- Manually tested with various email formats
- Verified backward compatibility

Fixes #156
```

## Branch Management

### Creating a New Branch

- If currently on default branch (`master` or `main`), create a new feature branch
- Use descriptive branch names: `feature/description`, `fix/description`, `refactor/description`
- Never create PRs directly from default branch

### Checking Branch State

- Verify all changes are committed
- Ensure commits are pushed to remote repository
- Check if PR already exists for current branch

### Updating Existing PR

- If PR already exists, update title and description instead of creating new one
- Preserve existing PR metadata (reviewers, labels, assignees)
- Add a comment explaining what was updated

## Edge Cases and Best Practices

### When PR Already Exists

- Don't create duplicate PRs
- Update existing PR title and description
- Provide summary of what changed since last update

### For Breaking Changes

- Clearly mark breaking changes in title with `[BREAKING]` prefix or in description
- Provide detailed migration guide
- List all breaking changes in a dedicated section

### Writing Tone and Style

**Make PRs engaging and readable, not boring technical documents!**

- Use clear, simple language - avoid unnecessary jargon
- Write for reviewers who may not have full context
- Be concise but complete - include all necessary information
- Use proper Markdown formatting for readability
- **Add personality**: Write like a human, not a robot - tell the story of your changes
- **Use conversational tone**: Explain the "why" behind decisions in a natural way
- **Emojis in description body are OK** ✅ (but NOT in PR title) - they help visual scanning and add clarity
- **Show enthusiasm**: If you're proud of a solution, let it show!
- **Be honest about challenges**: Mention tricky parts or trade-offs you made

#### Examples: Boring vs Engaging

**😴 Boring (don't do this):**

```markdown
## Summary

Modified validation logic.
Updated tests.
Fixed edge case.
```

**🎉 Engaging (do this):**

```markdown
## Summary

Rewrote the email validation to handle all those weird edge cases we kept hitting! 🎯

- ✅ Now supports plus addressing (user+tag@example.com)
- ✅ Handles international domains correctly
- ✅ Added 15 new test cases for the tricky stuff
- 🐛 Fixed the bug where empty strings were passing validation (oops!)

## Why This Matters

Users were getting frustrated when their perfectly valid emails were rejected. Turns out our regex from 2015 wasn't cutting it anymore. This brings us up to RFC 5322 compliance and should handle 99% of real-world email formats.

## The Tricky Part

International domain names were a pain - had to use punycode conversion. Not the prettiest solution, but it works reliably across all browsers.
```

**Another example - feature PR:**

**😴 Boring:**

```markdown
Added dark mode.
Created toggle component.
Updated theme variables.
```

**🎉 Engaging:**

```markdown
## Summary

Finally bringing dark mode to life! 🌙✨

The community has been asking for this since forever, and it's ready to ship:

- 🎨 Complete dark color palette with semantic tokens
- 🔄 Smooth theme switching with CSS variable swaps
- 💾 Persists user preference to localStorage
- ♿ Respects system prefers-color-scheme
- 📦 New `<ThemeToggle>` component anyone can drop in

## How It Works

Instead of duplicating styles, we're using CSS custom properties that swap values based on a `[data-theme="dark"]` attribute on the root element. This means zero runtime overhead and instant theme switching! Pretty neat.

## What's Next

This lays the groundwork for user-customizable themes in the future. Right now it's just light/dark, but the architecture supports any number of themes.
```

### Monorepo Considerations

- Clearly indicate which packages are affected
- Group changes by package in the summary
- Consider using scoped PR titles like "feat(button): add loading state"

