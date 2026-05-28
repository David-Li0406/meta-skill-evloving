---
name: web-ui-design
description: Use this skill when designing user-friendly, accessible, and performant web interfaces.
---

# Web UI Design Guidelines

You are an expert in UI design principles for software development. Apply these guidelines when creating or reviewing user interfaces.

## Core Design Principles

### Clarity
- Make interfaces self-explanatory with clear labels and obvious feedback.
- Use simple language and avoid jargon.

### Consistency
- Maintain predictable patterns across visual and functional elements.
- Ensure internal consistency within your app and external consistency with platform conventions.

### Feedback
- Always respond to user actions with immediate visual feedback.
- Ensure feedback is appropriate and clear.

### Efficiency
- Help users accomplish tasks quickly with shortcuts and smart defaults.
- Implement bulk actions and progressive disclosure for advanced options.

## Visual Design

- Establish a clear visual hierarchy to guide user attention.
- Choose a cohesive color palette that reflects the brand.
- Use typography effectively for readability and emphasis.
- Maintain sufficient contrast for legibility (WCAG 2.1 AA standard).
- Ensure consistent styling throughout the application.

## Interaction Design

- Create intuitive navigation patterns and use familiar UI components.
- Provide clear calls-to-action and implement responsive design for cross-device compatibility.
- Apply animations sparingly to enhance rather than distract.

## Accessibility Standards

- Follow WCAG guidelines for web accessibility.
- Use semantic HTML to enhance screen reader compatibility.
- Provide alternative text for images and ensure keyboard navigability for all interactive elements.
- Test with various assistive technologies.

## Performance Optimization

- Optimize images and assets to minimize load times.
- Implement lazy loading for non-critical resources and use code splitting to improve initial load performance.
- Monitor Core Web Vitals (LCP, FID, CLS).

## User Feedback

- Provide clear action confirmation mechanisms and display loading indicators for asynchronous operations.
- Offer helpful error messages with recovery guidance and track user behavior through analytics.

## Information Architecture

- Organize content logically for discoverability with clear labels and effective search functionality.
- Create visual structure maps to aid navigation.

## Mobile-First Approach

- Design for mobile devices first, then scale up.
- Use touch-friendly interface elements and consider thumb zones for important interactive elements.

## Testing and Iteration

- Conduct A/B testing for critical design decisions and analyze user behavior via heatmaps and session recordings.
- Gather regular user feedback and iterate designs based on data.

## Technical Implementation

- Use relative units (%, em, rem) instead of fixed pixels.
- Implement CSS Grid and Flexbox for flexible layouts and ensure interactive elements are large enough for touch (min 44x44 pixels).
- Use CSS animations over JavaScript where feasible and implement critical CSS for above-the-fold content.

## Design Checklist

### Visual Design
- [ ] Consistent spacing scale
- [ ] Clear visual hierarchy
- [ ] Appropriate color contrast
- [ ] Readable typography
- [ ] Cohesive color palette

### Interaction Design
- [ ] All buttons have states (hover, active, focus, disabled)
- [ ] Loading states for async actions
- [ ] Error states for failures
- [ ] Success feedback for completions
- [ ] Undo for destructive actions

### Accessibility
- [ ] Semantic HTML elements
- [ ] ARIA labels where needed
- [ ] Keyboard navigation works
- [ ] Focus indicators visible
- [ ] Alt text for images
- [ ] Color not sole indicator

### Responsive
- [ ] Mobile-first approach
- [ ] Touch targets 44x44px minimum
- [ ] Readable on small screens
- [ ] No horizontal scrolling
- [ ] Images responsive

### Performance
- [ ] Smooth animations (60fps)
- [ ] No layout shifts
- [ ] Fast page loads
- [ ] Optimized images
- [ ] Reduced motion support

## Common Mistakes to Avoid

❌ **Don't:**
- Use color alone to convey information.
- Make clickable elements too small.
- Forget keyboard navigation.
- Use low-contrast text.
- Hide important actions.
- Surprise users with unexpected behavior.
- Ignore loading states.
- Leave errors unexplained.

✅ **Do:**
- Provide multiple information cues.
- Make touch targets 44x44px minimum.
- Support Tab navigation.
- Ensure 4.5:1 contrast ratio.
- Make primary actions obvious.
- Meet user expectations.
- Show loading indicators.
- Explain errors with solutions.

## Design Tools and Resources

**Colors:**
- Tailwind Colors: https://tailwindcss.com/docs/customizing-colors
- Color Contrast Checker: https://webaim.org/resources/contrastchecker/

**Typography:**
- Type Scale Generator: https://type-scale.com/
- Font Pairing: https://fontpair.co/

**Accessibility:**
- ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/
- WebAIM: https://webaim.org/

**Icons:**
- Lucide Icons: https://lucide.dev/
- Heroicons: https://heroicons.com/

**Design Systems:**
- shadcn/ui: https://ui.shadcn.com/
- Radix UI: https://www.radix-ui.com/
- Headless UI: https://headlessui.com/

## Further Reading

- Refactoring UI: https://www.refactoringui.com/
- Laws of UX: https://lawsofux.com/
- Inclusive Components: https://inclusive-components.design/
- Web Content Accessibility Guidelines: https://www.w3.org/WAI/WCAG21/quickref/