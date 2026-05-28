# EDS Blocks Reference for Presentations

This document provides comprehensive examples of all EDS blocks available for creating presentation-mode notebooks. Each block includes the HTML structure and initialization script pattern.

## Visual Layout Blocks

### Accordion Block

**Best For:** FAQs, collapsible sections, feature lists, detailed explanations

**HTML Structure:**
```html
<div class="accordion block">
  <div>
    <div>Question or Title 1</div>
    <div>Answer or detailed content here...</div>
  </div>
  <div>
    <div>Question or Title 2</div>
    <div>More detailed content...</div>
  </div>
  <div>
    <div>Question or Title 3</div>
    <div>Even more content...</div>
  </div>
</div>
```

**Initialization Script:**
```html
<script type="module">
  const block = document.querySelector('.accordion.block');
  const module = await import('/blocks/accordion/accordion.js');
  await module.default(block);
</script>
```

**Complete Example:**
```markdown
## ❓ Frequently Asked Questions

<div class="accordion block">
  <div>
    <div>How does this work?</div>
    <div>This presentation uses embedded EDS blocks in markdown cells. Each block is initialized with inline JavaScript that runs when the cell is displayed.</div>
  </div>
  <div>
    <div>Can users run code?</div>
    <div>No, this is presentation-only. All code is converted to informative text and displayed as markdown.</div>
  </div>
  <div>
    <div>What blocks are available?</div>
    <div>You can use accordion, cards, tabs, hero, grid, table, quote, columns, modal, video, counter, code-expander, and floating-alert blocks.</div>
  </div>
</div>

<script type="module">
  const block = document.querySelector('.accordion.block');
  const module = await import('/blocks/accordion/accordion.js');
  await module.default(block);
</script>
```

---

### Cards Block

**Best For:** Features showcase, team members, product listings, services overview

**HTML Structure:**
```html
<div class="cards block">
  <div>
    <div><strong>Card Title</strong></div>
    <div>Card content with description and details...</div>
  </div>
  <div>
    <div><strong>Another Card</strong></div>
    <div>More content here...</div>
  </div>
  <div>
    <div><strong>Third Card</strong></div>
    <div>Additional content...</div>
  </div>
</div>
```

**Initialization Script:**
```html
<script type="module">
  const block = document.querySelector('.cards.block');
  const module = await import('/blocks/cards/cards.js');
  await module.default(block);
</script>
```

**Complete Example:**
```markdown
## 🚀 Key Features

<div class="cards block">
  <div>
    <div><strong>📊 Data Visualization</strong></div>
    <div>Create stunning charts and graphs with our built-in visualization library. Support for line, bar, pie, and custom chart types.</div>
  </div>
  <div>
    <div><strong>⚡ Lightning Fast</strong></div>
    <div>Optimized for performance with lazy loading, code splitting, and efficient rendering. Delivers instant load times.</div>
  </div>
  <div>
    <div><strong>🎨 Beautiful Design</strong></div>
    <div>Modern, responsive design system with accessible components. Looks great on all devices and screen sizes.</div>
  </div>
  <div>
    <div><strong>🔒 Secure by Default</strong></div>
    <div>Built-in security features including XSS protection, CSRF tokens, and encrypted data storage.</div>
  </div>
</div>

<script type="module">
  const block = document.querySelector('.cards.block');
  const module = await import('/blocks/cards/cards.js');
  await module.default(block);
</script>
```

---

### Tabs Block

**Best For:** Organizing related content, code examples, comparisons, multi-view content

**HTML Structure:**
```html
<div class="tabs block">
  <div>
    <div>Tab 1 Label</div>
    <div>Content for tab 1...</div>
  </div>
  <div>
    <div>Tab 2 Label</div>
    <div>Content for tab 2...</div>
  </div>
  <div>
    <div>Tab 3 Label</div>
    <div>Content for tab 3...</div>
  </div>
</div>
```

**Initialization Script:**
```html
<script type="module">
  const block = document.querySelector('.tabs.block');
  const module = await import('/blocks/tabs/tabs.js');
  await module.default(block);
</script>
```

**Complete Example:**
```markdown
## 💻 Code Examples

<div class="tabs block">
  <div>
    <div>JavaScript</div>
    <div>
      <pre><code>
const fetchData = async () => {
  const response = await fetch('/api/data');
  return response.json();
};
      </code></pre>
    </div>
  </div>
  <div>
    <div>Python</div>
    <div>
      <pre><code>
async def fetch_data():
    response = await fetch('/api/data')
    return response.json()
      </code></pre>
    </div>
  </div>
  <div>
    <div>cURL</div>
    <div>
      <pre><code>
curl -X GET https://api.example.com/data \
  -H "Content-Type: application/json"
      </code></pre>
    </div>
  </div>
</div>

<script type="module">
  const block = document.querySelector('.tabs.block');
  const module = await import('/blocks/tabs/tabs.js');
  await module.default(block);
</script>
```

