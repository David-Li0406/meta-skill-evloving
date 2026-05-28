---
name: Microservices Learning Platform
description: Coding standards and design principles for this project
---

# Project Skill: Microservices Learning Platform

## Design Principles

### Visual Identity
- **Theme**: Dark mode with purple/blue gradient accents
- **Style**: Glassmorphism, modern, premium feel
- **Typography**: Inter font for clean, readable text
- **Animations**: Subtle micro-animations for engagement

### Color Palette
```
Background: slate-950, slate-900, slate-800
Cards: white/5 with backdrop-blur (glassmorphism)
Primary: purple-500, purple-400
Secondary: blue-500, cyan-400
Text: slate-50 (headings), slate-300 (body), slate-500 (muted)
Accents: Gradient from purple-500 to blue-500
```

### Spacing & Layout
- Consistent padding: p-4, p-6, p-8
- Section spacing: py-16, py-24
- Card padding: p-6 or p-8
- Border radius: rounded-xl or rounded-2xl

---

## Code Standards

### JavaScript
- Use ES6+ features (arrow functions, destructuring, spread operator)
- Use `const` by default, `let` when reassignment is needed
- No `var` usage
- Use JSDoc comments for function documentation

### Components
- One component per file
- Use default exports
- Keep components focused and reusable
- Mobile-first responsive design

### File Naming
- Components: PascalCase (e.g., `ModuleCard.jsx`)
- Utils/hooks: camelCase (e.g., `useProgress.js`)
- Pages: lowercase with folders (e.g., `course/[module]/page.js`)

---

## Content Guidelines

### Teaching Approach
- Start simple, build complexity gradually
- Use real-world examples
- Include code snippets with syntax highlighting
- Add diagrams for architecture concepts
- Provide hands-on exercises

### Module Structure
1. **Objective**: What will the learner achieve?
2. **Theory**: Explain the concept
3. **Example**: Show real code
4. **Practice**: Hands-on exercise
5. **Summary**: Key takeaways
