# GDD Templates Reference

## Full System Design Document Template

```markdown
# [SYSTEM NAME] - System Design Document

**Document ID:** SYS-[ABBREV]-[NUM]
**Version:** 1.0
**Status:** Draft | Review | Approved
**Last Updated:** [DATE]
**Author:** [NAME]

---

## 1. Executive Summary

[2-3 sentence overview of what this system does and why it matters]

### 1.1 Design Pillars

1. **[Pillar Name]**: [One sentence explanation]
2. **[Pillar Name]**: [One sentence explanation]
3. **[Pillar Name]**: [One sentence explanation]

### 1.2 Player Fantasy

> "[First-person statement of what the player feels while engaging with this system]"

### 1.3 System Dependencies

| Dependency | Type | Description |
|------------|------|-------------|
| [System]   | Required | [Why needed] |
| [System]   | Optional | [Enhancement] |

---

## 2. Core Loop

### 2.1 Loop Diagram

[Mermaid diagram here]

### 2.2 Session Structure

| Phase | Duration | Player Actions | System Actions |
|-------|----------|----------------|----------------|
| Setup | Xs | [actions] | [actions] |
| Core | Xs | [actions] | [actions] |
| Resolution | Xs | [actions] | [actions] |

### 2.3 Win/Loss Conditions

**Win States:**
- [Condition]: [Outcome]

**Loss States:**
- [Condition]: [Outcome]

**Draw/Push States:**
- [Condition]: [Outcome]

---

## 3. Mechanics Specification

### 3.1 Input Mechanics

| Input | Trigger | Constraints | Feedback |
|-------|---------|-------------|----------|
| [Action] | [How activated] | [Limits] | [Response] |

### 3.2 Processing Mechanics

[Describe calculations, RNG, decision trees]

### 3.3 Output Mechanics

| Output | Condition | Value Range | Delivery |
|--------|-----------|-------------|----------|
| [Reward] | [When given] | [Min-Max] | [How shown] |

### 3.4 Edge Cases

| Scenario | Expected Behavior | Fallback |
|----------|-------------------|----------|
| [Edge case] | [What happens] | [If fails] |

---

## 4. Economy Integration

### 4.1 Currency Flow

**Inputs (Sinks):**
- [Currency]: [Amount] per [Action]

**Outputs (Faucets):**
- [Currency]: [Amount] per [Outcome]

### 4.2 Balance Targets

| Metric | Target | Acceptable Range |
|--------|--------|------------------|
| RTP | XX% | XX-XX% |
| Session EV | [value] | [range] |

### 4.3 Cross-System Influence

[Reference INFLUENCE-[ID] mappings]

---

## 5. Progression

### 5.1 Unlock Requirements

| Tier | Requirement | Unlocks |
|------|-------------|---------|
| 1 | [Condition] | [Features] |

### 5.2 Difficulty Scaling

[Describe how challenge increases]

### 5.3 Mastery Indicators

- [Metric]: [What it shows]

---

## 6. UI/UX Requirements

### 6.1 Screen Inventory

| Screen ID | Name | Purpose | Entry Points |
|-----------|------|---------|--------------|
| UI-[ID] | [Name] | [Purpose] | [How accessed] |

### 6.2 Key Interactions

[Describe critical touch/click targets]

### 6.3 Animation Requirements

| Animation | Trigger | Duration | Priority |
|-----------|---------|----------|----------|
| [Name] | [When] | Xms | [1-5] |

### 6.4 Audio Cues

| Sound | Trigger | Notes |
|-------|---------|-------|
| [Name] | [When] | [Style notes] |

---

## 7. Technical Notes

### 7.1 Data Structures

[Key objects/schemas]

### 7.2 State Management

[State machine or flow description]

### 7.3 API Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| /api/[path] | [GET/POST] | [What it does] |

### 7.4 Performance Targets

- Load time: <Xs
- Frame rate: X fps minimum
- Memory budget: X MB

---

## 8. Metrics & Analytics

### 8.1 KPIs

| Metric | Definition | Target | Alert Threshold |
|--------|------------|--------|-----------------|
| [Name] | [How calculated] | [Goal] | [Warning level] |

### 8.2 A/B Test Opportunities

- [Variable]: [Hypothesis]

### 8.3 Balancing Levers

| Lever | Range | Impact | Risk |
|-------|-------|--------|------|
| [Parameter] | [Min-Max] | [What changes] | [Danger] |

---

## 9. Appendices

### 9.A Probability Tables

[Full odds breakdowns]

### 9.B Payout Matrices

[Complete payout structures]

### 9.C Glossary

| Term | Definition |
|------|------------|
| [Term] | [Meaning in this context] |

### 9.D Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Name] | Initial document |
```

## Minigame Quick Spec Template

For rapid documentation of carnival-style minigames:

```markdown
# [MINIGAME NAME] - Quick Spec

**ID:** MINI-[NUM] | **Version:** X.X | **Status:** [Status]

## Core Concept
[One paragraph description]

## Inspiration
Based on: [Real-world game]
Key departures: [How this differs]

## Session Flow
1. [Step]
2. [Step]
3. [Step]

## Betting Structure
- Min bet: [amount]
- Max bet: [amount]
- Bet types: [list]

## Odds & Payouts
| Outcome | Odds | Payout |
|---------|------|--------|
| [X] | X% | X:1 |

**House Edge:** X% | **RTP:** X% | **Variance:** Low/Med/High

## Farm Influence
- Win → [Farm effect]
- Loss → [Farm effect]
- Streak bonus → [Farm effect]

## MVP Scope
Must have:
- [ ] [Feature]

Nice to have:
- [ ] [Feature]

Out of scope:
- [ ] [Feature]

## Open Questions
- [ ] [Question]
```

## Card-to-Farm Influence Map Template

```markdown
# Influence Map: [Source System] → [Target System]

**Map ID:** INFLUENCE-[NUM]
**Version:** X.X

## Influence Channels

| Trigger | Condition | Effect | Magnitude | Duration |
|---------|-----------|--------|-----------|----------|
| [Event] | [When] | [What happens] | [How much] | [How long] |

## Stacking Rules

- Same-type effects: [Stack/Replace/Max]
- Cross-type effects: [Additive/Multiplicative]
- Cap: [Maximum effect]

## Examples

**Scenario:** [Description]
**Trigger:** [What happened]
**Result:** [Calculated effect]
```
