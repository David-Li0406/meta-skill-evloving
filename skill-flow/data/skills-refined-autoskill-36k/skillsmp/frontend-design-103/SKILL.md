---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality and a clear aesthetic point-of-view. Use when asked to design/build or restyle any web UI (components, pages, dashboards, landing pages, posters/artifacts, or full apps) in React/Next/Vite/HTML/CSS, including typography, color systems, layout composition, and motion.
---

# Frontend Design

## Overview

Design and implement real, working UI with a bold, intentional aesthetic direction—while staying production-grade (accessible, responsive, performant, and consistent).

## Workflow

### 1) Establish context

- Identify **purpose**, **audience**, **constraints**, and **definition of done**.
- If requirements are missing, ask up to 3 targeted questions; otherwise proceed with best-effort assumptions and state them up front.
- Follow the project’s stack and conventions (React framework, styling system, component patterns) unless explicitly told to change them.

### 2) Commit to a bold direction

- Choose one extreme aesthetic and execute it with precision (e.g., brutally minimal, editorial/magazine, retro-futurist, industrial/utilitarian, luxury/refined, brutalist/raw, art deco/geometric, organic/natural, maximalist chaos).
- Write a 1–2 sentence **Design Direction** and 3–5 bullets for what makes it memorable (the “signature”).
- Avoid indecisive, evenly-distributed palettes and generic component patterns.
- Vary direction between tasks; do not converge on the same “default” look every time (avoid trendy autopilots like Space Grotesk unless explicitly required).

### 3) Build a small design system (tokens first)

- Define CSS variables/tokens early: typography, color palette, spacing rhythm, radii, shadows, borders, and motion curves/durations.
- Prefer a dominant “base” and sharp accents over timid multi-accent rainbow palettes.
- Reuse tokens everywhere (do not hardcode random values throughout components).

### 4) Compose layout intentionally

- Use unexpected composition (asymmetry, overlap, diagonal flow, grid breaks) when it supports the concept.
- Use negative space intentionally (or controlled density intentionally)—avoid default card grids unless the concept demands it.
- Make it responsive by design (fluid type scale, resilient grids, sensible breakpoints).

### 5) Add motion with restraint and impact

- Prefer one orchestrated “moment” (page load with staggered reveals) over scattered, noisy micro-animations.
- Use CSS-first where feasible; use a React motion library only if it’s already in the project (or if adding it is justified and acceptable).
- Respect accessibility: support `prefers-reduced-motion` and keep focus/keyboard flows stable.

### 6) Production-grade polish

- Cover interaction states: hover/active/disabled/loading/empty/error.
- Keep typography immaculate: line-length, line-height, letter-spacing, optical alignment, and hierarchy clarity.
- Keep accessibility non-negotiable: semantic HTML, ARIA only when needed, visible focus, keyboard navigation, and contrast.

## Aesthetics Guidelines (avoid “AI slop”)

### Typography

- Choose fonts that are characterful and context-appropriate; pair a distinctive display face with a refined body face.
- Avoid generic fonts (especially Arial, Roboto, Inter, and system defaults) unless the project or user mandates them.
- Use a real type scale; prefer fluid sizing (`clamp`) and deliberate rhythm over arbitrary sizes.

### Color & Theme

- Commit to a cohesive palette; use CSS variables for consistency.
- Prefer strong contrast and a clear accent strategy over safe, evenly-balanced color sprinkling.
- Avoid clichéd palettes (notably “purple gradient on white”) unless explicitly required.

### Motion

- Use animation to support comprehension and delight, not to decorate.
- Focus on one high-impact reveal sequence; use hover states sparingly but thoughtfully.
- Use scroll-triggered motion only when it adds meaning; keep it lightweight and avoid jank.
- Prefer CSS-only solutions when possible; when using JS-based motion, keep it lightweight and deterministic.

### Spatial Composition

- Break the grid with intent: asymmetry, overlap, and diagonal flows can be powerful when coherent.
- Choose density intentionally (generous negative space or tight editorial density), then execute consistently.

### Backgrounds & Visual Details

- Create atmosphere and depth: gradient meshes, noise/grain, geometric patterns, layered transparencies, dramatic shadows, decorative borders.
- Consider custom cursors and textures only when they fit the concept and do not harm usability.
- Keep effects context-matched; avoid trendy defaults that feel copy/pasted.

## Output Standard

- Implement real working code, not just design concepts.
- Prefer minimal, well-placed dependencies; do not introduce heavy UI kits unless asked.
- Match implementation complexity to the aesthetic vision (maximalist designs can earn elaborate effects; minimal designs must be precise and restrained).
- Deliver a cohesive UI that feels deliberately designed for the specific context, not like a generic template.
