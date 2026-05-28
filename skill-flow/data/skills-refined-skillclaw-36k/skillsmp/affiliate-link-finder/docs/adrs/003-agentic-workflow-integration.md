# ADR-003: Agentic Development Integration

**Status**: Accepted
**Date**: 2026-01-19
**Context**:
To scale development and maintain cognitive context, we offload rules and repetitive tasks to "Agents" within the IDE.

**Decision**:
We integrate a `.agent` directory structure:
1.  **Rules (`.agent/rules`)**: Enforce personality constraints (e.g., "ADHD Expert" ensures low cognitive load UI).
2.  **Skills (`.agent/skills`)**: Automate data gathering (e.g., "Affiliate-Link-Generator").
3.  **Workflows (`.agent/workflows`)**: Standardize complex tasks (e.g., `/fix` for automated debugging).

**Consequences**:
- **Positive**: Maintains high quality/consistency without mental strain on the developer. specific "ADHD Friendly" UI rules are enforced automatically.
- **Negative**: Requires maintenance of the `.agent` prompts as the project evolves.
