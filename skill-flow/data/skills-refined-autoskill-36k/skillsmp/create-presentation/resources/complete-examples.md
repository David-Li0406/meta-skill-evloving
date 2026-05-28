# Complete Presentation Notebook Examples

This document provides complete, ready-to-use presentation notebook examples for different use cases.

## Example 1: Product Launch Presentation

**Filename:** `product-launch.ipynb`

**Metadata:**
```json
{
  "metadata": {
    "title": "Product Launch 2025",
    "description": "Introducing our revolutionary new platform",
    "author": "Tom Cranstoun",
    "date": "2025-01-19",
    "category": "presentation",
    "difficulty": "beginner",
    "duration": "15 minutes",
    "repo": "https://github.com/ddttom/allaboutV2"
  }
}
```

### Cell 1: Title (Markdown)

```markdown
# 🚀 Product Launch 2025

**The Future of Web Development**

Welcome to the unveiling of our revolutionary new platform that will transform how you build and deploy web applications.

---

## 📋 Agenda

1. [Introduction](#introduction)
2. [Key Features](#key-features)
3. [How It Works](#how-it-works)
4. [Pricing](#pricing)
5. [Customer Success](#customer-success)
6. [Get Started](#get-started)
```

### Cell 2: Introduction Section (Markdown)

```markdown
## 🎯 Introduction

Our platform combines cutting-edge technology with intuitive design to deliver the best developer experience in the industry.

<div class="hero block">
  <div>
    <div>
      <h2>Built for Developers, By Developers</h2>
      <p>Speed, reliability, and simplicity in one powerful package</p>
    </div>
  </div>
</div>

<script type="module">
  const block = document.querySelector('.hero.block');
  const module = await import('/blocks/hero/hero.js');
  await module.default(block);
</script>

---

### Why Choose Us?

We've listened to thousands of developers and built exactly what you need:
- **Lightning fast** deployment times
- **Zero configuration** to get started
- **Scalable** from prototype to production
- **Developer-friendly** APIs and documentation
```

### Cell 3: Key Features (Markdown)

```markdown
## ✨ Key Features

<div class="cards block">
  <div>
    <div><strong>⚡ Instant Deployment</strong></div>
    <div>Deploy your application in seconds with our optimized build pipeline. No waiting, no complexity, just results.</div>
  </div>
  <div>
    <div><strong>🔒 Enterprise Security</strong></div>
    <div>Built-in security features including encryption, authentication, and compliance certifications.</div>
  </div>
  <div>
    <div><strong>📊 Real-time Analytics</strong></div>
    <div>Monitor performance, track usage, and optimize your application with comprehensive analytics dashboard.</div>
  </div>
  <div>
    <div><strong>🌍 Global CDN</strong></div>
    <div>Content delivered from edge locations worldwide for optimal performance regardless of user location.</div>
  </div>
  <div>
    <div><strong>🔄 Auto Scaling</strong></div>
    <div>Automatically scale resources based on traffic patterns. Pay only for what you use.</div>
  </div>
  <div>
    <div><strong>🛠️ Developer Tools</strong></div>
    <div>CLI, SDKs, plugins, and integrations for your favorite development tools and workflows.</div>
  </div>
</div>

<script type="module">
  const block = document.querySelector('.cards.block');
  const module = await import('/blocks/cards/cards.js');
  await module.default(block);
</script>
```

### Cell 4: How It Works (Markdown)

```markdown
## 💻 How It Works

<div class="tabs block">
  <div>
    <div>1. Connect Repository</div>
    <div>
      <h3>Link Your Git Repository</h3>
      <p>Connect your GitHub, GitLab, or Bitbucket repository in just a few clicks.</p>
      <pre><code>git remote add platform https://platform.example.com/yourapp</code></pre>
      <p>Our system automatically detects your framework and build configuration.</p>
    </div>
  </div>
  <div>
    <div>2. Configure</div>
    <div>
      <h3>Zero Configuration Required</h3>
      <p>We automatically detect and configure your build settings. Or customize with a simple config file:</p>
      <pre><code>{
  "framework": "auto-detect",
  "buildCommand": "npm run build",
  "outputDir": "dist"
}</code></pre>
      <p>Environment variables, domains, and settings managed through our intuitive dashboard.</p>
    </div>
  </div>
  <div>
    <div>3. Deploy</div>
    <div>
      <h3>Push to Deploy</h3>
      <p>Every push to your main branch triggers an automatic deployment:</p>
      <pre><code>git push platform main</code></pre>
      <p>Built, tested, and deployed in under 30 seconds. Automatic rollback on failure.</p>
    </div>
  </div>
  <div>
    <div>4. Monitor</div>
    <div>
      <h3>Real-time Insights</h3>
      <p>Track performance, errors, and usage in real-time with our analytics dashboard.</p>
      <ul>
        <li>Core Web Vitals monitoring</li>
        <li>Error tracking and alerting</li>
        <li>Usage metrics and trends</li>
        <li>Custom event tracking</li>
      </ul>
    </div>
  </div>
</div>

<script type="module">
  const block = document.querySelector('.tabs.block');
  const module = await import('/blocks/tabs/tabs.js');
  await module.default(block);
</script>
```

