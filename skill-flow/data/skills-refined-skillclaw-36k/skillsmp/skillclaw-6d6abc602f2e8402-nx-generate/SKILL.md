---
name: nx-generate
description: Use this skill when scaffolding code or transforming existing code with Nx generators, such as creating libraries, applications, or components, and automating repetitive tasks.
---

# Skill body

## Run Nx Generator

Nx generators are powerful tools that scaffold code, create projects, add components, make automated code migrations, or automate repetitive tasks in a monorepo. They ensure consistency across the codebase and reduce boilerplate work.

This skill applies when the user wants to:

- Create new libraries, applications, or projects
- Add components, services, modules, or other code artifacts
- Scaffold features or boilerplate code
- Run workspace-specific or custom generators
- Do anything else that an Nx generator exists for

## Generator Discovery Flow

### Step 1: List Available Generators

Use `mcp__nx-mcp__nx_generators` to get a list of all available generators in the workspace. This includes:

- Plugin generators (e.g., `@nx/react:component`, `@nx/js:library`)
- Local workspace generators (defined in the repo's own plugins)

### Step 2: Match Generator to User Request

Based on the user's request, identify which generator(s) could fulfill their needs. Consider:

- What artifact type they want to create (library, component, service, etc.)
- Which framework or technology stack is relevant
- Whether they mentioned specific generator names

**IMPORTANT**: When both a local workspace generator and an external plugin generator could satisfy the request, **always prefer the local workspace generator**. Local generators are customized for the specific repo's patterns and conventions.

It's possible that the user request is something that no Nx generator exists for whatsoever. In this case, you can stop using this skill and try to help the user another way. However, the burden of proof for this is high. Before aborting, carefully consider each and every generator that's available. Look into details for any that could be related in any way before making this decision.

## Pre-Execution Checklist

Before running any generator, complete these steps:

### 1. Fetch Generator Schema

Use `mcp__nx-mcp__nx_generator_schema` to understand all available options. Pay attention to:

- Required options that must be provided
- Optional options that may be relevant to the user's request
- Default values that might need to be overridden

### 2. Read Generator Source Code

Understanding what the generator actually does helps you:

- Know what files will be created/modified
- Understand any side effects (updating configs, installing dependencies, etc.)
- Identify options that might not be obvious from the schema

To find generator source code:

- For plugin generators:
- For local workspace generators:
- (Add any additional instructions as necessary)