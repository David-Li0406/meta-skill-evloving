# Web Interface Guidelines Skill

A comprehensive skill that teaches AI agents best practices for designing
user-friendly, accessible, and performant web interfaces.

## Overview

This skill provides a set of rules and guidelines for building exceptional web
UIs. It uses **MUST**, **SHOULD**, and **NEVER** directives to guide
decision-making across all aspects of interface development.

## What's Included

| File                                               | Description                                 |
| -------------------------------------------------- | ------------------------------------------- |
| [SKILL.md](SKILL.md)                               | The main skill definition with metadata     |
| [references/REFERENCE.md](references/REFERENCE.md) | Detailed guidelines covering all UI aspects |

## Topics Covered

### 🎯 Interactions

- Keyboard accessibility (WAI-ARIA APG patterns)
- Focus management and visible focus rings
- Touch targets and mobile input considerations
- Hydration handling and paste behavior
- Loading states and feedback patterns

### 🎬 Animation

- `prefers-reduced-motion` support
- Compositor-friendly properties (`transform`, `opacity`)
- Interruptible, purposeful animations

### 📐 Layout

- Optical alignment and deliberate positioning
- Responsive design across devices
- Safe areas and overflow handling

### ♿ Content & Accessibility

- Semantic HTML and ARIA best practices
- Status cues and redundant visual indicators
- Internationalization and locale-aware formatting

### 📝 Forms

- Submission behavior and keyboard shortcuts
- Labels, validation, and error handling
- Password manager compatibility

### ⚡ Performance

- Re-render minimization
- List virtualization
- Image optimization and CLS prevention
- Web Workers for expensive operations

### 🎨 Design

- Layered shadows and crisp edges
- Color contrast (APCA-preferred)
- Theme color and dark mode support

### ✍️ Copywriting

- Active voice and clear language
- Consistent formatting and terminology
- Action-oriented, helpful error messages

## Usage

Reference this skill when building or reviewing web interfaces. The guidelines
help ensure your UI is:

- **Accessible** — Keyboard navigable, screen reader friendly
- **Fast** — Optimized rendering and minimal layout shifts
- **Delightful** — Responsive feedback and polished interactions
- **Consistent** — Predictable patterns and clear language

## Key Principles

1. **Full keyboard support** — Every interaction works without a mouse
2. **No dead zones** — If it looks clickable, it must be clickable
3. **Respect user preferences** — Honor reduced motion, zoom, and locale
4. **Guide users forward** — No dead ends; always offer a next step or recovery

## References

- [WAI-ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/patterns/)
- [APCA Contrast Calculator](https://apcacontrast.com/)
- [nuqs — URL State Management](https://nuqs.dev)
- [Vercel Web Interface Guidelines](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/refs/heads/main/AGENTS.md)
