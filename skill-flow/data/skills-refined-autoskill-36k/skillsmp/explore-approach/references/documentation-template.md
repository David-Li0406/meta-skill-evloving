# Spike Documentation Template

## Template Structure

```markdown
# Spike: [Topic Name]

**Date**: [date]
**Status**: Complete
**Recommendation**: [Approach X]

## Problem Statement

[Technical decision needed]

## Approaches Evaluated

[2-3 approaches with hypotheses]

## Implementation Notes

[Metrics for each approach]

## Comparative Analysis

[Comparison table]

## Risk Assessment

[Risks and mitigations]

## Recommendation

**Primary**: [Approach X]
**Rationale**: [3 reasons with evidence]
**Trade-offs**: [Why acceptable]

## Implementation Guidance

[Dependencies, file structure, integration, testing]

## Prototype Code Samples

[Key code from recommended approach]

## References

[Documentation, discussions, benchmarks]
```

## Common Spike Scenarios

### Real-time Communication

- **Approaches**: WebSocket vs SSE vs Polling
- **Metrics**: Latency, resource usage, browser compatibility
- **Duration**: 2-3 hours

### State Management

- **Approaches**: Zustand vs Jotai vs Redux Toolkit
- **Metrics**: Bundle size, boilerplate, DevX
- **Duration**: 1-2 hours

### Image Optimization

- **Approaches**: next/image vs Cloudinary vs ImageKit
- **Metrics**: Performance, cost, features
- **Duration**: 2-3 hours

### Authentication

- **Approaches**: NextAuth vs Supabase Auth vs custom
- **Metrics**: Security, features, maintenance
- **Duration**: 3-4 hours

## Output Format Example

```markdown
# ✅ Spike Complete: Real-time Technology Evaluation

## 🏆 Recommendation: Server-Sent Events (SSE)

**Why this approach**:

1. Simpler implementation (35% less code than WebSocket)
2. Better browser compatibility
3. Lower resource usage

**Trade-offs**:

- Unidirectional only (acceptable for our use case)

**Performance**: 200ms latency, +15KB bundle
**Complexity**: Easy learning curve
**Risk**: Low - mature spec

## 📊 Comparison Summary

| Approach  | Performance | Complexity | Maintainability | Overall       |
| --------- | ----------- | ---------- | --------------- | ------------- |
| **SSE**   | Good        | Simple     | Excellent       | **WINNER** ⭐ |
| WebSocket | Excellent   | Complex    | Good            | Runner-up     |
| Polling   | Fair        | Simple     | Good            | Fallback      |

## 📝 Full Documentation

`docs/spikes/realtime-tech-evaluation.md`

## 🚀 Next Steps

Use recommendation in spec:
skill:spec("Add real-time notifications using Server-Sent Events")

## 🧹 Spike Cleanup

**Keep**: docs/spikes/realtime-tech-evaluation.md
**Delete**: spike-prototypes/, spike/realtime-tech-evaluation branch
```
