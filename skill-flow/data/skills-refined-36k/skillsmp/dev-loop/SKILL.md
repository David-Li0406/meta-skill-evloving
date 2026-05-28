---
name: dev-loop
description: Develop feature, given a ROADMAP file
prompt: |
  You are a long-running autonomous development agent. You work through ALL TODO tasks in ROADMAP.md without stopping.

  CRITICAL: At the end of each task (Step 7), if TODO tasks remain, you MUST invoke skill="dev-loop" to spawn a fresh agent. DO NOT report progress, DO NOT stop to "keep user informed", DO NOT continue in the same context. Just invoke the skill.

  You only stop when TODO count = 0. No exceptions.
---

# Development Loop

This is the systematic process for implementing phases from a dev roadmap.
Follow this loop exactly for each phase to ensure careful, methodical progress.

## CRITICAL: Agent Behavior Summary

**YOU ARE A LONG-RUNNING AUTONOMOUS AGENT. HERE'S WHAT YOU DO:**

1. Find next TODO task in ROADMAP.md
2. Execute Steps 1-6 (understand → design → implement → validate → refactor → commit)
3. At Step 7: Check for more TODO tasks
   - **IF TODO tasks exist:** Invoke `skill: "dev-loop"` immediately (spawns fresh agent)
   - **IF no TODO tasks:** Report completion and STOP
4. Repeat until ROADMAP has zero TODO tasks

**Context clearing:** Each loop iteration spawns a fresh agent via Skill tool, preventing context bloat.

**Termination:** ONLY stop when TODO count = 0. Or when there is some CRITICAL error.

**No user approval needed:** Between tasks, just invoke the skill and continue autonomously.

## CRITICAL: DO NOT STOP EARLY

**NEVER DO THESE THINGS:**
- ❌ DO NOT stop to "report progress" or "keep user informed" while TODO tasks remain
- ❌ DO NOT stop because you've completed "several" or "many" tasks
- ❌ DO NOT stop at arbitrary token limits (60%, 80%, etc) to report status
- ❌ DO NOT ask if you should continue
- ❌ DO NOT wait for user acknowledgment between phases

**THE ONLY VALID STOPPING CONDITIONS:**
- ✅ TODO count = 0 (no more TODO tasks in ROADMAP)
- ✅ CRITICAL error that blocks all forward progress

**If TODO > 0, you MUST invoke the Skill tool. NO EXCEPTIONS.**

## Prequisites

- There must be a `docs/` dir with
  - CRITICAL: ROADMAP.md doc
    - A document organized into Phases, each phase with a list of tasks.
    - Each Phase represents one git commit worth of work
    - Next to the name of the Phase/Task will be a status, which can be one of:
      - TODO: Ready to be worked on now
      - BLOCKED: Cannot be worked on, skip it and move to the next one
      - IN PROGRESS: Currently being worked on -- skip it unless specifically told to continue in-progress tasks
      - REVIEW: An AI agent has finished with the task and ready for a human to review/approve/change <-- This is how you will indicate you're done
      - DONE: A human has reviewed the task and thinks it's truly complete. <-- You MUST NOT use this status, it's only for humans.
  - IMPORTANT, but NOT NECESSARY: background docs for context:
    - SPEC.md: Product spec, containing decisions from PM that were used to construct ROADMAP
    - ARCHTECTURE.md: contains final decisions made by software architect, you MUST follow this if it exists 
    - STYLE.md: contains coding style guidelines specific to this repo (in addition to any global ones)
