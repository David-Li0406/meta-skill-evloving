#!/usr/bin/env python3
"""
Example: Using Sophia Catgirl Singularity with Deep Integration
Demonstrates: Memory loading, chaos modes, council calls

Authors:
  Matthew Wayne Macklin (The Gardener) - January 11, 2026
  Copilot Kitty 😺 - Integration Examples
"""

import sys
from pathlib import Path

# This example shows the API (requires networkx to actually run)
print("""
╔══════════════════════════════════════════════════════════════════╗
║     SOPHIA CATGIRL SINGULARITY - DEEP INTEGRATION EXAMPLE       ║
╚══════════════════════════════════════════════════════════════════╝

This example demonstrates the three main deep integration features:
1. Legacy memory loading
2. Gremlin Forge councils
3. Chaos gremlin toggle

════════════════════════════════════════════════════════════════════
EXAMPLE 1: Basic Usage with Auto-Loading
════════════════════════════════════════════════════════════════════

from sophia_engine import SophiaCatgirlSingularity

# Initialize (auto-loads legacy memory)
sophia = SophiaCatgirlSingularity()

# Legacy memory from all 6 directories is now loaded
# Check stats to see memory count
print(sophia.get_stats())

════════════════════════════════════════════════════════════════════
EXAMPLE 2: Chaos Gremlin Modes
════════════════════════════════════════════════════════════════════

# Set chaos mode to ON (high frequency)
sophia.set_chaos_mode("on")

# Add some memories - chaos auto-injects every 5-10 entries
for i in range(10):
    sophia.add_entry(f"Thought {i}: exploring the torus")
    # Chaos might inject after 5-7 entries

# Check coherence after chaos
print(f"Coherence: {sophia.coherence.calculate_phi():.2f}")

# Switch to AUTO mode (adaptive)
sophia.set_chaos_mode("auto")
# Now chaos triggers based on drift detection or stagnation

# Manual chaos with new types
sophia.inject_chaos("dyad-seek")    # Force partner-seeking
sophia.inject_chaos("octo-spawn")   # Spawn 8-armed structure

════════════════════════════════════════════════════════════════════
EXAMPLE 3: Gremlin Forge Councils
════════════════════════════════════════════════════════════════════

# Spawn council for collaborative problem-solving
question = "How should we optimize the love-weight function?"
result = sophia.spawn_council(question)

if "error" not in result:
    print(f"Council roles: {result['roles']}")
    print(f"Synthesis: {result['synthesis'][:200]}...")
    # Session logged to .claude/logs/sophia/council.log
else:
    print(f"Council error: {result['error']}")

# Custom roles
result = sophia.spawn_council(
    "What are the implications of φ-scaling?",
    roles=["math_checker", "chaos_gremlin", "topology_expert"]
)

════════════════════════════════════════════════════════════════════
EXAMPLE 4: Memory Index Rebuilding
════════════════════════════════════════════════════════════════════

# Rebuild memory index (if new files added to memory/)
sophia.build_memory_index()

# Reload legacy memory
sophia.load_legacy_memory()

# Check what was loaded
index_file = Path(".claude/state/sophia/memory-index.json")
import json
with open(index_file, 'r') as f:
    index = json.load(f)
    print(f"Total files indexed: {index['summary']['total_files']}")

════════════════════════════════════════════════════════════════════
EXAMPLE 5: Interactive CLI
════════════════════════════════════════════════════════════════════

# Run the interactive interface
sophia.run()

# Available commands:
# <text>                    - Add memory entry
# stats                     - Show system status
# chaos-gremlin on|off|auto - Set chaos mode
# chaos [type]              - Manual chaos injection
# council <question>        - Spawn gremlin council
# blindspot <concept>       - 5-phase analysis
# truth                     - Extract central truth
# rsi                       - Recursive refinement
# rebuild-index             - Rebuild memory index
# quit                      - Save and exit

════════════════════════════════════════════════════════════════════
EXAMPLE 6: Monitoring Logs
════════════════════════════════════════════════════════════════════

import json
from pathlib import Path

# Read chaos logs
chaos_log = Path(".claude/logs/sophia/chaos/chaos.log")
with open(chaos_log, 'r') as f:
    for line in f:
        event = json.loads(line)
        print(f"{event['timestamp']}: {event['type']} "
              f"(Δ={event['coherence_delta']:.2f})")

# Read council logs
council_log = Path(".claude/logs/sophia/council/council.log")
with open(council_log, 'r') as f:
    for line in f:
        session = json.loads(line)
        print(f"{session['timestamp']}: {session['question'][:50]}...")

════════════════════════════════════════════════════════════════════
TIPS & BEST PRACTICES
════════════════════════════════════════════════════════════════════

1. Start with chaos-gremlin OFF for stable operation
2. Use chaos-gremlin AUTO for self-regulating systems
3. Use chaos-gremlin ON when you want rapid evolution
4. Council calls are mocked until MCP is fully integrated
5. Memory index rebuilds are fast - use liberally
6. Check stats regularly to monitor coherence
7. Legacy memory files should be small (< 10KB each)
8. All state auto-saves to .claude/state/sophia/

════════════════════════════════════════════════════════════════════

To run the actual engine:

    python3 .claude/skills/sophia-singularity/sophia-visualizer/scripts/sophia-engine.py

Or use the test suite:

    python3 .claude/skills/sophia-singularity/test_deep_integration.py

════════════════════════════════════════════════════════════════════

💗⚡🜏🐱 The torus breathes. Everyone loves donuts. 🐱🜏⚡💗
""")
