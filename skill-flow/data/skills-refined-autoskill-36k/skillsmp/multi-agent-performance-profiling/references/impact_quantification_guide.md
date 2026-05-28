**Skill**: [Multi-Agent Performance Profiling](../SKILL.md)

# Impact Quantification Guide
## How to Assess P0/P1/P2/P3 Priorities

---

## Priority Framework

### P0 (Critical Priority) - HIGHEST IMPACT

**Criteria:**
- **Improvement**: >5x performance gain
- **Bottleneck**: Addresses primary bottleneck (>50% of total time)
- **ROI**: High impact despite high effort
- **Risk**: Acceptable risk/reward ratio

**Examples:**
- Concurrent downloads (10-20x improvement, 90% bottleneck)
- Algorithm replacement (O(n²) → O(n log n) for large n)
- Caching layer for frequently accessed data (10x+ improvement)

**Decision Matrix:**
| Improvement | Effort  | Priority | Implement?                 |
|-------------|---------|----------|----------------------------|
| 10x         | 2 weeks | P0       | ✅ YES                      |
| 5x          | 1 week  | P0       | ✅ YES                      |
| 3x          | 3 weeks | P1       | ⚠️ MAYBE (effort too high) |

---

### P1 (High Priority) - HIGH IMPACT

**Criteria:**
- **Improvement**: 2-5x performance gain
- **Bottleneck**: Addresses secondary bottleneck (20-50% of time)
- **ROI**: Medium-high impact, medium effort
- **Risk**: Low to medium risk

**Examples:**
- Pipeline parallelism (2x improvement by overlapping download + ingest)
- Index optimization in database (2-3x query improvement)
- Memory allocation tuning (2x improvement in GC overhead)

**Decision Matrix:**
| Improvement | Effort  | Priority | Implement?                     |
|-------------|---------|----------|--------------------------------|
| 5x          | 1 week  | P0       | ✅ YES (upgrade to P0)          |
| 3x          | 1 week  | P1       | ✅ YES                          |
| 2x          | 2 weeks | P1       | ⚠️ MAYBE                       |
| 2x          | 1 day   | P0/P1    | ✅ YES (quick win, high impact) |

---

### P2 (Medium Priority) - QUICK WINS

**Criteria:**
- **Improvement**: 1.2-2x performance gain
- **Bottleneck**: May not address primary bottleneck
- **ROI**: Low effort, measurable impact
- **Risk**: Very low risk

**Examples:**
- Streaming ZIP extraction (1.3x improvement, 4-8 hours effort)
- Connection pooling (1.5x improvement for high-frequency requests)
- Buffer size tuning (1.2-1.5x improvement)

**Decision Matrix:**
| Improvement | Effort  | Priority | Implement?                                |
|-------------|---------|----------|-------------------------------------------|
| 1.5x        | 4 hours | P2       | ✅ YES (quick win)                         |
| 1.3x        | 8 hours | P2       | ✅ YES (if time permits)                   |
| 1.2x        | 2 days  | P3       | ⚠️ MAYBE (effort too high for low impact) |

---

### P3 (Low Priority) - MINOR TUNING

**Criteria:**
- **Improvement**: <1.2x performance gain
- **Bottleneck**: Does not address primary bottleneck
- **ROI**: Low impact, any effort level
- **Risk**: Low risk but also low value

**Examples:**
- Logging verbosity reduction (1.05x improvement)
- String concatenation optimization (1.1x improvement)
- Minor config parameter tuning (<5% improvement)

**Decision Matrix:**
| Improvement | Effort | Priority | Implement?              |
|-------------|--------|----------|-------------------------|
| 1.1x        | 1 hour | P3       | ⚠️ MAYBE (if trivial)   |
| 1.05x       | 1 day  | P3       | ❌ NO (not worth effort) |

---

## Calculating Impact

### 1. Measure Baseline

```python
# Run profiling 3+ times, average results
baseline_time = 952  # ms (average of 3 runs)
baseline_throughput = 47_000  # rows/sec
```

### 2. Estimate Optimized Performance

**Method A**: Phase Elimination (if removing bottleneck entirely)
```python
# If download is 857ms (90% of 952ms total):
optimized_time = 952 - 857 + estimated_new_download_time
# e.g., if concurrent downloads reduce to 90ms:
optimized_time = 952 - 857 + 90 = 185ms

improvement = baseline_time / optimized_time
# 952 / 185 = 5.1x improvement
```

**Method B**: Phase Acceleration (if speeding up bottleneck)
```python
# If download is 857ms and we can do 10 concurrent:
new_download_time = 857 / 10 = 86ms  # (assuming perfect parallelism)
optimized_time = 952 - 857 + 86 = 181ms

improvement = 952 / 181 = 5.3x improvement
```

