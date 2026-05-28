# Pattern 4: Architecture

**Problem**: Code becomes a tangled mess as features are added. There's no clear place for new code, and everything depends on everything else.

**Solution**: Choose an architecture pattern that matches your tool's core processing model. The right pattern makes the code self-organizing.

---

## Concept

Architecture is about answering: **"How does data flow through this system?"**

Four proven patterns cover most CLI tools and applications:

| Pattern | Best For | Mental Model |
|---------|----------|--------------|
| **Pipeline** | Sequential transformations | Assembly line |
| **Batch Processor** | Many similar items | Checklist with progress |
| **Functional Modular** | Simple utilities | Pure functions, no state |
| **Event-Driven** | Reactive systems | Subscribe and respond |

---

## Decision Tree

```
What is the core processing model?

Is data transformed through distinct stages?
├─ Yes → Pipeline Architecture
└─ No ↓

Are you processing many similar items?
├─ Yes → Batch Processor Architecture
└─ No ↓

Is it a simple utility with minimal state?
├─ Yes → Functional Modular Architecture
└─ No ↓

Are you responding to external events?
├─ Yes → Event-Driven Architecture
└─ No → Start with Functional Modular, evolve as needed
```

---

## Pipeline Architecture

**Use when**: Data flows through distinct transformation stages.

**Mental model**: Assembly line—each station does one thing, passes to next.

```
Input → Stage 1 → Stage 2 → Stage 3 → Output
        (parse)   (process) (format)
```

### Implementation

```python
from dataclasses import dataclass
from typing import Generic, TypeVar
from abc import ABC, abstractmethod

T = TypeVar('T')
U = TypeVar('U')

@dataclass
class PipelineConfig:
    """Configuration flows through all stages."""
    input_path: str
    output_path: str
    verbose: bool = False

class Stage(ABC, Generic[T, U]):
    """Base class for pipeline stages."""

    @abstractmethod
    def process(self, input_data: T, config: PipelineConfig) -> U:
        pass

class Preprocessor(Stage[str, dict]):
    def process(self, input_data: str, config: PipelineConfig) -> dict:
        # Convert raw input to structured data
        return {"content": input_data, "metadata": {}}

class Processor(Stage[dict, dict]):
    def process(self, input_data: dict, config: PipelineConfig) -> dict:
        # Core business logic
        return {**input_data, "processed": True}

class Formatter(Stage[dict, str]):
    def process(self, input_data: dict, config: PipelineConfig) -> str:
        # Format for output
        return str(input_data)

class Pipeline:
    """Orchestrates stages in sequence."""

    def __init__(self, config: PipelineConfig):
        self.config = config
        self.preprocessor = Preprocessor()
        self.processor = Processor()
        self.formatter = Formatter()

    def run(self, raw_input: str) -> str:
        # Stage 1: Preprocess
        structured = self.preprocessor.process(raw_input, self.config)

        # Stage 2: Process
        processed = self.processor.process(structured, self.config)

        # Stage 3: Format
        output = self.formatter.process(processed, self.config)

        return output
```

### File Structure

```
src/my_tool/
├── pipeline.py      # Orchestrator + PipelineConfig
├── preprocessor.py  # Stage 1
├── processor.py     # Stage 2
├── formatter.py     # Stage 3
└── cli.py          # Entry point, creates Pipeline
```

---

## Batch Processor Architecture

**Use when**: Processing many similar items with progress tracking.

**Mental model**: Checklist—process each item, check it off, resume if interrupted.

```
Items[] → [For each: Process + Checkpoint] → Results[]
```

### Implementation

```python
from dataclasses import dataclass
from typing import List, Callable, TypeVar
from enum import Enum
import json
from pathlib import Path

T = TypeVar('T')
R = TypeVar('R')

class Status(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    ERROR = "error"
    SKIPPED = "skipped"

@dataclass
class BatchResult:
    total: int
    success: int
    errors: int
    skipped: int

class BatchProcessor:
    """Process items with checkpoint and resume support."""

    def __init__(self, state_file: Path):
        self.state_file = state_file
        self.processed: dict[str, Status] = {}

    def load_state(self):
        if self.state_file.exists():
            self.processed = json.loads(self.state_file.read_text())

    def save_state(self):
        self.state_file.write_text(json.dumps(self.processed, indent=2))

    def process(
        self,
        items: List[T],
        processor_fn: Callable[[T], R],
        get_id: Callable[[T], str],
        on_progress: Callable[[int, int], None] = None
    ) -> BatchResult:
        self.load_state()

        result = BatchResult(total=len(items), success=0, errors=0, skipped=0)

        for i, item in enumerate(items):
            item_id = get_id(item)

            # Skip already processed
            if item_id in self.processed:
                result.skipped += 1
                continue

            try:
                processor_fn(item)
                self.processed[item_id] = Status.SUCCESS.value
                result.success += 1
            except Exception as e:
                self.processed[item_id] = Status.ERROR.value
                result.errors += 1

            # Checkpoint after each item
            self.save_state()

            if on_progress:
                on_progress(i + 1, len(items))

        return result
```

