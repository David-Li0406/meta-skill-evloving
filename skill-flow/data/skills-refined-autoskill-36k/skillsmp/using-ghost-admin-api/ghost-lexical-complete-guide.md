# Ghost Admin API - Complete Lexical Format Guide

**Extracted from real Ghost blog posts**

This comprehensive guide provides real-world examples from Ghost Admin API responses showing how to structure all major content types in the Lexical format.

## Overview

Ghost uses a Lexical JSON format for rich text content. All content must be wrapped in a root structure:

```json
{
  "root": {
    "children": [/* content nodes go here */],
    "direction": "ltr",
    "format": "",
    "indent": 0,
    "type": "root",
    "version": 1
  }
}
```

---

## Table of Contents

### Basic Content
1. [Paragraphs](#1-paragraphs)
2. [Headers](#2-headers)
3. [Links](#3-links-inside-paragraphs)
4. [Text Formatting](#4-text-formatting)
5. [Lists](#5-lists)

### Rich Media
6. [Images](#6-images)
7. [Code Blocks](#7-code-blocks)

### Interactive Cards
8. [Bookmark Cards](#8-bookmark-cards)
9. [Signup Cards](#9-signup-cards)
10. [Toggle/Accordion](#10-toggle-accordion)

### Other Elements
11. [Line Breaks](#11-line-breaks)
12. [Post Metadata](#12-post-metadata)

---

## 1. Paragraphs

### Simple Paragraph

The most basic content unit. Contains text nodes as children.

```json
{
  "type": "paragraph",
  "children": [
    {
      "type": "extended-text",
      "text": "175,000 monthly downloads. Top 10% of 700,000 PyPI packages. Still a weekend project.",
      "format": 0,
      "detail": 0,
      "mode": "normal",
      "style": "",
      "version": 1
    }
  ],
  "direction": "ltr",
  "format": "",
  "indent": 0,
  "version": 1
}
```

**Key Fields:**
- `type`: Always `"paragraph"`
- `children`: Array of text or link nodes
- `direction`: Text direction (`"ltr"` for left-to-right)
- `indent`: Indentation level (0 = no indent)

---

## 2. Headers

### H2 Header

Headers use the `extended-heading` type with a `tag` field specifying the level.

```json
{
  "type": "extended-heading",
  "tag": "h2",
  "children": [
    {
      "type": "extended-text",
      "text": "What Top 10% Actually Means",
      "format": 0,
      "detail": 0,
      "mode": "normal",
      "style": "",
      "version": 1
    }
  ],
  "direction": "ltr",
  "format": "",
  "indent": 0,
  "version": 1
}
```

**Key Fields:**
- `type`: Always `"extended-heading"`
- `tag`: Header level - `"h1"`, `"h2"`, `"h3"`, `"h4"`, `"h5"`, or `"h6"`

**Available Header Tags:**
- `h1` - Main title (rarely used in content)
- `h2` - Section headers
- `h3` - Sub-section headers
- `h4`, `h5`, `h6` - Further nested headers

---

## 3. Links Inside Paragraphs

### Paragraph with Inline Links

Links are child nodes within paragraphs. Text before/after links are separate text nodes.

```json
{
  "type": "paragraph",
  "children": [
    {
      "type": "extended-text",
      "text": "Two years ago, I wrote about the unexpected joys of open source",
      "format": 0,
      "detail": 0,
      "mode": "normal",
      "style": "",
      "version": 1
    },
    {
      "type": "link",
      "url": "https://www.alt-counsel.com/the-unexpected-joys-of-open-source/",
      "children": [],
      "direction": "ltr",
      "format": "",
      "version": 1,
      "rel": null,
      "target": null,
      "title": null
    },
    {
      "type": "extended-text",
      "text": " when redlines went briefly viral. Last month, I discussed ",
      "format": 0,
      "detail": 0,
      "mode": "normal",
      "style": "",
      "version": 1
    },
    {
      "type": "link",
      "url": "https://www.alt-counsel.com/open-source-ai-and-why-october-matters/",
      "children": [
        {
          "type": "extended-text",
          "text": "adapting it for AI agents.",
          "format": 0,
          "detail": 0,
          "mode": "normal",
          "style": "",
          "version": 1
        }
      ],
      "direction": "ltr",
      "format": "",
      "indent": 0,
      "version": 1,
      "rel": "noreferrer",
      "target": null,
      "title": null
    }
  ],
  "direction": "ltr",
  "format": "",
  "indent": 0,
  "version": 1
}
```

**Link Types:**
1. **Empty link** (bare URL): `children: []` - URL text appears automatically
2. **Link with custom text**: `children` contains the link text

**Key Fields:**
- `type`: Always `"link"`
- `url`: The target URL (required)
- `children`: Empty array for bare URLs, or array with text nodes for custom text
- `rel`: Relationship attribute (e.g., `"noreferrer"`)
- `target`: Target attribute (e.g., `"_blank"`)
- `title`: Link title attribute

---

## 4. Text Formatting

### Bold Text

Formatting is controlled by the `format` field using bitwise flags.

```json
{
  "type": "paragraph",
  "children": [
    {
      "type": "extended-text",
      "text": "No revenue.",
      "format": 2,
      "detail": 0,
      "mode": "normal",
      "style": "",
      "version": 1
    },
    {
      "type": "extended-text",
      "text": " Enterprise companies use redlines and contribute $0.",
      "format": 0,
      "detail": 0,
      "mode": "normal",
      "style": "",
      "version": 1
    }
  ],
  "direction": "ltr",
  "format": "",
  "indent": 0,
  "version": 1
}
```

### Italic Text

```json
{
  "type": "extended-text",
  "text": "Every line of code is a long-term liability.",
  "format": 1,
  "detail": 0,
  "mode": "normal",
  "style": "",
  "version": 1
}
```

**Format Values (Bitwise Flags):**
- `0` = No formatting (normal text)
- `1` = Italic
- `2` = Bold
- `3` = Bold + Italic (1 + 2)
- `4` = Underline
- `8` = Strikethrough
- `16` = Code
- Combine with bitwise OR or addition

**Common Combinations:**
- Plain text: `format: 0`
- Italic: `format: 1`
- Bold: `format: 2`
- Bold + Italic: `format: 3`
- Code: `format: 16`
- Bold + Code: `format: 18` (2 + 16)

---

## 5. Lists

### Unordered List (Bullets)

Lists contain `listitem` children, each with their own text content.

```json
{
  "type": "list",
  "listType": "bullet",
  "start": 1,
  "tag": "ul",
  "children": [
    {
      "type": "listitem",
      "value": 1,
      "children": [
        {
          "type": "extended-text",
          "text": "Comparing contract drafts without uploading to third-party services",
          "format": 0,
          "detail": 0,
          "mode": "normal",
          "style": "",
          "version": 1
        }
      ],
      "direction": "ltr",
      "format": "",
      "indent": 0,
      "version": 1
    },
    {
      "type": "listitem",
      "value": 2,
      "children": [
        {
          "type": "extended-text",
          "text": "Tracking legislative changes",
          "format": 0,
          "detail": 0,
          "mode": "normal",
          "style": "",
          "version": 1
        }
      ],
      "direction": "ltr",
      "format": "",
      "indent": 0,
      "version": 1
    }
  ],
  "direction": "ltr",
  "format": "",
  "indent": 0,
  "version": 1
}
```

### Ordered List (Numbers)

Change `listType` to `"number"` and `tag` to `"ol"`:

```json
{
  "type": "list",
  "listType": "number",
  "start": 1,
  "tag": "ol",
  "children": [/* same listitem structure as above */],
  "direction": "ltr",
  "format": "",
  "indent": 0,
  "version": 1
}
```

**Key Fields:**
- `type`: Always `"list"`
- `listType`: `"bullet"` for unordered, `"number"` for ordered
- `tag`: `"ul"` for bullets, `"ol"` for numbered
- `start`: Starting number (typically `1`)
- `children`: Array of `listitem` nodes

**List Item Fields:**
- `type`: Always `"listitem"`
- `value`: Sequential number for the item
- `children`: Text content (can include formatted text and links)

---

## 6. Images

### Image Card

Real example from production Ghost blog:

```json
{
  "type": "image",
  "version": 1,
  "src": "https://www.alt-counsel.com/content/images/2025/10/Screenshot-2025-10-18-at-8.57.01---PM.png",
  "width": 2434,
  "height": 1776,
  "title": "",
  "alt": "",
  "caption": "<span style=\"white-space: pre-wrap;\">The output from Claude using my 3 page prompt. An illustrated deal timeline. A table of key terms with colour coded risk highlights. Isn't it mind blowing what you can generate with AI in 2024?</span>",
  "cardWidth": "regular",
  "href": ""
}
```

**Key Fields:**
- `type`: Always `"image"`
- `src`: Image URL (required)
- `width`: Image width in pixels
- `height`: Image height in pixels
- `alt`: Alt text for accessibility
- `title`: Image title
- `caption`: Caption displayed below image (can contain HTML)
- `cardWidth`: Display width - `"regular"`, `"wide"`, or `"full"`
- `href`: Optional link URL when image is clicked

**Card Width Options:**
- `"regular"` - Standard content width
- `"wide"` - Wider than content
- `"full"` - Full width of page

---

## 7. Code Blocks

### Code Block with Syntax Highlighting

Real example showing a Markdown code block:

```json
{
  "type": "codeblock",
  "version": 1,
  "code": "---\nname: Generate a pitch\ndescription: Define the scope of an article or newsletter\nwhen_to_use: at the beginning of drafting an article or newsletter\n---\n\n## Overview\nA pitch is a critical step in writing a blog that ensures that the aim\nof the post is clear and within a manageable scope...",
  "language": "markdown",
  "caption": ""
}
```

**Key Fields:**
- `type`: Always `"codeblock"`
- `code`: The actual code content (string, can contain newlines)
- `language`: Programming language for syntax highlighting
- `caption`: Optional caption below the code block
- `version`: Always `1`

**Common Language Values:**
- `"javascript"`, `"typescript"`
- `"python"`, `"java"`, `"cpp"`, `"csharp"`
- `"html"`, `"css"`, `"markdown"`
- `"bash"`, `"shell"`
- `"json"`, `"yaml"`, `"xml"`
- `"sql"`, `"graphql"`
- `"plaintext"` - for no highlighting

---

## 8. Bookmark Cards

### Bookmark Card

Rich preview cards for external links. Ghost auto-fetches metadata.

```json
{
  "type": "bookmark",
  "version": 1,
  "url": "https://www.alt-counsel.com/the-unexpected-joys-of-open-source/",
  "metadata": {
    "icon": "https://www.alt-counsel.com/content/images/icon/Small-Al---Counsel-Logo-17.png",
    "title": "The Unexpected Joys of Open Source",
    "description": "A brief flirtation with viral success brought new attention to one of my Python libraries and some real-world applications of the workings of open-source.",
    "author": "Houfu Ang",
    "publisher": "Alt + Counsel",
    "thumbnail": "https://www.alt-counsel.com/content/images/thumbnail/photo-1682687982049-b3d433368cd1-2"
  },
  "caption": ""
}
```

**Key Fields:**
- `type`: Always `"bookmark"`
- `url`: Target URL (required)
- `metadata`: Auto-fetched metadata object
  - `icon`: Favicon URL
  - `title`: Page title
  - `description`: Meta description
  - `author`: Author name
  - `publisher`: Publisher/site name
  - `thumbnail`: Preview image URL
- `caption`: Optional caption text

**Note:** Ghost automatically fetches metadata when you provide just the URL.

---

## 9. Signup Cards

### Email Signup/Newsletter Card

Real example showing full configuration:

```json
{
  "type": "signup",
  "version": 1,
  "alignment": "left",
  "backgroundColor": "#F0F0F0",
  "backgroundImageSrc": "",
  "backgroundSize": "cover",
  "textColor": "#000000",
  "buttonColor": "accent",
  "buttonTextColor": "#FFFFFF",
  "buttonText": "Subscribe",
  "disclaimer": "<span style=\"white-space: pre-wrap;\">No spam. Unsubscribe anytime.</span>",
  "header": "<span style=\"white-space: pre-wrap;\">Sign up for Alt + Counsel</span>",
  "labels": [],
  "layout": "wide",
  "subheader": "<span style=\"white-space: pre-wrap;\">Practical legal tech from Singapore. For teams that build solutions.</span>",
  "successMessage": "Email sent! Check your inbox to complete your signup.",
  "swapped": false
}
```

**Key Fields:**
- `type`: Always `"signup"`
- `version`: Always `1`
- `header`: Main heading text (HTML)
- `subheader`: Description/subtitle (HTML)
- `buttonText`: Text on the subscribe button
- `disclaimer`: Fine print text (HTML)
- `successMessage`: Message shown after submission
- `alignment`: Text alignment - `"left"`, `"center"`, or `"right"`
- `layout`: Card layout - `"wide"` or `"full"`
- `backgroundColor`: Hex color code (e.g., `"#F0F0F0"`)
- `backgroundImageSrc`: Optional background image URL
- `backgroundSize`: Background image sizing - `"cover"` or `"contain"`
- `textColor`: Text color hex code
- `buttonColor`: Button color - `"accent"` or hex code
- `buttonTextColor`: Button text color hex code
- `labels`: Array of label IDs to tag subscribers
- `swapped`: Boolean - swap image/content position

**Layout Options:**
- `"wide"` - Standard card width
- `"full"` - Full width of content area

---

## 10. Toggle (Accordion)

### Collapsible Content Section

Real example showing a table of contents:

```json
{
  "type": "toggle",
  "version": 1,
  "heading": "<span style=\"white-space: pre-wrap;\">Table of Contents</span>",
  "content": "<ol><li value=\"1\"><a href=\"#the-inflection-point-september-2025\" rel=\"noreferrer\"><span style=\"white-space: pre-wrap;\">The Inflection Point (September 2025)</span></a></li><li value=\"2\"><a href=\"#two-paradigmschat-vs-agents\" rel=\"noreferrer\"><span style=\"white-space: pre-wrap;\">Two Paradigms - Chat vs Agents</span></a></li></ol>"
}
```

**Key Fields:**
- `type`: Always `"toggle"`
- `version`: Always `1`
- `heading`: The clickable header text (HTML)
- `content`: The collapsible content (HTML)

**Use Cases:**
- Table of contents
- FAQ sections
- Expandable details
- Spoiler content
- Long lists or sections that can be hidden

**Note:** Both `heading` and `content` fields accept HTML markup, allowing for rich formatting.

---

## 11. Line Breaks

### Horizontal Rule / Divider

```json
{
  "type": "linebreak",
  "version": 1
}
```

**Key Fields:**
- `type`: Always `"linebreak"`
- `version`: Always `1`

**Usage:** Creates a visual separator between content sections, rendered as a horizontal line.

---

## 12. Post Metadata

### Complete Post Structure

When creating or updating a post, you need both the lexical content AND metadata:

```json
{
  "posts": [{
    "title": "What Top 10% Actually Means (For a Lawyer Who Codes)",
    "slug": "what-top-10-actually-means-for-a-lawyer-who-codes",
    "lexical": "{\"root\":{\"children\":[...],\"type\":\"root\",...}}",
    "status": "published",
    "visibility": "public",
    "featured": false,
    "custom_excerpt": "177K monthly downloads. Top 10% of 700K packages...",
    "feature_image": "https://www.alt-counsel.com/content/images/2025/10/Screenshot.png",
    "feature_image_caption": "<span style=\"white-space: pre-wrap;\">Screenshot description</span>",
    "tags": ["Open Source", "Python", "Programming", "LegalTech"],
    "authors": ["houfu@outlook.sg"],
    "published_at": "2025-10-27T00:26:45.000Z",
    "updated_at": "2025-10-20T08:17:09.000Z"
  }]
}
```

**Key Metadata Fields:**
- `title`: Post title (required)
- `slug`: URL-friendly slug (auto-generated if omitted)
- `lexical`: JSON string of content (use `JSON.stringify()`)
- `status`: `"draft"`, `"published"`, or `"scheduled"`
- `visibility`: `"public"`, `"members"`, or `"paid"`
- `featured`: Boolean for featured posts
- `custom_excerpt`: Custom excerpt/description
- `feature_image`: Featured image URL
- `feature_image_caption`: Caption for featured image
- `tags`: Array of tag names or slugs
- `authors`: Array of author emails or IDs
- `published_at`: Publication date (ISO 8601 format)
- `updated_at`: Last update timestamp (required for updates)

---

## Quick Reference Guide

### Format Flag Cheat Sheet

| Format | Value | Description |
|--------|-------|-------------|
| Normal | 0 | Plain text |
| Italic | 1 | *Italic* |
| Bold | 2 | **Bold** |
| Bold+Italic | 3 | ***Bold Italic*** |
| Underline | 4 | Underlined |
| Strikethrough | 8 | ~~Strikethrough~~ |
| Code | 16 | `Code` |

Combine with bitwise OR or addition (e.g., Bold + Italic = 2 + 1 = 3).

### Common Content Patterns

**Blog Post Structure:**
1. Opening paragraph
2. H2 Headers for sections
3. Paragraphs with formatted text and links
4. Bullet/numbered lists
5. Images with captions
6. Code blocks (for technical content)
7. Bookmark cards (for references)
8. Signup card (at end)

**Newsletter Structure:**
1. Brief intro paragraph
2. Toggle for table of contents
3. Multiple H2 sections
4. Bookmark cards for each article
5. Signup card

### Node Type Summary

| Type | Purpose | Children |
|------|---------|----------|
| `paragraph` | Text block | text, links |
| `extended-heading` | Headers (H1-H6) | text |
| `list` | Bullet/numbered lists | listitem |
| `listitem` | List items | text, links |
| `link` | Hyperlinks | text (optional) |
| `extended-text` | Actual text content | none |
| `image` | Images with captions | none |
| `codeblock` | Code with syntax highlighting | none |
| `bookmark` | Link preview cards | none |
| `signup` | Email signup forms | none |
| `toggle` | Collapsible sections | none |
| `linebreak` | Horizontal divider | none |

---

## Tips & Best Practices

1. **Lexical String:** Always stringify your Lexical JSON when sending to API
   ```javascript
   lexical: JSON.stringify(lexicalObject)
   ```

2. **Empty Links:** For bare URLs, use empty children array:
   ```json
   {"type": "link", "url": "https://example.com", "children": []}
   ```

3. **Update Timestamps:** Always include current `updated_at` when updating posts

4. **List Values:** List item `value` should be sequential (1, 2, 3...)

5. **Direction:** Use `"ltr"` for left-to-right languages (English, etc.)

6. **Version Fields:** Always include `version: 1` for nodes

7. **Required Fields:** Every container node needs:
   - `type`
   - `version`
   - `direction`
   - `format`
   - `indent`

8. **Testing:** Use `status: "draft"` when testing, then publish when ready

9. **Image Captions:** Can contain HTML for rich formatting

10. **Code Blocks:** Use appropriate language identifier for syntax highlighting

11. **Signup Cards:** Place at strategic points (mid-article or at end)

12. **Toggle Sections:** Great for long lists or optional content

---

## API Usage Examples

### Create a Post with Various Content Types

```bash
curl -X POST "https://your-site.com/ghost/api/admin/posts/" \
  -H "Authorization: Ghost YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept-Version: v6.0" \
  -d '{
    "posts": [{
      "title": "Complete Example Post",
      "lexical": "{\"root\":{\"children\":[{\"type\":\"paragraph\",\"children\":[{\"type\":\"extended-text\",\"text\":\"Opening paragraph\",\"format\":0,\"detail\":0,\"mode\":\"normal\",\"style\":\"\",\"version\":1}],\"direction\":\"ltr\",\"format\":\"\",\"indent\":0,\"version\":1},{\"type\":\"image\",\"version\":1,\"src\":\"https://example.com/image.jpg\",\"alt\":\"Example\",\"caption\":\"\",\"width\":1200,\"height\":800},{\"type\":\"codeblock\",\"version\":1,\"code\":\"console.log('\''Hello'\'');\",\"language\":\"javascript\",\"caption\":\"\"},{\"type\":\"signup\",\"version\":1,\"header\":\"Subscribe\",\"subheader\":\"Get updates\",\"buttonText\":\"Subscribe\"}],\"direction\":\"ltr\",\"format\":\"\",\"indent\":0,\"type\":\"root\",\"version\":1}}",
      "status": "draft"
    }]
  }'
```

### Update a Post

```bash
curl -X PUT "https://your-site.com/ghost/api/admin/posts/POST_ID/" \
  -H "Authorization: Ghost YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept-Version: v6.0" \
  -d '{
    "posts": [{
      "updated_at": "2025-10-20T08:17:09.000Z",
      "title": "Updated Title"
    }]
  }'
```

---

## Additional Resources

- [Ghost Admin API Documentation](https://ghost.org/docs/admin-api/)
- [Lexical Editor Documentation](https://lexical.dev/)
- Ghost Content API for reading published content
- Ghost Webhooks for automation

---

**Document Version:** 2.0  
**Last Updated:** October 2025  
**Ghost API Version:** v6.0  
**Based on:** Real production Ghost blog data (2 posts analyzed)

**Coverage:**
- ✅ Paragraphs (37 examples)
- ✅ Headers (16 examples)
- ✅ Links (5 examples)
- ✅ Formatted text (bold, italic)
- ✅ Lists (8 examples, 34 list items)
- ✅ Images (1 example)
- ✅ Code blocks (2 examples)
- ✅ Bookmark cards (6 examples)
- ✅ Signup cards (1 example)
- ✅ Toggle/accordion (1 example)
- ✅ Line breaks (1 example)