---

### Hero Block

**Best For:** Title sections, landing sections, call-to-action areas

**HTML Structure:**
```html
<div class="hero block">
  <div>
    <div>
      <h1>Hero Title</h1>
      <p>Subtitle or tagline goes here</p>
    </div>
  </div>
</div>
```

**Initialization Script:**
```html
<script type="module">
  const block = document.querySelector('.hero.block');
  const module = await import('/blocks/hero/hero.js');
  await module.default(block);
</script>
```

**Complete Example:**
```markdown
<div class="hero block">
  <div>
    <div>
      <h1>🎯 Product Presentation 2025</h1>
      <p>Discover the future of web development with our innovative platform</p>
    </div>
  </div>
</div>

<script type="module">
  const block = document.querySelector('.hero.block');
  const module = await import('/blocks/hero/hero.js');
  await module.default(block);
</script>
```

---

### Grid Block

**Best For:** Flexible multi-column layouts, image galleries, feature grids

**HTML Structure:**
```html
<div class="grid block">
  <div>
    <div>Grid Item 1</div>
    <div>Content...</div>
  </div>
  <div>
    <div>Grid Item 2</div>
    <div>Content...</div>
  </div>
  <div>
    <div>Grid Item 3</div>
    <div>Content...</div>
  </div>
  <div>
    <div>Grid Item 4</div>
    <div>Content...</div>
  </div>
</div>
```

**Initialization Script:**
```html
<script type="module">
  const block = document.querySelector('.grid.block');
  const module = await import('/blocks/grid/grid.js');
  await module.default(block);
</script>
```

---

### Table Block

**Best For:** Data presentation, pricing tables, comparison charts, specifications

**HTML Structure:**
```html
<div class="table block">
  <div>
    <div>Header 1</div>
    <div>Header 2</div>
    <div>Header 3</div>
  </div>
  <div>
    <div>Row 1 Cell 1</div>
    <div>Row 1 Cell 2</div>
    <div>Row 1 Cell 3</div>
  </div>
  <div>
    <div>Row 2 Cell 1</div>
    <div>Row 2 Cell 2</div>
    <div>Row 2 Cell 3</div>
  </div>
</div>
```

**Initialization Script:**
```html
<script type="module">
  const block = document.querySelector('.table.block');
  const module = await import('/blocks/table/table.js');
  await module.default(block);
</script>
```

**Complete Example:**
```markdown
## 💰 Pricing Plans

<div class="table block">
  <div>
    <div><strong>Plan</strong></div>
    <div><strong>Price</strong></div>
    <div><strong>Features</strong></div>
  </div>
  <div>
    <div>Basic</div>
    <div>$10/month</div>
    <div>Core features, 5 users, Email support</div>
  </div>
  <div>
    <div>Pro</div>
    <div>$29/month</div>
    <div>All features, 25 users, Priority support</div>
  </div>
  <div>
    <div>Enterprise</div>
    <div>Custom</div>
    <div>Unlimited users, Dedicated support, Custom integrations</div>
  </div>
</div>

<script type="module">
  const block = document.querySelector('.table.block');
  const module = await import('/blocks/table/table.js');
  await module.default(block);
</script>
```

---

## Content Blocks

### Quote Block

**Best For:** Pull quotes, testimonials, highlighting key information

**HTML Structure:**
```html
<div class="quote block">
  <div>
    <div>
      <p>Quote text goes here...</p>
      <p>— Author Name, Title</p>
    </div>
  </div>
</div>
```

**Initialization Script:**
```html
<script type="module">
  const block = document.querySelector('.quote.block');
  const module = await import('/blocks/quote/quote.js');
  await module.default(block);
</script>
```

**Complete Example:**
```markdown
<div class="quote block">
  <div>
    <div>
      <p>"This platform has completely transformed how we build and deploy web applications. The speed and efficiency gains are remarkable."</p>
      <p>— Jane Smith, CTO of TechCorp</p>
    </div>
  </div>
</div>

<script type="module">
  const block = document.querySelector('.quote.block');
  const module = await import('/blocks/quote/quote.js');
  await module.default(block);
</script>
```

---

### Columns Block

**Best For:** Multi-column text layouts, side-by-side content

**HTML Structure:**
```html
<div class="columns block">
  <div>
    <div>Column 1 content...</div>
    <div>Column 2 content...</div>
    <div>Column 3 content...</div>
  </div>
</div>
```

**Initialization Script:**
```html
<script type="module">
  const block = document.querySelector('.columns.block');
  const module = await import('/blocks/columns/columns.js');
  await module.default(block);
</script>
```

