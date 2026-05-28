---
name: eds-block-development
description: Use this skill when developing EDS blocks with vanilla JavaScript, following Content Driven Development principles and EDS best practices.
---

# EDS Block Development Guide

## Purpose

Guide developers through creating and modifying Adobe Edge Delivery Services (EDS) blocks using vanilla JavaScript patterns, Content Driven Development principles, and EDS best practices.

## When to Use This Skill

Automatically activates when:
- Creating new blocks in `/blocks/`
- Modifying existing block JavaScript (`.js` files)
- Implementing block decoration patterns
- Working with EDS content structures
- Using keywords: "block", "decorate", "EDS block"

## ⚠️ CRITICAL WARNING: EDS Reserved Class Names

**BEFORE WRITING ANY CODE, READ THIS:**

EDS automatically adds these class names to your blocks:
- `.{blockname}-container` - Added to parent `<section>` element
- `.{blockname}-wrapper` - Added to block's parent `<div>` wrapper

**❌ NEVER use these suffixes in your CSS or JavaScript:**
```css
/* ❌ PRODUCTION BUG - Will break entire page */
.overlay-container { position: fixed; opacity: 0; }

/* ✅ SAFE - Use different suffix */
.overlay-backdrop { position: fixed; opacity: 0; }
```

**Safe suffixes:** `-backdrop`, `-panel`, `-inner`, `-grid`, `-list`, `-content`, `-dialog`, `-popup`

## Quick Start: Block Structure

### File Organization

Every EDS block follows this structure:

```
blocks/your-block/
├── your-block.js             # Decoration logic (REQUIRED)
├── your-block.css            # Block-specific styles (REQUIRED)
├── README.md                 # Usage documentation (REQUIRED)
├── EXAMPLE.md                # Google Docs example (REQUIRED)
└── test.html                 # Development test file (RECOMMENDED)
```

**Critical naming convention:** File names must match the block name exactly (kebab-case).

## The Decorate Function Pattern

All EDS blocks export a default `decorate` function that receives the block element:

```javascript
export default function decorate(block) {
  // 1. Configuration (at the top)
  const config = {
    animationDuration: 300,
    maxItems: 10,
    errorMessage: 'Failed to load content'
  };

  // 2. Extract content from EDS structure
  const rows = Array.from(block.children);
  const content = rows.map(row => {
    const cells = Array.from(row.children);
    return cells.map(cell => cell.textContent.trim());
  });

  // 3. Create new DOM structure
  const container = document.createElement('div');
  container.className = 'your-block-wrapper';

  // 4. Build your component
  content.forEach(([title, description]) => {
    const item = document.createElement('div');
    item.className = 'your-block-item';
    item.innerHTML = `
      <h3>${title}</h3>
      <p>${description}</p>
    `;
    container.appendChild(item);
  });

  // 5. Setup event handlers
  container.querySelectorAll('.your-block-item').forEach(item => {
    item.addEventListener('click', () => {
      console.log('Item clicked');
    });
  });

  // 6. Append the container to the block
  block.appendChild(container);
}
```