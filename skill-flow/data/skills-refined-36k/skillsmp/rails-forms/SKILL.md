---
name: rails-forms
description: Rails form conventions. Use when creating or editing forms in Rails.
---

# Rails Forms

## Guidelines

- Inspect existing form patterns in the codebase first.
- Always use `form_with` when creating or modifying forms.
- Use the `turbo_data` helper for Turbo-related data attributes.
- For form actions, always use the `form_actions` component.

## Form fields

- Prefer using the `form_field` component with the appropriate field type; for hidden fields, use `hidden_field` instead; use field type `:base` only in rare cases for custom fields not used elsewhere in the codebase.
- Add custom labels, hints, and help texts via I18n using the keys expected by the `form_field` component. Check the component for the expected I18n keys.
- When adding I18n entries, update all locales in use.
