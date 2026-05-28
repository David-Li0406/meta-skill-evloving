# Verification Templates

Standardized verification checklists for different prompt types.

## Component Prompt Footer

```markdown
### Verification
- [ ] Types compile without errors (`typecheck` passes)
- [ ] Component renders in isolation (Storybook/test file)
- [ ] All states visually verified:
  - [ ] Default state
  - [ ] Hover state
  - [ ] Active/pressed state
  - [ ] Disabled state
  - [ ] Loading state (if applicable)
  - [ ] Error state (if applicable)
- [ ] Keyboard accessible:
  - [ ] Tab reaches element
  - [ ] Enter/Space triggers action
  - [ ] Focus ring visible
- [ ] Screen reader announces correctly
- [ ] Dark mode appearance verified
```

## Page/Flow Prompt Footer

```markdown
### Verification
- [ ] Happy path E2E test passes
- [ ] Error states manually tested:
  - [ ] Network failure
  - [ ] Validation failure
  - [ ] Empty data
- [ ] Mobile viewport verified (375px width)
- [ ] Tablet viewport verified (768px width)
- [ ] Desktop viewport verified (1280px width)
- [ ] Light theme verified
- [ ] Dark theme verified
- [ ] Loading states appear correctly
- [ ] Navigation works (back, forward, direct URL)
```

## Animation Prompt Footer

```markdown
### Verification
- [ ] Runs at 60fps (no jank)
- [ ] Respects `prefers-reduced-motion`:
  - [ ] Check with motion enabled
  - [ ] Check with motion disabled (instant/no animation)
- [ ] Doesn't block user interaction
- [ ] Feels responsive (<100ms feedback on user action)
- [ ] Completes in reasonable time (<500ms for micro, <1s for transitions)
- [ ] Works on low-end devices
```

## Form Prompt Footer

```markdown
### Verification
- [ ] All fields have labels (visible or aria-label)
- [ ] Required fields marked with asterisk
- [ ] Validation works:
  - [ ] Client-side validation on blur
  - [ ] Server-side validation on submit
  - [ ] Error messages appear inline
  - [ ] Error messages are specific
- [ ] Tab order is logical
- [ ] Submit disabled when invalid
- [ ] Success feedback shown
- [ ] Form data preserved on validation error
- [ ] Autofill works correctly
```

## Data Display Prompt Footer

```markdown
### Verification
- [ ] Empty state shows:
  - [ ] Appropriate illustration/icon
  - [ ] Helpful message
  - [ ] Call to action (if applicable)
- [ ] Loading state shows:
  - [ ] Skeleton matches data structure
  - [ ] Animation is subtle
  - [ ] Appears quickly (no delay before skeleton)
- [ ] Error state shows:
  - [ ] Error message
  - [ ] Retry action
- [ ] Data displays correctly:
  - [ ] With 1 item
  - [ ] With many items (10+)
  - [ ] With max items (pagination/infinite scroll)
  - [ ] With long text (truncation/wrapping)
```

## Modal/Dialog Prompt Footer

```markdown
### Verification
- [ ] Opens with animation
- [ ] Closes with animation
- [ ] Focus trapped inside modal
- [ ] Escape key closes modal
- [ ] Click outside closes modal (if dismissible)
- [ ] Focus returns to trigger on close
- [ ] Scrollable content works
- [ ] Mobile-friendly (full width on small screens)
- [ ] Backdrop present and interactive
- [ ] Screen reader announces:
  - [ ] Modal title on open
  - [ ] Modal closed on close
```

## Navigation Prompt Footer

```markdown
### Verification
- [ ] Active state shows current location
- [ ] Hover states on all links
- [ ] Touch targets minimum 44x44px
- [ ] Mobile menu:
  - [ ] Opens/closes smoothly
  - [ ] Doesn't shift page content
  - [ ] Close button accessible
- [ ] Keyboard navigation:
  - [ ] Tab through all items
  - [ ] Enter activates link
  - [ ] Arrow keys (if applicable)
- [ ] Deep linking works
- [ ] Browser back button works
```

## Responsive Prompt Footer

```markdown
### Verification
| Breakpoint | Width | Layout | Verified |
|------------|-------|--------|----------|
| Mobile | 375px | [expected] | [ ] |
| Mobile Large | 425px | [expected] | [ ] |
| Tablet | 768px | [expected] | [ ] |
| Desktop | 1024px | [expected] | [ ] |
| Desktop Large | 1440px | [expected] | [ ] |

- [ ] No horizontal scroll at any breakpoint
- [ ] Touch targets adequate on mobile
- [ ] Text readable without zoom
- [ ] Images scale appropriately
- [ ] Layout doesn't break between breakpoints
```

## API Integration Prompt Footer

```markdown
### Verification
- [ ] Success case works
- [ ] Loading state displays during fetch
- [ ] Error handling:
  - [ ] Network error shows message
  - [ ] 4xx error handled appropriately
  - [ ] 5xx error shows generic message
  - [ ] Timeout handled
- [ ] Retry functionality works
- [ ] Optimistic updates (if applicable):
  - [ ] UI updates immediately
  - [ ] Rollback on failure
- [ ] Race conditions handled
- [ ] Caching works (if applicable)
```

## Accessibility Prompt Footer

```markdown
### Verification
- [ ] WCAG 2.1 AA compliant:
  - [ ] Color contrast 4.5:1 for text
  - [ ] Color contrast 3:1 for UI components
  - [ ] Focus visible
  - [ ] Keyboard operable
- [ ] Screen reader tested:
  - [ ] VoiceOver (Mac)
  - [ ] NVDA (Windows) if possible
- [ ] Labels present:
  - [ ] All form inputs labeled
  - [ ] All buttons have text/aria-label
  - [ ] All images have alt text
- [ ] ARIA used correctly:
  - [ ] Live regions announce updates
  - [ ] Roles are appropriate
  - [ ] States are communicated
- [ ] Motion:
  - [ ] Reduced motion respected
  - [ ] No flashing content
```

## Theme-Aware Prompt Footer

```markdown
### Verification
- [ ] Light mode:
  - [ ] Background colors correct
  - [ ] Text colors readable
  - [ ] Border colors visible
  - [ ] Shadow appropriate
- [ ] Dark mode:
  - [ ] Background colors correct
  - [ ] Text colors readable
  - [ ] Border colors visible
  - [ ] Shadow appropriate
- [ ] Contrast maintained in both themes
- [ ] No white/black hardcoded
- [ ] Uses CSS variables/theme tokens
- [ ] System preference respected
- [ ] Manual toggle works
```

## Sprint-Level Verification

```markdown
## Sprint [N] Verification

### Pre-Ship Checklist
- [ ] All prompts in sprint completed
- [ ] Individual verifications passed
- [ ] Integration tests pass
- [ ] Visual regression (if applicable)
- [ ] Performance acceptable:
  - [ ] LCP < 2.5s
  - [ ] FID < 100ms
  - [ ] CLS < 0.1
- [ ] No console errors
- [ ] No TypeScript errors
- [ ] Accessibility audit passed
- [ ] Cross-browser tested:
  - [ ] Chrome
  - [ ] Firefox
  - [ ] Safari
  - [ ] Edge (if required)

### Rollback Plan
- [ ] Previous version tagged
- [ ] Rollback procedure documented
- [ ] Feature flags configured (if applicable)

### Monitoring
- [ ] Error tracking enabled
- [ ] Analytics events firing
- [ ] Alerts configured
```
