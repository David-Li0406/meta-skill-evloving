---
name: unity-component-design
description: Use when designing new Unity components (MonoBehaviours, ScriptableObjects, systems). Ensures proper architecture before writing code.
---

# Unity Component Design

## Overview

Design Unity components properly BEFORE writing code. Good architecture prevents rewrites.

## When to Use

- Creating new MonoBehaviour classes
- Designing ScriptableObject data structures
- Building new game systems
- Refactoring existing components

## The Process

### Phase 1: Requirements Gathering

**Ask these questions:**
1. What problem does this component solve?
2. What data does it need?
3. What other systems does it interact with?
4. What events should it emit/receive?
5. Does similar functionality exist already?

### Phase 2: Architecture Decision

**Choose the right type:**
| Use Case | Type |
|----------|------|
| Needs lifecycle (Update, Start) | MonoBehaviour |
| Static game data (monster stats) | ScriptableObject |
| Pure logic, no Unity dependencies | C# class |
| Shared state across scenes | Singleton MonoBehaviour |
| One-off data container | [System.Serializable] class |

### Phase 3: Design the Component

**Use the unity-architect agent:**
```
Task: Launch unity-architect agent with:
"Design a [component type] for [purpose] that [requirements]"
```

The agent will provide:
- Namespace and file location
- Fields with types and attributes
- Methods and their signatures
- Events to emit
- Dependencies to inject
- Inspector setup requirements

### Phase 4: Validate Design

**Checklist before coding:**
- [ ] Follows VeilBreakers namespace convention
- [ ] Uses [SerializeField] private, not public fields
- [ ] Has [RequireComponent] for dependencies
- [ ] Events have corresponding unsubscribe logic
- [ ] No Find() or GetComponent() in hot paths
- [ ] ScriptableObjects for config, not hardcoded values

### Phase 5: Create Implementation Plan

**Break into tasks:**
1. Create the file with class skeleton
2. Add fields and serialization
3. Implement lifecycle methods
4. Add public API
5. Wire up events
6. Write tests (if applicable)
7. Create prefab (if applicable)

## Quick Reference

| VeilBreakers System | Namespace | Base Class |
|---------------------|-----------|------------|
| Combat | VeilBreakers.Combat | MonoBehaviour or ScriptableObject |
| UI | VeilBreakers.UI | MonoBehaviour |
| Data | VeilBreakers.Data | ScriptableObject |
| Core | VeilBreakers.Core | MonoBehaviour (singleton) |
| Utils | VeilBreakers.Utils | Static class |

## Related Skills

- `superpowers:brainstorming` - For exploring requirements
- `superpowers:writing-plans` - For implementation planning
