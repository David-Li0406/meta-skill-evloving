---
name: rails-i18n
description: Rails I18n conventions. Use when creating or editing I18n strings in Rails.
---

# Rails I18n

## Guidelines

- Don't use relative lookups with leading dots (`.key`) or chain keys together with dots (`foo.bar.baz`). Instead, always use a symbol as the key and an array of symbols as the scope parameter: `t :baz, scope: %i[foo bar]`. Only deviate from this rule if absolutely necessary.
- Always try to use `action_i18n_scope` or `base_i18n_scope` (in that order) as the scope. Both are defined in `Baseline::I18nScopes`, but might be overwritten in the controller. When inside a section generated with the `section` helper, `section_i18n_scope` might be an even better option.
- Always use `|-` for multi-line strings in I18n files.
- For translated text in views that consists of one or more paragraphs, use the `md_to_html` helper, e.g. `md_to_html t(:text, scope: action_i18n_key)`.
- When moving text from a view to I18n, first determine the language of the text in the view, move each text fragment to the corresponding namespaced I18n file, and then translate each fragment into the other locales used in the namespace and add them to the correct I18n files.
- Don't use automatic safe HTML rendering with the `_html` postfix. Use the explicit `md_to_html` helper instead if the text fragment includes HTML.
- Prefer Markdown links to passing HTML anchor elements to I18n with the `link_to` helper. Add `{:target="_blank"}` to the Markdown link if it open in a new tab/window.
- Prefer these I18n keys: `headline` for headlines, `text` for the main text of the page or section, `cta` for the text of a call to action (often a button or link). If text needs to be broken up into several I18n keys, use `text_1`, `text_2`, etc. If none of these are a good match, check the locale files for keys that have been previously used for similar text fragments.
- Prefer simple names for interpolation attributes: `name`, `url`, `cta`, etc. When in doubt, check the locale files for interpolation attributes that have been previously used.
- Don't use quotes for I18n values, unless they contain a colon.
