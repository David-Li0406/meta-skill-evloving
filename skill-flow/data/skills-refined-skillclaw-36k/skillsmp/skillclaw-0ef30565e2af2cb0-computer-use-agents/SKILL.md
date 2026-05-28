---
name: computer-use-agents
description: Use this skill when you want to build AI agents that interact with computers like humans do, including tasks like screen control, desktop automation, and GUI automation.
---

# Computer Use Agents

## Overview

This skill focuses on building AI agents that can interact with computer interfaces by viewing screens, moving cursors, clicking buttons, and typing text. It covers various frameworks and methodologies, including Anthropic's Computer Use and OpenAI's Operator/CUA, with an emphasis on security and the unique challenges of vision-based control.

## Patterns

### Perception-Reasoning-Action Loop

The fundamental architecture of computer use agents consists of the following steps:

1. **PERCEPTION**: Capture the current screen state using screenshots.
2. **REASONING**: Analyze the screen content and plan the next action using a vision-language model.
3. **ACTION**: Execute mouse and keyboard operations based on the planned action.
4. **FEEDBACK**: Observe the result of the action and decide whether to continue or correct the course.

**Critical Insight**: Vision agents remain still during the "thinking" phase (1-5 seconds), which can create a detectable pause pattern.

## When to Use

- Building any computer use agent from scratch.
- Integrating vision models with desktop control.
- Understanding agent behavior patterns.

## Example Code

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
        # Resize for token efficiency (1280x800 is a good balance)
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
        # Additional action types can be implemented here
```