# Advanced Jupyter Notebook Testing Techniques - Browser Only

Advanced patterns and techniques for testing EDS blocks with Jupyter notebooks in the browser.

## Performance Testing

Measure block decoration performance:

```javascript
const { testBlock } = await import('/scripts/ipynb-helpers.js');

console.time('block-decoration');
const block = await testBlock('myblock', content);
console.timeEnd('block-decoration');
// Output: block-decoration: 15.234ms

return `Decoration time logged to console`;
```

## Testing Multiple Variations

Test multiple content variations:

```javascript
const { testBlock, showPreview } = await import('/scripts/ipynb-helpers.js');

const variations = [
  '<div><div>Test 1</div><div>Content 1</div></div>',
  '<div><div>Test 2</div><div>Content 2</div></div>',
  '<div><div>Test 3</div><div>Content 3</div></div>',
];

const results = [];

for (let i = 0; i < variations.length; i++) {
  const block = await testBlock('accordion', variations[i]);
  results.push(`Variation ${i + 1}: ${block.querySelectorAll('details').length} items`);

  // Optional: Open preview for each
  // await showPreview('accordion', variations[i]);
}

console.log(results.join('\n'));
return results;
```

## Generating Test Content

Create content programmatically:

```javascript
const { testBlock, showPreview } = await import('/scripts/ipynb-helpers.js');

function generateAccordionContent(numItems) {
  const items = Array.from({ length: numItems }, (_, i) => `
    <div>
      <div>Question ${i + 1}</div>
      <div>This is answer ${i + 1} with test content.</div>
    </div>
  `).join('');
  return items;
}

// Test with different sizes
const content3 = generateAccordionContent(3);
const block3 = await testBlock('accordion', content3);
await showPreview('accordion', content3);

const content10 = generateAccordionContent(10);
const block10 = await testBlock('accordion', content10);
// await showPreview('accordion', content10); // Uncomment to preview

return `Created ${block3.querySelectorAll('details').length} and ${block10.querySelectorAll('details').length} items`;
```

## Before/After Analysis

Analyze transformation impact:

```javascript
const { testBlock } = await import('/scripts/ipynb-helpers.js');

const content = `
  <div>
    <div>Question 1</div>
    <div>Answer 1</div>
  </div>
`;

const before = document.createElement('div');
before.className = 'accordion';
before.innerHTML = content;

const beforeHTML = before.innerHTML;
const beforeSize = new Blob([beforeHTML]).size;

// Decorate
const after = await testBlock('accordion', content);

const afterHTML = after.innerHTML;
const afterSize = new Blob([afterHTML]).size;

console.log('Original:', beforeSize, 'bytes');
console.log('Transformed:', afterSize, 'bytes');
console.log('Size ratio:', (afterSize / beforeSize).toFixed(2) + 'x');

return `Size: ${beforeSize}b → ${afterSize}b (${(afterSize / beforeSize).toFixed(2)}x)`;
```

## Batch Testing

Test multiple blocks efficiently:

```javascript
const { testBlock } = await import('/scripts/ipynb-helpers.js');

const blocks = {
  'accordion': '<div><div>Q</div><div>A</div></div>',
  'cards': '<div><div><img src="test.jpg" alt="Test"></div><div><h3>Title</h3><p>Content</p></div></div>',
  'columns': '<div><div><p>Column 1</p></div><div><p>Column 2</p></div></div>'
};

const results = {};

for (const [blockName, content] of Object.entries(blocks)) {
  try {
    const block = await testBlock(blockName, content);
    results[blockName] = { success: true, children: block.children.length };
    console.log(`✓ ${blockName}`);
  } catch (error) {
    results[blockName] = { success: false, error: error.message };
    console.log(`✗ ${blockName}: ${error.message}`);
  }
}

return results;
```

## Content Validation

Validate block output structure:

```javascript
const { testBlock } = await import('/scripts/ipynb-helpers.js');

function validateAccordion(block) {
  const errors = [];

  const details = block.querySelectorAll('details');
  if (details.length === 0) {
    errors.push('No <details> elements found');
  }

  details.forEach((detail, i) => {
    const summary = detail.querySelector('summary');
    if (!summary) {
      errors.push(`Item ${i}: Missing <summary>`);
    }
  });

  return {
    valid: errors.length === 0,
    errors
  };
}

const content = `
  <div>
    <div>Question</div>
    <div>Answer</div>
  </div>
`;

const block = await testBlock('accordion', content);
const validation = validateAccordion(block);

console.log(validation.valid ? '✓ Valid' : '✗ Invalid:', validation.errors);

return validation;
```

## Dynamic Content Generation

Generate realistic test content:

```javascript
const { testBlock, showPreview } = await import('/scripts/ipynb-helpers.js');

function generateRealisticAccordion() {
  const faqs = [
    {
      q: "What is Adobe Edge Delivery Services?",
      a: "Adobe Edge Delivery Services (EDS) is a composable platform for creating high-impact, high-performance websites."
    },
    {
      q: "How do blocks work?",
      a: "Blocks are JavaScript functions that decorate DOM elements, transforming simple HTML into interactive components."
    },
    {
      q: "Why use Jupyter notebooks for testing?",
      a: "Jupyter notebooks provide instant feedback without build steps, making development faster and more interactive."
    }
  ];

  return faqs.map(({q, a}) => `
    <div>
      <div>${q}</div>
      <div>${a}</div>
    </div>
  `).join('');
}

const realisticContent = generateRealisticAccordion();
const block = await testBlock('accordion', realisticContent);
await showPreview('accordion', realisticContent);

return `Generated ${block.querySelectorAll('details').length} FAQ items`;
```

## Test Data Libraries

Create reusable test data:

```javascript
const { testBlock } = await import('/scripts/ipynb-helpers.js');

const TestData = {
  accordion: {
    empty: '',
    single: '<div><div>Q</div><div>A</div></div>',
    multiple: `
      <div><div>Q1</div><div>A1</div></div>
      <div><div>Q2</div><div>A2</div></div>
      <div><div>Q3</div><div>A3</div></div>
    `,
    malformed: '<div><div>Q only</div></div>',
    nested: `
      <div>
        <div>Question with <strong>formatting</strong></div>
        <div>Answer with <a href="#">links</a> and <em>emphasis</em></div>
      </div>
    `
  }
};

const results = [];

// Test all variations
for (const [variant, content] of Object.entries(TestData.accordion)) {
  try {
    const block = await testBlock('accordion', content);
    results.push(`✓ ${variant}: ${block.children.length} children`);
  } catch (error) {
    results.push(`✗ ${variant}: ${error.message}`);
  }
}

console.log(results.join('\n'));
return results;
```

## Accessibility Testing

Check for accessibility issues:

```javascript
const { testBlock } = await import('/scripts/ipynb-helpers.js');

function checkAccessibility(block) {
  const issues = [];

  // Check for images without alt text
  const images = block.querySelectorAll('img');
  images.forEach((img, i) => {
    if (!img.alt) {
      issues.push(`Image ${i}: Missing alt attribute`);
    }
  });

  // Check for buttons without labels
  const buttons = block.querySelectorAll('button');
  buttons.forEach((btn, i) => {
    if (!btn.textContent.trim() && !btn.getAttribute('aria-label')) {
      issues.push(`Button ${i}: Missing label`);
    }
  });

  return {
    accessible: issues.length === 0,
    issues
  };
}

const content = `
  <div>
    <div>Question</div>
    <div>Answer</div>
  </div>
`;

const block = await testBlock('accordion', content);
const a11y = checkAccessibility(block);

console.log(a11y.accessible ? '✓ Accessible' : '⚠ Issues:', a11y.issues);

return a11y;
```

## Structure Analysis

Analyze block structure:

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

const block = await testBlock('accordion', content);

const analysis = {
  tagName: block.tagName,
  className: block.className,
  childCount: block.children.length,
  detailsElements: block.querySelectorAll('details').length,
  summaryElements: block.querySelectorAll('summary').length,
  structure: []
};

// Analyze each child
Array.from(block.children).forEach((child, i) => {
  analysis.structure.push({
    index: i,
    tagName: child.tagName,
    className: child.className,
    childCount: child.children.length
  });
});

console.log('Block Analysis:', JSON.stringify(analysis, null, 2));

return analysis;
```

## Sequential Testing with Delays

Test blocks with controlled timing:

```javascript
const { testBlock } = await import('/scripts/ipynb-helpers.js');

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

const tests = [
  { name: 'accordion', content: '<div><div>Q</div><div>A</div></div>' },
  { name: 'cards', content: '<div><div><img src="test.jpg" alt="Test"></div><div><h3>Title</h3></div></div>' },
  { name: 'columns', content: '<div><div><p>Col 1</p></div><div><p>Col 2</p></div></div>' }
];

const results = [];

for (const test of tests) {
  console.log(`Testing ${test.name}...`);

  try {
    const block = await testBlock(test.name, test.content);
    results.push(`✓ ${test.name}`);

    // Optional delay between tests
    await delay(100);
  } catch (error) {
    results.push(`✗ ${test.name}: ${error.message}`);
  }
}

console.log('\nResults:');
console.log(results.join('\n'));

return results;
```

## Snapshot Comparison

Compare outputs:

```javascript
const { testBlock } = await import('/scripts/ipynb-helpers.js');