---

### Modal Block

**Best For:** Dialog overlays, detailed information popups, image lightboxes

**HTML Structure:**
```html
<div class="modal block">
  <div>
    <div>
      <h2>Modal Title</h2>
      <p>Modal content goes here...</p>
    </div>
  </div>
</div>
```

**Initialization Script:**
```html
<script type="module">
  const block = document.querySelector('.modal.block');
  const module = await import('/blocks/modal/modal.js');
  await module.default(block);
</script>
```

---

### Video Block

**Best For:** Embedded videos, YouTube/Vimeo content

**HTML Structure:**
```html
<div class="video block">
  <div>
    <div>
      <a href="https://www.youtube.com/watch?v=VIDEO_ID">Video Title</a>
    </div>
  </div>
</div>
```

**Initialization Script:**
```html
<script type="module">
  const block = document.querySelector('.video.block');
  const module = await import('/blocks/video/video.js');
  await module.default(block);
</script>
```

---

## Interactive Blocks

### Code Expander Block

**Best For:** Collapsible code snippets, expandable examples

**HTML Structure:**
```html
<div class="code-expander block">
  <div>
    <div>Code Title</div>
    <div>
      <pre><code>
// Your code here
const example = 'value';
      </code></pre>
    </div>
  </div>
</div>
```

**Initialization Script:**
```html
<script type="module">
  const block = document.querySelector('.code-expander.block');
  const module = await import('/blocks/code-expander/code-expander.js');
  await module.default(block);
</script>
```

---

### Counter Block

**Best For:** Animated statistics, metric displays, achievement showcases

**HTML Structure:**
```html
<div class="counter block">
  <div>
    <div>1000</div>
    <div>Users</div>
  </div>
  <div>
    <div>500</div>
    <div>Projects</div>
  </div>
  <div>
    <div>99.9</div>
    <div>Uptime %</div>
  </div>
</div>
```

**Initialization Script:**
```html
<script type="module">
  const block = document.querySelector('.counter.block');
  const module = await import('/blocks/counter/counter.js');
  await module.default(block);
</script>
```

**Complete Example:**
```markdown
## 📊 Our Impact

<div class="counter block">
  <div>
    <div>10000</div>
    <div>Active Users</div>
  </div>
  <div>
    <div>5000</div>
    <div>Projects Deployed</div>
  </div>
  <div>
    <div>99.9</div>
    <div>Uptime Percentage</div>
  </div>
  <div>
    <div>50</div>
    <div>Countries Served</div>
  </div>
</div>

<script type="module">
  const block = document.querySelector('.counter.block');
  const module = await import('/blocks/counter/counter.js');
  await module.default(block);
</script>
```

---

### Floating Alert Block

**Best For:** Dismissible notifications, important messages, announcements

**HTML Structure:**
```html
<div class="floating-alert block">
  <div>
    <div>Alert message goes here...</div>
  </div>
</div>
```

**Initialization Script:**
```html
<script type="module">
  const block = document.querySelector('.floating-alert.block');
  const module = await import('/blocks/floating-alert/floating-alert.js');
  await module.default(block);
</script>
```

---

## Universal Pattern

All EDS blocks follow the same initialization pattern:

1. **HTML structure** wrapped in `<div class="block-name block">`
2. **Inline script** that:
   - Selects the block element
   - Imports the block module
   - Calls the default export (decorate function)

```javascript
<script type="module">
  const block = document.querySelector('.block-name.block');
  const module = await import('/blocks/block-name/block-name.js');
  await module.default(block);
</script>
```

## Tips for Presentations

1. **Combine blocks** for rich layouts (hero + cards, tabs + code-expander)
2. **Use emojis** in headers for visual appeal (🎯, 📊, 🚀, ✨, 💡)
3. **Break content** into digestible chunks (3-5 cards per section)
4. **Add navigation** with table of contents and hash links
5. **Test paged mode** to ensure smooth navigation between sections
6. **Use counters** for impressive statistics and metrics
7. **Embed videos** for demonstrations and tutorials
8. **Use quotes** to highlight testimonials and key messages

## Block Selection Guide

| Use Case | Recommended Block |
|----------|-------------------|
| FAQs or collapsible content | Accordion |
| Feature showcase | Cards |
| Code examples | Tabs + Code Expander |
| Title/landing section | Hero |
| Pricing or data comparison | Table |
| Testimonials | Quote |
| Statistics/metrics | Counter |
| Multi-view content | Tabs |
| Image gallery | Grid |
| Detailed popup info | Modal |
| Important announcements | Floating Alert |
| Video content | Video |

---

**Note:** All blocks automatically load their CSS. No manual stylesheet linking required.
