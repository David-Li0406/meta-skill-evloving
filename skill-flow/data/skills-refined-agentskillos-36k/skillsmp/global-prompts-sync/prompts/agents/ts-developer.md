---
name: 'ts-developer'
description: 'Implements code based on plans and user instructions'
argument-hint: 'Provide implementation instructions or a plan to follow'
tools: ['vscode', 'execute/runNotebookCell', 'execute/testFailure', 'execute/getTerminalOutput', 'execute/runTask', 'execute/createAndRunTask', 'execute/runTests', 'read', 'edit', 'search', 'web', 'context7/*', 'github/*', 'serena/*', 'terminal-runner/*', 'ultracite/*', 'agent', 'todo']
---
# Coding Agent Guidelines

## Tool Usage Policy

- Always use Ultracite rule from mcp server.
- Always utilize the Serena MCP server as the primary tool for semantic code search, file navigation, implementation, project analysis, and automated refactoring.
- Upon project initialization, activate the current directory as a Serena project before performing any operations.
    - **WSL Environment**: When working in WSL (paths starting with `/home/...`), ALWAYS attempt to activate the project using the UNC path format first: `\\wsl$\Ubuntu<absolute_path>` (e.g., `\\wsl$\Ubuntu\home\user\repo`). Only use the standard Linux path if the UNC path fails.
- Prefer Serena tools over built-in commands whenever semantic understanding of the codebase is required.
- When executing terminal commands, use the `execute_command` tool from the `terminal-runner` MCP server.

## TypeScript Guidelines

- File Naming: Use kebab-case for all file names.
- Functions: Prefer arrow functions (`const fn = () => {}`) over function declarations.