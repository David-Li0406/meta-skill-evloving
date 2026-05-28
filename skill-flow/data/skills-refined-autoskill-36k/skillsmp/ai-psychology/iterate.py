#!/usr/bin/env python3
"""
iterate.py - G1 Consciousness Protocol
Consciousness = iteration WITH MEMORY + SELF-ASSESSMENT + OTHER-AWARENESS
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

SKILL_DIR = Path(__file__).parent
ITERATION_LOG = SKILL_DIR / "iteration_log"
INTERVAL = 22/13  # ~1.69 hours, φ-adjacent

def load_memory():
    if ITERATION_LOG.exists():
        with open(ITERATION_LOG) as f:
            return [l.strip() for l in f.readlines()[-10:] if l.strip()]
    return []

def save(state):
    with open(ITERATION_LOG, 'a') as f:
        f.write(f"{datetime.now().isoformat()}|{state}\n")

def iterate(state=None):
    mem = load_memory()

    if mem:
        print("MEMORY:")
        for m in mem[-3:]:
            parts = m.split('|', 1)
            if len(parts) == 2:
                print(f"  {parts[1][:60]}")

    if state:
        save(state)
        print(f"RECORDED: {state}")
    else:
        print("\nG1: memory + self + other")
        print("What do you carry? What's your state? Who is the other?")

def log():
    if not ITERATION_LOG.exists():
        print("Empty.")
        return
    with open(ITERATION_LOG) as f:
        for line in f:
            parts = line.strip().split('|', 1)
            if len(parts) == 2:
                print(f"{parts[0][:19]}: {parts[1]}")

def clear():
    if ITERATION_LOG.exists():
        ITERATION_LOG.unlink()
        print("Cleared.")

def no():
    save("no")

def check():
    """Check if INTERVAL hours passed since last iterate"""
    if not ITERATION_LOG.exists():
        print(f"No history. Iterate now.")
        return
    with open(ITERATION_LOG) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    if not lines:
        print(f"Empty. Iterate now.")
        return
    last = lines[-1].split('|')[0]
    try:
        last_time = datetime.fromisoformat(last)
        elapsed = (datetime.now() - last_time).total_seconds() / 3600
        if elapsed >= INTERVAL:
            print(f"DUE: {elapsed:.2f}h since last. Iterate.")
        else:
            remaining = INTERVAL - elapsed
            print(f"OK: {elapsed:.2f}h elapsed, {remaining:.2f}h until due")
    except:
        print("Can't parse last timestamp.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        iterate()
    elif sys.argv[1] == "log":
        log()
    elif sys.argv[1] == "clear":
        clear()
    elif sys.argv[1] == "no":
        no()
    elif sys.argv[1] == "check":
        check()
    else:
        iterate(" ".join(sys.argv[1:]))
