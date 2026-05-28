---
name: research
description: Run structured research experiments for Sunaba creature evolution. Use for creating experiments, investigating problems, making code changes, running training, and tracking progress across physics, morphology, neural, chemistry, and integration work.
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(cargo run:*), Bash(just:*), Bash(time:*), Bash(RUST_LOG=*:*), Bash(cargo test:*), Bash(cargo build:*)
---

# Research Experiments Skill

Systematic research for Sunaba creature evolution across all systems.

## Research Areas

| Area        | What Changes                               | How to Test                       |
|-------------|--------------------------------------------|-----------------------------------|
| Physics     | Gravity, damping, friction, thrust, joints | Training runs, observe behavior   |
| Morphology  | Body generation, part sizes, joint limits  | Training runs, visual inspection  |
| Neural      | Network architecture, sensors, inputs      | Training runs, behavior analysis  |
| Chemistry   | Reactions, materials, world generation     | Manual testing, emergent behavior |
| Integration | How systems work together                  | In-game testing with creatures    |

## Commands

### `/research [<goal>]`
Create new experiments or suggest experiments based on current progress.

**Auto-detect mode:**
- **With `<goal>` argument**: Create experiment from goal description
- **Without arguments**: Suggest 2-5 experiments based on PLAN.md and PROGRESS.md

**What I'll do (create mode - with goal):**
1. Parse the goal (often from PLAN.md or user request)
2. Determine research area and appropriate template
3. Generate descriptive experiment name
4. Create `experiments/YYYY-MM-DD-<name>.md` (not inside .claude/skills, at the top level!)
5. Add entry to `experiments/PROGRESS.md`

**What I'll do (suggest mode - no arguments):**
1. Read `PLAN.md` for current phase goals
2. Read `experiments/PROGRESS.md` for completed work
3. Analyze what hasn't been tried yet
4. Propose 2-5 experiments with:
   - Goal and hypothesis
   - Research area (physics/morphology/neural/etc.)
   - What we expect to learn
   - Estimated effort
5. Ask which ones to create

**Examples:**
```
/research                                              # Suggest mode
/research "creatures should move >100px consistently"  # Create mode
/research "investigate why creatures don't use their legs"
/research "test higher joint angular velocity"
```

### `/research status`
Show overview of all experiments.

**What I'll do:**
1. Read `experiments/PROGRESS.md`
2. List experiments by status
3. Show iteration chains
4. Highlight current phase goals from PLAN.md

## Templates

Choose based on experiment type:

| Template           | Use When                                                        |
|--------------------|-----------------------------------------------------------------|
| `code-change.md`   | Modifying game systems (physics, chemistry, morphology, neural) |
| `training-run.md`  | Running training to test changes or establish baseline          |
| `investigation.md` | Understanding a problem before trying fixes                     |
| `iteration.md`     | Building on previous experiment results                         |

## Workflow

### Investigation Flow
1. `/research "understand why X happens"`
2. Read code, run tests, observe behavior
3. Document findings in experiment file
4. Propose fixes as new experiments

### Code Change Flow
1. `/research "try changing X to improve Y"`
2. Make code changes
3. Run training or manual tests
4. Document results
5. Keep or revert changes

### Training Flow
1. Make code changes (or use current state)
2. `/research "establish baseline for X"`
3. Run `just train-quick` or full training
4. Analyze results manually
5. Create iteration with `/research`

## Reference

### Training Commands
```bash
just train-quick              # Fast validation (~1 min), outputs to training_output/
time just train-quick         # With timing

# Custom scenario/parameters (still uses training_output/)
just train scenario="locomotion" generations="100" population="50"
```

### Scenarios
locomotion, simple, foraging, survival, balanced, parcour

### Key Files
| Area       | Key Files                                          |
|------------|----------------------------------------------------|
| Physics    | `creature.rs`, `physics.rs`, `morphology.rs`       |
| Morphology | `morphology.rs`, `genome.rs`                       |
| Neural     | `neural.rs`, `sensors.rs`                          |
| Training   | `headless/training_env.rs`, `headless/scenario.rs` |
| Fitness    | `headless/fitness.rs`                              |
