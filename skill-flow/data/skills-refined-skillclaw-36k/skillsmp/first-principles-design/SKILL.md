---
name: first-principles-design
description: First-principles approach to plugin design. Use when designing new plugins, evaluating features, or simplifying existing implementations.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, TodoWrite, AskUserQuestion
---

# First-Principles Plugin Design

Design plugins with maximum value and minimum complexity.

## Core Principle

> "What is the simplest thing that could possibly work?"

A plugin should do one thing well. Every tool, parameter, and configuration must earn its place.

## The 5-Step Design Process

### Step 1: Question the Need

Before designing anything, validate the requirement:

```
┌─ What problem are we solving?
│  └─ Can we state it in one sentence?
│
├─ Who has this problem?
│  └─ Real users or hypothetical?
│
├─ What's the current workaround?
│  └─ How painful is it really?
│
├─ Does a solution already exist?
│  └─ Official plugin? Third-party? Manual process?
│
└─ What's the minimum viable solution?
   └─ What's the 20% that delivers 80% value?
```

**Output**: Problem statement + validated need (or decision to not proceed)

### Step 2: Delete Scope

Ruthlessly cut features before you build:

```
Feature triage:
├─ P0 (Must have): Without this, plugin is useless
├─ P1 (Should have): Important but can ship without
├─ P2 (Nice to have): Delete from v1.0
└─ P3 (Future): Delete from planning entirely
```

**Rules**:
- Start with 1-3 tools maximum
- One credential type (API key OR OAuth, not both)
- No configuration options unless absolutely necessary
- No "just in case" error handling

**Output**: Minimal tool list (P0 only)

### Step 3: Simplify the Design

For each remaining tool:

```
Tool simplification:
├─ Parameters
│  ├─ Required: Minimum needed to function
│  ├─ Optional: Challenge each one - delete if possible
│  └─ Derived: Can we compute from other params?
│
├─ Output
│  ├─ Return raw API response when possible
│  ├─ Don't transform data unnecessarily
│  └─ JSON > formatted text (let workflow handle display)
│
└─ Error handling
   ├─ Fail fast with clear messages
   ├─ Don't retry automatically (let user decide)
   └─ Don't catch errors you can't handle meaningfully
```

**Output**: Simple tool specifications

### Step 4: Accelerate Development

Build fast by reusing:

```
Reuse checklist:
├─ Copy from official plugins (don't reinvent)
├─ Use standard patterns (tool → API → response)
├─ Skip abstraction layers (direct implementation)
├─ One file per tool (no shared utilities unless proven needed)
└─ Test with real API, not mocks
```

**Output**: Working implementation

### Step 5: Automate (Only if Needed)

After plugin works:

```
Automation candidates:
├─ Package build script (if releasing multiple times)
├─ Credential validation (if complex)
├─ Integration tests (if critical path)
└─ Nothing else until proven necessary
```

## Plugin Design Template

### Minimal Plugin Structure

```
my_plugin/
├── manifest.yaml          # Metadata
├── main.py                # Entry point (3 lines)
├── provider/
│   ├── provider.yaml      # Credentials (keep simple)
│   └── provider.py        # Validation (optional)
├── tools/
│   ├── tool_one.yaml      # Tool definition
│   └── tool_one.py        # Tool implementation
└── _assets/
    └── icon.svg
```

### Tool Design Checklist

```yaml
tool_design:
  name: verb_noun           # e.g., get_transactions, create_payment

  parameters:
    required:               # What's the minimum to make an API call?
      - name: essential_param
        why: "Cannot function without this"

    optional:               # Challenge each one
      - name: optional_param
        why: "Proven user need, not speculation"
        default: sensible_value

    deleted:                # Document what you didn't include
      - name: removed_param
        why: "Can be derived / rarely used / adds complexity"

  output:
    format: json            # Prefer JSON over text
    transform: minimal      # Pass through API response when possible

  errors:
    strategy: fail_fast     # Clear message, no retry logic
```

## Anti-Patterns in Plugin Design

| Anti-Pattern | Example | Better Approach |
|--------------|---------|-----------------|
| Kitchen sink | 15 tools in one plugin | 3-5 focused tools |
| Over-parameterization | 10 optional params | 1-2 optional max |
| Data transformation | Format dates, rename fields | Return raw, let workflow handle |
| Smart error handling | Auto-retry, fallbacks | Fail fast, clear message |
| Premature abstraction | BaseAPIClient class | Direct httpx calls |
| Both auth methods | API key AND OAuth | Pick one for v1 |

## Decision Tree: Do I Need This?

```
Feature request arrives
        │
        ▼
┌─ Can the plugin work without it? ─┐
│                                   │
▼ YES                               ▼ NO
DELETE IT                    ┌─ Is it P0 for MVP? ─┐
                             │                     │
                             ▼ YES                 ▼ NO
                        INCLUDE IT            DEFER TO v2
```

## Real Example: Transaction Query Tool

### Over-engineered (BAD)

```yaml
parameters:
  - account_id (required)
  - start_date (optional)
  - end_date (optional)
  - status_filter (optional)
  - category_filter (optional)
  - min_amount (optional)
  - max_amount (optional)
  - search_query (optional)
  - sort_order (optional)
  - page_size (optional)
  - page_number (optional)
  - include_pending (optional)
  - format_output (optional)
```

### First-principles (GOOD)

```yaml
parameters:
  - account_id (required)     # Must have
  - limit (optional, default: 50)  # Pagination
  # Everything else: use API defaults or let user filter in workflow
```

## Quick Reference

```
┌─────────────────────────────────────────────────────┐
│  FIRST-PRINCIPLES PLUGIN DESIGN                     │
├─────────────────────────────────────────────────────┤
│  1. QUESTION  → Is this plugin needed at all?       │
│  2. DELETE    → Cut to 1-3 tools, minimal params    │
│  3. SIMPLIFY  → Raw responses, fail fast            │
│  4. ACCELERATE → Copy patterns, skip abstraction    │
│  5. AUTOMATE  → Only after proven need              │
├─────────────────────────────────────────────────────┤
│  ✓ One plugin = one API service                     │
│  ✓ One tool = one operation                         │
│  ✓ Return JSON, let workflow transform              │
│  ✓ Fail fast with clear errors                      │
└─────────────────────────────────────────────────────┘
```
