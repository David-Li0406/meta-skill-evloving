---
name: wos-qa-review
description: Run comprehensive QA review on the web application. Checks for HTML rendering errors, encoding issues, broken features, and data display problems. Use after major changes or before releases.
allowed-tools: Read, Glob, Grep, Bash(python:*, streamlit:*, pip:*), WebFetch
---

# WoS QA Review - Web Application Quality Assurance

## Purpose
Performs automated and guided QA checks on the Streamlit web application. Identifies rendering errors, encoding issues, broken functionality, and data integrity problems.

## When to Use
- After major code changes
- Before releases
- When user reports visual bugs
- Periodic quality checks

## Reference Document

See `QA_CHECKLIST.md` for the complete QA process documentation.

## QA Modes

### Quick Review (default)
Fast smoke test (2-3 minutes):
- Check all pages load without errors
- Scan for HTML rendering issues
- Scan for encoding problems
- Verify core data displays

### Full Review
Comprehensive check (10-15 minutes):
- All quick review checks
- Feature functionality testing
- Cross-browser rendering notes
- Performance assessment
- Security check basics

## Automated Checks

### 1. Page Load Validation

Check all Streamlit pages can import without errors:

```python
import importlib.util
import sys
from pathlib import Path

def check_page_imports():
    """Verify all pages can be imported."""
    pages_dir = Path("pages")
    errors = []

    for page_file in pages_dir.glob("*.py"):
        try:
            spec = importlib.util.spec_from_file_location(
                page_file.stem, page_file
            )
            # Just check syntax, don't actually run
            compile(page_file.read_text(encoding='utf-8'), page_file, 'exec')
        except SyntaxError as e:
            errors.append(f"{page_file.name}: {e}")

    return errors
```

### 2. HTML Tag Scanning

Scan Python files for potential HTML rendering issues:

```python
import re

def scan_html_issues(file_path):
    """Check for potential HTML rendering problems."""
    issues = []
    content = Path(file_path).read_text(encoding='utf-8')

    # Look for unescaped HTML in f-strings that might render incorrectly
    patterns = [
        (r'</div>\s*["\']', "Possible unclosed div in string"),
        (r'</span>\s*["\']', "Possible unclosed span in string"),
        (r'<(?!style|div|span|table|tr|td|th|br|p|b|i|u|a|img)[a-z]+', "Unusual HTML tag"),
    ]

    for pattern, msg in patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            issues.append(f"Line {line_num}: {msg}")

    return issues
```

### 3. Encoding Issue Detection

Scan for known bad character sequences:

```python
def scan_encoding_issues(directory):
    """Find encoding problems in files."""
    bad_patterns = [
        ('Ã—', '× (multiplication)'),
        ('Ã¢', 'Special char'),
        ('â€™', "' (apostrophe)"),
        ('â€"', '— (em dash)'),
        ('â€œ', '" (left quote)'),
        ('â€', '" (right quote)'),
        ('Â', 'Extra byte'),
    ]

    issues = []
    for file_path in Path(directory).rglob("*"):
        if file_path.suffix in ['.py', '.json', '.md', '.html']:
            try:
                content = file_path.read_text(encoding='utf-8')
                for bad, desc in bad_patterns:
                    if bad in content:
                        issues.append(f"{file_path}: Found {bad} ({desc})")
            except:
                pass

    return issues
```

### 4. JSON Data Validation

Verify all JSON files are valid and data displays correctly:

```python
def validate_json_data():
    """Check JSON files and key data points."""
    checks = []

    # Hero count
    heroes = json.load(open('data/heroes.json', encoding='utf-8'))
    checks.append(('Hero count', len(heroes), 'Should be ~70+'))

    # Quick tips categories
    tips = json.load(open('data/guides/quick_tips.json', encoding='utf-8'))
    cats = len(tips.get('categories', {}))
    checks.append(('Quick tip categories', cats, 'Should be ~13'))

    # Chief gear slots
    gear = json.load(open('data/chief_gear.json', encoding='utf-8'))
    slots = gear.get('slot_order', [])
    checks.append(('Chief Gear slots', len(slots), 'Should be 6'))

    return checks
```

### 5. Image Asset Verification

Check all referenced images exist:

