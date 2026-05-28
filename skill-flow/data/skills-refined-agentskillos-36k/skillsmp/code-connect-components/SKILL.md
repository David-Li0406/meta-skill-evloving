---
name: code-connect-components
description: Connects Figma design components to code components using Code Connect
---

# Code Connect Components

You are helping to connect Figma design components to their corresponding code implementations using Figma's Code Connect feature.

## Important: Figma URL Requirements

**The Figma URL must include the `node-id` parameter**: `https://figma.com/design/:fileKey/:fileName?node-id=1-2`

**Format conversion needed:**
- URL format uses hyphens: `node-id=1-2`
- MCP tools expect colons: `nodeId=1:2`

## Prerequisites

- Figma MCP server must be connected (available at http://127.0.0.1:3845/mcp)
- The Figma component must be published to a team library
- Access to project codebase for component scanning

## Required Workflow

### Step 1: Extract Metadata from Figma URL

Parse the Figma URL provided:
- Extract file key: segment after `/design/`
- Extract node ID: convert `1-2` from URL to `1:2` for tools
- Example: `https://figma.com/design/kL9xQn2VwM8pYrTb4ZcHjF/DesignSystem?node-id=42-15`
  - fileKey: `kL9xQn2VwM8pYrTb4ZcHjF`
  - nodeId: `42:15` (converted from `42-15`)

**Note:** User must provide Figma URL with node-id parameter.

### Step 2: Get Node Metadata

Run `get_metadata` with the file key and node ID to fetch the node structure and identify all Figma components.

### Step 3: Check Existing Code Connect Mappings

For each Figma component identified (nodes with type `<symbol>`), check if it's already code connected using `get_code_connect_map`.

### Step 4: Get Design Context for Un-Connected Components

For components not yet connected, run `get_design_context` to fetch detailed component structure.

### Step 5: Scan Codebase for Matching Component

Search the codebase for components with similar structure, looking for:
- Matching or similar component names
- Props that correspond to Figma properties (variants, text, styles)
- Files in typical component directories (`src/components/`, `components/`, `ui/`, etc.)

### Step 6: Offer Code Connect Mapping

Present findings to user and offer to create the mapping with:
- File path of the matching component
- Component name
- Language and framework detected

### Step 7: Create the Code Connect Mapping

If user accepts, run `add_code_connect_map` with:
- `nodeId`: The Figma node ID (colon format: `1:2`)
- `source`: Path to code component file (relative to project root)
- `componentName`: Name of the component
- `clientLanguages`: Comma-separated languages (e.g., "typescript,javascript")
- `clientFrameworks`: Framework (e.g., "react", "vue", "svelte")
- `label`: Framework label (e.g., "React", "Vue", "SwiftUI")

### Step 8: Repeat for All Components

Process all un-connected components identified in Step 2 and provide a summary.

## MCP Tools Available

You have access to Figma MCP tools through the `figma` MCP server:
- `get_metadata` - Get node structure and hierarchy
- `get_code_connect_map` - Check existing mappings
- `get_design_context` - Get detailed component structure
- `add_code_connect_map` - Create code connection mapping
- `get_screenshot` - Get visual reference

## Best Practices

- Proactively search codebase for matching components
- Look beyond names - check prop alignment and structure
- Present multiple candidates if multiple matches found
- Gracefully handle cases where no match exists
