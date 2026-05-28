---
name: tui-development
description: Develop, test, and debug TUI (Terminal User Interface) applications using tmux. Use when building TUI apps, testing terminal rendering, debugging UI issues, capturing screenshots, or validating visual changes in an AI agent development loop.
allowed-tools:
  - Bash(tmux:*)
  - Bash(freeze:*)
  - Bash(cat:*)
  - Bash(diff:*)
  - Bash(sleep:*)
  - Bash(kill:*)
  - Bash(pgrep:*)
  - Bash(pkill:*)
  - Bash(cargo:*)
  - Bash(go:*)
  - Bash(npm:*)
  - Bash(npx:*)
  - Bash(python:*)
  - Bash(node:*)
  - Read
  - Write
  - Glob
---

# TUI Development Workflow for AI Agents

Develop, test, and validate Terminal User Interface applications using tmux as your "headless browser" for terminals.

## Philosophy

TUI development presents unique challenges for AI agents: the output is visual and not easily parseable. This skill enables a **visual verification loop**:

1. Make code changes
2. Run the TUI in a controlled tmux environment
3. Capture and analyze the visual output
4. Determine if changes achieved the desired effect

tmux serves as the equivalent of a headless browser for terminal applications—it provides a controlled, scriptable environment to run and interact with TUIs without requiring a physical terminal.

---

## Prerequisites

```bash
# Install freeze (Charm's terminal screenshot tool)
brew install charmbracelet/tap/freeze

# Verify tmux is available
which tmux
```

---

## 1. tmux Fundamentals

### Session Management

```bash
# Create a detached session with specific dimensions
tmux new-session -d -s <session-name> -x <cols> -y <rows> '<command>'

# List sessions
tmux list-sessions

# Attach to session (for debugging)
tmux attach-session -t <session-name>

# Kill session
tmux kill-session -t <session-name>

# Kill all sessions (cleanup)
tmux kill-server
```

### Terminal Environment

Set these environment variables for proper TUI rendering:

```bash
TERM=xterm-256color        # 256 color support
COLORTERM=truecolor        # 24-bit color support
LANG=en_US.UTF-8           # Unicode support
LC_ALL=en_US.UTF-8

# Full example
tmux new-session -d -s tui -x 120 -y 40 \
  'TERM=xterm-256color COLORTERM=truecolor ./my-tui-app'
```

### Size Guidelines

| Use Case | Size | Flags |
|----------|------|-------|
| Standard TUI | 80x24 | `-x 80 -y 24` |
| Wide tables/dashboards | 120x40 | `-x 120 -y 40` |
| Full-screen TUI | 160x50 | `-x 160 -y 50` |
| Mobile/narrow testing | 60x20 | `-x 60 -y 20` |
| Documentation screenshots | 100x30 | `-x 100 -y 30` |

---

## 2. Running TUI Applications

### Basic Patterns

```bash
# Run a binary
tmux new-session -d -s app -x 80 -y 24 './my-tui-app'

# With build step (Rust)
cargo build --release && \
  tmux new-session -d -s app -x 80 -y 24 './target/release/my-tui'

# With arguments
tmux new-session -d -s app -x 80 -y 24 './my-app --config config.toml'

# From specific directory
tmux new-session -d -s app -x 80 -y 24 -c /path/to/project './app'
```

### Language-Specific Examples

```bash
# Rust (ratatui, crossterm)
cargo run --release

# Go (bubbletea, tview)
go run .

# Python (textual, rich)
python -m myapp

# Node.js (blessed, ink)
npx tsx ./src/app.tsx
```

### Handling Startup Time

```bash
# Fixed delay (simple)
sleep 2

# Poll for specific content (more reliable)
for i in {1..30}; do
  tmux capture-pane -t app -p | grep -q "Ready" && break
  sleep 0.1
done

# Wait for any content to appear
until tmux capture-pane -t app -p 2>/dev/null | grep -q .; do
  sleep 0.1
done
```

---

## 3. Interacting with TUI Applications

### send-keys Basics

```bash
# Send literal text
tmux send-keys -t <target> 'text'

# Send special keys
tmux send-keys -t app Enter
tmux send-keys -t app Escape
tmux send-keys -t app Tab
tmux send-keys -t app Space
tmux send-keys -t app BSpace    # Backspace
```

### Key Reference

| Action | tmux Key |
|--------|----------|
| Enter/Return | `Enter` |
| Escape | `Escape` |
| Tab | `Tab` |
| Shift+Tab | `S-Tab` or `BTab` |
| Backspace | `BSpace` |
| Delete | `DC` |
| Home | `Home` |
| End | `End` |
| Page Up | `PgUp` |
| Page Down | `PgDn` |
| Arrow keys | `Up`, `Down`, `Left`, `Right` |
| Function keys | `F1` through `F12` |
| Ctrl+key | `C-<key>` (e.g., `C-c`, `C-a`) |
| Alt+key | `M-<key>` (e.g., `M-x`) |
| Ctrl+Alt+key | `C-M-<key>` |

