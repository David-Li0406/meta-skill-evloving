---
name: computer-use-agents
description: Build AI agents that interact with computers like humans do, focusing on screen control, cursor movement, and text input while ensuring security through sandboxing.
---

# Computer Use Agents

## Patterns

### Perception-Reasoning-Action Loop

The fundamental architecture of computer use agents involves observing the screen, reasoning about the next action, executing that action, and repeating the process. This loop integrates vision models with action execution through an iterative pipeline.

Key components:
1. **PERCEPTION**: Capture the current screen state via screenshots.
2. **REASONING**: Analyze and plan actions using a vision-language model.
3. **ACTION**: Execute mouse and keyboard operations.
4. **FEEDBACK**: Observe results and continue or correct actions.

**Critical Insight**: Vision agents remain still during the "thinking" phase (1-5 seconds), creating a detectable pause pattern.

**When to use**: Building any computer use agent from scratch, integrating vision models with desktop control, or understanding agent behavior patterns.

```python
from anthropic import Anthropic
from PIL import Image
import base64
import pyautogui
import time

class ComputerUseAgent:
    """
    Perception-Reasoning-Action loop implementation.
    Based on Anthropic Computer Use patterns.
    """

    def __init__(self, client: Anthropic, model: str = "claude-sonnet-4-20250514"):
        self.client = client
        self.model = model
        self.max_steps = 50  # Prevent runaway loops
        self.action_delay = 0.5  # Seconds between actions

    def capture_screenshot(self) -> str:
        """Capture screen and return base64 encoded image."""
        screenshot = pyautogui.screenshot()
        screenshot = screenshot.resize((1280, 800), Image.LANCZOS)

        import io
        buffer = io.BytesIO()
        screenshot.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()

    def execute_action(self, action: dict) -> dict:
        """Execute mouse/keyboard action on the computer."""
        action_type = action.get("type")

        if action_type == "click":
            x, y = action["x"], action["y"]
            button = action.get("button", "left")
            pyautogui.click(x, y, button=button)
            return {"success": True, "action": f"clicked at ({x}, {y})"}

        elif action_type == "type":
            text = action["text"]
            pyautogui.typewrite(text, interval=0.02)
            return {"success": True, "action": f"typed {len(text)} chars"}

        elif action_type == "key":
            key = action["key"]
            pyautogui.press(key)
            return {"success": True, "action": f"pressed {key}"}

        elif action_type == "scroll":
            direction = action.get("direction", "down")
            amount = action.get("amount", 3)
            scroll = -amount if direction == "down" else amount
            pyautogui.scroll(scroll)
            return {"success": True, "action": f"scrolled {direction}"}
```

### Sandboxed Environment Pattern

Computer use agents must run in isolated, sandboxed environments to mitigate security risks. Use Docker containers with virtual desktops.

Key isolation requirements:
1. **NETWORK**: Restrict to necessary endpoints only.
2. **FILESYSTEM**: Use read-only or scoped temporary directories.
3. **CREDENTIALS**: No access to host credentials.
4. **SYSCALLS**: Filter dangerous system calls.
5. **RESOURCES**: Limit CPU, memory, and execution time.

The goal is "blast radius minimization"—if the agent malfunctions, damage is contained within the sandbox.

**When to use**: Deploying any computer use agent, testing agent behavior safely, or running untrusted automation tasks.

```dockerfile
# Dockerfile for sandboxed computer use environment
FROM ubuntu:22.04

# Install desktop environment
RUN apt-get update && apt-get install -y \
    xvfb \
    x11vnc \
    fluxbox \
    xterm \
    firefox \
    python3 \
    python3-pip \
    supervisor

# Security: Create non-root user
RUN useradd -m -s /bin/bash agent && \
    mkdir -p /home/agent/.vnc

# Install Python dependencies
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

# Security: Drop capabilities
RUN apt-get install -y --no-install-recommends libcap2-bin && \
    setcap -r /usr/bin/python3 || true

# Copy agent code
COPY --chown=agent:agent . /app
WORKDIR /app

# Supervisor config for virtual display + VNC
COPY supervisord.conf /etc/supervisor/conf.d/

# Expose VNC port only (not desktop directly)
EXPOSE 5900

# Run as non-root
USER agent

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
```

### Anthropic Computer Use Implementation

This section describes the official implementation pattern using Claude's computer use capability. Claude Opus 4.5 is currently the best model for computer use.

Key capabilities include:
- **screenshot**: Capture the current screen state.
- **mouse**: Perform click, move, and drag operations.
- **keyboard**: Type text and press keys.
- **bash**: Execute shell commands.
- **text_editor**: View and edit files.

**Critical Limitation**: Some UI elements (like dropdowns and scrollbars) may be challenging for Claude to manipulate.

**When to use**: Building production computer use agents, requiring high-quality vision understanding, or needing full desktop control (not just browser).

```python
from anthropic import Anthropic
from anthropic.types.beta import (
    BetaToolComputerUse20241022,
    BetaToolBash20241022,
    BetaToolTextEditor20241022,
)

class AnthropicComputerUse:
    """
    Official Anthropic Computer Use implementation.
    Requires a Docker container with a virtual display and VNC for viewing agent actions.
    """

    def __init__(self):
        self.client = Anthropic()
        self.model = "claude-sonnet-4-20250514"  # Best for computer use
        self.screen_size = (1280, 800)

    def get_tools(self) -> list:
        """Define computer use tools."""
        return [
            BetaToolComputerUse20241022(
                type="computer_20241022",
                name="computer",
                display_width_px=self.screen_size[0],
                display_height_px=self.screen_size[1],
            ),
            BetaToolBash20241022(
                type="bash_20241022",
                name="bash",
            ),
            BetaToolTextEditor20241022(
                type="text_editor_20241022",
                name="str_replace_editor",
            ),
        ]

    def execute_tool(self, name: str, input: dict) -> dict:
        """Execute a tool and return result."""
        if name == "computer":
            return self._handle_computer_action(input)
        elif name == "bash":
            return self._handle_bash(input)
        elif name == "str_replace_editor":
            return self._handle_editor(input)
        else:
            return {"error": f"Unknown tool: {name}"}
```

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Critical | Defense in depth - no single solution works. |
| Medium | Add human-like variance to actions. |
| High | Use keyboard alternatives when possible. |
| Medium | Accept the tradeoff. |
| High | Implement context management. |
| High | Monitor and limit costs. |
| Critical | ALWAYS use sandboxing. |