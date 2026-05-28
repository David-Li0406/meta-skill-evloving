# Common Code Patterns in GUI Agent

Reference for code patterns to look for during review and their implications.

## Prompt Patterns

### Good: Structured Output Specification

```python
SYSTEM_PROMPT = """
You are a GUI automation agent.

Return your response as JSON matching this schema:
{
    "action_type": "click|type|hotkey|scroll|wait|done",
    "x": 0.0-1.0,  // normalized x coordinate
    "y": 0.0-1.0,  // normalized y coordinate
    "text": "...", // for type action
    "reasoning": "..." // explain your decision
}
"""
```

**Why good**: Clear schema, normalized coordinates, reasoning field for debugging.

### Bad: Ambiguous Output Format

```python
SYSTEM_PROMPT = """
Tell me what action to take and where to click.
"""
```

**Why bad**: No schema, LLM may return unparseable response.

---

### Good: Action Constraints

```python
SYSTEM_PROMPT = """
Available actions:
- click: Click at (x, y). Use for buttons, links, icons.
- type: Type text. Only use AFTER clicking a text field.
- hotkey: Press key combo. Use for shortcuts like Ctrl+S.

IMPORTANT: Never type without first clicking a text field.
"""
```

**Why good**: Clear constraints prevent common mistakes.

### Bad: Missing Constraints

```python
SYSTEM_PROMPT = """
You can click, type, or use hotkeys.
"""
```

**Why bad**: LLM may type without focusing a field first.

---

## Action Implementation Patterns

### Good: Complete Action Method

```python
def _drag(self, start_x: float, start_y: float,
          end_x: float, end_y: float) -> tuple[bool, str]:
    try:
        screen_w, screen_h = pyautogui.size()
        sx = int(start_x * screen_w)
        sy = int(start_y * screen_h)
        ex = int(end_x * screen_w)
        ey = int(end_y * screen_h)

        pyautogui.moveTo(sx, sy)
        pyautogui.drag(ex - sx, ey - sy, duration=0.5)
        time.sleep(self.config.action_delay)

        return True, f"Dragged from ({start_x:.2f}, {start_y:.2f}) to ({end_x:.2f}, {end_y:.2f})"
    except Exception as e:
        return False, f"Drag failed: {e}"
```

**Why good**:
- Normalized → pixel conversion
- Uses pyautogui.size() not hardcoded
- Includes action_delay
- Returns tuple with success message
- Exception handling with context

### Bad: Incomplete Action Method

```python
def _drag(self, start_x, start_y, end_x, end_y):
    pyautogui.moveTo(int(start_x * 1920), int(start_y * 1080))
    pyautogui.drag(int((end_x - start_x) * 1920), int((end_y - start_y) * 1080))
```

**Why bad**:
- Hardcoded screen dimensions
- No return value
- No exception handling
- No delay
- No type hints

---

### Good: Execute Dispatch

```python
def execute(self, action: NextAction) -> tuple[bool, str]:
    if action.action_type == ActionType.CLICK:
        if action.x is None or action.y is None:
            return False, "Click requires x and y coordinates"
        return self._click(action.x, action.y)

    elif action.action_type == ActionType.DRAG:
        if None in (action.start_x, action.start_y, action.end_x, action.end_y):
            return False, "Drag requires start and end coordinates"
        return self._drag(action.start_x, action.start_y,
                         action.end_x, action.end_y)

    else:
        return False, f"Unknown action type: {action.action_type}"
```

**Why good**: Validates parameters before calling, handles unknown types.

### Bad: Execute Dispatch

```python
def execute(self, action):
    if action.action_type == "click":
        self._click(action.x, action.y)
    elif action.action_type == "drag":
        self._drag(action.start_x, action.start_y, action.end_x, action.end_y)
```

**Why bad**:
- String comparison instead of enum
- No parameter validation
- No return value
- No fallback for unknown types

---

## Context Management Patterns

### Good: Stable Prefix Initialization

```python
class ContextManager:
    def __init__(self, config: ContextConfig):
        self.config = config
        self._system_prompt = self._build_system_prompt()  # Built once
        self._tool_definitions = self._build_tools()  # Built once
        self._history: list[ActionObservationPair] = []

    def get_messages(self) -> list[dict]:
        # Prefix is always the same - KV-cache friendly
        messages = [
            {"role": "system", "content": self._system_prompt},
            *self._tool_definitions,
        ]
        # Only history changes
        messages.extend(self._format_history())
        return messages
```

**Why good**: System prompt and tools never change after init.

### Bad: Dynamic Prefix

```python
def get_messages(self):
    messages = [
        {"role": "system", "content": self._build_system_prompt()},  # Rebuilt each time!
    ]
    messages.extend(self._history)
    return messages
```

**Why bad**: Prefix changes invalidate KV-cache, wasting compute.

---

### Good: History Compression

