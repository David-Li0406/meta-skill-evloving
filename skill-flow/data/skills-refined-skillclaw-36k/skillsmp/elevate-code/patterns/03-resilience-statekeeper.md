# Pattern 3: The Statekeeper (Resilience)

> *"Crash-only software is more reliable than software that tries not to crash."* — George Candea

**Problem**: Long-running operations crash midway, and users lose all progress. Network fails, user hits Ctrl+C, process gets killed.

**Solution**: Design for interruption. Checkpoint progress after each unit of work so operations can resume without starting over.

---

## Concept

The Statekeeper pattern ensures your tool can answer: **"If I crash now, how much work do I lose?"**

The answer should always be: **"At most one item."**

A good statekeeper:
1. Checkpoints after each item, not after batch
2. Writes state atomically (no corruption)
3. Detects and offers to resume on restart
4. Implements retry with backoff for transient failures

---

## Decision Tree

```
How long does the operation take?
├─ < 30 seconds → Skip this pattern
└─ > 30 seconds → Implement statekeeper
    │
    ├─ What kind of operation?
    │   ├─ Multi-item processing → Checkpoint per item
    │   ├─ API calls → Retry with backoff
    │   ├─ Long computation → Progress persistence
    │   └─ Mixed → All of the above
    │
    └─ State storage?
        ├─ Simple progress → JSON file
        ├─ Large state → SQLite
        └─ Distributed → External store (Redis)
```

---

## Implementation

### Checkpoint Per Item (Python)

```python
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Optional
from datetime import datetime

STATE_FILE = Path.home() / ".config" / "my-tool" / ".state.json"

@dataclass
class ProcessingState:
    total_items: int
    processed_items: List[str]
    current_index: int
    started_at: str
    last_updated: str

    @classmethod
    def new(cls, items: List[str]) -> "ProcessingState":
        return cls(
            total_items=len(items),
            processed_items=[],
            current_index=0,
            started_at=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat()
        )

    @classmethod
    def load(cls) -> Optional["ProcessingState"]:
        if not STATE_FILE.exists():
            return None
        data = json.loads(STATE_FILE.read_text())
        return cls(**data)

    def save(self):
        """Atomic save - write to temp, then rename."""
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        temp_path = STATE_FILE.with_suffix(".tmp")
        temp_path.write_text(json.dumps(asdict(self), indent=2))
        temp_path.rename(STATE_FILE)  # Atomic on POSIX

    def mark_complete(self, item_id: str):
        self.processed_items.append(item_id)
        self.current_index += 1
        self.last_updated = datetime.now().isoformat()
        self.save()

    def clear(self):
        if STATE_FILE.exists():
            STATE_FILE.unlink()

def process_items(items: List[str], processor_fn):
    """Process items with checkpoint support."""
    # Check for existing state
    state = ProcessingState.load()

    if state and state.processed_items:
        remaining = state.total_items - len(state.processed_items)
        print(f"Found incomplete run: {len(state.processed_items)}/{state.total_items} done")
        response = input(f"Resume from item {state.current_index + 1}? [Y/n] ")
        if response.lower() == 'n':
            state = ProcessingState.new(items)
    else:
        state = ProcessingState.new(items)

    # Process items, skipping already processed
    for i, item in enumerate(items):
        if item in state.processed_items:
            continue

        print(f"Processing {i + 1}/{len(items)}: {item}")

        try:
            processor_fn(item)
            state.mark_complete(item)  # Checkpoint after each item
        except KeyboardInterrupt:
            print(f"\nInterrupted. Progress saved at {state.current_index}/{state.total_items}")
            print("Run again to resume.")
            raise
        except Exception as e:
            print(f"Error processing {item}: {e}")
            # Don't mark complete, will retry on next run
            raise

    # All done, clean up state
    state.clear()
    print(f"Completed all {len(items)} items")
```

### Retry with Exponential Backoff

```python
import time
import random
from functools import wraps
from typing import Tuple, Type

def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    retryable_exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """Decorator for retry with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as e:
                    last_exception = e

                    if attempt == max_retries:
                        break

                    # Calculate delay
                    delay = min(base_delay * (exponential_base ** attempt), max_delay)
                    if jitter:
                        delay = delay * (0.5 + random.random())

                    print(f"Attempt {attempt + 1} failed: {e}")
                    print(f"Retrying in {delay:.1f}s...")
                    time.sleep(delay)

            raise last_exception
        return wrapper
    return decorator

# Usage
@retry_with_backoff(max_retries=3, retryable_exceptions=(ConnectionError, TimeoutError))
def fetch_data(url: str) -> dict:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()
```

### CSV-Based Progress Tracking

