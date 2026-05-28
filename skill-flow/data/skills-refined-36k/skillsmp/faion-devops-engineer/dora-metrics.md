---
id: dora-metrics
name: "DORA Metrics"
domain: OPS
skill: faion-devops-engineer
category: "best-practices-2026"
---

# DORA Metrics

### Problem

No objective way to measure DevOps performance.

### Solution: Four Key Metrics

| Metric | Elite | High | Medium | Low |
|--------|-------|------|--------|-----|
| Deployment Frequency | On-demand (multiple/day) | Weekly-monthly | Monthly-6mo | <6mo |
| Lead Time for Changes | <1 hour | 1 day-1 week | 1-6 months | >6mo |
| Change Failure Rate | 0-15% | 16-30% | 16-30% | >45% |
| Time to Restore | <1 hour | <1 day | 1 day-1 week | >6mo |

**Implementation:**
1. Instrument CI/CD pipelines
2. Track deployments automatically
3. Correlate incidents with changes
4. Dashboard visibility

**Tools:**
- Sleuth
- LinearB
- Jellyfish
- Built-in (GitHub, GitLab)

**Best Practices:**
- Measure consistently over time
- Focus on trends, not absolute values
- Use metrics to identify bottlenecks
- Don't use metrics punitively
