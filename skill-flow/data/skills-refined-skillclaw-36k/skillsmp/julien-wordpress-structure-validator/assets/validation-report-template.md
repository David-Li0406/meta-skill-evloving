# WordPress Structure Validation Report

**Date**: {DATE}
**Site**: {SITE_URL}
**Theme**: {THEME_NAME}
**WordPress Version**: {WP_VERSION}

---

## Executive Summary

| Category | Status |
|----------|--------|
| Templates | {TEMPLATE_STATUS} |
| theme.json | {THEME_JSON_STATUS} |
| Block Styles | {BLOCK_STYLES_STATUS} |
| Featured Images | {FEATURED_IMAGES_STATUS} |
| File Permissions | {PERMISSIONS_STATUS} |

**Overall Status**: {OVERALL_STATUS}

---

## ✅ Validations Passed

- [ ] `index.html` template present (required fallback)
- [ ] theme.json valid JSON syntax
- [ ] theme.json has complete color palette
- [ ] Homepage properly configured
- [ ] Featured Images set for all pages
- [ ] Block styles registered correctly
- [ ] File permissions correct (644/755)
- [ ] No orphaned templates found
- [ ] Template naming follows WordPress conventions
- [ ] WCAG AA contrast ratios met

---

## ⚠️ Warnings

{LIST_WARNINGS}

---

## ❌ Errors

{LIST_ERRORS}

---

## Templates Analysis

### Templates Found

| Template | Purpose | Status | Notes |
|----------|---------|--------|-------|
| `index.html` | Fallback | ✅ | Required |
| `page.html` | Standard pages | {PAGE_STATUS} | |
| `page-accueil.html` | Homepage | {HOMEPAGE_STATUS} | |
| `single.html` | Blog posts | {SINGLE_STATUS} | |
| `404.html` | Not found | {404_STATUS} | |

### Template Parts

| Part | Found | Used In |
|------|-------|---------|
| `header.html` | {HEADER_FOUND} | {HEADER_USAGE} |
| `footer.html` | {FOOTER_FOUND} | {FOOTER_USAGE} |

### Template Hierarchy Check

**Homepage** ({HOMEPAGE_ID}):
- Assigned template: `{HOMEPAGE_TEMPLATE}`
- Resolved to: `{HOMEPAGE_RESOLVED}`
- Front page setting: {FRONT_PAGE_SETTING}

**Standard Pages**:
{PAGE_TEMPLATE_LIST}

---

## theme.json Analysis

**Version**: {THEME_JSON_VERSION}

### Color Palette

| Slug | Color | Name | Contrast (vs white) |
|------|-------|------|---------------------|
{COLOR_PALETTE_TABLE}

**Accessibility**:
- Colors meeting WCAG AA: {AA_COLOR_COUNT}/{TOTAL_COLORS}
- Colors meeting WCAG AAA: {AAA_COLOR_COUNT}/{TOTAL_COLORS}

### Typography

**Font Sizes Defined**: {FONT_SIZE_COUNT}
**Font Families Defined**: {FONT_FAMILY_COUNT}

### Spacing

**Spacing Scale**: {SPACING_SCALE_COUNT} sizes
**Units Allowed**: {SPACING_UNITS}

---

## Block Styles Analysis

**Total Block Styles Registered**: {BLOCK_STYLE_COUNT}

### Registered Styles

| Block Type | Style Name | Implementation |
|------------|------------|----------------|
{BLOCK_STYLES_TABLE}

### CSS Files Enqueued

| File | Size | Version | Status |
|------|------|---------|--------|
{CSS_FILES_TABLE}

---

## Content Analysis

### Pages

**Total Pages**: {TOTAL_PAGES}
**Pages with Featured Image**: {PAGES_WITH_FEATURED} ({PERCENTAGE}%)
**Pages without Featured Image**: {PAGES_WITHOUT_FEATURED}

| Page ID | Title | Featured Image | Template |
|---------|-------|----------------|----------|
{PAGES_TABLE}

### Homepage Configuration

- **Show on front**: {SHOW_ON_FRONT}
- **Page for posts**: {PAGE_FOR_POSTS}
- **Front page ID**: {FRONT_PAGE_ID}

---

## File System Analysis

### Directory Structure

```
{THEME_NAME}/
{DIRECTORY_TREE}
```

### File Permissions (Docker/VPS)

| Path | Owner | Permissions | Status |
|------|-------|-------------|--------|
| `functions.php` | {FUNCTIONS_OWNER} | {FUNCTIONS_PERMS} | {FUNCTIONS_STATUS} |
| `theme.json` | {THEME_JSON_OWNER} | {THEME_JSON_PERMS} | {THEME_JSON_STATUS} |
| `templates/` | {TEMPLATES_OWNER} | {TEMPLATES_PERMS} | {TEMPLATES_STATUS} |
| `assets/css/` | {CSS_OWNER} | {CSS_PERMS} | {CSS_STATUS} |

**Expected**:
- Owner: `www-data:www-data` (33:33)
- Files: `644` (rw-r--r--)
- Directories: `755` (rwxr-xr-x)

---

## Recommendations

### High Priority

{HIGH_PRIORITY_RECOMMENDATIONS}

### Medium Priority

{MEDIUM_PRIORITY_RECOMMENDATIONS}

### Low Priority / Nice to Have

{LOW_PRIORITY_RECOMMENDATIONS}

---

## Detailed Findings

### Templates

{TEMPLATE_FINDINGS}

### theme.json

{THEME_JSON_FINDINGS}

### Block Styles

{BLOCK_STYLES_FINDINGS}

### Content

{CONTENT_FINDINGS}

### Performance

{PERFORMANCE_FINDINGS}

---

## Next Steps

1. {NEXT_STEP_1}
2. {NEXT_STEP_2}
3. {NEXT_STEP_3}

---

## References

- [WordPress Template Hierarchy](references/wordpress-template-hierarchy.md)
- [FSE Best Practices](references/fse-best-practices.md)
- [WCAG 2.2 Guidelines](https://www.w3.org/WAI/WCAG22/quickref/)

---

**Report Generated**: {TIMESTAMP}
**Validation Tool**: WordPress Structure Validator v1.0
