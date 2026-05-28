---
repos:
  - yourcompany/web
  - yourcompany/zest-react-native
---

# Update Zest Integration Skill

## Purpose

Update the Zest Integration skill at `templates/skills/ui-design-system/zest-integration/SKILL.md` with the latest provider, hooks, and theme integration patterns from source repositories.

## Instructions

This workflow analyzes source repositories to detect changes in Zest integration APIs (provider, hooks, theme system) and updates the skill documentation accordingly. Source repositories have been pre-cloned to the parent directory:
- `../web/app/libs/zest` (web implementation)
- `../zest-react-native/src` (React Native implementation)

**IMPORTANT**: Analyze integration APIs from the **source repositories**, not from node_modules or documentation.

Execute workflow phases sequentially, ONE AT A TIME.

## Workflow

### PHASE 1: Read Current Skill

Read `templates/skills/ui-design-system/zest-integration/SKILL.md`:
- Extract frontmatter (MUST preserve exactly)
- Identify documented provider props
- Note documented hooks and their APIs
- Review theme token hierarchy

### PHASE 2: Analyze Source Repositories

**Key Files to Read:**

**Web Implementation:**
- `../web/app/libs/zest/src/provider/ZestProvider.tsx` - Provider implementation
- `../web/app/libs/zest/src/hooks/` - useZestTheme, useZestStyles hooks
- `../web/app/libs/zest/src/theme/` - Theme token definitions

**React Native Implementation:**
- `../zest-react-native/src/provider/ZestProvider.tsx` - Provider implementation
- `../zest-react-native/src/hooks/` - Hook implementations
- `../zest-react-native/src/theme/` - Theme system

**Analysis Steps:**

**Analyze Provider (ZestProvider):**
- Read provider TypeScript definition from both platforms
- Extract exact prop types:
  - `theme` prop structure
  - `children` requirements
  - Optional configuration props
  - Platform-specific props
- Note default behavior
- Check for breaking changes in API

Example:
```typescript
// Read from ../web/app/libs/zest/src/provider/ZestProvider.tsx
interface ZestProviderProps {
  theme?: Theme;
  children: ReactNode;
  // ... extract all props
}
```

**Analyze Hooks:**

For `useZestTheme`:
- Read hook implementation and return type
- Document return value structure
- Note access to theme tokens
- Platform differences

For `useZestStyles`:
- Read hook signature (input and output types)
- Document how StylesConfig works
- Note performance considerations
- Platform-specific behavior

For other hooks:
- Identify any new hooks in source
- Document their purpose and usage

**Analyze Theme System:**

Token Hierarchy:
- Read theme token definitions from `../web/app/libs/zest/src/theme/` and `../zest-react-native/src/theme/`
- Document token categories:
  - Global tokens (primitives)
  - Alias tokens (semantic)
  - Component tokens
- Note dark mode support
- Platform differences in theme structure

### PHASE 3: Identify Changes

Compare source repositories against current documentation:

**Check for Provider Changes:**
- New props added to ZestProvider
- Props removed or deprecated
- Default behavior changes
- Breaking changes to provider API

**Verify Hook Changes:**
- New hooks available
- Hook signature changes
- Return type changes
- Performance improvements or caveats

**Identify Theme Changes:**
- New token categories
- Token naming changes
- Dark mode enhancements
- Platform-specific tokens

**Check for Pattern Changes:**
- Updated integration patterns
- New best practices
- Deprecated patterns

### PHASE 4: Generate Detailed Report

Create report: `templates/skills/ui-design-system/zest-integration/.updater/reports/$(date +%Y-%m-%d)-update.md`

**Report MUST include:**

**Executive Summary:**
- Components checked (Provider, hooks, theme system)
- API changes found
- New features added
- Breaking changes (if any)

**Provider Changes:**
```
### ZestProvider
- **Change**: Added `initialTheme` prop (optional)
- **Breaking**: No
- **Source**: ../zest-react-native/src/provider/ZestProvider.tsx:25

Before:
  interface Props { theme?: Theme; children: ReactNode }

After:
  interface Props { theme?: Theme; initialTheme?: string; children: ReactNode }
```

**Hook Changes:**
For each hook with changes:
- Hook name
- Signature change (input/output)
- Breaking or non-breaking
- Source file reference

**New Features:**
- New hooks available
- New provider props
- New theme capabilities

**Theme System Changes:**
- New token categories
- Token hierarchy updates
- Dark mode enhancements

**Platform Differences:**
- Web vs React Native differences
- Platform-specific considerations
- Migration notes if needed

**Verified (No Changes):**
- List APIs checked that had no changes

### PHASE 5: Update Skill Content

Update `templates/skills/ui-design-system/zest-integration/SKILL.md` while **preserving frontmatter exactly**:

**Update Provider Section:**
- Update ZestProvider prop types
- Update setup examples
- Document new configuration options
- Note breaking changes if any

**Update Hooks Section:**
- Update hook signatures and return types
- Add new hooks if available
- Update usage examples
- Document performance patterns

**Update Theme Section:**
- Update token hierarchy documentation
- Add new token categories
- Update dark mode examples
- Document platform differences

**Update Examples:**
- Ensure all code examples are current
- Update TypeScript types to match source
- Add examples for new features
- Remove examples of deprecated patterns

**Maintain Structure:**
- Keep existing section organization
- Preserve best practices and anti-patterns
- Keep "When to Use" guidelines
- Maintain testing patterns section

**Guidelines:**
- **Preserve frontmatter** - Name, description, metadata MUST NOT change
- **Exact types** - Copy TypeScript interfaces directly from source
- **Integration focus** - Emphasize setup and integration patterns, not component usage
- **Theme tokens** - Document token hierarchy and access patterns
- **Performance** - Note performance implications of patterns (e.g., StylesConfig in render)
- **Platform awareness** - Document differences between web and native
- **Dark mode** - Ensure dark mode patterns are current
- **Testing** - Update testing patterns if needed

**Critical Rules:**

**DO:**
- ✅ Read provider and hook definitions from source files
- ✅ Compare current skill against both web and native implementations
- ✅ Document theme token structure from source
- ✅ Preserve frontmatter exactly
- ✅ Note platform differences
- ✅ Document breaking changes clearly

**DON'T:**
- ❌ Skip API verification
- ❌ Add features not in source
- ❌ Change skill frontmatter
- ❌ Remove documented patterns still valid
- ❌ Make up examples not based on source
- ❌ Ignore platform differences

## Report

Display completion status:

```
✓ Updated zest-integration skill
✓ Generated report: templates/skills/ui-design-system/zest-integration/.updater/reports/YYYY-MM-DD-update.md

Summary:
- APIs checked: Provider, X hooks, theme system
- API changes: Y
- New features: Z
- Breaking changes: N

Next: Review the generated report and updated skill file.
```

**Artifacts created:**
1. Report: `templates/skills/ui-design-system/zest-integration/.updater/reports/$(date +%Y-%m-%d)-update.md`
2. Updated Skill: `templates/skills/ui-design-system/zest-integration/SKILL.md`

**IMPORTANT:** The report MUST be created in PHASE 4 before updating the skill file in PHASE 5.
