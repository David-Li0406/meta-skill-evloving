# Jupyter Notebook Testing Troubleshooting - Browser Only

Common issues and solutions when testing EDS blocks with Jupyter notebooks in the browser.

## No Output Displayed

**Problem:** Cell runs successfully but output cell is empty.

**Cause:** Missing `return` statement.

**Solution:**
```javascript
// ✅ GOOD - Shows output
const { testBlock } = await import('/scripts/ipynb-helpers.js');
const block = await testBlock('accordion', content);
return block.outerHTML;

// ❌ BAD - No output
const { testBlock } = await import('/scripts/ipynb-helpers.js');
const block = await testBlock('accordion', content);
```

**Always use `return` to display results in the output cell!**

## Helper Functions Not Defined

**Problem:** `ReferenceError: testBlock is not defined`

**Cause:** Missing import statement.

**Solution:**

Import the helper functions you need in each cell:
```javascript
// Import what you need
const { testBlock, showPreview } = await import('/scripts/ipynb-helpers.js');

// Use the functions
const block = await testBlock('accordion', content);
return block.outerHTML;
```

**Each cell is independent - import what you need!**

## Overlay Preview Not Appearing

**Problem:** `showPreview()` runs but no overlay appears.

**Cause:** JavaScript error during overlay creation.

**Solution:**

1. Check browser console (F12) for errors
2. Verify the helper module is loaded correctly
3. Test with a simple example:

```javascript
const { showPreview } = await import('/scripts/ipynb-helpers.js');
await showPreview('accordion', '<div><div>Q</div><div>A</div></div>');
return '✓ Preview overlay opened';
```

**Note:** Overlay previews don't have popup blocker issues - they appear on the same page!

## CSS Not Loading in Preview

**Problem:** Overlay preview shows unstyled content (no colors, no formatting).

**Cause:** Missing CSS file or incorrect path.

**Solutions:**

1. **Verify CSS file exists:**
```bash
ls -la blocks/accordion/accordion.css
# Should exist with content
```

2. **Check browser console:**
   - Press F12 to open DevTools
   - Look for 404 errors for CSS files

3. **Verify block CSS is linked:**
   - CSS loads automatically via the overlay system
   - Check that `blocks/blockname/blockname.css` exists

4. **Close and reopen overlay:**
   - Press ESC or click backdrop to close
   - Run the preview cell again

## Block Not Decorating

**Problem:** Overlay shows raw HTML structure, not decorated block.

**Cause:** Block JavaScript file missing or not executing.

**Solutions:**

1. **Verify block JavaScript exists:**
```bash
ls -la blocks/accordion/accordion.js
# Should exist and export default function
```

2. **Check block export:**
```javascript
// blocks/accordion/accordion.js should have:
export default function decorate(block) {
  // decoration logic
}
```

3. **Check browser console:**
   - Press F12 to open DevTools
   - Look for import errors or JavaScript errors

4. **Verify module path:**
   - Block JavaScript should be at: `/blocks/blockname/blockname.js`
   - Case-sensitive on production servers!

## Import Errors

**Problem:** `Failed to load module script` or 404 errors.

**Cause:** Incorrect import path.

**Solutions:**

1. **Check helper module path:**
```javascript
// ✅ CORRECT - absolute path from site root
const { testBlock, showPreview } = await import('/scripts/ipynb-helpers.js');

// ❌ INCORRECT - relative path
const { testBlock, showPreview } = await import('./scripts/ipynb-helpers.js');
```

2. **Verify file exists:**
   - Check `scripts/ipynb-helpers.js` is deployed
   - Check path is exactly `/scripts/ipynb-helpers.js`

3. **Check browser console:**
   - Look for 404 errors
   - Verify the full URL being loaded

## Async/Await Errors

**Problem:** `SyntaxError: await is only valid in async functions`

**Cause:** This shouldn't happen! Cells run in async context automatically.

**If you see this:**

```javascript
// ❌ DON'T DO THIS - unnecessary IIFE wrapper
return (async () => {
  const { testBlock } = await import('/scripts/ipynb-helpers.js');
  const block = await testBlock('accordion', content);
  return block.outerHTML;
})();

// ✅ DO THIS - simple and clean
const { testBlock } = await import('/scripts/ipynb-helpers.js');
const block = await testBlock('accordion', content);
return block.outerHTML;
```

**Cell code runs in `AsyncFunction` context - just use `await` directly!**

## Notebook Not Displaying

**Problem:** ipynb-viewer block shows error or blank content.

**Causes & Solutions:**

1. **Invalid .ipynb JSON:**
```bash
# Validate JSON syntax
cat test.ipynb | python -m json.tool
# Should output formatted JSON without errors
```

2. **Wrong file path:**
```
# Check block configuration in Google Doc:
| IPynb Viewer |
|--------------|
| /test.ipynb  |  ← Must match actual file path
```

3. **File not published:**
   - Ensure test.ipynb is committed to repository
   - Push changes to Git
   - Verify file appears on EDS site

4. **Check browser console:**
   - F12 to open DevTools
   - Look for fetch errors or JSON parse errors

## Cell Execution Stuck

**Problem:** Cell shows "Running..." but never completes.

**Causes:**

1. **Infinite loop:**
```javascript
// ❌ BAD - hangs forever
while (true) {
  // infinite loop
}

// ✅ GOOD - has exit condition
let count = 0;
while (count < 10) {
  count++;
}
```

