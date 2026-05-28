---
name: work-creation-cycle
description: HAIOS Work Creation Cycle for structured work item population. Use when
  creating new work items. Guides VERIFY->POPULATE->READY workflow.
recipes:
- work
generated: 2025-12-25
last_updated: '2026-01-17T11:59:42'
---
# Work Creation Cycle

This skill defines the VERIFY-POPULATE-READY cycle for populating work items after scaffolding. It ensures work items have complete Context and Deliverables before being actioned.

## When to Use

**Invoked automatically** by `/new-work` command after scaffolding.
**Manual invocation:** `Skill(skill="work-creation-cycle")` when populating an existing work file.

---

## The Cycle

```
VERIFY --> POPULATE --> READY --> CHAIN
                                    |
                          [confidence check]
                           /              \
                     HIGH                  LOW
                      |                     |
              auto-chain to           /reason +
           /new-plan or              user decision
           /new-investigation
```

### 1. VERIFY Phase

**On Entry:**
```bash
just set-cycle work-creation-cycle VERIFY {work_id}
```

**Goal:** Confirm work file was created and is valid.

**Actions:**
1. Read the work file: `docs/work/active/{id}/WORK.md` (E2-212 directory structure)
2. Verify file has valid YAML frontmatter
3. Confirm `status: active` and `current_node: backlog`
4. Check for `spawned_by` field if this is spawned work

**Exit Criteria:**
- [ ] Work file exists at expected path
- [ ] Frontmatter valid (template: work_item)
- [ ] Status is `active`

**Tools:** Read, Glob

---

### 2. POPULATE Phase

**On Entry:**
```bash
just set-cycle work-creation-cycle POPULATE {work_id}
```

**Goal:** Fill in essential work item fields.

**Guardrails (MUST follow):**
1. **Context section MUST be populated** - Replace `[Problem and root cause]` with actual problem description
2. **Deliverables MUST be actionable** - Replace placeholders with specific checkboxes
3. **MUST validate against source investigation** (Session 192 - see below)

**Actions:**
1. Prompt for Context: "What problem does this work item solve?"
2. Fill in Context section with problem statement
3. Prompt for Deliverables: "What are the specific outputs?"
4. Fill in Deliverables as checklist items
5. Optionally set: milestone, priority, spawned_by, blocked_by
6. **MUST:** Run Investigation Design Validation (see below)

**MUST Gate: Investigation Design Validation (Session 192 - E2-290 Learning)**

IF `spawned_by` or `spawned_by_investigation` is populated:
1. **MUST** read the source investigation: `docs/work/active/{inv_id}/investigations/*.md`
2. **MUST** find the `## Design Outputs` section
3. **MUST** verify coverage:
   - For each schema/structure in Design Outputs → deliverable exists
   - For each "Integration Mechanism" description → deliverable exists
   - For each "Key Design Decision" that implies implementation → deliverable exists
4. **If gap found:** Add missing deliverables before proceeding

**Example (E2-290 gap that prompted this gate):**
```
Investigation INV-064 had:
  Design Outputs:
    - Queue Schema (work_queues.yaml) ✓ → deliverable existed
    - Queue Integration Mechanism ✗ → NO deliverable for wiring into survey-cycle

Result: Infrastructure built, but no governance integration.
```

> **Anti-pattern prevented:** "Design without Deliverable" - Investigation designs integration but work item only lists infrastructure. Implementation completes infrastructure, never wires it in.

**Exit Criteria:**
- [ ] Context section has real content (not placeholder)
- [ ] Deliverables have specific items (not placeholders)
- [ ] **MUST:** If spawned by investigation, deliverables cover all Design Outputs
- [ ] Optional: milestone assigned

**Tools:** Edit, AskUserQuestion, Read

---

### 3. READY Phase

**On Entry:**
```bash
just set-cycle work-creation-cycle READY {work_id}
```

**Goal:** Validate work item is actionable.

**Guardrails (MUST follow - E2-191):**
1. **Context MUST NOT contain placeholders** - Detect `[Problem and root cause]`
2. **Deliverables MUST NOT contain placeholders** - Detect `[Deliverable 1]`, `[Deliverable 2]`

**Actions:**
1. Read work file to verify all fields populated
2. Check Context section contains >20 characters AND no placeholder text
3. Check Deliverables has at least one checkbox item AND no placeholder text
4. **If placeholders found:** Report to user, recommend completing POPULATE phase
5. Update History section with population timestamp

**Exit Criteria:**
- [ ] Context populated with meaningful content (no placeholders)
- [ ] Deliverables has actionable checklist (no placeholders)
- [ ] Work item ready for further lifecycle progression

**Tools:** Read, Edit

---

### 4. CHAIN Phase (Post-READY)

**On Entry:**
```bash
just set-cycle work-creation-cycle CHAIN {work_id}
```

**Goal:** Route to appropriate next cycle based on confidence.

**Confidence-Based Routing:**

| Signal | Confidence | Action |
|--------|------------|--------|
| ID starts with `INV-` | HIGH | Auto-chain: `/new-investigation {id} {title}` |
| `spawned_by_investigation` is populated | HIGH | Auto-chain: `/new-plan {id} {title}` (discovery done) |
| Clear technical deliverables, small scope | HIGH | Auto-chain: `/new-plan {id} {title}` |
| Complex/architectural work | LOW | Chain to `/reason` for structured decision |
| Unclear if needs investigation first | LOW | Chain to `/reason` for structured decision |
| No clear signals | LOW | Chain to `/reason` for structured decision |

**Actions:**
1. Read work file frontmatter for signals (id prefix, spawned_by_investigation)
2. Assess deliverables complexity
3. **If HIGH confidence:** Auto-invoke appropriate command
4. **If LOW confidence:** Invoke `/reason` and ask user

**Exit Criteria:**
- [ ] Next lifecycle step initiated (plan, investigation, or user decision)

**Tools:** Read, Skill

---

## Composition Map

| Phase | Primary Tool | Memory Integration |
|-------|--------------|-------------------|
| VERIFY | Read, Glob | - |
| POPULATE | Edit, AskUserQuestion | Query for prior similar work |
| READY | Read, Edit | - |
| CHAIN | Read, Skill | - |

---

## Quick Reference

| Phase | Question to Ask | If NO |
|-------|-----------------|-------|
| VERIFY | Does work file exist? | Re-run /new-work |
| POPULATE | Is Context filled? | Prompt user for problem statement |
| POPULATE | Are Deliverables defined? | Prompt user for outputs |
| POPULATE | **If spawned by INV: Do deliverables cover all Design Outputs?** | **Add missing deliverables** |
| READY | Is work item actionable? | Return to POPULATE |

---

## Related

- **Investigation-cycle skill:** Parallel workflow for research
- **Implementation-cycle skill:** Parallel workflow for implementation
- **Work item template:** `.claude/templates/work_item.md`
- **ADR-039:** Work Item as File Architecture
- **/new-work command:** Creates work item files
