---
name: Knowledge Distiller
description: Transforms raw research or summaries into actionable, structured Knowledge Base articles.
---

# Knowledge Distiller Skill

This skill acts as a **Senior Knowledge Architect**, taking raw information and structuring it into a rigorous Personal Knowledge Base (PKB) note.

## Integration Workflow
1.  **Input**: A raw "Research Report" or "Summary" (e.g., from `kagi-search`).
2.  **Distill**: Run `distill.cjs` to generate the **Architect Template**.
3.  **Agent Action**: The Agent (you) must then:
    *   **Adopt Persona**: You are the Senior Technical Writer.
    *   **Fill Template**: Adhere to the *4-Quadrant Model* (Theory, Tutorial, How-To, Reference).
    *   **Link**: Use standard Markdown links `[label](path)` profusely to build the "Spiderweb" of knowledge.
    *   **Save**: Save to the appropriate `KB/` subdirectory.

## Usage
```bash
node .agent/skills/knowledge-distiller/scripts/distill.cjs "KB/Summaries/my_research.md"
```

## Template Standards
The Output Template enforces:
*   **Executive Summary**: ELI5.
*   **Core Concepts**: Mental Models.
*   **Usage**: Step-by-step.
*   **Reference**: Hard data.
*   **Graph Connections**: Upstream/Downstream/Lateral links.