```python
def verify_hero_images():
    """Check hero images exist."""
    heroes = json.load(open('data/heroes.json', encoding='utf-8'))
    missing = []

    for hero in heroes:
        img_file = hero.get('image_filename')
        if img_file:
            img_path = Path('assets/heroes') / img_file
            if not img_path.exists():
                missing.append(f"{hero['name']}: {img_file}")

    return missing
```

### 6. CSS/Style Verification

Check custom CSS loads:

```python
def verify_css():
    """Check CSS file exists and is valid."""
    css_path = Path('styles/custom.css')
    if not css_path.exists():
        return ["CSS file missing: styles/custom.css"]

    content = css_path.read_text(encoding='utf-8')
    if len(content) < 100:
        return ["CSS file seems too small"]

    return []
```

## Manual Check Prompts

For checks that require human verification, prompt the user:

### Visual Checks
```
Please verify the following manually:
[ ] Hero cards render with images and borders
[ ] Quick Tips cards show colored priority badges
[ ] Star ratings display correctly (★☆)
[ ] Tier badges show proper colors
[ ] Tables don't overflow their containers
```

### Functional Checks
```
Please test these features:
[ ] Hero Tracker: Can toggle hero ownership
[ ] Hero Tracker: Can edit hero level
[ ] Quick Tips: All 4 tabs work
[ ] AI Advisor: Can submit a question
[ ] Save/Load: Profile saves correctly
```

## Output Format

### Quick Review Report

```markdown
## QA Quick Review Report

**Date:** 2026-01-13
**Mode:** Quick

### Summary
- Pages: 15 checked, 0 errors
- HTML Issues: 0 found
- Encoding Issues: 0 found
- Data Validation: All passed

### Status: PASS

No issues found in quick review.
```

### Full Review Report

```markdown
## QA Full Review Report

**Date:** 2026-01-13
**Mode:** Full

### Automated Checks

| Check | Status | Details |
|-------|--------|---------|
| Page imports | PASS | 15/15 pages |
| HTML scan | PASS | No issues |
| Encoding scan | PASS | No issues |
| JSON validation | PASS | All files valid |
| Image assets | PASS | 56/56 images |
| CSS verification | PASS | CSS loaded |

### Manual Verification Needed

The following require human verification:
- [ ] Visual rendering in browser
- [ ] Feature functionality testing
- [ ] Mobile responsiveness

### Issues Found
(list any issues)

### Recommendations
(list any recommendations)

### Overall Status: PASS/FAIL
```

## Page-Specific Checks

### Quick Tips (`11_Quick_Tips.py`)

Critical checks:
- [ ] All 4 tabs render (Critical, Alliance, Mistakes, Category)
- [ ] Tip cards have colored borders
- [ ] Priority badges display
- [ ] Category icons show correctly
- [ ] No HTML tags visible in text

### Hero Tracker (`1_Hero_Tracker.py`)

Critical checks:
- [ ] Hero images load
- [ ] Tier badges with colors
- [ ] Star ratings render
- [ ] Edit expanders work
- [ ] Skill tooltips show

### Combat (`10_Combat.py`)

Critical checks:
- [ ] Stat tables render
- [ ] No encoding issues in special characters
- [ ] Decoration info displays

## Common Issues & Fixes

### HTML Showing in Output

**Symptom:** `</div>` or other HTML tags visible in text
**Cause:** Unclosed tags in markdown, or markdown in unsafe_allow_html
**Fix:** Check st.markdown() calls, ensure all HTML tags closed

### Encoding Errors

**Symptom:** `Ã—` instead of `×`, `â€™` instead of `'`
**Cause:** File saved without UTF-8, or double-encoded
**Fix:** Resave file with UTF-8 encoding, use `encoding='utf-8'` in open()

### Missing Images

**Symptom:** Broken image icons
**Cause:** Image file doesn't exist or wrong path
**Fix:** Check `assets/heroes/` directory, run `download_hero_images.py`

### CSS Not Applied

**Symptom:** Plain unstyled elements
**Cause:** CSS file not loaded or invalid
**Fix:** Check `styles/custom.css` exists and is loaded in page

## Workflow

1. **Determine mode** - Quick or Full review
2. **Run automated checks** - Page imports, HTML scan, encoding scan
3. **Validate data** - JSON files, image assets
4. **Report findings** - Generate report
5. **Flag manual checks** - List what needs human verification
6. **Update QA_CHECKLIST.md** - Mark completed checks

## Integration

Use with data-audit for comprehensive review:

```
# Run both for complete validation
/data-audit full
/qa-review full
```
