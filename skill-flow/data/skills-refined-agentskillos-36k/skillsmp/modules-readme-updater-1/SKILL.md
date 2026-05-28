---
name: modules-readme-updater
description: Update the README.md file to list all available journal modules under the Features section with categorized, collapsible sections. Use when adding, removing, or reorganizing modules and keeping documentation in sync.
---

# Modules README Updater

This Skill updates the project README.md to accurately document all existing journal modules in a categorized, collapsible structure under the Features section, preserving existing text and formatting.

## When to use this Skill

Use this Skill when:
- A new module is added or removed
- Module names or emojis change
- Module categories need to be updated
- The README documentation is outdated
- You want to ensure modules are documented consistently with the codebase

## Instructions

### Step 1: Discover all modules and their emojis

1. Scan `resources/views/app/journal/entry/partials/*.blade.php` files.
2. Extract the emoji from each module's `<x-slot:emoji>` tag.
3. Extract the title from each module's `<x-slot:title>` tag.
4. Build a complete list of all modules with their emojis.

### Step 2: Categorize modules

Based on the application's categorization logic, organize modules into these categories:

- 💪 **Body & Health**: Sleep, Physical activity, Health, Hygiene
- 🧠 **Mind & Emotions**: Mood, Energy
- 💼 **Work**: Work, Primary obligation, Day type
- 👥 **Social**: Social density, Kids, Sexual activity
- 📍 **Places**: Travel, Shopping

### Step 3: Update the Features section

1. Locate the Features section in README.md (starts around line 10).
2. Preserve the introductory text: "Daily logging of your life"
3. Replace the module list with categorized collapsible sections.

Structure:

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

  <details>
  <summary>💼 Work (3 modules)</summary>

  - 💼 Work
  - 🎯 Primary obligation
  - 📅 Day type
  </details>

  <details>
  <summary>👥 Social (3 modules)</summary>

  - 👥 Social density
  - 🧒 Kids
  - ❤️ Sexual activity
  </details>

  <details>
  <summary>📍 Places (2 modules)</summary>

  - ✈️ Travel
  - 🛍️ Shopping
  </details>

- Ability to prevent editing older journal entries
```

### Step 4: Preserve existing content

1. DO NOT modify the introductory paragraphs above Features.
2. DO NOT modify sections below Features (Core principles, User and developer principles, etc.).
3. DO NOT change the "Ability to prevent editing older journal entries" line.
4. Only update the module list within the collapsible sections.

### Step 5: Formatting rules

- Use HTML `<details>` and `<summary>` tags for collapsible sections.
- Maintain consistent indentation (2 spaces per level).
- Include a blank line after `<summary>` tag for proper rendering.
- Keep module count in parentheses accurate.
- Use the correct emoji for each module from the codebase.
- Maintain alphabetical or logical ordering within each category.

## Validation checklist

- All modules from `resources/views/app/journal/entry/partials/` are included.
- Each module has the correct emoji from its blade file.
- Modules are categorized correctly (Body & Health, Mind & Emotions, Work, Social, Places).
- Module counts in summaries are accurate.
- Collapsible sections use proper HTML `<details>` tags.
- Markdown indentation is correct (2 spaces per level).
- No unrelated content was changed.
- Introductory text and other features remain unchanged.

## Output expectation

The Features section clearly documents all journal modules organized into categorized, collapsible sections with emojis, using clean and valid Markdown/HTML that renders properly on GitHub.
