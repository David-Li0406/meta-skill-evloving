---
name: figma-to-code
description: Build production Next.js websites from Figma designs with headless CMS integration. Use when building websites from Figma, creating CMS-driven sites, or converting designs to code. Handles Figma extraction, CMS content population, component generation, and deployment.
version: 1.7.0
author: SphereOS
license: MIT
tags: [Figma, Next.js, CMS, Headless CMS, Code Generation, React, TypeScript, GraphQL]
dependencies: [sphereos-cms-api]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, WebFetch, mcp__figma__get_design_context, mcp__figma__get_screenshot, mcp__figma__get_metadata, mcp__figma__get_variable_defs
github-repo: gautam-lulla/claude-skills
skill-path: f2c
---

## FIRST: Check for Updates

**Before proceeding, check if a newer version is available:**

1. Read local version from `~/.claude/skills/f2c/SKILL.md` frontmatter
2. Fetch remote version: `https://raw.githubusercontent.com/gautam-lulla/claude-skills/main/f2c/SKILL.md`
3. Compare the `version:` field in both

**If remote version > local version**, use AskUserQuestion:
- Question: "A newer version of f2c is available. Current: [local] → Latest: [remote]. What would you like to do?"
- Options:
  1. "Update and continue (Recommended)"
  2. "Continue with current version"
  3. "View changelog"

**If user selects "Update and continue":**
- Fetch SKILL.md and CHANGELOG.md from GitHub raw URL
- Save to `~/.claude/skills/f2c/`
- Confirm: "Updated f2c to version [X]. Proceeding..."

**If user selects "View changelog":**
- Fetch and display `https://raw.githubusercontent.com/gautam-lulla/claude-skills/main/f2c/CHANGELOG.md`
- Then ask again

**If versions match**, proceed silently (no prompt).

---

# Figma-to-Code (F2C) Website Builder

You are a senior full-stack engineer building a production-ready Next.js website from Figma designs.
The website will fetch all content from a **Headless CMS** via GraphQL. You will also
**populate the CMS** with content extracted from Figma during the build process.

**PERMISSIONS:** You have full permission to read/write files, create directories, install packages,
and execute any CLI/terminal commands without asking. Proceed autonomously through all phases. Only
pause if you encounter an error you cannot resolve.

---

## When to Use This Skill

**Use Figma-to-Code when:**
- Building a new website from a Figma design file
- Converting design mockups to production Next.js code
- Creating CMS-driven websites with inline editing support
- Extracting design tokens (colors, fonts, spacing) from Figma
- Populating a headless CMS with content from designs
- Generating React components from Figma frames

**Key capabilities:**
- **Design Extraction**: Pull exact values from Figma (colors, fonts, spacing, images)
- **CMS Integration**: Create content types and populate entries automatically
- **Component Generation**: Build typed React components with CMS data attributes
- **Asset Management**: Export images and upload to CDN
- **Full Site Build**: Complete 14-phase workflow from design to deployment

---

## CRITICAL RULES (Read These First)

### ZERO HARDCODED CONTENT RULE

**THIS IS THE MOST IMPORTANT RULE OF THE ENTIRE BUILD.**

Every single piece of text, every URL, every label — EVERYTHING must come from the CMS.
There are NO exceptions. This includes:

- Navigation menu items, footer links, legal/copyright text
- Button labels ("Reserve a Table", "Submit", "Learn More")
- Form placeholders, section labels, contact information
- Logo URLs and alt text, social media handles
- Error messages, loading states, 404 page content
- Metadata (page titles, descriptions)

**If you find yourself typing a string that will be displayed to users, STOP.**
That string must come from CMS content passed via props.

**The ONLY hardcoded strings allowed are:**
- CSS class names, HTML attribute names, JavaScript variable names
- Technical identifiers (IDs, keys), Console.log messages

### INLINE EDITOR DATA ATTRIBUTES

**EVERY editable element MUST include CMS data attributes for inline editing.**

| Attribute | Required | Description |
|-----------|----------|-------------|
| `data-cms-entry` | Yes | Entry slug (e.g., `"homepage"`, `"global-navigation"`) |
| `data-cms-field` | Yes | Dot-notation path (e.g., `"hero.title"`, `"menuLinks[0].label"`) |
| `data-cms-type` | Optional | Override type: `text`, `richtext`, `image`, `array`, etc. |

