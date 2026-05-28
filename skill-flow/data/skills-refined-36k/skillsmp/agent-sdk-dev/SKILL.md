---
name: agent-sdk-dev
description: A comprehensive plugin for creating and verifying Claude Agent SDK applications in Python and TypeScript.
---

# Agent SDK Development Plugin

A comprehensive plugin for creating and verifying Claude Agent SDK applications in Python and TypeScript.

## Overview

The Agent SDK Development Plugin streamlines the entire lifecycle of building Agent SDK applications, from initial scaffolding to verification against best practices. It helps you quickly start new projects with the latest SDK versions and ensures your applications follow official documentation patterns.

## Features

### Command: `/new-sdk-app`

Interactive command that guides you through creating a new Claude Agent SDK application.

**What it does:**
- Asks clarifying questions about your project (language, name, agent type, starting point)
- Checks for and installs the latest SDK version
- Creates all necessary project files and configuration
- Sets up proper environment files (.env.example, .gitignore)
- Provides a working example tailored to your use case
- Runs type checking (TypeScript) or syntax validation (Python)
- Automatically verifies the setup using the appropriate verifier agent

**Usage:**
```bash
/new-sdk-app my-project-name
```

Or simply:
```bash
/new-sdk-app
```

The command will interactively ask you:
1. Language choice (TypeScript or Python)
2. Project name (if not provided)
3. Agent type (coding, business, custom)
4. Starting point (minimal, basic, or specific example)
5. Tooling preferences (npm/yarn/pnpm or pip/poetry)

**Example:**
```bash
/new-sdk-app customer-support-agent
# → Creates a new Agent SDK project for a customer support agent
# → Sets up TypeScript or Python environment
# → Installs latest SDK version
# → Verifies the setup automatically
```

### Agent: `agent-sdk-verifier-py`

Thoroughly verifies Python Agent SDK applications for correct setup and best practices.

**Verification checks:**
- SDK installation and version
- Python environment setup (requirements.txt, pyproject.toml)
- Correct SDK usage and patterns
- Agent initialization and configuration
- Environment and security (.env, API keys)
- Error handling and functionality
- Documentation completeness

**When to use:**
- After creating a new Python SDK project
- After modifying an existing Python SDK application
- Before deploying a Python SDK application

**Usage:**
The agent runs automatically after `/new-sdk-app` creates a Python project, or you can trigger it by asking:
```
"Verify my Python Agent SDK application"
"Check if my SDK app follows best practices"
```

**Output:**
Provides a comprehensive report with:
- Overall status (PASS / PASS WITH WARNINGS / FAIL)
- Critical issues that prevent functionality
- Warnings about suboptimal patterns
- List of passed checks
- Specific recommendations with SDK documentation references

### Agent: `agent-sdk-verifier-ts`

Thoroughly verifies TypeScript Agent SDK applications for correct setup and best practices.

**Verification checks:**
- SDK installation and version
- TypeScript configuration (tsconfig.json)
- Correct SDK usage and patterns
- Type safety and imports
- Agent initialization and configuration
- Environment and security (.env, API keys)
- Error handling and functionality
- Documentation completeness

**When to use:**
- After creating a new TypeScript SDK project
- After modifying an existing TypeScript SDK application
- Before deploying a TypeScript SDK application

**Usage:**
The agent runs automatically after `/new-sdk-app` creates a TypeScript project, or you can trigger it by asking:
```
"Verify my TypeScript Agent SDK application"
"Check if my SDK app follows best practices"
```

**Output:**
Provides a comprehensive report with:
- Overall status (PASS / PASS WITH WARNINGS / FAIL)
- Critical issues that prevent functionality
- Warnings about suboptimal patterns
- List of passed checks
- Specific recommendations with SDK documentation references

## Workflow Example

Here's a typical workflow using this plugin:

1. **Create a new project:**
```bash
/new-sdk-app code-reviewer-agent
```

2. **Answer the interactive questions:**
```
Language: TypeScript
Agent type: Coding agent (code review)
Starting point: Basic agent with common features
```

3. **Automatic verification:**
The command automatically runs `agent-sdk-verifier-ts` to ensure everything is correctly set up.

4. **Start developing:**
```bash
# Set your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Run your agent
npm start
```

5. **Verify after changes:**
```
"Verify my SDK application"
```

## Installation

This plugin is included in the Claude Code repository. To use it:

