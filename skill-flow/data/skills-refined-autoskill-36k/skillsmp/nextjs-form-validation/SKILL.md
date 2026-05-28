---
name: nextjs-form-validation
description: Comprehensive form validation patterns for Next.js applications with client-side validation, error display, and loading states. Use when creating or enhancing forms that need validation, error handling, real-time feedback, or loading indicators. Includes patterns for number ranges, dates, emails, slugs, and custom validation rules.
---

# Next.js Form Validation

Reusable patterns for building robust forms with validation, error handling, and loading states in Next.js applications.

## Quick Start

1. **Choose validation pattern** from [validation-patterns.md](references/validation-patterns.md)
2. **Implement error display** using [error-display.md](references/error-display.md)
3. **Add loading states** with [loading-states.md](references/loading-states.md)
4. **Use template** from [assets/form-template.tsx](assets/form-template.tsx) as starting point

## Common Validation Rules

See [validation-patterns.md](references/validation-patterns.md) for complete implementations:

- **Number ranges** - Min/max validation with custom messages
- **Date ranges** - Past/future dates, min/max duration
- **Email** - RFC-compliant email validation
- **Phone** - US phone number formats
- **Text length** - Min/max character limits
- **Slug** - URL-safe slugs (lowercase, hyphens)
- **URL** - Valid URL format
- **Password** - Strength requirements
- **Percentage** - 0-100% validation
- **Required fields** - Non-empty validation

## Error Display Patterns

See [error-display.md](references/error-display.md) for complete implementations:

- **Inline errors** - Below input with icon
- **Error borders** - Red border on invalid fields
- **Error banners** - Prominent top-of-form messages
- **Field-level state** - Track individual field errors
- **Real-time validation** - Validate on blur/change
- **Form-level validation** - Validate before submission
- **Error summary** - List all errors at once
- **Success states** - Confirmation messages

## Loading States

See [loading-states.md](references/loading-states.md) for complete implementations:

- **LoadingButton** - Reusable button with spinner
- **useTransition** - React 18 transition hook
- **Disabled states** - Disable form during submission
- **Loading overlay** - Full-form loading indicator
- **Progress indicator** - Multi-step progress bars

## Form Template

Use [assets/form-template.tsx](assets/form-template.tsx) as a starting point. The template includes:

- Client-side validation with real-time feedback
- Error display with icons and borders
- Loading states with useTransition
- Disabled states during submission
- Dark theme styling (zinc/emerald)

Customize the template by:
1. Adding/removing fields
2. Updating validation functions
3. Modifying error messages
4. Adjusting styling

## Best Practices

**Validation Timing:**
- Validate on blur for better UX (don't interrupt typing)
- Validate on submit to catch all errors
- Clear errors on change to provide immediate feedback

**Error Messages:**
- Be specific ("Must be at least 8 characters" vs "Invalid")
- Use friendly language
- Provide actionable guidance

**Loading States:**
- Always disable form during submission
- Show spinner on submit button
- Prevent double submissions

**Accessibility:**
- Use semantic HTML (label, input)
- Associate labels with inputs
- Provide error messages via aria-describedby
- Ensure keyboard navigation works

## Dark Theme Styling

All patterns use consistent dark theme:
- Background: `bg-zinc-950`
- Border: `border-zinc-800`
- Focus: `focus:border-emerald-500`
- Error: `border-red-500`, `text-red-400`
- Success: `text-emerald-400`
- Disabled: `opacity-50`
