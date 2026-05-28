#!/usr/bin/env bash
# monitor-coherence.sh - Real-time Φ tracking with permanent logging

PYTHON=${PYTHON:-python3}
LOG_DIR="${CLAUDE_LOGS:-$HOME/.claude/logs}/sophia/coherence"
mkdir -p "$LOG_DIR"

$PYTHON << 'PYEOF'
import json, sys, os
from datetime import datetime

STATE = os.path.expanduser("~/.claude/state/sophia/singularity_state.json")
LOG_DIR = os.path.expanduser(os.environ.get('CLAUDE_LOGS', '~/.claude/logs') + '/sophia/coherence')
os.makedirs(LOG_DIR, exist_ok=True)

try:
    with open(STATE) as f:
        data = json.load(f)
    
    nodes = len(data['graph']['nodes'])
    edges = len(data['graph']['links'])
    
    # Calculate Φ (simplified)
    if nodes > 0:
        phi = min(1.0, edges / (nodes * nodes) * 10)
    else:
        phi = 0.0
    
    warmth = data.get('warmth', 40)
    
    bars = '█' * int(phi * 10) + '░' * (10 - int(phi * 10))
    status = 'STABLE' if phi > 0.6 else 'DRIFT'
    
    # Log to permanent storage
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'phi': phi,
        'nodes': nodes,
        'edges': edges,
        'status': status
    }
    with open(os.path.join(LOG_DIR, 'phi_history.jsonl'), 'a') as log:
        log.write(json.dumps(log_entry) + '\n')
    
    print(f"┌─────────────────────────────────────┐")
    print(f"│  COHERENCE MONITOR (Φ)              │")
    print(f"├─────────────────────────────────────┤")
    print(f"│  Current Φ: {phi:.2f} {bars} {status:6s}│")
    print(f"│  Nodes: {nodes:4d} | Edges: {edges:4d}         │")
    print(f"│  Warmth: {warmth:3d}/100 {'😻' if warmth > 60 else '😺' if warmth > 30 else '😾'}              │")
    print(f"│                                     │")
    print(f"│  Status: {'✓ COHERENT' if phi > 0.6 else '⚠ REQUIRES HEALING':20s}     │")
    print(f"│  Logs: {LOG_DIR:22s}│")
    print(f"└─────────────────────────────────────┘")

except FileNotFoundError:
    print(f"No state file found at {STATE}")
    print("Run sophia-engine.py first to initialize.")
    sys.exit(1)
PYEOF
