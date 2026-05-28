# Pattern 2: The Safety Net (Safety)

> *"Undo is the most important command in any system."* — Alan Cooper

**Problem**: Users run the wrong command, target the wrong file, or make a typo—and there's no way to recover.

**Solution**: Every destructive action must be reversible without heroics. Implement undo logs, soft deletes, and dry-run previews.

---

## Concept

The Safety Net pattern ensures your tool can answer: **"Can I undo what I just did?"**

A good safety net:
1. Never permanently destroys data on first action
2. Provides `--dry-run` to preview destructive operations
3. Logs all mutations for reversal
4. Makes undo as easy as do

---

## Decision Tree

```
Is the operation destructive?
├─ No (read-only) → Skip this pattern
└─ Yes → Implement safety net
    │
    ├─ Single item or batch?
    │   ├─ Single → Soft delete or undo log
    │   └─ Batch → Require --dry-run first OR --yes flag
    │
    └─ How to reverse?
        ├─ Move to trash → Soft delete with timestamp
        ├─ Log the inverse → Undo log (JSON)
        └─ Wrap in transaction → Rollback on failure
```

---

## Implementation

### Soft Delete (Single Items)

```python
import os
import shutil
import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional

TRASH_DIR = Path.home() / ".config" / "my-tool" / "trash"

@dataclass
class DeletedItem:
    original_path: str
    trash_path: str
    deleted_at: str
    metadata: Optional[dict] = None

def soft_delete(file_path: Path) -> DeletedItem:
    """Move file to trash instead of deleting permanently."""
    TRASH_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    trash_name = f"{timestamp}_{file_path.name}"
    trash_path = TRASH_DIR / trash_name

    # Move to trash
    shutil.move(str(file_path), str(trash_path))

    # Log the deletion
    item = DeletedItem(
        original_path=str(file_path),
        trash_path=str(trash_path),
        deleted_at=timestamp
    )
    _append_to_deletion_log(item)

    return item

def restore_last() -> Optional[DeletedItem]:
    """Restore the most recently deleted item."""
    log = _read_deletion_log()
    if not log:
        print("Nothing to restore")
        return None

    item = log.pop()
    trash_path = Path(item["trash_path"])
    original_path = Path(item["original_path"])

    if not trash_path.exists():
        print(f"Trash file not found: {trash_path}")
        return None

    # Restore
    original_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(trash_path), str(original_path))

    # Update log
    _write_deletion_log(log)

    print(f"Restored: {original_path}")
    return DeletedItem(**item)

def _append_to_deletion_log(item: DeletedItem):
    log = _read_deletion_log()
    log.append(asdict(item))
    _write_deletion_log(log)

def _read_deletion_log() -> list:
    log_path = TRASH_DIR / "deletion_log.json"
    if not log_path.exists():
        return []
    return json.loads(log_path.read_text())

def _write_deletion_log(log: list):
    log_path = TRASH_DIR / "deletion_log.json"
    log_path.write_text(json.dumps(log, indent=2))
```

### Undo Log (State Mutations)

```python
import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Any, Callable

UNDO_LOG = Path.home() / ".config" / "my-tool" / "undo_log.json"

@dataclass
class UndoEntry:
    action: str
    timestamp: str
    forward_data: dict  # What was done
    reverse_data: dict  # How to undo

def log_action(action: str, forward: dict, reverse: dict):
    """Log an action with its reverse operation."""
    entry = UndoEntry(
        action=action,
        timestamp=datetime.now().isoformat(),
        forward_data=forward,
        reverse_data=reverse
    )

    log = _read_undo_log()
    log.append(asdict(entry))
    _write_undo_log(log)

def undo_last() -> bool:
    """Undo the most recent action."""
    log = _read_undo_log()
    if not log:
        print("Nothing to undo")
        return False

    entry = log.pop()
    action = entry["action"]
    reverse = entry["reverse_data"]

    # Execute the reverse operation
    if action == "rename":
        Path(reverse["to"]).rename(reverse["from"])
    elif action == "write":
        Path(reverse["path"]).write_text(reverse["original_content"])
    elif action == "delete":
        # Restore from trash
        pass

    _write_undo_log(log)
    print(f"Undone: {action}")
    return True

# Example usage in rename operation
def rename_file(old_path: Path, new_path: Path):
    """Rename a file with undo support."""
    old_path.rename(new_path)
    log_action(
        action="rename",
        forward={"from": str(old_path), "to": str(new_path)},
        reverse={"from": str(new_path), "to": str(old_path)}
    )
```

### Dry Run (Batch Operations)

