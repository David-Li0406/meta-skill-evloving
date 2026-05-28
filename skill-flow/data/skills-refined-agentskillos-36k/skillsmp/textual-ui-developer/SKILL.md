---
name: textual-ui-developer
description: Develop and improve the MassGen Textual TUI by running it in a browser via textual-serve and using Claude's browser tool for visual feedback.
---

# Textual UI Developer

This skill provides a workflow for developing and improving the MassGen Textual TUI with visual feedback.

## Purpose

Use this skill when you need to:
- Debug or improve the Textual TUI display
- Add new widgets or features to the TUI
- Fix styling or layout issues
- Test the TUI visually in a browser

## For MassGen Agents

When running via MassGen, do NOT use `execute_command` for
long-running servers like textual-serve. The `execute_command` tool blocks
until completion and will timeout.

Instead, use background shell tools:

```python
# Start the server in background
result = start_background_shell("uv run massgen --textual-serve")
shell_id = result["shell_id"]

# Check if it's running
status = get_background_shell_status(shell_id)

# When done, kill it
kill_background_shell(shell_id)
```

Available background shell tools:
- `start_background_shell(command)` - Start a long-running command
- `get_background_shell_status(shell_id)` - Check if still running
- `get_background_shell_output(shell_id)` - Get stdout/stderr
- `kill_background_shell(shell_id)` - Terminate the process
- `list_background_shells()` - List all background shells

## Setup (Claude Code)

### Step 1: Ensure textual-serve is available

The `textual-serve` package should already be installed. If not:

```bash
uv pip install textual-serve
```

### Step 2: Start Claude with Browser Access

Claude Code must be running with Chrome integration:

```bash
claude --chrome
```

### Step 3: Start the Textual TUI Server

Run in background so you can continue working:

```bash
uv run massgen --textual-serve &
```

Or with a specific config:

```bash
uv run massgen --textual-serve --config massgen/configs/basic/three_haiku_default.yaml
```

## Workflow

### Visual Development Loop

1. **Start the server** in background (with optional test prompt):
   ```bash
   # Without prompt (shows welcome screen first)
   uv run massgen --textual-serve &

   # With prompt (auto-submits when launched - faster testing!)
   uv run massgen --textual-serve "What is 2+2?" &
   ```

2. **Open in browser** using browser tools:
   - First call `tabs_context_mcp` to get browser context
   - Navigate to `http://localhost:8000`
   - Click on the landing page card to launch the TUI
   - Wait 2-3 seconds for the app to fully load
   - If you used a prompt, agents will start working immediately!

3. **Take screenshots** at key points:
   - Welcome screen (initial state)
   - After submitting a question (agent panels visible)
   - After agents complete (final state)
   - Modals (press 's', 'o', 'v' to open Status, Events, Votes)

4. **Make changes** to the Textual code:
   - Widget files: `massgen/frontend/displays/textual_widgets/`
   - Main display: `massgen/frontend/displays/textual_terminal_display.py`
   - Themes: `massgen/frontend/displays/textual_themes/`

5. **IMPORTANT - Restart server after changes**:
   CSS and Python changes require restarting the server:
   ```bash
   pkill -f "massgen --textual-serve" && pkill -f "massgen --display textual"
   sleep 2
   uv run massgen --textual-serve &
   ```
   Then open a NEW browser tab to test changes.

### Key Files

| File | Description |
|------|-------------|
| `massgen/frontend/displays/textual_terminal_display.py` | Main Textual app and display logic |
| `massgen/frontend/displays/textual_widgets/` | Custom widgets (tab bar, tool cards, etc.) |
| `massgen/frontend/displays/textual_widgets/tab_bar.py` | Agent tab switching widget |
| `massgen/frontend/displays/textual_widgets/tool_card.py` | Tool call display cards |
| `massgen/frontend/displays/textual_themes/dark.tcss` | Dark theme CSS |
| `massgen/frontend/displays/textual_themes/light.tcss` | Light theme CSS |

### Key Classes in textual_terminal_display.py

| Class | Purpose |
|-------|---------|
| `TextualApp` | Main Textual application, handles compose, keyboard bindings, modals |
| `TextualTerminalDisplay` | Bridge between orchestrator and TextualApp |
| `HeaderWidget` | Top status bar showing agents, turn, question |
| `AgentPanel` | Scrollable panel for agent output with tool cards |
| `WelcomeScreen` | Initial splash screen with logo |
| `BaseModal` | Base class for all modal dialogs |
| `VoteResultsModal`, `OrchestratorEventsModal`, `SystemStatusModal` | Various info modals |

### Commands Reference

```bash
# Start TUI server (default port 8000)
uv run massgen --textual-serve

# Start with a pre-filled prompt (auto-submits when TUI launches!)
uv run massgen --textual-serve "What is 2+2?"

# Start with specific config
uv run massgen --textual-serve --config path/to/config.yaml

# Start with config AND prompt
uv run massgen --textual-serve --config massgen/configs/basic/three_haiku_agents.yaml "Write a haiku"

# Start on different port
uv run massgen --textual-serve --textual-serve-port 9000

# Run TUI directly in terminal (no browser)
uv run massgen --display textual

# Kill all TUI processes
pkill -f "massgen --textual-serve" && pkill -f "massgen --display textual"
```

**Pro tip**: Using `--textual-serve "prompt"` auto-submits the question when you click the landing page card, saving time during iterative testing!

## Keyboard Shortcuts

When the TUI is running:
- `s` - Open System Status modal
- `o` - Open Orchestrator Events modal
- `v` - Open Voting Breakdown modal
- `q` - Quit the application
- `1-9` - Switch to agent by number
- `Tab` / `Shift+Tab` - Cycle through agents
- `Ctrl+P` - Open command palette
- `ESC` - Close modals (may require clicking Close button in browser)

## Tips

1. **Hot reload limitations**: textual-serve spawns new instances per connection, but Python code changes require server restart.

2. **CSS changes**: Both `dark.tcss` and `light.tcss` need updating for theme consistency.

3. **Check the console**: The terminal running textual-serve shows Python errors and tracebacks.

4. **Browser limitations**: Some keyboard shortcuts (like ESC) may not work properly in textual-serve browser mode. The Close button always works.

5. **High CPU warning**: Complex tasks with many tool calls can cause high CPU usage. Use simple test prompts like "What is 2+2?" for quick UI testing.

6. **Test prompts**:
   - Simple: "What is 2+2?" (no tools, fast)
   - With tools: "Create a poem and write it to a file" (uses filesystem tools)
   - Complex: "Search the web for X" (longer running)

7. **Tab switching**: Click directly on agent tabs or use number keys (1, 2, 3...) to switch between agents.

## Common Issues

### Server not reflecting changes
**Solution**: Kill and restart the server, then open a new browser tab.

### ESC key not closing modals
**Cause**: Browser captures ESC before textual-serve.
**Solution**: Click the "Close (ESC)" button instead.

### Agents stuck on "Waiting for agent..."
**Cause**: MCP server initialization can take time.
**Solution**: Wait 5-10 seconds, or check terminal for errors.

### High CPU usage
**Cause**: Complex tool-using tasks or busy loops.
**Solution**: Use `pkill -9 -f "massgen"` to force kill, then restart.

## Textual Resources

- **Textual Docs**: https://textual.textualize.io/
- **Widget Gallery**: https://textual.textualize.io/widget_gallery/
- **CSS Reference**: https://textual.textualize.io/css_types/
- **textual-serve Repo**: https://github.com/Textualize/textual-serve
