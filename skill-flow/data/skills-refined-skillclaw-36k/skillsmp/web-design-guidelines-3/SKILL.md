---
name: web-design-guidelines
description: Use when reviewing UI, accessibility, or UX in web interfaces and you need to audit components against web design best practices.
---

# Web Design Guidelines (Vercel)

## Overview
Use this skill to audit UI code against Vercel’s Web Interface Guidelines. Focus on accessibility, focus states, forms, performance, and interaction rules.

## When to Use
- Reviewing UI for accessibility or UX issues
- Auditing new components for best practices
- Checking forms, dialogs, focus, or navigation behavior
- Verifying design consistency and interaction rules

## How It Works
1. Fetch the latest rules from:
   `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`
2. Read the specified files or ask which files to review
3. Compare code against the rules
4. Report findings using the output format in the guidelines

## Quick Reference
- Accessibility: aria-labels, semantic HTML, keyboard handlers
- Focus: visible focus, focus-visible, trap in dialogs
- Forms: labels, validation, error messaging
- Navigation: URL state, deep-linking, internal links
- Performance: image sizing, lazy loading, layout stability

## Example Trigger
"Review this modal for accessibility and focus handling." → Use this skill to fetch guidelines and audit the modal component.

## Common Mistakes
- Skipping the guideline fetch and relying on memory
- Reviewing without the file list or pattern
- Ignoring the required output format

Full reference: https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines
