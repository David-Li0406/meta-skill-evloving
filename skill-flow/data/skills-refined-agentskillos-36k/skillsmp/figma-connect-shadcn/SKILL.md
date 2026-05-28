---
name: figma-connect-shadcn
description: Connect shadcn/ui components to their Figma design system counterparts using Code Connect.
---
# Connect shadcn/ui Components to Figma

## When to Use This Skill
- User wants to connect shadcn/ui components to Figma
- User just added new shadcn components via `npx shadcn@latest add <component>`
- Running as part of CI/CD to keep Figma connections in sync
- Periodic audit to find unconnected components

## Incremental Behavior
This skill is **incremental by default**:
- Scans for `.figma.tsx` files next to each component
- Only processes components that are **missing** their Code Connect file
- Skips components that already have connections
- Reports both "already connected" and "newly connected" in final summary

To **force reconnection** of all components, user must explicitly request it.

## Prerequisites

### 1. FIGMA_ACCESS_TOKEN
Ensure `.env` has a valid Figma token:
```bash
FIGMA_ACCESS_TOKEN=figd_...
```

Get one from: https://www.figma.com/developers/api#access-tokens

### 2. Locate shadcn Configuration
Find the `components.json` file to determine:
- **Component output path**: Check `aliases.ui` (typically `@/components/ui`)
- **Style variant**: `style` field (e.g., `"new-york"` or `"default"`)
- **Icon library**: `iconLibrary` field (e.g., `"lucide"`)

## Required Inputs
1. **Figma file URL**: The Figma file containing shadcn component designs
2. **shadcn component folder**: Auto-discovered from `components.json` → typically `src/components/ui/`

## Execution Steps

### Step 1: Extract Figma Components

**Use the `figma-explore` skill's script** to get all components from the Figma file:

```bash
source .env && node .github/skills/figma-explore/figma-extract-all.js "<figmaUrl>" --output .temp/figma-connect-shadcn
```

This creates:
- `.temp/figma-connect-shadcn/figma-components-index.json` - List of all Figma components
- `.temp/figma-connect-shadcn/<component>.json` - Evidence for each component

**If the script fails**, check:
- Token expired? Regenerate at https://www.figma.com/developers/api#access-tokens
- No access? User may need to duplicate a Community file to their account

### Step 2: Discover Project Configuration

Read `components.json` and write notes to `.temp/figma-connect-shadcn/shadcn-discovery.md`:

```markdown
# shadcn/ui Discovery Notes

## Configuration (from components.json)
- Style: {style}
- UI Path: {aliases.ui}
- Icon Library: {iconLibrary}
- Tailwind CSS Variables: {tailwind.cssVariables}

## Installed Components
{list of .tsx files in ui folder, excluding .stories.tsx and .test.tsx}

## Figma Source
- File Key: {fileKey}
- Components Found: {count from figma-components-index.json}
```

### Step 3: Inventory shadcn Components

Scan the UI components folder:

```bash
# Expected location from components.json aliases.ui
packages/client/src/components/ui/
```

**For each `.tsx` file**, check if a corresponding `.figma.tsx` exists:
- `button.tsx` → check for `button.figma.tsx`
- `card.tsx` → check for `card.figma.tsx`

**Filter out non-component files:**
- `*.stories.tsx` (Storybook)
- `*.test.tsx` (tests)
- `*.figma.tsx` (Code Connect files themselves)
- `index.ts` (barrel exports)

Write to `.temp/figma-connect-shadcn/shadcn-components.md`:

```markdown
# shadcn Components Inventory

## Summary
- Total components: 14
- Already connected: 8 ✅
- Need connection: 6 ⏳

## Component Status
| Component | File | Figma Connect | Status |
|-----------|------|---------------|--------|
| Button | button.tsx | button.figma.tsx | ✅ Already connected |
| Card | card.tsx | - | ⏳ Needs connection |
...
```

### Step 4: Match shadcn to Figma Components

Read `.temp/figma-connect-shadcn/figma-components-index.json` and match shadcn component names to Figma components.

**Matching strategy:**
1. Exact name match (case-insensitive): `button.tsx` → `Button`
2. Common aliases: `input.tsx` → `Input` or `Text Field` or `TextField`
3. Compound components: `card.tsx` → `Card` (matches CardHeader, CardContent, etc.)

Write to `.temp/figma-connect-shadcn/shadcn-figma-mapping.md`:

```markdown
# shadcn → Figma Component Mapping

| shadcn Component | Figma Component | Node ID | Evidence File |
|------------------|-----------------|---------|---------------|
| button | Button | 16:1234 | button.json |
| card | Card | 16:2345 | card.json |
| select | Select & Combobox | 16:1730 | select_combobox.json |
| skeleton | - | - | ❌ No match |
```

### Step 5: Generate Connection Tasks

**Only create tasks for components that need connection** (from Step 3's inventory) and have a Figma match (from Step 4's mapping).

Write to `.temp/figma-connect-shadcn/shadcn-connect-tasks.md`:

```markdown
# Code Connect Tasks

## Run Info
- Date: {timestamp}
- Total shadcn components: 14
- Already connected: 8 (skipped)
- No Figma match: 1 (skipped)
- Tasks to run: 5

## Tasks to Execute
Each task will be executed by a subagent with the figma-connect-component skill.

### Task 1: Card
- **Code Path**: packages/client/src/components/ui/card.tsx
- **Figma Node ID**: 16:2345
- **Figma URL**: https://figma.com/design/{fileKey}?node-id=16-2345
- **Evidence File**: .temp/figma-connect-shadcn/card.json
- **Output**: packages/client/src/components/ui/card.figma.tsx
- **Status**: ⏳ Pending

### Task 2: Input
- **Code Path**: packages/client/src/components/ui/input.tsx
- **Figma Node ID**: 16:3456
- **Figma URL**: https://figma.com/design/{fileKey}?node-id=16-3456
- **Evidence File**: .temp/figma-connect-shadcn/input.json
- **Output**: packages/client/src/components/ui/input.figma.tsx
- **Status**: ⏳ Pending

...

## Skipped - Already Connected
| Component | Existing File |
|-----------|---------------|
| Button | button.figma.tsx |
| Calendar | calendar.figma.tsx |
...

## Skipped - No Figma Match
- skeleton.tsx (no corresponding Figma component found in index)
```

