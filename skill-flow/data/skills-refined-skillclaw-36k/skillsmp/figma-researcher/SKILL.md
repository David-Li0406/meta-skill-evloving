---
name: figma-researcher
description: "WHAT: Research Figma designs using MCP server for implementation details. WHEN: implementing UX changes, extracting design specs, auditing design tokens. KEYWORDS: figma, mcp, design, research, specs, tokens, colors, spacing, implementation."
---

# Figma Researcher

Research Figma designs to gather implementation context for developers.

## When to Use This Skill

Use this skill when you need to:
- Implement UX changes from Figma designs
- Extract design specifications (colors, spacing, typography, layout)
- Audit Figma files for design token compliance
- Verify implementations match designs
- Document design system patterns

## How It Works

### Step 1: Verify Figma MCP is Configured

Before doing anything else, check if the Figma MCP server is available:

```
Tool: ListMcpResourcesTool
Parameters:
  server: "figma"
```

**If MCP is not available**, stop and instruct the user:

```
⚠️ Figma MCP is not configured.

To use Figma features:
1. Run: claude mcp add --transport http figma https://mcp.figma.com/mcp
2. Run: /mcp in Claude Code and authenticate with Figma
3. Restart this conversation

Installation guide: https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/#claude-code
```

### Step 2: Get Figma MCP Documentation

Once MCP is available, get context on available Figma tools:

```
Tool: ListMcpResourcesTool
Parameters:
  server: "figma"
```

This returns available resources and documentation from the Figma MCP server. Read these resources to understand:
- Available tools (get_design_context, get_screenshot, get_metadata, get_variable_defs)
- Tool parameters and usage
- How to work with Figma file URLs and node IDs

### Step 3: Research Like a Developer Would

With the Figma MCP tools available, conduct research to gather implementation details:

**Always start with:**
1. **Extract file key and node ID** from the Figma URL provided by user
2. **Get metadata** first to understand structure and discover child node IDs
3. **Use node IDs from metadata AS-IS** - do NOT convert format:
   - ✅ Correct: Use `0:31829` directly from metadata
   - ❌ Wrong: Converting to `0-31829` or other formats
   - Node IDs in metadata are in the correct format for all MCP tools
4. **Get design context** for 2-3 key components/frames (not all):
   - Generated code snippets
   - Layout properties (spacing, padding, alignment)
   - Visual properties (colors, borders, shadows)
   - Typography (fonts, sizes, weights)
   - Component structure
5. **Get screenshots** for 1-2 key screens only (see Screenshot Guidelines below)
6. **Get variable definitions** to map design tokens (if needed)

**Screenshot Guidelines (IMPORTANT):**

**⚠️ Screenshots are NOT saved to disk:**
- Figma MCP `get_screenshot` shows images in your context window only
- Images are NOT automatically saved to the visuals folder
- If user needs saved screenshots, recommend:
  1. Manual export from Figma (no API key needed)
  2. Use `figma-dev-mode-figma-image-downloader` skill (requires FIGMA_API_KEY)

Figma MCP has a **8000 pixel limit** for screenshots. To avoid errors:

1. **Target specific nodes, not full pages:**
   - ✅ Screenshot individual components/frames (e.g., `node-id=123-456`)
   - ❌ Screenshot entire pages or canvases (will often exceed 8000px)

2. **Check metadata dimensions before screenshots:**
   - Use `get_metadata` to see frame dimensions (width × height)
   - If total pixels > 8000×8000 (64M pixels), target smaller nodes

3. **Handle screenshot errors gracefully:**
   - If you get "image bigger than 8000 pixels" error:
     - Look at metadata to find child frames/components
     - Take multiple screenshots of smaller sections
     - Document which sections couldn't be captured
   - Inform user: "The design is too large for a single screenshot. I'll capture individual components instead."

4. **Prioritize design context over screenshots:**
   - `get_design_context` has no size limit and provides implementation details
   - Use screenshots for visual verification, not as primary source

**Document findings clearly:**
- Colors with hex values and suggested token mappings
- Spacing with pixel values and suggested token mappings
- Typography specifications
- Layout structure and properties
- Asset URLs if images are present
- Any discrepancies or recommendations

## Best Practices

**Check MCP first, always:**
- Never attempt to use Figma tools without verifying MCP is configured
- If not configured, stop and provide clear installation instructions

**Be context-efficient (CRITICAL):**
- Get metadata first, but DON'T expand large responses
- **Select 2-3 KEY components only** - don't analyze every frame in metadata
- Use node IDs from metadata exactly as shown (e.g., `0:31829`)
- Take 1-2 targeted screenshots max (specific components, not full pages)
- Summarize design context, don't dump all properties
- Focus on actionable specs: colors, spacing, typography, layout structure
- Stop after gathering enough context - don't be exhaustive

**Let the MCP guide you:**
- Use ListMcpResourcesTool to get Figma documentation
- Read the documentation to understand available tools
- Follow the tool usage patterns described in MCP resources

**Think like a researcher:**
- Start broad (metadata), then narrow down (specific nodes)
- Get targeted data points (2-3 key components)
- Document concisely for the implementer
- Note any ambiguities briefly

**Be practical:**
- Extract file key from URL (the part after `/design/`)
- Use node IDs from metadata as-is (already in correct format)
- Take screenshots at appropriate levels (component, not entire page)
- Map colors/spacing to design system tokens when possible
- Provide actionable recommendations, not exhaustive dumps

**Example workflow:**
```
1. Get metadata for file
2. Find 2-3 key frames in metadata (e.g., main screen, component detail)
3. Call get_design_context on those specific node IDs (use as-is from metadata)
4. Take 1 screenshot of the main screen
5. Summarize findings concisely
6. STOP - don't analyze every single component
```

## Common Workflows

### Implementing a UX Change
1. Verify Figma MCP is configured
2. Get MCP documentation to understand available tools
3. Extract file key and node ID from URL
4. Get metadata to understand page structure
5. Get design context for target component
6. Get screenshot for visual reference
7. Get variables to map design tokens
8. Document specifications for implementer

### Auditing Design Token Usage
1. Verify Figma MCP is configured
2. Get variable definitions for the file
3. Get design context for components
4. Compare Figma variables with codebase design tokens
5. Identify hardcoded values vs token usage
6. Generate compliance report with recommendations

### Verifying Implementation
1. Verify Figma MCP is configured
2. Get design context for reference design
3. Get screenshot for visual comparison
4. Compare implementation code with Figma specs
5. Document any discrepancies
6. Recommend fixes with specific token references
