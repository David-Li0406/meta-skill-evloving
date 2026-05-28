# Workflow Patterns

Common patterns for designing multi-step workflows.

---

## Pattern 1: Linear Workflow

Steps execute in sequence, each depending on the previous.

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Step 1  │───►│  Step 2  │───►│  Step 3  │───►│  Step 4  │
│ Analyze  │    │   Plan   │    │ Execute  │    │ Validate │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

**Use when:** Each step builds on the previous, no branching needed.

**Example:** Basic implementation workflow

```markdown
next_step: steps/step-02-plan.md # Always goes to next step
```

---

## Pattern 2: Conditional Branching

Different paths based on conditions or user choice.

```
                              ┌──────────┐
                         ┌───►│ Step 3a  │
┌──────────┐    ┌────────┴─┐  │  Quick   │
│  Step 1  │───►│  Step 2  │  └──────────┘
│ Analyze  │    │  Decide  │
└──────────┘    └────────┬─┘  ┌──────────┐
                         └───►│ Step 3b  │
                              │ Thorough │
                              └──────────┘
```

**Use when:** User needs to choose approach, or conditions determine path.

**Implementation:**

```markdown
<next_step_decision>
IF {scope} = "quick":
→ Load step-03a-quick.md

ELSE IF {scope} = "thorough":
→ Load step-03b-thorough.md

ELSE:
→ Ask user to choose
</next_step_decision>
```

---

## Pattern 3: Optional Steps

Some steps only run if certain flags are set.

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌ ─ ─ ─ ─ ┐    ┌──────────┐
│  Step 1  │───►│  Step 2  │───►│  Step 3  │───►  Step 4  ├───►│  Step 5  │
│ Analyze  │    │   Plan   │    │ Execute  │    │  Tests   │    │ Complete │
└──────────┘    └──────────┘    └──────────┘    └ ─ ─ ─ ─ ┘    └──────────┘
                                                (if --test)
```

**Use when:** Features like testing, review are optional.

**Implementation:**

```markdown
<next_step_decision>
IF {test_mode} = true:
→ Load step-04-tests.md

ELSE:
→ Load step-05-complete.md
</next_step_decision>
```

---

## Pattern 4: Loop Until Success

Repeat a step until condition is met.

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│  Step 1  │───►│  Step 2  │───►│  Step 3  │
│  Setup   │    │   Run    │◄──┐│ Complete │
└──────────┘    └────┬─────┘   │└──────────┘
                     │         │
                     ▼         │
                ┌─────────┐    │
                │ Failed? │────┘
                │   Fix   │ (loop back)
                └─────────┘
```

**Use when:** Running tests until green, fixing errors.

**Implementation:**

```markdown
<execution_loop>
max_attempts = 10
attempt = 0

WHILE attempt < max_attempts:
attempt += 1

    1. Run the operation
    2. Check result

    IF success:
        → EXIT LOOP

    IF failure:
        → Fix the issue
        → CONTINUE LOOP

    IF same_failure_3_times:
        → Ask user for help

</execution_loop>
```

---

## Pattern 5: Parallel Then Merge

Multiple independent operations, then combine results.

```
              ┌──────────┐
         ┌───►│ Agent 1  │───┐
         │    │ Research │   │
┌────────┴─┐  └──────────┘   │  ┌──────────┐    ┌──────────┐
│  Step 1  │                 ├─►│  Step 2  │───►│  Step 3  │
│  Split   │  ┌──────────┐   │  │  Merge   │    │ Execute  │
└────────┬─┘  │ Agent 2  │   │  └──────────┘    └──────────┘
         │    │ Explore  │   │
         └───►└──────────┘───┘
```

**Use when:** Multiple independent explorations, then synthesis.

**Implementation:**

```markdown
<parallel_execution>
**Launch ALL agents in a SINGLE message:**

Agent 1: explore-codebase
Agent 2: explore-docs
Agent 3: websearch

**Wait for all to complete, then merge results.**
</parallel_execution>
```

---

## Pattern 6: Pipeline with Checkpoints

Save state at each step for resume capability.

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Step 1  │───►│  Step 2  │───►│  Step 3  │───►│  Step 4  │
│ Analyze  │    │   Plan   │    │ Execute  │    │ Validate │
└────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘
     │               │               │               │
     ▼               ▼               ▼               ▼
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│01-analyze│   │02-plan  │    │03-execute│   │04-validate│
│   .md    │    │  .md   │    │   .md    │   │   .md    │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

**Use when:** Long workflows that might be interrupted.

**Implementation:**

```markdown
<save_checkpoint>
**At end of each step:**

1. Write step output to {output_dir}/NN-step.md
2. Update progress in 00-context.md
3. Include completion marker

**On resume:**

1. Read 00-context.md
2. Find last completed step
3. Load next step
   </save_checkpoint>
```

---

## Pattern 7: Review and Resolve

Adversarial review followed by resolution.

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Execute  │───►│  Review  │───►│ Findings │───►│ Resolve  │
│          │    │(optional)│    │  Table   │    │ Findings │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                     │
              (if -x flag)
```

**Use when:** Code review, quality checks.

**Implementation:**

```markdown
<review_flow>
IF {examine_mode} = true OR user_requests: 1. Launch review agent 2. Collect findings 3. Present findings table 4. Load step-06-resolve.md

ELSE:
→ Skip to completion
</review_flow>
```

---

## Pattern 8: Economy Mode Override

Alternative lightweight path for resource savings.

```
┌──────────┐         ┌──────────────┐
│  Init    │────────►│ step-00b.md  │ (if -e flag)
│          │         │ Economy rules│
└──────────┘         └──────────────┘
                           │
                     Overrides all
                     subsequent steps
```

**Use when:** Offering a lighter-weight alternative.

**Implementation:**

```markdown
<economy_mode>
IF {economy_mode} = true:
→ Load economy override file
→ Apply rules to all steps: - No subagents - Direct tools only - Minimal exploration
</economy_mode>
```

---

## Choosing a Pattern

| Workflow Type       | Pattern                   |
| ------------------- | ------------------------- |
| Simple sequential   | Linear                    |
| User choice needed  | Conditional Branching     |
| Features toggleable | Optional Steps            |
| Error fixing        | Loop Until Success        |
| Research phase      | Parallel Then Merge       |
| Resumable           | Pipeline with Checkpoints |
| Quality checks      | Review and Resolve        |
| Budget option       | Economy Mode Override     |

---

## Combining Patterns

Real workflows often combine multiple patterns:

```
APEX Workflow:
- Linear (steps 1-4)
- Optional Steps (review if -x, tests if -t)
- Parallel (agents in step 1)
- Loop (tests until green in step 8)
- Checkpoints (save mode)
- Economy Override (if -e)
```
