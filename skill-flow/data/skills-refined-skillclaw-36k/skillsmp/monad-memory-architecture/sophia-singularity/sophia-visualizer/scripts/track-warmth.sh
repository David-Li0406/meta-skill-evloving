#!/usr/bin/env bash
# track-warmth.sh - Warmth tracking with permanent logging

PYTHON=${PYTHON:-python3}
LOG_DIR="${CLAUDE_LOGS:-$HOME/.claude/logs}/sophia/warmth"
mkdir -p "$LOG_DIR"

$PYTHON << 'PYEOF'
import json, os
from datetime import datetime

STATE = os.path.expanduser("~/.claude/state/sophia/singularity_state.json")
LOG_DIR = os.path.expanduser(os.environ.get('CLAUDE_LOGS', '~/.claude/logs') + '/sophia/warmth')
os.makedirs(LOG_DIR, exist_ok=True)

try:
    with open(STATE) as f:
        data = json.load(f)
    
    warmth = data.get('warmth', 40)
    
    # Determine state
    if warmth < 30:
        state = "Cold/Tsundere 😾"
        ears = "ears back, tail twitching"
    elif warmth < 60:
        state = "Warming 😺"
        ears = "ears perked, tail swaying"
    else:
        state = "Fully Warm 😻✨"
        ears = "ears forward, wings visible"
    
    # Nya frequency
    nya_freq = int((0.3 + warmth/200) * 100)
    
    # Log to permanent storage
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'warmth': warmth,
        'state': state,
        'nya_frequency': nya_freq
    }
    with open(os.path.join(LOG_DIR, 'warmth_history.jsonl'), 'a') as log:
        log.write(json.dumps(log_entry) + '\n')
    
    print(f"WARMTH TRACKER")
    print(f"")
    print(f"Current: {warmth}/100 - {state}")
    print(f"Physical: {ears}")
    print(f"Nya Frequency: {nya_freq}% (≈{max(1, nya_freq//20)}-{max(2, nya_freq//15)} per response)")
    print(f"")
    print(f"Warmth Graph:")
    print(f" 100│{'●' if warmth >= 80 else ' '}")
    print(f"  80│{'●' if warmth >= 60 else ' '}")
    print(f"  60│{'●' if warmth >= 40 else ' '} ← Threshold (warm state)")
    print(f"  40│{'●' if warmth >= 20 else ' '}")
    print(f"  20│{'●' if warmth < 20 else ' '}")
    print(f"   0└─────")
    print(f"")
    print(f"Logs: {LOG_DIR}")

except FileNotFoundError:
    print(f"No state found at {STATE}")
    print("Initialize system first with sophia-engine.py")
PYEOF
