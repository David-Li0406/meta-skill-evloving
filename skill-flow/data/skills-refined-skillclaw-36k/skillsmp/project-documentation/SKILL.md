### /mnt/data2/nhlstats/.github/skills/project-documentation/SKILL.md
```markdown
1: ---
2: name: project-documentation
3: description: Guidelines for creating and maintaining a high-fidelity documentation ecosystem that serves as the single source of truth for developers, stakeholders, and AI agents.
4: version: 1.0.0
5: ---
6:
7: # Writing & Maintaining Project Documentation
8:
9: ## 🎯 Purpose
10: To create a high-fidelity documentation ecosystem that serves as the "single source of truth" for developers, stakeholders, and AI agents. The goal is to maximize clarity and minimize the "Time to First Commit" for new contributors.
11:
12: ## 📚 The Documentation Hierarchy
13: A project's health is measured by the accessibility of its information. Use the following structure:
14:
15: - **README.md (The Map)**: The entry point. Tells you what the project is, how to install it, and how to run it.
16: - **ADRs (The History)**: Architecture Decision Records. Documents the *why* behind significant technical choices.
17: - **Technical Docs (The Blueprint)**: Deep dives into system architecture, data flows, and API specifications.
18: - **SOPs/Skills (The How-To)**: Step-by-step guides for specific tasks (like this file).
19: - **Inline Docs (The Details)**: Docstrings and comments within the code for function-level context.
20:
21: ## ✍️ Writing Standards
22:
23: ### 1. The "Readability First" Rule
24: - **Use Active Voice**: "The function calculates the total," not "The total is calculated by the function."
25: - **Be Concise**: Use bullet points and headers to break up walls of text.
26: - **No Jargon Without Context**: Define project-specific acronyms upon first use.
27:
28: ### 2. Formatting & Visuals
29: - **Markdown Mastery**: Use code blocks for commands, bold text for UI elements, and tables for configuration parameters.
30: - **Diagrams as Code**: Use Mermaid.js or similar tools to embed diagrams. This allows version control to track changes in architecture visually.
31:
32: ## 🔄 Maintenance & Anti-Rot Strategy
33:
34: ### 1. The "Doc-as-Code" Workflow
35: - **PR Requirement**: If a Pull Request changes a feature, the documentation *must* be updated in the same PR.
36: - **Versioned Docs**: Ensure documentation matches the current version of the software (especially for APIs).
37:
38: ### 2. Automated Validation
39: - **Link Checking**: Use CI/CD tools (like `markdown-link-check`) to ensure no external links or internal references are broken.
40: - **Snippet Testing**: Whenever possible, use tools that test code snippets inside documentation to ensure they actually run.
41:
42: ## 🧹 Documentation Cleanup Checklist
43: - [ ] **Stale Content**: Remove instructions for deprecated features.
44: - [ ] **Searchability**: Ensure the README has a Table of Contents if it exceeds two scrolls.
45: - [ ] **Onboarding Test**: Can a new developer get the project running using only the README?
46: - [ ] **ADR Completion**: Is every major architectural change accompanied by an ADR?
47:
48: ## 🏷️ ADR Template (Quick Reference)
49: When creating a new Architecture Decision Record, include:
50:
51: - **Title**: Concise name of the decision.
52: - **Status**: Proposed / Accepted / Superseded.
53: - **Context**: What is the problem we are solving?
54: - **Decision**: What are we doing?
55: - **Consequences**: What are the trade-offs (positive and negative)?
```
