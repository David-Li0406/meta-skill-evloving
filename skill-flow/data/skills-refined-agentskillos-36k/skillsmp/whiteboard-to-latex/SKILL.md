---
name: whiteboard_to_latex
description: Extracts content from a whiteboard image, converts it to academic LaTeX matching the user's existing note style, and saves it. Use when the user provides a whiteboard image requiring conversion to LaTeX notes.
---

# Whiteboard to LaTeX Conversion

This skill converts whiteboard images into LaTeX notes that seamlessly integrate with the user's current notebook.

## Core Resources

- **Style Guide**: `references/style_guide.md` - Strictly defines the valid environments and structure.
- **Template**: `assets/note_template.tex` - Standard note structure with all allowed environments.
- **Script**: `scripts/update_main_index.py` - Automatically ensures the new note is included in the main document.

## Workflow

### 1. Preparation

1.  **Context Check**: Confirm the user has created the target file (e.g., `L/L26.tex`) with the basic `\section{Notes X...}` header. If not, ask them to, or do it if explicitly requested.
2.  **Style Loading**: Read `references/style_guide.md` to load the allowed theorem environments and formatting rules into context. **Do not hallucinate new environments.**
3.  **Template Reference**: Optionally review `assets/note_template.tex` for standard environment usage patterns and formatting examples.

### 2. Vision & Transcription

1.  **Analyze Image**:
    -   Identify headers, main theorems, proofs, and examples.
    -   Transcribe text verbatim.
    -   Convert math to standard LaTeX.
2.  **Construct Content**:
    -   Use the environments from the Style Guide (`theorem`, `definition`, `remark`, etc.).
    -   **Important**: Follow the **Proof Handling** rule in the style guide (e.g., comment out proofs if required).
    -   **Fragments Only**: Do NOT write `\documentclass` or preamble. Only write the content body.

### 3. File Writing

Use `replace_file_content` (or `write_to_file` if overwriting) to populate the target `L/LX.tex` (or `T/TX.tex`) file.

### 4. Integration & Verification

1.  **Update Index**:
    -   Run `scripts/update_main_index.py` to ensure the new file is `\input` in `ODE.tex`.
    -   ```bash
        ./.agent/skills/whiteboard_to_latex/scripts/update_main_index.py L
        # Or
        ./.agent/skills/whiteboard_to_latex/scripts/update_main_index.py T
        ```
2.  **Verify**:
    -   Check if the file content looks correct (balanced braces, correct environments).
    -   Report back to the user: "Populated Notes X. Added to ODE.tex."