2. **Missing return statement:**
```javascript
// Cell may appear stuck if no return
const { testBlock } = await import('/scripts/ipynb-helpers.js');
await testBlock('accordion', content);
// Add: return '✓ Complete';
```

**Solution:** Reload the page to reset all cells.

## Console Output Not Showing

**Problem:** `console.log()` output not visible.

**Cause:** Browser console not open.

**Solution:**

1. Open browser DevTools:
   - Chrome/Firefox: F12 or Cmd+Option+I (Mac)
   - Safari: Cmd+Option+C

2. Go to Console tab

3. Rerun the cell

**Note:** Cell output area shows `return` values, not `console.log()`. Console logs appear in browser DevTools console.

## Overlay Display Issues

**Problem:** Overlay content appears too small or cut off.

**Current behavior:** Overlay is full-screen with scrollable content.

**Solution:**
- The overlay automatically fills the screen
- Content is scrollable if it exceeds viewport height
- Use browser zoom (Cmd/Ctrl +/-) to adjust size if needed

## Block Content Not Found

**Problem:** `testBlock()` runs but block has no content.

**Cause:** Empty or incorrect content structure.

**Solution:**

```javascript
// ✅ GOOD - proper EDS table structure
const content = `
  <div>
    <div>Question</div>
    <div>Answer</div>
  </div>
`;

// ❌ BAD - empty or wrong structure
const content = '';
const content = '<div>Just one div</div>';
```

**Verify content structure matches block expectations!**

## ESC Key Not Closing Overlay

**Problem:** Pressing ESC doesn't close preview overlay.

**Cause:** Rare keyboard focus issue.

**Solution:**

1. Click on the overlay backdrop
2. Or click the ✕ Close button in overlay header
3. Or press ESC again

## Multiple Overlays

**Problem:** Running preview cell multiple times creates multiple overlays.

**This is normal behavior.** The overlay system removes the previous overlay before creating a new one, so you should only see one at a time.

**If you see multiple overlays:**
- There may be a JavaScript error - check console
- Refresh the page to reset

## Cell Execution Order

**Problem:** Getting import errors or undefined functions.

**Solution:**

Each cell is independent! Just import what you need in each cell:

```javascript
const { testBlock } = await import('/scripts/ipynb-helpers.js');
```

**No need to run cells in any specific order!**

## Helper Module Changes Not Reflecting

**Problem:** Updated scripts/ipynb-helpers.js but changes don't appear.

**Cause:** Browser cache.

**Solution:**

1. Hard refresh the page:
   - Chrome/Firefox: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
   - Safari: Cmd+Option+R

2. Or clear browser cache for the site

3. Reload the page

## Block Changes Not Reflecting

**Problem:** Updated block JavaScript/CSS but preview looks the same.

**Causes & Solutions:**

1. **Browser cache:**
   - Hard refresh page (Cmd+Shift+R)
   - Close and reopen overlay

2. **Changes not deployed:**
```bash
# Verify changes committed and pushed
git status
git log --oneline -n 5
```

3. **Wrong block being tested:**
```javascript
// Make sure block name matches
const { showPreview } = await import('/scripts/ipynb-helpers.js');
await showPreview('accordion', content);  // Tests 'accordion' block
```

## Cross-Origin Issues

**Problem:** Errors about CORS or cross-origin requests.

**Cause:** Trying to load resources from different domain.

**Note:** The overlay system doesn't have CORS issues since it's on the same page.

**If you still see CORS errors:**
- Check that CSS/JS files are on the same domain as the EDS site
- Verify all paths are absolute (start with `/`)

## Getting Help

If you're still stuck:

1. **Check browser console (F12)** - Most errors show here
2. **Check import statements** - Must use absolute paths starting with `/`
3. **Check file paths** - Case-sensitive, must start with `/`
4. **Try simple example** - Test with helloworld block first
5. **Reload page** - Fresh start often fixes issues
6. **Check examples** - See EXAMPLES.md for working patterns

## Quick Debugging Checklist

```javascript
// 1. Test import works
const { testBlock, showPreview } = await import('/scripts/ipynb-helpers.js');
console.log('Import successful');

// 2. Test basic DOM creation
const div = document.createElement('div');
div.textContent = 'Test';
console.log('DOM working:', div.outerHTML);
// Should show: <div>Test</div>

// 3. Test simple block
const block = await testBlock('helloworld', '');
console.log('Block created:', block.className);
// Should show: helloworld block

// 4. Return something to verify cell execution
return '✓ All checks passed';
```

## Common Patterns to Avoid

```javascript
// ❌ DON'T: Use IIFE wrappers (unnecessary)
return (async () => { ... })();

// ❌ DON'T: Forget return statement (no output)
const { testBlock } = await import('/scripts/ipynb-helpers.js');
const block = await testBlock(...);

// ❌ DON'T: Use relative import paths
import('../../scripts/helpers.js')

// ✅ DO: Import what you need in each cell
const { testBlock } = await import('/scripts/ipynb-helpers.js');
const block = await testBlock('accordion', content);
return block.outerHTML;

// ✅ DO: Use absolute import paths
import('/scripts/ipynb-helpers.js')

// ✅ DO: Run any cell at any time (cell independence!)
```
