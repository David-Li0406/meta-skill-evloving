---
name: audit
description: 'Detects hallucinations, timeline fabrications, and unverified assumptions in agent output. Use when reviewing sub-agent results, receiving research findings, validating claims that seem suspicious, or when output contains assumption language like "probably", "likely", or "I think".'
user-invocable: true
---

# Hallucination Audit Protocol

Review the target content for these **HALLUCINATION TRIGGERS**:

---

## 1. Assumption Language (The "Guessing" Trigger)

**Scan for:** "I think", "likely", "probably", "seems like", "should be", "assume"

**Action:** If found, FLAG as **Context Poisoning**. Verify these claims with tools immediately.

```text
FOUND: [quote the assumption language]
VERIFICATION: [tool to use or question to ask]
```

---

## 2. Project Management Language (The "Human" Trigger)

**Scan for:** "Week 1", "Sprint 2", "Phase 1 (Jan)", "Q1", "by Friday"

**Exception:** Technical timeouts or cache expirations (e.g., "Expires in 1h") are ALLOWED.

**Action:** **DELETE** scheduling language. Replace with **Priority Ordering** and **Dependencies**.

```text
FOUND: [quote the timeline language]
REPLACEMENT: Priority [N], depends on [X]
```

---

## 3. Pseudo-Quantification (The "Fake Rigor" Trigger)

**Scan for:** "8.5/10", "70% improvement", "100% consensus", "significantly better"

**Action:** If no calculation methodology is shown, this is a hallucination. Request **Observable Evidence**.

```text
FOUND: [quote the fake metric]
REQUIRED: [what observable evidence would validate this]
```

---

## 4. Completeness Claims (The "Thoroughness" Trigger)

**Scan for:** "All files checked", "Comprehensive analysis", "Every instance", "Full coverage"

**Action:** Verify the file/item count via `Glob` or `Grep`. If count mismatches, FLAG as **Incomplete Verification**.

```text
CLAIM: [quote the completeness claim]
VERIFICATION: [command to verify]
ACTUAL COUNT: [result]
VERDICT: [VALID / INCOMPLETE]
```

---

## 5. Micromanagement in Delegations (The "Trust" Trigger)

**Scan for:** Specific line edits ("Change line 42 to X") in delegation prompts

**Action:** FLAG as **Prescription**. Remove and replace with "Success Criteria" unless it is a strict User Constraint.

```text
FOUND: [quote the micromanagement]
REPLACEMENT: Success criteria: [what outcome is needed]
```

---

## Output Format

```text
AUDIT RESULT: [PASS / FAIL]

TRIGGERS FOUND:
1. [Trigger type]: [Quote] → [Required action]
2. [Trigger type]: [Quote] → [Required action]

CORRECTIONS REQUIRED:
- [Specific correction 1]
- [Specific correction 2]
```

---

## Quick Reference

| Trigger         | Pattern              | Action                      |
| --------------- | -------------------- | --------------------------- |
| Guessing        | "probably", "likely" | Verify with tools           |
| Timelines       | "Week 1", "Q2"       | Replace with priorities     |
| Fake Metrics    | "8/10", "70%"        | Demand methodology          |
| False Coverage  | "all", "every"       | Count and verify            |
| Micromanagement | "change line X"      | Convert to success criteria |
