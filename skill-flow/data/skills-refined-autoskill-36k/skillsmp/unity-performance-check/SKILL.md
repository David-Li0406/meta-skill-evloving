---
name: unity-performance-check
description: Use before committing code or after major changes to verify performance. Catches expensive operations before they cause frame drops.
---

# Unity Performance Check

## Overview

Verify code performance BEFORE it causes problems in production. Frame drops ruin games.

## When to Use

- Before committing new code
- After implementing Update/FixedUpdate logic
- When adding new systems
- Before major milestones
- When users report lag

## The Quick Check (30 seconds)

Run these searches on changed files:

```
// RED FLAGS - Fix these immediately:
GetComponent         // In Update? Cache it
Find(                // In Update? Never do this
FindObjectOfType     // Anywhere? Avoid if possible
new List             // In Update? Preallocate
new Dictionary       // In Update? Preallocate
.ToString()          // In Update? Cache or avoid
string +             // In Update? StringBuilder
foreach              // On non-List? May allocate
```

## The Full Check (5 minutes)

**Use the unity-performance-profiler agent:**
```
Task: Launch unity-performance-profiler agent with:
"Analyze [file/folder] for performance issues"
```

## Performance Rules

### Update Loop (60fps = 16.6ms budget)
| Operation | Cost | Rule |
|-----------|------|------|
| GetComponent | ~1ms | Cache in Start |
| Find/FindObjectOfType | ~5-50ms | Never use |
| Instantiate | ~2-10ms | Use object pool |
| new List/Dictionary | ~0.1ms + GC | Preallocate |
| String concat | ~0.5ms + GC | StringBuilder |
| LINQ query | ~1-5ms + GC | Use loops |
| Physics.Raycast | ~0.1ms | Batch or limit |

### Memory (GC spikes cause stutters)
| Cause | Solution |
|-------|----------|
| new in Update | Preallocate collections |
| String operations | Cache strings, use StringBuilder |
| LINQ methods | Convert to explicit loops |
| Boxing (int to object) | Use generics |
| Closures in lambdas | Cache delegates |
| foreach on IEnumerable | Use for loops on arrays/lists |

### VeilBreakers-Specific
| System | Performance Concern | Solution |
|--------|---------------------|----------|
| Combat | Damage calc per frame | Batch damage events |
| Brand lookup | Switch statement | Dictionary lookup |
| Synergy calc | Recalc every frame | Cache on party change |
| UI updates | Rebuild every frame | Dirty flag pattern |

## Checklist

Before committing, verify:
- [ ] No GetComponent in Update/FixedUpdate
- [ ] No Find/FindObjectOfType anywhere
- [ ] No allocations in hot paths
- [ ] Collections preallocated
- [ ] Strings not concatenated in loops
- [ ] Events properly unsubscribed
- [ ] Object pooling for spawned objects

## If Performance is Bad

1. **Profile first** - Don't guess, measure
2. **Find the hotspot** - Usually 1-2 methods
3. **Fix the algorithm** - O(n²) → O(n) > micro-optimizations
4. **Cache results** - Don't recalculate what hasn't changed
5. **Batch operations** - Process multiple items together
6. **Use jobs/burst** - For heavy math (advanced)
