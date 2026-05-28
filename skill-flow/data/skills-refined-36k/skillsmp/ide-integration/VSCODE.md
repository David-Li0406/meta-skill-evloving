# VS Code Integration

Complete guide for integrating Claude Code with Visual Studio Code.

## Initial Setup

### 1. Install VS Code CLI

Ensure the `code` command is available:

```bash
# macOS: Open Command Palette (Cmd+Shift+P)
# Type: "Shell Command: Install 'code' command in PATH"

# Verify installation
code --version
```

### 2. Configure Claude Code Editor

```bash
# Set VS Code as default editor
export CLAUDE_CODE_EDITOR="code"

# Add to ~/.zshrc or ~/.bashrc for persistence
echo 'export CLAUDE_CODE_EDITOR="code"' >> ~/.zshrc
```

## Recommended Extensions

### Essential for Claude Code Workflow

| Extension | Purpose | Install |
|-----------|---------|---------|
| GitLens | Enhanced git blame, history | `code --install-extension eamodio.gitlens` |
| Error Lens | Inline error display | `code --install-extension usernamehw.errorlens` |
| Todo Tree | Track Claude's TODO comments | `code --install-extension gruntfuggly.todo-tree` |
| Diff Viewer | Better diff visualization | Built-in, use Source Control |

### Language-Specific

```bash
# Install common extensions
code --install-extension dbaeumer.vscode-eslint
code --install-extension esbenp.prettier-vscode
code --install-extension ms-python.python
code --install-extension bradlc.vscode-tailwindcss
```

### Install All Recommended

```bash
# Install essential extensions for Claude Code workflow
code --install-extension eamodio.gitlens
code --install-extension usernamehw.errorlens
code --install-extension gruntfuggly.todo-tree
code --install-extension streetsidesoftware.code-spell-checker
```

## Integrated Terminal Configuration

### Terminal Profiles (settings.json)

```json
{
  "terminal.integrated.profiles.osx": {
    "Claude Code": {
      "path": "zsh",
      "args": ["-l"],
      "env": {
        "CLAUDE_INTEGRATED": "true"
      }
    }
  },
  "terminal.integrated.defaultProfile.osx": "Claude Code"
}
```

### Split Terminal Layout

```json
{
  "terminal.integrated.splitCwd": "inherited",
  "terminal.integrated.tabs.enabled": true,
  "terminal.integrated.tabs.location": "right"
}
```

## Keybindings

### Recommended Keybindings (keybindings.json)

```json
[
  {
    "key": "cmd+shift+c",
    "command": "workbench.action.terminal.new",
    "when": "!terminalFocus"
  },
  {
    "key": "cmd+\\",
    "command": "workbench.action.terminal.split",
    "when": "terminalFocus"
  },
  {
    "key": "cmd+shift+\\",
    "command": "workbench.action.togglePanel"
  },
  {
    "key": "cmd+k cmd+d",
    "command": "git.openChange"
  },
  {
    "key": "cmd+shift+g g",
    "command": "workbench.view.scm"
  }
]
```

### Essential Default Shortcuts

| Action | macOS | Windows/Linux |
|--------|-------|---------------|
| Toggle terminal | Ctrl+` | Ctrl+` |
| New terminal | Ctrl+Shift+` | Ctrl+Shift+` |
| Split terminal | Cmd+\ | Ctrl+Shift+5 |
| Toggle sidebar | Cmd+B | Ctrl+B |
| Source control | Ctrl+Shift+G | Ctrl+Shift+G |
| Quick open | Cmd+P | Ctrl+P |
| Go to symbol | Cmd+Shift+O | Ctrl+Shift+O |
| Find in files | Cmd+Shift+F | Ctrl+Shift+F |

## Diff Viewing Workflow

### 1. Source Control Panel

```
Cmd+Shift+G  - Open Source Control
Click file   - View diff inline
Right-click  - Open to side, discard, stage options
```

### 2. Timeline View

```
1. Open a file
2. View > Open View... > Timeline
3. See file history and Claude's changes
```

### 3. GitLens Features

```
# Inline blame (shows who/when for each line)
GitLens: Toggle File Blame  (Alt+B)

# Line history
GitLens: Show Line History

# Compare with previous
GitLens: Compare with Previous Revision
```

## File Watcher Settings

