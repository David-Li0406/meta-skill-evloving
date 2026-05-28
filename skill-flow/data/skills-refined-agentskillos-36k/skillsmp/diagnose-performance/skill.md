---
name: diagnose-performance
description: Diagnose Manny MCP performance issues and suggest optimizations
tags: [monitoring, performance, optimization, diagnostics]
---

# Performance Diagnostician Skill

**Purpose:** Automatically diagnose performance issues in the Manny MCP codebase and suggest specific fixes or optimizations.

**When to use:**
- User reports "slow" performance
- Builds taking too long
- Low cache hit rates
- After implementing new features (check for regressions)
- Proactively during long-running sessions
- When asked about optimization status

---

## Execution Steps

### 1. Run Full Performance Scan

```bash
./monitor.py --metric all
```

Capture ALL output - you'll interpret this.

### 2. Analyze Each Metric

#### Build Performance
- **Expected:** Incremental 25-35s, Clean 30-40s
- **Alert threshold:** >60s incremental, >70s clean
- **If SLOW:**
  - Check if offline mode (`-o`) is enabled in server.py:377
  - Check thread count (`-T 2`) matches CPU cores
  - Suggest: `rm -rf ~/.m2/repository` if Maven cache corrupted
  - Suggest: Force clean build once to reset state
  - Consider: Phase 4B build artifact caching (CONFIGURATION.md)

#### Cache Performance
- **Expected:** Hit rate >50%
- **Alert threshold:** <30%
- **If LOW:**
  - Cache may be too small (increase `max_size` in cache_layer.py)
  - TTL may be too short (increase `default_ttl`)
  - Cache may have been cleared recently (normal)
  - If persistent: code is changing frequently, consider longer TTL
  - Check: Run cache stats to see what's being cached

#### Search Engine
- **Expected:** Build <1s, total keys ~1,287
- **Alert threshold:** >5s build time
- **If SLOW:**
  - Index may need rebuild
  - File count may have increased significantly
  - Check: Number of Java files (should be ~43)
  - Suggest: Force rebuild with `import search_engine; search_engine._search_index = None`

#### Command Latency
- **Expected:** <10ms average
- **Alert threshold:** >100ms
- **If SLOW:**
  - Event-driven file monitoring may have failed (fallback to polling)
  - Check: Is watchdog installed? (`pip list | grep watchdog`)
  - Check: Response file permissions
  - Suggest: Restart MCP server
  - Consider: Phase 4A optimizations (orjson, WebSocket push)

#### State File Writes
- **Expected:** 6-10/min
- **Alert threshold:** >20/min
- **If HIGH:**
  - State change detection may not be working
  - Check: GameEngine.java:4600-4785 (hasSignificantChange)
  - Player may be very active (normal for combat/skilling)
  - Consider: Increase `unchangedTicks` threshold (currently 10)

### 3. Check for Regressions

Compare current metrics to baselines in OPTIMIZATIONS.md:
- Builds: Should be ~10x faster than pre-optimization (was 5min)
- Commands: Should be ~500x faster (was 500ms)
- Searches: Should be ~1000x faster (was 50ms)

If any metric is regressed:
- Something broke the optimization
- Check git history for recent changes
- Suggest rollback procedures from OPTIMIZATION_QUICK_REFERENCE.md

### 4. Suggest Optimizations

Based on findings:

**If builds are slow but acceptable (35-50s):**
- Mention Phase 4B build artifact caching could help
- Show OPTIMIZATION_PHASE4_AUDIT.md lines 157-202

**If cache hit rate is low but not critical (30-40%):**
- Suggest tuning TTL or max_size
- Show CONFIGURATION.md lines 67-148

**If dashboard polling is visible in logs:**
- Mention Phase 4A could reduce dashboard overhead by 90%
- Show OPTIMIZATION_PHASE4_AUDIT.md lines 21-75

**If everything is healthy:**
- Report: "All optimizations working as expected ✅"
- Show summary of current performance vs baseline
- Mention: Phase 4 optimizations available if needed

### 5. Provide Actionable Fix

Don't just report problems - **provide the exact fix:**

**Example: Slow builds**
```bash
# Fix 1: Check offline mode is enabled
grep "\-o" /home/wil/manny-mcp/server.py

# Fix 2: Clear Maven cache
rm -rf ~/.m2/repository

# Fix 3: Force clean build
./venv/bin/python -c "from server import build_plugin; build_plugin(clean=True)"

# Fix 4: Verify thread count matches CPU
# Edit server.py:377, change -T to match your CPU cores (max 8)
```