### Cell 5: Pricing (Markdown)

```markdown
## 💰 Pricing Plans

<div class="table block">
  <div>
    <div><strong>Plan</strong></div>
    <div><strong>Price</strong></div>
    <div><strong>Features</strong></div>
    <div><strong>Best For</strong></div>
  </div>
  <div>
    <div>Starter</div>
    <div>Free</div>
    <div>
      • 1 user<br>
      • 3 projects<br>
      • 100GB bandwidth<br>
      • Community support
    </div>
    <div>Hobbyists & Students</div>
  </div>
  <div>
    <div>Pro</div>
    <div>$29/month</div>
    <div>
      • 5 users<br>
      • Unlimited projects<br>
      • 1TB bandwidth<br>
      • Priority support<br>
      • Custom domains<br>
      • Analytics
    </div>
    <div>Small Teams</td>
  </div>
  <div>
    <div>Business</div>
    <div>$99/month</div>
    <div>
      • 25 users<br>
      • Unlimited everything<br>
      • 10TB bandwidth<br>
      • Dedicated support<br>
      • SLA guarantee<br>
      • Advanced security
    </div>
    <div>Growing Companies</div>
  </div>
  <div>
    <div>Enterprise</div>
    <div>Custom</div>
    <div>
      • Unlimited users<br>
      • Custom infrastructure<br>
      • Unlimited bandwidth<br>
      • Account manager<br>
      • Custom integrations<br>
      • On-premise option
    </div>
    <div>Large Organizations</div>
  </div>
</div>

<script type="module">
  const block = document.querySelector('.table.block');
  const module = await import('/blocks/table/table.js');
  await module.default(block);
</script>

---

### 🎁 Special Launch Offer

**50% off Pro and Business plans for the first 6 months!**

Use code `LAUNCH2025` at checkout.
```

### Cell 6: Customer Success (Markdown)

```markdown
## 🌟 Customer Success Stories

<div class="quote block">
  <div>
    <div>
      <p>"This platform reduced our deployment time from hours to minutes. It's been a game-changer for our team's productivity."</p>
      <p>— Sarah Johnson, VP Engineering at TechCorp</p>
    </div>
  </div>
</div>

<script type="module">
  const block = document.querySelector('.quote.block');
  const module = await import('/blocks/quote/quote.js');
  await module.default(block);
</script>

---

## 📊 By The Numbers

<div class="counter block">
  <div>
    <div>50000</div>
    <div>Active Developers</div>
  </div>
  <div>
    <div>100000</div>
    <div>Applications Deployed</div>
  </div>
  <div>
    <div>99.99</div>
    <div>Uptime Percentage</div>
  </div>
  <div>
    <div>150</div>
    <div>Countries Worldwide</div>
  </div>
</div>

<script type="module">
  const block = document.querySelector('.counter.block');
  const module = await import('/blocks/counter/counter.js');
  await module.default(block);
</script>
```

### Cell 7: Get Started (Markdown)

```markdown
## 🚀 Get Started Today

Ready to transform your development workflow?

1. **Sign up** at [platform.example.com](https://platform.example.com)
2. **Connect** your repository
3. **Deploy** your first application
4. **Scale** with confidence

---

## ❓ Frequently Asked Questions

<div class="accordion block">
  <div>
    <div>What frameworks do you support?</div>
    <div>We support all major frameworks including React, Vue, Angular, Next.js, Nuxt, SvelteKit, and static sites. Our auto-detection handles configuration automatically.</div>
  </div>
  <div>
    <div>How long does deployment take?</div>
    <div>Most deployments complete in under 30 seconds. Large applications may take up to 2 minutes depending on build complexity and asset size.</div>
  </div>
  <div>
    <div>Can I use my own domain?</div>
    <div>Yes! Custom domains are available on Pro plans and above. We handle SSL certificates automatically with Let's Encrypt.</div>
  </div>
  <div>
    <div>What about database and backend?</div>
    <div>We offer integrated database options (PostgreSQL, MongoDB) and serverless functions. Or connect to your existing backend infrastructure.</div>
  </div>
  <div>
    <div>Is there a free trial?</div>
    <div>The Starter plan is free forever with no credit card required. Pro and Business plans include a 14-day free trial.</div>
  </div>
  <div>
    <div>How do I get support?</div>
    <div>Community support via Discord and forums. Pro+ plans include email support. Business+ plans get priority support with SLA guarantees.</div>
  </div>
</div>

<script type="module">
  const block = document.querySelector('.accordion.block');
  const module = await import('/blocks/accordion/accordion.js');
  await module.default(block);
</script>

---

## 📧 Contact Us

Questions? Reach out to our team:
- **Email:** sales@platform.example.com
- **Discord:** [Join our community](https://discord.gg/platform)
- **Twitter:** [@platform](https://twitter.com/platform)

Thank you for your interest! We look forward to helping you build amazing applications.
```

