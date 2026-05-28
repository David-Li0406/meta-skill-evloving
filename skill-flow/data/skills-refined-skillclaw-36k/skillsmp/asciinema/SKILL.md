---
name: asciinema
description: Guide for recording terminal demos with asciinema-style recordings. Use when creating CLI tool demos, DevOps workflows, or any terminal-based demonstrations.
---

# Terminal Recording Guide

This skill covers recording terminal demos using asciinema-style recordings. The recordings can be:
1. Embedded as interactive terminal replays
2. Converted to video for final production

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Phase 1: Script Definition                                  │
│  - Define scenes with actions                               │
│  - Specify commands, waits, patterns                        │
│  - Configure typing simulation                              │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 2: Recording                                          │
│  - PTY session with shell                                   │
│  - Human-like typing simulation                             │
│  - Captures all terminal output                             │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 3: Output                                             │
│  - Asciicast v2 format (.cast)                              │
│  - Optional video conversion                                │
│  - Embeddable player or GIF/MP4                             │
└─────────────────────────────────────────────────────────────┘
```

## Script Format

Terminal demos are defined in YAML format:

```yaml
type: terminal
shell: /bin/zsh  # or /bin/bash
dimensions:
  cols: 120
  rows: 40

scenes:
  - name: "Install the CLI"
    actions:
      - type: command
        text: "npm install -g @mypackage/cli"
        delay_after: 3000

  - name: "Initialize project"
    actions:
      - type: command
        text: "mycli init my-project"
        delay_after: 2000
      - type: wait_for
        pattern: "Project initialized successfully"
        timeout: 10000

  - name: "Show result"
    actions:
      - type: command
        text: "ls -la my-project"
        delay_after: 1500
```

## Action Types

### command
Execute a command with realistic typing:

```yaml
- type: command
  text: "npm install"
  delay_after: 2000  # Wait 2s after command completes
```

### type
Type text without executing (no Enter key):

```yaml
- type: type
  text: "partial command"
  delay_after: 500
```

### wait
Simple pause:

```yaml
- type: wait
  delay_after: 1000  # Wait 1 second
```

### wait_for
Wait for specific output pattern:

```yaml
- type: wait_for
  pattern: "Success|Complete"  # Regex pattern
  timeout: 30000  # Max wait in ms
```

### clear
Clear the screen (Ctrl+L):

```yaml
- type: clear
  delay_after: 500
```

## Using the Terminal Recorder

### Basic Usage

```python
from utils.terminal_recorder import (
    TerminalRecorder,
    TerminalConfig,
    TerminalScene,
    TerminalAction,
)

# Create config
config = TerminalConfig(
    cols=120,
    rows=40,
    shell="/bin/zsh",
    typing_speed_min=0.03,
    typing_speed_max=0.10,
    mistake_probability=0.02,  # 2% chance of typos
)

# Define scenes
scenes = [
    TerminalScene(
        name="Install package",
        actions=[
            TerminalAction(
                action_type="command",
                text="npm install",
                delay_after=3000,
            ),
        ],
    ),
]

# Record
recorder = TerminalRecorder(config)
result = recorder.record_script(
    scenes=scenes,
    output_path=Path(".demo/my-demo/terminal.cast"),
)

if result.status == "success":
    print(f"Recording saved: {result.cast_path}")
    print(f"Duration: {result.duration_seconds}s")
```

### From YAML Script

```python
from utils.terminal_recorder import parse_terminal_script, record_terminal_demo

# Load script
with open("terminal-script.yaml") as f:
    scenes = parse_terminal_script(f.read())

# Record
result = record_terminal_demo(
    scenes=[s.__dict__ for s in scenes],
    output_dir=Path(".demo/my-demo"),
)
```

## Typing Simulation

The recorder simulates human typing with:

1. **Variable Speed**: Random delay between keystrokes (30-120ms)
2. **Punctuation Pauses**: Longer pauses after periods, commas
3. **Word Pauses**: Slight pause after spaces
4. **Typos**: Configurable probability of making and correcting typos

### Configuring Typing

```python
config = TerminalConfig(
    typing_speed_min=0.03,   # 30ms minimum
    typing_speed_max=0.12,   # 120ms maximum
    mistake_probability=0.02, # 2% typo rate
)
```

### Disabling Typos

For cleaner demos:

```python
config = TerminalConfig(
    mistake_probability=0.0,  # No typos
)
```

## Output Formats

### Asciicast v2 (.cast)

The native format is asciicast v2 JSON:

```json
{"version": 2, "width": 120, "height": 40, "timestamp": 1704672000}
[0.5, "o", "$ npm install\n"]
[1.2, "o", "Installing packages...\n"]
[3.5, "o", "Done!\n"]
```

### Converting to Video

Use the `convert_cast_to_video` function:

```python
from utils.terminal_recorder import convert_cast_to_video

