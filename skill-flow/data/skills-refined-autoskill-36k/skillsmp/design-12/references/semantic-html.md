# Semantic HTML Reference

## Why Semantic HTML?

1. **Accessibility** — Screen readers understand content structure
2. **SEO** — Search engines can parse content meaning
3. **Maintainability** — Code is self-documenting
4. **Performance** — Browsers optimize for standard elements

---

## Document Structure

### Page Layout Elements

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title</title>
</head>
<body>
  <header>
    <!-- Site header: logo, main nav -->
  </header>

  <nav aria-label="Main navigation">
    <!-- Primary navigation -->
  </nav>

  <main>
    <!-- Primary content -->
    <article>
      <!-- Self-contained content -->
    </article>

    <aside>
      <!-- Related but separate content -->
    </aside>
  </main>

  <footer>
    <!-- Site footer: copyright, links -->
  </footer>
</body>
</html>
```

---

## Content Elements

### Headings

Follow hierarchy strictly. Never skip levels.

```html
<h1>Main Page Title</h1>
  <h2>Section Title</h2>
    <h3>Subsection Title</h3>
      <h4>Minor Heading</h4>
  <h2>Another Section</h2>
```

**Rules:**
- One `<h1>` per page
- Don't use headings for styling (use CSS)
- Don't skip levels (h1 → h3)

### Paragraphs and Text

```html
<p>Regular paragraph text.</p>

<strong>Important text (semantically important)</strong>
<em>Emphasized text (semantically emphasized)</em>

<mark>Highlighted text</mark>
<small>Fine print or legal text</small>

<time datetime="2024-01-15">January 15, 2024</time>
<abbr title="HyperText Markup Language">HTML</abbr>
```

### Lists

```html
<!-- Unordered list (bullets) -->
<ul>
  <li>Item one</li>
  <li>Item two</li>
</ul>

<!-- Ordered list (numbers) -->
<ol>
  <li>First step</li>
  <li>Second step</li>
</ol>

<!-- Description list (key-value pairs) -->
<dl>
  <dt>Term</dt>
  <dd>Definition</dd>

  <dt>Another Term</dt>
  <dd>Another definition</dd>
</dl>
```

---

## Interactive Elements

### Buttons vs Links

**Use `<button>` for actions:**
```html
<button type="button" onclick="submitForm()">Submit</button>
<button type="button" onclick="openModal()">Open Settings</button>
<button type="submit">Save Changes</button>
```

**Use `<a>` for navigation:**
```html
<a href="/about">About Us</a>
<a href="#section-id">Jump to Section</a>
<a href="mailto:email@example.com">Contact Us</a>
```

**Common Mistakes:**
```html
<!-- ❌ Wrong: Link styled as button but navigates -->
<button onclick="location.href='/about'">About</button>

<!-- ✅ Correct: Use link, style with CSS -->
<a href="/about" class="button">About</a>

<!-- ❌ Wrong: Div with click handler -->
<div onclick="submit()">Submit</div>

<!-- ✅ Correct: Proper button -->
<button type="button" onclick="submit()">Submit</button>
```

---

## Forms

### Complete Form Example

```html
<form action="/submit" method="POST">
  <fieldset>
    <legend>Personal Information</legend>

    <div class="form-group">
      <label for="name">Full Name</label>
      <input
        type="text"
        id="name"
        name="name"
        required
        aria-describedby="name-hint"
      >
      <small id="name-hint">Enter your legal name</small>
    </div>

    <div class="form-group">
      <label for="email">Email Address</label>
      <input
        type="email"
        id="email"
        name="email"
        required
        aria-describedby="email-error"
      >
      <span id="email-error" class="error" role="alert" hidden>
        Please enter a valid email address
      </span>
    </div>

    <div class="form-group">
      <label for="country">Country</label>
      <select id="country" name="country" required>
        <option value="">Select a country</option>
        <option value="us">United States</option>
        <option value="uk">United Kingdom</option>
      </select>
    </div>

    <div class="form-group">
      <label for="message">Message</label>
      <textarea
        id="message"
        name="message"
        rows="4"
        aria-describedby="message-hint"
      ></textarea>
      <small id="message-hint">Maximum 500 characters</small>
    </div>
  </fieldset>

  <fieldset>
    <legend>Preferences</legend>

    <div class="checkbox-group">
      <input type="checkbox" id="newsletter" name="newsletter">
      <label for="newsletter">Subscribe to newsletter</label>
    </div>

    <div class="radio-group">
      <span id="contact-label">Preferred contact method:</span>
      <div role="radiogroup" aria-labelledby="contact-label">
        <input type="radio" id="contact-email" name="contact" value="email">
        <label for="contact-email">Email</label>

        <input type="radio" id="contact-phone" name="contact" value="phone">
        <label for="contact-phone">Phone</label>
      </div>
    </div>
  </fieldset>

  <button type="submit">Submit Form</button>
</form>
```

### Form Rules

1. Every input MUST have a `<label>`
2. Use `for` attribute to connect label to input
3. Group related inputs with `<fieldset>` and `<legend>`
4. Link hints/errors with `aria-describedby`
5. Use appropriate input types (`email`, `tel`, `number`, etc.)

---

## Tables

### When to Use Tables

Tables are for **tabular data only**, not layout.

```html
<table>
  <caption>Quarterly Sales Report</caption>

  <thead>
    <tr>
      <th scope="col">Product</th>
      <th scope="col">Q1</th>
      <th scope="col">Q2</th>
      <th scope="col">Q3</th>
      <th scope="col">Q4</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <th scope="row">Widget A</th>
      <td>$1,000</td>
      <td>$1,200</td>
      <td>$1,100</td>
      <td>$1,400</td>
    </tr>
    <tr>
      <th scope="row">Widget B</th>
      <td>$800</td>
      <td>$900</td>
      <td>$950</td>
      <td>$1,000</td>
    </tr>
  </tbody>

  <tfoot>
    <tr>
      <th scope="row">Total</th>
      <td>$1,800</td>
      <td>$2,100</td>
      <td>$2,050</td>
      <td>$2,400</td>
    </tr>
  </tfoot>
</table>
```

---

## Images

### Standard Image

```html
<img
  src="product.jpg"
  alt="Red leather wallet with three card slots"
  width="300"
  height="200"
  loading="lazy"
>
```

### Image with Caption

```html
<figure>
  <img src="chart.png" alt="Bar chart showing sales growth from 2020 to 2024">
  <figcaption>Figure 1: Annual sales growth</figcaption>
</figure>
```

### Alt Text Guidelines

| Image Type | Alt Text |
|------------|----------|
| Informative | Describe content and function |
| Decorative | Use `alt=""` (empty) |
| Functional (button/link) | Describe the action |
| Complex (charts) | Summarize + provide detailed description elsewhere |

---

## ARIA (When Needed)

Use ARIA only when native HTML isn't sufficient:

```html
<!-- Custom disclosure widget -->
<button aria-expanded="false" aria-controls="panel-1">
  Show Details
</button>
<div id="panel-1" hidden>
  Details content here
</div>

<!-- Live region for dynamic updates -->
<div aria-live="polite" aria-atomic="true">
  Item added to cart
</div>

<!-- Custom tab interface -->
<div role="tablist">
  <button role="tab" aria-selected="true" aria-controls="tab-1">Tab 1</button>
  <button role="tab" aria-selected="false" aria-controls="tab-2">Tab 2</button>
</div>
<div role="tabpanel" id="tab-1">Content 1</div>
<div role="tabpanel" id="tab-2" hidden>Content 2</div>
```

**Rule:** Use native HTML elements first. ARIA is a last resort.
