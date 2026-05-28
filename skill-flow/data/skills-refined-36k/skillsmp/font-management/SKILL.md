---
name: Font Management
description: Automates font synchronization, CSS generation, and TypeScript configuration for the application.
---

# Font Management Skill

This skill manages the fonts used in the application. It ensures that font files are properly copied to the public directory, CSS imports are generated, and a TypeScript configuration file is created for usage in the application logic.

## Usage

To synchronize fonts, run the synchronization script:

```bash
node .agent/skills/fonts/scripts/sync-fonts.cjs
```

## What it does

1. **Scans Dependencies**: Reads `package.json` to find all dependencies starting with `@fontsource/`.
2. **Copies Files**: Copies relevant font files (WOFF format, Latin/Latin-Ext subsets, non-italic) from `node_modules` to `public/fonts`.
3. **Generates CSS**: Creates or updates `src/fonts.css` with `@import` statements for the utilized fonts.
4. **Generates TypeScript Config**: Creates `src/lib/fonts.ts` which exports a `FONT_FILES` object mapping font families and weights to their file paths.

## Configuration

The script currently filters for:

- Format: `.woff`
- Subsets: `latin`, `latin-ext` (files matching `*latin*`)
- Style: Normal (excludes `*italic*`)

## Adding a New Font

1. Install the font package:

    ```bash
    npm install @fontsource/font-name
    ```

2. Run the sync script:

    ```bash
    node .agent/skills/fonts/scripts/sync-fonts.cjs
    ```

3. The font is now available in `src/fonts.css` and `src/lib/fonts.ts`.
