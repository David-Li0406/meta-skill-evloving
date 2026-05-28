# XHTML Syntax Rules Reference

## Element Case

All element names must be lowercase:

```html
<!-- Correct -->
<div>content</div>
<section>content</section>

<!-- Wrong -->
<DIV>content</DIV>
<Section>content</Section>
```

## Attribute Case

All attribute names must be lowercase:

```html
<!-- Correct -->
<input type="text" name="field" id="field"/>

<!-- Wrong -->
<input TYPE="text" NAME="field" ID="field"/>
```

## Attribute Quoting

All attribute values must use double quotes:

```html
<!-- Correct -->
<div class="container" id="main">

<!-- Wrong -->
<div class=container id='main'>
```

## Boolean Attributes

Use empty value style for boolean attributes:

```html
<!-- Correct -->
<input type="checkbox" checked=""/>
<button disabled="">Click</button>
<details open="">Content</details>

<!-- Wrong -->
<input type="checkbox" checked>
<input type="checkbox" checked="checked">
<input type="checkbox" checked="true">
```

## Tag Closing

Every element must be explicitly closed:

```html
<!-- Correct -->
<p>Paragraph text.</p>
<li>List item</li>

<!-- Wrong (implicit close) -->
<p>Paragraph text.
<li>List item
```

## Void Elements (Self-Closing)

HTML has specific void elements that cannot have content and must self-close:

```html
<!-- Void elements - use self-closing syntax -->
<meta charset="utf-8"/>
<link rel="stylesheet" href="styles.css"/>
<input type="text" name="field"/>
<img src="image.jpg" alt="Description"/>
<br/>
<hr/>
```

**Complete list of void elements:** area, base, br, col, embed, hr, img, input, link, meta, source, track, wbr

## Custom Elements (Never Self-Closing)

Custom elements and web components are NOT void elements. They must always have explicit opening and closing tags, even when empty:

```html
<!-- Correct - custom elements need closing tags -->
<icon-wc name="home"></icon-wc>
<layout-stack></layout-stack>
<accordion-wc></accordion-wc>
<toast-wc></toast-wc>

<!-- Wrong - custom elements cannot be self-closing -->
<icon-wc name="home"/>
<layout-stack/>
```

This applies to all custom elements including:
- Layout elements: `<layout-stack>`, `<layout-grid>`, `<layout-card>`, etc.
- Web components: `<icon-wc>`, `<tabs-wc>`, `<accordion-wc>`, `<dropdown-wc>`, etc.
- Any element with a hyphen in its name

## Nesting

Elements must be properly nested (close in reverse order):

```html
<!-- Correct -->
<p><strong><em>Text</em></strong></p>

<!-- Wrong -->
<p><strong><em>Text</strong></em></p>
```

## Doctype

Use lowercase doctype:

```html
<!-- Correct -->
<!doctype html>

<!-- Wrong -->
<!DOCTYPE html>
<!DOCTYPE HTML>
```

## Language Attribute

Always include lang attribute on html element:

```html
<!-- Correct -->
<html lang="en">

<!-- Wrong -->
<html>
```

## Character Encoding

Always declare charset in head:

```html
<head>
  <meta charset="utf-8"/>
  <!-- Must be first in head -->
</head>
```

## Special Characters

Escape special characters in content:

| Character | Entity |
|-----------|--------|
| `<` | `&lt;` |
| `>` | `&gt;` |
| `&` | `&amp;` |
| `"` | `&quot;` (in attributes) |

## Comments

HTML comments syntax:

```html
<!-- This is a comment -->

<!--
  Multi-line
  comment
-->
```

## Whitespace

- Use spaces, not tabs (2-space indent recommended)
- No trailing whitespace
- Single newline at end of file
