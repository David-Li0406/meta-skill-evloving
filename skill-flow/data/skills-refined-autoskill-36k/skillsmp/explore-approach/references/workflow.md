# Spike Workflow

## Phase 1: Understand the Problem

- Extract technical decision from topic
- Ask clarifying questions:
  - Primary Goal: Performance / DX / Maintainability / Cost?
  - Constraints: Bundle size / Browser compatibility / Budget?
  - Timeline: Quick prototype / Thorough evaluation?
  - Integration: Existing tech stack requirements?

## Phase 2: Create Spike Branch

```bash
git checkout -b spike/[topic-name]
```

- `spike/` prefix (NOT `feature/`)
- Descriptive topic name
- Temporary branch (deleted after)

## Phase 3: Define Approaches

- Identify 2-3 approaches to evaluate
- Document hypothesis for each
- Define evaluation criteria:
  - Performance (latency, throughput, resources)
  - Complexity (LOC, learning curve)
  - Maintainability (docs, community)
  - Integration (stack compatibility)
  - Cost (if applicable)

## Phase 4: Implement Prototypes

- Create `spike-prototypes/[approach-name]` directories
- Implement minimal viable prototypes
- Time-box each prototype (1-2 hours max)
- Measure key metrics:
  - Setup time
  - Lines of code
  - Dependencies added
  - Performance (latency, bundle size, memory)
  - Developer experience (learning curve, type safety)

## Phase 5: Comparative Analysis

- Create comprehensive comparison table
- Identify winners by category
- Document trade-offs

## Phase 6: Risk Assessment

- Technical risks for each approach
- Mitigation strategies
- Long-term concerns (vendor lock-in, scalability, breaking changes)

## Phase 7: Document Findings

- Create `docs/spikes/[topic-name].md`
- Permanent documentation for future reference
- Includes:
  - Problem statement
  - Approaches evaluated
  - Implementation notes
  - Comparative analysis
  - Risk assessment
  - **Recommendation with rationale**
  - Implementation guidance
  - Code samples

## Phase 8: Present Recommendation

- Clear summary to agent
- Primary recommendation
- Alternative recommendation (if primary blocked)
- Next steps

## Cleanup Process

After spike completion:

1. **Keep**:
   - `docs/spikes/[topic].md` (permanent)

2. **Optional Delete** (after implementation):
   - `spike-prototypes/` directory
   - `spike/[topic]` branch

3. Agent confirms cleanup with user
