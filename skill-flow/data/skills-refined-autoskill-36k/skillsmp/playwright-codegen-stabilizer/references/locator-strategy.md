# Locator Strategy

## Locator Priority (Prefer Top)

1) `get_by_test_id(...)` (best if the app provides stable `data-testid`)
2) `get_by_role(role, name=..., exact=...)` (accessibility-first)
3) `get_by_label(...)` / `get_by_placeholder(...)` (form fields)
4) Scoped `locator(css)` using stable attributes (`name`, `id`, `aria-*`, `data-*`)
5) Text-based CSS (`:has-text()`) only when scoped and stable

Avoid:
- Absolute XPath
- Over-broad CSS like `div:nth-child(7) ...`
- `.nth()` without a container identity assertion

## Duplicate Text (“Next”, “확인”, “다음”, …)

If text appears multiple times:
- First locate the **section/container** you mean (a region, form, modal, panel).
- Then locate within that container.

Patterns:
- `container = page.get_by_role("region", name="Shipping")`
- `container.get_by_role("button", name="Next")`

If there is no accessible structure:
- use a stable ancestor selector (form id, panel id, dialog root)
- then search inside it

## Popup/Modal Locators

In modal dialogs:
- prefer `page.get_by_role("dialog")` as the root container
- locate inside that dialog only

## When You Must Use Fallbacks

Fallbacks are appropriate when:
- the site is unstable and the best locator breaks intermittently
- localization changes text
- A/B UI changes reorder elements

Rules:
- Keep fallbacks in a single place (config or locator registry).
- Log which fallback matched.
- Keep the list short (2–5).
