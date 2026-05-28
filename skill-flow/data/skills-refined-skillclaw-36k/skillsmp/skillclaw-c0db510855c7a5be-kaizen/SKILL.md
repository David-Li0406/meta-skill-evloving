---
name: kaizen
description: Use this skill when you want to implement continuous improvement in code quality, refactor existing code, or discuss process enhancements.
---

# Kaizen: Continuous Improvement

## Overview

Embrace small, continuous improvements to enhance quality and prevent errors by design. The core principle is that many small improvements are more effective than one large change.

## When to Use

**Always applied for:**

- Code implementation and refactoring
- Architecture and design decisions
- Process and workflow improvements
- Error handling and validation

**Philosophy:** Focus on incremental progress and prevention rather than seeking perfection through massive efforts.

## The Four Pillars

### 1. Continuous Improvement (Kaizen)

Small, frequent improvements compound into significant gains.

#### Principles

**Incremental over revolutionary:**

- Make the smallest viable change that improves quality.
- Implement one improvement at a time.
- Verify each change before proceeding to the next.
- Build momentum through small wins.

**Always leave code better:**

- Fix small issues as you encounter them.
- Refactor while you work (within scope).
- Update outdated comments.
- Remove dead code when you see it.

**Iterative refinement:**

- First version: make it work.
- Second pass: make it clear.
- Third pass: make it efficient.
- Avoid trying to accomplish all three at once.

### Examples

<Good>
```typescript
// Iteration 1: Make it work
const calculateTotal = (items: Item[]) => {
  let total = 0;
  for (let i = 0; i < items.length; i++) {
    total += items[i].price * items[i].quantity;
  }
  return total;
};

// Iteration 2: Make it clear (refactor)
const calculateTotal = (items: Item[]): number => {
  return items.reduce((total, item) => {
    return total + (item.price * item.quantity);
  }, 0);
};

// Iteration 3: Make it robust (add validation)
const calculateTotal = (items: Item[]): number => {
  if (!items?.length) return 0;

  return items.reduce((total, item) => {
    if (item.price < 0 || item.quantity < 0) {
      throw new Error('Price and quantity must be non-negative');
    }
    return total + (item.price * item.quantity);
  }, 0);
};
```
Each step is complete, tested, and working.
</Good>

<Bad>
```typescript
// Trying to do everything at once
const calculateTotal = (items: Item[]): number => {
  // Validate, optimize, add features, handle edge cases all together
  if (!items?.length) return 0;
  const validItems = items.filter(item => {
    if (item.price < 0) throw 
```
</Bad>