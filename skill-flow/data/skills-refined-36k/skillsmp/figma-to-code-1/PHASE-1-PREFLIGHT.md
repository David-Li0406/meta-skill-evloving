# Phase 1: Pre-flight Validation & Authentication

Before building anything, validate credentials, explore the Figma file, and **auto-discover all pages**.

## Step 0: Save Configuration to Project

**CRITICAL: Save the user's pasted configuration before proceeding.**

When the user pastes their configuration prompt:

1. Create the project-config directory:
   ```bash
   mkdir -p project-config
   ```

2. Write the configuration to `/project-config/config.md`:
   ```typescript
   // Save the exact configuration the user pasted
   await writeFile('project-config/config.md', userPastedConfiguration);
   ```

3. Confirm to the user:
   ```
   ✓ Configuration saved to /project-config/config.md

   This file will be your project's reference document.
   It's safe to commit to version control (no secrets).
   ```

**Note:** If `/project-config/config.md` already exists (re-running the skill), read from it instead of asking for configuration again.

## Step 1: Read Configuration & Collect Credentials

1. Read `/project-config/config.md` and extract all configuration values

2. Display configuration summary:
```
Configuration Loaded:
─────────────────────
Project: [Project Name]
Figma File: [Figma Main File URL]

CMS:
  Type: [CMS Type]
  GraphQL URL: [CMS GraphQL URL]
  Organization ID: [CMS Organization ID]
  Admin Email: [CMS Admin Email]
  Admin Password: [provided/missing]
```

3. For any missing credentials, prompt the user:
```
┌─────────────────────────────────────────────────────────────┐
│  CREDENTIALS REQUIRED                                       │
├─────────────────────────────────────────────────────────────┤
│  CMS Admin Login:                                           │
│    URL: [CMS Admin Login URL]                               │
│    Email: [CMS Admin Email]                                 │
│                                                             │
│  Please provide the CMS admin password:                     │
│  > _                                                        │
│                                                             │
│  (This will NOT be written to any files)                    │
└─────────────────────────────────────────────────────────────┘
```

## Step 2: Authenticate with CMS

Test CMS authentication using the login mutation (adapt based on CMS schema):

```typescript
const { data, errors } = await client.mutate({
  mutation: LOGIN,
  variables: { email: cmsAdminEmail, password: cmsAdminPassword },
});

if (errors || !data?.login?.accessToken) {
  throw new Error('CMS authentication failed');
}
```

If login fails, STOP and report the error with troubleshooting steps.

## Step 3: Figma Page Discovery (AUTO)

**CRITICAL: Pages are auto-discovered from Figma, NOT manually entered.**

Use the Figma MCP to automatically inventory all pages in the design file:

### 3.1 Extract File Key and Get Metadata

```typescript
// Extract file key from the main Figma URL
// https://www.figma.com/design/bGCUY43jJhcFUafm33ncgW/Project-Name
const fileKey = figmaMainUrl.match(/\/design\/([^\/]+)/)?.[1];

// Use Figma MCP to get file metadata
const metadata = await mcp__figma__get_metadata({
  fileKey,
  nodeId: "0:1" // Root node to get all pages
});
```

### 3.2 Identify Page Frames

Parse the metadata to identify all website page frames. Look for:
- Frames with dimensions matching standard breakpoints (1440px desktop, 375px mobile)
- Frames named with page identifiers (Homepage, About, Menu, Contact, etc.)
- Desktop/Mobile pairs for each page

**Naming conventions to detect:**
- `1440 - Homepage`, `375 - Homepage` (dimension prefix)
- `Homepage Desktop`, `Homepage Mobile` (device suffix)
- `Homepage`, `Homepage (Mobile)` (parenthetical)

### 3.3 Auto-Detect Global Components

Identify navigation and footer frames:
- Look for frames named: `Navigation`, `Nav`, `Header`, `Menu Overlay`, `Expanded Menu`
- Look for frames named: `Footer`, `Site Footer`
- Match desktop (1440px) and mobile (375px) variants

### 3.4 Generate Page Inventory

Create `/project-config/pages.md` with discovered pages:

```markdown
# Auto-Discovered Pages

> Generated from Figma file: [Main File URL]
> Discovery date: [Current Date]

## Website Pages

| Page Name | Slug | Desktop Frame | Mobile Frame |
|-----------|------|---------------|--------------|
| Homepage | / | [node-id=195:1342](url) | [node-id=418:3286](url) |
| Menu | /menu | [node-id=297:1732](url) | [node-id=428:4784](url) |
| About | /about | [node-id=112:6096](url) | [node-id=418:3764](url) |
...

## Global Components

| Component | Desktop Frame | Mobile Frame |
|-----------|---------------|--------------|
| Navigation | [node-id=X:Y](url) | [node-id=X:Y](url) |
| Footer | [node-id=X:Y](url) | [node-id=X:Y](url) |
| Expanded Menu | [node-id=X:Y](url) | [node-id=X:Y](url) |

## Summary

- **Total Pages:** X
- **Desktop Frames:** X (1440px)
- **Mobile Frames:** X (375px)
```

### 3.5 User Confirmation

Display discovered pages and ask for confirmation:

```
┌─────────────────────────────────────────────────────────────┐
│  FIGMA PAGE DISCOVERY COMPLETE                              │
├─────────────────────────────────────────────────────────────┤
│  Found 9 pages:                                             │
│    ✓ Homepage (Desktop + Mobile)                            │
│    ✓ Menu (Desktop + Mobile)                                │
│    ✓ Programming (Desktop + Mobile)                         │
│    ✓ Private Events (Desktop + Mobile)                      │
│    ✓ About (Desktop + Mobile)                               │
│    ✓ Contact (Desktop + Mobile)                             │
│    ✓ FAQ (Desktop + Mobile)                                 │
│    ✓ 404 (Desktop + Mobile)                                 │
│                                                             │
│  Global Components:                                         │
│    ✓ Navigation (Desktop + Mobile)                          │
│    ✓ Footer (Desktop + Mobile)                              │
│    ✓ Expanded Menu (Desktop + Mobile)                       │
│                                                             │
│  Saved to: /project-config/pages.md                         │
│                                                             │
│  Review and confirm these pages are correct.                │
│  You can edit pages.md to exclude pages or adjust slugs.    │
└───────────────────────────���─────────────────────────────────┘
```

**If pages are missing or incorrectly identified:**
- User can manually edit `/project-config/pages.md`
- Or provide hints in config.md under `## Page Hints` section

## Step 4: Component Library Discovery

**CRITICAL: Pre-fetch component metadata to avoid duplicate work during build.**

Figma design files typically have a dedicated Components or Design System page containing reusable UI components. Extract this inventory upfront so Phase 7 can reference existing components instead of rebuilding them.

### 4.1 Locate Components Page

From the root metadata (Step 3.1), identify the Components/Design System page:
- Look for pages named: `Components`, `Design System`, `UI Kit`, `Component Library`
- Get the page's node ID

```typescript
// Find the Components page from root metadata
const componentsPage = pages.find(page =>
  /^(components|design system|ui kit|component library)$/i.test(page.name)
);

if (!componentsPage) {
  console.warn('No Components page found - skipping component discovery');
}
```

### 4.2 Extract Component Metadata

Use Figma MCP to get all components on the page:

```typescript
// Get metadata for the Components page
const componentMetadata = await mcp__figma__get_metadata({
  fileKey,
  nodeId: componentsPage.nodeId
});
```

### 4.3 Parse Component Structure

Identify all component frames and their variants:
- Top-level frames are typically component categories (Buttons, Cards, Forms, etc.)
- Child frames are individual components
- Look for variant indicators: `Default`, `Hover`, `Active`, `Disabled`, `Small`, `Large`

### 4.4 Generate Component Inventory

Create `/project-config/components.md`:

```markdown
# Component Library Inventory

> Generated from Figma file: [Main File URL]
> Components page node ID: [Node ID]
> Discovery date: [Current Date]

## Component Categories

### Buttons
| Component | Node ID | Variants | Used On Pages |
|-----------|---------|----------|---------------|
| Primary Button | 123:456 | Default, Hover, Disabled | Homepage, Contact |
| Secondary Button | 123:457 | Default, Hover | Menu, About |
| Icon Button | 123:458 | Default, Hover | All pages |

### Cards
| Component | Node ID | Variants | Used On Pages |
|-----------|---------|----------|---------------|
| Event Card | 234:567 | Default, Featured | Homepage, Programming |
| Menu Item Card | 234:568 | Default | Menu |

### Forms
| Component | Node ID | Variants | Used On Pages |
|-----------|---------|----------|---------------|
| Text Input | 345:678 | Default, Focus, Error | Contact |
| Select | 345:679 | Default, Open | Contact |

### Navigation
| Component | Node ID | Variants | Used On Pages |
|-----------|---------|----------|---------------|
| Nav Link | 456:789 | Default, Active | Global |
| Mobile Menu Item | 456:790 | Default | Global |

## Summary

- **Total Components:** X
- **Categories:** X
- **With Variants:** X

## Usage Notes

Reference this file during Phase 7 (Component Building) to:
1. Check if a component already exists before building
2. Get the correct node ID for `get_design_context`
3. Understand component variants to implement
```

### 4.5 User Confirmation

```
┌─────────────────────────────────────────────────────────────┐
│  COMPONENT LIBRARY DISCOVERY COMPLETE                       │
├─────────────────────────────────────────────────────────────┤
│  Found 24 components in 6 categories:                       │
│    • Buttons (4 components)                                 │
│    • Cards (5 components)                                   │
│    • Forms (6 components)                                   │
│    • Navigation (3 components)                              │
│    • Typography (4 components)                              │
│    • Icons (2 components)                                   │
│                                                             │
│  Saved to: /project-config/components.md                    │
│                                                             │
│  This inventory will be used in Phase 7 to avoid            │
│  rebuilding existing components.                            │
└─────────────────────────────────────────────────────────────┘
```

**If no Components page exists:**
- Log a warning but continue
- Components will be discovered ad-hoc during page building

## Step 5: Figma Reference Frames

1. Identify reference frames (Style Guide, Components, Design System)
2. Document in `/docs/figma-reference-frames.md`
3. These are NOT pages to build, but resources for token extraction

## Step 6: Font Check

1. Extract all font families from Figma
2. Create `/docs/font-manifest.json`:
```json
{
  "fonts": [
    {"family": "Inter", "source": "google", "status": "available"},
    {"family": "Custom Font", "source": "custom", "status": "missing", "suggestedFallback": "Source Sans Pro"}
  ],
  "missingFonts": ["Custom Font"],
  "fontHandling": "STRICT",
  "canProceed": false
}
```

3. If STRICT mode and fonts missing, STOP and prompt user for resolution

## Checkpoint

```bash
osascript -e 'display notification "Phase 1: Pre-flight complete" with title "Claude Code" sound name "Ping"'
```

**Outputs:**
- `/project-config/config.md` - Project configuration
- `/project-config/pages.md` - Auto-discovered page inventory
- `/project-config/components.md` - Component library inventory
- `/docs/figma-reference-frames.md` - Reference frame documentation
- `/docs/font-manifest.json` - Font availability check

**Next:** Proceed to [PHASE-2-INIT.md](PHASE-2-INIT.md)
