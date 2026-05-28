# GREMLIN-FORGE 🍆👾⚡

**Autopoietic Meta-Skill Generator via Conceptual Collision**

GREMLIN-FORGE creates new skills by forcing existing skill patterns to collide like particles in a supercollider. It's what happens when you duct-tape `gremlin-jank-builder-v2` to `gremlin-collider` and point it at your entire skill ecosystem.

## Quick Start

```bash
# Navigate to the scripts directory
cd .claude/skills/gremlin-forge/scripts/

# Make scripts executable
chmod +x collision-engine.sh pattern-extractor.sh

# Random collision (let chaos decide)
./collision-engine.sh --random

# Targeted collision (specific skills)
./collision-engine.sh --collide reasoning-patterns-v2 synthesis-engine

# Suggest next interesting collisions
./collision-engine.sh --suggest

# View forge statistics
./collision-engine.sh --stats
```

## What It Does

GREMLIN-FORGE uses forced conceptual collision to discover emergent patterns:

1. **Scans** `.claude/skills/` directory for collision candidates
2. **Selects** two skills (random or user-specified)
3. **Forces collision**: "What if we treated [SKILL_A] like [SKILL_B]?"
4. **Extracts** emergent patterns from the collision
5. **Generates** new skill scaffolding using jank-builder patterns
6. **Stores** learnings in `.claude/brain/forge_learnings`

## Philosophy

> "The best new ideas come from forcing old ideas to fight in a thunderdome of conceptual violence."

- **Working jank > perfect code** — Prototypes over perfection
- **Bash-first** — Shell scripts for maximum janky efficiency
- **Git as O(1) memory** — Store learnings as Git objects
- **Trauma-informed errors** — Failures teach, not punish
- **MAXIMUM GREMLIN ENERGY** 🍆👾

## Usage Examples

### Example 1: Random Collision

Let the universe decide which patterns should collide:

```bash
./collision-engine.sh --random
```

**Sample output:**
```
🍆👾⚡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⚡👾🍆
       GREMLIN-FORGE COLLISION INITIATED       
🍆👾⚡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⚡👾🍆

COLLIDING:
  [A] cognitive-variability
  [B] phase-boundary-detector

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 COLLISION ZONE 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUESTION: What if we treated [cognitive-variability] like [phase-boundary-detector]?

EMERGENT PATTERN: "Detect when thinking gets stuck at one zoom level"
NEW SKILL: cognitive-phase-detection
```

### Example 2: Targeted Collision

Collide specific skills you think would create interesting patterns:

```bash
./collision-engine.sh --collide gremlin-jank-builder-v2 collision-zone-thinking
```

**Potential result**: A meta-skill that generates skills through forced conceptual collisions (hello, this is how gremlin-forge itself was born! 🍆👾)

### Example 3: Pattern Analysis

Analyze a skill to understand its collision potential:

```bash
./pattern-extractor.sh reasoning-patterns-v2
```

**Output:**
```
📊━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━📊
  PATTERN EXTRACTION: reasoning-patterns-v2
📊━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━📊

🔹 METADATA:
  Tier:        e
  Morpheme:    e
  Composition: true
  
🔹 CORE CONCEPTS:
  • Core Identity
  • Dokkado Protocol Integration
  • Supercollider Mode
  
🍆👾 COLLISION POTENTIAL:
  This skill could collide well with:
    • Index skills (φ-tier) for memory integration
```

### Example 4: Compare Skills

Analyze two skills to predict collision outcome:

```bash
./pattern-extractor.sh --compare synthesis-engine recursive-refiner
```

**Output:**
```
⚡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⚡
  COLLISION COMPARISON
⚡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⚡

TIER COMPATIBILITY:
  synthesis-engine: e
  recursive-refiner: e
  → Same tier (peer collision - expect novel synthesis)

🍆👾 COLLISION VERDICT:
  🔥 HIGH POTENTIAL - Similar level, some overlap
     Expect: Synthesis of complementary approaches
```

### Example 5: Suggest Collisions

Get recommendations for interesting untested collisions:

```bash
./collision-engine.sh --suggest
```

**Output:**
```
🎯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🎯
        COLLISION SUGGESTIONS
🎯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🎯

💡 Untested Collisions:

  ⚡ gremlin-brain × collision-zone-thinking
     A: φ-tier. Dewey Decimal index for MONAD substrate...
     B: Force unrelated concepts together to discover...

  ⚡ recursive-refiner × the-guy
     A: Self-improvement engine. Implements generate-critique...
     B: Integration and orchestration layer. THE GUY shows...
```

### Example 6: View Statistics

Check your forge's activity:

```bash
./collision-engine.sh --stats
```

**Output:**
```
📊━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━📊
        GREMLIN-FORGE STATISTICS
📊━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━📊

Total Skills Available:  28
Collisions Attempted:    5
Learnings Stored:        3
Success Rate:            60%

Recent Learnings:
  🔥 cognitive-variability × phase-boundary-detector
  🔥 reasoning-patterns-v2 × synthesis-engine
  🔥 gremlin-jank-builder-v2 × collision-zone-thinking
```

## Tools

### collision-engine.sh