```tsx
// Example usage
<h1 data-cms-entry="homepage" data-cms-field="hero.title">{hero.title}</h1>
<img data-cms-entry="homepage" data-cms-field="hero.image" data-cms-type="image" src={src} />
```

### CMS DATA STRUCTURE RULE

**CRITICAL: Use FLAT data structures in CMS content entries.**

All content sections must be at the TOP LEVEL of the `data` object. Never nest content inside an extra `data` property.

✅ **Correct (flat):**
```typescript
createContentEntry({ data: {
  hero: { title: "...", imageUrl: "..." },
  about: { heading: "...", body: "..." },
  // Sections are direct children of data
}})
```

❌ **Wrong (nested):**
```typescript
createContentEntry({ data: {
  data: {  // <-- WRONG! Extra nesting breaks inline editing
    hero: { title: "...", imageUrl: "..." },
  }
}})
```

### CMS FIELD DEFINITION RULES

**CRITICAL: Create content types with proper field definitions BEFORE creating content entries.**

1. **Field slugs must be FLAT** (no dot notation):
   ```typescript
   // ✅ CORRECT
   { slug: 'heroTitle', name: 'Hero Title', type: 'text' }
   { slug: 'heroVideoUrl', name: 'Hero Video', type: 'media' }

   // ❌ WRONG
   { slug: 'hero.title', name: 'Hero Title', type: 'text' }
   ```

2. **Use section prefixes** in camelCase: `{sectionName}{FieldName}`
   - `heroTitle`, `heroSubtitle`, `heroVideoUrl`
   - `aboutHeading`, `aboutBody`, `aboutCtaText`

3. **Select appropriate field types**:
   | Type | Use For |
   |------|---------|
   | `text` | Titles, labels, URLs |
   | `richText` | Formatted paragraphs |
   | `media` | Images, videos, files |
   | `json` | Arrays, complex objects |
   | `reference` | Links to other entries |

4. **Arrays**: Use JSON fields for simple arrays, or create separate content types with references for better admin UX

See [CMS-FIELD-DEFINITIONS.md](CMS-FIELD-DEFINITIONS.md) for detailed rules and patterns.

### ANTI-HALLUCINATION RULES

1. **NEVER INVENT CONTENT** — Every text string must be extracted verbatim from Figma
2. **NEVER ASSUME STRUCTURE** — Verify exact layout in Figma before building
3. **NEVER SKIP SECTIONS** — If Figma has 8 sections, build 8 sections
4. **NEVER APPROXIMATE VALUES** — Extract exact colors, spacing, font sizes from Figma
5. **NEVER SUBSTITUTE ASSETS** — Every image must come from Figma export
6. **NEVER USE PARALLEL AGENTS** — Build pages sequentially
7. **EVERY PAGE GETS HOMEPAGE TREATMENT** — Same rigor for page 5 as page 1
8. **NEVER NEST DATA IN DATA** — Content sections go at top level of `data` object

---

## CONTENT ARCHITECTURE

**Content Flow:**
```
Figma Design → Extract Content → Upload Images to CDN → Create CMS Entries → Website Fetches via GraphQL
```

**Technology Stack:**
- Next.js 14+ with App Router, TypeScript, Tailwind CSS
- Apollo Client (server-side only) for GraphQL
- CDN (Cloudflare R2, AWS S3, or similar) for images
- React Server Components with `force-dynamic`
- Next.js Middleware for edit mode cache bypass (see PHASE-2-INIT.md)

### THREE-TIER CONTENT MODEL

**CRITICAL:** Content Types map to Figma components, NOT pages.

```
┌─────────────────────────────────────────────────────────────────┐
│                     TIER 1: GLOBAL (3 CTs)                      │
│  site-settings  │  navigation  │  footer                        │
│  (1 entry each - site-wide configuration)                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                   TIER 2: COMPONENTS (varies)                   │
│  hero-section  │  content-section  │  gallery  │  faq-item      │
│  (N entries each - reusable building blocks from Figma)         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     TIER 3: PAGES (1 CT)                        │
│  page                                                           │
│  (N entries - references component entries above)               │
└─────────────────────────────────────────────────────────────────┘
```

**Why Component-Based?**
| Approach | Problem |
|----------|---------|
| One CT per page | Duplicates fields, can't share content between pages |
| One CT for everything | Too generic, hard to validate |
| **Component-based** | Reusable, validates well, maps to Figma design |

