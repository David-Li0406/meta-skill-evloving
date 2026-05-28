---
name: obsidian-plugin-deploy
description: Build and deploy Obsidian plugins to Windows test vault from WSL or Windows environment. Use when working on Obsidian plugin development and need to test changes in the actual Obsidian application. Handles npm build, file copying to vault paths, and creates plugin directory structure automatically. Cross-platform support for WSL and native Windows.
---

# Obsidian Plugin Deploy

## Overview

This skill automates the build and deployment process for Obsidian plugins when developing in WSL or Windows environments. It builds the plugin, creates the necessary directory structure, and copies files to the correct location in the vault.

## Quick Start

Deploy the current plugin to test vault:

```bash
python3 .claude/skills/obsidian-plugin-deploy/scripts/deploy.py
```

Or on Windows:
```cmd
python .claude/skills/obsidian-plugin-deploy/scripts/deploy.py
```

The script will:
1. Run `npm run build` to compile the plugin
2. Auto-detect the correct vault path (WSL `/mnt/c/` or Windows `C:\`)
3. Create the plugin directory at `<vault>/.obsidian/plugins/ai-terminal/`
4. Copy `main.js`, `manifest.json`, and `styles.css` to the plugin directory
5. Display success message

After deployment, reload Obsidian (Ctrl+R) to see the changes.

## Configuration

The deployment script uses these default values:
- **Plugin ID**: `ai-terminal`
- **Test Vault (WSL)**: `/mnt/c/obsidian/test`
- **Test Vault (Windows)**: `C:\obsidian\test`

To modify these values, edit the script configuration:

```python
# In .claude/skills/obsidian-plugin-deploy/scripts/deploy.py
PLUGIN_ID = "your-plugin-id"
OBSIDIAN_TEST_VAULT = Path("/mnt/c/path/to/your/vault")
```

The script automatically detects the environment and adjusts paths accordingly.

## Workflow

1. **Make changes** to plugin source code
2. **Run deployment script** to build and copy files
3. **Reload Obsidian** (Ctrl+R in the app)
4. **Test changes** in Obsidian
5. Repeat as needed

## Troubleshooting

**Build fails**: Check that `npm install` has been run and `package.json` is configured correctly.

**Permission denied**: Ensure the vault path is accessible and you have write permissions.

**Plugin not appearing**: Verify the plugin directory was created and contains all required files (`main.js`, `manifest.json`).

**Changes not reflected**: Make sure to reload Obsidian after deployment (Ctrl+R or restart the app).

**Path not found**: The script auto-detects WSL vs Windows paths. If detection fails, manually edit `OBSIDIAN_TEST_VAULT` in the script.

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Examples from other skills:**
- PDF skill: `fill_fillable_fields.py`, `extract_form_field_info.py` - utilities for PDF manipulation
- DOCX skill: `document.py`, `utilities.py` - Python modules for document processing

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read by Codex for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Codex's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Codex should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Codex produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Not every skill requires all three types of resources.**
