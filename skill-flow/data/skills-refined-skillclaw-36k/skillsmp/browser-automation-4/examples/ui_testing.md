# UI Testing Example

## Use Case
Visual verification and user interface testing.

## Task Setup

```
TaskName: "Verifying Responsive Design"

Task: Test responsive layout at different breakpoints:
1. Navigate to https://example.com
2. Set viewport to mobile size (375x667)
3. Capture screenshot labeled "mobile"
4. Verify mobile menu hamburger icon is visible
5. Set viewport to tablet size (768x1024)
6. Capture screenshot labeled "tablet"
7. Set viewport to desktop size (1920x1080)
8. Capture screenshot labeled "desktop"
9. Verify navigation bar shows all menu items inline
10. Return confirmation of all screenshots and layout verification results

RecordingName: responsive_test
```

## Expected Return

```
Breakpoint Testing Results:
- Mobile (375x667): ✓ Hamburger menu visible, screenshot saved
- Tablet (768x1024): ✓ Hybrid layout correct, screenshot saved
- Desktop (1920x1080): ✓ Full navigation visible, screenshot saved

All responsive breakpoints passed validation.
Screenshots saved to artifacts directory.
```

## Variations

### Component Visibility Testing
```
Task: On the dashboard page:
1. Verify that all expected widgets are visible:
   - Sales chart
   - Recent orders table
   - User statistics cards
   - Activity feed
2. Capture screenshot showing all components
3. Return list of visible components and any missing ones
```

### Interactive Element Testing
```
Task: Test interactive elements on the product page:
1. Hover over product image - verify zoom feature activates
2. Click on thumbnail images - verify main image updates
3. Click "Size" dropdown - verify options appear
4. Select different colors - verify product image changes
5. Document all interactions and any issues found
```

### Animation Testing
```
Task: Test page animations:
1. Navigate to landing page
2. Observe hero section fade-in animation on load
3. Scroll down to trigger scroll-based animations
4. Note timing and smoothness of each animation
5. Capture video recording showing all animations
6. Return assessment of animation quality
```

### Accessibility Testing
```
Task: Perform basic accessibility checks:
1. Navigate using only keyboard (Tab key)
2. Verify all interactive elements are reachable
3. Check focus indicators are visible
4. Test that modal can be closed with Escape key
5. Verify alt text exists on images
6. Return accessibility audit results
```

### Cross-Browser Verification
```
Task: Verify consistent rendering:
1. Capture screenshot of homepage layout
2. Note any browser-specific styling differences
3. Test critical user flows (login, checkout)
4. Document any browser compatibility issues
5. Return compatibility report
```

## Visual Regression Testing

### Before/After Comparison
```
Task: Test UI changes after deployment:
1. Navigate to staging.example.com/dashboard
2. Capture full-page screenshot
3. Navigate to production.example.com/dashboard
4. Capture full-page screenshot
5. Note any visible differences in layout, colors, or spacing
6. Return comparison summary
```

### Component State Testing
```
Task: Test button states:
1. Capture button in default state
2. Hover over button - capture hover state
3. Click button - capture active/loading state
4. After action completes - capture success state
5. Return screenshots of all states
```

## Performance Testing

### Load Time Verification
```
Task: Measure page load performance:
1. Navigate to https://example.com
2. Measure time until page is interactive
3. Note time until largest contentful paint
4. Verify all critical resources loaded
5. Return performance metrics
```

### Network Throttling Test
```
Task: Test on slow connection:
1. Enable network throttling (3G simulation)
2. Navigate to product gallery page
3. Note loading behavior and user experience
4. Verify loading indicators appear appropriately
5. Return loading performance assessment
```

## Error State Testing

### 404 Page Testing
```
Task: Verify error page handling:
1. Navigate to https://example.com/nonexistent-page
2. Verify 404 page displays correctly
3. Check that "Return Home" link works
4. Capture screenshot of error page
5. Return error page content verification
```

### Form Error Testing
```
Task: Test form validation errors:
1. Try submitting empty form
2. Capture validation error messages
3. Try invalid email format
4. Capture email-specific error
5. Try password too short
6. Capture password error
7. Return all validation messages and their accuracy
```

## User Flow Testing

### Complete E2E Flow
```
Task: Test complete checkout flow:
1. Browse products and add item to cart
2. Verify cart badge updates
3. Navigate to cart page
4. Update quantity and verify total recalculates
5. Proceed to checkout
6. Fill shipping information
7. Select payment method
8. Review order summary
9. Stop before final submission
10. Capture screenshots at each step
11. Return flow completion report
```

### Multi-User Scenario
```
Task: Test user switching:
1. Log in as admin user
2. Verify admin panel is accessible
3. Log out
4. Log in as regular user
5. Verify admin panel is NOT accessible
6. Return permission verification results
```