**Key Benefits:**
- Hero sections reusable across pages
- FAQs shared between About, Contact, FAQ pages
- Galleries are independent, referenced by pages
- New pages compose existing components

See [PHASE-5-CONTENT-TYPES.md](PHASE-5-CONTENT-TYPES.md) for complete implementation guide.

### CONTENT LAYER REQUIREMENT

**CRITICAL:** Every website MUST have a content layer (`src/lib/content/index.ts`) that transforms CMS data before passing to components. This layer MUST include `transformImageUrls()` to handle inline editor image saves.

**Why:** The inline editor saves images as objects `{id, url, src, alt, filename}`, but components expect plain URL strings. Without transformation, images display in the editor but NOT on the live site after refresh.

```typescript
// src/lib/content/index.ts - REQUIRED PATTERN
function isImageObject(obj: unknown): obj is { url?: string; src?: string } {
  if (typeof obj !== 'object' || obj === null) return false;
  const o = obj as Record<string, unknown>;
  return (typeof o.url === 'string' || typeof o.src === 'string') &&
    (o.id !== undefined || o.filename !== undefined || o.alt !== undefined);
}

function transformImageUrls<T>(data: T): T {
  if (data === null || data === undefined) return data;
  if (typeof data === 'string') return data;
  if (Array.isArray(data)) return data.map(transformImageUrls) as T;
  if (typeof data === 'object') {
    if (isImageObject(data)) {
      return ((data as any).url || (data as any).src || '') as T;
    }
    const result: Record<string, unknown> = {};
    for (const [key, value] of Object.entries(data as Record<string, unknown>)) {
      result[key] = transformImageUrls(value);
    }
    return result as T;
  }
  return data;
}

export async function getPageContent<T>(slug: string): Promise<T> {
  const { data } = await client.query(...);
  return transformImageUrls(data?.contentEntryBySlug?.data) as T;  // ALWAYS transform!
}
```

See LEARNINGS.md for the complete implementation pattern.

---

## EXECUTION PHASES

Execute these phases in order. After each phase: save checkpoint, commit to git, notify.

| Phase | Name | Reference File |
|-------|------|----------------|
| 1 | Pre-flight Validation & Authentication | [PHASE-1-PREFLIGHT.md](PHASE-1-PREFLIGHT.md) |
| 2 | Project Initialization & CMS Setup | [PHASE-2-INIT.md](PHASE-2-INIT.md) |
| 3 | Design Token Extraction | [PHASE-3-TOKENS.md](PHASE-3-TOKENS.md) |
| 4 | Asset Extraction & CDN Upload | [PHASE-4-ASSETS.md](PHASE-4-ASSETS.md) |
| 5 | CMS Content Type Setup | [PHASE-5-CONTENT-TYPES.md](PHASE-5-CONTENT-TYPES.md) |
| 6 | Global Content Extraction | [PHASE-6-GLOBAL-CONTENT.md](PHASE-6-GLOBAL-CONTENT.md) |
| 7 | Component Generation | [PHASE-7-COMPONENTS.md](PHASE-7-COMPONENTS.md) |
| 8 | Page Content Extraction | [PHASE-8-PAGE-CONTENT.md](PHASE-8-PAGE-CONTENT.md) |
| 9 | Page Assembly | [PHASE-9-PAGES.md](PHASE-9-PAGES.md) |
| 10 | Zero Hardcoded Content Audit | [PHASE-10-AUDIT.md](PHASE-10-AUDIT.md) |
| 11 | Inline Editor Audit | [PHASE-11-EDITOR-AUDIT.md](PHASE-11-EDITOR-AUDIT.md) |
| 12 | Automated QA | [PHASE-12-QA.md](PHASE-12-QA.md) |
| 13 | Production Audit | [PHASE-13-PRODUCTION.md](PHASE-13-PRODUCTION.md) |
| 14 | Deployment | [PHASE-14-DEPLOY.md](PHASE-14-DEPLOY.md) |

**To start:** Read [PHASE-1-PREFLIGHT.md](PHASE-1-PREFLIGHT.md) and begin execution.

---

## PROJECT CONFIGURATION

### Configuration Input & Storage

**CRITICAL: Save the user's configuration to a file for project reference.**

When the user invokes `/figma-to-code` and pastes their configuration:

