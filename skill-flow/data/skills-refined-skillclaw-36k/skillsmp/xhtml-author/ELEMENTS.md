# Semantic HTML5 Elements Guide

## Document Structure

### `<header>`
Page or section header. Can contain navigation, logo, search.

```html
<header>
  <nav>...</nav>
  <h1>Site Title</h1>
</header>
```

### `<nav>`
Navigation section. Use aria-label when multiple navs exist.

```html
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>
```

### `<main>`
Primary content. Only ONE per page.

```html
<main id="main">
  <!-- Primary page content -->
</main>
```

### `<article>`
Self-contained content that could be distributed independently.

```html
<article>
  <h2>Article Title</h2>
  <p>Article content...</p>
</article>
```

### `<section>`
Thematic grouping. Should have a heading.

```html
<section>
  <h2>Section Title</h2>
  <p>Section content...</p>
</section>
```

### `<aside>`
Tangentially related content (sidebars, pull quotes).

```html
<aside aria-label="Related articles">
  <h2>Related</h2>
  <ul>...</ul>
</aside>
```

### `<footer>`
Page or section footer.

```html
<footer>
  <p>Copyright 2024</p>
</footer>
```

## Content Elements

### `<figure>` and `<figcaption>`
Self-contained media with caption.

```html
<figure>
  <img src="chart.png" alt="Sales data for Q4"/>
  <figcaption>Figure 1: Q4 Sales Performance</figcaption>
</figure>
```

### `<blockquote>`
Extended quotation.

```html
<blockquote cite="https://source.com">
  <p>Quoted text here.</p>
</blockquote>
```

### `<details>` and `<summary>`
Expandable content.

```html
<details>
  <summary>Click to expand</summary>
  <p>Hidden content revealed on click.</p>
</details>
```

### `<hgroup>`
Group heading with subheading.

```html
<hgroup>
  <h1>Main Title</h1>
  <p>Subtitle or tagline</p>
</hgroup>
```

## Text Semantics

| Element | Purpose | Example |
|---------|---------|---------|
| `<strong>` | Important text | `<strong>Warning:</strong>` |
| `<em>` | Emphasized text | `<em>really</em> important` |
| `<mark>` | Highlighted text | `<mark>highlighted</mark>` |
| `<code>` | Code snippet | `<code>const x = 1</code>` |
| `<kbd>` | Keyboard input | `Press <kbd>Enter</kbd>` |
| `<abbr>` | Abbreviation | `<abbr title="HyperText">HTML</abbr>` |
| `<time>` | Date/time | `<time datetime="2024-01-01">Jan 1</time>` |
| `<address>` | Contact info | `<address>email@example.com</address>` |

## Tables

Use proper table structure:

```html
<table>
  <thead>
    <tr>
      <th scope="col">Name</th>
      <th scope="col">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Item</td>
      <td>100</td>
    </tr>
  </tbody>
</table>
```

## Forms

Use fieldset and legend for groups:

```html
<form>
  <fieldset>
    <legend>Personal Information</legend>

    <label for="name">Name</label>
    <input type="text" id="name" name="name"/>

    <label for="email">Email</label>
    <input type="email" id="email" name="email"/>
  </fieldset>

  <button type="submit">Submit</button>
</form>
```

## Avoid These

| Instead of | Use |
|------------|-----|
| `<div class="header">` | `<header>` |
| `<div class="nav">` | `<nav>` |
| `<div class="main">` | `<main>` |
| `<div class="footer">` | `<footer>` |
| `<div class="sidebar">` | `<aside>` |
| `<div class="article">` | `<article>` |
| `<b>` | `<strong>` |
| `<i>` | `<em>` |