```python
import csv
from pathlib import Path
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

class Status(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    ERROR = "error"
    SKIPPED = "skipped"

@dataclass
class ProgressEntry:
    id: str
    status: Status
    error_message: Optional[str] = None

def load_progress(csv_path: Path) -> dict[str, ProgressEntry]:
    """Load progress from CSV file."""
    if not csv_path.exists():
        return {}

    progress = {}
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            progress[row['id']] = ProgressEntry(
                id=row['id'],
                status=Status(row['status']),
                error_message=row.get('error_message')
            )
    return progress

def save_progress(csv_path: Path, entries: List[ProgressEntry]):
    """Save progress to CSV file."""
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'status', 'error_message'])
        writer.writeheader()
        for entry in entries:
            writer.writerow({
                'id': entry.id,
                'status': entry.status.value,
                'error_message': entry.error_message or ''
            })

def update_status(csv_path: Path, item_id: str, status: Status, error: str = None):
    """Update a single item's status in the CSV."""
    progress = load_progress(csv_path)
    progress[item_id] = ProgressEntry(id=item_id, status=status, error_message=error)
    save_progress(csv_path, list(progress.values()))
```

### Node.js Implementation

```javascript
const fs = require('fs');
const path = require('path');

const STATE_DIR = path.join(require('os').homedir(), '.config', 'my-tool');
const STATE_FILE = path.join(STATE_DIR, 'state.json');

function loadState() {
  if (!fs.existsSync(STATE_FILE)) return null;
  return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
}

function saveState(state) {
  if (!fs.existsSync(STATE_DIR)) {
    fs.mkdirSync(STATE_DIR, { recursive: true });
  }

  // Atomic write: temp file then rename
  const tempFile = STATE_FILE + '.tmp';
  fs.writeFileSync(tempFile, JSON.stringify(state, null, 2));
  fs.renameSync(tempFile, STATE_FILE);
}

function clearState() {
  if (fs.existsSync(STATE_FILE)) {
    fs.unlinkSync(STATE_FILE);
  }
}

async function processWithCheckpoints(items, processorFn) {
  let state = loadState();

  if (state && state.processedIds.length > 0) {
    const remaining = state.totalItems - state.processedIds.length;
    console.log(`Found incomplete run: ${state.processedIds.length}/${state.totalItems} done`);
    // Prompt user to resume...
  } else {
    state = {
      totalItems: items.length,
      processedIds: [],
      currentIndex: 0,
      startedAt: new Date().toISOString()
    };
  }

  const processedSet = new Set(state.processedIds);

  for (let i = 0; i < items.length; i++) {
    const item = items[i];

    if (processedSet.has(item.id)) {
      continue; // Skip already processed
    }

    console.log(`Processing ${i + 1}/${items.length}: ${item.id}`);

    try {
      await processorFn(item);

      // Checkpoint after each item
      state.processedIds.push(item.id);
      state.currentIndex = i + 1;
      state.lastUpdated = new Date().toISOString();
      saveState(state);
    } catch (error) {
      console.error(`Error processing ${item.id}:`, error.message);
      throw error;
    }
  }

  clearState();
  console.log(`Completed all ${items.length} items`);
}

// Retry with backoff
async function withRetry(fn, maxRetries = 3, baseDelay = 1000) {
  let lastError;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;

      if (attempt === maxRetries) break;

      const delay = baseDelay * Math.pow(2, attempt);
      console.log(`Attempt ${attempt + 1} failed, retrying in ${delay}ms...`);
      await new Promise(r => setTimeout(r, delay));
    }
  }

  throw lastError;
}
```

---

## Mechanism Selection

| Scenario | Mechanism | Implementation |
|----------|-----------|----------------|
| Multi-item processing | Checkpoints | Save progress after each item |
| API calls | Retry with backoff | 3 retries: 1s, 2s, 4s |
| Long computation | Progress persistence | Serialize intermediate state |
| Partial success | Graceful degradation | Return what worked, report failures |

---

## Checklist

- [ ] State file location follows platform conventions
- [ ] State is saved after each item (not after batch)
- [ ] Atomic writes prevent corruption (temp + rename)
- [ ] Resume prompt on restart if incomplete state exists
- [ ] API calls retry with exponential backoff
- [ ] Progress bar shows current/total
- [ ] Graceful handling of Ctrl+C (save state before exit)

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Checkpoint after batch | Crash = lose all progress | Checkpoint per item |
| Write directly to state file | Crash mid-write = corruption | Temp file + atomic rename |
| No retry on network errors | Single failure = complete failure | Retry with backoff |
| Silent failures | User thinks it worked | Fail loudly with context |

---

## Success Signals

- Ctrl+C at 50%, resume → completes remaining 50% with zero rework
- Network blip mid-batch → automatic retry, no user intervention
- Process killed → state file intact, no corruption
- Users trust the tool for long-running jobs