const content = `
  <div>
    <div>Question</div>
    <div>Answer</div>
  </div>
`;

// Generate block
const block = await testBlock('accordion', content);
const snapshot = block.outerHTML;

// Store snapshot in sessionStorage for later comparison
sessionStorage.setItem('accordion-snapshot', snapshot);

console.log('Snapshot saved to sessionStorage');
console.log('Length:', snapshot.length, 'characters');

return `Snapshot: ${snapshot.length} chars`;
```

```javascript
// Later, compare with stored snapshot
const { testBlock } = await import('/scripts/ipynb-helpers.js');

const content = `
  <div>
    <div>Question</div>
    <div>Answer</div>
  </div>
`;

const block = await testBlock('accordion', content);
const current = block.outerHTML;

const stored = sessionStorage.getItem('accordion-snapshot');

const same = current === stored;
console.log(same ? '✓ Identical to snapshot' : '✗ Different from snapshot');

if (!same) {
  console.log('Current length:', current.length);
  console.log('Stored length:', stored?.length || 0);
}

return { same, currentLength: current.length, storedLength: stored?.length || 0 };
```

## Interactive Debugging

Step-by-step debugging:

```javascript
const content = `
  <div>
    <div>Question</div>
    <div>Answer</div>
  </div>
`;

console.log('Step 1: Creating block element');
const block = document.createElement('div');
block.className = 'accordion';
block.innerHTML = content;
console.log('  Initial HTML:', block.innerHTML.substring(0, 50) + '...');

console.log('Step 2: Importing block module');
const module = await import(`/blocks/accordion/accordion.js`);
console.log('  Module loaded:', !!module.default);

console.log('Step 3: Decorating block');
await module.default(block);
console.log('  Final HTML:', block.innerHTML.substring(0, 50) + '...');

console.log('Step 4: Analyzing result');
const details = block.querySelectorAll('details');
console.log('  Created details:', details.length);

return `✓ Debug complete: ${details.length} details created`;
```

## Performance Metrics Collection

Collect comprehensive metrics:

```javascript
const { testBlock } = await import('/scripts/ipynb-helpers.js');

const content = `
  <div>
    <div>Question</div>
    <div>Answer</div>
  </div>
`;

const metrics = {
  blockName: 'accordion',
  timestamp: new Date().toISOString()
};

// Measure decoration time
const startTime = performance.now();
const block = await testBlock('accordion', content);
const endTime = performance.now();

metrics.decorationTime = (endTime - startTime).toFixed(2) + 'ms';

// Measure sizes
const beforeHTML = `<div class="accordion">${content}</div>`;
const afterHTML = block.outerHTML;

metrics.beforeSize = new Blob([beforeHTML]).size;
metrics.afterSize = new Blob([afterHTML]).size;
metrics.sizeRatio = (metrics.afterSize / metrics.beforeSize).toFixed(2) + 'x';

// Count elements
metrics.elementsBefore = beforeHTML.match(/<[^>]+>/g)?.length || 0;
metrics.elementsAfter = afterHTML.match(/<[^>]+>/g)?.length || 0;

console.log('Performance Metrics:', JSON.stringify(metrics, null, 2));

return metrics;
```

## Tips for Advanced Testing

### Use Console Effectively

```javascript
const { testBlock } = await import('/scripts/ipynb-helpers.js');

console.group('Block Testing');
console.log('Testing accordion block...');

const block = await testBlock('accordion', '<div><div>Q</div><div>A</div></div>');

console.log('Result:', block);
console.table([
  { metric: 'Children', value: block.children.length },
  { metric: 'Class', value: block.className },
  { metric: 'Details', value: block.querySelectorAll('details').length }
]);

console.groupEnd();

return '✓ Check console for detailed output';
```

### Store Results for Later Analysis

```javascript
const { testBlock } = await import('/scripts/ipynb-helpers.js');

// Run test and store results
const content = '<div><div>Q</div><div>A</div></div>';
const block = await testBlock('accordion', content);

const results = {
  timestamp: Date.now(),
  blockName: 'accordion',
  children: block.children.length,
  html: block.outerHTML
};

// Store in sessionStorage
const stored = JSON.parse(sessionStorage.getItem('test-results') || '[]');
stored.push(results);
sessionStorage.setItem('test-results', JSON.stringify(stored));

console.log(`Stored result ${stored.length}`);

return `Stored ${stored.length} results`;
```

```javascript
// Retrieve and analyze stored results
(() => {
  const stored = JSON.parse(sessionStorage.getItem('test-results') || '[]');

  console.log(`Found ${stored.length} stored results`);
  stored.forEach((result, i) => {
    console.log(`${i + 1}. ${result.blockName} - ${new Date(result.timestamp).toLocaleTimeString()}`);
  });

  return stored;
})();
```