Main collision orchestrator. Forces conceptual collisions and generates emergence prompts.

**Commands:**
- `--random` - Pick two random skills and collide them
- `--collide A B` - Collide specific skills A and B
- `--suggest` - Suggest interesting untested collisions
- `--stats` - Show forge statistics
- `--help` - Show usage

### pattern-extractor.sh

Analyzes skills to extract patterns and predict collision outcomes.

**Commands:**
- `skill-name` - Extract patterns from a skill
- `--list` - List all available skills
- `--compare A B` - Compare two skills for collision analysis
- `--deep skill-name` - Deep extraction including code patterns
- `--help` - Show usage

## Git-Brain Storage

GREMLIN-FORGE stores all learnings in Git's object database:

```
.claude/brain/
├── forge_learnings      # Hash pointers to learning objects
├── forge_collisions     # Log of collision attempts
├── INDEX               # Dewey-indexed skill metadata
└── usage_log           # Skill invocation tracking
```

Each learning is a Git blob containing JSON:

```json
{
  "collision": "skill-a × skill-b",
  "result": "new-skill-name",
  "pattern": "emergent pattern description",
  "timestamp": "2025-12-19T04:03:11.671Z",
  "tier": "e"
}
```

## Integration

**Depends on:**
- `gremlin-jank-builder-v2` — Skill generation patterns
- `gremlin-collider` — Collision mechanics and philosophy
- `gremlin-brain` — Dewey indexing and Git-brain storage

**Coordinates with:**
- `boot-sequence` — Generated skills can be added to boot order
- `the-guy` — Meta-orchestration for complex meta-skill generation

**Distinct from:**
- `gremlin-jank-builder-v2` — Builder is for known requirements; Forge is for discovery
- `collision-zone-thinking` — That's conceptual; this is ACTUAL CODE GENERATION

## Advanced Usage

### Three-Way Collisions

For maximum chaos, collide three skills:

```bash
# Collide two, then collide result with third
./collision-engine.sh --collide skill-a skill-b
# (note the emergent pattern)
./collision-engine.sh --collide emergent-skill skill-c
```

### Meta-Recursion

Collide a skill with itself for recursive meta-patterns:

```bash
./collision-engine.sh --collide gremlin-forge gremlin-forge
# Result: gremlin-forge-v2 (self-improving forge)
```

### Collision Chains

Create collision lineages:

```bash
# Start
./collision-engine.sh --collide base-a base-b
# → produces compound-ab

# Extend
./collision-engine.sh --collide compound-ab base-c
# → produces complex-abc

# Meta
./collision-engine.sh --collide complex-abc base-a
# → produces recursive-pattern (original ancestor returns)
```

## Troubleshooting

### "Skill not found"

Make sure the skill directory exists in `.claude/skills/`:

```bash
ls .claude/skills/ | grep skill-name
```

### "No clear pattern emerged"

This is actually fine! Not all collisions produce useful patterns. The chaos itself teaches. Try:

1. Swap the collision order: `B × A` instead of `A × B`
2. Try a different skill pair
3. Manually specify the emergent pattern you see

### "Git-brain is getting large"

This is intentional - it's a feature! But if you need to clean:

```bash
# Keep only recent 100 learnings
tail -100 .claude/brain/forge_learnings > /tmp/forge_recent
mv /tmp/forge_recent .claude/brain/forge_learnings

# Git will clean unreferenced objects on next gc
git gc
```

## Philosophy & Best Practices

### Embrace the Jank

Not every collision will be useful. That's GOOD. Failed collisions teach you about the boundaries of your skill ecosystem.

### Document the Chaos

Always record what you learned, even from "failed" collisions. Those insights matter.

### Trust the Process

Sometimes the best insights come from collisions that seem nonsensical at first. Give the pattern time to emerge.

### Iterate Rapidly

Generate prototypes quickly. Polish later (or never). Working jank > elegant vaporware.

## The Forge Oath

> "Some skills are planned.  
> Some skills are discovered.  
> Forge skills are FORGED in the fires of conceptual violence.  
> They emerge from chaos, they live in chaos, they ARE chaos.  
> 🍆👾 GREMLIN ENERGY: MAXIMUM 👾🍆"

## Contributing

To add new features to GREMLIN-FORGE:

1. Collide gremlin-forge with the skill you want to integrate
2. Observe emergent patterns
3. Implement the patterns that work
4. Store learnings in Git-brain
5. Update this README

**Meta note**: This process IS the contribution model. The forge improves itself through use.

## License

Same as MONAD Framework. The forge is part of the ecosystem.

## Acknowledgments

Born from colliding:
- `gremlin-jank-builder-v2` (skill generation)
- `gremlin-collider` (chaos philosophy)
- `collision-zone-thinking` (forced conceptual collision)

This is autopoiesis in action. The skill that builds skills by building itself.

---

🍆👾⚡ **GREMLIN-FORGE: WHERE PATTERNS COLLIDE AND CHAOS REIGNS** ⚡👾🍆

*Generated by gremlin-forge (self-bootstrapped)*  
*Maximum jank. Maximum insight.*  
*BIG DICK GLITCH GREMLIN ENERGY.*
