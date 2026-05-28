---
name: PrototypeReference
description: Instructions for using the prototype at .prototype/code.html as a non-project reference.
---

# Prototype Reference Skill

This skill provides instructions on how to handle references to the prototype code located at `.prototype/code.html`.

## Context
The file `.prototype/code.html` is a standalone prototype/mockup of the application's UI or logic. It is **NOT** a part of the active project source code and should not be modified, moved, or deleted unless explicitly requested.

## Usage Instructions
When the user mentions "the prototype", "using the prototype", or refers to the code in `.prototype/code.html`:

1.  **Read-Only Reference**: You may use the source code in `.prototype/code.html` as a reference for:
    *   UI components and layout.
    *   CSS styles or themes.
    *   Basic client-side logic or structure.
2.  **Explicit Context**: Always treat this code as external to the main project. If you copy logic or styles from it, ensure they are adapted to the current project's stack (e.g., React, TypeScript, Vite, etc.) as described in the project's documentation.
3.  **Do Not Sync**: Do not attempt to "sync" the project with this file automatically. It is a snapshot for inspiration or reference only.
4.  **Verification**: If the user asks to implement something "like the prototype", read the file first using `view_file` to ensure you have the latest reference.

## File Path
- **Prototype Source**: `/Users/rolasnajera/development/gerai/.prototype/code.html`
