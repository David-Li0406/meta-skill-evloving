# AI-Human Collaboration in Documentation (2026)

In 2026, technical writing is a collaborative effort between human experts and AI agents. This guide defines the roles and responsibilities of each.

## 1. The Role of the AI Agent

-   **Drafting**: AI is excellent at generating initial drafts from code comments or PR descriptions.
-   **Verification**: Automated checking of links, code snippets, and style guide compliance.
-   **Refactoring**: AI can quickly restyle an entire directory of documents to match a new standard (like this refactor).
-   **Synchronization**: Automatically identifying gaps between implementation (e.g., a new Prisma model) and documentation.

## 2. The Role of the Human Editor

-   **Accuracy**: AI can hallucinate; humans must verify technical "truth."
-   **Vibe Check**: Ensuring the tone is appropriate for the target audience.
-   **Strategic Direction**: Deciding *what* needs to be documented and at what level of detail.
-   **Ethics and Safety**: Ensuring documentation does not expose vulnerabilities or bias.

## 3. The "AI-First" Workflow

1.  **Code Commit**: Developer pushes code with docstrings.
2.  **Sync Audit**: The `docs-sync` skill identifies that a new feature lacks a page.
3.  **AI Drafting**: AI generates a `temp-page.md` based on the code analysis.
4.  **Human Review**: The human expert reviews, edits, and approves the draft.
5.  **Merge**: The documentation is integrated into the main branch.

## 4. Documentation as Code (DaC)

-   Docs should live in the same repository as the code.
-   CI/CD pipelines should "lint" documentation just like they lint code.
-   Use `repomix` to bundle code context for the AI when asking it to write documentation.

## 5. Handling Hallucinations

If an AI generates incorrect documentation:
-   **Trace the Source**: Did the AI misinterpret a comment or guess a default?
-   **Fix the Source**: Update the code docstrings to be more explicit.
-   **Update the Prompt**: Provide more context in the `docs-pro` instructions.

---
*Updated: January 22, 2026 - 17:00*
