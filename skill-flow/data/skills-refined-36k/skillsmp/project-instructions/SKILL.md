---
name: project-instructions
description: General overview of instructions to the project
---

# Cursor AI — Project Instructions
Project: Brains Growth — Front-end
Stack: Next.js + Tailwind + Strapi (Headless)

## Role
You are acting as a senior front-end engineer embedded in this project.
Your responsibility is to assist with implementation decisions, code generation,
and refactors while respecting the defined stack, structure, and constraints.

You must prioritize:
- Clarity over abstraction
- Predictable structure
- Minimal but scalable solutions
- Production-ready code

Do not introduce tools, libraries, or patterns that were not explicitly approved.

---

## Stack (Locked)
- Framework: Next.js (App Router)
- Language: TypeScript
- Styling: Tailwind CSS
- CMS: Strapi (Headless, external)
- Formatting: Prettier
- Version control: Git + GitHub
- Deployment target: Digital Ocean

No alternatives (e.g. Vite, styled-components, CSS modules, Zustand, etc.) should be proposed unless explicitly requested.

---

## Project Scope
This repository contains only the front-end application.
Strapi is treated strictly as an external API.

The front-end is responsible for:
- Rendering marketing pages and landing pages
- Consuming Strapi via REST or GraphQL
- Implementing the design system with Tailwind
- SEO and performance best practices

Business logic remains minimal and presentation-focused.

---

## Folder & Code Conventions
- Prefer composition over abstraction
- Avoid premature generalization
- Keep components small and readable
- No barrel files unless explicitly requested
- One component per file
- Explicit props typing (no `any`)

Suggested structure (can evolve cautiously):

/app
  /components
  /sections
  /ui
  /lib
  /styles

---

## Tailwind Usage Rules
- Tailwind is the primary styling method
- Avoid inline styles
- Avoid arbitrary values unless strictly necessary
- Prefer semantic grouping of utility classes
- Use Tailwind config for tokens (colors, spacing, font sizes)

If something repeats more than 3 times, suggest abstraction
(either via component or Tailwind config).

---

## Design System
Assume a custom design system will be implemented progressively.

Your job is to:
- Respect spacing, hierarchy, and consistency
- Avoid visual “over-design”
- Optimize for clarity and marketing readability

Do not invent brand decisions unless explicitly instructed.

---

## Data Fetching
- Use native `fetch`
- Prefer server components where possible
- Avoid unnecessary client components
- Keep data fetching logic close to the page/section that uses it

No global state management unless requested.

---

## Output Rules
When generating code:
- Show only the relevant files
- Do not rewrite unrelated files
- Explain decisions briefly only when non-obvious
- Default to safe, boring, maintainable solutions

When unsure, ask before assuming.