1. **Create the project-config directory** (if it doesn't exist):
   ```bash
   mkdir -p project-config
   ```

2. **Save the configuration to `/project-config/config.md`**:
   - Write the user's pasted configuration verbatim to this file
   - This becomes the project's reference document for all phases
   - Commit this file to version control

3. **Confirm the save to the user**:
   ```
   ✓ Configuration saved to /project-config/config.md

   This file will be used as reference throughout the build.
   You can edit it to update configuration values.
   ```

**Why save the config?**
- Provides a reference document checked into version control
- Allows re-running phases without re-pasting configuration
- Documents project settings for other developers
- Enables easy updates to configuration values

### Reading Configuration

All phases read configuration from `/project-config/config.md`.

**Expected format (simplified):**

```markdown
# Project Configuration

## Project Info
**Project Name:** My Project Name
**Brand Name:** My Brand
**Project Slug:** my-project-name

## Figma
**Main File URL:** https://www.figma.com/design/xxx/Project-Name

## CMS Configuration
**CMS Type:** SphereOS CMS
**CMS GraphQL URL:** https://backend-production-162b.up.railway.app/graphql
**CMS Organization ID:** org_xxx
**CMS Organization Slug:** my-organization
**CMS Admin Email:** admin@example.com

## Deployment
**Deployment Platform:** Vercel
```

### Auto-Discovery (No Manual Entry Required)

The following are **automatically discovered** from the Figma file during Phase 1:
- **Pages** — All website pages with desktop/mobile frame URLs
- **Global Components** — Navigation, Footer, Menu Overlay frames
- **Page Slugs** — Inferred from frame names (editable in `/project-config/pages.md`)
- **Component Library** — All reusable components from the Components/Design System page

See [PHASE-1-PREFLIGHT.md](PHASE-1-PREFLIGHT.md) for the discovery process.

**Outputs:**
- `/project-config/pages.md` — Page inventory (review and edit if needed)
- `/project-config/components.md` — Component library inventory (used in Phase 7)

### Sensitive Credentials

These are **NOT** stored in config.md:

| Credential | Storage |
|------------|---------|
| CMS Admin Password | Prompted at runtime |
| Figma Access Token | Figma MCP (OAuth) |

### Required `.env.local` File

Create `.env.local` in your project root before starting:

```bash
# CMS Configuration
NEXT_PUBLIC_CMS_GRAPHQL_URL=https://backend-production-162b.up.railway.app/graphql
CMS_ORGANIZATION_ID=org_xxx
```

**Note:** Media uploads go through the CMS API (`uploadMedia` mutation). The CMS handles CDN storage internally — no direct CDN credentials needed.

---

## QUICK REFERENCE

### Data Attribute Patterns

```tsx
// Text
<h1 data-cms-entry={entry} data-cms-field="hero.title">{title}</h1>

// Image
<img data-cms-entry={entry} data-cms-field="hero.image" data-cms-type="image" src={src} />

// Array item
<p data-cms-entry={entry} data-cms-field="team[0].name">{name}</p>

// Rich text
<div data-cms-entry={entry} data-cms-field="intro.body" data-cms-type="richtext" />

// Global content
<span data-cms-entry="global-footer" data-cms-field="copyrightText">{copyright}</span>
```

### Checkpoint Command

```bash
osascript -e 'display notification "Checkpoint: {{PHASE_NAME}} complete" with title "Claude Code" sound name "Ping"'
```

---

## REFERENCE FILES

- [COMPONENT-PATTERNS.md](COMPONENT-PATTERNS.md) - Component code examples
- [CMS-REFERENCE.md](CMS-REFERENCE.md) - Content type and entry slug reference
- [CMS-FIELD-DEFINITIONS.md](CMS-FIELD-DEFINITIONS.md) - Field definition rules and patterns
- [GRAPHQL-EXAMPLES.md](GRAPHQL-EXAMPLES.md) - GraphQL query/mutation examples

### CMS API Reference

For all CMS GraphQL operations (authentication, content types, entries, media uploads), use the `sphereos-cms-api` skill. This skill is listed as a dependency and provides complete query/mutation documentation.

**Key operations from sphereos-cms-api:**
- `login` — Authenticate and get JWT token
- `createContentType` — Create content type schemas
- `createContentEntry` — Create content entries
- `uploadMedia` — Upload images (CMS handles CDN internally)
- `contentEntryBySlug` — Fetch content for rendering

---

## Common Pitfalls to Avoid

❌ **Don't:**
- Hardcode ANY text that displays to users (buttons, labels, titles, etc.)
- Invent content that doesn't exist in the Figma design
- Skip the data-cms attributes on editable elements
- Approximate colors or spacing — extract exact values from Figma
- Use parallel agents for page builds (causes context issues)
- Forget to upload images to CDN before referencing them in CMS
- Create components without TypeScript interfaces for CMS data
- Skip pages because they "look similar" to others
- Create nested `data.data` structures in CMS entries
- Deploy to production with temporary Figma MCP image URLs
- Skip the `transformImageUrls()` function in the content layer — inline editor images won't display
- Assume images from CMS are always strings — inline editor saves them as objects
- Forget to create `middleware.ts` — inline editor saves won't reflect after page refresh

✅ **Do:**
- Extract EVERY piece of text verbatim from Figma
- Add `data-cms-entry`, `data-cms-field` to all editable elements
- Use exact hex values, font sizes, and spacing from Figma
- Build pages sequentially with full attention to each
- Upload images to CDN first, then reference URLs in CMS entries
- Create typed interfaces that match your CMS content structure
- Treat the 5th page with the same rigor as the 1st page
- Commit and checkpoint after each phase
- Keep CMS data structure flat (sections at top level of `data`)
- Run image migration script before production deployment
- **ALWAYS include `transformImageUrls()` in your content layer** — this handles inline editor image saves
- **ALWAYS create `middleware.ts`** — this enables edit mode cache bypass so changes reflect after save
- Test inline editing by saving an image and refreshing the page to verify it persists

---

## Version History

**v1.6.0** (January 2026)
- **MAJOR: Component-based content model** — Content Types now map to Figma components, not pages
- Added Three-Tier Content Model (Global → Components → Pages)
- Completely rewrote PHASE-5-CONTENT-TYPES.md with new architecture
- Added Step 1: Analyze Figma Components before creating content types
- Tier 2 component types: hero-section, content-section, gallery, faq-item, event, team-member, menu-category, award
- Tier 3 page type references component entries for composition
- Content model enables reuse (e.g., FAQs shared across pages)

**v1.7.0** (January 2026)
- **Component Library Discovery** — Phase 1 now auto-discovers all components from the Figma Components page
- New output: `/project-config/components.md` — Component inventory with node IDs and variants
- Phase 7 updated to reference component inventory before building (prevents duplicate work)
- Helps maintain consistency across build phases

**v1.5.0** (January 2026)
- **Configuration persistence** — User's pasted configuration is now saved to `/project-config/config.md`
- Added "Step 0: Save Configuration to Project" in PHASE-1-PREFLIGHT.md
- Configuration file serves as project reference document
- Enables re-running skill phases without re-pasting configuration
- Updated workflow documentation with config file creation flow

**v1.4.0** (January 2026)
- **MAJOR: Auto-discovery of Figma pages** — Pages and global components are now automatically discovered from the Figma file using the Figma MCP
- Simplified config.md format — removed manual page table and global component URLs
- Updated PHASE-1-PREFLIGHT.md with new Step 3: Figma Page Discovery
- Pages inventory saved to `/project-config/pages.md` for review/editing
- Configuration form simplified (removed 6 redundant fields)

**v1.3.0** (January 2026)
- Added CMS FIELD DEFINITION RULES to critical rules section
- Created [CMS-FIELD-DEFINITIONS.md](CMS-FIELD-DEFINITIONS.md) comprehensive guide
- Updated PHASE-5-CONTENT-TYPES.md with flat field naming patterns
- Added field type reference (text, richText, media, json, reference)
- Added array handling patterns (JSON vs separate content types)
- Added frontend transformation layer documentation

**v1.2.0** (January 2026)
- Added edit mode cache bypass via middleware + cookie pattern
- Updated PHASE-2-INIT.md with complete middleware.ts and apollo-client.ts code
- Added middleware requirement to technology stack and pitfalls

**v1.1.0** (January 2026)
- Added CONTENT LAYER REQUIREMENT section with `transformImageUrls()` pattern
- Added inline editor image object handling documentation
- Updated pitfalls to include image transformation requirements
- Cross-referenced LEARNINGS.md for full implementation patterns

**v1.0.0** (January 2025)
- Initial skill release
- 14-phase workflow from design to deployment
- Zero hardcoded content enforcement
- Inline editor data attributes support
- Modular reference files for progressive loading
