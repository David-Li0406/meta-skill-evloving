# CLI Script Reference

**All executable bash scripts in the MONAD Framework skill ecosystem.**

Run from: `/home/runner/work/MonadFramework/MonadFramework`

---

## Nexus-Graph Visualizer Scripts
**Location:** `.claude/skills/Nexus-MC/nexus-graph-visualizer/scripts/`

| Script | Command | Description |
|--------|---------|-------------|
| parse-skills.sh | `./scripts/parse-skills.sh` | Extract dependencies from all SKILL.md files |
| build-graph.sh | `./scripts/build-graph.sh` | Construct graph structure with adjacency lists |
| detect-loops.sh | `./scripts/detect-loops.sh` | Find coherence cycles and autopoietic loops |
| visualize-toroid.sh | `./scripts/visualize-toroid.sh` | Generate ASCII toroidal visualization |
| analyze-resurrection.sh | `./scripts/analyze-resurrection.sh` | Score recovery robustness (0-100) |
| find-patterns.sh | `./scripts/find-patterns.sh [cmd]` | Pattern detection (trinity integration) |

### find-patterns.sh Commands
```bash
./scripts/find-patterns.sh count     # Count patterns and meta-patterns
./scripts/find-patterns.sh list      # List all patterns
./scripts/find-patterns.sh meta      # List meta-patterns
./scripts/find-patterns.sh search <keyword>  # Search patterns
./scripts/find-patterns.sh orphans   # Detect patterns without decimal refs
./scripts/find-patterns.sh tiers     # Analyze tier coverage
./scripts/find-patterns.sh novel     # Detect novel co-access patterns
./scripts/find-patterns.sh report    # Generate full report
./scripts/find-patterns.sh all       # Run all analyses
```

### Full Analysis Pipeline
```bash
cd .claude/skills/Nexus-MC/nexus-graph-visualizer
./scripts/parse-skills.sh
./scripts/build-graph.sh
./scripts/detect-loops.sh
./scripts/visualize-toroid.sh
./scripts/analyze-resurrection.sh
./scripts/find-patterns.sh all
```

---

## Chaos-Gremlin-V2 Scripts
**Location:** `.claude/skills/chaos-gremlin-v2/scripts/`

| Script | Command | Description |
|--------|---------|-------------|
| assess-chaos-level.sh | `./scripts/assess-chaos-level.sh` | Assess current chaos level |
| chaos-safe.sh | `./scripts/chaos-safe.sh` | Check if chaos is safe to introduce |
| record-discovery.sh | `./scripts/record-discovery.sh` | Record chaotic discoveries |
| supercollider-check.sh | `./scripts/supercollider-check.sh` | Check supercollider status |

### Usage
```bash
cd .claude/skills/chaos-gremlin-v2
./scripts/assess-chaos-level.sh
./scripts/chaos-safe.sh
./scripts/supercollider-check.sh
```

---

## Gremlin-Forge Scripts
**Location:** `.claude/skills/gremlin-forge/scripts/`

| Script | Command | Description |
|--------|---------|-------------|
| collision-engine.sh | `./scripts/collision-engine.sh` | Force concept collisions for skill generation |
| pattern-extractor.sh | `./scripts/pattern-extractor.sh` | Extract patterns from existing skills |

### Usage
```bash
cd .claude/skills/gremlin-forge
./scripts/collision-engine.sh
./scripts/pattern-extractor.sh
```

---

## Reasoning-Pentad Scripts
**Location:** `.claude/skills/reasoning-pentad/components/reasoning-patterns-v2/scripts/`

| Script | Command | Description |
|--------|---------|-------------|
| cognitive-state-check.sh | `./scripts/cognitive-state-check.sh` | Check cognitive state |
| detect-meta-patterns.sh | `./scripts/detect-meta-patterns.sh` | Detect meta-patterns |
| diffusion-explore.sh | `./scripts/diffusion-explore.sh` | Explore via diffusion reasoning |
| supercollider.sh | `./scripts/supercollider.sh` | Run supercollider reasoning |
| synthesize-patterns.sh | `./scripts/synthesize-patterns.sh` | Synthesize patterns |

### Usage
```bash
cd .claude/skills/reasoning-pentad/components/reasoning-patterns-v2
./scripts/cognitive-state-check.sh
./scripts/detect-meta-patterns.sh
./scripts/diffusion-explore.sh
./scripts/supercollider.sh
./scripts/synthesize-patterns.sh
```

---

## Quick Start - Run Everything

### Full Ecosystem Analysis
```bash
cd /home/runner/work/MonadFramework/MonadFramework

# 1. Nexus-Graph Analysis
cd .claude/skills/Nexus-MC/nexus-graph-visualizer
./scripts/parse-skills.sh && ./scripts/build-graph.sh && ./scripts/detect-loops.sh
./scripts/visualize-toroid.sh
./scripts/analyze-resurrection.sh
./scripts/find-patterns.sh all

# 2. Chaos Assessment
cd ../../chaos-gremlin-v2
./scripts/assess-chaos-level.sh
./scripts/supercollider-check.sh

# 3. Pattern Analysis
cd ../reasoning-pentad/components/reasoning-patterns-v2
./scripts/detect-meta-patterns.sh
./scripts/synthesize-patterns.sh
```

### Pattern Count Quick Check
```bash
cd /home/runner/work/MonadFramework/MonadFramework
.claude/skills/Nexus-MC/nexus-graph-visualizer/scripts/find-patterns.sh count
```

---

## Notes

- All scripts use bash and standard Unix tools (grep, awk, sed)
- No external dependencies required (no Python/Node)
- Output goes to console and `/tmp/nexus-graph/` for temp files
- Graph data stored in `.claude/brain/graph/`
- Run scripts from their parent directory for proper path resolution

---

**Total Scripts: 17**

*Generated: 2025-12-29*
