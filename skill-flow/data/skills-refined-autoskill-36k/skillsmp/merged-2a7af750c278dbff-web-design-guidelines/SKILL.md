---
name: web-design-guidelines
description: Review UI code for compliance with Web Interface Guidelines. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices".
---

# Web Interface Guidelines

Review files for compliance with Web Interface Guidelines.

## When to Use

Use this skill when a user requests to:
- Review UI/UX for accessibility or design issues.
- Audit a site against best practices.
- Check a specific feature or flow for UI guidelines.

## Philosophy

Aim for accessible, predictable interfaces that reduce user error and cognitive load. Prioritize clarity over novelty and fix issues based on user impact (accessibility → usability → visual polish). Use evidence from the UI and user flows, not personal taste.

## How It Works

1. Fetch the latest guidelines from the source URL below.
2. Read the specified files (or prompt user for files/pattern).
3. Check against all rules in the fetched guidelines.
4. Output findings in the terse `file:line` format.

## Guidelines Source

Fetch fresh guidelines before each review:

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

Use WebFetch to retrieve the latest rules.

## Usage

When a user provides a file or pattern argument:
1. Fetch guidelines from the source URL above.
2. Read the specified files.
3. Apply all rules from the fetched guidelines.
4. Output findings using the format specified in the guidelines.

If no files are specified, ask the user which files to review.

## Rules Overview

### Accessibility
- Ensure all interactive elements are accessible (e.g., `aria-label`, keyboard handlers).
- Use semantic HTML and provide alt text for images.

### Focus States
- Maintain visible focus on interactive elements and avoid removing outlines without replacements.

### Forms
- Ensure inputs have meaningful names and types, and provide inline error messages.

### Performance
- Optimize for large lists and avoid layout thrashing.

### Navigation & State
- Ensure URLs reflect the state of the application and provide confirmation for destructive actions.

### Anti-patterns
- Avoid common pitfalls such as disabling zoom or using inline click handlers on non-semantic elements.

## Output Format

Group findings by file using the `file:line` format. Provide terse findings without extensive explanations unless necessary.

```ts
## src/Button.tsx

src/Button.tsx:42 - icon button missing aria-label
src/Button.tsx:18 - input lacks label
```

## Remember

The agent is capable of extraordinary work in this domain. Use judgment, adapt to context, and push boundaries when appropriate.