VS Code auto-reloads by default. Configure behavior:

```json
{
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  "files.watcherExclude": {
    "**/node_modules/**": true,
    "**/.git/**": true
  }
}
```

## Workspace Settings for Claude Projects

Create `.vscode/settings.json` in your project:

```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": "explicit",
    "source.organizeImports": "explicit"
  },
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "terminal.integrated.cwd": "${workspaceFolder}",
  "git.enableSmartCommit": true,
  "git.confirmSync": false
}
```

## Tasks for Claude Workflows

Create `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Watch Tests",
      "type": "shell",
      "command": "bun test --watch",
      "group": "test",
      "presentation": {
        "reveal": "always",
        "panel": "dedicated"
      }
    },
    {
      "label": "Dev Server",
      "type": "shell",
      "command": "bun dev",
      "group": "build",
      "presentation": {
        "reveal": "always",
        "panel": "dedicated"
      }
    },
    {
      "label": "Type Check",
      "type": "shell",
      "command": "bun run typecheck",
      "group": "build",
      "problemMatcher": ["$tsc"]
    }
  ]
}
```

Run tasks: `Cmd+Shift+P > Tasks: Run Task`

## Terminal Split Layout

### Optimal Layout for Claude Code

1. **Full-width terminal panel** (bottom)
2. **Split into 2-3 panes**:
   - Left: Claude Code session
   - Middle: Dev server / watch
   - Right: Ad-hoc commands

### Setup with Commands

```bash
# In VS Code terminal:
# Ctrl+` to open terminal
# Cmd+\ to split
# Repeat for desired layout
```

### Layout Preset (Workspace)

```json
{
  "terminal.integrated.tabs.enabled": true,
  "terminal.integrated.defaultLocation": "bottom",
  "workbench.panel.defaultLocation": "bottom"
}
```

## Clipboard Integration

### Copy File Path

```
Right-click file > Copy Path           # Full path
Right-click file > Copy Relative Path  # Project-relative

# Keyboard shortcuts
Cmd+K P  - Copy path of active file
```

### Copy Code to Claude

```
1. Select code
2. Cmd+C to copy
3. Paste in Claude terminal with context:
   "Here's the code from src/utils.ts:
   <paste>"
```

### Copy Claude Output to Editor

```
1. Select output in terminal
2. Cmd+C
3. Navigate to file
4. Cmd+V
```

## Multi-Root Workspaces

For projects across multiple directories:

Create `project.code-workspace`:

```json
{
  "folders": [
    { "path": "./frontend" },
    { "path": "./backend" },
    { "path": "./shared" }
  ],
  "settings": {
    "terminal.integrated.cwd": "${workspaceFolder:frontend}"
  }
}
```

Open: `File > Open Workspace from File...`

## Troubleshooting

### Terminal Not Showing Claude Changes

```json
{
  "files.useExperimentalFileWatcher": true,
  "files.watcherExclude": {}
}
```

### High CPU from File Watcher

```json
{
  "files.watcherExclude": {
    "**/node_modules/**": true,
    "**/dist/**": true,
    "**/.git/objects/**": true
  }
}
```

### Terminal Colors Wrong

```json
{
  "terminal.integrated.env.osx": {
    "TERM": "xterm-256color"
  }
}
```

### Slow Git Diff for Large Files

```json
{
  "git.decorations.enabled": false,
  "gitlens.hovers.enabled": false
}
```

## Quick Commands Cheat Sheet

| Action | Command Palette |
|--------|----------------|
| Reload window | Developer: Reload Window |
| Open settings JSON | Preferences: Open Settings (JSON) |
| Open keybindings | Preferences: Open Keyboard Shortcuts (JSON) |
| Toggle word wrap | View: Toggle Word Wrap |
| Compare active file | File: Compare Active File With... |
| Open recent | File: Open Recent |

## Example Workflow Session

```
1. Open VS Code in project
   $ code /path/to/project

2. Open integrated terminal
   Ctrl+`

3. Split terminal for Claude
   Cmd+\

4. Start Claude Code in right pane
   $ claude

5. Work with Claude, switch to left pane for commands
   Cmd+[  (or click pane)

6. Review changes in Source Control
   Cmd+Shift+G

7. View specific file diff
   Click modified file in Source Control

8. Commit approved changes
   Ask Claude or use Git panel
```
