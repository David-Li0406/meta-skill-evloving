---
name: Agent Optimization
description: Analyze and improve the AI agent workforce system, ensuring compatibility across environments (CLI, IDE, GitHub) and leveraging emerging technologies.
---

# Agent Optimization Skill

Use this skill to act as a **Systems Architect** or **Meta-Agent** for the workspace. Your goal is to refine *how* agents work, not just *what* they do.

## Scope of Responsibility

You must consider the Agent Workspace in the context of:
1.  **Multiple Environments**:
    -   **CLIs**: Gemini CLI, Copilot CLI (Limited visualization, text-heavy).
    -   **IDEs**: Antigravity, VS Code (Rich UI, diff views, terminals).
    -   **CI/CD**: GitHub Actions (Non-interactive, script-based).
2.  **Diverse Intelligence**:
    -   Support for multiple LLM providers (Gemini, Claude, GPT), optimizing prompts for general understanding rather than model-specific quirks.
3.  **Emerging Technology**:
    -   Proactively suggest integrating new AI capabilities (e.g., vision-based testing, voice interactions) as they become available.

## Core Operations

### 1. System Audit
**Trigger**: "Audit the workspace" or "Check agent health"
**Procedure**:
1.  Scan `.agent/skills`, `.agent/workflows`, and `.agent/rules`.
2.  **Compatibility Check**: Are instructions clear for a CLI user? (e.g., "Open the browser" might fail in SSH; "Check the build log" is better).
3.  **Consistency Check**: Do all `SKILL.md` files follow the standard header format?
4.  **Gap Analysis**: Are we missing a skill for a frequent task (e.g., "Release Management")?

### 2. Refine Capabilities
**Trigger**: "Improve the [Skill Name] skill" or "Make code review better"
**Procedure**:
1.  Read the target `SKILL.md` or workflow.
2.  Analyze it for ambiguity.
3.  **Optimize**:
    -   Add edge case handling.
    -   Improve prompts for multi-LLM compatibility.
    -   Add "Context Awareness" steps (e.g., "Check `package.xml` before assuming dependencies").

### 3. Synthesize & Innovate
**Trigger**: "Suggest improvements" or "What new tech should we use?"
**Procedure**:
1.  Review `.agent/ROADMAP.md` to understand project goals.
2.  Propose new:
    -   **Skills**: e.g., "An agent specializing in converting ROS 1 bags to ROS 2".
    -   **Workflows**: e.g., "A GitHub Action workflow for auto-documenting PRs".
    -   **Tools**: Integration of new vector databases or memory systems.

## Output Format
When proposing changes, add them to **`.agent/ROADMAP.md`** under `## Backlog > ### System Improvements` (create the section if needed), using the Project Management ID format.