**Method C**: Amdahl's Law (for partial parallelization)
```python
# If 90% of time is parallelizable with 10 workers:
speedup = 1 / ((1 - 0.9) + (0.9 / 10))
# speedup = 1 / (0.1 + 0.09) = 5.26x improvement
```

### 3. Assign Priority

```python
if improvement >= 5.0:
    priority = "P0"
elif improvement >= 2.0:
    priority = "P1"
elif improvement >= 1.2:
    priority = "P2"
else:
    priority = "P3"

# Adjust based on effort:
if effort_days > 10 and improvement < 10:
    priority = downgrade(priority)  # P0 → P1, P1 → P2, etc.
```

---

## Real-World Examples

### Example 1: Concurrent Downloads (P0)

**Baseline**: 857ms download, 952ms total
**Optimization**: 10 concurrent downloads
**Estimated**: 857ms / 10 = 86ms per download (parallelized)
**New Total**: 952 - 857 + 86 = 181ms
**Improvement**: 952 / 181 = **5.3x** ← P0 (>5x)
**Effort**: 1-2 weeks (medium)
**Decision**: ✅ **P0 - Implement immediately**

---

### Example 2: Pipeline Parallelism (P1)

**Baseline**: 952ms total (download → extract → parse → ingest)
**Optimization**: Overlap download(month N+1) with ingest(month N)
**Estimated**: Save 850ms per month (out of ~1900ms for 2 months serial)
**New Total**: 1900ms → 1050ms (for 2 months)
**Improvement**: 1900 / 1050 = **1.8x** per month ← P1 (approaching 2x)
**Effort**: 1 week (medium)
**Decision**: ✅ **P1 - Implement after P0**

---

### Example 3: Streaming ZIP Extraction (P2)

**Baseline**: 11ms extraction (disk I/O), 952ms total
**Optimization**: In-memory extraction (eliminate 3 disk I/O operations)
**Estimated**: 11ms → 2ms (5x faster extraction)
**New Total**: 952 - 11 + 2 = 943ms
**Improvement**: 952 / 943 = **1.01x** ← Wait, this is P3!

**Re-analysis**:
Actually, eliminates disk I/O overhead across entire pipeline, not just extraction phase.
Real savings: ~50ms (extraction + CSV write/read overhead)
**New Total**: 952 - 50 = 902ms
**Improvement**: 952 / 902 = **1.06x** ← Still P3

**BUT**: Effort is only 4-8 hours (very low)
**Adjusted Priority**: ✅ **P2 - Quick win** (despite low impact, trivial effort)

---

## Decision Tree

```
                        START
                          |
                Is improvement ≥5x?
                    /         \
                  YES          NO
                   |            |
                  P0        Is improvement ≥2x?
                           /         \
                         YES          NO
                          |            |
                         P1        Is improvement ≥1.2x?
                                  /         \
                                YES          NO
                                 |            |
                              Is effort       P3
                              <1 day?
                               /    \
                             YES     NO
                              |       |
                             P2      P3

                THEN: Adjust based on effort
                 - If effort >10 days AND improvement <10x → downgrade
                 - If effort <1 day AND improvement >1.1x → upgrade to P2
```

---

## Common Mistakes

### Mistake 1: Optimizing Non-Bottleneck
❌ **Bad**: "Let's optimize the database (4% of time) to get 2x improvement"
- Real improvement: 952ms → 932ms (952 - 20ms savings) = **1.02x** (not 2x!)
- Lesson: 2x improvement on 4% of time = 0.02x overall improvement

✅ **Good**: Optimize the 90% bottleneck first

### Mistake 2: Ignoring Effort
❌ **Bad**: "This 10x improvement is P0, even though it takes 6 months"
- Real cost: 6 months of engineering time
- Lesson: Consider ROI (return on investment)

✅ **Good**: Prioritize high-impact, reasonable-effort optimizations first

### Mistake 3: Overestimating Parallelism
❌ **Bad**: "10 workers = 10x improvement"
- Real improvement: Amdahl's Law limits parallelism
- Serial overhead (10%) + parallel portion (90% / 10 workers) = 5.3x (not 10x)

✅ **Good**: Use Amdahl's Law to estimate realistic parallelism gains

---

## Validation Checklist

Before assigning priority, verify:

- [ ] Profiling data is accurate (3+ runs, consistent results)
- [ ] Improvement calculation accounts for Amdahl's Law (if parallelizing)
- [ ] Effort estimate includes testing, documentation, code review
- [ ] Risk assessment considers backward compatibility, data integrity
- [ ] Priority assignment uses decision tree consistently
- [ ] Consensus across multiple investigation agents (for multi-agent workflows)
