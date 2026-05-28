---
name: html-dev
description: |
  HTML structure, semantics, accessibility, and SEO best practices.
  WHEN: Writing semantic HTML, implementing ARIA accessibility, creating forms/tables, adding SEO meta tags, structuring HTML documents, template sections in Vue/React.
  WHEN NOT: CSS styling (use tailwind-css-dev), JavaScript logic (use js-dev), Vue-specific patterns (use vuejs-dev).
---

# HTML Development

Semantic HTML, accessibility, and structure best practices.

## Document Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Page description for SEO">
  <title>Page Title</title>
</head>
<body>
  <header><!-- Site header, nav --></header>
  <main><!-- Primary content --></main>
  <footer><!-- Site footer --></footer>
</body>
</html>
```

## Semantic Elements

### Page Structure

```html
<header>    <!-- Introductory content, nav -->
<nav>       <!-- Navigation links -->
<main>      <!-- Main content (one per page) -->
<article>   <!-- Self-contained content -->
<section>   <!-- Thematic grouping -->
<aside>     <!-- Sidebar, related content -->
<footer>    <!-- Footer content -->
```

### Content Elements

```html
<h1> to <h6>   <!-- Headings (one h1 per page) -->
<p>            <!-- Paragraph -->
<blockquote>   <!-- Quoted content -->
<figure>       <!-- Image with caption -->
<figcaption>   <!-- Caption for figure -->
<address>      <!-- Contact information -->
<time>         <!-- Date/time -->
<mark>         <!-- Highlighted text -->
<code>         <!-- Code snippet -->
<pre>          <!-- Preformatted text -->
```

### Example: Article

```html
<article>
  <header>
    <h2>Article Title</h2>
    <p>By <address class="inline">Author Name</address></p>
    <time datetime="2024-01-15">January 15, 2024</time>
  </header>
  
  <section>
    <h3>Section Heading</h3>
    <p>Content...</p>
  </section>
  
  <footer>
    <p>Tags: <a href="#">tag1</a>, <a href="#">tag2</a></p>
  </footer>
</article>
```

## Forms

### Basic Structure

```html
<form action="/submit" method="POST">
  <fieldset>
    <legend>Personal Information</legend>
    
    <div>
      <label for="name">Name</label>
      <input type="text" id="name" name="name" required>
    </div>
    
    <div>
      <label for="email">Email</label>
      <input type="email" id="email" name="email" required>
    </div>
  </fieldset>
  
  <button type="submit">Submit</button>
</form>
```

### Input Types

```html
<input type="text">       <!-- Single line text -->
<input type="email">      <!-- Email validation -->
<input type="password">   <!-- Hidden text -->
<input type="number">     <!-- Numeric input -->
<input type="tel">        <!-- Phone number -->
<input type="url">        <!-- URL validation -->
<input type="date">       <!-- Date picker -->
<input type="time">       <!-- Time picker -->
<input type="datetime-local">
<input type="search">     <!-- Search field -->
<input type="file">       <!-- File upload -->
<input type="checkbox">   <!-- Checkbox -->
<input type="radio">      <!-- Radio button -->
<input type="range">      <!-- Slider -->
<input type="color">      <!-- Color picker -->
<input type="hidden">     <!-- Hidden field -->
```

### Input Attributes

```html
<input 
  required              <!-- Must be filled -->
  disabled              <!-- Cannot interact -->
  readonly              <!-- Cannot edit -->
  placeholder="Hint"    <!-- Placeholder text -->
  value="Default"       <!-- Default value -->
  minlength="3"         <!-- Minimum length -->
  maxlength="100"       <!-- Maximum length -->
  min="0"               <!-- Minimum number -->
  max="100"             <!-- Maximum number -->
  step="5"              <!-- Number increment -->
  pattern="[A-Za-z]+"   <!-- Regex pattern -->
  autocomplete="email"  <!-- Autofill hint -->
>
```

### Select & Textarea

```html
<select id="country" name="country">
  <option value="">Select a country</option>
  <optgroup label="North America">
    <option value="us">United States</option>
    <option value="ca">Canada</option>
  </optgroup>
</select>

<textarea id="message" name="message" rows="4" cols="50"
          placeholder="Enter message..."></textarea>
```

## Tables

```html
<table>
  <caption>Monthly Sales</caption>
  <thead>
    <tr>
      <th scope="col">Month</th>
      <th scope="col">Sales</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">January</th>
      <td>$10,000</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <th scope="row">Total</th>
      <td>$120,000</td>
    </tr>
  </tfoot>
