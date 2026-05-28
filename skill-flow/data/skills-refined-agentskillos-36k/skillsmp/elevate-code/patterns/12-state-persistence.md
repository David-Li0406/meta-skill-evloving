# Pattern 12: State Persistence

**Problem**: User data, configuration, and progress are lost when the tool restarts. Or worse, data corruption from crashes mid-write.

**Solution**: Use atomic writes, platform-appropriate locations, and structured state files.

---

## Concept

State Persistence answers: **"Where does my data live, and is it safe?"**

Good state persistence provides:
1. **Durability** — Data survives restarts and crashes
2. **Atomicity** — No partial writes or corruption
3. **Discoverability** — Files in expected locations
4. **Portability** — Works across platforms

---

## File Locations

### Platform Conventions

| Platform | User Config | User Data | Cache |
|----------|-------------|-----------|-------|
| **Linux** | `~/.config/<app>/` | `~/.local/share/<app>/` | `~/.cache/<app>/` |
| **macOS** | `~/.config/<app>/` | `~/Library/Application Support/<app>/` | `~/Library/Caches/<app>/` |
| **Windows** | `%APPDATA%\<app>\` | `%LOCALAPPDATA%\<app>\` | `%LOCALAPPDATA%\<app>\Cache\` |

### Python: Platform-Aware Paths

```python
import os
import sys
from pathlib import Path

def get_config_dir(app_name: str) -> Path:
    """Get platform-appropriate config directory."""
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", "~"))
    elif sys.platform == "darwin":
        base = Path.home() / ".config"  # Or Library/Application Support
    else:  # Linux and others
        base = Path(os.environ.get("XDG_CONFIG_HOME", "~/.config"))

    config_dir = base.expanduser() / app_name
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir

def get_data_dir(app_name: str) -> Path:
    """Get platform-appropriate data directory."""
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", "~"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", "~/.local/share"))

    data_dir = base.expanduser() / app_name
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

def get_cache_dir(app_name: str) -> Path:
    """Get platform-appropriate cache directory."""
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", "~")) / "Cache"
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Caches"
    else:
        base = Path(os.environ.get("XDG_CACHE_HOME", "~/.cache"))

    cache_dir = base.expanduser() / app_name
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir
```

### Node.js: Platform-Aware Paths

```javascript
const os = require('os');
const path = require('path');
const fs = require('fs');

function getConfigDir(appName) {
  let base;

  switch (process.platform) {
    case 'win32':
      base = process.env.APPDATA || path.join(os.homedir(), 'AppData', 'Roaming');
      break;
    case 'darwin':
      base = path.join(os.homedir(), '.config');
      break;
    default: // Linux
      base = process.env.XDG_CONFIG_HOME || path.join(os.homedir(), '.config');
  }

  const configDir = path.join(base, appName);
  fs.mkdirSync(configDir, { recursive: true });
  return configDir;
}

// Simplified: always use ~/.config for CLI tools
function getSimpleConfigDir(appName) {
  const configDir = path.join(os.homedir(), '.config', appName);
  fs.mkdirSync(configDir, { recursive: true });
  return configDir;
}
```

---

## Atomic Writes

**Critical**: Never write directly to the final file path. A crash mid-write corrupts data.

### Python

```python
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

def atomic_write_json(path: Path, data: dict):
    """Write JSON atomically - safe from crashes."""
    path.parent.mkdir(parents=True, exist_ok=True)

    # Write to temp file in same directory (same filesystem)
    temp_path = path.with_suffix('.tmp')
    temp_path.write_text(json.dumps(data, indent=2))

    # Atomic rename (on POSIX systems)
    temp_path.rename(path)

