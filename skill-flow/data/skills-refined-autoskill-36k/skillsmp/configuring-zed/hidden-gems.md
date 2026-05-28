# Zed Hidden Gems

Source: [Part 1](https://zed.dev/blog/hidden-gems-team-edition-part-1), [Part 2](https://zed.dev/blog/hidden-gems-part-2).

## Vim: Toggle dbg!() Wrapper (Rust)

Keybindings to wrap/unwrap Rust expressions with `dbg!()`:

```json
{
  "context": "vim_mode == visual",
  "bindings": {
    "\\ d": ["workspace::SendKeystrokes", "\" a s dbg!( ctrl-r a ) escape"]
  }
},
{
  "context": "vim_mode == normal",
  "bindings": {
    "\\ d": ["workspace::SendKeystrokes", "v a a \" a y g v [ x [ x \" a p"]
  }
}
```

Visual mode `\d` wraps selection. Normal mode `\d` removes wrapper when cursor inside.

## Prose-Writing Focus Mode

Three commands in sequence:
1. `workspace: close all docks` - removes all panels
2. `workspace: close inactive tabs and panes` - cleans workspace
3. `workspace: toggle centered layout` - centers remaining pane with narrow column

## Select All Regex Matches

1. `buffer search: deploy`
2. Enable regex mode
3. Enter pattern
4. `alt-enter` (or click button) creates cursor at every match

## Split Selection into Line Cursors

`editor: split selection into lines` - places a cursor on each line of selection for bulk edits.

## Autosave on Terminal Switch

```json
{ "autosave": "on_focus_change" }
```

Files save when switching from editor to terminal - tests always run against latest code.

## Outline Modal with Context Filtering

`cmd-shift-O` opens outline. Add spaces to filter by context:
- `pub fn` - public functions only
- `trait ` (trailing space) - trait definitions
- `impl Foo for` - trait implementations for Foo

## Open Files in New Pane

Hold `cmd` (macOS) / `ctrl` (Linux/Windows) when opening from project panel or file finder. File opens in new right-hand pane instead of replacing current.

For go-to-definition: hold `alt` + `cmd`/`ctrl`.

## Lazygit as Task

`~/.config/zed/tasks.json`:
```json
{
  "label": "LazyGit",
  "command": "lazygit",
  "shell": { "program": "sh" },
  "hide": "on_success",
  "reveal_target": "center",
  "show_summary": false,
  "show_command": false,
  "allow_concurrent_runs": true,
  "use_new_terminal": true
}
```

Keybinding (`keymap.json`):
```json
"cmd-shift-g": [
  "task::Spawn",
  { "task_name": "LazyGit", "reveal_target": "center" }
]
```

## Edit Task Commands Before Running

In task modal:
- `tab` expands task into editable command (add env vars, flags)
- `alt-enter` runs as oneshot task, saves to history for reuse

## Bun Test Gutter Buttons

`tasks.json`:
```json
{
  "label": "Bun Test",
  "command": "bun test",
  "args": ["\"$ZED_RELATIVE_FILE\" -t=\"$ZED_SYMBOL\""],
  "tags": ["js-test", "ts-test", "bun-test", "tsx-test"]
}
```

Play buttons appear in gutter next to tests. Requires `@types/bun` in project or this config.

## Television as Telescope-style File Finder

Install [television](https://github.com/alexpasmantier/television), then:

`tasks.json`:
```json
{
  "label": "Television File Finder",
  "command": "zed \"$(tv files)\"",
  "hide": "always",
  "allow_concurrent_runs": true,
  "use_new_terminal": true
}
```

`keymap.json` (override default file finder):
```json
{
  "bindings": {
    "cmd-p": [
      "task::Spawn",
      { "task_name": "Television File Finder", "reveal_target": "center" }
    ]
  }
}
```

## Auto-Attach to Project tmux Session

`settings.json`:
```json
"terminal": {
  "shell": {
    "with_arguments": {
      "program": "/bin/zsh",
      "args": ["-c", "tmux new-session -A -s \"$(basename \"$PWD\")\""]
    }
  }
}
```

Terminal auto-attaches to tmux session named after project directory. `-A` creates if missing.

## Map Unknown File Extensions to Languages

Temporary: `language selector: toggle` in command palette, pick language (resets on close).

Permanent (`settings.json`):
```json
"file_types": { "JavaScript": ["*.jsm"] }
```

## File Icons in Tabs

```json
"tabs": { "file_icons": true }
```

Or navigate to `zed://settings/tabs.file_icons` in command palette.

## Task Variables

- `$ZED_RELATIVE_FILE` - current file path relative to project
- `$ZED_SYMBOL` - selected symbol/function name
