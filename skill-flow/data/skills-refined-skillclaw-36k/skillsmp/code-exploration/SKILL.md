---
name: code-exploration
description:
  Explore the codebase to find relevant files and information. Use when the user asks to "explore the codebase", "find the code for", or even when simply mentioning editing the codebase (the user needs to know what files to edit).
model: claude-haiku-4-5
allowed-tools:
  - Bash(fd*)
  - Bash(rg*)
  - Bash(wc*)
  - Bash(sort*)
  - Bash(jq*)
---

# Code Exploration

## TODOs

- scripts:
  - find all packages in monorepo
  - find X dep in any package deps, using `fd` and `jq`
  - find declarations

- checklist:
  - [ ] list of all packages in the monorepo
  - [ ] package relationships
  - [ ] each package's architecture + important dependencies (RN, Uniwind,
        Tanstack Query, Zustand, etc)
  - [ ] understand feature organization
    - listed all recursive dirs in `expo/**`, which is good!
      - lists all feature dir names, route dirs, and top-level dirs
  - [ ] existing UI patterns
    - 1 feature dir's files, 1 route dir's files, ALL /ui/* component files
  - [ ] example files that were read:
    - tab route _layout.tsx
    - features/sessions/components/session-card.tsx
    - text and input ui components
    - features/sessions/hooks/use-sessions.ts
    - constants/colors.ts

- issues with normal explorer:
  - `ls` prints permissions, my username, LOC, month/day, and file name
  - `fd` prints ENTIRE absolute path for each dir