```python
def _maybe_compress(self):
    token_count = self._estimate_tokens()

    if token_count > self.config.compression_threshold:
        # Keep recent pairs
        recent = self._history[-self.config.min_recent_pairs:]
        old = self._history[:-self.config.min_recent_pairs]

        if old:
            # Summarize old history
            summary = self._summarize_history(old)
            self._compressed_summary = summary
            self._history = recent
```

**Why good**: Preserves recent context, summarizes old.

### Bad: History Truncation

```python
def _maybe_compress(self):
    if len(self._history) > 10:
        self._history = self._history[-10:]  # Just drops old history
```

**Why bad**: Loses information without summarization.

---

## Screenshot Patterns

### Good: Grid Overlay

```python
def add_grid_overlay(self, image: Image.Image) -> Image.Image:
    draw = ImageDraw.Draw(image)
    width, height = image.size

    # Draw grid lines at 0.1 intervals
    for i in range(1, 10):
        # Vertical lines
        x = int(width * i / 10)
        draw.line([(x, 0), (x, height)], fill='red', width=1)
        draw.text((x + 2, 2), f"{i/10:.1f}", fill='yellow')

        # Horizontal lines
        y = int(height * i / 10)
        draw.line([(0, y), (width, y)], fill='red', width=1)
        draw.text((2, y + 2), f"{i/10:.1f}", fill='yellow')

    return image
```

**Why good**: Grid matches normalized coordinate system.

### Bad: Pixel-Based Grid

```python
def add_grid_overlay(self, image):
    draw = ImageDraw.Draw(image)

    # Grid every 100 pixels
    for x in range(0, image.width, 100):
        draw.line([(x, 0), (x, image.height)], fill='red')
        draw.text((x, 0), str(x), fill='yellow')  # Pixel labels!
```

**Why bad**: Grid labels show pixels, but LLM needs normalized coords.

---

### Good: Coordinate Logging

```python
def _click(self, x: float, y: float) -> tuple[bool, str]:
    screen_w, screen_h = pyautogui.size()
    pixel_x = int(x * screen_w)
    pixel_y = int(y * screen_h)

    logger.info(f"Click: normalized=({x:.3f}, {y:.3f}), "
                f"pixel=({pixel_x}, {pixel_y}), "
                f"screen={screen_w}x{screen_h}")

    pyautogui.click(pixel_x, pixel_y)
    return True, f"Clicked at ({x:.2f}, {y:.2f})"
```

**Why good**: Logs both normalized and pixel for debugging.

### Bad: No Coordinate Logging

```python
def _click(self, x, y):
    pyautogui.click(int(x * 1920), int(y * 1080))
```

**Why bad**: Can't debug coordinate mismatches.

---

## Error Handling Patterns

### Good: Contextual Error

```python
def execute(self, action: NextAction) -> tuple[bool, str]:
    try:
        if action.action_type == ActionType.CLICK:
            return self._click(action.x, action.y)
    except pyautogui.FailSafeException:
        return False, f"Failsafe triggered during {action.action_type} at ({action.x}, {action.y})"
    except Exception as e:
        return False, f"{action.action_type} failed: {e}"
```

**Why good**: Error includes action context.

### Bad: Generic Error

```python
def execute(self, action):
    try:
        if action.action_type == "click":
            self._click(action.x, action.y)
    except:
        print("Something went wrong")
```

**Why bad**:
- Bare except
- No context in error
- Print instead of return/log

---

## Anti-Patterns to Flag

### 1. Hardcoded Screen Dimensions

```python
# BAD
x = int(normalized_x * 1920)
y = int(normalized_y * 1080)

# GOOD
screen_w, screen_h = pyautogui.size()
x = int(normalized_x * screen_w)
y = int(normalized_y * screen_h)
```

### 2. Missing Action Delay

```python
# BAD
def _click(self, x, y):
    pyautogui.click(x, y)
    return True, "Clicked"

# GOOD
def _click(self, x, y):
    pyautogui.click(x, y)
    time.sleep(self.config.action_delay)
    return True, "Clicked"
```

### 3. String Action Types

```python
# BAD
if action.action_type == "click":

# GOOD
if action.action_type == ActionType.CLICK:
```

### 4. Mutable System Prompt

```python
# BAD
self.system_prompt += f"\nCurrent time: {datetime.now()}"

# GOOD
# Keep system_prompt immutable, add time to user message
```

### 5. Silent Failures

```python
# BAD
try:
    result = llm.call(prompt)
except:
    pass

# GOOD
try:
    result = llm.call(prompt)
except Exception as e:
    logger.error(f"LLM call failed: {e}")
    return None, f"LLM error: {e}"
```

### 6. Unbounded History

```python
# BAD
self.history.append(new_entry)  # Grows forever

# GOOD
self.history.append(new_entry)
self._maybe_compress()  # Check and compress if needed
```
