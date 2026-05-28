# Phase 11: Inline Editor Data Attributes Audit

**CRITICAL:** Verify ALL editable elements have CMS data attributes.

## Automated Check

```bash
# Count elements with data attributes
grep -r "data-cms-entry" src/components/ --include="*.tsx" | wc -l
grep -r "data-cms-field" src/components/ --include="*.tsx" | wc -l
```

## Validation Rules

| Element Type | Required Attributes |
|--------------|---------------------|
| Text (h1, h2, p, span) | `data-cms-entry`, `data-cms-field` |
| Button/Link text | `data-cms-entry`, `data-cms-field` |
| Image | `data-cms-entry`, `data-cms-field`, `data-cms-type="image"` |
| Rich text | `data-cms-entry`, `data-cms-field`, `data-cms-type="richtext"` |
| Array container | `data-cms-entry`, `data-cms-field`, `data-cms-type="array"` |
| Array items | `data-cms-field="arrayName[index].property"` |
| Form placeholder | `data-cms-readonly="true"` |

## Manual Audit

For EVERY component rendering CMS content:

### Text Elements
- [ ] Has `data-cms-entry` with correct entry slug
- [ ] Has `data-cms-field` with correct dot-notation path
- [ ] Field path matches CMS data structure

### Images
- [ ] Has `data-cms-entry` and `data-cms-field`
- [ ] Has `data-cms-type="image"`

### Arrays
- [ ] Parent has `data-cms-type="array"`
- [ ] Each item uses indexed path: `field[0].property`

## Report Format

```
INLINE EDITOR DATA ATTRIBUTES AUDIT
===================================

Navigation.tsx:
  ✓ Logo image - data-cms-entry="global-settings" data-cms-type="image"
  ✓ Menu links - indexed paths for each item
  ✓ CTA button - correct attributes

Footer.tsx:
  ✓ All elements have correct attributes

... (all components)

SUMMARY:
- Total editable elements: 147
- Elements with correct attributes: 147
- Missing/incorrect: 0

✓ All editable elements have correct CMS data attributes.
```

## If Elements Missing Attributes

1. List each with file, line, and what's missing
2. Add correct attributes
3. Re-run audit
4. **Do NOT proceed until all elements correct**

## Git Commit

```bash
git commit -m "chore: inline editor data attributes audit passed"
```

## Checkpoint

```bash
osascript -e 'display notification "Phase 11: Editor audit passed" with title "Claude Code" sound name "Ping"'
```

**Next:** Proceed to [PHASE-12-QA.md](PHASE-12-QA.md)
