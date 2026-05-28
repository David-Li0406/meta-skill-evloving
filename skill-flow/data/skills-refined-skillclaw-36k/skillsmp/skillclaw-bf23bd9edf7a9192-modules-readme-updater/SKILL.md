---
name: modules-readme-updater
description: Use this skill to update the README.md file to accurately document all available journal modules under the Features section, ensuring consistency and clarity when adding, removing, or reorganizing modules.
---

# Skill body

This Skill updates the project README.md to accurately document all existing journal modules in a clear, consistent, and properly formatted structure under the Features section.

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

1. Open README.md and locate the Features section (starts around line 10).
2. Preserve the introductory text: "Daily logging of your life".
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
```

### Step 4: Formatting rules

- Use spaces, not tabs.
- Keep indentation consistent.
- Do not add descriptions or extra text.
- Do not modify other sections of README.md.

## Validation checklist

- README.md updated starting at the correct line.
- Features section exists.
- “Daily logging of your life” is the parent item.
- All modules are listed.
- Modules are categorized and formatted correctly.
- Markdown indentation is correct.
- No unrelated content was changed.

## Output expectation

The Features section clearly documents all journal modules as categorized collapsible sections under daily life logging, using clean and valid Markdown.