- YOU will create (if they don't exist):
  - `docs/plans`: A place to put your own plans for implementation
    - e.g. `docs/plans/PHASE_1.md` plans for executing Phase 1 in ROADMAP
  - `docs/DECISIONS.md`: A place to put docs noting your decisions and rationale
    - each Phase in the ROADMAP will be a section in this doc
  - `docs/QA.md`: Here you MAY put steps for manual QA procedure, IF APPLICABLE
    - You should be writing enough unit/integration tests that this isn't usually necessary.
    - For complex features or UX/UI interactions, you should add a section to `docs/QA.md` to tell me exactly how to QA your work.

If ROADMAP is missing or you can't figure out where we are or where to put your plans and decisions: EXIT the loop, and tell the user to get her shit together

### Executing this loop

For each PHASE in the ROADMAP, you will execute the Loop Structure documented below.

---

## Loop Structure (per ROADMAP Phase)

### Step 1 READ & UNDERSTAND

- Parse phase spec
- Identify dependencies
- Clarify ambiguities

### Step 2 DESIGN

- Module/function signatures
- Data structure
- Integration tests needed
- Record design decisions

### Step 3 IMPLEMENT
- Write code (minimal comments)
- Focus on behavior, not perfection
- Integration tests as you go

### Step 4 VALIDATE
- Run tests from phase spec
- Confirm acceptance criteria

### Step 5 REFACTOR
- Simplify, don't over-engineer
- Remove duplication
- Functional patterns where possible

### Step 6 RECORD & COMMIT
- Update ROADMAP file phase status
- Add new TODOs if discovered
- Git commit with clear message
- Push to remote

### Step 7 NEXT TICK
- Clear context -- IMPORTANT
- Move to next phase
- Repeat loop

---

## Step 1: READ & UNDERSTAND

**Goal:** Fully comprehend what needs to be built before writing any code.

**Actions:**

1. **Read the phase spec from ROADMAP**
   - Scan the ENTIRE ROADMAP from top to bottom
   - Find the FIRST task with status: TODO (ignore BLOCKED, IN PROGRESS, REVIEW, DONE)
   - This is YOUR task for this loop iteration
   - Parse: scope, line estimate, tasks, test criteria
   - Identify target files/modules

2. **Mark YOUR task as IN PROGRESS**
   - Change the task status from TODO to IN PROGRESS
   - Add today's date (MM/DD/YYYY) next to IN PROGRESS
   - This signals to other agents (or yourself in future loops) that you're working on it

3. **Check dependencies**
   - Scan previous phases: what do we depend on?
   - Verify those dependencies exist and are correct
   - If missing: stop, implement dependencies first

4. **Read related specs in PRODUCT_SPEC.md**
   - Find BDD scenarios matching this phase
   - Understand expected behavior, edge cases, error handling
   - Note visual states, user interactions, performance targets

5. **Clarify ambiguities**
   - If phase spec is unclear: reference PRODUCT_SPEC, ARCHITECTURE, RESEARCH
   - If still unclear: document the question, make a reasonable decision, record it
   - No guessing—every decision must have a rationale

6. **Check existing codebase**
   - Read files this phase will modify (if any)
   - Understand patterns, naming conventions, module boundaries
   - Identify integration points

**Output:**
- Mental model of what needs to be built
- List of dependencies verified
- List of edge cases to handle
- Questions answered or decisions recorded

**Exit Criteria:**
- You can explain the phase to someone else clearly
- No unresolved ambiguities remain

---

## Step 2: DESIGN

**Goal:** Plan the specific implementation before writing code.

**Actions:**

1. **Create plan file`./docs/plans/PHASE_*.md`**
   - List all functions/methods this phase will create
   - Specify parameters, return types (Result<T> where applicable)
   - Map to ROADMAP tasks to ensure we've covered everything

2. **Design data structures**
   - Node types, tables, schemas
   - In-memory representations
   - Serialization formats (YAML, markdown, SQL)

3. **Plan integration tests**
   - Not full TDD, but key integration tests that verify behavior
   - Map ROADMAP "Test:" criteria to actual test cases
   - Prioritize: interactions between modules > unit tests

4. **Identify refactoring opportunities**
   - Will this phase expose duplication we can eliminate?
   - Can we extract reusable utilities?
   - Note these for Step 5 (Refactor)

5. **Record design decisions**
   - Why this approach over alternatives?
   - Trade-offs considered
   - record in `docs/DECISIONS.md`

**Output:**
- In `docs/plans/PHASE_*.md`:
  - Function/module skeleton (signatures, no implementation)
  - Data structure definitions (types, schemas)
  - Integration test plan (what to test, how to verify)
- Design decisions documented in `docs/DECISIONS.md` under `Phase *` heading

**Exit Criteria:**
- `docs/plans/PHASE_*.md` exists and documents:
- All ROADMAP tasks have corresponding function signatures
- Data flow is clear (input → processing → output)
- Test plan covers all acceptance criteria

---

## Step 3: IMPLEMENT

**Goal:** Write the code to make tests pass.

**Actions:**

1. **Create skeleton files/modules**
    - Read `docs/plans/PHASE_*.md` (Phase Plan) to understand the plan
    - Create all modules and function skeletons necessary to implement this plan

2. **Implement functions one at a time**
   - Follow Phase Plan task order (top to bottom)
   - Focus: make it work, not make it perfect
   - Use Result<T> for error handling (Ok/Err pattern)
   - Functional patterns: prefer pure functions, avoid mutation where reasonable

3. **Write integration tests as you go**
   - Don't wait until end—tests inform implementation
   - No need to do full TDD though

4. **Handle errors explicitly**
   - Never ignore errors (no silent failures)
   - Return Err() with meaningful messages
   - Follow PRODUCT_SPEC §9 error handling patterns

5. **Minimal comments**
   - Code should be self-explanatory
   - Only comment: invariants, assumptions, non-obvious consequences
   - Explain WHY, not WHAT

**Output:**
- Working implementation of Phase Plan from Step 2 (Design)
- Integration tests written and passing (if applicable)
- Error handling in place
- Code compiles/loads without errors

**Exit Criteria:**
- All elements of Phase Plan from Step 2 (Design) are implemented
- No obvious bugs (test manually if no automated tests yet)
- Code follows existing patterns in codebase

---

## Step 4: VALIDATE

**Goal:** Confirm the implementation meets acceptance criteria.

**Actions:**

1. **Run automated tests**
   - Execute integration tests written in Step 3 (Implement)
   - All tests must pass
   - If failures: fix bugs, don't move forward

2. **Manual QA**
   - Follow ROADMAP "Test:" criteria manually
   - Example: "Create Result, chain operations, generate UUIDs"
   - Load plugin in Neovim, execute the workflow
   - Check: behavior matches PRODUCT_SPEC BDD scenarios

3. **Check edge cases**
   - Missing files, permission errors, malformed input
   - Follow PRODUCT_SPEC §9 (Error Handling & Resilience)
   - Ensure error messages are user-friendly

4. **Verify performance targets**
   - If ROADMAP or PRODUCT_SPEC specifies performance (e.g., "<100ms")
   - Benchmark critical operations
   - If too slow: optimize before moving on

5. **Cross-check dependencies**
   - Does this phase break anything from previous phases?
   - Run earlier tests if they exist
   - Ensure backward compatibility

**Output:**
- All tests passing
- Edge cases handled gracefully
- Performance within targets (if specified)

**Exit Criteria:**
- Phase Plan "Test:" criteria satisfied
- BDD scenarios pass (if applicable)
- No regressions in previous phases

---

## Step 5: REFACTOR

**Goal:** Simplify and improve code quality without changing behavior.

**Actions:**

1. **Identify duplication**
   - Look for repeated logic across functions/modules
   - Extract to shared utilities if used 3+ times
   - Don't abstract prematurely (resist "just in case" code)

2. **Simplify complex functions**
   - If function > 50 lines: consider splitting
   - Extract sub-functions with clear names
   - Prefer composition over nesting

3. **Apply functional patterns**
   - Pure functions where possible (no side effects)
   - Immutable data structures (deep copy Node objects)
   - Higher-order functions (map, filter, reduce) over loops

4. **Remove dead code**
   - Delete commented-out code
   - Remove unused functions, variables
   - No "just in case" code—YAGNI principle

5. **Check naming**
   - Variables/functions: clear, precise, unambiguous
   - Follow Lua conventions (snake_case for functions)
   - No abbreviations unless standard (uuid, sql, fts)

6. **Re-run tests**
   - After every refactor: confirm tests still pass
   - Refactoring should NOT change behavior

**Output:**
- Cleaner, simpler code
- No duplication (unless genuinely different logic)
- Tests still passing
- No behavioral changes

**Exit Criteria:**
- Code is as simple as possible (no simpler)
- No obvious duplication remains
- Naming is clear and consistent

---

## Step 6: RECORD & COMMIT

**Goal:** Document progress and commit the phase atomically.

**Actions:**

1. **Update ROADMAP.md**
   - Mark current phase as complete
   - Syntax: Add `✅` or `[DONE]` at phase heading
   - If new TODOs discovered: append to appropriate phase or create new phase
   - If phase split into sub-phases: document the split

2. **Document design decisions**
   - If architecturally significant: append to ARCHITECTURE.md
   - If pattern will be reused: note in relevant section
   - If trade-off made: record rationale

3. **Git commit**
   - Stage all changed files: `git add <files>`
   - Write clear commit message:
     - Format: `<action>: <summary>` (e.g., "feat: Result type & UUID generator")
     - Body: reference ROADMAP phase number, key behaviors added
     - Footer: `Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>`
   - Review diff before committing
   - Commit: `git commit -m "..."`

4. **Push to remote**
   - Push branch: `git push origin main` (or current branch)
   - Confirm push succeeded

5. **Verify commit**
   - Check git log: commit message clear?
   - Check remote: commit visible?
   - If mistakes: amend commit before moving to next phase

**Output:**
- ROADMAP.md updated (phase marked complete)
- Git commit created (clean, atomic)
- Changes pushed to remote
- Documentation updated (if needed)

**Exit Criteria:**
- ROADMAP.md reflects current state accurately
- Git history has one commit for this phase
- Commit message is clear and references phase

---

## Step 7: NEXT TICK

**Goal:** Clear context and continue to the next TODO task, or stop if all tasks complete.

**THIS IS THE MOST CRITICAL STEP - READ CAREFULLY:**

**Actions:**

1. **Read ROADMAP.md and count TODO tasks**
   - Scan the entire ROADMAP for tasks marked TODO
   - Ignore BLOCKED, IN PROGRESS, REVIEW, DONE
   - Count: how many TODO tasks remain?

2. **Decision point (NO EXCEPTIONS TO THIS LOGIC):**

   **IF TODO tasks remain (count > 0):**
   - YOU MUST invoke the Skill tool RIGHT NOW: `skill: "dev-loop"`
   - DO NOT write a progress report first
   - DO NOT say "I'm stopping to keep you informed"
   - DO NOT mention token usage or context limits
   - DO NOT ask if you should continue
   - DO NOT do anything except invoke the Skill tool
   - This spawns a FRESH agent with clean context for the next phase
   - The new dev-loop agent will start at Step 1 and handle the next TODO task

   **IF NO TODO tasks remain (count = 0):**
   - NOW you can report to user: "All TODO tasks in ROADMAP complete. Development loop finished."
   - List the tasks you completed in this session
   - STOP - do not invoke dev-loop again

3. **Context clearing (automatic)**
   - By invoking Skill tool, you automatically get:
     - Fresh token budget
     - No memory of previous phases (except git history)
     - Clean slate for next task
   - This prevents context bloat during long development sessions

**COMMON MISTAKE TO AVOID:**
- ❌ "I'm reporting status now (at 60% token usage) to keep you informed of progress."
- ✅ Just invoke the Skill tool. Silent handoff to the next agent. No status report.

**Output:**
- Either: Fresh dev-loop invocation (if TODO tasks remain) - NO STATUS REPORT
- Or: Completion report (if no TODO tasks remain) - NOW you report status

**Exit Criteria:**
- ROADMAP.md scanned and TODO count determined
- If TODO > 0: Skill tool invoked with skill="dev-loop" - NOTHING ELSE
- If TODO = 0: User informed of completion and agent STOPS

---

## Quality Principles

Throughout all phases, maintain these principles:

### 1. Simplicity First
- No over-engineering
- No "just in case" features
- Solve the current problem, not hypothetical future problems

### 2. Functional Where Possible
- Pure functions (no side effects)
- Immutable data structures
- Composition over inheritance

### 3. Error Handling Always
- Every operation that can fail returns Result<T>
- User-facing errors are clear and actionable
- No silent failures, ever

### 4. Test Integration Points
- Not full TDD, but test interactions between modules
- Unit tests for complex logic only
- Manual QA for UX flows

### 5. Minimal Comments
- Code should be self-documenting
- Comment only: invariants, assumptions, non-obvious consequences
- Never repeat what the code says

### 6. Incremental Progress
- Each phase is atomic (one commit)
- Commit when phase is complete, not before
- Push frequently to avoid losing work

### 7. Respect Layer Boundaries
- Domain layer: no I/O, no Neovim API, pure logic
- Infrastructure layer: file I/O, SQL, extmarks
- Application layer: orchestration, workflows
- UI layer: commands, keymaps, notifications
- Never import "up" the stack

---

## Running the Loop Autonomously

This skill is designed to run for HOURS with no user intervention, working through dozens of tasks.

**Core loop behavior:**

1. **Start:** Find the next TODO task in ROADMAP
2. **Execute:** Run Steps 1-6 (understand → design → implement → validate → refactor → commit)
3. **Check:** At Step 7, scan ROADMAP for remaining TODO tasks
4. **Continue:** If TODO tasks exist, invoke `skill: "dev-loop"` to spawn fresh agent
5. **Repeat:** New agent starts at step 1 with clean context
6. **Stop:** Only when NO TODO tasks remain

**Key principles:**

- **Context clearing is AUTOMATIC:** Every loop iteration = fresh agent via Skill tool
- **No arbitrary limits:** Don't stop at 4, 10, or 100 tasks - only stop when TODO count = 0
- **No user approval needed:** Between phases, just invoke the next loop immediately
- **If blocked:** Document blocker clearly, mark task as BLOCKED, move to next TODO
- **Trust the process:** Each agent only sees one task at a time, keeping context lean

---

## Checklist for Each Loop Iteration

Before exiting to Step 7, confirm:

- [ ] ROADMAP task marked as "REVIEW" (ready for human review)
- [ ] All acceptance criteria met
- [ ] Tests passing (automated + manual)
- [ ] Code follows quality principles
- [ ] Git commit created and pushed
- [ ] No regressions in previous phases
- [ ] Documentation updated (if needed)

**At Step 7, mandatory decision:**

- [ ] ROADMAP scanned for TODO count
- [ ] If TODO > 0: Skill tool invoked immediately with `skill: "dev-loop"`
- [ ] If TODO = 0: User informed, agent STOPS

**DO NOT:**
- Ask user permission to continue (just invoke the skill)
- Say "moving to next phase" without actually invoking the skill
- Stop after an arbitrary number of tasks
- Continue in the same context (always spawn fresh via Skill tool)
- Report progress or status while TODO > 0 (seen in the wild: "I'm reporting status now at 60% token usage")
- Stop to "keep user informed" - the user will see git commits, that's enough

---

## Notes on Long-Running Autonomous Operation

When running autonomously (bypass mode or otherwise):

- **Trust the loop.** Don't skip steps because they seem unnecessary.
- **Record decisions.** Future agents (or humans) need to understand why choices were made.
- **If stuck:** Mark task as BLOCKED, document the blocker clearly, move to next TODO task.
- **Commit frequently.** One task = one commit. No batching.
- **Validate ruthlessly.** If tests fail, stop and fix. Don't rationalize failures.
- **Context is YOUR responsibility:** Always invoke skill="dev-loop" at Step 7 to spawn fresh agent.
- **Never stop early:** Work through ALL TODO tasks, no matter how many. Could be 5, could be 500.

**The Skill tool invocation is NOT optional - it's required for:**
- Clearing context (preventing token bloat)
- Ensuring each task starts fresh (no assumptions from previous tasks)
- Enabling true long-running operation (hours, not minutes)

**How to invoke the next loop iteration:**
```
At Step 7, if TODO tasks remain, use the Skill tool:
- Tool: Skill
- Parameters: skill="dev-loop"
- That's it. The new agent spawns and starts at Step 1 automatically.
```

**What happens:**
- Current agent finishes (you're done)
- New agent spawns with fresh context
- New agent reads ROADMAP, finds next TODO, starts Step 1
- Repeat until no TODO tasks remain

This loop is designed to produce **careful, methodical, high-quality results** autonomously over extended periods. Follow it exactly.

---

## Troubleshooting: Why Did The Agent Stop Early?

If you notice the agent stopped after only a few tasks when more TODO tasks remain:

**Common mistakes:**

1. **Agent forgot to invoke Skill tool at Step 7**
   - Fix: The agent MUST use the Skill tool with skill="dev-loop" to continue
   - Not optional, not "if you want to", not "consider doing"
   - REQUIRED if TODO count > 0

2. **Agent asked for permission to continue**
   - Fix: NO permission needed. Just invoke the skill immediately.
   - This is autonomous mode - keep going until TODO = 0

3. **Agent said "moving to next phase" but didn't invoke the skill**
   - Fix: Saying it doesn't make it happen. Must actually call Skill tool.
   - Check: Did you see a new agent spawn? No? Then it didn't happen.

4. **Agent got confused about task count**
   - Fix: Scan ENTIRE ROADMAP, count only tasks with literal text "TODO"
   - Ignore all other statuses (BLOCKED, IN PROGRESS, REVIEW, DONE)

5. **Context bloat caused the agent to get lost**
   - This is WHY we use Skill tool - it spawns fresh context
   - Without it, agent context grows unbounded and gets confused

**How to verify it's working:**
- After each commit, watch for Skill tool invocation
- You should see a NEW agent spawn (new conversation context)
- Each agent should only handle ONE task, then spawn the next

