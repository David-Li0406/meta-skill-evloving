---
name: pull-request-description
description: Pull request description generation instructions
argument-hint: N/A
---

# Pull Request Description Instructions

## Format

Follow this structure when generating pull request descriptions:

```markdown
# [Title - short, descriptive summary]

## ✅ Type of PR

- [ ] Refactor
- [ ] Feature
- [ ] Bug Fix
- [ ] Optimization
- [ ] Documentation Update

## 🗒️ Description

[Concise description focusing on functional changes, not technical details]

## 🚶‍➡️ Behavior

- [User-facing behavior changes]
- [Focus on user experience]
- [Be precise, not vague]

## 🧪 Steps to test

- [ ] [Step 1]
- [ ] [Step 2]
- [ ] [Step 3]
```

## Guidelines

1. **Title**: Short but descriptive, captures the essence of the change
2. **Type**: Select at least one type based on commit history
3. **Description**:
   - Keep it concise
   - Focus on **what** changed functionally
   - Highlight important details in **bold**
   - Avoid deep technical implementation details
4. **Behavior**:
   - Summarize user-facing changes
   - Use bullet points
   - Focus on the user experience
   - Be precise and specific
5. **Steps to test**:
   - Provide clear testing steps
   - Use checkboxes for clarity
   - Focus on functional validation
   - Exclude installation/setup steps

## Example

```markdown
# Add user authentication with OAuth2

## ✅ Type of PR

- [x] Feature

## 🗒️ Description

Implements OAuth2 authentication flow allowing users to sign in with Google and GitHub. Adds **session management** and **token refresh** capabilities.

## 🚶‍➡️ Behavior

- Users can now sign in using their Google or GitHub accounts
- Sessions persist across browser restarts
- Automatic token refresh prevents unexpected logouts
- Clear error messages for authentication failures

## 🧪 Steps to test

- [ ] Click "Sign in with Google" and complete OAuth flow
- [ ] Verify session persists after browser restart
- [ ] Click "Sign in with GitHub" and complete OAuth flow
- [ ] Test logout functionality
- [ ] Verify error handling with invalid credentials
```

## Tips

- Base the description on the actual commits in the PR
- Ensure all sections are filled out
- Keep language clear and non-technical for stakeholders
- Link to related issues when applicable
- Highlight breaking changes prominently