# Convert to GIF
gif_path = convert_cast_to_video(
    cast_path=Path("demo.cast"),
    output_path=Path("demo.gif"),
    theme="monokai",
    font_size=14,
)

# Convert to MP4
mp4_path = convert_cast_to_video(
    cast_path=Path("demo.cast"),
    output_path=Path("demo.mp4"),
    theme="monokai",
)
```

**Requirements:** `agg` (asciinema GIF generator) and `ffmpeg`

```bash
cargo install agg
brew install ffmpeg  # or apt install ffmpeg
```

## Embedding

### Web Player

Use asciinema-player for web embedding:

```html
<script src="https://unpkg.com/asciinema-player@3.6.1/dist/bundle/asciinema-player.min.js"></script>
<link rel="stylesheet" href="https://unpkg.com/asciinema-player@3.6.1/dist/bundle/asciinema-player.min.css" />

<div id="player"></div>
<script>
  AsciinemaPlayer.create('demo.cast', document.getElementById('player'), {
    theme: 'monokai',
    speed: 1.5,
  });
</script>
```

### GitHub README

```markdown
[![asciicast](https://asciinema.org/a/YOUR_ID.svg)](https://asciinema.org/a/YOUR_ID)
```

## Best Practices

### Philosophy: Show Real Things Working

**The most important rule:** Demos should show the *experience* of using a feature, not the *evidence* that it was built.

- **Never** show `cat file.py` or `head -n 50 code.py` - that's what a PR diff shows
- **Never** create simulators or mock scripts - if the feature isn't working, fix it first
- **Always** show real commands producing real output
- **Rule of thumb:** If your demo could be replaced by linking to the PR, it's not a demo

### Technical Tips

1. **Keep commands short**: Long commands are harder to read
2. **Add delays after output**: Give viewers time to read
3. **Use wait_for patterns**: More reliable than fixed delays
4. **Clear between sections**: Helps separate demo parts
5. **Test locally first**: Run commands manually to verify
6. **Minimize typos**: Low probability (1-2%) is more realistic

## Troubleshooting

### Shell not starting

Check the shell path exists:
```bash
which zsh
which bash
```

### Command hangs

Use `wait_for` with timeout:
```yaml
- type: wait_for
  pattern: "\\$"  # Wait for prompt
  timeout: 5000
```

### Output not captured

Ensure commands produce output to stdout/stderr.

### Timing issues

Increase `delay_after` values for slower commands.

## Example: Full CLI Demo

```yaml
type: terminal
shell: /bin/zsh
dimensions:
  cols: 100
  rows: 30

scenes:
  - name: "Introduction"
    narration_notes: "Let me show you how to get started with our CLI"
    actions:
      - type: command
        text: "echo 'Welcome to MyCLI Demo!'"
        delay_after: 1500
      - type: clear
        delay_after: 500

  - name: "Installation"
    narration_notes: "First, install the CLI globally"
    actions:
      - type: command
        text: "npm install -g @myorg/cli"
        delay_after: 4000
      - type: wait_for
        pattern: "added .* packages"
        timeout: 30000

  - name: "Verify installation"
    actions:
      - type: command
        text: "mycli --version"
        delay_after: 1000

  - name: "Create project"
    narration_notes: "Now let's create a new project"
    actions:
      - type: command
        text: "mycli new my-project"
        delay_after: 2000
      - type: wait_for
        pattern: "Project created"
        timeout: 10000

  - name: "Explore structure"
    actions:
      - type: command
        text: "cd my-project && tree -L 2"
        delay_after: 2000

  - name: "Wrap up"
    narration_notes: "And that's it! You're ready to start building"
    actions:
      - type: wait
        delay_after: 2000
```

---

**When to use this skill:**
- Creating CLI tool installation demos
- DevOps workflow demonstrations
- Backend command-line tutorials
- Any terminal-based feature showcase
