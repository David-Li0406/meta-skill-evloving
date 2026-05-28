---
name: orchestrating-multi-agent-systems
description: Use this skill when you need to create and manage multi-agent systems, facilitating agent coordination, task routing, and complex workflows across various AI providers.
---

# Skill body

## Overview

This skill empowers Claude to create and manage sophisticated multi-agent systems using the AI SDK v5. It facilitates agent collaboration, task delegation, and intelligent routing, enabling the creation of complex AI-powered workflows.

## How It Works

1. **Project Initialization**: Sets up a basic multi-agent project structure, including agent files and orchestration configurations.
2. **Agent Creation**: Facilitates the creation of specialized agents with custom system prompts, tool definitions, and handoff rules.
3. **Orchestration Configuration**: Configures the agent orchestration workflow, defining how agents interact and pass tasks to each other.

## When to Use This Skill

This skill activates when you need to:
- Create a new multi-agent system from scratch.
- Orchestrate existing agents to perform a complex task.
- Define handoff rules between agents.
- Route tasks intelligently to the most appropriate agent.
- Coordinate a workflow involving multiple LLMs.

## Examples

### Example 1: Building a Code Generation Pipeline

User request: "Set up a multi-agent system for code generation with an architect, coder, tester, reviewer, and documenter."

The skill will:
1. Initialize a multi-agent project with the specified agents.
2. Create individual agent files (architect.ts, coder.ts, etc.) with relevant system prompts and tool access.
3. Configure an orchestration workflow to pass tasks between the agents in the order: Architect -> Coder -> Tester -> Reviewer -> Documenter.

### Example 2: Intelligent Routing for Customer Support

User request: "Create a multi-agent system for customer support that routes inquiries to the appropriate agent based on the topic."

The skill will:
1. Initialize a multi-agent project with a coordinator agent and specialized support agents (e.g., billing, technical support).
2. Configure routing rules to direct inquiries to the appropriate agent based on the topic.