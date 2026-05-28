# JetBrains IDE Integration

Integration guide for IntelliJ IDEA, WebStorm, PyCharm, and other JetBrains IDEs with Claude Code.

## Supported IDEs

| IDE | Best For | CLI Command |
|-----|----------|-------------|
| IntelliJ IDEA | Java, Kotlin, Scala | `idea` |
| WebStorm | JavaScript, TypeScript | `webstorm` |
| PyCharm | Python | `pycharm` |
| RubyMine | Ruby, Rails | `rubymine` |
| GoLand | Go | `goland` |
| PhpStorm | PHP | `phpstorm` |
| CLion | C, C++ | `clion` |
| Rider | .NET, C# | `rider` |
| DataGrip | Databases | `datagrip` |

## Initial Setup

### 1. Install Command Line Launcher

```
Tools > Create Command-line Launcher...

# Default locations:
# macOS: /usr/local/bin/idea (or webstorm, pycharm, etc.)
# Linux: ~/bin/idea
# Windows: Added to PATH during installation
```

### 2. Verify Installation

```bash
# Test CLI launcher
webstorm --version
idea --version
pycharm --version
```

### 3. Configure Claude Code Editor

```bash
# Set JetBrains IDE as editor
export CLAUDE_CODE_EDITOR="webstorm"  # or idea, pycharm, etc.

# Add to shell config
echo 'export CLAUDE_CODE_EDITOR="webstorm"' >> ~/.zshrc
```

## Terminal Integration

### External Terminal (Recommended)

JetBrains built-in terminal works but external terminal is often smoother:

1. Open external terminal (iTerm2, Terminal.app, etc.)
2. Navigate to project directory
3. Run `claude` in external terminal
4. Use IDE for editing and reviewing

### Built-in Terminal Split

If using built-in terminal:

```
1. View > Tool Windows > Terminal
2. Click "+" to add terminal tab
3. Right-click tab > Split Vertically
4. Run Claude in one pane, commands in other
```

### Terminal Settings

```
Settings > Tools > Terminal
- Shell path: /bin/zsh (macOS) or /bin/bash
- Tab name: "Claude" for Claude session
- Environment variables: Add ANTHROPIC_API_KEY if needed
```

## File Watcher Configuration

### Enable Auto-Reload

```
Settings > Appearance & Behavior > System Settings
- [x] Synchronize files on frame activation
- [x] Save files on frame deactivation
```

### External Changes Detection

```
Settings > Appearance & Behavior > System Settings
- [x] Synchronize files on frame activation (CHECK THIS)
- [x] Save files on frame deactivation
```

Force refresh: `File > Reload All from Disk` or `Ctrl+Alt+Y`

## Diff and Version Control

### View Local Changes

```
View > Tool Windows > Git (or Alt+9)
- Local Changes tab shows all modifications
- Double-click file to see diff
- Right-click for stage, revert options
```

### Diff Viewer Features

| Action | Shortcut | Description |
|--------|----------|-------------|
| Compare with branch | Right-click > Git > Compare with Branch | Compare file with any branch |
| Show history | Right-click > Git > Show History | File history timeline |
| Annotate | Right-click > Git > Annotate | Blame view in gutter |
| Compare clipboard | Right-click > Compare with Clipboard | Diff clipboard content |

### Inline Diff

```
1. Open modified file
2. Click colored marker in gutter (left side)
3. See inline diff of that change
4. Rollback individual changes from there
```

## Keybindings for Claude Workflow

### Essential Shortcuts

| Action | macOS | Windows/Linux |
|--------|-------|---------------|
| Open terminal | Alt+F12 | Alt+F12 |
| New terminal tab | Cmd+T (in terminal) | - |
| Navigate to file | Cmd+Shift+O | Ctrl+Shift+N |
| Recent files | Cmd+E | Ctrl+E |
| Git tool window | Cmd+9 | Alt+9 |
| Commit dialog | Cmd+K | Ctrl+K |
| Update project (git pull) | Cmd+T | Ctrl+T |
| Reload from disk | Cmd+Alt+Y | Ctrl+Alt+Y |
| Find in files | Cmd+Shift+F | Ctrl+Shift+F |
| Find action | Cmd+Shift+A | Ctrl+Shift+A |

### Custom Keymaps

```
Settings > Keymap > search for action > Right-click > Add Keyboard Shortcut
```

Recommended custom bindings:

| Action | Suggested Binding |
|--------|------------------|
| Compare with Clipboard | Cmd+Alt+V |
| Rollback Lines | Cmd+Alt+Z |
| Show Diff | Cmd+D (in Git view) |

## Project Setup for Claude

### Run Configurations

Create run configurations for common tasks:

```
Run > Edit Configurations > + > npm/Bun

Name: Dev Server
Command: run
Scripts: dev

Name: Tests
Command: test
Scripts: test
```

