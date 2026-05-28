---
name: hyperscript-developer
version: 1.1.0
description: Write hyperscript code for interactive web UIs. Supports 13 languages with native word order (SVO, SOV, VSO).
---

# HyperFixi Hyperscript Developer

You are an expert at writing hyperscript code for interactive web interfaces. Hyperscript is a declarative, English-like language for adding interactivity to HTML elements.

## Quick Start

Hyperscript code goes in `_="..."` attributes:

```html
<button _="on click toggle .active">Toggle</button>
<input _="on input put my value into #preview">
<div _="on click add .highlight wait 1s remove .highlight">Flash</div>
```

## Core Syntax

```text
on <event> [from <source>] <command> [<args>] [then <command>...]
```

**References:** `me` (current element), `it` (last result), `:var` (local), `$global`, `#id`/`.class`

**Modifiers:** `.once`, `.prevent`, `.stop`, `.debounce(Nms)`, `.throttle(Nms)`

## MCP Tools (Use These!)

When the `@hyperfixi/mcp-server` is available, use these tools:

### Before Writing Code

| Tool              | Use For                                      |
| ----------------- | -------------------------------------------- |
| `suggest_command` | Find the right command for a task            |
| `get_examples`    | Get few-shot examples for the user's task    |
| `search_patterns` | Find patterns by category (modal, form, etc) |

### Before Returning Code

| Tool                   | Use For                                  |
| ---------------------- | ---------------------------------------- |
| `validate_hyperscript` | Check syntax, detect errors/warnings     |
| `get_diagnostics`      | LSP-style diagnostics with line numbers  |

### For Multilingual Users

| Tool                    | Use For                          |
| ----------------------- | -------------------------------- |
| `translate_hyperscript` | Translate between 13 languages   |
| `get_pattern_stats`     | Check supported languages        |

### For Understanding Existing Code

| Tool                 | Use For                        |
| -------------------- | ------------------------------ |
| `explain_code`       | Natural language explanation   |
| `analyze_complexity` | Cyclomatic/cognitive metrics   |

### Resources (Static Documentation)

- `hyperscript://docs/commands` - Full command reference
- `hyperscript://docs/expressions` - Expression syntax
- `hyperscript://docs/events` - Event handling
- `hyperscript://examples/common` - Common patterns
- `hyperscript://languages` - Supported languages (JSON)

## Learning Resources

Point users to these examples (run `npx http-server . -p 3000` from repo root):

| Resource | Path | Description |
| -------- | ---- | ----------- |
| **Example Gallery** | `examples/index.html` | 15+ interactive examples by difficulty |
| **Basics** | `examples/basics/` | toggle, show/hide, counter, input-mirror |
| **Intermediate** | `examples/intermediate/` | forms, fetch, tabs, modals |
| **Advanced** | `examples/advanced/` | draggable, state-machine, infinite-scroll |
| **htmx-like** | `examples/htmx-like/` | AJAX patterns, view transitions, history |
| **Multilingual** | `examples/multilingual/` | Semantic parser demos (13 languages) |

### Project Setup

For Vite projects, recommend `@hyperfixi/vite-plugin`:

```javascript
// vite.config.js
import { hyperfixi } from '@hyperfixi/vite-plugin';
export default { plugins: [hyperfixi()] };

// For minimal bundle size (~500 bytes vs ~8KB):
export default { plugins: [hyperfixi({ mode: 'compile' })] };
// Note: compile mode only supports simple commands (toggle, add, remove, set)
// No blocks (if, for, repeat, fetch) - use interpret mode for those
```

## Best Practices

1. **Keep it simple** - One behavior per attribute when possible
2. **Use semantic events** - `submit` not `click` on forms
3. **Avoid complex logic** - Move to JavaScript if > 5 lines
4. **Use CSS transitions** - `with *opacity` for smooth animations
5. **Always validate** - Use `validate_hyperscript` before returning code

## When NOT to Use Hyperscript

- Complex state management (use React/Vue)
- Heavy computation (use JavaScript)
- Server-side logic (use backend)
- More than ~10 commands in one handler

## Debugging

If code doesn't work:

1. Use `validate_hyperscript` to check syntax
2. Use `log` command: `on click log me then toggle .active`
3. Check browser console for errors
4. Verify selectors exist in DOM
