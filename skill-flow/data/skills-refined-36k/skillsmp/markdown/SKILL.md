---
title: Markdown & MDX documentation rules for staystack-ts
description: Rules and conventions for writing MDX/Markdown documentation in the staystack-ts repository.
tags:
  - markdown
  - mdx
  - docs
  - editorial
name: markdown
---

# Markdown Skill (staystack-ts)

## What is it?

This skill codifies the repository's MDX/Markdown conventions: structure, style, formatting, and required content sections so documentation is consistent, machine-indexable, and useful for humans and RAG systems.

## Why use it?

- Keeps documentation consistent and searchable.
- Ensures content follows the "What/Why/How" pattern for clarity.
- Improves indexing and discoverability by enforcing frontmatter and tags.

## How to use it

1. Add a YAML frontmatter with `title`, `description`, and `tags` for every top-level MDX/Markdown file.
2. Structure pages with clear headings and prefer the "What is it? / Why use it? / How to use it?" pattern.
3. Use fenced code blocks with language tags for all code examples (e.g., `ts`, `bash`).
4. Use GitHub-style callouts for emphasis (e.g., `> [!NOTE]`).
5. Include sections: `Scalability & Performance`, `Security & Best Practices`, and `Limitations & Trade-offs` when the content is a feature or public API.

## Style & Visuals

> [!WARNING]
> Bold emphasis (double asterisks) must not be used in documentation files.

- Use headings (`#`, `##`, `###`) for hierarchy; avoid vague headings like "Introduction" or "Conclusion"—be specific (e.g., "What is it?", "How to use it?").
- Lists: use ordered (`1.`) or unordered (`-`) for any itemized content.
- Code blocks: always use fenced blocks with an appropriate language tag.
- Diagrams: use Mermaid for complex flows or architecture diagrams.
- Media: include high-quality screenshots or videos for UI features; prefer progressive loading for large media.

## Content & Structure requirements

- Every feature or top-level guide must include the three core sections: What / Why / How.
- Frontmatter MUST include `title`, `description`, and `tags` to support indexing and content discovery.
- Link related content using relative links for better knowledge graph construction.
- Include a `Scalability & Performance` section and a `Security & Best Practices` section for features and APIs.
- Explicitly list `Limitations & Trade-offs` (latency, concurrency, complexity) for any feature.

> [!NOTE]
> Use the "What / Why / How" structure for short pages and expand with examples and callouts for longer guides.

## Technical accuracy & examples

- When including code examples, use TypeScript with explicit types where applicable and mark status (Stable/Experimental/Deprecated).

Example frontmatter and snippet:

````plaintext

---
title: feature-x
description: "Short one-line description of Feature X"
tags: [feature, api]
---

## What is it?

Short explanation.

## Quick start

```ts
// TypeScript example with explicit types
const greet = (name: string): string => `hello ${name}`;
```

````

## Scalability & Performance

- Note performance characteristics and recommended limits.

## Security & Best Practices

- List security considerations and best practices.

## Limitations & Trade-offs

- Describe trade-offs and limitations.

```

## Validation & Quality

- Prefer short, focused pages. Break large topics into multiple pages.
- Ensure examples are copy-paste ready and runnable when possible.
- Run the repository's formatting tooling (Prettier) and follow the repository's linting guidance for any embedded code snippets.

## Governance

- Keep this SKILL as the canonical source for MDX/Markdown rules in the repo. Source rules are archived under `.claude/agents/skills/markdown/SKILL.md`.
- When rules change, update this SKILL and archive the prior version under `.claude/agents/skills/markdown/SKILL.md`.

## Limitations & trade-offs

- Strict formatting and frontmatter requirements add authoring overhead but improve discoverability and machine readability.
```

```

```