### Timing Between Actions

```bash
# Bad: no delay
tmux send-keys -t app 'j' && tmux send-keys -t app Enter

# Good: small delay for TUI to process
tmux send-keys -t app 'j'
sleep 0.1
tmux send-keys -t app Enter

# Better: wait for expected state
tmux send-keys -t app 'j'
until tmux capture-pane -t app -p | grep -q "item 2"; do sleep 0.05; done
tmux send-keys -t app Enter
```

### Complex Interactions

```bash
# Navigate a menu
tmux send-keys -t app Down Down Enter
sleep 0.2

# Type into an input field
tmux send-keys -t app 'my search query' Enter

# Open command palette
tmux send-keys -t app C-p
sleep 0.1
tmux send-keys -t app 'command name' Enter

# Scroll through content
for i in {1..10}; do
  tmux send-keys -t app Down
  sleep 0.05
done
```

---

## 4. Observing and Capturing State

### capture-pane Options

```bash
# Basic capture with ANSI colors
tmux capture-pane -t <target> -p -e > output.txt

# Capture specific line range
tmux capture-pane -t app -p -e -S 0 -E 20 > output.txt

# Include scrollback history
tmux capture-pane -t app -p -e -S -1000 > output.txt
```

| Flag | Purpose |
|------|---------|
| `-p` | Print to stdout (instead of tmux buffer) |
| `-e` | Include ANSI escape sequences (colors) |
| `-S n` | Start line (negative = scrollback) |
| `-E n` | End line |
| `-J` | Join wrapped lines |

### Reading Content Programmatically

```bash
# Search for content
tmux capture-pane -t app -p | grep -q "Error" && echo "Error found!"

# Check for UI element
if tmux capture-pane -t app -p | grep -q "Save successful"; then
  echo "Save completed"
fi

# Get specific line
tmux capture-pane -t app -p | sed -n '5p'

# Count occurrences
tmux capture-pane -t app -p | grep -c "item"
```

### Screenshots with freeze

```bash
# Capture terminal content
tmux capture-pane -t app -p -e > .agent/tui-dev/capture.txt

# Basic PNG
freeze .agent/tui-dev/capture.txt -o screenshot.png

# Styled screenshot
freeze .agent/tui-dev/capture.txt -o screenshot.png \
  --theme dracula \
  --padding 20 \
  --margin 20 \
  --border.radius 8 \
  --shadow.blur 20 \
  --font.family "JetBrains Mono" \
  --font.size 14 \
  --window

# SVG output (scalable)
freeze .agent/tui-dev/capture.txt -o screenshot.svg
```

#### freeze Options

| Option | Description | Example |
|--------|-------------|---------|
| `--theme` | Color theme | `dracula`, `monokai`, `nord` |
| `--padding` | Internal padding (px) | `20` |
| `--margin` | External margin (px) | `20` |
| `--border.radius` | Corner radius | `8` |
| `--shadow.blur` | Shadow blur radius | `20` |
| `--font.family` | Font name | `"JetBrains Mono"` |
| `--font.size` | Font size | `14` |
| `--window` | Show window chrome | (flag) |
| `-o` | Output file | `.png`, `.svg`, `.webp` |

### State Comparison

```bash
# Capture "before" state
tmux capture-pane -t app -p > .agent/tui-dev/before.txt

# Make interaction
tmux send-keys -t app Enter
sleep 0.5

# Capture "after" state
tmux capture-pane -t app -p > .agent/tui-dev/after.txt

# Compare
diff .agent/tui-dev/before.txt .agent/tui-dev/after.txt
```

---

## 5. AI Agent Development Loop

### The Workflow

```
┌──────────────────────────────────────────────────────────┐
│                  TUI Development Loop                     │
├──────────────────────────────────────────────────────────┤
│                                                           │
│   ┌────────┐    ┌────────┐    ┌────────┐                 │
│   │ 1.Edit │───▶│2.Build │───▶│ 3.Run  │                 │
│   │  Code  │    │  App   │    │in tmux │                 │
│   └────────┘    └────────┘    └────────┘                 │
│        ▲                           │                      │
│        │                           ▼                      │
│   ┌────────┐    ┌────────┐    ┌────────┐                 │
│   │ 6.Fix  │◀───│5.Verify│◀───│4.Capture│                │
│   │ Issues │    │ State  │    │ Output │                 │
│   └────────┘    └────────┘    └────────┘                 │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### Complete Development Cycle

```bash
# === 1. Edit code ===
# (Make code changes with Edit tool)

# === 2. Build ===
cargo build --release
if [ $? -ne 0 ]; then
  echo "Build failed"
  exit 1
fi

# === 3. Start TUI ===
tmux kill-session -t tui 2>/dev/null || true
tmux new-session -d -s tui -x 120 -y 40 \
  'TERM=xterm-256color ./target/release/my-tui'
sleep 2

