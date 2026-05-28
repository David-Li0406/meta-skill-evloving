---
name: tailwind-css-v4
description: Use this skill when you want to implement Tailwind CSS v4 with CSS-first configuration, container queries, and modern design patterns in your web projects.
---

# Tailwind CSS v4 Patterns

## Overview

Tailwind CSS v4 introduces a CSS-first configuration approach, leveraging the Oxide engine for improved performance and native support for container queries. This skill provides guidance on utilizing Tailwind CSS v4 effectively in your projects.

## 1. Tailwind v4 Architecture

### Key Changes from v3

| v3 (Legacy)          | v4 (Current)                 |
|----------------------|------------------------------|
| `tailwind.config.js` | CSS-based `@theme` directive |
| PostCSS plugin       | Oxide engine (10x faster)    |
| JIT mode             | Native, always-on            |
| Plugin system        | CSS-native features          |
| `@apply` directive   | Still works, discouraged     |

### Core Concepts

| Concept            | Description                          |
|--------------------|--------------------------------------|
| **CSS-first**      | Configuration in CSS, not JavaScript |
| **Oxide Engine**   | Rust-based compiler, much faster     |
| **Native Nesting** | CSS nesting without PostCSS          |
| **CSS Variables**  | All tokens exposed as `--*` vars     |

## 2. CSS-Based Configuration

### Theme Definition

Define your theme using the `@theme` directive:

```css
@theme {
  /* Colors */
  --color-primary: oklch(0.7 0.15 250);
  --color-surface: oklch(0.98 0 0);
  --color-surface-dark: oklch(0.15 0 0);

  /* Spacing scale */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 2rem;

  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

### When to Extend vs Override

| Action              | Use When                                   |
|---------------------|--------------------------------------------|
| **Extend**          | Adding new values alongside defaults       |
| **Override**        | Replacing default scale entirely           |
| **Semantic tokens** | Project-specific naming (primary, surface) |

## 3. Container Queries

### Breakpoint vs Container

| Type                         | Responds To          |
|------------------------------|----------------------|
| **Breakpoint** (`md:`)       | Viewport width       |
| **Container** (`@container`) | Parent element width |

### Container Query Usage

| Pattern              | Classes                            |
|----------------------|------------------------------------|
| Define container     | `@container` on parent             |
| Container breakpoint  | `@sm:`, `@md:`, `@lg:` on children |
| Named containers      | `@container/card` for specificity  |

### When to Use

| Scenario               | Use                                   |
|------------------------|---------------------------------------|
| Page-level layouts     | Viewport breakpoints                  |
| Component-level        | Container queries                      |
| Reusable components     | Container queries (context-independent)|

## 4. Responsive Design

### Breakpoint System

| Prefix | Min Width | Target |
|--------|-----------|--------|
| (none) | 0px       | Mobile-first base |
| `sm`   | 640px     | Small devices |
| `md`   | 768px     | Medium devices |
| `lg`   | 1024px    | Large devices |
| `xl`   | 1280px    | Extra large devices |
| `2xl`  | 1536px    | 2x extra large devices |

## Conclusion

Utilize this skill to effectively implement Tailwind CSS v4 in your projects, taking advantage of its modern features and improved performance.