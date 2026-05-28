---
repos:
  - yourcompany/web
  - yourcompany/zest-react-native
  - yourcompany/shared-mobile-modules
---

# Update Zest Components Skill

## Purpose

Update the Zest Components skill at `templates/skills/ui-design-system/zest-components/SKILL.md` with the latest component APIs and usage patterns from source repositories.

## Instructions

This workflow analyzes source repositories to detect changes in Zest component APIs and updates the skill documentation accordingly. Source repositories have been pre-cloned to the parent directory:
- `../web/app/libs/zest` (web implementation)
- `../zest-react-native/src` (React Native implementation)
- `../shared-mobile-modules` (production examples)

**IMPORTANT**: Analyze component APIs from the **source repositories**, not from node_modules or documentation.

Execute workflow phases sequentially, ONE AT A TIME.

## Workflow

### PHASE 1: Read Current Skill

Read `templates/skills/ui-design-system/zest-components/SKILL.md`:
- Extract frontmatter (MUST preserve exactly)
- Identify currently documented components
- Note existing examples and patterns

### PHASE 2: Analyze Source Repositories

**Key Files to Read:**

**Web Implementation:**
- `../web/app/libs/zest/src/index.tsx` - Main exports
- `../web/app/libs/zest/src/components/` - Component implementations

**React Native Implementation:**
- `../zest-react-native/src/index.tsx` - Main exports
- `../zest-react-native/src/components/` - Component implementations

**Production Examples:**
- `../shared-mobile-modules/src/modules/**/components/**/*.tsx` - Real usage patterns

**Analysis Steps:**

For Web (`../web/app/libs/zest`):
- Read `src/index.tsx` to see all exported components
- For each component, read its TypeScript definition to get exact props/types
- Note component variants (size, variant, color props, etc.)

For React Native (`../zest-react-native`):
- Read `src/index.tsx` to see all exported components
- For each component, read its TypeScript definition
- Compare with web version for platform differences

For Production Examples (`../shared-mobile-modules`):
- Find real-world usage of Zest components
- Note common patterns and best practices
- Identify testID usage patterns

### PHASE 3: Identify Changes

Compare source repositories against current documentation:

**Check for New Components:**
- Components in source exports but not documented
- List component name, purpose, key props

**Verify Signature Changes (CRITICAL):**
- For EVERY documented component, verify its current signature
- Check for:
  - New props added
  - Props removed or deprecated
  - Prop type changes (e.g., `string` → `string | number`)
  - Optional props becoming required (`prop?` vs `prop`)
  - New variants or size options
  - Breaking changes
- **DO NOT SKIP** - verify even if component seems unchanged

**Identify Updated Patterns:**
- New usage patterns from production code
- Better examples from shared-mobile-modules
- Updated best practices

**Check for Deprecated/Removed:**
- Components in docs but not in source exports
- Mark as deprecated if removed from API

### PHASE 4: Generate Detailed Report

Create report: `templates/skills/ui-design-system/zest-components/.updater/reports/$(date +%Y-%m-%d)-update.md`

**Report MUST include:**

**Executive Summary:**
- Total components checked: X
- Signature changes found: Y
- New components added: Z
- Components deprecated: N

**Signature Changes:**
For each component with signature changes:
```
### ComponentName
- **Change**: Prop `foo` added (optional, type: string)
- **Breaking**: No
- **Source**: ../zest-react-native/src/components/ComponentName.tsx:15

Before:
  interface Props { bar: number }

After:
  interface Props { bar: number; foo?: string }
```

**Components Verified (No Changes):**
- List all components checked that had no signature changes
- Shows thoroughness of the check

**New Components:**
For each new component:
```
### NewComponent
- **Purpose**: Brief description
- **Key Props**: Most important props
- **Source**: ../web/app/libs/zest/src/components/NewComponent.tsx
```

**Deprecated Components:**
- Components no longer in source exports
- Recommend replacement if available

**Production Patterns:**
- Notable usage patterns from shared-mobile-modules
- Best practices observed in real code

**Platform Differences:**
- Differences between web and React Native implementations
- Platform-specific considerations

### PHASE 5: Update Skill Content

Update `templates/skills/ui-design-system/zest-components/SKILL.md` while **preserving frontmatter exactly**:

**Add New Components:**
- Add to appropriate section (similar components grouped)
- Include TypeScript signature (copy from source)
- Show basic usage example
- Explain when to use it
- Include testID example
- Reference production usage if available

**Update Existing Components:**
- Update prop signatures to match source
- Update examples if API changed
- Add notes about breaking changes
- Preserve existing best practices unless incorrect
- Keep testID patterns

**Update Examples:**
- Replace outdated examples with current API
- Add production examples from shared-mobile-modules
- Ensure all examples are valid TypeScript
- Include testID in interactive components

**Maintain Structure:**
- Keep existing section organization
- Preserve "When to Use" guidelines
- Keep anti-patterns and common mistakes
- Maintain consistent formatting

**Guidelines:**
- **Preserve frontmatter** - Name, description, metadata MUST NOT change
- **Exact signatures** - Copy TypeScript types directly from source, don't paraphrase
- **Production examples** - Prefer real examples from shared-mobile-modules over synthetic ones
- **TestID patterns** - All interactive component examples should include testID
- **Platform awareness** - Note when behavior differs between web and native
- **Verify comprehensively** - Check EVERY component's signature, even if it looks unchanged
- **Breaking changes** - Clearly mark any breaking API changes
- **Consistent style** - Match existing documentation formatting

**Critical Rules:**

**DO:**
- ✅ Read TypeScript definitions directly from source files
- ✅ Compare current skill against source repos systematically
- ✅ Preserve frontmatter exactly
- ✅ Include testID in all examples
- ✅ Document platform differences
- ✅ List ALL components checked in report (even unchanged ones)

**DON'T:**
- ❌ Skip signature verification for existing components
- ❌ Add components not in source exports
- ❌ Change skill frontmatter (name, description)
- ❌ Remove well-documented components still in API
- ❌ Make up examples not based on source code
- ❌ Assume API unchanged without checking source

## Report

Display completion status:

```
✓ Updated zest-components skill
✓ Generated report: templates/skills/ui-design-system/zest-components/.updater/reports/YYYY-MM-DD-update.md

Summary:
- Components checked: X
- Signature changes: Y
- New components: Z
- Deprecated: N

Next: Review the generated report and updated skill file.
```

**Artifacts created:**
1. Report: `templates/skills/ui-design-system/zest-components/.updater/reports/$(date +%Y-%m-%d)-update.md`
2. Updated Skill: `templates/skills/ui-design-system/zest-components/SKILL.md`

**IMPORTANT:** The report MUST be created in PHASE 4 before updating the skill file in PHASE 5.
