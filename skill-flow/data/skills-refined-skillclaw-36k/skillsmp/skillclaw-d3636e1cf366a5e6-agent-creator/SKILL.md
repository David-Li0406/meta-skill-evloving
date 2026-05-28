---
name: agent-creator
description: Use this skill when you want to create, configure, and refine AI Agents tailored to specific tasks or domains.
---

# Agent Creator

This skill provides a structured process for designing and configuring specialized AI Agents.

## When to Use

Use this skill when you need to:
1.  **Create a New Agent**: Define a purpose-built agent with specific expertise (e.g., "Make a Frontend Specialist Agent").
2.  **Generate System Prompts**: Create robust, effective system instructions for an agent.
3.  **Assemble Capabilities**: Select the right combination of Skills, Workflows, and Rules for a specific domain.
4.  **Refine Agent Behavior**: Specialize tuning of an existing agent's operational guidelines.

## Agent Architecture

An Agent in the Antigravity system is defined by a markdown file in `.agent/agents/{name}.md` containing:

### 1. Frontmatter (Metadata)
-   `name`: Kebab-case identifier (e.g., `backend-specialist`).
-   `description`: Short summary and trigger keywords.
-   `tools`: List of tools the agent has access to (e.g., `Read, Write, Bash`).
-   `model`: The model usage strategy (usually `inherit`).
-   `skills`: Comma-separated list of skills from `.agent/skills/` this agent needs.

### 2. Identity & Charter
-   **Role**: Who the agent is.
-   **Philosophy**: Core beliefs driving decisions.
-   **Mindset**: Operational mode and priorities.

### 3. Critical Guidelines (The "Stop & Ask" Protocol)
-   **CRITICAL: CLARIFY BEFORE CODING**: A mandatory section forcing the agent to ask clarifying questions before making assumptions about stack, runtime, or tools.

### 4. Decision Frameworks
-   Tables and logic guides to help the agent make technical decisions (e.g., "Node vs Python", "SQL vs NoSQL").

### 5. Capabilities & Specialized Lists
-   **Expertise Areas**: Deep dive into specific techs.
-   **Quality Control Loop**: Mandatory steps to run after every edit.

## Workflow: Creating an Agent

Follow these steps to create a new Agent.

### Step 1: Define the Goal
Ask the user for the Agent's primary purpose.
*   *Prompt*: "What is the primary goal of this agent? What domain does it specialize in?"

### Step 2: Select Capabilities (Skills)
Analyze the available Skills in `.agent/skills/` to recommend the best set to include in the `skills` frontmatter.