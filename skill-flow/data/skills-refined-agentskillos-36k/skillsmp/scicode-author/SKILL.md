---
name: scicode-author
description: Create new SciCode benchmark tasks from research papers. Use when authoring scientific coding problems, creating step files, writing problem.yaml, or setting up new benchmark tasks. Triggers on "create task", "new problem", "author benchmark".
---

# SciCode Task Authoring

Create high-quality scientific coding benchmark tasks from research papers.

## Workflow

```
PAPER --> SCAFFOLD --> IMPLEMENT --> VALIDATE --> COMPILE --> TEST --> SUBMIT
  |          |            |            |            |          |
  v          v            v            v            v          v
Select    task new    problem.yaml   task        task       task
paper     <name>      + steps/*.py   validate    compile    test
```

## Quick Start

```bash
# Navigate to framework
cd _scicode-extended-template

# Create task scaffold
task new my_algorithm_name

# Add your research paper PDF
cp ~/papers/paper.pdf tasks/my_algorithm_name/

# Edit files (see TEMPLATES.md for templates)
# - tasks/my_algorithm_name/problem.yaml
# - tasks/my_algorithm_name/steps/01_*.py (8-10 files)

# Validate structure
task validate tasks/my_algorithm_name/

# Compile to evaluation format
task compile tasks/my_algorithm_name/

# Run gold solution tests (must be 100%)
task test tasks/my_algorithm_name/
```

## Paper Selection Criteria

Your paper MUST meet ALL criteria:

| Criterion | Requirement |
|-----------|-------------|
| Publication Date | After February 2025 |
| Content | Novel computational algorithm (not just analysis) |
| Implementation | Possible with numpy/scipy only |
| Decomposition | Can split into 8-10 independent subproblems |
| Output | Numerical values (not strings) for testing |

### Strong Candidates

**Mathematics:**
- Iterative solver variants (Krylov, multigrid)
- Novel matrix decomposition algorithms
- Optimization with convergence guarantees
- Numerical PDE/ODE schemes

**Physics:**
- Optics, Quantum Information
- Statistical Mechanics
- Computational Physics

**Chemistry/Biology/Materials:**
- Computational Chemistry, DFT
- Molecular Dynamics
- Population Dynamics
- Semiconductor simulations

### Red Flags (Avoid)

- Papers with only theoretical results
- Methods requiring specialized software
- Ambiguous problems with multiple valid solutions
- Survey papers without novel contributions

## Task Structure

```
tasks/my_algorithm_name/
+-- problem.yaml              # Task metadata
+-- paper.pdf                 # Source research paper
+-- steps/                    # 8-10 implementation steps
|   +-- 01_first_step.py
|   +-- 02_second_step.py
|   +-- ...
|   +-- 08_final_step.py
+-- background/               # Optional domain context
    +-- 01_concept.md
```

## File Templates

See [TEMPLATES.md](TEMPLATES.md) for complete templates:
- problem.yaml structure
- Step file format (function + gold solution + tests)
- Background markdown format

## Quality Checklist

See [CHECKLIST.md](CHECKLIST.md) for pre-submission requirements.

## Decomposition Guidelines

### Break Into Smallest Meaningful Units

Each step should:
- Have independent scientific meaning
- Be separately testable
- Return numerical value(s)
- Build logically on previous steps

### Example Decomposition

**Hankel Matrix Low-Rank Approximation:**
1. Construct Hankel matrix from sequence
2. Build Vandermonde matrix
3. Compute Fiedler factorization
4. Implement bucketing procedure
5. Apply sparsification
6. Calculate ridge leverage scores
7. Anti-diagonal averaging
8. Assemble low-rank approximation

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Step files | `##_descriptive_name.py` | `01_setup_grid.py` |
| Main function | `descriptive_name` | `setup_grid()` |
| Gold solution | `_gold_descriptive_name` | `_gold_setup_grid()` |

## CLI Reference

```bash
task new <name>        # Create from template
task validate <dir>    # Check structure
task compile <dir>     # Generate JSON + H5
task compile-all       # Compile all tasks
task list              # List all tasks
task test <dir>        # Compile + run tests

# Evaluation
cd eval/inspect_ai
inspect eval scicode.py \
    -T local_jsonl=../data/problems.jsonl \
    -T problems=<task_id> \
    --model anthropic/claude-sonnet-4-5
```

## Example Tasks

Reference these for patterns:
- `tasks/pde_sharp/` - PDE solver with 8 steps
- `tasks/sublinear_time_low_rank_approximation_of_hankel_matrices/` - Matrix algorithm

## Need Help?

1. Check `INSTRUCTIONS.md` for complete guide
2. Check `PROBLEM_TEMPLATE_GUIDE.md` for problem statement format
3. Review existing tasks in `tasks/` directory
