---
name: external-skills
description: Reference for bundling and conditionally activating external skills from other repositories
---

# External Skills

Bundle skills from other repositories into your plugin with conditional activation based on project context.

## Overview

External skills allow you to:
- **Bundle skills** from other GitHub repositories into your plugin
- **Conditionally activate** them based on project type (React, Python, etc.)
- **Install once**, use everywhere - skills auto-activate when conditions match

## Quick Reference

| Feature | Description |
|---------|-------------|
| Source Format | `owner/repo` (GitHub) |
| Condition Types | `any` (OR), `all` (AND) |
| Rule Types | `files`, `dependencies`, `devDependencies` |
| Skills Selection | `"*"` (all) or `["skill1", "skill2"]` |

## Configuration Schema

### Basic Structure

```json
{
  "externalSkills": [
    {
      "source": "owner/repo",
      "description": "What this skill provides",
      "skills": "*",
      "condition": { ... }
    }
  ]
}
```

### Full Schema

```json
{
  "externalSkills": [
    {
      "source": "string",           // Required: GitHub repo "owner/repo"
      "description": "string",      // Optional: Human-readable description
      "skills": "*" | ["array"],    // Optional: "*" for all, or specific skill names
      "condition": {                // Optional: When to activate (always if omitted)
        "type": "any" | "all",      // "any" = OR logic, "all" = AND logic
        "rules": [
          { "files": ["glob patterns"] },
          { "dependencies": ["package names"] },
          { "devDependencies": ["package names"] }
        ]
      }
    }
  ]
}
```

## Condition Rules

### File-Based Conditions

Activate when specific files exist in the project:

```json
{ "files": ["next.config.*", "next.config.ts", "next.config.js"] }
```

Common patterns:
- Next.js: `["next.config.*"]`
- TypeScript: `["tsconfig.json"]`
- Python: `["requirements.txt", "pyproject.toml"]`
- Rust: `["Cargo.toml"]`
- Go: `["go.mod"]`

### Dependency-Based Conditions

Activate when packages are in `package.json` dependencies:

```json
{ "dependencies": ["react", "next"] }
```

### DevDependency-Based Conditions

Activate when packages are in `package.json` devDependencies:

```json
{ "devDependencies": ["typescript", "@types/react"] }
```

### Combining Rules

**Any (OR) - Default:**
```json
{
  "type": "any",
  "rules": [
    { "files": ["next.config.*"] },
    { "dependencies": ["next"] }
  ]
}
```
Activates if next.config.* exists **OR** next is a dependency.

**All (AND):**
```json
{
  "type": "all",
  "rules": [
    { "files": ["tsconfig.json"] },
    { "dependencies": ["react"] }
  ]
}
```
Activates only if tsconfig.json exists **AND** react is a dependency.

## Common Templates

### React/Next.js Projects

```json
{
  "source": "vercel-labs/agent-skills",
  "description": "Vercel AI SDK skills for React and Next.js",
  "skills": "*",
  "condition": {
    "type": "any",
    "rules": [
      { "files": ["next.config.*", "next.config.ts", "next.config.js", "next.config.mjs"] },
      { "dependencies": ["next", "react"] },
      { "devDependencies": ["next", "react"] }
    ]
  }
}
```

### TypeScript Projects

```json
{
  "source": "example/typescript-skills",
  "description": "TypeScript development skills",
  "skills": "*",
  "condition": {
    "type": "any",
    "rules": [
      { "files": ["tsconfig.json", "tsconfig.*.json"] },
      { "devDependencies": ["typescript"] }
    ]
  }
}
```

### Python Projects

```json
{
  "source": "example/python-skills",
  "description": "Python development skills",
  "skills": "*",
  "condition": {
    "type": "any",
    "rules": [
      { "files": ["requirements.txt", "pyproject.toml", "setup.py", "Pipfile", "poetry.lock"] }
    ]
  }
}
```

### Node.js Projects (Any)

```json
{
  "source": "example/node-skills",
  "description": "Node.js development skills",
  "skills": "*",
  "condition": {
    "type": "any",
    "rules": [
      { "files": ["package.json"] }
    ]
  }
}
```

### Always Active (No Condition)

```json
{
  "source": "example/general-skills",
  "description": "General development skills",
  "skills": "*"
}
```

## Selecting Specific Skills

Instead of importing all skills with `"*"`, you can select specific ones:

```json
{
  "source": "vercel-labs/agent-skills",
  "skills": ["nextjs-app-router", "react-server-components"],
  "condition": { ... }
}
```

## How It Works

```
digraph ExternalSkillsFlow {
    rankdir=TB;
    node [shape=box, style=rounded];

    A[Plugin Loaded] -> B{Has externalSkills?};
    B -- No --> C[Use local skills only];
    B -- Yes --> D[Check each external skill];
    D -> E{Has condition?};
    E -- No --> F[Always activate];
    E -- Yes --> G[Evaluate rules];
    G -> H{type = any?};
    H -- Yes --> I[OR: Any rule matches?];
    H -- No --> J[AND: All rules match?];
    I -- Yes --> F;
    I -- No --> K[Skip this skill];
    J -- Yes --> F;
    J -- No --> K;
    F -> L[Load external skills];
    K --> M[Continue to next];
}
```

## Management Commands

Use the `/external-skill` command to manage external skills:

```bash
# Add a new external skill
/external-skill add vercel-labs/agent-skills

# List configured external skills
/external-skill list

# Remove an external skill
/external-skill remove vercel-labs/agent-skills
```

## Best Practices

1. **Always add descriptions** - Help users understand what each external skill provides

2. **Use appropriate conditions** - Don't load React skills for Python projects

3. **Prefer `"any"` type** - More flexible, activates if any condition matches

4. **Be specific with file patterns** - `next.config.*` is better than just `*.config.*`

5. **Combine file and dependency checks** - Covers both new and existing projects

6. **Test conditions** - Verify skills activate correctly in different project types

## Troubleshooting

**Skills not activating:**
- Check if condition rules match your project
- Verify file patterns are correct
- Ensure dependencies are in the right section (dependencies vs devDependencies)

**Too many skills loading:**
- Add more specific conditions
- Use `"all"` type for stricter matching
- Select specific skills instead of `"*"`

**Source not found:**
- Verify GitHub repo format: `owner/repo`
- Check repo exists and is accessible
- Ensure the repo has a valid skill structure
