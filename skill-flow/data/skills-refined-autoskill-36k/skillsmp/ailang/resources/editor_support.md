# AILANG Editor Support

## VS Code Extension

### Installation

```bash
ailang editor install vscode
```

This installs:
- Syntax highlighting for `.ail` files
- Basic language configuration
- Extension in `~/.vscode/extensions/ailang/`

### Manual Installation

If automatic install fails:

```bash
# Find the extension files
ls ~/.vscode/extensions/ailang/

# Or install from AILANG repo
git clone https://github.com/sunholo-data/ailang
cp -r ailang/editor/vscode ~/.vscode/extensions/ailang
```

### Features

- **Syntax highlighting** for keywords, types, strings, comments
- **File association** for `.ail` files
- **Bracket matching** for `{}`, `[]`, `()`
- **Comment toggling** with `Cmd+/` or `Ctrl+/`

## Vim / Neovim

### Installation

```bash
# Vim
ailang editor install vim

# Neovim
ailang editor install neovim
```

### Manual Installation

```bash
# Vim
mkdir -p ~/.vim/syntax ~/.vim/ftdetect
# Copy syntax/ailang.vim and ftdetect/ailang.vim

# Neovim
mkdir -p ~/.config/nvim/syntax ~/.config/nvim/ftdetect
# Copy syntax/ailang.vim and ftdetect/ailang.vim
```

### Verify Installation

```vim
:set filetype?
" Should show: filetype=ailang
```

## Code Formatting

AILANG does not currently have an official formatter. Follow these conventions:

### Indentation
- Use 2 spaces (not tabs)
- Indent function bodies
- Indent match arms

### Line Length
- Aim for 80-100 characters
- Break long function signatures after `->`

### Example Style

```ailang
module myproject/example

import std/json (decode)
import std/list (map, filter)

type Person = {
  name: string,
  age: int
}

export func greet(person: Person) -> string {
  "Hello, " ++ person.name ++ "!"
}

export func main() -> () ! {IO} {
  let alice = {name: "Alice", age: 30};
  print(greet(alice))
}
```

### Style Guidelines

1. **Module names**: lowercase with slashes (`myproject/utils`)
2. **Type names**: PascalCase (`Person`, `HttpResponse`)
3. **Function names**: camelCase (`getUserById`, `parseJson`)
4. **Constants**: camelCase (`defaultTimeout`)
5. **One blank line** between top-level declarations
6. **No trailing whitespace**

## Language Server (Planned)

A Language Server Protocol (LSP) implementation is planned for future releases, which will enable:
- Autocomplete
- Go to definition
- Hover documentation
- Real-time error checking
- Rename refactoring

Track progress: https://github.com/sunholo-data/ailang/issues

## Troubleshooting

### Syntax highlighting not working

1. Restart your editor after installation
2. Check file extension is `.ail`
3. For VS Code: Check Extensions panel for "AILANG"
4. For Vim: Run `:set filetype?` - should show `ailang`

### Reinstall

```bash
# Remove and reinstall
ailang editor uninstall vscode
ailang editor install vscode
```
