---
name: gemini-cli-init
description: Initialize Gemini CLI integration for PACK auditor workflow
metadata:
  short-description: Setup Gemini CLI as auditor
---

# Gemini CLI Initialization

## When to use

Use this skill when setting up a new project to use Gemini CLI as an auditor agent, or when onboarding a repository to the PACK multi-agent workflow with Gemini integration.

## Procedure

1. Verify Gemini CLI is installed:
   ```bash
   which gemini && gemini --version
   ```
   If not installed: `npm install -g @google/gemini-cli`

2. Verify version is 0.24.0 or higher. If not, update:
   ```bash
   npm install -g @google/gemini-cli@latest
   ```

3. Create project-level Gemini configuration:
   ```bash
   mkdir -p .gemini/personas
   cp .agent/gemini/settings.json.template .gemini/settings.json
   cp .agent/gemini/personas/auditor.md .gemini/personas/auditor.md
   ```

4. Create task and plan files if they do not exist:
   ```bash
   touch .agent/task.md .agent/implementation_plan.md
   ```

5. Verify setup with test invocation:
   ```bash
   export GEMINI_SYSTEM_MD="./.gemini/personas/auditor.md"
   echo "Hello, identify yourself" | gemini --model gemini-2.5-pro -y
   ```
   Expect response identifying as "Lead Solutions Architect".

6. (Optional) Add to .gitignore if not already present:
   ```
   .gemini/
   ```

## Inputs and outputs

- Inputs: Gemini CLI installed, Google account authenticated
- Outputs: `.gemini/` directory configured for auditor workflow

## Constraints

- Requires npm for Gemini CLI installation
- Requires Google account authentication (run `gemini` once to authenticate)
- Model availability depends on your Gemini API access tier

## Examples

```bash
# Quick setup
$gemini-cli-init

# Manual verification
gemini --version
ls -la .gemini/
```