# === 4. Capture state ===
mkdir -p .agent/tui-dev
tmux capture-pane -t tui -p -e > .agent/tui-dev/state.txt

# === 5. Verify ===
# Check for expected content
if ! grep -q "Welcome" .agent/tui-dev/state.txt; then
  echo "ERROR: Welcome message not displayed"
fi

# Check for errors
if grep -q "Error\|panic\|crash" .agent/tui-dev/state.txt; then
  echo "ERROR: Crash detected"
fi

# === 6. Interactive verification ===
tmux send-keys -t tui Tab
sleep 0.2
tmux send-keys -t tui Enter
sleep 0.5
tmux capture-pane -t tui -p -e > .agent/tui-dev/state-after.txt

if grep -q "Feature Active" .agent/tui-dev/state-after.txt; then
  echo "SUCCESS: Feature working"
fi

# === Cleanup ===
tmux kill-session -t tui
```

### Validation Helper Patterns

```bash
# Assert content present
assert_content() {
  local pattern="$1"
  local target="${2:-tui}"
  if ! tmux capture-pane -t "$target" -p | grep -q "$pattern"; then
    echo "FAIL: Expected '$pattern' not found"
    return 1
  fi
  echo "PASS: Found '$pattern'"
}

# Assert content absent
assert_no_content() {
  local pattern="$1"
  local target="${2:-tui}"
  if tmux capture-pane -t "$target" -p | grep -q "$pattern"; then
    echo "FAIL: Unexpected '$pattern' found"
    return 1
  fi
  echo "PASS: '$pattern' correctly absent"
}

# Wait for content with timeout
wait_for_content() {
  local pattern="$1"
  local timeout="${2:-30}"
  local target="${3:-tui}"

  for i in $(seq 1 $timeout); do
    if tmux capture-pane -t "$target" -p | grep -q "$pattern"; then
      return 0
    fi
    sleep 0.1
  done
  echo "TIMEOUT: '$pattern' not found after ${timeout}00ms"
  return 1
}
```

### Regression Detection

```bash
# Save known-good state as golden file
tmux capture-pane -t tui -p > .agent/tui-dev/golden/main-screen.txt

# Compare current state against golden
tmux capture-pane -t tui -p > .agent/tui-dev/current.txt

# Strip ANSI codes for content comparison
strip_ansi() {
  sed 's/\x1b\[[0-9;]*m//g'
}

diff <(strip_ansi < .agent/tui-dev/golden/main-screen.txt) \
     <(strip_ansi < .agent/tui-dev/current.txt)
```

---

## 6. Troubleshooting

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| App exits immediately | Missing TTY | Run inside tmux session |
| No colors in capture | Missing `-e` flag | Add `-e` to capture-pane |
| Wrong dimensions | Not set explicitly | Use `-x` and `-y` flags |
| Keys not registering | Too fast | Add `sleep 0.1` between sends |
| Unicode garbled | Locale issue | Set `LANG=en_US.UTF-8` |
| App unresponsive | Wrong TERM | Try `TERM=xterm-256color` |

### Debugging Rendering

```bash
# Check TERM value
tmux send-keys -t app 'echo $TERM' Enter
sleep 0.5
tmux capture-pane -t app -p | tail -2

# Verify color support
tmux send-keys -t app 'tput colors' Enter
sleep 0.5
tmux capture-pane -t app -p | tail -2

# Check for ANSI codes in capture
cat -v .agent/tui-dev/capture.txt | head -10
# Should show ^[[38;5;... sequences

# Verify session dimensions
tmux display-message -t app -p '#{window_width}x#{window_height}'
```

### Handling Crashes

```bash
# Check if session exists
tmux has-session -t tui 2>/dev/null
echo $?  # 0 = exists, 1 = gone

# Check running process
tmux list-panes -t tui -F '#{pane_pid} #{pane_current_command}'

# Capture crash output before cleanup
tmux capture-pane -t tui -p -e -S -1000 > .agent/tui-dev/crash-log.txt
```

---

## Directory Convention

Use `.agent/tui-dev/` for TUI development artifacts:

```
.agent/tui-dev/
├── captures/          # Raw terminal captures
│   ├── current.txt
│   └── before.txt
├── screenshots/       # Generated images
│   └── feature.png
├── golden/            # Reference states for regression
│   └── main-screen.txt
└── logs/              # Build/crash logs
    └── crash-log.txt
```

---

## Quick Reference

```bash
# Start TUI in tmux
tmux new-session -d -s tui -x 120 -y 40 'TERM=xterm-256color ./app'

# Wait for startup
sleep 2

# Send keystrokes
tmux send-keys -t tui Down Enter

# Capture output
tmux capture-pane -t tui -p -e > .agent/tui-dev/output.txt

# Take screenshot
freeze .agent/tui-dev/output.txt -o screenshot.png --theme nord

# Check for content
tmux capture-pane -t tui -p | grep -q "Success" && echo "OK"

# Cleanup
tmux kill-session -t tui
```
