# Test Fixtures

Organization and management of test fixture files.

## Directory Structure

```
.claude/test/
├── fixtures/
│   ├── valid/                    # Files that should PASS validation
│   │   ├── minimal.html          # Minimal valid HTML
│   │   ├── full-semantic.html    # Complete semantic HTML
│   │   ├── sample.css            # Valid CSS
│   │   ├── good-component.js     # Valid JavaScript
│   │   ├── markdown/             # Valid markdown files
│   │   ├── readability/          # Readable content
│   │   └── seo/                  # SEO-compliant pages
│   │
│   ├── invalid/                  # Files that should FAIL validation
│   │   ├── html-validate/        # HTML validation failures
│   │   ├── htmlhint/             # HTMLHint rule violations
│   │   ├── pa11y/                # Accessibility failures
│   │   ├── eslint/               # JavaScript errors
│   │   ├── stylelint/            # CSS errors
│   │   ├── markdown/             # Markdown errors
│   │   └── cspell/               # Spelling errors
│   │
│   ├── budget/                   # Resource budget test files
│   └── images/                   # Image validation files
│
└── validators/                   # Test files (*.test.js)
```

## Fixture Naming

| Type | Convention | Example |
|------|------------|---------|
| Valid | Descriptive name | `full-semantic.html` |
| Invalid | Rule or error type | `missing-alt.html`, `no-doctype.html` |
| Temporary | `temp-*` prefix | `temp-test-123.html` |

## Creating Valid Fixtures

### Minimal HTML Template

```html
<!doctype html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Test Page</title>
  <meta name="description" content="Test page description" />
</head>
<body>
  <main>
    <h1>Test Content</h1>
    <p>Test paragraph.</p>
  </main>
</body>
</html>
```

### Minimal CSS Template

```css
/* Valid CSS fixture */
:root {
  --color-text: #333;
}

body {
  color: var(--color-text);
}
```

### Minimal JavaScript Template

```javascript
/**
 * Valid JavaScript fixture
 */
export function example() {
  const message = 'Hello';
  return message;
}
```

## Creating Invalid Fixtures

Organize by the validator or rule they trigger:

```
.claude/test/fixtures/invalid/
├── html-validate/
│   ├── missing-doctype.html      # No <!doctype>
│   ├── duplicate-id.html         # Repeated IDs
│   └── void-style.html           # <br> instead of <br />
│
├── pa11y/
│   ├── missing-alt.html          # <img> without alt
│   ├── low-contrast.html         # Poor color contrast
│   └── missing-label.html        # Input without label
│
└── eslint/
    ├── uses-var.js               # var instead of const/let
    ├── default-export.js         # export default
    └── missing-semicolon.js      # No semicolons
```

## Temporary Fixtures

For tests that need dynamic content, create and clean up fixtures:

```javascript
import { writeFile, mkdir, rm } from 'node:fs/promises';
import { join } from 'node:path';
import { before, after } from 'node:test';

const tempDir = join(import.meta.dirname, 'temp');

describe('Dynamic fixture tests', () => {
  before(async () => {
    await mkdir(tempDir, { recursive: true });
  });

  after(async () => {
    await rm(tempDir, { recursive: true });
  });

  it('tests with generated fixture', async () => {
    const fixture = join(tempDir, 'test.html');
    await writeFile(fixture, '<!doctype html>...');
    // Test with fixture
  });
});
```

## Binary Fixtures

Generate binary data programmatically rather than committing binary files:

### PNG Generation

```javascript
function createMinimalPNG() {
  return Buffer.from([
    0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,
    0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,
    0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
    0x08, 0x06, 0x00, 0x00, 0x00, 0x1F, 0x15, 0xC4,
    0x89, 0x00, 0x00, 0x00, 0x0A, 0x49, 0x44, 0x41,
    0x54, 0x78, 0x9C, 0x63, 0x00, 0x01, 0x00, 0x00,
    0x05, 0x00, 0x01, 0x0D, 0x0A, 0x2D, 0xB4, 0x00,
    0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE,
    0x42, 0x60, 0x82
  ]);
}
```

### WebP Generation

```javascript
function createMinimalWebP() {
  return Buffer.from([
    0x52, 0x49, 0x46, 0x46, // RIFF
    0x1A, 0x00, 0x00, 0x00, // File size
    0x57, 0x45, 0x42, 0x50, // WEBP
    0x56, 0x50, 0x38, 0x4C, // VP8L
    0x0D, 0x00, 0x00, 0x00, // Chunk size
    0x2F, 0x00, 0x00, 0x00, // Signature
    0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00,
    0x00, 0x00
  ]);
}
```

## Fixture Best Practices

| Practice | Rationale |
|----------|-----------|
| Keep fixtures minimal | Easier to understand what's being tested |
| One error per invalid fixture | Clear cause-effect relationship |
| Use descriptive names | `missing-alt.html` not `test1.html` |
| Document purpose in file | Comment at top explaining what it tests |
| Avoid dependencies | Fixtures should be self-contained |
| Clean up temp files | Use `after()` hooks for cleanup |

## Fixture Discovery

Find all fixtures for a specific validator:

```javascript
import { readdirSync } from 'node:fs';
import { join } from 'node:path';

const fixturesDir = join(import.meta.dirname, '../fixtures');

function getValidFixtures(extension = '.html') {
  return readdirSync(join(fixturesDir, 'valid'))
    .filter(f => f.endsWith(extension))
    .map(f => join(fixturesDir, 'valid', f));
}

function getInvalidFixtures(validator) {
  const dir = join(fixturesDir, 'invalid', validator);
  return readdirSync(dir).map(f => join(dir, f));
}
```
