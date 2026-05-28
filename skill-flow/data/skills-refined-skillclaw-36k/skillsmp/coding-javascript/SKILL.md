---
name: coding-javascript
description: Apply this skill when generating JavaScript (JS) code
---

## Style

Python code should generally follow the style conventions of the StandardJS.

All code should match `prettier` formatting with the following config:

```json
{
  "semi": false,
  "singleQuote": true,
  "printWidth": 120,
  "bracketSameLine": true,
  "arrowParens": "avoid"
}
```

## Comments

Comments should never be added to generated code.

## Functions

Favor pure functions whenever possible.
