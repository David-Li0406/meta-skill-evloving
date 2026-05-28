---
name: create-svg-component
description: Use this skill when you need to create dynamic SVG components with state-based styling and precise layout control.
---

# SVG Component Creation

This skill allows you to create dynamic SVG components that can be styled based on their state. You can control colors using CSS variables and define gradients for visual effects.

## When to Use This Skill

Use this skill when you need to create SVG diagrams or components that require dynamic styling based on different states, such as success, warning, or error states.

## Core Principles

1. Define gradients in the SVG `<defs>` section.
2. Use CSS selectors to control the fill based on the `data-status` attribute.
3. Change the status in JavaScript to trigger CSS updates without replacing innerHTML.

## ⚠️ Prerequisites

Before starting, ensure you have read the following documents:

1. [Architecture Overview](RNBT_architecture/README.md)
2. [Coding Style Guide](.claude/guides/CODING_STYLE.md)

## Input/Output Structure

**Input:** `Figma_Conversion/Static_Components/[ProjectName]/[ComponentName]/`

**Output:**
```
components/[ComponentName]/
├── views/component.html       # SVG + gradients + layer classes
├── styles/component.css       # CSS for [data-status] selectors
├── scripts/
│   ├── register.js            # setStatus, getStatus API
│   └── beforeDestroy.js
├── preview.html
└── README.md
```

## Layer Class Naming Conventions

| Class                | Purpose                |
|----------------------|-----------------------|
| `layer-grad0` ~ `layer-grad9` | Gradient fill         |
| `layer-fill-primary` | Primary solid color    |
| `layer-fill-secondary` | Secondary solid color  |
| `layer-stroke`      | Outline                |

## Key API Functions

```javascript
// Change status - only updates the data-status attribute
function setStatus(config, status) {
    container.dataset.status = status;  // CSS controls color
    this._currentStatus = status;
}

// Get current status
function getStatus() {
    return this._currentStatus;
}
```

## Prohibited Practices

- ❌ Changing colors by replacing innerHTML
- ❌ Mismatched creation/cleanup
- ❌ Using `function(response)` → must use `function({ response })`

## Related Resources

| Reference | Location |
|-----------|----------|
| Example   | [Symbol Test Project](RNBT_architecture/Projects/Symbol_Test/page/components/Cube3DSymbol/) |