---
name: create-detector
description: This skill should be used when creating a new MUI component detector for the parser. It guides through analyzing HTML, identifying the MUI component type, and creating the detector following the established pattern.
---

# Create Detector

This skill creates new MUI component detectors for the HTML parser.

## When to Use

Use this skill when:
- Adding support for a new MUI component type
- The user provides HTML samples of a component to detect

## Prerequisites

Gather from the user:
1. **HTML sample** - Real HTML of the MUI component (ideally both states if applicable)
2. **Description** - What the component does / represents in the form

## Process

### Step 1: Identify MUI Component

Analyze the HTML to identify which MUI component it is:
- Look for MUI class patterns: `Mui{Component}-{part}` (e.g., `MuiSwitch-root`, `MuiAutocomplete-root`)
- Common components: Switch, TextField, Autocomplete, Select, Checkbox, RadioGroup, DatePicker
- Determine the field kind from the MUI component name (e.g., MuiSwitch → "toggle", MuiAutocomplete → "autocomplete")

### Step 2: Analyze Structure

Examine the HTML to identify:
- **Root element**: Tag, identifying classes, data-testid
- **Nested structure**: Required child elements that define the component
- **Unique identifier**: What makes each instance unique (typically `input[name]`)
- **State indicator**: How to determine the current value (class presence, attribute, etc.)
- **Portaled elements**: Some MUI components render parts at document root (menus, modals, dialogs). Look for ID patterns linking component to portal (e.g., `#menu-{fieldName}`, `#dialog-{id}`)

### Step 3: Design Meta Fields

Determine what selectors are needed for page object interaction:
- What element(s) need to be located for reading state?
- What element(s) need to be located for writing/changing state?
- Meta fields can be **relative** (to `path`) or **absolute** (for portaled elements)
- For portaled content, use role-based selectors (e.g., `[role="listbox"] [role="option"]`)

**IMPORTANT - Meta Field Rules:**
1. **Meta fields are LOCATORS, not values** - Never extract actual text/values, always provide selectors
2. **NEVER use element IDs in locators** - MUI generates dynamic IDs like `:r4v:` that change between renders
3. **Prefer role-based selectors** - Use `[role="option"]`, `[role="listbox"]`, etc. for accessibility elements
4. **Prefer data-testid selectors** - Use `[data-testid="..."]` when available
5. **Prefer class-based selectors** - Use `.MuiComponent-part` patterns as fallback

### Step 4: Create Detector Folder

Create `src/detectors/{kind}/` with files:
```
src/detectors/{kind}/
├── types.ts      # {Kind}Meta, {Kind}Node interfaces
├── validate.ts   # Validation function
├── detector.ts   # Detector implementation
├── index.ts      # Exports
└── doc.md        # Documentation
```

Use templates from `references/templates.md`.

### Step 5: Implement Validation

In `validate.ts`:
- Check root element tag and attributes
- Validate nested structure exists
- Return false if any check fails
- Return true if all checks pass

### Step 6: Implement Detector

In `detector.ts`:
- Call validate function
- Construct `path` selector that uniquely identifies the component
- Construct `meta` object with sub-element selectors
- Return `DetectionResult` with node and childContainers

### Step 7: Document Meta Fields

In `doc.md`:
- Include example HTML (both states if applicable)
- Show example JSON output
- Document each meta field with description
- Explain value handling - be EXACT about state checking (e.g., which class indicates ON/OFF)

### Step 8: Register Detector

Update `src/detectors/index.ts`:
1. Import the detector: `import { {kind}Detector } from "./{kind}";`
2. Add to detectors array
3. Re-export types: `export type { {Kind}Meta, {Kind}Node } from "./{kind}";`

### Step 9: Create Tests

Create `tests/detectors/{kind}.test.ts`:
- Test valid detection with expected output
- Test rejection of invalid structures

## Output Schema Reference

Every detector produces:
```typescript
{
  type: "field" | "section",
  kind: string,                    // detector name
  path: string,                    // selector to locate root element
  meta: { [key: string]: string }  // selectors (relative to path, or absolute for portals)
}
```

## Templates

See `references/templates.md` for file templates.
