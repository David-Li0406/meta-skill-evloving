---
name: vscode-extensions
description: Instructions for building and installing VS Code extensions in this project.
---

# VS Code Extension Development

This project includes several custom VS Code extensions. To streamline the development and installation process, use the `makeVscePackageforVSCode` terminal function.

## Prerequisites

Ensure you have the following installed:
- `vsce` (Visual Studio Code Extension Manager): `npm install -g @vscode/vsce`
- `code` CLI (should be in your PATH)

## `makeVscePackageforVSCode`

This function automates the entire flow:
1.  **Compiles** the extension (`npm run compile`).
2.  **Packages** the extension into a `.vsix` file, bypassing prompts for missing repositories or licenses.
3.  **Installs** the extension into VS Code, forcing an update if a version is already installed.

### Usage

Navigate to any extension directory (e.g., `visualStudioCodeExtensions/git`) and run:

```bash
makeVscePackageforVSCode
```

> [!TIP]
> This function is defined in `terminal/functions/misc.sh`. If it's not available, ensure your shell has sourced the terminal functions.
