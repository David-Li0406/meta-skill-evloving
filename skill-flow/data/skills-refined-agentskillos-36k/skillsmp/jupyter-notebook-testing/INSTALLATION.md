# Jupyter Notebook Testing Installation - Browser Only

Setup guide for testing EDS blocks with Jupyter notebooks in the browser.

## Overview

The Jupyter notebook testing system runs **exclusively in the browser** via the ipynb-viewer block on EDS sites. No local installation required!

## Prerequisites

To use the notebook testing system, you need:

- An EDS site with the ipynb-viewer block deployed
- A modern web browser (Chrome, Firefox, Safari, Edge)
- The test.ipynb notebook added to your EDS site

That's it! No Node.js, Python, or Jupyter installation needed.

## Setup

### 1. Deploy ipynb-viewer Block

Ensure the ipynb-viewer block is deployed to your EDS site:

```
blocks/
└── ipynb-viewer/
    ├── ipynb-viewer.js
    ├── ipynb-viewer.css
    └── README.md
```

### 2. Add test.ipynb to Your Site

Place the test.ipynb notebook in your site repository:

```
project/
├── test.ipynb          # Main test notebook
├── blocks/
│   └── ipynb-viewer/
└── scripts/
    └── ipynb-helpers.js
```

### 3. Create Page with ipynb-viewer Block

In your Google Doc or directly in your EDS page:

```
| IPynb Viewer |
|--------------|
| /test.ipynb  |
```

### 4. Open in Browser

1. Publish your page
2. Open the page in your browser
3. The notebook will be displayed with interactive cells

## File Structure

Your project should have:

```
project/
├── test.ipynb                      # Browser-only test notebook
├── scripts/
│   └── ipynb-helpers.js           # Helper functions module
├── blocks/
│   ├── ipynb-viewer/              # Notebook viewer block
│   │   ├── ipynb-viewer.js
│   │   ├── ipynb-viewer.css
│   │   └── README.md
│   ├── accordion/                  # Example block to test
│   │   ├── accordion.js
│   │   ├── accordion.css
│   │   └── README.md
│   └── [other blocks]/
└── styles/                         # EDS core styles
    ├── styles.css
    ├── fonts.css
    └── lazy-styles.css
```

## Verify Setup

### Test 1: Page Loads

Open your EDS page with the ipynb-viewer block:
- ✅ Notebook cells are visible
- ✅ Markdown cells are formatted
- ✅ Code cells have "Run" buttons

### Test 2: Test a Block

Run any code cell with an import and test:

```javascript
const { testBlock } = await import('/scripts/ipynb-helpers.js');
const block = await testBlock('accordion', '<div><div>Q</div><div>A</div></div>');
return block.outerHTML;
```

Expected output: Decorated HTML of the accordion block

### Test 3: Generate Preview

Run a preview cell:

```javascript
const { showPreview } = await import('/scripts/ipynb-helpers.js');
await showPreview('accordion', '<div><div>Q</div><div>A</div></div>');
return '✓ Preview overlay opened';
```

Expected result:
- ✅ Full-screen overlay appears on same page
- ✅ Styled accordion block visible
- ✅ Close button works
- ✅ ESC key or backdrop click closes overlay

## Browser Configuration

### Browser Console

Open browser console (F12 or Cmd+Option+I) to see:
- Console.log() output from cells
- Error messages
- Debug information

## No Installation Needed!

Unlike traditional Jupyter setups, the browser-only approach requires:

- ❌ No Node.js installation
- ❌ No Python installation
- ❌ No Jupyter installation
- ❌ No TSLab/JSLab kernel
- ❌ No jsdom installation
- ❌ No VS Code extensions

Just deploy the ipynb-viewer block and open notebooks in the browser!

## Development vs End-User

### For Developers

As a developer, you can:
1. Create/edit .ipynb files locally
2. Commit to repository
3. Deploy to EDS site
4. Test in browser

### For End Users

End users can:
1. Open EDS pages with notebooks
2. Read markdown documentation
3. Click "Run" on code cells
4. See results inline
5. Generate popup previews
6. Learn interactively

## Troubleshooting Setup

### Notebook Not Displaying

**Problem:** ipynb-viewer block shows error or blank content

**Solution:**
- Verify .ipynb file is valid JSON
- Check file path in block configuration
- Ensure file is published to EDS site
- Check browser console for errors

### Helper Functions Not Working

**Problem:** `testBlock is not defined`

**Solution:**
- Import the helpers in each cell: `const { testBlock } = await import('/scripts/ipynb-helpers.js');`
- Verify scripts/ipynb-helpers.js exists
- Check import path is absolute: `/scripts/ipynb-helpers.js`
- Check browser console for import errors

### Overlay Not Appearing

**Problem:** `showPreview()` doesn't show overlay

**Solution:**
- Check browser console for JavaScript errors
- Verify import statement is correct
- Try a simple test to confirm it works

### Blocks Not Decorating

**Problem:** Overlay shows undecorated HTML

**Solution:**
- Verify block JavaScript file exists: `blocks/blockname/blockname.js`
- Check block CSS file exists: `blocks/blockname/blockname.css`
- Check browser console for 404 errors
- Verify paths are absolute (start with `/`)

## Next Steps

After setup:

1. ✅ Import helpers in each cell with direct ES6 imports
2. ✅ Test simple blocks with `testBlock()`
3. ✅ Generate overlay previews with `showPreview()`
4. ✅ Create your own test scenarios
5. ✅ Share executable notebooks with users

## Resources

- **Main Documentation**: [docs/for-ai/explaining-jupyter.md](../../../docs/for-ai/explaining-jupyter.md)
- **Examples**: [EXAMPLES.md](EXAMPLES.md)
- **Skill Guide**: [SKILL.md](SKILL.md)
- **ipynb-viewer Block**: [blocks/ipynb-viewer/README.md](../../../blocks/ipynb-viewer/README.md)
