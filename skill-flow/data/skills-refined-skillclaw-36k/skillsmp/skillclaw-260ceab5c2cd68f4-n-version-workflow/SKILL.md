---
name: n-version-workflow
description: Use this skill when you need to implement N-version programming for critical systems, generating multiple independent solutions to select the best one through comparison.
---

# N-Version Programming Workflow Skill

## Purpose

Execute an N-version programming workflow for critical implementations where multiple independent solutions should be generated and compared to select the best approach.

## When to Use This Skill

**USE FOR:**
- Critical security features (authentication, authorization)
- Complex algorithms with multiple valid approaches
- High-risk refactoring of core components
- Architecture decisions with significant long-term impact
- When correctness is paramount over speed

**AVOID FOR:**
- Simple CRUD operations
- Straightforward bug fixes
- Documentation updates
- Minor UI tweaks
- Time-sensitive quick fixes

## Configuration

### Core Parameters

**N (Number of Versions):**
- `3` - Default for standard tasks
- `4-6` - Critical features requiring high confidence
- `2` - Quick validation of approach

**Selection Criteria** (priority order):
1. Correctness - Meets requirements and passes tests
2. Security - No vulnerabilities or anti-patterns
3. Simplicity - Ruthless simplicity, minimal complexity
4. Philosophy Compliance - Follows project principles
5. Performance - Efficiency and resource usage

**Agent Diversity Profiles:**
- `conservative` - Proven patterns and safety
- `innovative` - Novel approaches and optimizations
- `minimalist` - Ruthless simplicity
- `pragmatic` - Balance trade-offs for practical solutions
- `performance-focused` - Optimize for speed and efficiency

## Execution Process

### Step 1: Prepare Common Context

- **Use prompt-writer agent** to create a crystal-clear specification.
- Document all requirements explicitly.
- Define success criteria measurably.
- Prepare identical task specifications for all N versions.
- Identify evaluation metrics upfront.
- **CRITICAL: Capture explicit user requirements that CANNOT be optimized away.**

**Output:** Single authoritative specification document.

### Step 2: Generate N Independent Implementations

- Spawn N subprocesses simultaneously.
- Each subprocess receives IDENTICAL task specifications.