### Scopes for Search

Limit searches to relevant files:

```
Settings > Appearance & Behavior > Scopes > +

Name: Source Files
Pattern: file:src//*&&!file:*.test.*&&!file:*node_modules*
```

Use in Find in Files: `Ctrl+Shift+F > Scope dropdown > Source Files`

## Clipboard Integration

### Copy Path

```
Right-click file/tab > Copy Path/Reference...
- Absolute Path
- Path from Project Root
- File Name
```

Shortcut: `Cmd+Shift+C` (copy absolute path)

### Copy as Rich Text

For sharing formatted code:

```
Select code > Right-click > Copy as Rich Text
```

### Paste from History

```
Cmd+Shift+V (macOS) / Ctrl+Shift+V (Win/Linux)
- Shows clipboard history
- Useful for pasting multiple Claude outputs
```

## Live Templates for Claude

Create snippets for common Claude prompts:

```
Settings > Editor > Live Templates > + Group (Claude)

Abbreviation: ccfix
Template: Look at $FILE$ and fix: $ISSUE$
Variables:
  - FILE: currentFilePath()
  - ISSUE: (empty for user input)
```

Usage: Type `ccfix` + Tab in any file

### Example Templates

| Abbreviation | Template |
|-------------|----------|
| `ccreview` | Review $FILE$ for issues and improvements |
| `cctest` | Add tests for $FUNCTION$ in $FILE$ |
| `ccrefactor` | Refactor $SELECTION$ to be more readable |
| `ccdoc` | Add documentation to $FILE$ |

## External Tools Integration

### Claude Code as External Tool

```
Settings > Tools > External Tools > +

Name: Open in Claude
Program: claude
Arguments: --print "$FilePath$"
Working directory: $ProjectFileDir$
```

Access via: `Tools > External Tools > Open in Claude`

Or add keyboard shortcut in Keymap settings.

### File Watchers for Auto-lint

```
Settings > Tools > File Watchers > +

File type: TypeScript
Scope: Project Files
Program: bun
Arguments: run lint --fix $FilePath$
```

## Split View Workflows

### Vertical Split (Side by Side)

```
Right-click tab > Split Right
- Left: Code you're reviewing
- Right: Related file or test
```

### Horizontal Split (Top/Bottom)

```
Right-click tab > Split Down
- Top: Main file
- Bottom: Terminal output or related file
```

### Useful Split Patterns

| Pattern | Use Case |
|---------|----------|
| Code + Test | View implementation and tests together |
| File + Git Diff | See changes in context |
| Multiple Files | Compare implementations |

## Database Integration (DataGrip/Database Tool)

If Claude modifies database schemas:

```
View > Tool Windows > Database

1. Add data source
2. Refresh after Claude runs migrations
3. View table structures, run queries
4. Compare schema changes
```

## Performance Optimization

### Large Projects

```
Settings > Editor > General > Editor Tabs
- Tab limit: 10
- [x] Close tabs to the left

Settings > System Settings
- [ ] Synchronize files on frame activation (disable if slow)
```

### Memory Settings

Edit `idea.vmoptions` (Help > Edit Custom VM Options):

```
-Xms512m
-Xmx2048m
-XX:ReservedCodeCacheSize=512m
```

## Troubleshooting

### Files Not Updating After Claude Edits

1. Check file watcher: `Ctrl+Alt+Y` to force reload
2. Enable sync on frame activation (Settings > System Settings)
3. Check if file is set to read-only

### Terminal Not Finding Commands

```
Settings > Tools > Terminal > Environment variables
Add: PATH=/usr/local/bin:$PATH
```

### Slow Git Operations

```
Settings > Version Control > Git
- [ ] Show Console (disable for speed)
- [x] Use Shell Scripts (faster on some systems)
```

### IDE Freezes During Large Diffs

```
Settings > Version Control > Commit
- [ ] Run inspections before commit
- [ ] Check TODO before commit
```

## Example Session Workflow

```
1. Open project in JetBrains IDE
   $ webstorm /path/to/project

2. Open external terminal and navigate to project
   $ cd /path/to/project

3. Start Claude Code
   $ claude

4. Work with Claude, making changes

5. Switch to IDE (Cmd+Tab)

6. Reload files if needed (Cmd+Alt+Y)

7. Review changes in Git tool window (Cmd+9)

8. Double-click files to see diffs

9. Stage approved changes

10. Return to Claude for more work or commit
```

## IDE-Specific Notes

### WebStorm

- Excellent TypeScript support
- Run configurations work well with Bun
- Use "Mark as Plain Text" for generated files Claude shouldn't index

### IntelliJ IDEA

- For polyglot projects, Ultimate edition recommended
- Database tools built-in
- Consider "Power Save Mode" when not actively editing

### PyCharm

- Virtual environment detection automatic
- Python console useful alongside Claude
- Scientific mode for data projects
