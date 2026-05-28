---
name: vscode-ext-localization
description: Use this skill when you need to localize new or existing VS Code extensions, ensuring all user-facing strings and configurations are properly translated.
---

# Skill body

This skill helps you localize every aspect of VS Code extensions.

## When to use this skill

Use this skill when you need to:

- Localize new or existing contributed configurations (settings), commands, menus, views, or walkthroughs.
- Localize new or existing messages or other string resources contained in extension source code that are displayed to the end user.

## Instructions

VS Code localization is composed of three different approaches, depending on the resource that is being localized. When a new localizable resource is created or updated, the corresponding localization for all currently available languages must be created/updated.

1. **Configurations** (Settings, Commands, Menus, Views, Walkthrough Titles and Descriptions) defined in `package.json`:
   - Create an exclusive `package.nls.LANGID.json` file, such as `package.nls.pt-br.json` for Brazilian Portuguese (`pt-br`) localization.
   
2. **Walkthrough content** (defined in its own Markdown files):
   - Create an exclusive Markdown file like `walkthrough/someStep.pt-br.md` for Brazilian Portuguese localization.
   
3. **Messages and strings** located in extension source code (JavaScript or TypeScript files):
   - Create an exclusive `bundle.l10n.pt-br.json` for Brazilian Portuguese localization.