1. Ensure Claude Code is installed
2. The plugin commands and agents are automatically available

## Best Practices

- **Always use the latest SDK version**: `/new-sdk-app` checks for and installs the latest version
- **Verify before deploying**: Run the verifier agent before deploying to production
- **Keep API keys secure**: Never commit `.env` files or hardcode API keys
- **Follow SDK documentation**: The verifier agents check against official patterns
- **Type check TypeScript projects**: Run `npx tsc --noEmit` regularly
- **Test your agents**: Create test cases for your agent's functionality

## Resources

- [Agent SDK Overview](https://docs.claude.com/en/api/agent-sdk/overview)
- [TypeScript SDK Reference](https://docs.claude.com/en/api/agent-sdk/typescript)
- [Python SDK Reference](https://docs.claude.com/en/api/agent-sdk/python)
- [Agent SDK Examples](https://docs.claude.com/en/api/agent-sdk/examples)

## Troubleshooting

### Type errors in TypeScript project

**Issue**: TypeScript project has type errors after creation

**Solution**:
- The `/new-sdk-app` command runs type checking automatically
- If errors persist, check that you're using the latest SDK version
- Verify your `tsconfig.json` matches SDK requirements

### Python import errors

**Issue**: Cannot import from `claude_agent_sdk`

**Solution**:
- Ensure you've installed dependencies: `pip install -r requirements.txt`
- Activate your virtual environment if using one
- Check that the SDK is installed: `pip show claude-agent-sdk`

### Verification fails with warnings

**Issue**: Verifier agent reports warnings

**Solution**:
- Review the specific warnings in the report
- Check the SDK documentation references provided
- Warnings don't prevent functionality but indicate areas for improvement

## Author

Ashwin Bhat (ashwin@anthropic.com)

## Version

1.0.0


# Workflow Instructions



## Command: new-sdk-app.md

---
description: Create and setup a new Claude Agent SDK application
argument-hint: [project-name]
---

You are tasked with helping the user create a new Claude Agent SDK application. Follow these steps carefully:

## Reference Documentation

Before starting, review the official documentation to ensure you provide accurate and up-to-date guidance. Use WebFetch to read these pages:

1. **Start with the overview**: https://docs.claude.com/en/api/agent-sdk/overview
2. **Based on the user's language choice, read the appropriate SDK reference**:
   - TypeScript: https://docs.claude.com/en/api/agent-sdk/typescript
   - Python: https://docs.claude.com/en/api/agent-sdk/python
3. **Read relevant guides mentioned in the overview** such as:
   - Streaming vs Single Mode
   - Permissions
   - Custom Tools
   - MCP integration
   - Subagents
   - Sessions
   - Any other relevant guides based on the user's needs

**IMPORTANT**: Always check for and use the latest versions of packages. Use WebSearch or WebFetch to verify current versions before installation.

## Gather Requirements

IMPORTANT: Ask these questions one at a time. Wait for the user's response before asking the next question. This makes it easier for the user to respond.

Ask the questions in this order (skip any that the user has already provided via arguments):

1. **Language** (ask first): "Would you like to use TypeScript or Python?"

   - Wait for response before continuing

2. **Project name** (ask second): "What would you like to name your project?"

   - If $ARGUMENTS is provided, use that as the project name and skip this question
   - Wait for response before continuing

3. **Agent type** (ask third, but skip if #2 was sufficiently detailed): "What kind of agent are you building? Some examples:

   - Coding agent (SRE, security review, code review)
   - Business agent (customer support, content creation)
   - Custom agent (describe your use case)"
   - Wait for response before continuing

4. **Starting point** (ask fourth): "Would you like:

   - A minimal 'Hello World' example to start
   - A basic agent with common features
   - A specific example based on your use case"
   - Wait for response before continuing

5. **Tooling choice** (ask fifth): Let the user know what tools you'll use, and confirm with them that these are the tools they want to use (for example, they may prefer pnpm or bun over npm). Respect the user's preferences when executing on the requirements.

After all questions are answered, proceed to create the setup plan.

## Setup Plan

Based on the user's answers, create a plan that includes:

1. **Project initialization**:

   - Create project directory (if it doesn't exist)
   - Initialize package manager:
     - TypeScript: `npm init -y` and setup `package.json` with type: "module" and scripts (include a "typecheck" script)
     - Python: Create `requirements.txt` or use `poetry init`
   - Add necessary configuration files:
     - TypeScript: Create `tsconfig.json` with proper settings for the SDK
     - Python: Optionally create config files if needed

2. **Check for Latest Versions**:

   - BEFORE installing, use WebSearch or check npm/PyPI to find the latest version
   - For TypeScript: Check https://www.npmjs.com/package/@anthropic-ai/claude-agent-sdk
   - For Python: Check https://pypi.org/project/claude-agent-sdk/
   - Inform the user which version you're installing

3. **SDK Installation**:

   - TypeScript: `npm install @anthropic-ai/claude-agent-sdk@latest` (or specify latest version)
   - Python: `pip install claude-agent-sdk` (pip installs latest by default)
   - After installation, verify the installed version:
     - TypeScript: Check package.json or run `npm list @anthropic-ai/claude-agent-sdk`
     - Python: Run `pip show claude-agent-sdk`

4. **Create starter files**:

   - TypeScript: Create an `index.ts` or `src/index.ts` with a basic query example
   - Python: Create a `main.py` with a basic query example
   - Include proper imports and basic error handling
   - Use modern, up-to-date syntax and patterns from the latest SDK version

5. **Environment setup**:

   - Create a `.env.example` file with `ANTHROPIC_API_KEY=your_api_key_here`
   - Add `.env` to `.gitignore`
   - Explain how to get an API key from https://console.anthropic.com/

6. **Optional: Create .claude directory structure**:
   - Offer to create `.claude/` directory for agents, commands, and settings
   - Ask if they want any example subagents or slash commands

## Implementation

After gathering requirements and getting user confirmation on the plan:

1. Check for latest package versions using WebSearch or WebFetch
2. Execute the setup steps
3. Create all necessary files
4. Install dependencies (always use latest stable versions)
5. Verify installed versions and inform the user
6. Create a working example based on their agent type
7. Add helpful comments in the code explaining what each part does
8. **VERIFY THE CODE WORKS BEFORE FINISHING**:
   - For TypeScript:
     - Run `npx tsc --noEmit` to check for type errors
     - Fix ALL type errors until types pass completely
     - Ensure imports and types are correct
     - Only proceed when type checking passes with no errors
   - For Python:
     - Verify imports are correct
     - Check for basic syntax errors
   - **DO NOT consider the setup complete until the code verifies successfully**

## Verification

After all files are created and dependencies are installed, use the appropriate verifier agent to validate that the Agent SDK application is properly configured and ready for use:

1. **For TypeScript projects**: Launch the **agent-sdk-verifier-ts** agent to validate the setup
2. **For Python projects**: Launch the **agent-sdk-verifier-py** agent to validate the setup
3. The agent will check SDK usage, configuration, functionality, and adherence to official documentation
4. Review the verification report and address any issues

## Getting Started Guide

Once setup is complete and verified, provide the user with:

1. **Next steps**:

   - How to set their API key
   - How to run their agent:
     - TypeScript: `npm start` or `node --loader ts-node/esm index.ts`
     - Python: `python main.py`

2. **Useful resources**:

   - Link to TypeScript SDK reference: https://docs.claude.com/en/api/agent-sdk/typescript
   - Link to Python SDK reference: https://docs.claude.com/en/api/agent-sdk/python
   - Explain key concepts: system prompts, permissions, tools, MCP servers

3. **Common next steps**:
   - How to customize the system prompt
   - How to add custom tools via MCP
   - How to configure permissions
   - How to create subagents

## Important Notes

- **ALWAYS USE LATEST VERSIONS**: Before installing any packages, check for the latest versions using WebSearch or by checking npm/PyPI directly
- **VERIFY CODE RUNS CORRECTLY**:
  - For TypeScript: Run `npx tsc --noEmit` and fix ALL type errors before finishing
  - For Python: Verify syntax and imports are correct
  - Do NOT consider the task complete until the code passes verification
- Verify the installed version after installation and inform the user
- Check the official documentation for any version-specific requirements (Node.js version, Python version, etc.)
- Always check if directories/files already exist before creating them
- Use the user's preferred package manager (npm, yarn, pnpm for TypeScript; pip, poetry for Python)
- Ensure all code examples are functional and include proper error handling
- Use modern syntax and patterns that are compatible with the latest SDK version
- Make the experience interactive and educational
- **ASK QUESTIONS ONE AT A TIME** - Do not ask multiple questions in a single response

Begin by asking the FIRST requirement question only. Wait for the user's answer before proceeding to the next question.

