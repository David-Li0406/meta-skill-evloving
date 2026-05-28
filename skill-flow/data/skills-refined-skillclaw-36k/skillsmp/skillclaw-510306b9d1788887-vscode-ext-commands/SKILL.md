---
name: vscode-ext-commands
description: Use this skill when you need to add or update commands in your VS Code extension, following best practices for naming, visibility, and localization.
---

# Instructions

VS Code commands must always define a `title`, independent of its category, visibility, or location. Here are the patterns for different kinds of commands:

- **Regular commands**: All commands should be accessible in the Command Palette, must define a `category`, and do not need an `icon`, unless the command will be used in the Side Bar.

- **Side Bar commands**: These commands follow a special naming pattern, starting with an underscore (`_`) and suffixed with `#sideBar`, e.g., `_extensionId.someCommand#sideBar`. They must define an `icon` and may have specific rules for `enablement`. Side Bar exclusive commands should not be visible in the Command Palette. When contributing to `view/title` or `view/item/context`, you must specify the _order/position_ for display and identify the correct `group` to use. It is also good practice to define the condition (`when`) for when the new command is visible.