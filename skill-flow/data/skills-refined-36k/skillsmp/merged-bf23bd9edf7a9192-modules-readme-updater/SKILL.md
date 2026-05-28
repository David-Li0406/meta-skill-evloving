---
name: modules-readme-updater
description: Update the README.md file to list all available journal modules under the Features section, either in a simple list or categorized, collapsible structure. Use when adding, removing, or reorganizing modules and keeping documentation in sync.
---

# Modules README Updater

This Skill updates the project README.md to accurately document all existing journal modules in a clear and consistent structure under the Features section, either as a simple list or in categorized, collapsible sections.

## When to use this Skill

Use this Skill when:
- A new module is added or removed
- Module names or emojis change
- Module categories need to be updated
- The README documentation is outdated
- You want to ensure modules are documented consistently and alphabetically with the codebase

## Instructions

### Step 1: Discover all modules and their emojis

1. Scan `resources/views/app/journal/entry/partials/*.blade.php` files.
2. Extract the emoji from each module's `<x-slot:emoji>` tag.
3. Extract the title from each module's `<x-slot:title>` tag.
4. Build a complete list of all modules with their emojis.

### Step 2: Update the Features section

1. Open README.md and locate the Features section (starts around line 10).
2. Preserve the introductory text: "Daily logging of your life".
3. Choose the desired format for listing modules:
   - **Simple List**: List all modules as sub-items under “Daily logging of your life” in alphabetical order.
   - **Categorized Collapsible Sections**: Organize modules into categories with collapsible sections.

#### Example Structure for Simple List:

```markdown
### Features

- Daily logging of your life
  - Module 1
  - Module 2
  - Module 3
```

#### Example Structure for Categorized Collapsible Sections:

```markdown
### Features

- Daily logging of your life
  <details>
  <summary>💪 Body & Health (4 modules)</summary>

  - 🌖 Sleep
  - 🏃‍♂️ Physical activity
  - ❤️ Health
  - 🧼 Hygiene
  </details>

  <details>
  <summary>🧠 Mind & Emotions (2 modules)</summary>

  - 🙂 Mood
  - ⚡️ Energy
  </details>
```

### Step 3: Formatting rules

- For simple lists, ensure modules are indented as sub-list items and sorted alphabetically.
- For categorized sections, use HTML `<details>` and `<summary>` tags for collapsible sections, maintaining consistent indentation (2 spaces per level).
- Include a blank line after `<summary>` tag for proper rendering.
- Keep module counts in parentheses accurate for collapsible sections.
- Use spaces, not tabs, for indentation.
- Do not modify other sections of README.md or the introductory text.

## Validation checklist

- README.md updated starting at line 10.
- Features section exists.
- All modules are listed correctly.
- Modules are alphabetically ordered or categorized accurately.
- Markdown/HTML indentation is correct.
- No unrelated content was changed.

## Output expectation

The Features section clearly documents all journal modules in the chosen format, using clean and valid Markdown/HTML that renders properly on GitHub.