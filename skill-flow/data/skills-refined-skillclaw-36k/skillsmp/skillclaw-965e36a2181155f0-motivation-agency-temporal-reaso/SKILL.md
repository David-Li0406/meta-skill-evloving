---
name: motivation-agency-temporal-reasoning
description: Use this skill when you need to determine the direction of motivation (approach or avoidance) based on agency (self or environment) and temporal constraints.
---

# Skill body

## When to Use

### ✓ Trigger Conditions
- You need to decide whether to approach or avoid a target based on your motivation direction.
- The agency (self or environment) is already determined.
- There are time constraints affecting your decision-making.

### ✗ Not Trigger
- The motivation direction is already clear.
- The agency is not defined.
- There are no time constraints affecting the decision.

## Core Function

**Role:** Derive the motivation direction (approach or avoidance) based on the agency (self or environment) and the temporal context (short-term or long-term).

## Processing Logic

```
┌─ Agency (Self/Environment) is determined
│
├─ Agency = Self (S)?
│  ├─ Motivation = Approach (+)? → K9-S+ (Skill Acquisition)
│  └─ Motivation = Avoid (-)? → K9-S- (Bad Habit Removal)
│
└─ Agency = Environment (E)?
   ├─ Motivation = Approach (+)? → K9-E+ (Relationship Building)
   └─ Motivation = Avoid (-)? → K9-E- (Harmful Relationship Removal)
```

## Matrix

|  | Approach (+) | Avoid (-) |
|-----|--------------|-----------|
| **Self (S)** | K9-S+: Skill Acquisition | K9-S-: Bad Habit Removal |
| **Environment (E)** | K9-E+: Relationship Building | K9-E-: Harmful Relationship Removal |

## Application Rules (if-then-else)

```
IF Agency = S AND Motivation = +
  THEN K9-S+ (Skill Acquisition)
ELSE IF Agency = S AND Motivation = -
  THEN K9-S- (Bad Habit Removal)
ELSE IF Agency = E AND Motivation = +
  THEN K9-E+ (Relationship Building)
ELSE IF Agency = E AND Motivation = -
  THEN K9-E- (Harmful Relationship Removal)
```

## Edge Cases / Failure Modes

### ⚠️ Failure 1: Overemphasis on Avoidance
**Symptoms:** Constantly choosing K9-S- and K9-E- leads to stagnation in growth.  
**Countermeasure:** Regularly choose K9-S+ and K9-E+ to encourage positive development.

### ⚠️ Failure 2: Misidentifying Opportunities as Threats
**Symptoms:** Missing out on opportunities due to excessive avoidance.  
**Countermeasure:** Reassess the situation to ensure a balanced approach.

### ⚠️ Failure 3: Confusion Between Approach and Avoidance
**Symptoms:** Expressing a desire to avoid while approaching.  
**Countermeasure:** Clarify intentions and align actions with true motivations.

## Test Cases

### Test 1: Learning a New Skill
**Input:** Agency=S, Motivation="I want to learn Rust."  
**Expected:** K9-S+ (Skill Acquisition)  
**Actual:** ✓ Learning plan created.

### Test 2: Removing Legacy Systems
**Input:** Agency=E, Motivation="I need to migrate from old systems."  
**Expected:** K9-E- (Harmful Relationship Removal)  
**Actual:** ✓ Migration plan created.

### Test 3: Breaking Bad Habits
**Input:** Agency=S, Motivation="I want to stop staying up late."  
**Expected:** K9-S- (Bad Habit Removal)  
**Actual:** ✓ Improved sleep habits.