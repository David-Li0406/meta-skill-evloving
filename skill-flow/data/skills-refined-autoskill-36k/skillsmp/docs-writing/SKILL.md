---
name: docs-writing
description: Writing clear, user-facing documentation for non-technical users. Use when creating in-app docs, help content, or feature documentation.
license: MIT
metadata:
  author: shipitsmarter
  version: "1.0"
---

# Documentation Writing Guide

A skill for writing consistent, clear documentation for non-technical users.

---

## Purpose

This guide ensures all in-app documentation:
- Is written for **non-technical users** (support agents, operations staff, customers)
- Follows a **consistent structure** and tone
- Uses **plain language** without jargon
- Is **scannable** and **actionable**

---

## Voice & tone

### Be friendly but professional
- Write like you're helping a colleague, not lecturing
- Use "you" to address the reader directly
- Avoid passive voice when possible

### Be concise
- One idea per sentence
- Short paragraphs (2-5 sentences max)
- Cut filler words: "just", "simply", "basically", "actually"

### Be confident
- Use definitive language: "Select Save" not "You should select Save"
- Avoid hedging: "This will update..." not "This should update..."

---

## Structure template

Every doc page should follow this structure:

```markdown
# Page title

Brief one-sentence description of what this page/feature does.

## On this page

<div class="markdown-toc">

- [What you can do here](#what-you-can-do)
- [Step-by-step: Common tasks](#common-tasks)
- [Field guide](#field-guide)
- [Troubleshooting](#troubleshooting)

</div>

## What you can do here {#what-you-can-do}

Bullet list of capabilities (3-6 items).

## Step-by-step: Common tasks {#common-tasks}

### Task name

When to use this: One sentence explaining the scenario.

1. Step one.
2. Step two.
3. Step three.

![Description of screenshot](/docs/area/screenshot-name.png)

**What you should see:**
- Expected result 1
- Expected result 2

---

## Field guide {#field-guide}

### Term or UI element

Plain-language explanation. What it does, when to use it.

---

## Troubleshooting {#troubleshooting}

### "Error message or problem description"

**Likely cause:**
Brief explanation.

**What to try:**
1. First thing to try.
2. Second thing to try.

---

## Related pages

- [Related page 1](/docs/related-page-1)
- [Related page 2](/docs/related-page-2)
```

---

## Writing rules

### Headings

| Level | Use for | Example |
|-------|---------|---------|
| H1 | Page title only (one per page) | `# Shipments` |
| H2 | Major sections | `## What you can do here` |
| H3 | Tasks, terms, or problems | `### Create a shipment` |
| H4 | Subsections within H3 (rare) | `#### Advanced options` |

### Lists

- Use **numbered lists** for sequential steps
- Use **bullet lists** for non-sequential items
- Keep list items parallel in structure
- Start each item with a verb when possible

**Good:**
1. Open the Settings panel.
2. Select your preferred option.
3. Select Save.

**Bad:**
1. You need to open Settings.
2. The preferred option should be selected.
3. Saving is the next step.

### UI elements

| Element | How to write | Example |
|---------|--------------|---------|
| Buttons | Bold, exact label | Select **Save** |
| Menu items | Bold, exact label | Select **File** > **Export** |
| Field names | Bold | Enter the **Reference number** |
| Tabs | Bold | Open the **Details** tab |
| Page names | Bold | Go to the **Shipments** page |
| Keyboard keys | Code format | Press `Ctrl+S` |
| Values/input | Code format | Enter `123456` |

### Screenshots

- Use sparingly — only when UI is complex or non-obvious
- Capture only the relevant area (crop tightly)
- Add a brief alt text description
- Name files descriptively: `create-shipment-step-2-address.png`
- Store in `public/docs/<area>/`

```markdown
![The address form with required fields highlighted](/docs/shipments/create-shipment-address-form.png)
```

### Links

**Internal docs links:**
```markdown
See [Creating a shipment](/docs/shipment-create) for details.
```

**Section links (same page):**
```markdown
See [Troubleshooting](#troubleshooting) below.
```

**External links** (open in new tab automatically):
```markdown
Learn more at [PostHog docs](https://posthog.com/docs).
```