### File Structure

```
src/my_tool/
├── batch.py         # BatchProcessor
├── items.py         # Item loading/parsing
├── processor.py     # Single-item processing logic
├── progress.py      # Progress tracking (CSV/JSON)
└── cli.py          # Entry point
```

---

## Functional Modular Architecture

**Use when**: Building simple utilities with minimal state.

**Mental model**: Pure functions—input in, output out, no side effects.

```
                ┌─────────┐
Input ──────────┤ fn(x)   ├──────────► Output
                └─────────┘
                No state, no side effects
```

### Implementation

```python
# utils.py - Pure utility functions
def parse_url(url: str) -> dict:
    """Parse URL into components. Pure function."""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    return {
        "scheme": parsed.scheme,
        "host": parsed.netloc,
        "path": parsed.path
    }

def sanitize_filename(name: str) -> str:
    """Remove invalid characters from filename. Pure function."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name

# service.py - Orchestrates pure functions
def process_item(item: dict) -> dict:
    """Process a single item using pure functions."""
    url_parts = parse_url(item["url"])
    filename = sanitize_filename(item["title"])
    return {**item, "url_parts": url_parts, "filename": filename}

# cli.py - Entry point with minimal orchestration
def main():
    items = load_items()
    results = [process_item(item) for item in items]
    save_results(results)
```

### Node.js Version

```javascript
// utils.js - Pure functions
function parseUrl(url) {
  const parsed = new URL(url);
  return {
    scheme: parsed.protocol.replace(':', ''),
    host: parsed.hostname,
    path: parsed.pathname
  };
}

function sanitizeFilename(name) {
  return name.replace(/[<>:"/\\|?*]/g, '_');
}

// service.js - Composition
function processItem(item) {
  const urlParts = parseUrl(item.url);
  const filename = sanitizeFilename(item.title);
  return { ...item, urlParts, filename };
}

module.exports = { parseUrl, sanitizeFilename, processItem };
```

### File Structure

```
src/
├── utils.js         # Pure utility functions
├── service.js       # Business logic (composes utils)
├── state.js         # Persistence (isolated side effects)
└── cli.js          # Entry point
```

---

## Event-Driven Architecture

**Use when**: Responding to external events (browser, file system, network).

**Mental model**: Subscribe and respond—events trigger handlers.

```
Event Source ──► [Event] ──► Handler ──► State Update
                              │
                              ▼
                         [Message] ──► UI
```

### Implementation (Browser Extension)

```typescript
// types.ts
type MessageAction =
  | { type: 'GET_STATE' }
  | { type: 'UPDATE_CONFIG'; payload: Config }
  | { type: 'TRIGGER_ACTION'; payload: { id: string } };

interface MessageResponse<T = unknown> {
  success: boolean;
  data?: T;
  error?: string;
}

// background.ts - Event handlers
chrome.runtime.onInstalled.addListener(() => {
  initializeState();
});

chrome.tabs.onCreated.addListener((tab) => {
  handleTabCreated(tab);
});

chrome.tabs.onRemoved.addListener((tabId) => {
  handleTabRemoved(tabId);
});

chrome.runtime.onMessage.addListener((message: MessageAction, sender, sendResponse) => {
  handleMessage(message)
    .then(response => sendResponse(response))
    .catch(error => sendResponse({ success: false, error: error.message }));
  return true; // Keep channel open for async response
});

async function handleMessage(message: MessageAction): Promise<MessageResponse> {
  switch (message.type) {
    case 'GET_STATE':
      return { success: true, data: await getState() };
    case 'UPDATE_CONFIG':
      await updateConfig(message.payload);
      return { success: true };
    case 'TRIGGER_ACTION':
      await triggerAction(message.payload.id);
      return { success: true };
    default:
      return { success: false, error: 'Unknown action' };
  }
}

// popup.ts - Sends messages to background
async function loadState() {
  const response = await chrome.runtime.sendMessage({ type: 'GET_STATE' });
  if (response.success) {
    renderUI(response.data);
  }
}
```

### File Structure

```
src/
├── types.ts         # Message types, state interfaces
├── background.ts    # Service worker, event handlers
├── popup.ts         # UI controller
├── state.ts         # State management
└── utils.ts        # Pure utilities
```

---

## Choosing an Architecture

| Question | If Yes → Pattern |
|----------|------------------|
| Does data flow through distinct transformation stages? | Pipeline |
| Are you processing many similar items with progress? | Batch Processor |
| Is it a simple utility with pure functions? | Functional Modular |
| Are you responding to events (UI, network, filesystem)? | Event-Driven |

---

## Checklist

- [ ] Architecture pattern is explicitly chosen and documented
- [ ] Data flow is clear (can diagram in <1 minute)
- [ ] Each module has one responsibility
- [ ] Dependencies flow one direction (no cycles)
- [ ] New feature has obvious home (no "where does this go?")
