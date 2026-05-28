---
name: create-pull-request
description: Use this skill when you need to create a well-structured pull request with a concise and informative description.
---

# Skill body

## Overview

This skill guides you through creating a pull request (PR) that is clear, concise, and ready for review. It emphasizes the importance of a well-structured description and title, ensuring that your changes are easily understood by reviewers.

## Steps to Create a Pull Request

1. **Verify Branch State**
   ```bash
   # Check current branch
   git branch --show-current

   # Ensure all changes are committed
   git status

   # View commits that will be included in the PR
   git log main..HEAD --oneline
   ```

2. **Review Changes**
   Before creating the PR, understand what you're submitting:
   ```bash
   # See all changes vs main branch
   git diff main...HEAD

   # List changed files
   git diff main...HEAD --name-only
   ```

3. **Create the Pull Request**
   Use the following command to create your PR:
   ```bash
   gh pr create --title "<type>: <short description>" --body "$(cat <<'EOF'
   ## Summary

   Brief description of what this PR does and why.

   ## Changes

   - <list key files/components changed>
   - <explain non-obvious implementation decisions>

   ## Testing

   - [ ] Unit tests added/updated
   - [ ] Integration tests pass
   - [ ] Manual testing completed

   ## Related Issues

   Closes #[issue-number]
   EOF
   )"
   ```

## Title Format
Follow conventional commit style for the title:
- `feat: add user dashboard`
- `fix: resolve cart duplication issue`

## Best Practices
- **Be Brief**: Keep descriptions concise; avoid walls of text.
- **Be Specific**: Focus on what changed and why, not how.
- **No Fluff**: Skip unnecessary sections like test plans unless truly needed.
- **PR Size**: Keep PRs small and focused; ideally under 400 lines.

## Anti-patterns
- Long descriptions that nobody reads.
- Copy-pasting commit messages as bullet points.
- Including "This PR does X" in the description.
- Test plan sections (CI runs tests automatically).