---
name: tailwind-architect
description: >
  This skill should be used when generating, refactoring, or maintaining Tailwind CSS code.
  It enforces the Oxide CSS-first configuration model, @theme-based design tokens, v4.1-native utilities,
  and structured migration from Tailwind v3, while preventing legacy configuration, plugin usage,
  and arbitrary-value or hex-based styling.
license: MIT
---

# Tailwind CSS v4.1 Architect

## Purpose and Scope

Establish Tailwind CSS v4.1 as a CSS-first, token-driven system backed by the Oxide engine.  
Enforce v4.1-native utilities and prevent reintroduction of v3-era patterns such as JS configs,
plugin-based features, and arbitrary-value abuse.

Use this skill when:

- Authoring new Tailwind v4.1 styling for components or pages.
- Refactoring legacy Tailwind v3 or mixed code to v4.1.
- Setting up or reviewing the global Tailwind architecture for a project.

---

## 1. Context Discovery Protocol

Execute this sequence immediately when the skill is activated for a project.

1. **Audit Tailwind Version**
   - Inspect `package.json` for the `tailwindcss` dependency.
   - If the version is `< 4.0`, stop and signal that the project is not yet on v4.  
     - Suggest upgrading before applying this protocol.

2. **Locate Tailwind Entry Point**
   - Identify the CSS file containing `@import "tailwindcss";`.  
     - Treat this file as the **authoritative entry point** for theme and engine configuration.
   - Ignore `tailwind.config.js` and `tailwind.config.ts` by default.  
     - Only read them if the user explicitly asks for v3 → v4 migration.

3. **Load Migration Knowledge When Needed**
   - When the user requests help migrating legacy patterns or plugins, consult  
     `references/v3-to-v4-migration.md` to map v3 constructs to v4.1-native architecture.

---

## 2. Core Configuration Model

Apply the Tailwind CSS v4.1 configuration model as follows.

1. **CSS-First Configuration**
   - Assume Tailwind runs in **CSS-first mode** with Oxide.
   - Use the entry CSS file to define configuration, not JS.

2. **@theme as Single Source of Tokens**
   - Place all design tokens in an `@theme` block:
     - Colors (prefer OKLCH),
     - Typography,
     - Spacing and layout scales,
     - Animation tokens.

3. **Forbidden / Required Behaviour**
   - **FORBIDDEN:** Create, edit, or rely on `tailwind.config.js` or `tailwind.config.ts`, except when explicitly migrating data from v3.
   - **REQUIRED:** Use `@theme` for any repeated visual decision instead of arbitrary values in markup.

Example pattern:

```css
@import "tailwindcss";

@theme {
  /* Colors (use OKLCH for P3 support) */
  --color-brand-primary: oklch(0.6 0.18 250);
  --color-brand-surface: oklch(0.95 0.02 250);

  /* Typography */
  --font-display: "Satoshi", sans-serif;
  --font-body: "Inter", sans-serif;

  /* Spacing / layout */
  --spacing-container: 1440px;
  --spacing-sidebar: 16rem;
}
```

---

## 3. Reasoning Loop for Each Styling Request

Apply this loop for every styling or refactoring request.

### 3.1 Check Native Capability

- Prefer native v4.1 utilities; do not suggest plugins.

### 3.2 Token Management

- Use utilities for layout; add or reuse tokens for design decisions.

### 3.3 Syntax Validation

- Reject plugins, hex colors, arbitrary values, and overuse of `@apply`.

---

## 4. Workflows

Use `assets/globals-template.css` for new global or update styling.
Use `references/v3-to-v4-migration.md` for migration mapping.

---