</table>
```

## Accessibility (A11y)

### ARIA Attributes

```html
<!-- Roles -->
<div role="alert">Error message</div>
<nav role="navigation">...</nav>
<div role="dialog" aria-modal="true">...</div>

<!-- States -->
<button aria-pressed="true">Toggle</button>
<input aria-invalid="true">
<div aria-expanded="false">...</div>
<button aria-disabled="true">...</button>

<!-- Properties -->
<input aria-label="Search">
<input aria-labelledby="label-id">
<input aria-describedby="hint-id">
<div aria-live="polite">Dynamic content</div>
<button aria-haspopup="menu">Menu</button>
```

### Accessible Patterns

```html
<!-- Skip link -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<!-- Image -->
<img src="photo.jpg" alt="Description of image">
<img src="decorative.png" alt="" role="presentation">

<!-- Icon button -->
<button aria-label="Close">
  <svg aria-hidden="true">...</svg>
</button>

<!-- Loading state -->
<button aria-busy="true" aria-live="polite">
  Loading...
</button>

<!-- Required field -->
<label for="email">
  Email <span aria-hidden="true">*</span>
</label>
<input id="email" required aria-required="true">

<!-- Error message -->
<input id="email" aria-invalid="true" aria-describedby="email-error">
<p id="email-error" role="alert">Please enter a valid email</p>
```

### Keyboard Navigation

```html
<!-- Focusable elements (natural tab order) -->
<a href="#">Link</a>
<button>Button</button>
<input>
<select>
<textarea>

<!-- Custom focusable -->
<div tabindex="0">Focusable div</div>
<div tabindex="-1">Programmatically focusable only</div>

<!-- Skip navigation -->
<a href="#main" class="sr-only focus:not-sr-only">
  Skip to main content
</a>
```

## Lists

```html
<!-- Unordered -->
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
</ul>

<!-- Ordered -->
<ol>
  <li>First</li>
  <li>Second</li>
</ol>

<!-- Description list -->
<dl>
  <dt>Term</dt>
  <dd>Definition</dd>
</dl>
```

## Links & Buttons

```html
<!-- Links: navigation -->
<a href="/page">Go to page</a>
<a href="#section">Jump to section</a>
<a href="mailto:email@example.com">Email us</a>
<a href="tel:+1234567890">Call us</a>
<a href="/file.pdf" download>Download PDF</a>
<a href="https://external.com" target="_blank" rel="noopener noreferrer">
  External link
</a>

<!-- Buttons: actions -->
<button type="button">Action</button>
<button type="submit">Submit form</button>
<button type="reset">Reset form</button>
```

## Media

```html
<!-- Responsive image -->
<img 
  src="image.jpg" 
  srcset="image-400.jpg 400w, image-800.jpg 800w"
  sizes="(max-width: 600px) 400px, 800px"
  alt="Description"
  loading="lazy"
>

<!-- Picture (art direction) -->
<picture>
  <source media="(min-width: 800px)" srcset="large.jpg">
  <source media="(min-width: 400px)" srcset="medium.jpg">
  <img src="small.jpg" alt="Description">
</picture>

<!-- Video -->
<video controls poster="thumbnail.jpg">
  <source src="video.mp4" type="video/mp4">
  <source src="video.webm" type="video/webm">
  <track kind="captions" src="captions.vtt" srclang="en" label="English">
  Your browser doesn't support video.
</video>
```

## Meta Tags

```html
<head>
  <!-- Essential -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title - Site Name</title>
  <meta name="description" content="155 character description">
  
  <!-- Open Graph (social sharing) -->
  <meta property="og:title" content="Title">
  <meta property="og:description" content="Description">
  <meta property="og:image" content="https://example.com/image.jpg">
  <meta property="og:url" content="https://example.com/page">
  <meta property="og:type" content="website">
  
  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Title">
  
  <!-- Favicon -->
  <link rel="icon" href="/favicon.ico">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
</head>
```

## Anti-Patterns to Avoid

1. **Div soup** → Use semantic elements (nav, main, article, section)
2. **Missing alt text** → Always provide alt for meaningful images
3. **Click handlers on divs** → Use button or a elements
4. **Skipping heading levels** → h1 → h2 → h3 (no skipping)
5. **Label without for** → Always link label to input with for/id
6. **Placeholder as label** → Use visible label elements
7. **target="_blank" without rel** → Add rel="noopener noreferrer"