**Example: Low cache hit rate**
```python
# Fix: Increase TTL in cache_layer.py:158
_tool_cache = LRUCache(max_size=100, default_ttl=600)  # Was 300, now 600 (10 min)

# Then restart MCP server
```

**Example: Missing search index**
```python
# Force rebuild search index
./venv/bin/python -c "
import search_engine
search_engine._search_index = None
from search_engine import get_search_index
index = get_search_index('/home/wil/Desktop/manny')
print(f'Index rebuilt: {index.get_stats()}')
"
```

---

## Output Format

### Summary Section
```
Performance Diagnostics Report
==============================
Status: [✅ Healthy | ⚠️ Issues Found | ❌ Critical Issues]

Metrics Summary:
- Builds: [time]s (✅ OK | ⚠️ SLOW)
- Cache Hit Rate: [rate]% (✅ OK | ⚠️ LOW)
- Search Engine: [time]s (✅ OK | ⚠️ SLOW)
- Commands: [time]ms (✅ OK | ⚠️ SLOW)
- State Writes: [count]/min (✅ OK | ⚠️ HIGH)
```

### Issues Section (if any)
```
Issues Detected:
1. [Issue name] - [severity]
   Cause: [explanation]
   Fix: [specific command or code change]

2. [Issue name] - [severity]
   ...
```

### Recommendations Section
```
Optimization Opportunities:
- [Current state is optimal] OR
- [Suggest specific Phase 4 optimizations if beneficial]
- [Reference specific documentation sections]
```

---

## Cross-References

Use these docs for detailed guidance:

- **OPTIMIZATION_QUICK_REFERENCE.md** - Troubleshooting recipes (start here!)
- **OPTIMIZATIONS.md** - Phase 1-3 baselines and architecture
- **CONFIGURATION.md** - Settings tuning for specific issues
- **OPTIMIZATION_PHASE4_AUDIT.md** - Future optimization suggestions
- **OPTIMIZATION_ROADMAP.md** - Meta-view of all phases

---

## Proactive Monitoring

If invoked during a long session without user request:

1. Run quick health check: `./monitor.py --metric all`
2. Only report if issues found
3. Be concise - user is overseeing, not managing details
4. Format as: "Performance check: [✅ All healthy | ⚠️ Found X issues]"

---

## Example Invocations

### User says: "Builds seem slow"
```
1. Run: ./monitor.py --metric builds
2. Check output against baseline (30s expected)
3. If >60s: Diagnose (offline mode? Maven cache? Thread count?)
4. Provide specific fix commands
5. Explain expected result after fix
```

### User says: "Is everything optimized?"
```
1. Run: ./monitor.py --metric all
2. Compare all metrics to baselines
3. Report: "Phases 1-3 complete and performing as expected"
4. Mention: "Phase 4 optimizations available (see OPTIMIZATION_PHASE4_AUDIT.md)"
5. Show quick wins if user wants more speed
```

### User asks: "Why is the cache not working?"
```
1. Run: ./monitor.py --metric cache
2. Interpret hit rate and size
3. Check if cache is being populated (size > 0?)
4. Suggest: Increase TTL or max_size if hit rate low
5. Provide exact file path and line number to edit
```

### Proactive (long session, no user request)
```
Every 30-60 minutes of activity:
1. Quick check: ./monitor.py --metric all
2. If all ✅: Stay silent (don't spam user)
3. If any ⚠️: Report concisely: "Performance check: Cache hit rate dropped to 25% (was 50%)"
4. Offer: "Should I diagnose and suggest a fix?"
```

---

## Important Notes

- **Always run monitor.py** - Don't guess based on documentation
- **Provide exact commands** - User is overseeing, not debugging
- **Reference line numbers** - e.g., "server.py:377" not "the build function"
- **Be actionable** - Every problem needs a specific fix
- **Know when to escalate** - If critical regression, alert clearly

---

## Success Criteria

✅ **Skill is successful when:**
- Performance issues are identified automatically
- Root cause is explained clearly
- Specific fix is provided (copy-paste ready)
- User can verify fix worked with monitor.py
- No manual debugging required by user

❌ **Skill fails when:**
- Reports issues without running monitor.py
- Suggests "check the docs" without specific guidance
- Provides vague fixes ("optimize the code")
- Doesn't verify current state before suggesting changes
