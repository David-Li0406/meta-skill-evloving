# Agent Patterns - Complete Catalog

Kaizen provides 12 production-ready agent patterns: 9 multi-agent pipelines + 3 single-agent patterns.

## Multi-Agent Pipeline Patterns (Phase 3)

All 9 patterns accessible via `Pipeline` factory methods:

1. **Sequential** - `Pipeline.sequential(agents)` - Linear processing (A → B → C)
2. **Supervisor-Worker** - `Pipeline.supervisor_worker(supervisor, workers)` - Task decomposition with A2A worker selection ✅
3. **Router (Meta-Controller)** - `Pipeline.router(agents)` - Intelligent routing with A2A capability matching ✅
4. **Ensemble** - `Pipeline.ensemble(agents, synthesizer, top_k=3)` - Multi-perspective with A2A top-k discovery ✅
5. **Blackboard** - `Pipeline.blackboard(specialists, controller)` - Iterative collaboration with A2A specialist selection ✅
6. **Consensus** - `Pipeline.consensus(agents, threshold=0.8)` - Democratic voting
7. **Debate** - `Pipeline.debate(agents, rounds=3)` - Adversarial analysis
8. **Handoff** - `Pipeline.handoff(agents)` - Tier escalation (L1 → L2 → L3)
9. **Parallel** - `Pipeline.parallel(agents, max_workers=10)` - Concurrent execution

✅ = A2A protocol integration (4 patterns with semantic agent discovery)

## Single-Agent Patterns (Phase 4)

3 advanced reasoning patterns extending BaseAgent:

1. **Planning Agent** - Plan Before You Act (Plan → Validate → Execute)
2. **PEV Agent** - Iterative refinement (Plan → Execute → Verify → Refine loop)
3. **Tree-of-Thoughts Agent** - Multi-path exploration (Generate N → Evaluate → Select best)

Plus existing patterns:
4. **ReAct Agent** - Reason + Act interleaving
5. **Chain-of-Thought Agent** - Step-by-step reasoning
6. **SimpleQA Agent** - Direct question answering

## References

**Comprehensive Guides**:
- `sdk-users/apps/kaizen/docs/guides/pipeline-patterns.md` - All 9 pipeline patterns (667 lines)
- `sdk-users/apps/kaizen/docs/guides/single-agent-patterns.md` - All 6 single-agent patterns (400 lines)
- `sdk-users/apps/kaizen/docs/guides/planning-agent.md` - Planning Agent detailed guide
- `sdk-users/apps/kaizen/docs/guides/pev-agent.md` - PEV Agent detailed guide
- `sdk-users/apps/kaizen/docs/guides/tree-of-thoughts-agent.md` - ToT Agent detailed guide
- `sdk-users/apps/kaizen/docs/guides/multi-agent-coordination.md` - Integration guide

**Examples**:
- `examples/2-multi-agent/` - Multi-agent coordination examples
- `examples/1-single-agent/` - Single-agent pattern examples

**Source**:
- `src/kaizen/orchestration/patterns/` - Pipeline pattern implementations
- `src/kaizen/agents/specialized/` - Single-agent pattern implementations
- `src/kaizen/orchestration/pipeline.py` - Pipeline factory methods

**Architecture Decisions**:
- `docs/architecture/adr/ADR-018-pipeline-pattern-architecture-phase3.md` - Pipeline patterns
- `docs/architecture/adr/ADR-019-single-agent-pattern-architecture-phase4.md` - Single-agent patterns
