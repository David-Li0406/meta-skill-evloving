# Replit Documentation Style Guide

## Core Principles

- Write in active voice and present tense
- Prioritize clarity and consistency
- Use imperative mood and second person (e.g. "you must choose...")
- Keep sentences and paragraphs short (aim for under 25 words per sentence)
- Write for a global audience

## Text Formatting

### Code and Technical Elements
- Use `monospace` for:
  - Code snippets
  - File names and paths
  - Methods, functions, classes, interfaces, etc.
  - Commands and command output
  - Environment variables
  - Database names
  - Package names

### UI Elements
- Use **bold** for:
  - Key terms on first use
  - UI labels including button, dialog, and field names
  - Menu items
    - Use > to separate menu sequences (e.g., **File > Save**)

### Major Titled Works
- Use *italics* for:
  - App names
  - Novel titles, publications, and works of art
  - Scientific names
  - Foreign language words

### Commas
- Use Oxford commas

## Language Guidelines

### Capitalization
- Use sentence case for headings
- Capitalize product-specific terms consistently
- Use lowercase for common technical terms unless they're proper nouns

### Lists
- Introduce lists with complete sentences followed by a colon
- Avoid stating the number of items in the lists when introducing them
- Make list items parallel
- Capitalize the first word of each list item
- Use punctuation consistently within lists
- Use [ordered lists](https://mintlify.com/docs/list-table#ordered-list) for sequential items. Use [unordered lists](https://mintlify.com/docs/list-table#unordered-list) otherwise.
- Use bullet lists for non-sequential items
- Avoid single-item lists

### Links and References
- Use descriptive link text (not "click here" or "this document")
- Make link text meaningful out of context
- Use inline links when possible
- Keep linked text concise

### Numbers
- Spell out numbers zero through nine
- Use numerals for 10 and above
- Use numerals for all measurements
- Don't start sentences with numbers

## Writing Technical Content

### Commands and Code
- Show commands in code blocks using appropriate syntax highlighting
- Include example output when helpful
- Explain any placeholder values
- Use consistent formatting for command flags and arguments

### Procedures
- For multi-line sequential instructions, use the [Steps](#steps) guidance
- Break complex tasks into clear steps
- Begin each step with an action verb
- Include one action per step
- Provide context before steps
- Include expected outcomes where helpful

### Examples
- Use realistic, relevant examples
- Keep examples simple and focused
- Explain complex examples
- Use consistent formatting for similar examples

## Accessibility Guidelines

- Use heading levels in logical order (don't skip levels)
- Provide helpful alt text for images
- Don't rely solely on color to convey meaning
- Use sufficient contrast for text
- Make link text descriptive and unique
- Avoid directional language as the sole identification method ("select the button on the right")

## Content Types

### Headings
- Use sentence case
- Keep headings concise
- Make headings descriptive
- Maintain clear hierarchy
- Avoid placing a sub-heading immediately after a heading
- Limit levels of headings to two when possible

### Tables
- Use clear column headers
- Keep tables simple
- Align similar content consistently
- Use headers to explain table content

### Callouts and Admonitions
- Use the [Mintlify Callout components](https://mintlify.com/docs/content/components/callouts)
- Use callouts sparingly and keep the text concise
- Use [Note Callouts](https://mintlify.com/docs/content/components/callouts#note-callouts) for supplemental info
- Use [Warning Callouts](https://mintlify.com/docs/content/components/callouts#warning-callouts) for potential problems or important cautions
- Use [Info Callouts](https://mintlify.com/docs/content/components/callouts#info-callouts) for Note callouts that require lower visibility
- Use [Tip Callouts](https://mintlify.com/docs/content/components/callouts#tip-callouts) for performance improvements or shortcuts
- Avoid [Check Callouts](https://mintlify.com/docs/content/components/callouts#check-callouts)
- Avoid adjacent callouts

### Accordions and Accordion Groups
- Use [Accordions](https://mintlify.com/docs/content/components/accordions) and [Accordion Group](https://mintlify.com/docs/content/components/accordion-groups#faq-without-icon) components sparingly and only when the content can be skipped

### Card Groups
- Use [Card](https://mintlify.com/docs/content/components/cards) and [Card Group](https://mintlify.com/docs/content/components/card-groups) components sparingly

### Tabs
- Use tabs when displaying a code example or multiple languages or equivalent methods to accomplish the same result
- Use [Code Groups](https://mintlify.com/docs/content/components/code-groups) instead of Tabs when code blocks are independent of the descriptive text
- Avoid including link anchors in tabbed content
- Avoid asymmetric information between tabs

# Tooltips
- Use descriptive text instead of the [Tooltip component](https://mintlify.com/docs/content/components/tooltips) when possible

### Steps
- Use the Mintlify [Steps component](https://mintlify.com/docs/content/components/steps) for multi-line sequential instructions

### Code Blocks
- Use the [Mintlify Code Block component](https://mintlify.com/docs/code)
- Include the language for syntax highlighting and descriptive title
- Limit the code block to the relevant code
- Sparingly use a comment and ellipsis (e.g. "// ...") to omit unnecessary or variable code
- Use [line highlighting](https://mintlify.com/docs/content/components/code#line-highlighting) to emphasize specific lines
- Use [Code Groups](https://mintlify.com/docs/content/components/code-groups) to display a code example in different languages or environments, or [Tabs](#tabs) if each version requires a separate explanation

## Formatting Conventions

### Images
- Use [img tags](https://mintlify.com/docs/image-embeds#using-embeds) for images instead of Markdown syntax
- Always include descriptive and accurate [alt](https://www.w3schools.com/TAGS/att_img_alt.asp) text

### Videos
- Use [iframe tags](https://mintlify.com/docs/image-embeds#videos) to embed YouTube videos
- Avoid relying on video content alone to cover concepts

### File Paths
- Use forward slashes for paths unless specifically showing Windows paths
- Show full paths when necessary for clarity
- Use placeholder text in angle brackets for variable parts of paths unless it conflicts with convention

### Dates and Times
- Format dates as MMM DD, YYYY (e.g., Jan 15, 2024)
- Include time zones when relevant
- Use lowercase "am" and "pm", preceded by a space (e.g. "11:30 am")

## Best Practices

- Keep documentation current and accurate
- Review and update regularly
- Maintain consistent terminology
- Consider the user's perspective
- Focus on clarity over cleverness
- Test instructions before publishing
