---
name: git-commit-message-generator
description: Use this skill when you need to generate descriptive commit messages based on staged changes, ensuring adherence to the Conventional Commits format.
---

# Skill body

## Overview

This skill automatically generates conventional commit messages by analyzing the current staged changes in your Git repository. It is designed to help you create clear, consistent, and informative commit messages.

## When to Use

Activate this skill when the user:
- Mentions "commit", "committing", "staged changes", or "ready to commit"
- Shows `git add` or `git status` output with staged changes
- Asks "what should my commit message be?"
- Says "I need to commit my changes"
- Requests help writing commit messages

## Workflow

1. **Check for Staged Changes**:
   - Run `git diff --cached --name-status`.
   - If no staged files exist, prompt the user to stage changes using `git add .`.

2. **Analyze Staged Changes**:
   - Use `git diff --cached` to inspect the changes and determine the type of commit (e.g., `feat`, `fix`, `refactor`, etc.).

3. **Compose Commit Message**:
   - Format the message according to the Conventional Commits specification:
     ```
     <type>(<scope>): <subject>

     [optional body]
     ```
   - Choose `type` based on the changes:
     - `feat`: New feature
     - `fix`: Bug fix
     - `docs`: Documentation changes
     - `style`: Code style changes
     - `refactor`: Code refactoring
     - `test`: Adding or updating tests
     - `chore`: Maintenance tasks
   - Optionally include a `scope` to clarify the area of change.

4. **Display the Commit Message**:
   - Present the generated commit message to the user for review.

5. **Commit Changes**:
   - If the user approves, execute the commit using:
     ```bash
     git commit -m "type(scope): subject" -m "description..."
     ```

## Commit Message Guidelines

**DO:**
- Use imperative mood (e.g., "add feature" not "added feature").
- Keep the subject line under 72 characters.
- Capitalize the first letter of the subject.
- Explain the "why" in the body, not just the "what".

**DON'T:**
- Use vague messages like "update" or "fix stuff".
- Include technical implementation details in the summary.
- Write paragraphs in the summary line.
- Use past tense.

## Examples

**Feature commit:**
```
feat(auth): add JWT authentication

Implement JWT-based authentication system with:
- Login endpoint with token generation
- Token validation middleware
- Refresh token support
```

**Bug fix:**
```
fix(api): handle null values in user profile

Prevent crashes when user profile fields are null.
Add null checks before accessing nested properties.
```