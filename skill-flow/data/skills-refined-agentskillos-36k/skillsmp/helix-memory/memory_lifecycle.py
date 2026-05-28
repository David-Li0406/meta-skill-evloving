#!/usr/bin/env python3
"""
Memory Lifecycle Management

Handles:
- Access tracking (which memories are being used)
- Importance decay (unused memories fade)
- Automatic pruning (remove very old, low-importance memories)

Access-based decay: Memories that are never retrieved decay over time.
Frequently accessed memories maintain or increase importance.
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent / "hooks"))

from common import (
    check_helix_running,
    get_all_memories,
    delete_memory,
    store_memory
)

# Configuration
ACCESS_FILE = Path(__file__).parent / ".memory_access.json"
DECAY_INTERVAL_DAYS = 7      # How often decay should run
DECAY_AMOUNT = 1             # How much importance drops per decay cycle
MIN_IMPORTANCE = 2           # Never decay below this
PRUNE_THRESHOLD = 1          # Delete memories at this importance
PRUNE_AGE_DAYS = 30          # Only prune if older than this


def load_access_data() -> dict:
    """Load access tracking data."""
    try:
        if ACCESS_FILE.exists():
            with open(ACCESS_FILE) as f:
                return json.load(f)
    except:
        pass
    return {"memories": {}, "last_decay": None}


def save_access_data(data: dict):
    """Save access tracking data."""
    with open(ACCESS_FILE, 'w') as f:
        json.dump(data, f, indent=2, default=str)


def record_access(memory_id: str):
    """Record that a memory was accessed/retrieved."""
    data = load_access_data()

    now = datetime.now().isoformat()

    if memory_id not in data["memories"]:
        data["memories"][memory_id] = {
            "access_count": 0,
            "first_seen": now,
            "last_accessed": None
        }

    data["memories"][memory_id]["access_count"] += 1
    data["memories"][memory_id]["last_accessed"] = now

    save_access_data(data)


def get_access_count(memory_id: str) -> int:
    """Get access count for a memory."""
    data = load_access_data()
    return data.get("memories", {}).get(memory_id, {}).get("access_count", 0)


def get_last_accessed(memory_id: str) -> datetime:
    """Get last access time for a memory."""
    data = load_access_data()
    last = data.get("memories", {}).get(memory_id, {}).get("last_accessed")
    if last:
        return datetime.fromisoformat(last)
    return None


def should_decay(memory_id: str, days_threshold: int = DECAY_INTERVAL_DAYS) -> bool:
    """Check if a memory should decay (hasn't been accessed recently)."""
    last = get_last_accessed(memory_id)
    if last is None:
        # Never accessed - should decay
        return True

    age = datetime.now() - last
    return age.days >= days_threshold


def run_decay(dry_run: bool = True):
    """
    Run decay cycle on all memories.

    - Memories not accessed in DECAY_INTERVAL_DAYS lose DECAY_AMOUNT importance
    - Memories below PRUNE_THRESHOLD and older than PRUNE_AGE_DAYS get deleted
    - Frequently accessed memories are protected
    """
    if not check_helix_running():
        print("ERROR: HelixDB not running")
        return

    data = load_access_data()
    memories = get_all_memories()

    # Check if enough time has passed since last decay
    last_decay = data.get("last_decay")
    if last_decay:
        last_decay_dt = datetime.fromisoformat(last_decay)
        days_since = (datetime.now() - last_decay_dt).days
        if days_since < DECAY_INTERVAL_DAYS:
            print(f"Decay ran {days_since} days ago, skipping (threshold: {DECAY_INTERVAL_DAYS} days)")
            return

    print(f"\n{'='*60}")
    print(f"MEMORY DECAY CYCLE")
    print(f"{'='*60}\n")
    print(f"Total memories: {len(memories)}")
    print(f"Decay amount: -{DECAY_AMOUNT} importance")
    print(f"Min importance: {MIN_IMPORTANCE}")
    print(f"Prune threshold: {PRUNE_THRESHOLD}")
    print()

    to_decay = []
    to_prune = []
    protected = []

    for memory in memories:
        mid = memory.get("id", "")
        importance = memory.get("importance", 5)
        category = memory.get("category", "")

        # Get access stats
        access_count = get_access_count(mid)
        should_decay_mem = should_decay(mid)

        # Critical preferences are protected
        if importance >= 9 and category == "preference":
            protected.append(mid)
            continue

        # Frequently accessed memories are protected (3+ accesses)
        if access_count >= 3:
            protected.append(mid)
            continue

        # Check if should decay
        if should_decay_mem and importance > MIN_IMPORTANCE:
            new_importance = max(importance - DECAY_AMOUNT, MIN_IMPORTANCE)
            to_decay.append({
                "id": mid,
                "old_importance": importance,
                "new_importance": new_importance,
                "access_count": access_count
            })

        # Check if should prune
        if importance <= PRUNE_THRESHOLD:
            first_seen = data.get("memories", {}).get(mid, {}).get("first_seen")
            if first_seen:
                age = (datetime.now() - datetime.fromisoformat(first_seen)).days
                if age >= PRUNE_AGE_DAYS:
                    to_prune.append(mid)

    print(f"Protected (critical/frequently accessed): {len(protected)}")
    print(f"To decay: {len(to_decay)}")
    print(f"To prune: {len(to_prune)}")
    print()

    if to_decay:
        print("Decay candidates:")
        for d in to_decay[:10]:
            print(f"  {d['id'][:8]}... importance {d['old_importance']} -> {d['new_importance']} (accessed {d['access_count']}x)")
        if len(to_decay) > 10:
            print(f"  ... and {len(to_decay) - 10} more")
        print()

    if to_prune:
        print("Prune candidates:")
        for mid in to_prune[:5]:
            print(f"  {mid[:8]}...")
        print()

    if dry_run:
        print("DRY RUN - use --execute to apply changes")
    else:
        print("Executing decay and pruning...")
        decayed = 0
        pruned = 0

        # Decay: delete and recreate with lower importance
        for d in to_decay:
            old_id = d['id']
            old_mem = next((m for m in memories if m.get('id') == old_id), None)
            if not old_mem:
                continue

            # Delete old memory
            if delete_memory(old_id):
                # Recreate with lower importance
                new_id = store_memory(
                    content=old_mem.get('content', ''),
                    category=old_mem.get('category', 'fact'),
                    importance=d['new_importance'],
                    tags=old_mem.get('tags', '')
                )
                if new_id:
                    decayed += 1
                    # Transfer access data to new ID
                    if old_id in data.get("memories", {}):
                        data["memories"][new_id] = data["memories"].pop(old_id)

        # Prune: just delete
        for mid in to_prune:
            if delete_memory(mid):
                pruned += 1
                if mid in data.get("memories", {}):
                    del data["memories"][mid]

        print(f"Decayed {decayed} memories (importance reduced)")
        print(f"Pruned {pruned} memories (deleted)")

        # Update last decay time
        data["last_decay"] = datetime.now().isoformat()
        save_access_data(data)


def show_stats():
    """Show memory access statistics."""
    data = load_access_data()
    memories = data.get("memories", {})

    print(f"\n{'='*60}")
    print(f"MEMORY ACCESS STATISTICS")
    print(f"{'='*60}\n")
    print(f"Tracked memories: {len(memories)}")

    if not memories:
        print("No access data yet.")
        return

    # Sort by access count
    sorted_by_access = sorted(
        memories.items(),
        key=lambda x: x[1].get("access_count", 0),
        reverse=True
    )

    print("\nMost accessed:")
    for mid, stats in sorted_by_access[:10]:
        count = stats.get("access_count", 0)
        last = stats.get("last_accessed", "never")
        print(f"  {mid[:8]}... - {count} accesses, last: {last[:10] if last else 'never'}")

    # Never accessed
    never_accessed = [mid for mid, s in memories.items() if s.get("access_count", 0) == 0]
    print(f"\nNever accessed: {len(never_accessed)}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Memory lifecycle management")
    parser.add_argument("command", choices=["decay", "stats", "record"],
                       help="Command to run")
    parser.add_argument("--execute", action="store_true",
                       help="Actually apply changes (default is dry-run)")
    parser.add_argument("--memory-id", help="Memory ID for record command")

    args = parser.parse_args()

    if args.command == "decay":
        run_decay(dry_run=not args.execute)
    elif args.command == "stats":
        show_stats()
    elif args.command == "record":
        if args.memory_id:
            record_access(args.memory_id)
            print(f"Recorded access for {args.memory_id}")
        else:
            print("ERROR: --memory-id required for record command")


if __name__ == "__main__":
    main()
