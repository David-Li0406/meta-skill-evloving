---
name: claude-skill-importer
description: Automates the import and normalization of Claude Code skills (Markdown files) into the Antigravity skill structure.
---

# Claude Skill Importer

This skill provides utilities to import skills defined for "Claude Code" (e.g., from `any-forward/skills` or loose `.md` files) and convert them into the structured format required by Antigravity Agents.

## Capabilities

1. **Import**: Copies skills from a source directory.
2. **Normalize**:
   - Ensures valid YAML Frontmatter (`name`, `description`) exists.
   - Converts flat `.md` files into valid Skill Directories (`folder/SKILL.md`).
3. **Completeness**:
   - Generates `metadata.json` automatically.
   - Generates `SKILL.ja.md` (Japanse placeholder) automatically to satisfy strict format requirements.

## Usage

You can invoke this skill by running the bundled script via `run_command`.

### Command Syntax

```bash
node .gemini/antigravity/skills/ai-tools/claude-skill-importer/scripts/importer.js <SOURCE_DIRECTORY> [TARGET_CATEGORY_NAME]
```

- **SOURCE_DIRECTORY**: The absolute path to the folder containing Claude skills. This can be:
  - A flat folder of `.md` files.
  - A standard `plugins/` structure (Trail of Bits style).
- **TARGET_CATEGORY_NAME** (Optional): The name of the subdirectory within `.gemini/antigravity/skills/` where these will be placed. Defaults to `imported-skills`.

### Example

```bash
# Import skills from a flat folder into "my-new-skills"
node .gemini/antigravity/skills/ai-tools/claude-skill-importer/scripts/importer.js /Users/me/downloads/claude-skills my-new-skills
```

## Supported Source Formats

- **Flat Markdown**: `folder/my-skill.md` -> `skills/imported/my-skill/SKILL.md`
- **Plugin Structure**: `folder/plugins/my-plugin/skills/my-skill/SKILL.md` -> `skills/imported/my-skill/SKILL.md`

## Localization Process (Post-Import)

The importer script generates `SKILL.ja.md` as a **placeholder**. You MUST complete the translation process manually or by instructing the agent.

1. **Verify**: Check the generated `SKILL.ja.md`. It will contain a `> Note: This is a placeholder` block.
2. **Translate**:
   - Read the content of the English `SKILL.md`.
   - Translate the Title, Description, and Body content into Japanese.
   - **Important**: Keep the YAML Frontmatter keys (like `name`, `description`) in English format, but translate their _values_ if appropriate (or append `(JP)`). Ensure `language: ja` is present.
3. **Overwrite**: Replace the placeholder content in `SKILL.ja.md` with the full Japanese translation.