```python
from dataclasses import dataclass
from typing import List
import sys

@dataclass
class PlannedAction:
    action: str
    target: str
    details: str

def process_batch(items: List[str], dry_run: bool = False) -> List[PlannedAction]:
    """Process items with dry-run support."""
    plan = []

    for item in items:
        action = PlannedAction(
            action="delete",
            target=item,
            details=f"Remove file: {item}"
        )
        plan.append(action)

    if dry_run:
        print("DRY RUN - No changes will be made:\n")
        for action in plan:
            print(f"  [{action.action}] {action.target}")
            print(f"          {action.details}")
        print(f"\nTotal: {len(plan)} actions")
        print("\nRun with --execute to apply these changes.")
        return plan

    # Actually execute
    for action in plan:
        # Perform the action
        print(f"Executing: {action.action} {action.target}")

    return plan

# CLI usage
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes")
    parser.add_argument("--execute", action="store_true", help="Apply changes")
    parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation")
    args = parser.parse_args()

    if len(args.files) > 10 and not args.dry_run and not args.yes:
        print(f"This will affect {len(args.files)} files.")
        print("Run with --dry-run first, or --yes to confirm.")
        sys.exit(1)

    process_batch(args.files, dry_run=args.dry_run)
```

### Node.js Implementation

```javascript
const fs = require('fs');
const path = require('path');

const CONFIG_DIR = path.join(require('os').homedir(), '.config', 'my-tool');
const DELETION_LOG = path.join(CONFIG_DIR, 'deletion-log.json');

function ensureDir() {
  if (!fs.existsSync(CONFIG_DIR)) {
    fs.mkdirSync(CONFIG_DIR, { recursive: true });
  }
}

function logDeletion(item) {
  ensureDir();
  const log = readLog();
  log.push({
    ...item,
    deletedAt: new Date().toISOString()
  });
  fs.writeFileSync(DELETION_LOG, JSON.stringify(log, null, 2));
}

function readLog() {
  if (!fs.existsSync(DELETION_LOG)) return [];
  return JSON.parse(fs.readFileSync(DELETION_LOG, 'utf8'));
}

function getRecentDeletions(count = 10) {
  const log = readLog();
  return log.slice(-count).reverse();
}

function removeLogEntries(ids) {
  const log = readLog();
  const filtered = log.filter(entry => !ids.includes(entry.id));
  fs.writeFileSync(DELETION_LOG, JSON.stringify(filtered, null, 2));
}

// Example: Gmail-style trash with restore
async function trashEmails(emailIds) {
  // Log BEFORE deleting (enables restore even if crash)
  for (const id of emailIds) {
    const email = await getEmailById(id);
    logDeletion({
      id: email.id,
      threadId: email.threadId,
      from: email.from,
      subject: email.subject,
      snippet: email.snippet
    });
  }

  // Now actually trash
  await gmail.users.messages.batchModify({
    userId: 'me',
    requestBody: { ids: emailIds, addLabelIds: ['TRASH'] }
  });
}

async function restoreEmails(count = 1) {
  const recent = getRecentDeletions(count);
  const ids = recent.map(e => e.id);

  await gmail.users.messages.batchModify({
    userId: 'me',
    requestBody: { ids, removeLabelIds: ['TRASH'] }
  });

  removeLogEntries(ids);
  return recent;
}
```

---

## Mechanism Selection

| Scope | Mechanism | Implementation |
|-------|-----------|----------------|
| Single item | Soft delete | Move to `.trash/` with timestamp |
| Batch operation | Dry run | `--dry-run` shows plan, `--execute` runs it |
| State mutation | Undo log | JSON file recording reverse operations |
| Database | Transaction | Wrap in transaction, rollback on failure |

---

## Checklist

- [ ] Destructive commands have `--dry-run` flag
- [ ] Batch operations (>10 items) require `--dry-run` or `--yes`
- [ ] Deletions go to trash first (soft delete)
- [ ] Undo log persists to disk (survives restart)
- [ ] `<tool> undo` command exists
- [ ] Undo works for at least the last N operations
- [ ] Permanent deletion requires explicit `--purge` or 30-day TTL

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| "Are you sure?" prompt | Users always click yes | Implement real undo |
| Undo only in memory | Restart = permanent | Persist to disk |
| No dry-run | Users can't preview | Add `--dry-run` flag |
| Immediate hard delete | No recovery possible | Soft delete first |

---

## Success Signals

- Wrong command on wrong target → recover in <60 seconds
- `--dry-run` output matches `--execute` result exactly
- Undo works after restart, not just during session
- Users trust the tool with important data
