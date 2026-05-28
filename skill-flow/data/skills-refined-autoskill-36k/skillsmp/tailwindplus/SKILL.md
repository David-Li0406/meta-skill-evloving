---
name: tailwindplus
description: Access TailwindPlus UI component library - search, list, and retrieve code for Marketing, Application UI, and eCommerce components in HTML/React/Vue with Tailwind CSS v3/v4
---

# TailwindPlus Component Browser

This skill provides access to the TailwindPlus UI component library with 657+ professional components.

## Setup Required

Before using this skill, you need to specify the location of your TailwindPlus JSON data file.
Tell Claude the path to your `tailwindplus-components-*.json` file and Claude will use it in the commands.

Example: "My TailwindPlus data is at ~/data/tailwindplus-components-2026-01-08.json"

## Available Commands

All commands require the JSON data file path as the first argument.

### Get Component Info
```bash
./info.sh <json_file>
```
Returns metadata about the TailwindPlus data file.

### List All Components
```bash
./list_components.sh <json_file>
```
Returns all component names organized by category.

### Search Components
```bash
./search_components.sh <json_file> "hero"
./search_components.sh <json_file> "pricing table"
```
Search for components by keyword (case-insensitive, supports multi-word).

### Get Component Code
```bash
./get_component.sh <json_file> "Application UI.Forms.Input Groups.Simple" -f html -v 4 -m light
./get_component.sh <json_file> "Ecommerce.Components.Product Overviews.With image gallery and expandable details" -f react -v 4 -m none
```

**Required Parameters:**
- `json_file`: Path to the TailwindPlus JSON data file
- `full_name`: The complete dotted path (e.g., "Application UI.Forms.Input Groups.Simple")
- `-f, --framework`: `html`, `react`, or `vue`
- `-v, --version`: `3` or `4` (Tailwind CSS version)
- `-m, --mode`: Theme mode

**Mode Requirements (CRITICAL):**
- Application UI and Marketing components: use `light`, `dark`, or `system`
- eCommerce components: use `none` only

## Component Categories

1. **Application UI** - Forms, navigation, data display, overlays, layout components
2. **Marketing** - Hero sections, features, pricing, testimonials, CTAs, footers
3. **Ecommerce** - Product lists, shopping carts, checkout forms, order history

## Framework Options

- `html` - Pure HTML with Tailwind CSS classes
- `react` - React/JSX components
- `vue` - Vue.js components

## Usage Examples

When user asks for a component:
1. First search to find available components
2. Get the exact component code with proper parameters

Example workflow for finding a button component:
```bash
# Step 1: Search
./search_components.sh <json_file> "button"
# Step 2: Get the component
./get_component.sh <json_file> "Application UI.Elements.Buttons.Primary" -f react -v 4 -m light
```
