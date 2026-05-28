---
name: debate-workflow
description: Use this skill when you need to facilitate structured multi-perspective debates for important architectural decisions and complex trade-offs where multiple valid approaches exist.
---

# Skill body

## Purpose

Implement structured multi-perspective debate for important architectural decisions, design trade-offs, and complex problems where multiple valid approaches exist.

## When to Use This Skill

**USE FOR:**
- Major architectural decisions (framework selection, system design)
- Complex trade-offs with no clear winner
- Controversial changes affecting multiple teams
- High-impact decisions requiring buy-in
- When perspectives genuinely conflict

**AVOID FOR:**
- Simple implementation choices
- Decisions with obvious correct answers
- Time-sensitive hot fixes
- Minor refactoring
- Routine feature additions

## Configuration

### Core Parameters

**Number of Perspectives:**
- `3` - Default (security, performance, simplicity)
- `5` - Extended (add: maintainability, user experience)
- `7` - Comprehensive (add: scalability, cost)

**Debate Rounds:**
- `2` - Quick (position + challenge)
- `3` - Standard (position + challenge + synthesis)
- `4-5` - Deep (multiple challenge/response cycles)

**Convergence Criteria:**
- `100%` - Strong consensus (all perspectives agree)
- `2/3` - Majority rule (two-thirds agreement)
- `synthesis` - Facilitator synthesizes best hybrid
- `evidence` - Follow strongest evidence/arguments

## Standard Perspective Profiles

**Security Perspective:**
- Focus: Vulnerabilities, attack vectors, data protection
- Questions: "What could go wrong? How do we prevent breaches?"
- Agent: security agent

**Performance Perspective:**
- Focus: Speed, scalability, resource efficiency
- Questions: "Will this scale? What are the bottlenecks?"
- Agent: optimizer agent

**Simplicity Perspective:**
- Focus: Minimal complexity, ruthless simplification
- Questions: "Is this the simplest solution? Can we remove abstractions?"
- Agent: cleanup agent + reviewer agent

**Maintainability Perspective:**
- Focus: Long-term evolution, technical debt
- Questions: "Can future developers understand this? How hard to change?"
- Agent: reviewer agent + architect agent

**User Experience Perspective:**
- Focus: API design, usability
- Questions: "Is this user-friendly? How does it affect the end-user experience?"
- Agent: user experience agent