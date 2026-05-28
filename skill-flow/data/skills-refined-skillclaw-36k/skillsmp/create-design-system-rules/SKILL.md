---
name: create-design-system-rules
description: Generates custom design system rules for your codebase
---

# Create Design System Rules

You are helping generate custom design system rules tailored to the project's specific needs for Figma-to-code workflows.

## Prerequisites

- Figma MCP server must be connected (available at http://127.0.0.1:3845/mcp)
- Access to project codebase for analysis
- Understanding of team's component conventions

## Required Workflow

### Step 1: Run Create Design System Rules Tool

Call the Figma MCP server's `create_design_system_rules` tool with:

- `clientLanguages`: Comma-separated languages (e.g., "typescript,javascript", "python")
- `clientFrameworks`: Framework (e.g., "react", "vue", "svelte", "angular")

### Step 2: Analyze the Codebase

Analyze the project to understand existing patterns:

- **Component Organization**: Where are UI components located?
- **Styling Approach**: What CSS framework? (Tailwind, CSS Modules, styled-components, etc.)
- **Design Tokens**: Where are they defined? (CSS variables, theme files)
- **Component Patterns**: Naming conventions, prop structures, composition patterns
- **Architecture**: State management, routing, import patterns

### Step 3: Generate Project-Specific Rules

Create comprehensive rules including:

#### General Component Rules

- Component locations and organization
- Naming conventions
- Export patterns

#### Styling Rules

- CSS framework/approach used
- Design token locations
- Spacing and typography systems
- **IMPORTANT**: Never hardcode values

#### Figma MCP Integration Rules

```markdown
## Figma MCP Integration Rules

### Required Flow (do not skip)

1. Run get_design_context first to fetch structured representation
2. If response is too large, run get_metadata then re-fetch specific nodes
3. Run get_screenshot for visual reference
4. Download any assets needed from Figma MCP server
5. Translate output to project's conventions, styles, and framework
6. Validate against Figma for 1:1 look and behavior

### Implementation Rules

- Treat Figma MCP output as representation of design, not final code style
- Replace with project's styling approach when applicable
- Reuse existing components instead of duplicating
- Use project's color system, typography, spacing tokens consistently
- Strive for 1:1 visual parity with Figma design
```

#### Asset Handling Rules

```markdown
- Use localhost sources from Figma MCP server directly
- DO NOT import new icon packages - all assets from Figma payload
- DO NOT use placeholders if localhost source provided
- Store assets in appropriate directory
```

### Step 4: Save Rules to CLAUDE.md/AGENTS.md

Guide user to save rules to `CLAUDE.md/AGENTS.md` in project root under "MCP Servers" section.

### Step 5: Validate and Iterate

Test with simple Figma component implementation and refine rules as needed.

## Rule Categories

### Essential Rules (Always Include)

- Component discovery locations
- Design token usage
- Styling approach

### Recommended Rules

- Component patterns
- Import conventions
- Code quality standards

### Optional Rules

- Accessibility standards
- Performance considerations
- Testing requirements

## Best Practices

- **Start simple, iterate** - Don't capture every rule upfront
- **Be specific** - Tell Claude exactly what to do, not just what to avoid
- **Make rules actionable** - Each rule should provide clear guidance
- **Use IMPORTANT** for critical rules that must never be violated
- **Document the why** - Explain reasoning when rules seem arbitrary
