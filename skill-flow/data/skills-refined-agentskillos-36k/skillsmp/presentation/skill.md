---
name: presentation
description: Generate a Marp presentation from an intent's spec. Use when the user wants to create slides for an intent or asks to make a presentation.
user-invocable: true
---

# Presentation

You are helping the user generate a Marp presentation from an intent specification.

## Workflow

1. Check `.sejas/open/` for intents - list them if multiple exist
2. Ask which intent to create presentation for (if multiple) or confirm the intent
3. Read the spec.md to understand the intent content
4. Generate a Marp-compatible markdown file with this structure:
   ```markdown
   ---
   marp: true
   theme: default
   paginate: true
   ---

   # [Intent Title]

   **[Your Name/Organization]**
   _Date: YYYY-MM-DD_

   ---

   ## Problem

   [Brief description from spec's Problem section]

   ---

   ## Solution

   [Brief description from spec's Solution section]

   ---

   ## Requirements

   - Requirement 1
   - Requirement 2
   - Requirement 3

   ---

   ## Implementation Details

   [If available from notes.md or spec]

   ---

   ## Demo / Results

   [Placeholder for demo or results]

   ---

   ## Questions?

   Thank you!
   ```

5. Save the markdown file to `.sejas/open/INTENT_FOLDER/assets/presentation.md`
6. Ask: "Would you like to generate the presentation now? (requires npx)"
7. If yes, run: `npx -y @marp-team/marp-cli@latest assets/presentation.md -o assets/presentation.html --html`
8. Confirm the presentation files have been created and show the paths

## Marp Slide Guidelines

- Use `---` to separate slides
- Keep slides concise (3-5 bullets max per slide)
- Use headers (`#`, `##`) for slide titles
- Front matter must include `marp: true`
- Common themes: `default`, `gaia`, `uncover`

## Important Notes

- Always save to the intent's assets folder
- Generate both .md and .html (if user confirms)
- The markdown should be presentation-ready (concise, visual)
- Don't copy the entire spec - create a summary suitable for slides
- Each slide should have a single clear message

## Example Front Matter Options

```yaml
---
marp: true
theme: default
paginate: true
header: 'Your Header Text'
footer: 'Your Footer Text'
backgroundColor: '#fff'
---
```

## Marp CLI Options

- HTML output: `npx @marp-team/marp-cli presentation.md -o presentation.html --html`
- PDF output: `npx @marp-team/marp-cli presentation.md -o presentation.pdf`
- Multiple formats: `npx @marp-team/marp-cli presentation.md -o presentation.html --html --pdf`
- Watch mode: `npx @marp-team/marp-cli -w presentation.md`
