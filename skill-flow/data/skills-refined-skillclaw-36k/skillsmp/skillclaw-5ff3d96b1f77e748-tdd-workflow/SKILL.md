---
name: tdd-workflow
description: Use this skill when writing new features, fixing bugs, or refactoring code to ensure adherence to test-driven development principles with a focus on achieving 80%+ test coverage.
---

# Skill body

## Overview

This skill ensures that all code development follows TDD principles, achieving comprehensive test coverage.

## Trigger Conditions

- Writing new features or functionalities
- Fixing bugs (write a test that reproduces the bug first)
- Refactoring existing code
- Adding API endpoints
- Creating new components
- Implementing core business logic

## Role Integration

| Role    | TDD Usage Scenario                  |
| ------- | ----------------------------------- |
| `/lead` | Define testing strategy, review coverage |
| `/dev`  | Execute TDD cycle, write tests and implementations |
| `/qa`   | Supplement boundary tests, perform E2E testing |

**Typical Workflow**:

```
/lead → Define interfaces and testing strategy
  ↓
/dev → TDD Cycle (RED → GREEN → REFACTOR)
  ↓
/qa → Validate coverage, supplement boundary tests
  ↓
/commit → Commit code and tests
```

## Core Principles

### 1. Test First

**Always** write tests before writing the implementation code to make the tests pass.

### 2. TDD Cycle

```
RED → GREEN → REFACTOR → REPEAT

RED:      Write a failing test
GREEN:    Write the minimum code to make the test pass
REFACTOR: Improve the code while keeping the tests passing
REPEAT:   Move to the next scenario
```

### 3. Coverage Requirements

| Code Type     | Coverage Requirement |
| --------------| -------------------- |
| General Business Code | 80%+       |
| Financial Calculations | 100%       |
| Authentication Logic | 100%       |
| Security-Critical Code | 100%       |
| Core Business Logic | 100%       |

## Complete TDD Example

### Scenario: Implementing a User Points Calculator

#### Step 1: User Story

```markdown
As a user, I want to calculate points based on my activities,
so that I can understand my membership level and redeemable rewards.

Acceptance Criteria:

- 1 point for every 10 currency units spent
- Extra points for consecutive check-in days
- VIP users earn double points
- Points capped at 10,000 per month
```

#### Step 2: Define Interface (SCAFFOLD)

```typescript
// src/services/points.ts

export interface UserActivity {
  purchaseAmount: number; // Amount spent (currency units)
  consecutiveCheckIns: number; // Number of consecutive check-in days
  isVip: boolean; // Is the user a VIP
  currentMonthPoints: number; // Points already earned this month
}

export interface PointsResult {
  earnedPoints: number; // Points earned in this transaction
  totalPoints: number; // Total points accumulated
  capped: boolean; // Has the cap been reached?
  cappedAmount: number; // Amount of points capped
}

export function calculatePoints(activity: UserActivity): PointsResult {
  // TODO: Implementation
  throw new Error("Not implemented");
}
```

#### Step 3: Write Failing Test (RED)

```typescript
// src/services/points.test.ts

import { calculatePoints, type UserActivity } from "./points";

describe("calculatePoints", () => {
  // Basic scenarios
  describe("Basic Points Calculation", () => {
    it("Earns 1 point for every 10 currency units spent", () => {
      const activity: UserActivity = {
        purchaseAmount: 100,
        consecutiveCheckIns: 0,
        isVip: false,
        currentMonthPoints: 0,
      };

      const result = calculatePoints(activity);

      expect(result.earnedPoints).toBe(10);
      expect(result.totalPoints).toBe(10);
      expect(result.capped).toBe(false);
    });
```