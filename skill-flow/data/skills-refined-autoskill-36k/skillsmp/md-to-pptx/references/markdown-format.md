# Markdown Format Reference

The parser uses standard Markdown with intelligent slide detection.

## Example Structure

```markdown
# Presentation Title
Subtitle text here

## Slide Title
Content for this slide.

- Bullet point 1
- Bullet point 2

## Another Slide

1. Numbered item
2. Another item

### Sub-heading (stays on same slide)

More content...
```

## Slide Detection Rules

- `# H1` - Creates title slide
- `## H2` - Creates new content slide
- `### H3` and below - Stays on current slide as sub-heading
- Content between headings goes on the same slide

## Supported Elements

| Element | Support | Notes |
|---------|---------|-------|
| Headings | Full | H1/H2 create slides, H3+ are content |
| Paragraphs | Full | Auto-wrapped text |
| Bullet lists | Full | Nested supported |
| Numbered lists | Full | Nested supported |
| Code blocks | Basic | Monospace font, background color |
| Tables | Full | Converts to native PPT tables |
| Images | Local only | `![alt](path/to/image.png)` |
| Charts | Auto | Tables with numeric data can become charts |

## Image Handling

Only local file paths are supported:
```markdown
![Description](./images/diagram.png)
![](../assets/photo.jpg)
```

Network URLs and base64 images are skipped with a warning.

## Layout Selection

The generator automatically selects layouts based on content:

| Content Type | Layout |
|--------------|--------|
| H1 only | Title slide (centered) |
| Text + bullets | Content slide |
| Many elements (>4) | Two-column |
| Image present | Image-focused |
| Table with numbers | Chart slide |
