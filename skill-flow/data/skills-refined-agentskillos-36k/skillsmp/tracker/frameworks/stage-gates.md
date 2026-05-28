# Stage Gates

## Gate Philosophy

Gates exist to ensure quality, not create bureaucracy.

Each gate has:
- **MUST-HAVE** requirements (block transition if unmet)
- **SHOULD-HAVE** enhancements (noted but don't block)

The goal: Prevent premature advancement while keeping momentum.

---

## Gate Definitions

### CAPTURED → VALIDATING

**Purpose:** Ensure the idea is articulated enough to research.

**MUST-HAVE:**
- [ ] Problem statement articulated (who has this problem?)
- [ ] Target audience defined (who specifically?)
- [ ] Solution hypothesis stated (what might solve it?)
- [ ] Success criteria sketched (what would "working" look like?)

**SHOULD-HAVE:**
- [ ] Personal motivation noted (why you?)
- [ ] Initial assumptions listed (what are we betting on?)

---

### VALIDATING → VALIDATED

**Purpose:** Ensure validation is thorough before committing to build.

**MUST-HAVE:**
- [ ] Validation report complete (using id8scout template)
- [ ] Market analysis section complete with sources
- [ ] Competitive landscape mapped
- [ ] Community signals gathered (real quotes/posts)
- [ ] Verdict rendered: BUILD / PIVOT / KILL
- [ ] Confidence level assigned: High / Medium / Low

**SHOULD-HAVE:**
- [ ] Founder fit assessment complete
- [ ] Execution plan sketched
- [ ] Budget/timeline estimates (calibrated for AI-augmented solo builder)

---

### VALIDATED → ARCHITECTING

**Purpose:** Confirm BUILD commitment before investing in design.

**MUST-HAVE:**
- [ ] Verdict is BUILD (not PIVOT or KILL)
- [ ] Founder explicitly commits to proceed
- [ ] Target MVP scope articulated

**SHOULD-HAVE:**
- [ ] Key risks identified
- [ ] Initial stack preferences noted

---

### ARCHITECTING → BUILDING

**Purpose:** Ensure design is solid before coding begins.

**MUST-HAVE:**
- [ ] Architecture document complete (using id8architect template)
- [ ] System components defined
- [ ] Data model designed
- [ ] Stack selected with rationale
- [ ] MVP scope locked (what's in, what's out)
- [ ] Build roadmap with phases

**SHOULD-HAVE:**
- [ ] API contracts sketched
- [ ] Infrastructure approach defined
- [ ] Cost estimates for MVP phase

---

### BUILDING → LAUNCHING

**Purpose:** Ensure product is ready for real users.

**MUST-HAVE:**
- [ ] MVP is functional (core use case works)
- [ ] MVP is testable (someone else can use it)
- [ ] Launch checklist started (using id8launch template)
- [ ] Landing page or entry point exists
- [ ] Basic analytics instrumented

**SHOULD-HAVE:**
- [ ] Known bugs documented
- [ ] Launch date targeted
- [ ] Initial users identified (who will you launch to?)

---

### LAUNCHING → GROWING

**Purpose:** Confirm product is live with real traction.

**MUST-HAVE:**
- [ ] Product is live (accessible to public or target users)
- [ ] Real users exist (not just you)
- [ ] Baseline metrics captured (what are current numbers?)
- [ ] Feedback channel exists (how do users tell you things?)

**SHOULD-HAVE:**
- [ ] Launch retrospective done (what worked, what didn't)
- [ ] First growth experiment identified
- [ ] Retention baseline measured

---

### GROWING → OPERATING

**Purpose:** Confirm sustainable operation before steady state.

**MUST-HAVE:**
- [ ] Growth model documented (how does this grow?)
- [ ] Key metrics stable or improving
- [ ] Core systems documented (SOPs exist for critical ops)
- [ ] Not dependent on heroics (you can take a week off)

**SHOULD-HAVE:**
- [ ] Growth playbook complete (using id8growth template)
- [ ] Ops playbook complete (using id8ops template)
- [ ] Team/delegation plan if needed

---

### OPERATING → EXITING

**Purpose:** Ensure exit decision is deliberate and prepared.

**MUST-HAVE:**
- [ ] Exit decision made (why exit now?)
- [ ] Exit type identified (acquisition, acqui-hire, sale, shutdown)
- [ ] Exit memo drafted (using id8exit template)
- [ ] Data room 80%+ complete

**SHOULD-HAVE:**
- [ ] Potential buyers/acquirers identified
- [ ] Valuation range estimated
- [ ] Timeline targeted

---

### Any State → ICE

**Purpose:** Ensure freezing is intentional with context.

**MUST-HAVE:**
- [ ] Reason for freezing logged
- [ ] Expected conditions for thaw noted (optional but encouraged)

**SHOULD-HAVE:**
- [ ] Target thaw date (if known)
- [ ] Handoff notes if someone else might revive

---

### Any State → KILLED

**Purpose:** Capture learnings before closing.

**MUST-HAVE:**
- [ ] Kill reason documented
- [ ] Lessons learned logged (at least 3 bullets)

**SHOULD-HAVE:**
- [ ] Post-mortem summary
- [ ] What you'd do differently
- [ ] Reusable assets identified

---

## Gate Verification Process

When `/tracker update <project> <new-state>` is called:

### Step 1: Load Requirements
```
requirements = GATE_REQUIREMENTS[current_state → new_state]
```

### Step 2: Check Each Requirement
```
For each MUST-HAVE:
  - Check if in project.gates_passed
  - If not, add to unmet list
```

### Step 3: Decision
```
If unmet.length > 0:
  - Block transition
  - Show: "Gate blocked. Unmet requirements:"
  - List each unmet requirement
  - Suggest: "Use /tracker gate-pass to mark requirements met"
Else:
  - Allow transition
  - Reset decay timer
  - Log transition in history
```

### Step 4: Note SHOULD-HAVEs
```
For each SHOULD-HAVE not in gates_passed:
  - Note: "Consider also completing: {requirement}"
```

---

## Marking Requirements Complete

### `/tracker gate-pass <project-slug> <requirement>`

1. Load project card
2. Add requirement text to `gates_passed` array
3. Save project card
4. Show updated gate status

### Example
```
/tracker gate-pass my-project "Problem statement articulated"
→ Added to gates_passed
→ Gate status: 3/4 MUST-HAVEs complete
```

---

## Gate Override

In exceptional cases, gates can be overridden:

```
/tracker update <project> <state> --force
```

**Requires:**
- Explicit reason for override
- Logged in project history as "Gate override: {reason}"

**Use sparingly.** Gates exist for a reason.
