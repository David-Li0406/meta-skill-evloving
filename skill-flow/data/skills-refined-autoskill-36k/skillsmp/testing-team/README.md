# Testing Team

Complete QA, playtesting, and code quality team for game development.

## Expertise

This skill provides a full QA team covering:

- **Playtesting**: Fun evaluation, difficulty tuning
- **UX Research**: Player behavior, friction points
- **Unit Testing**: Component and function tests
- **Integration Testing**: API and system tests
- **E2E Testing**: Full user flow validation
- **Code Review**: Quality, patterns, best practices
- **Performance Testing**: FPS, load times, memory
- **Accessibility Testing**: A11y compliance
- **Bug Tracking**: Issue management, reproduction

## When to Use

Invoke this skill when you need to:

- Plan testing strategy for a feature
- Write unit or integration tests
- Set up E2E testing with Playwright
- Conduct code review
- Evaluate if something is fun to play
- Find and document bugs
- Improve code quality

## Testing Pyramid

```
        /\
       /  \      E2E Tests
      /----\     (Few, Slow, Expensive)
     /      \
    /--------\   Integration Tests
   /          \  (Some, Medium)
  /------------\
 /              \ Unit Tests
/________________\ (Many, Fast, Cheap)
```

## Test Patterns

### Unit Test (Vitest)

```typescript
import { describe, it, expect } from "vitest";
import { calculateHarvest } from "./harvest";

describe("calculateHarvest", () => {
  it("returns base yield for healthy crops", () => {
    const result = calculateHarvest({
      cropType: "wheat",
      health: 100,
      weatherBonus: 1.0,
    });
    expect(result.yield).toBe(10);
  });

  it("applies weather multiplier", () => {
    const result = calculateHarvest({
      cropType: "wheat",
      health: 100,
      weatherBonus: 1.5,
    });
    expect(result.yield).toBe(15);
  });
});
```

### E2E Test (Playwright)

```typescript
import { test, expect } from "@playwright/test";

test.describe("Farming Flow", () => {
  test("player can plant and harvest crop", async ({ page }) => {
    await page.goto("/game");

    // Plant seed
    await page.click('[data-testid="plot-0-0"]');
    await page.click('[data-testid="seed-wheat"]');

    // Wait for growth (or mock time)
    await page.click('[data-testid="skip-day"]');

    // Harvest
    await page.click('[data-testid="plot-0-0"]');

    // Verify inventory updated
    await expect(page.locator('[data-testid="wheat-count"]'))
      .toHaveText("10");
  });
});
```

### Component Test

```typescript
import { render, screen } from "@testing-library/react";
import { ResourceBar } from "./ResourceBar";

test("displays correct percentage", () => {
  render(<ResourceBar current={75} max={100} color="health" />);

  const bar = screen.getByRole("progressbar");
  expect(bar).toHaveStyle({ width: "75%" });
});
```

## Playtesting Framework

### Session Structure

1. **Pre-Session** (5 min)
   - Explain what you're testing
   - No tutorial for the feature

2. **Play Session** (15-30 min)
   - Observe silently
   - Note confusion points
   - Time to completion

3. **Debrief** (10 min)
   - What was fun?
   - What was frustrating?
   - What was confusing?

### Metrics to Track

| Metric | What It Reveals |
|--------|-----------------|
| Time to first action | Onboarding clarity |
| Error rate | UI/UX issues |
| Retry rate | Difficulty balance |
| Session length | Engagement |
| Quit points | Frustration sources |

## Code Review Checklist

- [ ] Does it work as intended?
- [ ] Are there edge cases?
- [ ] Is error handling appropriate?
- [ ] Is the code readable?
- [ ] Are there performance concerns?
- [ ] Is it tested?
- [ ] Does it follow project patterns?

## Bug Report Template

```markdown
## Bug: [Short Description]

**Severity**: Critical / High / Medium / Low
**Version**: v0.1.0
**Platform**: Chrome/Windows

### Steps to Reproduce
1. Go to...
2. Click on...
3. Observe...

### Expected Behavior
[What should happen]

### Actual Behavior
[What actually happens]

### Screenshots/Video
[Attach if helpful]

### Additional Context
[Any other info]
```

## Integration

This skill works alongside:

- `fun-advisor` - Is it fun to play?
- `react-game-ui` - Component testing
- `drizzle-game-schema` - Data validation

## Usage in Claude Code

```
/testing-team

"Write E2E tests for the inventory system..."
"Review this PR for code quality..."
"Plan playtesting for the new minigame..."
```
