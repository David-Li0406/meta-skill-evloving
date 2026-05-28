# Screenshot Testing Patterns

Common patterns and strategies for effective screenshot-based UI testing.

## Pattern 1: Smoke Test

Quick verification that an application launches and displays correctly.

**When to use:** After deployments, before deeper testing

**Workflow:**
1. Launch application
2. `list_windows` to verify app appears
3. `screenshot_window` to capture initial state
4. Verify key elements are present

**Pass criteria:**
- Window appears with expected title
- Main UI elements visible
- No obvious rendering errors

## Pattern 2: Regression Testing

Compare current UI against known-good baseline.

**When to use:** Before releases, after UI changes

**Workflow:**
1. Capture baseline screenshots (once, store in version control)
2. After changes, capture new screenshots
3. Compare current vs baseline
4. Report differences

**Organizing baselines:**
```
test-screenshots/
├── baseline/
│   ├── login-screen.png
│   ├── dashboard.png
│   └── settings.png
└── current/
    └── 2024-01-21/
        ├── 20240121_143052.png
        └── ...
```

**Comparison checklist:**
- [ ] Layout unchanged
- [ ] Colors/styles consistent
- [ ] Text content correct
- [ ] Icons/images present
- [ ] No clipping or overflow

## Pattern 3: State Machine Testing

Test UI across different application states.

**When to use:** Testing flows with multiple states

**States to capture:**
- Empty/initial state
- Loading state
- Success state
- Error state
- Edge cases (long content, empty data)

**Example - Form states:**
```
1. Empty form → screenshot
2. Partially filled → screenshot
3. Validation errors → screenshot
4. Submitted/loading → screenshot
5. Success message → screenshot
```

## Pattern 4: Multi-Window Testing

Test applications with multiple windows or dialogs.

**When to use:** Apps with modals, preferences, popups

**Workflow:**
1. `list_windows` to see all windows
2. Screenshot main window
3. Trigger dialog/modal
4. `list_windows` again (new window appears)
5. Screenshot dialog
6. Verify dialog content and positioning

**Tips:**
- Dialogs may have generic titles - identify by size
- Some dialogs are modal (main window dims)
- Capture both dialog and background state

## Pattern 5: Multi-Display Testing

Test applications across multiple monitors.

**When to use:** Testing display-specific behavior

**Workflow:**
1. `list_displays` to enumerate monitors
2. Note display bounds and positions
3. Move app window to each display
4. `screenshot_screen` for full display capture
5. Or `screenshot_window` for just the app

**Considerations:**
- Different displays may have different DPI/scaling
- Window positions are global coordinates
- Some apps behave differently on non-primary displays

## Pattern 6: Responsive Testing

Test UI at different window sizes.

**When to use:** Apps with responsive layouts

**Workflow:**
1. Set window to target size
2. Screenshot at each breakpoint
3. Compare layouts across sizes

**Common breakpoints:**
- Mobile: 375x667
- Tablet: 768x1024
- Desktop: 1280x720
- Large: 1920x1080

## Pattern 7: Localization Testing

Test UI with different languages/locales.

**When to use:** Internationalized applications

**What to check:**
- Text fits within containers
- No truncation or overflow
- RTL languages render correctly
- Date/number formats correct
- Icons/symbols appropriate

**Workflow:**
1. Switch app language
2. Screenshot key screens
3. Check text rendering
4. Compare with English baseline for layout shifts

## Pattern 8: Accessibility Spot Check

Visual verification of accessibility concerns.

**What to check:**
- Sufficient color contrast
- Focus indicators visible
- Text readable at standard sizes
- Interactive elements distinguishable

**Note:** Full accessibility testing requires additional tools, but screenshot testing can catch obvious visual issues.

## Anti-Patterns to Avoid

### ❌ Pixel-Perfect Comparison

Don't expect exact pixel matches:
- Anti-aliasing varies by system
- Font rendering differs across platforms
- Timestamps/dynamic content changes

**Instead:** Focus on structural/layout verification

### ❌ Testing Without Baselines

Don't just capture screenshots without comparison:
- No way to detect regressions
- Misses subtle changes

**Instead:** Establish and maintain baselines

### ❌ Ignoring Window State

Don't assume window IDs persist:
- IDs change when windows close/reopen
- Always `list_windows` before capturing

**Instead:** Always refresh window list before capturing

### ❌ Testing Only Happy Path

Don't skip error states:
- Errors reveal important UI behavior
- Users will encounter errors

**Instead:** Test all states systematically

## Reporting Results

### Structured Report Format

```markdown
## Screenshot Test Report

**Application:** MyApp v1.2.3
**Date:** 2024-01-21
**Platform:** macOS 14.0

### Summary
- Tests run: 8
- Passed: 7
- Issues: 1

### Results

#### Login Screen ✓
- Form renders correctly
- All elements present
- Proper alignment

#### Dashboard ✓
- Layout correct
- Data displays properly

#### Settings ⚠
- Issue: "Save" button clipped on right edge
- Expected: Full button visible
- Screenshot: settings-issue.png
```

### Issue Documentation

When reporting issues:
1. Describe what's wrong
2. Note expected vs actual
3. Reference screenshot file
4. Suggest severity (critical/major/minor)

## Integration with CI/CD

For automated testing pipelines:

1. **Baseline storage:** Keep baselines in version control
2. **Capture on build:** Run screenshot tests in CI
3. **Compare automatically:** Use image diff tools
4. **Report results:** Generate comparison reports
5. **Update baselines:** Review and update when UI intentionally changes

**Note:** The screenshot-mcp tools provide capture capability. For automated comparison, integrate with image comparison tools in your CI pipeline.
