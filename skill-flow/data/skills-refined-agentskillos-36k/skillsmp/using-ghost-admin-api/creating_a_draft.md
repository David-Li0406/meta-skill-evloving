# Post a draft to Ghost

Before posting to Ghost, always ensure content quality auditor has gone through the post, and the
human partner has confirmed that all required issues have been resolved.

When posting to Ghost, use the lexical format for content. Ghost's modern editor uses lexical JSON format rather than mobiledoc.

**Content Guidelines:**
- Do NOT use horizontal rules to organize posts - use headings, spacing, or other formatting instead
- Horizontal rules break markdown to lexical conversion and aren't part of alt-counsel's content style

## Building Lexical Content

The skill includes `scripts/ghost-lexical-single.js`, a fluent builder API for creating Ghost lexical format JSON. This makes it easy to programmatically construct Ghost posts with proper lexical structure.

**For detailed reference:** See [ghost-lexical-complete-guide.md](./ghost-lexical-complete-guide.md) for comprehensive documentation on Ghost's lexical format with real-world examples from actual blog posts.

### Basic Usage

```javascript
const { LexicalBuilder, text } = require('./.claude/skills/using-ghost-admin-api/scripts/ghost-lexical-single.js');

const content = new LexicalBuilder()
  .h1('My First Post')
  .paragraph('Hello, ', text.bold('world'), '!')
  .h2('Features')
  .bulletList(['Easy to use', 'One file', 'No dependencies'])
  .build();

console.log(JSON.stringify(content));
```

### Available Methods

The `LexicalBuilder` class provides methods for common content elements:

**Headings:**
- `.h1(content)`, `.h2(content)`, `.h3(content)`, `.h4(content)`, `.h5(content)`, `.h6(content)`

**Text blocks:**
- `.paragraph(...items)` - accepts plain text strings and formatted text objects

**Lists:**
- `.bulletList(items)` - creates unordered list
- `.numberedList(items)` - creates ordered list

**Media & Cards:**
- `.image(src, options)` - image card with optional caption, dimensions
- `.codeBlock(code, language, caption)` - code block with syntax highlighting
- `.bookmark(url, options)` - bookmark card with metadata
- `.signupCard(options)` - newsletter signup card
- `.toggle(heading, content)` - collapsible toggle/accordion

**IMPORTANT:** Do NOT use horizontal rules (`.hr()` or `.lineBreak()`) to organize posts in final drafts. Use headings, spacing, or other formatting instead. Horizontal rules are not part of alt-counsel's content style.

### Text Formatting

Use the `text` helper object to add formatting within paragraphs:

```javascript
.paragraph(
  'This is ',
  text.bold('bold text'),
  ' and this is ',
  text.italic('italic text'),
  ' and ',
  text.code('code'),
  '.'
)
```

Available text formatting:
- `text.normal(content)` - plain text
- `text.bold(content)` - bold
- `text.italic(content)` - italic
- `text.boldItalic(content)` - bold and italic
- `text.code(content)` - inline code
- `text.underline(content)` - underlined
- `text.strikethrough(content)` - strikethrough

### Complete Example

```javascript
const { LexicalBuilder, text, Link } = require('./.claude/skills/using-ghost-admin-api/scripts/ghost-lexical-single.js');

const content = new LexicalBuilder()
  .h1('Technical Deep Dive')
  .paragraph('Welcome to this ', text.bold('comprehensive guide'), ' on legal tech.')
  .h2('Key Features')
  .bulletList([
    'Easy to integrate',
    'No external dependencies',
    'Type-safe builder pattern'
  ])
  .h2('Code Example')
  .codeBlock(
    'function hello() {\n  console.log("Hello, world!");\n}',
    'javascript',
    'A simple example'
  )
  .h2('Learn More')
  .paragraph(
    'For more information, visit ',
    Link.withText('https://example.com', 'our documentation'),
    '.'
  )
  .build();

// Use in Ghost API
const lexical = JSON.stringify(content);
```

## Adding Metadata

Once you have the lexical content, combine it with metadata to create a complete post.

### Auto-generating Missing Metadata

**Important:** When creating a draft, the skill should check if required metadata is missing and generate it automatically:

1. **Title**: If not provided, extract from the first heading (h1/h2) in the lexical content, or generate based on the post content
2. **Custom Excerpt**: If not provided, generate a concise 1-2 sentence summary from the post content (aim for ~250-299 characters)
3. **Tags**: If not provided or if tags need validation, **use the tag-registry skill** to:
   - Suggest 3-4 appropriate tags from the canonical registry
   - Validate that tags follow naming conventions
   - Ensure at least 1 Core Topic tag is included
   - Warn if proposing new tags not in the registry

Before creating the post, always verify these three fields exist and generate them if missing. For tags specifically, invoke the tag-registry skill to ensure consistency and prevent tag sprawl.

### Required and Key Fields

```javascript
const postData = {
  // Required
  title: "Your Post Title",
  lexical: JSON.stringify(content),

  // Key optional fields (with defaults)
  status: "draft",                        // Default: "draft". Options: "draft", "published", "scheduled"
  custom_excerpt: "",                     // Default: auto-generated from content
  tags: [],                               // Default: no tags. Format: [{ name: "TagName" }]
  visibility: "public",                   // Default: "public". Options: "public", "members", "paid"
  featured: false                         // Default: false
};
```

### Complete Example

```javascript
const GhostAdminAPI = require('@tryghost/admin-api');
const { LexicalBuilder, text } = require('./.claude/skills/using-ghost-admin-api/scripts/ghost-lexical-single.js');

// Initialize Ghost API
const api = new GhostAdminAPI({
  url: process.env.GHOST_SITE_URL,
  key: process.env.GHOST_ADMIN_API_KEY,
  version: 'v6.0'
});

// Build content
const content = new LexicalBuilder()
  .h1('Lawyers Got Prompt Engineering Wrong')
  .paragraph('At TechLawFest 2025, Singapore lawyers packed a workshop on prompt engineering.')
  .h2('What Changed')
  .paragraph('Meanwhile, the technology shifted: agent skills became available.')
  .build();

// Create post with metadata
const postData = {
  title: "Lawyers Got Prompt Engineering Wrong (And Why That Matters)",
  lexical: JSON.stringify(content),
  status: "draft",
  custom_excerpt: "At TechLawFest 2025, Singapore lawyers packed a workshop on prompt engineering. Meanwhile, the technology shifted.",
  tags: [
    { name: "Artificial Intelligence" },
    { name: "LegalTech" }
  ],
  visibility: "public",
  featured: false
};

// Create the post
api.posts.add(postData)
  .then((response) => {
    console.log('Post created:', response.url);
    console.log('Post ID:', response.id);
  })
  .catch((error) => {
    console.error('Error:', error);
  });
```

## Recommended: Using the Post Creation Script

