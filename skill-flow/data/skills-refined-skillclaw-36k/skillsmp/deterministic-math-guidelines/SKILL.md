---
name: deterministic-math-guidelines
description: Use when writing game logic code - ensures deterministic math operations across platforms
---

# DeterministicMath Usage Guidelines

## Overview

Guidelines for using deterministic math in Swift StateTree game logic to ensure consistent behavior across platforms.

**Announce at start:** "I'm using the deterministic-math-guidelines skill to ensure cross-platform deterministic behavior."

## When to Use

- Writing game logic code
- Implementing physics or movement
- Calculating distances or angles
- Performing vector operations
- Working with collision detection

## Core Principles

### ❌ Never Use Swift's Built-in Math Functions

**Forbidden:**
```swift
// ❌ DON'T DO THIS
let angle = atan2(dy, dx)
let distance = sqrt(dx * dx + dy * dy)
let normalized = vector / sqrt(vector.x * vector.x + vector.y * vector.y)
```

**Why:** These functions are platform-dependent and may produce different results across macOS, Linux, and other platforms.

**Also forbidden:**
- `cos`, `sin`, `atan2`, `sqrt`, `pow`
- Do not import `Darwin` or `Glibc` for math functions

### ✅ Always Use DeterministicMath Methods

**Correct:**
```swift
// ✅ DO THIS
let angle = direction.toAngle()  // IVec2.toAngle() returns Angle
let isNear = position.isWithinDistance(to: target, threshold: distance)
let normalized = direction.normalizedVec()
```

## Available Methods

### Angles

**Get angle from direction vector:**
```swift
let direction = IVec2(x: 1000, y: 0)  // Fixed-point (scale 1000)
let angle = direction.toAngle()  // Returns Angle type
```

### Vector Operations

**Normalize vector:**
```swift
let direction = IVec2(x: 1000, y: 1000)
let normalized = direction.normalizedVec()  // Returns IVec2
```

**Scale vector:**
```swift
let velocity = direction.scaled(by: speed)  // Returns IVec2
```

### Distance Calculations

**Check if within distance:**
```swift
let isNear = position.isWithinDistance(to: target, threshold: 1000)
```

**Move towards target:**
```swift
let newPosition = position.moveTowards(target: target, maxDistance: 1000)
```

## Semantic Types

### Always Prefer Semantic Types

**❌ Don't use raw IVec2:**
```swift
// ❌ DON'T DO THIS
let distanceSquared = position.distanceSquared(to: target)  // Returns Int64
if distanceSquared < threshold * threshold {
    // ...
}
```

**✅ Use semantic types:**
```swift
// ✅ DO THIS
let position = Position2(x: 1000, y: 2000)
let target = Position2(x: 2000, y: 3000)
if position.isWithinDistance(to: target, threshold: 1000) {
    // ...
}
```

### Available Semantic Types

- **Position2**: 2D position with distance/movement methods
- **Velocity2**: 2D velocity with physics operations
- **Angle**: Angle with rotation operations
- **Acceleration2**: 2D acceleration

## Fixed-Point Arithmetic Rules

### ❌ Never Manipulate Scale Directly

**Forbidden:**
```swift
// ❌ DON'T DO THIS
let floatValue = intValue / 1000  // Manual scale conversion
let intValue = floatValue * 1000  // Manual scale conversion
```

**Why:** Scale is an implementation detail. Use semantic types or provided methods.

### ✅ Use Provided Methods

**Correct:**
```swift
// ✅ DO THIS
let position = Position2(x: 1000, y: 2000)  // Fixed-point internally
let floatX = position.x.asFloat()  // If conversion needed
```

## Int64 Return Values

### ❌ Never Use Int64 Directly in Game Logic

**Forbidden:**
```swift
// ❌ DON'T DO THIS
let distanceSquared: Int64 = vec.distanceSquared(to: other)
if distanceSquared < threshold {
    // ...
}
```

