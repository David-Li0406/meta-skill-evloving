---
name: cascade-workflow
description: Use this skill when you need to implement graceful degradation through cascading fallback strategies, ensuring that your system maintains acceptable functionality even when optimal approaches fail.
---

# Skill body

## Purpose

Implement graceful degradation through cascading fallback strategies. When optimal approaches fail or timeout, the system automatically falls back to simpler, more reliable alternatives while maintaining acceptable functionality.

## When to Use This Skill

**USE FOR:**
- External service dependencies (APIs, databases)
- Time-sensitive operations with acceptable degraded modes
- Operations where partial results are better than no results
- High-availability requirements (system must always respond)
- Scenarios where waiting for a perfect solution is worse than a good-enough solution

**AVOID FOR:**
- Operations requiring exact correctness (no acceptable degradation)
- Security-critical operations (authentication, authorization)
- Financial transactions (no room for "approximate")
- When failures must surface to the user (diagnostic operations)
- Simple operations with no meaningful fallback

## Configuration

### Core Parameters

**Timeout Strategy:**
- `aggressive` - Fast failures, quick degradation (5s / 2s / 1s)
- `balanced` - Reasonable attempts (30s / 10s / 5s) - **DEFAULT**
- `patient` - Thorough attempts before fallback (120s / 30s / 10s)
- `custom` - Define your own timeouts

**Fallback Types:**
- `service` - External API → Cached data → Static defaults
- `quality` - Comprehensive → Standard → Minimal analysis
- `freshness` - Real-time → Recent → Historical data
- `completeness` - Full dataset → Sample → Summary
- `accuracy` - Precise → Approximate → Estimate

**Degradation Notification:**
- `silent` - Log only, no user notification
- `warning` - Inform user of degradation
- `explicit` - Detailed explanation of what degraded and why

## Cascade Level Requirements

**PRIMARY (Optimal):**
- Best possible outcome
- May depend on external services
- May be slow or resource-intensive
- Can fail or timeout

**SECONDARY (Acceptable):**
- Reduced quality but functional
- More reliable than primary
- Faster or fewer dependencies
- Acceptable for users

**TERTIARY (Minimal):**
- Basic functionality with significant limitations
- May not meet user expectations but provides some level of service