### Step 6: Execute Tasks via Subagents

**Only process tasks with "⏳ Pending" status** from the tasks document.

**Before spawning subagents:** Read the full contents of `.github/skills/figma-connect-component/SKILL.md` and store it. Subagents cannot access skill files directly, so you must inline the instructions.

For each pending task, spawn a subagent with:
1. The skill instructions (inlined)
2. The component code path
3. The Figma evidence file content (read from `.figma-components/{name}.json`)
4. The output path for the `.figma.tsx` file

```typescript
// First, read the skill file (do this once before the loop)
const skillInstructions = readFile('.github/skills/figma-connect-component/SKILL.md')

// Then for each pending task:
const evidenceFile = readFile(`.temp/figma-connect-shadcn/${componentName}.json`)

runSubagent({
  description: "Connect Card to Figma",
  prompt: `
    Create a Figma Code Connect file for a React component.
    
    ## Inputs
    - Component Path: packages/client/src/components/ui/card.tsx
    - Figma File Key: ${fileKey}
    - Figma Node ID: 16:2345
    - Output Path: packages/client/src/components/ui/card.figma.tsx
    
    ## Figma Component Evidence
    \`\`\`json
    ${JSON.stringify(evidenceFile, null, 2)}
    \`\`\`
    
    ## Instructions
    Follow these instructions to create the Code Connect file:
    
    ${skillInstructions}
    
    ## Return
    Return the file path of the created .figma.tsx file, or an error message if failed.
  `
})
```

Update each task status in the document as it completes (⏳ → ✅ or ❌).

### Step 7: Verify and Report

After all subagents complete, update `.temp/figma-connect-shadcn/shadcn-connect-tasks.md` with final summary:

```markdown
## Run Summary
- **Run Date**: 2026-01-16 14:30
- **Total shadcn components**: 14
- **Already connected (before run)**: 8
- **Tasks attempted**: 6
- **Successful**: 5
- **Failed**: 1

## Newly Created
| Component | Figma Connect File | Status |
|-----------|-------------------|--------|
| Card | card.figma.tsx | ✅ Created |
| Input | input.figma.tsx | ✅ Created |
| Textarea | textarea.figma.tsx | ✅ Created |
| Select | select.figma.tsx | ✅ Created |
| Label | label.figma.tsx | ✅ Created |

## Failed
| Component | Error |
|-----------|-------|
| Tooltip | No matching Figma component found |

## Previously Connected (Unchanged)
Button, Calendar, DatePicker, ... (8 components)

## Next Steps
Run `npx @figma/code-connect publish` to push connections to Figma.
```

## shadcn-Specific Mapping Rules

### Component Name Mapping
| shadcn Export | Typical Figma Name |
|---------------|-------------------|
| `Button` | `Button` |
| `Card`, `CardHeader`, `CardTitle`, `CardContent` | `Card` (compound) |
| `Input` | `Input` / `Text Field` |
| `Label` | `Label` |
| `Select`, `SelectTrigger`, `SelectContent` | `Select` / `Dropdown` |
| `Sheet`, `SheetTrigger`, `SheetContent` | `Sheet` / `Drawer` / `Side Panel` |
| `AlertDialog` | `Alert Dialog` / `Modal` |
| `DropdownMenu` | `Dropdown Menu` / `Menu` |

### Variant Mapping (shadcn → Figma)
```tsx
// shadcn uses lowercase variants
variant: figma.enum('Variant', {
  'Default': 'default',
  'Destructive': 'destructive',
  'Outline': 'outline',
  'Secondary': 'secondary',
  'Ghost': 'ghost',
  'Link': 'link'
})

size: figma.enum('Size', {
  'Default': 'default',
  'Small': 'sm',
  'Large': 'lg',
  'Icon': 'icon'
})
```

### Compound Component Pattern
shadcn uses compound components. Connect the root and document composition:

```tsx
import figma from '@figma/code-connect'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from './card'

// Connect the main Card component
figma.connect(Card, 'https://figma.com/...', {
  props: {
    children: figma.children('*')
  },
  example: ({ children }) => (
    <Card>
      <CardHeader>
        <CardTitle>Title</CardTitle>
        <CardDescription>Description</CardDescription>
      </CardHeader>
      <CardContent>
        {children}
      </CardContent>
      <CardFooter>
        Footer content
      </CardFooter>
    </Card>
  )
})
```

## Output Files

All work files go in `.temp/figma-connect-shadcn/`:
- `figma-components-index.json` - Index of all Figma components
- `<component>.json` - Detailed evidence per component (e.g., `button.json`)
- `shadcn-discovery.md` - Configuration findings
- `shadcn-components.md` - Component inventory
- `shadcn-figma-mapping.md` - Figma node mappings
- `shadcn-connect-tasks.md` - Task list and status

### Final Code Connect Files
Code Connect files go next to components:
- `packages/client/src/components/ui/button.figma.tsx`
- `packages/client/src/components/ui/card.figma.tsx`
- etc.

## Verification

After all connections are created:

```bash
# Validate connections
npx @figma/code-connect parse

# Publish to Figma
npx @figma/code-connect publish
```