---

## Language guidelines

### Words to use

| Instead of | Use |
|------------|-----|
| utilize | use |
| terminate | end, stop |
| commence | start, begin |
| prior to | before |
| in order to | to |
| functionality | feature |
| leverage | use |
| facilitate | help, enable |
| endeavor | try |
| optimal | best |

### Words to avoid

| Avoid | Why |
|-------|-----|
| simple, simply | Implies it's the user's fault if they struggle |
| just | Minimizes effort; often unnecessary |
| obviously | If it were obvious, you wouldn't need to say it |
| easy | Subjective; can frustrate users |
| please | Unnecessary in instructions |
| etc. | Be specific or omit |
| click | Use "select" (works for mouse, touch, keyboard) |

### Technical terms

When you must use a technical term:
1. Define it on first use
2. Add it to the Field guide section
3. Use consistently throughout

```markdown
Select the **carrier** (the company that delivers the package).
```

---

## Formatting patterns

### Callouts

Use blockquotes for important notes:

```markdown
> **Note:** This action cannot be undone.
```

```markdown
> **Tip:** You can also press `Ctrl+S` to save quickly.
```

### Code/values

Use backticks for:
- Exact values to enter: `ABC123`
- Keyboard shortcuts: `Ctrl+C`
- File names: `export.csv`
- Error codes: `ERR_TIMEOUT`

### Tables

Use for comparing options or listing fields:

```markdown
| Field | Required | Description |
|-------|----------|-------------|
| Reference | Yes | Your internal order number |
| Weight | Yes | Package weight in kg |
| Notes | No | Optional delivery instructions |
```

---

## Accessibility

- Write descriptive link text: "See [how to create a shipment](/docs/...)" not "Click [here](/docs/...)"
- Add alt text to all images
- Don't rely on color alone to convey meaning
- Use proper heading hierarchy (don't skip levels)

---

## Example: Before & after

### Before (too technical, passive, wordy)

> In order to utilize the shipment creation functionality, users should navigate to the Shipments page and click on the "Create" button. The system will then display a form where the user can input the necessary shipment details. It is recommended that all required fields are completed prior to submission.

### After (clear, active, scannable)

> ## Create a shipment
>
> 1. Go to the **Shipments** page.
> 2. Select **Create**.
> 3. Fill in the required fields (marked with *).
> 4. Select **Save**.
>
> **What you should see:** The new shipment appears in your list.

---

## Checklist before publishing

- [ ] Page follows the structure template
- [ ] Title is clear and matches what users would search for
- [ ] TOC links work correctly
- [ ] All screenshots exist and are properly sized
- [ ] No jargon without explanation
- [ ] Steps are numbered and start with verbs
- [ ] UI elements are bold
- [ ] Links use descriptive text
- [ ] Troubleshooting covers common issues
- [ ] Related pages section links to relevant docs
- [ ] Ran docs-assets test: `npm run test -- src/docs/__tests__/docs-assets.spec.ts`

---

## Quick reference card

```
STRUCTURE
─────────
# Title (one H1)
## On this page (TOC)
## What you can do here
## Step-by-step: Common tasks
### Task name
## Field guide
### Term
## Troubleshooting
### "Problem"
## Related pages

FORMATTING
──────────
**Bold** = UI elements (buttons, fields, pages)
`Code` = values, keys, file names
[Link text](/docs/slug) = internal links
![Alt text](/docs/area/file.png) = images
> **Note:** = callouts

LANGUAGE
────────
• Use "select" not "click"
• Use "you" not "the user"
• Start steps with verbs
• One idea per sentence
• Cut: just, simply, easy, please
```

---

## File locations in this project

- **Doc pages:** `src/docs/pages/*.md`
- **Registry:** `src/docs/registry.ts` (register new docs here)
- **Hierarchy:** `src/docs/hierarchy.ts` (add metadata for breadcrumbs)
- **Screenshots:** `public/docs/<area>/`
- **Styles:** `src/assets/scss/components/_markdown.scss`

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| **planning** | Documentation planning as part of feature development |
| **pr-review** | Documentation verification during PR review |
