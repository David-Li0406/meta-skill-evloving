---
name: reusable-apm-package
description: Use this skill when you want to create a reusable APM package that includes agent primitives and workflows.
---

# Skill body

## Overview

This skill guides you through the process of creating a reusable APM (Application Performance Monitoring) package that contains agent primitives and workflows.

## Getting Started

1. **Install the Package**:
   ```bash
   apm install your-org/{{project_name}}
   ```

2. **Compile the Package**:
   ```bash
   apm compile
   ```

## Package Structure

Your APM package will include the following components:

- **Instructions**: Define guardrails and standards in the `.apm/instructions/` directory.
- **Prompts**: Create executable workflows in the `.apm/prompts/` directory.
- **Agents**: Develop specialized personas in the `.apm/agents/` directory.

## Example Workflows

- `hello-world.prompt.md`: A simple hello world workflow to demonstrate basic functionality.
- `feature-implementation.prompt.md`: A workflow for implementing features within your application.

## Customization

Replace `{{project_name}}` and `{{description}}` with your specific project details to tailor the package to your needs.