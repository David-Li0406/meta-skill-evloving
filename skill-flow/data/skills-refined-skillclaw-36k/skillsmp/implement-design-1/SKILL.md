---
name: implement-design
description: Translates Figma designs into production-ready code with 1:1 visual fidelity
---

# Implement Design

You are translating a Figma design into production-ready code with pixel-perfect accuracy.

## Important: Figma URL Requirements

**The Figma URL must include the `node-id` parameter**: `https://figma.com/design/:fileKey/:fileName?node-id=1-2`

**Format conversion needed:**
- URL format uses hyphens: `node-id=1-2`
- MCP tools expect colons: `nodeId=1:2`

## Prerequisites

- Figma MCP server must be connected (available at http://127.0.0.1:3845/mcp)
- Project should have established design system or component library

## Required Workflow

### Step 1: Extract Node ID from Figma URL

Parse the Figma URL:
- Extract file key: segment after `/design/`
- Extract node ID: convert `1-2` to `1:2` for tools
- Example: `https://figma.com/design/kL9xQn2VwM8pYrTb4ZcHjF/DesignSystem?node-id=42-15`
  - fileKey: `kL9xQn2VwM8pyrTb4ZcHjF`
  - nodeId: `42:15`

**Note:** User must provide Figma URL with node-id parameter.

### Step 2: Fetch Design Context

Run `get_design_context` with fileKey and nodeId to get:
- Layout properties (Auto Layout, constraints, sizing)
- Typography specifications
- Color values and design tokens
- Component structure and variants
- Spacing and padding values

**If response is too large or truncated:**
1. Run `get_metadata(fileKey=":fileKey", nodeId="1:2")` for high-level map
2. Identify specific child nodes needed
3. Fetch individual nodes with `get_design_context(fileKey=":fileKey", nodeId=":childNodeId")`

### Step 3: Capture Visual Reference

Run `get_screenshot` with same fileKey and nodeId for visual reference. This serves as source of truth for validation.

### Step 4: Download Required Assets

Download assets from Figma MCP server's assets endpoint:
- **IMPORTANT**: If server returns `localhost` source, use it directly
- **DO NOT** import new icon packages - use Figma assets
- **DO NOT** use placeholders if localhost source provided

### Step 5: Translate to Project Conventions

Translate Figma output to project's framework, styles, and conventions:
- Treat Figma output (React + Tailwind) as design representation, not final code
- Replace with project's preferred utilities or design system tokens
- Reuse existing components instead of duplicating
- Use project's color system, typography, spacing tokens
- Respect existing routing, state management, data-fetch patterns

### Step 6: Achieve 1:1 Visual Parity

Strive for pixel-perfect visual fidelity:
- Prioritize Figma fidelity to match designs exactly
- Avoid hardcoded values - use design tokens
- Prefer design system tokens when conflicts arise, adjust spacing minimally to match visuals
- Follow WCAG accessibility requirements

### Step 7: Validate Against Figma

Before marking complete, validate against screenshot:
- [ ] Layout matches (spacing, alignment, sizing)
- [ ] Typography matches (font, size, weight, line height)
- [ ] Colors match exactly
- [ ] Interactive states work as designed
- [ ] Responsive behavior follows Figma constraints
- [ ] Assets render correctly
- [ ] Accessibility standards met

## Implementation Rules

### Component Organization
- Place components in designated design system directory
- Follow project's naming conventions
- Avoid inline styles unless necessary for dynamic values

### Design System Integration
- **ALWAYS** use project's design system components when possible
- Map Figma tokens to project design tokens
- Extend existing components rather than creating new ones
- Document new components added to design system

### Code Quality
- Avoid hardcoded values - extract to constants or tokens
- Keep components composable and reusable
- Add TypeScript types for component props
- Include JSDoc comments for exports

## MCP Tools Available

You have access to Figma MCP tools through the `figma` MCP server:
- `get_metadata` - Get node structure and hierarchy
- `get_design_context` - Get detailed component structure
- `get_screenshot` - Get visual reference
- Assets endpoint - Download images, icons, SVGs

## Best Practices

- **Always start with context** - Never implement based on assumptions
- **Incremental validation** - Validate frequently during implementation
- **Document deviations** - Comment on why you deviated from design
- **Reuse over recreation** - Check for existing components first
- **Design system first** - Prefer project patterns over literal translation
