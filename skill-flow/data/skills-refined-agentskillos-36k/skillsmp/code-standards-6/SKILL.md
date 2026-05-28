---
name: code_standards
description: Project-specific coding standards and optimization rules for the Portfolio codebase.
---

# Code Standards

This skill defines the technical requirements and best practices for the Devon Nathan Portfolio project. Follow these rules for all code modifications and reviews.

## 1. Type Safety & Categories
- **Mandatory Typing**: Every variable declaration must include an explicit type. Avoid `any`.
- **Enums for Display**: Use String Enums for categories where the key and value are identical display-ready strings (e.g., `JavaScript = "JavaScript"`). This ensures a single source of truth for both logic and UI titles.
- **Single Source of Truth**: Derive arrays for looping using `Object.values(EnumName)` rather than hardcoding.

## 2. Performance & Optimization
- **Loop Minimization**: Avoid multiple `.filter()` calls on the same dataset.
- **Preprocessing**: Group or map data into appropriate structures (e.g., `Record<Enum, Item[]>`) before the `return` statement in components using `.reduce()`.
- **Dry Sections**: Render repeating visual sections (like skill categories) using a single `.map()` over the Enum values.
- **Unused Imports**: Always remove unused imports and dead code before finalizing a file.
- **Centralized Constants**: Shared configuration objects (like `IDENTITIES` or `TITLES`) must be defined in a single location within the `data/` directory and imported where needed. Never duplicate shared data across multiple components.

## 3. Visual & Aesthetic Consistency
- **Motion Orchestration**: Ensure `AnimatePresence` and `layout` props are used correctly to prevent layout shifts.
- **Theme Awareness**: Always use theme-aware color variables (e.g., `text-primary`, `text-text-muted`) rather than hardcoded colors.

## 4. Audit Findings
- **Responsive Grids**: Always check grid layouts on small screens to ensure `md:` and `lg:` breakpoints are balanced.
- **Service Categories**: Supported categories: `Infrastructure`, `Web`, `Blockchain`, `AI`.
- **Skill Categories**: Supported categories: `JavaScript`, `Python`, `Databases`, `Blockchain`.
- **Project Categories**: Supported categories: `Blockchain`, `AI`, `Full Stack`.
