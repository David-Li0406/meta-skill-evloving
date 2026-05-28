---
name: a2ui-core
description: The foundational skill for building Agent-to-User Interface (A2UI) components with Lit. Defines the protocol, base classes, and patterns for Generative UI that is "Safe Like Data, Expressive Like Code".
---

# A2UI Core: Protocol & Implementation

## Overview

A2UI (Agent-to-User Interface) enables AI agents to "speak UI" by transmitting **intent and structure** rather than executable code. This skill provides the patterns for building compliant Lit components.

## Core Philosophy

> **"Safe Like Data, Expressive Like Code"**

| Principle | Implementation |
|:----------|:---------------|
| **No Executable Logic** | Agents send JSON component trees, never JavaScript |
| **Trusted Catalog** | Only registered components render; unknown types are ignored |
| **Native Fidelity** | Components inherit host app's design system via CSS variables |

---

## Protocol Specification

### The Adjacency List Model

Unlike the DOM (nested tree), A2UI uses a **flat list with ID references**. This:
- Prevents LLM syntax errors from deep nesting
- Enables O(1) updates by component ID
- Allows efficient streaming

```json
{
  "surfaceUpdate": {
    "surfaceId": "main-view",
    "components": [
      { "id": "root", "component": { "Column": { "children": { "explicitList": ["header", "content"] } } } },
      { "id": "header", "component": { "Text": { "text": { "literalString": "Title" } } } },
      { "id": "content", "component": { "Text": { "text": { "path": "/data/message" } } } }
    ]
  }
}
```

### Message Verbs

| Verb | Description |
|:-----|:------------|
| `surfaceUpdate` | Structural blueprints (component definitions) |
| `dataModelUpdate` | State patches; triggers Signal reactivity |
| `beginRendering` | Mount a specific root component |
| `userAction` | Client → Agent intent (unidirectional) |
| `deleteSurface` | Teardown and cleanup |

### Data Binding (JSON Pointers - RFC 6901)

Properties can be:
- **Literal**: `{ "label": { "literalString": "Submit" } }`
- **Bound**: `{ "value": { "path": "/user/email" } }` → Reactive subscription

---

## Implementation with Lit

### Base Class: DynamicComponent

All A2UI components extend `DynamicComponent` (see `assets/DynamicComponent.ts`):

```typescript
// Usage in your component
@customElement('agui-my-widget')
export class MyWidget extends DynamicComponent {
  render() {
    const label = this.resolve(this.componentDefinition.label);
    return html`<span>${label}</span>`;
  }
}
```

**Key Methods:**
- `resolve(prop)` → Resolves literal values or subscribes to data paths
- `dispatchUserAction(name, context)` → Sends intent to agent

### Component Registry

The **Trusted Catalog** pattern (see `assets/ComponentRegistry.ts`):

```typescript
componentRegistry.register('MyWidget', MyWidget, 'agui-my-widget');
```

If an agent requests an unregistered component, the renderer safely ignores it.

### Smart Wrappers

For 3rd-party libraries (Chart.js, D3, etc.), use Smart Wrappers (see `assets/ChartWrapper.ts`):
1. Create a container element
2. Bridge A2UI props to library API in `updated()`
3. Clean up in `disconnectedCallback()`

---

## Component Implementation Checklist

- [ ] Extend `DynamicComponent` (or `LitElement` for simple cases)
- [ ] Use `@customElement('agui-*')` naming convention
- [ ] Use `resolve()` for all dynamic properties
- [ ] Use `dispatchUserAction()` for all user interactions
- [ ] Apply styling via CSS custom properties (see `a2ui-design-bridge` skill)
- [ ] Register in `ComponentRegistry` if using full A2UI stack

---

## Validation

Run the payload validator to check JSON structure:

```bash
python3 scripts/validate_payload.py '<json_payload>'
```

---

## Assets

| File | Purpose |
|:-----|:--------|
| `assets/DynamicComponent.ts` | Base class with signal binding |
| `assets/ComponentRegistry.ts` | Trusted Catalog singleton |
| `assets/ChartWrapper.ts` | Smart Wrapper template |
| `scripts/validate_payload.py` | JSON structure validator |
