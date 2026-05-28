# Project States

## State Definitions

### CAPTURED
**Definition:** Raw idea logged, no validation work started.

**Contains:**
- Project name and slug
- One-liner description
- Date captured
- Initial notes/context

**Entry:** Idea captured via `/tracker new`
**Exit:** Problem/audience/hypothesis articulated → VALIDATING

**Decay Window:** 14 days
**Rationale:** Ideas are cheap. Validate quickly or drop.

---

### VALIDATING
**Definition:** Active problem/solution testing in progress.

**Contains:**
- Research notes
- Partial findings
- Competitor observations
- Community signals

**Entry:** From CAPTURED after hypothesis stated
**Exit:** Complete validation report with verdict → VALIDATED

**Decay Window:** 30 days
**Rationale:** Research shouldn't drag on indefinitely.

---

### VALIDATED
**Definition:** Worth building, scope defined. Verdict rendered.

**Contains:**
- Full validation report
- Verdict (BUILD/PIVOT/KILL)
- Confidence level
- Scope fence

**Entry:** From VALIDATING after scout completes
**Exit (BUILD):** Commit to proceed → ARCHITECTING
**Exit (KILL):** → ARCHIVED

**Decay Window:** 21 days
**Rationale:** Decide: build, pivot, or kill.

---

### ARCHITECTING
**Definition:** Technical design in progress.

**Contains:**
- Architecture drafts
- Stack decisions
- Data model sketches
- Build roadmap draft

**Entry:** From VALIDATED after BUILD verdict accepted
**Exit:** Architecture doc + roadmap approved → BUILDING

**Decay Window:** 14 days
**Rationale:** Design paralysis is real. Ship the architecture.

---

### BUILDING
**Definition:** Active development. MVP in progress.

**Contains:**
- Build log
- Progress notes
- Blockers
- Stage progress (1-11)

**Entry:** From ARCHITECTING after architecture approved
**Exit:** MVP functional + launch checklist ready → LAUNCHING

**Decay Window:** 90 days
**Rationale:** Longer runway, but not infinite. Ship something.

---

### LAUNCHING
**Definition:** Preparing for and executing go-to-market.

**Contains:**
- Launch plan
- Assets created
- Timeline
- Channel strategy

**Entry:** From BUILDING after MVP complete
**Exit:** Live with real users + baseline metrics → GROWING

**Decay Window:** 21 days
**Rationale:** Launch momentum matters. Ship it.

---

### GROWING
**Definition:** Live, acquiring users. Scaling and optimizing.

**Contains:**
- Growth model
- Experiment log
- Metrics dashboard
- Channel performance

**Entry:** From LAUNCHING after first real users
**Exit:** Stable metrics + systems documented → OPERATING

**Decay Window:** 180 days
**Rationale:** Growth takes time, but needs activity.

---

### OPERATING
**Definition:** Steady state. Maintenance mode.

**Contains:**
- Ops playbook
- SOPs
- Team info
- Health metrics

**Entry:** From GROWING after systems stable
**Exit:** Exit decision made → EXITING

**Decay Window:** None (no decay)
**Rationale:** Maintenance can be sparse. No forced decay.

---

### EXITING
**Definition:** Active exit process in progress.

**Contains:**
- Exit memo
- Data room
- Deal notes
- Buyer conversations

**Entry:** From OPERATING after exit decision
**Exit:** Deal closed → EXITED

**Decay Window:** 60 days
**Rationale:** Deals have momentum or they die.

---

### EXITED
**Definition:** Exit complete. Transition finished.

**Contains:**
- Final outcome
- Deal terms
- Transition notes
- Learnings

**Entry:** From EXITING after deal closed
**Exit:** After 30 days → ARCHIVED

**Decay Window:** None
**Rationale:** Terminal state, auto-archives.

---

## Special States

### ICE ❄️
**Definition:** Intentionally frozen. Not dead, but not active.

**Entry Triggers:**
- Manual `/tracker ice` command
- Decay hits 100% without action (auto-freeze)

**Contains:**
- Freeze date
- Freeze reason
- Previous state (preserved)
- Expected thaw conditions

**Exit:** Manual `/tracker thaw` → Returns to previous state

**Decay:** Frozen (no decay while on ice)

**Time Limits:**
| Duration | Action |
|----------|--------|
| 0-3 months | Standard ice |
| 3-6 months | Monthly prompt: "Still want this on ice?" |
| 6+ months | Force decision: REVIVE or ARCHIVE |

---

### KILLED ⚰️
**Definition:** Failed or abandoned. Lessons logged.

**Entry Triggers:**
- Scout verdict = KILL
- Manual `/tracker kill` command
- Abandoned from ICE (6+ months)

**Contains:**
- Kill reason
- Lessons learned
- Post-mortem summary
- Final state before kill

**Exit:** None (terminal)

---

### ARCHIVED ✅
**Definition:** Successfully completed or permanently closed.

**Entry Triggers:**
- From EXITED after 30 days
- Manually archived from any state
- Killed projects move here

**Contains:**
- Full history
- Outcome summary
- Learnings
- Final artifacts

**Exit:** None (terminal)

---

## Valid Transitions

```
CAPTURED → VALIDATING, ICE, KILLED
VALIDATING → VALIDATED, ICE, KILLED
VALIDATED → ARCHITECTING (if BUILD), KILLED (if KILL verdict), ICE
ARCHITECTING → BUILDING, ICE, KILLED
BUILDING → LAUNCHING, ICE, KILLED
LAUNCHING → GROWING, ICE, KILLED
GROWING → OPERATING, EXITING, ICE
OPERATING → EXITING, ICE
EXITING → EXITED
EXITED → ARCHIVED
ICE → (previous state via thaw)
```

### Invalid Transitions (Blocked)
- Cannot skip states (e.g., CAPTURED → BUILDING)
- Cannot reverse flow (e.g., BUILDING → VALIDATING)
- Cannot un-kill or un-archive

---

## Transition Verification

When `/tracker update <project> <new-state>` is called:

1. **Check current state** - Load from project card
2. **Verify transition is valid** - Check against valid transitions map
3. **Check gate requirements** - Load from stage-gates.md
4. **Execute or block** - Proceed if valid, explain if blocked
