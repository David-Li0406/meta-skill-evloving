# Educational Notebook Examples

This file contains complete examples of different notebook types with actual code patterns from production notebooks.

## Table of Contents

- [Blog Post Notebook](#blog-post-notebook)
- [Tutorial Notebook](#tutorial-notebook)
- [Concept Explanation Notebook](#concept-explanation-notebook)
- [Reference Guide Notebook](#reference-guide-notebook)
- [Interactive Demo Notebook](#interactive-demo-notebook)

---

## Blog Post Notebook

**Purpose:** Engaging content with demonstrations, optimized for readability and shareability.

**Based on:** `blog.ipynb` - Interactive blog post about ipynb-viewer

### Metadata Example

```json
{
  "metadata": {
    "title": "Interactive Blog Post: Introducing ipynb-viewer for EDS",
    "description": "Learn how ipynb-viewer transforms Jupyter notebooks into interactive blog posts",
    "author": "Your Name",
    "date": "2025-01-17",
    "version": "1.0",
    "category": "blog",
    "difficulty": "beginner",
    "duration": "20 minutes",
    "tags": ["blog", "ipynb-viewer", "EDS", "interactive", "tutorial"],
    "license": "MIT"
  }
}
```

**Why these fields:**
- **category: "blog"** → Blue badge showing content type
- **difficulty: "beginner"** → Orange badge, accessible to all readers
- **duration: "20 minutes"** → Purple badge, helps readers plan their time
- **tags** → Searchable keywords, gray pills for categorization

### Structure Overview (41 cells)

- **Cell 1 (Markdown):** Title, introduction, "what is this?" explanation
- **Cell 2 (Markdown):** Table of Contents with anchor links
- **Cells 3-40:** Progressive parts (Part 1 through Part 8)
- **Cell 41 (Markdown):** Call-to-action, contact information

### Cell Pattern Examples

#### Header Cell
```markdown
# 📓 Interactive Blog Post: Introducing ipynb-viewer for EDS

Welcome to this **interactive blog post**! Unlike traditional articles, you can actually **run the code examples** right here in your browser.

## What is ipynb-viewer?

The **ipynb-viewer** block is a revolutionary tool for Adobe Edge Delivery Services (EDS) that allows you to:

📝 Display Jupyter notebooks directly on your website
▶️ Execute JavaScript code cells interactively in the browser
🎨 Show styled block previews with full CSS/JS support
📚 Create living documentation with runnable examples
🎓 Build interactive tutorials and demos
```

#### Table of Contents
```markdown
## 📋 Table of Contents

[Part 1: What is ipynb-viewer?](#part-1)
[Part 2: Getting Started with ipynb-viewer](#part-2)
[Part 3: Testing EDS Blocks](#part-3)
[Part 4: Visual Overlay Previews ★](#part-4)
[Part 5: Cell Independence](#part-5)
[Part 6: Enhanced Markdown Rendering](#part-6)
[Part 7: Advanced Patterns](#part-7)
[Part 8: Best Practices & Next Steps](#part-8)
```

#### Part Introduction
```markdown
## 🚀 Part 2: Getting Started with ipynb-viewer

### Adding the Block to Your EDS Page

To display a Jupyter notebook on your EDS website, add this block to your Google Doc:

```
| IPynb Viewer |
|--------------|
| /blog.ipynb  |
```

That's it! The notebook will be fetched, parsed, and rendered with interactive code cells.

### Your First Code Cell

Let's start simple. Click the **Run** button on the code cell below to execute JavaScript in your browser:
```

#### Simple Demonstration Code
```javascript
// Your first interactive code cell!
const greeting = 'Hello from ipynb-viewer!';
const date = new Date().toLocaleDateString();

console.log(greeting);
console.log('Today is:', date);

return `${greeting} 🎉 Today is ${date}`;
```

#### Explanation After Code
```markdown
### 💡 What Just Happened?

When you clicked "Run":
✅ The JavaScript code executed **in your browser**
✅ Console output appeared below the cell
✅ The return value was displayed

**Key insight:** No server required! Code runs directly in the browser using native JavaScript.
```

#### Testing EDS Blocks
```javascript
// Import helper functions (no initialization required!)
const { testBlock } = await import('/scripts/ipynb-helpers.js');

// Define accordion content in EDS table format (rows and columns)
const accordionContent = `
  <div>
    <div>What is ipynb-viewer?</div>
    <div>A block that displays Jupyter notebooks on EDS pages with interactive JavaScript execution.</div>
  </div>
  <div>
    <div>Why use it?</div>
    <div>Create living documentation, interactive tutorials, and shareable demos without server setup.</div>
  </div>
`;

// Test the block decoration
const block = await testBlock('accordion', accordionContent);

console.log('✓ Accordion block decorated successfully!');
console.log('Block has', block.querySelectorAll('details').length, '<details> elements');

return block.outerHTML;
```

#### Visual Overlay Preview
```javascript
// Import showPreview helper
const { showPreview } = await import('/scripts/ipynb-helpers.js');

// Create accordion content
const content = `
  <div>
    <div>🎨 Styled Preview</div>
    <div>This accordion has full CSS styling from accordion.css! Click to expand/collapse.</div>
  </div>
  <div>
    <div>🖥️ Responsive Controls</div>
    <div>Use the buttons at the top to switch between Mobile (375px), Tablet (768px), and Desktop views!</div>
  </div>
`;

// Open the overlay preview!
await showPreview('accordion', content);

return '✓ Overlay opened! Check it out, then close it to continue reading.';
```

#### Best Practices Section
```markdown
### ✅ Best Practices Checklist

✅ **Import what you need** - Each cell imports independently
✅ **Use simple async pattern** - No IIFE wrappers, just `await` and `return`
✅ **One test per cell** - Keep cells focused and clear
✅ **Add markdown documentation** - Explain what each test does
✅ **Use overlay previews** - Visual verification is critical
✅ **Test edge cases** - Empty content, single item, many items
```

#### Call-to-Action/Contact
```markdown
## Want to Know More?

**Your Company Name** offers consulting services for EDS development.

### Get in Touch

📧 **Email**: [contact@example.com](mailto:contact@example.com)
🌐 **Website**: [https://example.com](https://example.com)

---

We're passionate about helping businesses leverage the power of Edge Delivery Services.
```

### Key Patterns

**Content Ratio:** ~65% markdown, ~35% code
**Engagement:** Emojis in headers, rhetorical questions, direct address ("you")
**Flow:** Introduction → Table of Contents → Progressive Parts → Summary → CTA
**Code Style:** Heavily commented, console.log() for visibility, clear return values

---

## Tutorial Notebook

**Purpose:** Step-by-step learning with exercises and progressive complexity.

### Metadata Example

```json
{
  "metadata": {
    "title": "Tutorial: Building Your First EDS Block",
    "description": "Hands-on tutorial for creating, testing, and deploying EDS blocks from scratch",
    "author": "Your Name",
    "date": "2025-01-17",
    "version": "1.0",
    "category": "tutorial",
    "difficulty": "intermediate",
    "duration": "45 minutes",
    "tags": ["tutorial", "EDS", "blocks", "hands-on", "learning"],
    "license": "MIT"
  }
}
```

**Why these fields:**
- **category: "tutorial"** → Clearly identifies as step-by-step learning
- **difficulty: "intermediate"** → Sets expectations for required knowledge
- **duration: "45 minutes"** → Longer duration reflects hands-on exercises
- **tags** → Includes "hands-on" and "learning" for educational context

### Structure Template (20-30 cells)

```markdown
# 🎓 Tutorial: Building Your First EDS Block

Welcome to this hands-on tutorial! By the end, you'll understand how to create, test, and deploy EDS blocks.

## What You'll Learn

- Block structure and naming conventions
- Content models and decoration patterns
- Testing with testBlock() and showPreview()
- Deployment best practices

## Prerequisites

- Basic JavaScript knowledge
- Familiarity with HTML/CSS
- EDS project setup

## Estimated Time

⏱️ 30-45 minutes
```

### Part Structure

#### Part 1: Foundation
```markdown
## 📚 Part 1: Understanding Block Basics

Before we start building, let's understand what EDS blocks are and how they work.

### What is a Block?

A **block** is a self-contained component that transforms simple content into interactive elements.

**Example:** A tabs block transforms this structure:
```
| Tabs |
| Tab 1 | Tab 2 |
| Content 1 | Content 2 |
```

Into interactive tabs with styling and click handlers!

### Block Structure

Every block has three files:
- `blockname.js` - Decoration logic
- `blockname.css` - Styling
- `README.md` - Documentation

Let's see an example...
```

#### Interactive Exercise
```javascript
// 🎯 Exercise 1: Your First Block Test
// Instructions: Run this cell to see a simple block in action

const { testBlock } = await import('/scripts/ipynb-helpers.js');

const simpleContent = `
  <div>
    <div>First Item</div>
    <div>First Description</div>
  </div>
`;

const block = await testBlock('accordion', simpleContent);

console.log('✓ Block created!');
console.log('Tag name:', block.tagName);
console.log('Classes:', block.className);

// ✏️ Try This: Change 'First Item' to your own text and run again!

return block.outerHTML;
```

#### Part 2: Building
```markdown
## 🔨 Part 2: Creating Your Block

Now that you understand the basics, let's create a real block!

### Step 1: Define the Content Model

First, decide what content structure your block needs.

**Our goal:** Create a "feature" block with icon, title, and description.

**Content structure:**
```
| Feature |
| 🚀 | Fast | Lightning-fast page loads |
| 🎨 | Beautiful | Stunning designs |
```

### Step 2: Write the Decoration Logic

The decoration function transforms the table into HTML...
```

#### Incremental Demonstration
```javascript
// Step 2 Demo: Building the decoration function

// Let's decorate a feature block step by step

const content = `
  <div>
    <div>🚀</div>
    <div>Fast</div>
    <div>Lightning-fast page loads</div>
  </div>
`;

// Create the block
const block = document.createElement('div');
block.className = 'feature block';
block.innerHTML = content;

// Extract parts (mimicking what decoration does)
const rows = block.querySelectorAll(':scope > div');
console.log('Found', rows.length, 'feature items');

rows.forEach((row, i) => {
  const cells = row.querySelectorAll(':scope > div');
  console.log(`Item ${i + 1}:`);
  console.log('  Icon:', cells[0]?.textContent);
  console.log('  Title:', cells[1]?.textContent);
  console.log('  Description:', cells[2]?.textContent);
});

return '✓ Check console to see the parsed structure';
```

#### Part 3: Testing
```markdown
## 🧪 Part 3: Testing Your Block

Let's test our feature block with different scenarios.

### Test 1: Single Feature

First, test with one feature:
```

```javascript
const { showPreview } = await import('/scripts/ipynb-helpers.js');

const singleFeature = `
  <div>
    <div>⚡</div>
    <div>Performance</div>
    <div>Optimized for speed</div>
  </div>
`;

await showPreview('feature', singleFeature);

return '✓ Check the overlay preview!';
```

```markdown
### Test 2: Multiple Features

Now test with multiple features:
```

```javascript
const { showPreview } = await import('/scripts/ipynb-helpers.js');

const multipleFeatures = `
  <div>
    <div>⚡</div><div>Performance</div><div>Optimized for speed</div>
  </div>
  <div>
    <div>🎨</div><div>Design</div><div>Beautiful interfaces</div>
  </div>
  <div>
    <div>🔒</div><div>Security</div><div>Enterprise-grade protection</div>
  </div>
`;

await showPreview('feature', multipleFeatures);

return '✓ Three features displayed!';
```

#### Summary
```markdown
## 🎉 Congratulations!

You've learned how to:
✅ Understand block structure
✅ Define content models
✅ Test with testBlock()
✅ Visualize with showPreview()

### Next Steps

1. **Create your own block** - Try building a custom block
2. **Read the docs** - See blocks/README.md for more info
3. **Explore examples** - Check out other blocks in /blocks/
4. **Share** - Show your team what you built!

### Resources

- [EDS Documentation](https://www.aem.live/docs/)
- [Block Examples](/blocks/)
- [Testing Guide](/docs/testing.md)
```

### Key Patterns

**Content Ratio:** ~70% markdown, ~30% code
**Engagement:** Exercises, "try this" moments, incremental building
**Flow:** Foundation → Building → Testing → Summary
**Code Style:** Step-by-step demonstrations, encouraging experimentation

---

## Concept Explanation Notebook

**Purpose:** Deep dive into a single topic with technical details and demonstrations.

### Metadata Example

```json
{
  "metadata": {
    "title": "Understanding Block Decoration in EDS",
    "description": "A comprehensive deep dive into how EDS blocks transform content into interactive elements",
    "author": "Your Name",
    "date": "2025-01-17",
    "version": "1.0",
    "category": "concept",
    "difficulty": "advanced",
    "duration": "30 minutes",
    "tags": ["concept", "EDS", "blocks", "decoration", "technical"],
    "license": "MIT"
  }
}
```

**Why these fields:**
- **category: "concept"** → Identifies as explanatory/educational content
- **difficulty: "advanced"** → Indicates technical depth and complexity
- **duration: "30 minutes"** → Medium duration for focused deep dive
- **tags** → "technical" signals detailed explanation

### Structure Template (15-25 cells)

```markdown
# 🔍 Understanding Block Decoration in EDS

A comprehensive guide to how EDS blocks transform content into interactive elements.

## The Problem

Traditional web development requires:
- Writing HTML manually
- Complex JavaScript for interactivity
- Tight coupling between content and code

This makes it hard for non-developers to create content.

## The Solution

EDS blocks solve this by:
✅ Separating content from presentation
✅ Using simple table structures
✅ Automating decoration with JavaScript

Let's explore how this works...

## Table of Contents

[The Decoration Process](#decoration)
[Content Models](#content-models)
[Decoration Functions](#decoration-functions)
[Live Examples](#examples)
[Best Practices](#best-practices)
```

### Technical Deep Dive

```markdown
## 🔧 The Decoration Process

When a page loads, EDS:

1. **Parses the document** - Converts Google Docs to HTML
2. **Identifies blocks** - Finds tables marked as blocks
3. **Calls decoration** - Invokes `decorate{BlockName}()`
4. **Applies styling** - Loads block CSS
5. **Enables interaction** - Attaches event handlers

Let's see each step in action...

### Step 1: Initial HTML Structure

Before decoration, blocks are simple div structures:
```

```javascript
// This is what EDS creates from a table
const initialHTML = `
  <div class="accordion block">
    <div>
      <div>Question 1</div>
      <div>Answer 1</div>
    </div>
    <div>
      <div>Question 2</div>
      <div>Answer 2</div>
    </div>
  </div>
`;

console.log('Initial structure (before decoration):');
console.log(initialHTML);

return '✓ This is raw, undecorated HTML';
```

```markdown
### Step 2: Decoration Transformation

The decoration function transforms this structure:
```

```javascript
const { testBlock } = await import('/scripts/ipynb-helpers.js');

const content = `
  <div>
    <div>Question 1</div>
    <div>Answer 1</div>
  </div>
  <div>
    <div>Question 2</div>
    <div>Answer 2</div>
  </div>
`;

// Before
console.log('BEFORE decoration:');
console.log('Raw divs with no semantic meaning');

// After
const decorated = await testBlock('accordion', content);
console.log('\nAFTER decoration:');
console.log('Semantic <details>/<summary> elements');
console.log('Interactive collapse/expand behavior');
console.log('Proper ARIA attributes');

return decorated.outerHTML;
```

```markdown
### What Changed?

The decoration function:
✅ Replaced divs with semantic HTML (`<details>`, `<summary>`)
✅ Added ARIA attributes for accessibility
✅ Attached event listeners for interaction
✅ Applied CSS classes for styling

This is the **power of decoration** - simple content becomes rich, interactive elements!
```

### Comparison Tables

```markdown
## ⚖️ Content Models: Simple vs Complex

| Aspect | Simple Model | Complex Model |
|--------|-------------|---------------|
| **Structure** | 2 columns (Q/A) | 3+ columns (icon/title/desc) |
| **Use case** | FAQ, accordion | Cards, features, pricing |
| **Decoration** | 1:1 mapping | Custom reorganization |
| **Example** | Accordion | Hero, cards |

### When to Use Each

**Simple Model:**
- Straightforward content
- Predictable structure
- Minimal decoration logic

**Complex Model:**
- Rich layouts
- Multiple content types
- Advanced styling needs
```

### Best Practices Section

```markdown
## ✅ Best Practices

### Do's

✅ **Keep decoration pure** - No side effects
✅ **Handle edge cases** - Empty content, missing cells
✅ **Use semantic HTML** - Better accessibility
✅ **Add ARIA attributes** - Screen reader support
✅ **Return early** - If invalid content

### Don'ts

❌ **Don't modify global state** - Blocks should be isolated
❌ **Don't assume structure** - Validate content
❌ **Don't add heavy dependencies** - Keep blocks lightweight
❌ **Don't skip testing** - Always test edge cases
```

### Key Patterns

**Content Ratio:** ~55% markdown, ~45% code
**Engagement:** Problem/solution framing, technical depth, comparisons
**Flow:** Problem → Solution → How it works → Examples → Best practices
**Code Style:** Before/after comparisons, detailed console.log(), explanatory comments

---

## Reference Guide Notebook

**Purpose:** Quick lookup with comprehensive examples for each feature.

### Metadata Example

```json
{
  "metadata": {
    "title": "EDS Helper Functions Reference",
    "description": "Complete API reference with examples for ipynb-helpers.js functions",
    "author": "Your Name",
    "date": "2025-01-17",
    "version": "1.0",
    "category": "reference",
    "difficulty": "intermediate",
    "duration": "15 minutes",
    "tags": ["reference", "api", "documentation", "helpers", "EDS"],
    "license": "MIT"
  }
}
```

**Why these fields:**
- **category: "reference"** → Clear reference/documentation identifier
- **difficulty: "intermediate"** → Assumes basic knowledge, provides advanced usage
- **duration: "15 minutes"** → Quick lookup, not linear reading
- **tags** → "api" and "documentation" for searchability

### Structure Template (25-40 cells)

```markdown
# 📖 EDS Helper Functions Reference

Complete guide to ipynb-helpers.js functions with examples.

## Quick Reference

| Function | Purpose | Returns |
|----------|---------|---------|
| `testBlock(name, html)` | Test block decoration | DOM element |
| `showPreview(name, html)` | Styled overlay preview | Success message |

## Usage Patterns

### Import
```javascript
const { testBlock, showPreview } = await import('/scripts/ipynb-helpers.js');
```

### Basic Test
```javascript
const block = await testBlock('accordion', content);
```

### Visual Preview
```javascript
await showPreview('accordion', content);
```

---

## Table of Contents

[testBlock() Function](#testblock)
[showPreview() Function](#showpreview)
[Common Patterns](#patterns)
[Error Handling](#errors)
[Performance Tips](#performance)
```

### Function Documentation

```markdown
## 🔬 testBlock() Function

**Signature:**
```javascript
async testBlock(blockName: string, innerHTML: string): Promise<HTMLElement>
```

**Parameters:**
- `blockName` - Name of the block (e.g., 'accordion', 'tabs')
- `innerHTML` - HTML content string

**Returns:** Decorated DOM element

**Purpose:** Test block decoration logic in the browser

### Basic Usage
```

```javascript
const { testBlock } = await import('/scripts/ipynb-helpers.js');

const content = '<div><div>Q</div><div>A</div></div>';
const block = await testBlock('accordion', content);

console.log('Block type:', block.className);
console.log('Children:', block.children.length);

return block.outerHTML;
```

```markdown
### With Multiple Items
```

```javascript
const { testBlock } = await import('/scripts/ipynb-helpers.js');

const multiContent = `
  <div><div>Q1</div><div>A1</div></div>
  <div><div>Q2</div><div>A2</div></div>
  <div><div>Q3</div><div>A3</div></div>
`;

const block = await testBlock('accordion', multiContent);
const itemCount = block.querySelectorAll('details').length;

return `Created ${itemCount} accordion items`;
```

```markdown
### Error Handling
```

```javascript
const { testBlock } = await import('/scripts/ipynb-helpers.js');

try {
  const block = await testBlock('nonexistent-block', '<div>test</div>');
  return '✓ Block decorated';
} catch (error) {
  console.error('Error:', error.message);
  return '✗ Block not found: ' + error.message;
}
```

### Key Patterns

**Content Ratio:** ~40% markdown, ~60% code
**Engagement:** Function signatures, parameter tables, multiple examples
**Flow:** Overview → Function docs → Examples → Error handling → Performance
**Code Style:** Short, focused examples, one concept per cell, error handling

---

## Interactive Demo Notebook

**Purpose:** Showcase capabilities with minimal explanation, maximum showing.

### Metadata Example

```json
{
  "metadata": {
    "title": "EDS Blocks Interactive Demo",
    "description": "Quick interactive showcase of EDS block capabilities - just click and explore!",
    "author": "Your Name",
    "date": "2025-01-17",
    "version": "1.0",
    "category": "demo",
    "difficulty": "beginner",
    "duration": "10 minutes",
    "tags": ["demo", "showcase", "interactive", "blocks", "EDS"],
    "license": "MIT"
  }
}
```

**Why these fields:**
- **category: "demo"** → Identifies as quick showcase
- **difficulty: "beginner"** → No prerequisite knowledge needed
- **duration: "10 minutes"** → Short, quick exploration
- **tags** → "showcase" emphasizes visual/interactive nature

### Structure Template (15-20 cells)

```markdown
# 🎨 EDS Blocks Interactive Demo

See what EDS blocks can do! Click "Run" on each cell to see live demonstrations.

## What You'll See

- Accordion blocks (FAQ-style)
- Tabs blocks (tabbed content)
- Cards blocks (grid layouts)
- Hero blocks (page headers)

No explanation needed - just click and explore! 🚀
```

### Rapid Demonstrations

```javascript
// Demo 1: Accordion
const { showPreview } = await import('/scripts/ipynb-helpers.js');

await showPreview('accordion', `
  <div><div>🚀 Fast</div><div>Lightning-fast page loads</div></div>
  <div><div>🎨 Beautiful</div><div>Stunning, responsive designs</div></div>
  <div><div>📱 Mobile</div><div>Perfect on any device</div></div>
`);

return '✓ Accordion demo opened!';
```

```javascript
// Demo 2: Tabs
const { showPreview } = await import('/scripts/ipynb-helpers.js');

await showPreview('tabs', `
  <div>
    <div>Features</div>
    <div><h3>Amazing Features</h3><p>List of features here...</p></div>
  </div>
  <div>
    <div>Pricing</div>
    <div><h3>Simple Pricing</h3><p>Pricing details here...</p></div>
  </div>
  <div>
    <div>Support</div>
    <div><h3>24/7 Support</h3><p>Contact information here...</p></div>
  </div>
`);

return '✓ Tabs demo opened! Try clicking between tabs.';
```

```markdown
## 🎯 Try It Yourself

Want to experiment? Modify the content in the cells above and run them again!

**Ideas to try:**
- Change the emoji icons
- Add more items
- Modify the text
- Try different content lengths
```

### Key Patterns

**Content Ratio:** ~30% markdown, ~70% code
**Engagement:** Visual demonstrations, minimal explanation, experimentation encouraged
**Flow:** Quick intro → Rapid demos → Invitation to experiment
**Code Style:** Inline content strings, immediate showPreview(), short return messages

---

## Summary: Choosing the Right Pattern

| Notebook Type | Best For | Content Ratio | Cells |
|---------------|----------|---------------|-------|
| **Blog Post** | Engagement, shareability | 65% MD / 35% code | 30-45 |
| **Tutorial** | Step-by-step learning | 70% MD / 30% code | 20-30 |
| **Concept Explanation** | Technical deep dives | 55% MD / 45% code | 15-25 |
| **Reference Guide** | Quick lookup | 40% MD / 60% code | 25-40 |
| **Interactive Demo** | Showcasing capabilities | 30% MD / 70% code | 15-20 |

**Universal Best Practices:**
- Always include Table of Contents
- Use progressive disclosure (simple → complex)
- Add emojis to section headers (sparingly)
- Include call-to-action or next steps
- Make code cells self-contained with imports
- Use console.log() for visibility
- Return meaningful values from code cells
