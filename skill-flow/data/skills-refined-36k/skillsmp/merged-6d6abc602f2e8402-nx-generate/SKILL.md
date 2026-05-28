---
name: nx-generate
description: Use this skill when scaffolding code or transforming existing code with Nx generators, such as creating libraries, applications, or components, and automating repetitive tasks.
---

# Run Nx Generator

Nx generators are powerful tools that scaffold code, create projects, add components, make automated code migrations, or automate repetitive tasks in a monorepo. They ensure consistency across the codebase and reduce boilerplate work.

This skill applies when the user wants to:

- Create new libraries, applications, or projects
- Add components, services, modules, or other code artifacts
- Scaffold features or boilerplate code
- Run workspace-specific or custom generators
- Do anything else that an Nx generator exists for

## Generator Discovery Flow

### Step 1: List Available Generators

Use `mcp__nx-mcp__nx_generators` to get a list of all available generators in the workspace, including:

- Plugin generators (e.g., `@nx/react:component`, `@nx/js:library`)
- Local workspace generators (defined in the repo's own plugins)

### Step 2: Match Generator to User Request

Identify which generator(s) could fulfill the user's needs based on:

- The artifact type they want to create (library, component, service, etc.)
- The relevant framework or technology stack
- Any specific generator names mentioned

**IMPORTANT**: Always prefer local workspace generators over external plugin generators when both could work, as they are customized for the specific repo's patterns and conventions.

## Pre-Execution Checklist

Before running any generator, complete these steps:

### 1. Fetch Generator Schema

Use `mcp__nx-mcp__nx_generator_schema` to understand all available options, including:

- Required options that must be provided
- Optional options that may be relevant to the user's request
- Default values that might need to be overridden

### 2. Read Generator Source Code

Understanding what the generator does helps you:

- Know what files will be created/modified
- Understand any side effects (updating configs, installing dependencies, etc.)
- Identify options that might not be obvious from the schema

To find generator source code:

- For plugin generators: Use `node -e "console.log(require.resolve('@nx/<plugin>/generators.json'));"` to find the generators.json, then locate the source from there.
- For local generators: They are typically in `tools/generators/` or a local plugin directory. Search the repo for the generator name to find it.

### 3. Understand Repo Context

Examine the target area of the codebase:

- Look at similar existing artifacts (other components, libraries, etc.)
- Identify patterns and conventions used in the repo
- Note naming conventions, file structures, and configuration patterns

### 4. Validate Required Options

Ensure all required options have values:

- Map the user's request to generator options
- Infer values from context where possible
- Ask the user for any critical missing information

## Execution

You might need to prefix commands with npx/pnpx/yarn if Nx isn't installed globally. Many generators behave differently based on where they are executed.

### Consider Dry-Run (Optional)

Running with `--dry-run` first is encouraged but not mandatory. Use your judgment based on the complexity of the generator.

### Running the Generator

Execute the generator with:

```bash
nx generate <generator-name> <options> --no-interactive
```

**CRITICAL**: Always include `--no-interactive` to prevent prompts that would hang the execution.

### Handling Generator Failures

If the generator fails:

1. **Diagnose the error** - Read the error message carefully.
2. **Identify the cause** - Missing options, invalid values, conflicts, etc.
3. **Attempt automatic fix** - Adjust options or resolve conflicts.
4. **Retry** - Run the generator again with corrected options.

## Post-Generation

### 1. Modify Generated Code (If Needed)

Generators provide a starting point, but the output may need adjustment to match the user's specific requirements:

- Add or modify functionality as requested
- Adjust imports, exports, or configurations
- Integrate with existing code patterns in the repo

### 2. Format Code

Run formatting on all generated/modified files:

```bash
nx format --fix
```

### 3. Run Verification

Verify that the generated code works correctly. This may involve running linting, testing, or building the new project.

### 4. Handle Verification Failures

When verification fails, address manageable issues directly or escalate extensive problems to the user with a description of what was generated and the issues encountered.

## Error Handling

### Generator Failures

- Check the error message for specific causes.
- Verify all required options are provided.
- Check for conflicts with existing files.

### Missing Options

- Consult the generator schema for required fields.
- Infer values from context when reasonable.
- Ask the user for values that cannot be inferred.

## Key Principles

1. **Local generators first** - Always prefer workspace/local generators over external plugin generators.
2. **Understand before running** - Read both the schema and the source code to fully understand what will happen.
3. **No prompts** - Always use `--no-interactive` to prevent hanging.
4. **Generators are starting points** - Modify the output as needed to fully satisfy the user's requirements.
5. **Verify changes work** - Ensure the code builds, lints, and tests pass.
6. **Be proactive about fixes** - Attempt to resolve errors automatically when possible.
7. **Match repo patterns** - Study existing similar code in the repo and match its conventions.