**Why:** Int64 return values are for internal library use (collision detection, raycasting).

### ✅ Use Semantic Type Methods

**Correct:**
```swift
// ✅ DO THIS
if position.isWithinDistance(to: target, threshold: 1000) {
    // ...
}
```

## When Helper Methods Don't Exist

**If a needed helper method doesn't exist:**

1. **Propose adding it to DeterministicMath library**
2. **Don't implement workarounds in game logic**
3. **Check existing methods first:**
   - Distance comparisons: `Position2.isWithinDistance(to:threshold:)`
   - Movement: `Position2.moveTowards(target:maxDistance:)`
   - Vector operations: `IVec2.scaled(by:)`, `IVec2.normalizedVec()`

## Collision Detection Range Limits

### ICircle

**Coordinates:**
- Must be within `FixedPoint.WORLD_MAX_COORDINATE` (≈ ±1,073,741,823 fixed-point units)
- ≈ ±1,073,741.823 Float units with scale 1000

**Radius:**
- Must be within `FixedPoint.MAX_CIRCLE_RADIUS` (≈ 2,147,483,647 fixed-point units)
- ≈ 2,147,483.647 Float units with scale 1000

**Invariant enforcement:**
- `ICircle.init` automatically clamps radius to `MAX_CIRCLE_RADIUS`
- Coordinates should be validated by game logic

### IRay and ILineSegment

**Coordinates:**
- Must be within `FixedPoint.WORLD_MAX_COORDINATE`
- Upgraded to use direct Int64 distance calculation
- No longer limited to 46.34 unit limit

**Radius:**
- Circle radius must be within `FixedPoint.MAX_CIRCLE_RADIUS`

### IAABB2

**No inherent coordinate limits:**
- Uses simple comparisons (min/max checks)
- No distance calculation, so no overflow risk
- Supports full `Int32` coordinate range

### Normal Game Scenarios

- Most games will never approach these limits
- `WORLD_MAX_COORDINATE` (≈ 1 million Float units) is very large for most 2D games
- Use `FixedPoint.clampToWorldRange()` to ensure coordinates are within safe bounds

## Code Review Checklist

When reviewing game logic code:

- [ ] No Swift built-in math functions (`cos`, `sin`, `atan2`, `sqrt`, `pow`)
- [ ] No `Darwin` or `Glibc` imports for math
- [ ] No manual fixed-point scale conversions (`/1000`, `*1000`)
- [ ] No direct use of `Int64` return values from `IVec2` methods
- [ ] Semantic types used instead of raw `IVec2` when possible
- [ ] Helper methods from DeterministicMath library used
- [ ] Coordinates validated to be within `WORLD_MAX_COORDINATE`
- [ ] Collision detection uses appropriate types (`ICircle`, `IAABB2`, etc.)

## Examples

### ✅ Good: Using Semantic Types

```swift
struct Player {
    var position: Position2
    var velocity: Velocity2
    
    mutating func moveTowards(target: Position2, speed: Int32) {
        if position.isWithinDistance(to: target, threshold: speed) {
            position = target
        } else {
            let direction = target - position
            let normalized = direction.normalizedVec()
            velocity = Velocity2(normalized.scaled(by: speed))
            position = position.moveTowards(target: target, maxDistance: speed)
        }
    }
}
```

### ❌ Bad: Using Raw Math

```swift
struct Player {
    var x: Int32
    var y: Int32
    
    mutating func moveTowards(targetX: Int32, targetY: Int32, speed: Int32) {
        let dx = targetX - x
        let dy = targetY - y
        let distance = sqrt(Double(dx * dx + dy * dy))  // ❌ Platform-dependent!
        let normalizedX = Int32(Double(dx) / distance * Double(speed))
        let normalizedY = Int32(Double(dy) / distance * Double(speed))
        x += normalizedX
        y += normalizedY
    }
}
```
