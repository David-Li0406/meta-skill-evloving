# Phase 10: Zero Hardcoded Content Audit

**CRITICAL VERIFICATION PHASE**

Before proceeding to QA, audit EVERY file for hardcoded content.

## Automated Check

```bash
# Search for potential hardcoded strings in components
grep -r "\"[A-Z]" src/components/ --include="*.tsx" | grep -v "className" | grep -v "import"
grep -r "'[A-Z]" src/components/ --include="*.tsx" | grep -v "className" | grep -v "import"
```

## Manual Audit Checklist

For EVERY `.tsx` file in `src/components/` and `src/app/`:

1. Open the file
2. Search for all quoted strings (`"` and `'`)
3. For each string, determine:
   - CSS class? ✓ OK
   - HTML attribute? ✓ OK (unless user-facing like alt text)
   - Technical identifier? ✓ OK
   - **Displayed to users? ✗ MUST BE A PROP**

## Files to Audit

- [ ] `src/components/layout/Navigation.tsx`
- [ ] `src/components/layout/Footer.tsx`
- [ ] `src/components/blocks/*.tsx` (all files)
- [ ] `src/components/ui/*.tsx` (all files)
- [ ] `src/app/layout.tsx`
- [ ] `src/app/page.tsx`
- [ ] `src/app/*/page.tsx` (all pages)
- [ ] `src/app/not-found.tsx` (if exists)

## Report Format

```
ZERO HARDCODED CONTENT AUDIT
============================

✓ Navigation.tsx - 0 hardcoded strings
✓ Footer.tsx - 0 hardcoded strings
✓ HeroSection.tsx - 0 hardcoded strings
... (all files)

TOTAL: 0 violations found

All user-facing content comes from CMS via props.
```

## If Violations Found

1. List each violation with file and line number
2. Fix by converting to prop
3. Re-run audit
4. **Do NOT proceed until 0 violations**

## Git Commit

```bash
git commit -m "chore: zero hardcoded content audit passed"
```

## Checkpoint

```bash
osascript -e 'display notification "Phase 10: Content audit passed" with title "Claude Code" sound name "Ping"'
```

**Next:** Proceed to [PHASE-11-EDITOR-AUDIT.md](PHASE-11-EDITOR-AUDIT.md)
