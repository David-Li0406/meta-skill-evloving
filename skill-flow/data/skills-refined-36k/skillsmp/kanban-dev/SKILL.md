---
name: kanban_dev
description: Expert knowledge for developing, porting, and integrating the Vibe Kanban application with KOR SDK.
---

# Kanban Dev Skill

This skill provides the context and guidelines for creating the **KOR Kanban** application, based on the [Vibe Kanban](https://github.com/BloopAI/vibe-kanban) project.

## 1. Architecture Overview

### Reference Architecture (Vibe Kanban)

- **Frontend**: React (Vite), TypeScript, Tailwind CSS, Shadcn UI, Framer Motion, Zustand, React Query.
- **Backend (Original)**: Rust (Axum, SQLx, SQLite).
- **Core Concept**: Manages "Agents" and "Tasks" (Kanban cards) to orchestrate coding workflows.

### Target Architecture (KOR Kanban)

- **Frontend**: Ported React application using the "Incredible UI" standards.
- **Backend**: Python-based (KOR SDK Integration).
  - The Rust backend logic (Task persistence, Agent execution) should be mapped to KOR's `Agent` and `Task` primitives.
  - **Integration Point**: A local FastAPI server or direct Python integration to serve the frontend API.

## 2. Directory Structure Knowledge

When working with the reference code (`temp_vibe_kanban`):

- `frontend/src/components/ui`: Base UI components (Buttons, Inputs) - heavily styled with Tailwind.
- `frontend/src/components/tasks`: Kanban board logic (Columns, Cards, Drag & Drop).
- `frontend/src/stores`: Zustand state stores (Global state).
- `frontend/src/hooks`: Custom React hooks.

## 3. UI/UX Guidelines ("Incredible UI")

- **Visuals**: Use "Vibe" aesthetics—glassmorphism, fluid animations (Framer Motion), dark mode by default.
- **Interactivity**: Everything should feel alive. Hover states, drag feedback, instant updates.
- **Components**: Use `shadcn/ui` components as the foundation.

## 4. Porting Strategy

1. **Scaffolding**: Start with a fresh Vite + React + TypeScript setup in `apps/kor-kanban`.
2. **Dependencies**: Install `framer-motion`, `tailwindcss`, `clsx`, `tailwind-merge`, `@dnd-kit/core`.
3. **Component Migration**:
    - Copy `ui` components first.
    - Copy `tasks` components, but **strip backend calls** initially. Replace with mock data or local state.
4. **Integration**:
    - defining a `useKanban` hook that adapters to KOR SDK's state.

## 5. Development Workflow

- Run `npm run dev` in `apps/kor-kanban` to test UI.
- Use `generate_image` (if needed) to visualize new UI concepts before coding complex CSS.
- Keep components small and focused.

## 6. Implementation Checklist

- [ ] Setup `apps/kor-kanban`
- [ ] Configure Tailwind & Shadcn
- [ ] Port/Create `KanbanBoard` component
- [ ] Implement Drag & Drop
- [ ] Connect to KOR Data
