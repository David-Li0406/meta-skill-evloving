**Skill**: [Multi-Agent Performance Profiling](../SKILL.md)

# Master Performance Optimization Integration Report
## [Project Name] - [Feature/Refactor Name]

**Date**: YYYY-MM-DD
**Integration Agent**: Complete Synthesis
**Status**: ✅ Ready for Implementation

---

## Executive Summary

### Critical Discovery

[One-sentence statement of what IS or ISN'T the bottleneck - surprise finding]

**Example**: QuestDB ILP ingestion is NOT the bottleneck. The system achieves **1.1M rows/sec** for pure database ingestion, which is **11x faster** than the 100K rows/sec target.

The reported "[Current throughput]" pipeline throughput includes:
- **X% [Phase Name]** (Xms)
- **Y% [Phase Name]** (Yms)
- **Z% [Phase Name]** (Zms)

### Key Findings from All Investigation Agents

#### 1. Profiling Agent
- [Primary finding - what takes most time]
- [Quantified performance: Xms for Y rows = Z rows/sec]
- [CPU/memory observations]

#### 2. [Database/Server] Config Agent
- [Current configuration assessment]
- [Production tuning available vs development]
- [Expected improvement percentage]

#### 3. [Client/Library] Agent
- [API usage pattern assessment]
- [Optimization opportunities]
- [Configuration recommendations]

#### 4. [Batch/Size/Algorithm] Agent
- [Current approach assessment]
- [Optimal parameters determination]
- [Tradeoff analysis]

#### 5. Integration Agent (This Report)
- **Primary bottleneck**: [Phase Name] (Xms, Y% of time)
- **Primary solution**: [Recommendation] (Nx improvement)
- **Secondary solution**: [Recommendation] (Nx improvement)
- **Quick win**: [Recommendation] (Nx improvement)

---

## Top 3 Recommendations (Consensus)

All investigation agents agree on these priorities:

### 1. [Optimization Name] (P0) - HIGHEST IMPACT

**Impact**: 🔴 **Nx improvement**
**Effort**: High/Medium/Low (N days)
**Expected Improvement**: [Current] → [Target] [metric]

**Rationale**:
- [Why this is the primary bottleneck]
- [Supporting evidence from profiling]
- [Why this is feasible/safe to implement]
- [Memory/complexity tradeoffs]

**Implementation**:
```python
# Pseudocode or architecture description
from concurrent.futures import ThreadPoolExecutor

def optimized_approach():
    # Implementation details
    pass
```

**Risks/Considerations**:
- [Risk 1 and mitigation]
- [Risk 2 and mitigation]

---

### 2. [Optimization Name] (P1) - HIGH IMPACT

**Impact**: 🟠 **Nx improvement**
**Effort**: High/Medium/Low (N days)
**Expected Improvement**: [Current] → [Target] [metric]

**Rationale**:
- [Why this is secondary priority]
- [Supporting evidence]
- [Comparison to P0]

**Implementation**:
[Description or pseudocode]

---

### 3. [Optimization Name] (P2) - QUICK WIN

**Impact**: 🟡 **Nx improvement**
**Effort**: High/Medium/Low (N hours)
**Expected Improvement**: [Current] → [Target] [metric]

**Rationale**:
- [Why this is a quick win]
- [Low effort, medium impact]
- [Can be done in parallel with P0/P1]

**Implementation**:
[Description or pseudocode]

---

## Agent Investigation Summary

### Profiling Agent Findings

**Location**: `tmp/perf-optimization/profiling/`

**Key Results**:
- [Phase 1]: Xms (Y% of total)
- [Phase 2]: Xms (Y% of total)
- [Phase 3]: Xms (Y% of total)
- [Phase 4]: Xms (Y% of total)

**Recommendation**: [One-sentence summary of profiling agent's primary recommendation]

**Evidence**:
- Benchmark runs: [Number of iterations, consistency of results]
- Throughput: [Current rows/sec, target rows/sec]
- Memory usage: [Peak, average]

---

### [Database/Server] Config Agent Findings

**Location**: `tmp/perf-optimization/[config-type]/`

**Key Results**:
- Current config: [Description of current settings]
- Production config: [Description of optimal settings]
- Expected improvement: <X% (worth it? yes/no)

**Recommendation**: [One-sentence summary]

**Supporting Evidence**:
- [Config parameter 1]: [Current value] → [Recommended value] = [Impact]
- [Config parameter 2]: [Current value] → [Recommended value] = [Impact]

---

### [Client/Library] Agent Findings

**Location**: `tmp/perf-optimization/[client-type]/`

**Key Results**:
- Current API usage: [Description - e.g., "using dataframe() bulk ingestion"]
- Alternative approaches: [List of alternatives considered]
- Expected improvement: <X% (worth it? yes/no)

**Recommendation**: [One-sentence summary]

---

### [Batch/Size/Algorithm] Agent Findings

**Location**: `tmp/perf-optimization/[analysis-type]/`

**Key Results**:
- Current batch size: [X rows/items]
- Optimal range: [Y-Z rows/items]
- Memory overhead: [MB per batch]
- Expected improvement: <X% (current is already optimal? yes/no)

**Recommendation**: [One-sentence summary]

---

## Consensus Analysis

### Areas of Agreement (All Agents)

1. **Primary Bottleneck**: [X/4 agents] agree that [Phase Name] is the bottleneck
2. **Recommended Optimization**: [X/4 agents] recommend [Optimization Name]
3. **Expected Impact**: Consensus on [Nx] improvement potential

### Areas of Disagreement

[If any agents contradict each other, document here. Otherwise state "None - all agents in consensus"]

**Example disagreement**:
- Agent 2 recommends database config tuning (+50% improvement)
- Agent 1 profiling shows database is only 4% of time
- **Resolution**: Profiling agent's empirical evidence takes priority

---

## Implementation Roadmap

### Phase 1: P0 Optimizations (Week 1-2)
- [ ] Implement [P0 Optimization Name]
- [ ] Re-run profiling to verify [Nx] improvement achieved
- [ ] Update benchmarks and documentation

**Success Criteria**: Achieve [Target metric] or better

---

### Phase 2: P1 Optimizations (Week 3-4)
- [ ] Implement [P1 Optimization Name]
- [ ] Re-run profiling to verify [Nx] improvement achieved
- [ ] Update benchmarks

**Success Criteria**: Achieve [Target metric] or better

---

### Phase 3: P2 Quick Wins (As time permits)
- [ ] Implement [P2 Optimization Name]
- [ ] Re-run profiling to verify [Nx] improvement achieved

**Success Criteria**: Any measurable improvement (>1.2x)

---

## Risk Assessment

| Risk     | Likelihood   | Impact       | Mitigation            |
|----------|--------------|--------------|-----------------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Mitigation strategy] |
| [Risk 2] | High/Med/Low | High/Med/Low | [Mitigation strategy] |

---

## Validation Plan

**Before Optimization**:
```bash
# Baseline profiling
uv run python tmp/perf-optimization/profiling/profile_pipeline.py
# Expected output: [Current metric]
```

**After Each Optimization**:
```bash
# Re-run profiling
uv run python tmp/perf-optimization/profiling/profile_pipeline.py
# Verify: [Expected metric after P0/P1/P2]
```

**Acceptance Criteria**:
- P0 implemented → Achieve [X metric] (Nx improvement)
- P1 implemented → Achieve [Y metric] (Nx improvement)
- P2 implemented → Achieve [Z metric] (Nx improvement)

---

## Appendices

### Appendix A: Full Profiling Results
[Link to or inline profiling data]

### Appendix B: Configuration Recommendations
[Link to or inline config recommendations]

### Appendix C: Alternative Approaches Considered
[List of approaches considered but rejected, with rationale]
