---
name: lua-standard
description: "Lua/Neovim coding standards. Use when: writing or reviewing Lua code (*.lua) for Neovim plugins or configuration."
---

# Lua/Neovim Standard

## 1. Scoping & Variables

- **Always use `local`**: Never pollute global namespace
- **Stateless modules**: Avoid module-scope mutable state; pass dependencies as arguments
- **Use `vim.g` / `vim.b` intentionally**: Only for Vim options, not general state

## 2. Type Annotations (LuaCATS)

Required annotations for functions:

- `---@param name type`
- `---@return type`

Example:
```lua
---@param opts { silent?: boolean, desc: string }
---@return nil
local function setup_keymap(opts)
end
```

## 3. Naming Conventions

- **Variables/Functions**: `snake_case`
- **Boolean**: `is_`, `has_`, `can_` prefix
- **Constants**: `SCREAMING_SNAKE_CASE`
- **Private functions**: `_` prefix

## 4. Neovim API Best Practices

- **Keymaps must have `desc`**: Required for which-key discoverability
- **Use `<Plug>` mappings**: In plugins, expose for user customization
- **Prefer `vim.keymap.set`**: Over `vim.api.nvim_set_keymap`
- **Use `vim.notify`**: Over `print()` for user messages

## 5. Error Handling

- **Use `pcall` / `xpcall`**: For operations that may fail
- **Early returns**: Check preconditions first
- **Validate inputs**: Check nil before operations

## 6. Module Pattern

```lua
local M = {}

function M.public_function()
end

local function private_helper()
end

return M
```

## 7. Performance

- **Cache requires**: Store at module top
- **Prefer `vim.uv`**: Over `vim.fn` for filesystem

## 8. Review Checklist

1. Global variables → add `local`
2. Missing LuaCATS annotations → add `---@param` / `---@return`
3. Keymaps without `desc` → require description
4. `print()` for messages → use `vim.notify`
5. Missing error handling for IO → add `pcall`
6. Deprecated APIs → suggest modern alternatives
7. Non-snake_case naming → rename
8. Module-level mutable state → refactor
