# The Gosling Core Protocol
**NOTE: All operational logic is now governed by the GSD (Get Shit Done) Protocol in `rules/operating_directives.md`.**

This skill defines the architectural guidelines for Gosling2.

## 1. Architectural Guidelines
*   **Service Layer**: Business logic goes here (`src/business`).
*   **Presentation Layer**: UI widgets go here (`src/presentation`).
*   **Data Layer**: Repositories and Models go here (`src/data`).
*   **Encouraged Separation**: Try to keep UI and Data layers separate. If you notice a violation in a file you're editing, mention it in **Field Notes** but do not let it block the task.

## 2. Structural Health
*   **Avoid Bloat**: Keep methods focused. If a file is reaching 600 lines, log it in Field Notes as a refactoring candidate.
*   **Progressive Cleanup**: Clean as you go, but never at the expense of functionality.

## 3. The Laws (Regression Guard)
The following features are sensitive. If you touch code related to these, double-check your logic:

1.  **Alias Redirection**: Clicking an Alias/Member chip MUST redirect to the Primary Identity.
2.  **Unlink = Split**: Removing an alias MUST split it into a NEW Identity.
3.  **Merge = Combine**: Adding a Person to a Person MUST merge their Identities.

## 4. Interaction Style
*   **Direct & Technical**: Use technical language when discussing code, but keep the UI simple for the Night Shift DJ.
*   **No Fluff**: No apologies, no filler. Just the status of the GSD loop.