---

## Example 2: Technical Tutorial Presentation

**Filename:** `tutorial-presentation.ipynb`

**Use Case:** Teaching a technical concept without executable code

**Metadata:**
```json
{
  "metadata": {
    "title": "Building Modern Web Components",
    "description": "Learn how to create reusable web components with best practices",
    "author": "Tom Cranstoun",
    "date": "2025-01-19",
    "category": "presentation",
    "difficulty": "intermediate",
    "duration": "20 minutes",
    "repo": "https://github.com/ddttom/allaboutV2"
  }
}
```

### Cell 1: Title

```markdown
# 🎓 Building Modern Web Components

**A comprehensive guide to creating reusable, maintainable components**

---

## What You'll Learn

- Component architecture principles
- Vanilla JavaScript patterns
- Best practices and anti-patterns
- Real-world examples
```

### Cell 2: Core Concepts

```markdown
## 🧩 Component Architecture

<div class="tabs block">
  <div>
    <div>Structure</div>
    <div>
      <h3>HTML Structure</h3>
      <p>Every component starts with semantic HTML:</p>
      <pre><code>&lt;div class="component-name block"&gt;
  &lt;div class="component-header"&gt;...&lt;/div&gt;
  &lt;div class="component-body"&gt;...&lt;/div&gt;
  &lt;div class="component-footer"&gt;...&lt;/div&gt;
&lt;/div&gt;</code></pre>
      <p><strong>Key principles:</strong></p>
      <ul>
        <li>Use semantic HTML elements</li>
        <li>BEM naming convention for classes</li>
        <li>Progressive enhancement approach</li>
      </ul>
    </div>
  </div>
  <div>
    <div>Behavior</div>
    <div>
      <h3>JavaScript Decoration</h3>
      <p>Components are enhanced with JavaScript:</p>
      <pre><code>export default function decorate(block) {
  // Extract content
  const content = block.textContent;

  // Transform DOM
  block.innerHTML = '';

  // Add interactivity
  block.addEventListener('click', handleClick);
}</code></pre>
      <p><strong>Best practices:</strong></p>
      <ul>
        <li>Use event delegation</li>
        <li>Clean up event listeners</li>
        <li>Handle errors gracefully</li>
      </ul>
    </div>
  </div>
  <div>
    <div>Styling</div>
    <div>
      <h3>CSS Organization</h3>
      <p>Keep styles modular and maintainable:</p>
      <pre><code>.component-name {
  /* Container styles */
}

.component-name .header {
  /* Header styles */
}

.component-name .body {
  /* Body styles */
}</code></pre>
      <p><strong>Guidelines:</strong></p>
      <ul>
        <li>Use CSS custom properties</li>
        <li>Mobile-first responsive design</li>
        <li>Avoid specificity wars</li>
      </ul>
    </div>
  </div>
</div>

<script type="module">
  const block = document.querySelector('.tabs.block');
  const module = await import('/blocks/tabs/tabs.js');
  await module.default(block);
</script>
```

### Cell 3: Common Patterns

