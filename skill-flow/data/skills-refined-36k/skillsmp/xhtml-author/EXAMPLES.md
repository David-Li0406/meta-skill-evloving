# XHTML Code Examples

## Basic Page

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Page Title</title>
</head>
<body>
  <h1>Hello World</h1>
  <p>Welcome to this page.</p>
</body>
</html>
```

## Full Page Structure

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <meta name="description" content="Page description"/>
  <title>Complete Page Example</title>
</head>
<body>
  <header>
    <nav aria-label="Main navigation">
      <ul>
        <li><a href="#main">Skip to content</a></li>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
        <li><a href="/contact">Contact</a></li>
      </ul>
    </nav>
    <h1>Site Name</h1>
  </header>

  <main id="main">
    <article>
      <h2>Article Title</h2>
      <p>Article introduction paragraph.</p>

      <section>
        <h3>First Section</h3>
        <p>Section content goes here.</p>
      </section>

      <section>
        <h3>Second Section</h3>
        <p>More content here.</p>
      </section>
    </article>

    <aside aria-label="Related content">
      <h2>Related Links</h2>
      <ul>
        <li><a href="/related-1">Related Article 1</a></li>
        <li><a href="/related-2">Related Article 2</a></li>
      </ul>
    </aside>
  </main>

  <footer>
    <p>Copyright 2024 Company Name</p>
  </footer>
</body>
</html>
```

## Contact Form

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>Contact Us</title>
</head>
<body>
  <main>
    <h1>Contact Us</h1>

    <form action="/submit" method="post">
      <fieldset>
        <legend>Your Information</legend>

        <label for="name">Full Name</label>
        <input type="text" id="name" name="name" required=""/>

        <label for="email">Email Address</label>
        <input type="email" id="email" name="email" required=""/>

        <label for="phone">Phone (optional)</label>
        <input type="tel" id="phone" name="phone"/>
      </fieldset>

      <fieldset>
        <legend>Your Message</legend>

        <label for="subject">Subject</label>
        <select id="subject" name="subject">
          <option value="">Select a topic</option>
          <option value="general">General Inquiry</option>
          <option value="support">Support</option>
          <option value="sales">Sales</option>
        </select>

        <label for="message">Message</label>
        <textarea id="message" name="message" rows="5" required=""></textarea>
      </fieldset>

      <button type="submit">Send Message</button>
    </form>
  </main>
</body>
</html>
```

## Data Table

```html
<table>
  <caption>Monthly Sales Data</caption>
  <thead>
    <tr>
      <th scope="col">Month</th>
      <th scope="col">Revenue</th>
      <th scope="col">Growth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">January</th>
      <td>$10,000</td>
      <td>+5%</td>
    </tr>
    <tr>
      <th scope="row">February</th>
      <td>$12,000</td>
      <td>+20%</td>
    </tr>
    <tr>
      <th scope="row">March</th>
      <td>$11,500</td>
      <td>-4%</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <th scope="row">Total</th>
      <td>$33,500</td>
      <td>+7%</td>
    </tr>
  </tfoot>
</table>
```

## Image with Figure

```html
<figure>
  <img src="diagram.png" alt="System architecture showing three connected components"/>
  <figcaption>Figure 1: System Architecture Overview</figcaption>
</figure>
```

## Navigation with Current Page

```html
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li><a href="/about" aria-current="page">About</a></li>
    <li><a href="/contact">Contact</a></li>
  </ul>
</nav>
```

## Custom Elements

```html
<product-card sku="ABC123" price="29.99">
  <h2>Product Name</h2>
  <p>Product description text.</p>
  <img src="product.jpg" alt="Product photo"/>
</product-card>

<status-badge type="success">Active</status-badge>
<status-badge type="warning">Pending</status-badge>
<status-badge type="error">Failed</status-badge>

<user-avatar src="/avatars/user.jpg" alt="John Doe" size="medium"/>
```
