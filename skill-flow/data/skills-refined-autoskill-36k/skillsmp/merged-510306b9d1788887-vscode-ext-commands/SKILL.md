---
name: vscode-ext-commands
description: Use this skill when you need to add or update commands in your VS Code extension, following best practices for naming, visibility, and localization.
---

# VS Code extension command contribution

This skill helps you to contribute commands in VS Code extensions.

## When to use this skill

Use this skill when you need to:
- Add or update commands to your VS Code extension.

# Instructions

VS Code commands must always define a `title`, independent of its category, visibility, or location. We use a few patterns for each "kind" of command, with some characteristics described below:

- **Regular commands**: By default, all commands should be accessible in the Command Palette, must define a `category`, and don't need an `icon`, unless the command will be used in the Side Bar.

- **Side Bar commands**: Their names follow a special pattern, starting with an underscore (`_`) and suffixed with `#sideBar`, like `_extensionId.someCommand#sideBar`. They must define an `icon`, and may or may not have some rule for `enablement`. Side Bar exclusive commands should not be visible in the Command Palette. When contributing to the `view/title` or `view/item/context`, inform the _order/position_ for display, and use terms "relative to other command/button" to identify the correct `group`. It is also a good practice to define the condition (`when`) for when the new command is visible.