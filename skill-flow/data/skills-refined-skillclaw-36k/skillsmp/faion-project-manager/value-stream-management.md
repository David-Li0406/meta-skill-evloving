---
id: value-stream-management
name: "Value Stream Management"
domain: PM
skill: faion-project-manager
category: "pmbok8"
---

# Value Stream Management

## Problem

AI productivity gains evaporate when lacking end-to-end visibility. Teams optimize locally while constraints shift.

## Solution: VSM + Flow Metrics + DORA

**Value Stream Mapping (VSM):**
- Originated from lean management
- Popularized by Mik Kersten's "Project to Product" (2018)
- Identifies bottlenecks outside software team

**Key VSM Metrics:**

| Metric | Definition | Purpose |
|--------|------------|---------|
| **Lead Time** | Time from accept work to handoff | End-to-end flow |
| **Process Time** | Time if uninterrupted | Efficiency |
| **%C/A** | % received without rework needed | Quality |
| **Cycle Time** | Time within a process | Process efficiency |
| **Throughput** | Items completed per time period | Delivery rate |

## DORA Metrics

| Metric | Description | Level Indicator |
|--------|-------------|-----------------|
| **Deployment Frequency** | How often code deploys to production | Elite: multiple/day |
| **Change Lead Time** | Commit to production time | Elite: <1 hour |
| **Change Failure Rate** | % deployments causing failure | Elite: <5% |
| **Mean Time to Recovery** | Time to restore service | Elite: <1 hour |
| **Reliability** | Service availability | New metric |

## Combining DORA + Flow Metrics

**DORA:** Development -> Release (DevOps efficiency)
**Flow Metrics:** Customer request -> Release -> Customer (business value)

**Best Practice:**
- Use DORA for DevOps maturity
- Use Flow Metrics for holistic value delivery
- ValueOps Insights: alignment score from both

**VSM Implementation:**
```
1. Map current value stream (request -> delivery)
2. Identify bottlenecks with metrics
3. Measure DORA for DevOps stages
4. Apply Flow Metrics end-to-end
5. Optimize flow, not just individual stages
6. Monitor AI productivity paradox
```