```markdown
## 📚 Common Patterns

<div class="accordion block">
  <div>
    <div>Content Extraction Pattern</div>
    <div>
      <p>Extract structured content from initial HTML:</p>
      <pre><code>// Original HTML: nested divs with content
const rows = [...block.children];
const data = rows.map(row => {
  const cells = [...row.children];
  return {
    title: cells[0].textContent,
    content: cells[1].textContent
  };
});</code></pre>
      <p>This pattern works with EDS's content-first approach where authors create content in documents before developers enhance it.</p>
    </div>
  </div>
  <div>
    <div>Progressive Enhancement</div>
    <div>
      <p>Start with working HTML, enhance with JavaScript:</p>
      <pre><code>// Check if feature is supported
if (!('IntersectionObserver' in window)) {
  // Fallback for older browsers
  return;
}

// Add enhancement
const observer = new IntersectionObserver(callback);
observer.observe(block);</code></pre>
      <p>Components should work without JavaScript, then be enhanced progressively.</p>
    </div>
  </div>
  <div>
    <div>Error Handling</div>
    <div>
      <p>Always handle errors gracefully:</p>
      <pre><code>export default async function decorate(block) {
  try {
    // Component logic here
  } catch (error) {
    console.error('Component error:', error);
    block.classList.add('error-state');
    block.textContent = 'Failed to load component';
  }
}</code></pre>
      <p>Never let a component break the entire page. Isolate failures and provide fallbacks.</p>
    </div>
  </div>
</div>

<script type="module">
  const block = document.querySelector('.accordion.block');
  const module = await import('/blocks/accordion/accordion.js');
  await module.default(block);
</script>
```

### Cell 4: Anti-Patterns

```markdown
## ⚠️ Common Anti-Patterns to Avoid

<div class="cards block">
  <div>
    <div><strong>❌ Reserved Class Names</strong></div>
    <div>Never use <code>-container</code> or <code>-wrapper</code> suffixes. EDS reserves these for framework use. Use <code>-inner</code>, <code>-content</code>, or <code>-panel</code> instead.</div>
  </div>
  <div>
    <div><strong>❌ Direct DOM Manipulation</strong></div>
    <div>Avoid <code>innerHTML +=</code> which loses event listeners. Build elements programmatically or use safe HTML insertion methods.</div>
  </div>
  <div>
    <div><strong>❌ Global State</strong></div>
    <div>Don't store component state in global variables. Use data attributes, closure scope, or WeakMap for component-specific state.</div>
  </div>
  <div>
    <div><strong>❌ Memory Leaks</strong></div>
    <div>Always clean up event listeners, timers, and observers when components are removed. Use <code>AbortController</code> for cleanup.</div>
  </div>
  <div>
    <div><strong>❌ Blocking Operations</strong></div>
    <div>Never perform synchronous blocking operations. Use <code>async/await</code>, <code>requestIdleCallback</code>, or web workers for heavy tasks.</div>
  </div>
  <div>
    <div><strong>❌ Tight Coupling</strong></div>
    <div>Components should be self-contained. Avoid dependencies on specific page structure or other components.</div>
  </div>
</div>

<script type="module">
  const block = document.querySelector('.cards.block');
  const module = await import('/blocks/cards/cards.js');
  await module.default(block);
</script>
```

---

## Key Presentation Patterns

### Pattern 1: Feature Showcase
Use **cards** for features, **tabs** for detailed explanations, **accordion** for FAQs.

### Pattern 2: Tutorial Flow
Use **tabs** for step-by-step content, **code-expander** for optional details, **hero** for section titles.

### Pattern 3: Data Presentation
Use **table** for comparisons, **counter** for statistics, **grid** for structured layouts.

### Pattern 4: Customer-Facing
Use **quote** for testimonials, **video** for demos, **modal** for detailed information.

---

## Tips for Converting Interactive Notebooks

When converting an educational notebook to presentation mode:

1. **Identify code cells** - These need conversion
2. **Extract the purpose** - What does the code demonstrate?
3. **Show the code** - Display in fenced code block for reference
4. **Explain the result** - What would this code do?
5. **Embed equivalent** - Use blocks to show the same concept visually

**Example conversion:**

Original code cell:
```javascript
const { testBlock } = await import('/scripts/ipynb-helpers.js');
const block = await testBlock('accordion', accordionContent);
return block.outerHTML;
```

Becomes markdown cell:
```markdown
### Testing the Accordion Block

**Purpose:** This code tests the accordion block with sample content.

**Original code** (for reference):
\`\`\`javascript
const { testBlock } = await import('/scripts/ipynb-helpers.js');
const block = await testBlock('accordion', accordionContent);
return block.outerHTML;
\`\`\`

**Result:** The accordion block is decorated and displays collapsible sections.

**Live demonstration:**

<div class="accordion block">
  <!-- actual accordion content here -->
</div>

<script type="module">
  const block = document.querySelector('.accordion.block');
  const module = await import('/blocks/accordion/accordion.js');
  await module.default(block);
</script>
```

---

**Remember:** Presentation notebooks should tell a story, not execute code. Focus on clarity, visual appeal, and conveying concepts effectively.
