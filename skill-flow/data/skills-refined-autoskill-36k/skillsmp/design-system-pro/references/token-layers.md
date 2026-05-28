# Layered Design Token Strategy

## 1. Primitive Tokens (The Foundation)
Foundational values with no semantic meaning.
- **Naming**: `color-blue-500`, `spacing-4`, `font-bold`.
- **Purpose**: Restrict choices to a brand-approved palette.

---

## 2. Semantic Tokens (The Logic)
Tokens that describe *how* a value is used.
- **Naming**: `action-primary-bg`, `text-muted`, `border-decorative`.
- **Purpose**: Enable multi-theming (Light/Dark/High Contrast) by remapping semantic names to different primitives.

---

## 3. Component Tokens (The Specifics)
Tokens that describe a specific UI component's properties.
- **Naming**: `button-radius`, `card-shadow-hover`, `nav-item-active-color`.
- **Purpose**: Allow fine-grained control over components without affecting the rest of the system.

---

## Multi-Brand Inheritance
For 2026 enterprise systems:
1. **Core System**: Global primitives.
2. **Brand Package**: Remaps core primitives to brand semantics.
3. **Product Package**: Overrides specific brand semantics for product-level needs.
