# Commit Message Examples

## Simple Changes (No Body)

**Typo fix:**

```
Fix typo in README
```

**Simple refactor:**

```
Replace rmdir with rm
```

**Simple addition:**

```
Add eq helper to Handlebars
```

## Simple Body (1-2 Sentences)

**Explaining rationale:**

```
Uppercase README.md and CLAUDE.md

This is necessary to ensure a simpler rebasing process with the skills
repo.
```

**Explaining technical detail:**

```
Fix import paths to use explicit .js extensions

TypeScript's NodeNext module resolution requires explicit file extensions in import paths. This change updates all relative imports to include .js extensions, which is necessary for the compiled JavaScript to work correctly with Node.js ESM.
```

## Bullet List Body

**Multiple specific changes:**

```
Configure package for npm publishing

- Set version to 0.0.1
- Remove private flag to allow publishing
- Update bin entry to point to compiled dist/index.js
- Add files array to specify published files (dist, templates, prompts, docs)
- Add build script using tsconfig.build.json
- Add prepublishOnly hook to build before publishing
```

**Multiple refactoring steps:**

```
Refactor Tag and Tags components

- Extract Tag component into separate file with props for name, href, icon, and selected
- Update Tags to accept ReactNode array of Tag components instead of tag strings
- Simplify Header component by removing discriminated union type and titleHref prop
- Update all Header usages to map tag strings to Tag components
```

## Paragraph + Bullet List

**Context followed by specific changes:**

```
Migrate Tailwind configuration to CSS

Much of the config was straightforward to migrate, but there were a few
items that changed:

- Content: We no longer need to specify the content. This is handled
  automatically in v4.
- Dark mode: We were previously using tailwind-theme-swapper to set the
  dark mode class. However, in v4 this defaults to using the
  `prefers-color-scheme` CSS media feature, which is what we want, so we
  can remove the old configuration.
- Spacing: With v4, we can now set the top-level --spacing variable
  instead of configuring each spacing value individually. In addition, I
  removed the unused spacing values and used the --spacing() function to
  calculate the MainNavigation icon sizes.
- Screens: The previous custom "screens" media queries are now redefined
  as custom variants.
- Custom variants: The previous custom variants (hocus, shocus and
  selected) have all be converted to proper custom variants using the v4
  syntax.
- Extend: Previously, we extended a few values in the original theme.
  This is now easier in Tailwind v4—I just override the variables
  directly.
- Theme swapper: The previous logic that required tailwind-theme-swapper
  can now easily be accomplished by modifying the theme CSS variables
  when in dark mode.
```