def atomic_write_text(path: Path, content: str):
    """Write text atomically."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix('.tmp')
    temp_path.write_text(content)
    temp_path.rename(path)

# Alternative using tempfile (more portable)
def atomic_write_portable(path: Path, data: dict):
    """Atomic write that works on Windows too."""
    import tempfile

    path.parent.mkdir(parents=True, exist_ok=True)

    # Create temp file in same directory
    fd, temp_path = tempfile.mkstemp(
        dir=path.parent,
        prefix='.tmp_',
        suffix='.json'
    )

    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(data, f, indent=2)

        # On Windows, need to remove target first
        if os.name == 'nt' and path.exists():
            path.unlink()

        os.rename(temp_path, path)
    except:
        os.unlink(temp_path)
        raise
```

### Node.js

```javascript
const fs = require('fs');
const path = require('path');
const os = require('os');

function atomicWriteJson(filePath, data) {
  const dir = path.dirname(filePath);
  fs.mkdirSync(dir, { recursive: true });

  // Write to temp file
  const tempPath = filePath + '.tmp';
  fs.writeFileSync(tempPath, JSON.stringify(data, null, 2));

  // Atomic rename
  fs.renameSync(tempPath, filePath);
}

// With proper error handling
function atomicWriteJsonSafe(filePath, data) {
  const dir = path.dirname(filePath);
  fs.mkdirSync(dir, { recursive: true });

  const tempPath = `${filePath}.${process.pid}.tmp`;

  try {
    fs.writeFileSync(tempPath, JSON.stringify(data, null, 2));
    fs.renameSync(tempPath, filePath);
  } catch (error) {
    // Clean up temp file on error
    try {
      fs.unlinkSync(tempPath);
    } catch {}
    throw error;
  }
}
```

---

## State File Patterns

### Per-Account State

```python
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import json

@dataclass
class AccountState:
    """State for a single account."""
    last_check: str | None = None
    seen_ids: list[str] = None
    cursor: str | None = None

    def __post_init__(self):
        if self.seen_ids is None:
            self.seen_ids = []

def get_state_path(account: str = "default") -> Path:
    config_dir = get_config_dir("my-tool")
    return config_dir / f"state-{account}.json"

def load_state(account: str = "default") -> AccountState:
    """Load state for account, or return empty state."""
    path = get_state_path(account)
    if not path.exists():
        return AccountState()

    try:
        data = json.loads(path.read_text())
        return AccountState(**data)
    except (json.JSONDecodeError, TypeError):
        # Corrupt file, start fresh
        return AccountState()

def save_state(state: AccountState, account: str = "default"):
    """Save state atomically."""
    path = get_state_path(account)
    atomic_write_json(path, asdict(state))

def update_state(account: str, **updates):
    """Update specific fields in state."""
    state = load_state(account)
    for key, value in updates.items():
        if hasattr(state, key):
            setattr(state, key, value)
    save_state(state, account)
```

### Audit Log

```python
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import json

@dataclass
class AuditEntry:
    """Single audit log entry."""
    timestamp: str
    action: str
    target: str
    details: dict | None = None

class AuditLog:
    """Append-only audit log with rotation."""

    def __init__(self, app_name: str, max_entries: int = 1000):
        self.path = get_config_dir(app_name) / "audit.json"
        self.max_entries = max_entries

    def _read(self) -> list[dict]:
        if not self.path.exists():
            return []
        try:
            return json.loads(self.path.read_text())
        except json.JSONDecodeError:
            return []

    def _write(self, entries: list[dict]):
        atomic_write_json(self.path, entries)

    def log(self, action: str, target: str, details: dict | None = None):
        """Add entry to audit log."""
        entry = AuditEntry(
            timestamp=datetime.now().isoformat(),
            action=action,
            target=target,
            details=details
        )

        entries = self._read()
        entries.append(asdict(entry))

        # Rotate if too large
        if len(entries) > self.max_entries:
            entries = entries[-self.max_entries:]

        self._write(entries)

    def get_recent(self, count: int = 10) -> list[AuditEntry]:
        """Get most recent entries."""
        entries = self._read()
        return [AuditEntry(**e) for e in entries[-count:]]
```

### State Schema Versioning

```python
from dataclasses import dataclass

CURRENT_SCHEMA_VERSION = 2

@dataclass
class VersionedState:
    """State with schema version for migrations."""
    schema_version: int
    data: dict

def migrate_state(state: dict) -> dict:
    """Migrate state to current schema version."""
    version = state.get("schema_version", 1)

    # Migration chain
    if version < 2:
        # v1 -> v2: Rename 'items' to 'entries'
        if "items" in state.get("data", {}):
            state["data"]["entries"] = state["data"].pop("items")
        version = 2

    state["schema_version"] = CURRENT_SCHEMA_VERSION
    return state

def load_versioned_state(path: Path) -> dict:
    """Load state with automatic migration."""
    if not path.exists():
        return {"schema_version": CURRENT_SCHEMA_VERSION, "data": {}}

    state = json.loads(path.read_text())
    if state.get("schema_version", 1) < CURRENT_SCHEMA_VERSION:
        state = migrate_state(state)
        atomic_write_json(path, state)

    return state
```

---

## Browser Extension: IndexedDB

```typescript
// telemetry.ts - IndexedDB wrapper
const DB_NAME = 'my-extension';
const DB_VERSION = 1;

interface TelemetryDB extends IDBDatabase {
  // Type-safe store names
}

class Telemetry {
  private db: IDBDatabase | null = null;

  async init(): Promise<void> {
    if (this.db) return;

    return new Promise((resolve, reject) => {
      const request = indexedDB.open(DB_NAME, DB_VERSION);

      request.onerror = () => reject(request.error);

      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;

        // Create object stores
        if (!db.objectStoreNames.contains('events')) {
          const store = db.createObjectStore('events', {
            keyPath: 'id',
            autoIncrement: true
          });
          store.createIndex('timestamp', 'timestamp');
          store.createIndex('type', 'type');
        }

        if (!db.objectStoreNames.contains('state')) {
          db.createObjectStore('state', { keyPath: 'key' });
        }
      };

      request.onsuccess = () => {
        this.db = request.result;
        resolve();
      };
    });
  }

  async logEvent(type: string, data: Record<string, unknown>): Promise<void> {
    await this.init();

    return new Promise((resolve, reject) => {
      const tx = this.db!.transaction('events', 'readwrite');
      const store = tx.objectStore('events');

      const event = {
        type,
        timestamp: Date.now(),
        data
      };

      const request = store.add(event);
      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve();
    });
  }

  async getState<T>(key: string, defaultValue: T): Promise<T> {
    await this.init();

    return new Promise((resolve, reject) => {
      const tx = this.db!.transaction('state', 'readonly');
      const store = tx.objectStore('state');
      const request = store.get(key);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        resolve(request.result?.value ?? defaultValue);
      };
    });
  }

  async setState<T>(key: string, value: T): Promise<void> {
    await this.init();

    return new Promise((resolve, reject) => {
      const tx = this.db!.transaction('state', 'readwrite');
      const store = tx.objectStore('state');
      const request = store.put({ key, value });

      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve();
    });
  }
}

export const telemetry = new Telemetry();
```

---

## Checklist

- [ ] Config/state in platform-appropriate location
- [ ] All writes are atomic (temp + rename)
- [ ] Graceful handling of corrupt/missing files
- [ ] Per-entity state namespacing (e.g., `state-{account}.json`)
- [ ] Audit log for destructive operations
- [ ] Schema version for future migrations
- [ ] Auto-cleanup of old entries (TTL)

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Write to final path | Crash = corruption | Temp file + atomic rename |
| Hardcoded paths | Breaks on other systems | Use platform-aware paths |
| No schema version | Can't migrate | Add version field |
| Unbounded logs | Disk fills up | Rotate/TTL old entries |
