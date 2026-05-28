---
name: writing-commit-messages
description: Write git commit messages for Tenzir repositories. Use when committing changes, running git commit, drafting commit messages, detecting staged changes, or asking about commit format and subject lines.
---

# Commit Message Writing

Write clear, consistent git commit messages in Tenzir projects.

## Format

```
<subject>

<body>
```

**Subject line:**

- Keep under 50 characters
- Use imperative mood ("Add feature" not "Added feature")
- Focus on user capability, not implementation
- Capitalize first letter
- No period at the end

**Body (optional):**

- Wrap at 72 characters
- Explain _what_ and _why_, not _how_
- Separate from subject with blank line

## Writing Style

**Perspective:** Write from users' capabilities and needs, not technical implementation.

Good: "Add DNS resolution operator"
Bad: "Implement dns_lookup in libtenzir"

**Voice:** Active voice, present tense.

Good: "Fix crash when input file is empty"
Bad: "Fixed a bug that was causing crashes"

## Examples

```
Add slice function for substring extraction
```

```
Fix crash when input file is empty

The parser assumed at least one byte of input. Now it handles
empty files gracefully by returning an empty result.

Resolves: #456
```

```
Remove deprecated export command

Use `to` instead. The export command has been deprecated since v4.0.
```

## Best Practices

- One logical change per commit—don't split a single change across commits
- Commit early and often; each commit should be a self-contained snapshot
- Order commits logically so dependencies appear in sequence
- Write for someone reading the log in 6 months
- Reference issues when relevant: `Resolves: #123` or `See also: #456`
- Use `git commit --fixup <SHA1>` for corrections meant to be squashed
