---
name: widget-tester
description: Use this skill when testing the embeddable Bible widget functionality in the KR92 Bible Voice project, including creating widget tests, validating embed API responses, and checking audio integration.
---

# Widget Tester

## Capabilities
- Generate test HTML pages for widget validation
- Validate embed API responses
- Test different reference formats
- Check audio integration
- Create regression test cases

## Widget Overview

The widget (`public/widget.js`) is an embeddable JavaScript component that displays Bible verses on external websites.

### Basic Usage
```html
<script src="https://your-app-url.com/widget.js" defer></script>
<div class="rn-bible" data-ref="Joh.3:16"></div>
```

## Usage Examples

### Example 1: Create Comprehensive Test Page
**User:** "Create a test page for all widget features"

**Assistant:**
```html
<!DOCTYPE html>
<html lang="fi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Raamattu Widget Test - Comprehensive</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      max-width: 1200px;
      margin: 0 auto;
      padding: 2rem;
      background: #f5f5f5;
    }
    section {
      background: white;
      padding: 2rem;
      margin: 2rem 0;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1, h2 {
      color: #333;
    }
    .test-case {
      margin: 1.5rem 0;
      padding: 1rem;
      border-left: 3px solid #4CAF50;
      background: #f9f9f9;
    }
    .test-label {
      font-weight: bold;
      color: #666;
      margin-bottom: 0.5rem;
    }
  </style>
</head>
<body>
  <h1>🧪 Raamattu Widget - Comprehensive Test Suite</h1>

  <!-- Single Verse Tests -->
  <section>
    <h2>1. Single Verse Tests</h2>

    <div class="test-case">
      <div class="test-label">Test 1.1: Basic Finnish reference</div>
      <div class="rn-bible" data-ref="Joh.3:16"></div>
    </div>

    <div class="test-case">
      <div class="test-label">Test 1.2: English reference</div>
      <div class="rn-bible" data-ref="John 3:16"></div>
    </div>

    <div class="test-case">
      <div class="test-label">Test 1.3: Period separator</div>
      <div class="rn-bible" data-ref="Joh.3.16"></div>
    </div>
  </section>

  <!-- Verse Range Tests -->
  <section>
    <h2>2. Verse Range Tests</h2>
    <!-- Add tests for verse ranges here -->
  </section>
</body>
</html>
```