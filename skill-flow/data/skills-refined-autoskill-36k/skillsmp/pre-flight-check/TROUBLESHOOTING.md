# Pre-Flight Troubleshooting Guide

When validation fails, use this guide to identify what went wrong.

## HTML Validation Errors

### html-validate errors

| Error Message | Cause | Fix |
|---------------|-------|-----|
| `void element must use self-closing syntax` | Missing `/` before `>` | `<br>` → `<br/>` |
| `element should be lowercase` | Uppercase tag | `<DIV>` → `<div>` |
| `attribute value must be quoted` | Unquoted attribute | `class=foo` → `class="foo"` |
| `multiple <h1> are not allowed` | More than one h1 | Keep only one `<h1>` per page |
| `element requires a lang attribute` | Missing lang on html | `<html>` → `<html lang="en">` |
| `inline style is not allowed` | Style attribute used | Move to CSS file |
| `unknown element` | Undefined custom element | Add to `elements.json` or use `x-` prefix |

### htmlhint errors

| Error Message | Cause | Fix |
|---------------|-------|-----|
| `doctype must be declared first` | Missing doctype | Add `<!doctype html>` at start |
| `img tag must have alt attribute` | Missing alt | Add `alt="description"` |
| `id must be unique` | Duplicate id | Use unique id values |
| `special characters must be escaped` | Unescaped `<`, `>`, `&` | Use `&lt;`, `&gt;`, `&amp;` |

## CSS Validation Errors

### stylelint errors

| Error Message | Cause | Fix |
|---------------|-------|-----|
| `Expected nesting depth to be no more than 3` | Too deeply nested | Refactor selector structure |
| `Unexpected duplicate property` | Same property twice | Remove duplicate |
| `Unexpected empty block` | `{}` with no declarations | Remove or add content |
| `Unexpected unknown value` | Invalid property value | Check valid values for property |
| `Unexpected named color` | Using `red`, `blue` | Use custom property or hex/rgb |

### Common CSS Issues

| Symptom | Likely Cause | Check |
|---------|--------------|-------|
| Styles not applying | Wrong layer order | Check `@layer` declarations |
| Hover not working | Specificity issue | Check selector specificity |
| Nesting errors | Missing `&` or wrong depth | Review nesting structure |
| Variable undefined | Typo or scope issue | Check custom property name |

## JavaScript Validation Errors

### eslint errors

| Error Message | Cause | Fix |
|---------------|-------|-----|
| `Unexpected var, use let or const` | Using `var` | Use `const` (preferred) or `let` |
| `'X' is assigned but never used` | Unused variable | Remove or prefix with `_` |
| `Expected '===' and instead saw '=='` | Loose equality | Use `===` or `!==` |
| `Identifier 'my_var' is not in camelCase` | Snake case used | Rename to `myVar` |
| `Unexpected default export` | Using `export default` | Use `export { Name }` |
| `Function has a complexity of X` | Too complex | Break into smaller functions |

### Common JavaScript Issues

| Symptom | Likely Cause | Check |
|---------|--------------|-------|
| Component not rendering | Missing `connectedCallback` | Add lifecycle method |
| Events not bubbling | Missing `bubbles: true` | Add to CustomEvent options |
| Memory leak warning | Missing cleanup | Add `disconnectedCallback` |
| Lang not updating | No MutationObserver | Add observer for lang attribute |

## Accessibility Errors

### pa11y errors

| Error Message | Cause | Fix |
|---------------|-------|-----|
| `Form field has no label` | Input without label | Add `<label for="id">` |
| `Link text is empty` | `<a></a>` or icon-only | Add text or `aria-label` |
| `Image has no alt attribute` | Missing alt | Add `alt="description"` |
| `Heading levels should increase by one` | Skipped heading | Use proper hierarchy |
| `Document has no main landmark` | Missing `<main>` | Add `<main>` element |

### Common Accessibility Fixes

| Issue | Quick Fix |
|-------|-----------|
| No label for input | Add `<label>` with `for` matching `id` |
| Empty button | Add text or `aria-label` |
| Low contrast | Use design token colors |
| No focus visible | Don't remove `:focus` outline |
| Non-keyboard accessible | Add `tabindex` and key handlers |

## Spelling Errors

### cspell errors

| Error Message | Cause | Fix |
|---------------|-------|-----|
| `Unknown word` | Not in dictionary | Add to `project-words.txt` or fix spelling |

### Adding Words to Dictionary

```bash
# Via command
/add-word YourWord

# Manual
echo "YourWord" >> project-words.txt
```

## Image Errors

### image-check.js errors

| Error Message | Cause | Fix |
|---------------|-------|-----|
| `Missing WebP alternative` | No .webp version | Run `npm run optimize:images` |
| `Missing AVIF alternative` | No .avif version | Run `npm run optimize:images` |
| `File exceeds size limit` | Image too large | Compress or resize |

### image-html-check.js errors

| Error Message | Cause | Fix |
|---------------|-------|-----|
| `Missing loading attribute` | No `loading` attr | Add `loading="lazy"` |
| `Missing dimensions` | No width/height | Add `width` and `height` attrs |
| `Consider using picture` | Multiple formats exist | Use `<picture>` element |

## Link Errors

### link-checker errors

| Error Message | Cause | Fix |
|---------------|-------|-----|
| `404 Not Found` | Broken internal link | Fix href path |
| `File does not exist` | Referenced file missing | Create file or fix path |

## Metadata Errors

### metadata-check.js errors

| Error Message | Cause | Fix |
|---------------|-------|-----|
| `Missing required meta: X` | Required tag absent | Add the meta tag |
| `og:image must use absolute URL` | Relative URL used | Use full https:// URL |

## Still Stuck?

1. **Read the full error message** - Often includes line number
2. **Check the config file** - `.htmlvalidate.json`, `eslint.config.js`, etc.
3. **Look at passing examples** - `test/fixtures/valid/`
4. **Check the skill documentation** - Relevant skill's SKILL.md
5. **Run with verbose output** - Add `--debug` flag if available
