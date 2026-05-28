# Kaizen Framework Skills

27 skills for Kaizen AI agent framework covering core patterns, multi-agent coordination, multi-modal processing, autonomous tool calling, observability, memory systems, checkpoint/resume, and journey orchestration.

## Skill Categories

### Core Patterns (6 Skills - CRITICAL/HIGH)

Essential patterns for building Kaizen agents:

1. **[kaizen-baseagent-quick.md](kaizen-baseagent-quick.md)** - BaseAgent implementation, signature, config (3-step pattern)
2. **[kaizen-signatures.md](kaizen-signatures.md)** - InputField, OutputField, type-safe I/O, validation
3. **[kaizen-config-patterns.md](kaizen-config-patterns.md)** - Domain config vs BaseAgentConfig, auto-extraction
4. **[kaizen-ux-helpers.md](kaizen-ux-helpers.md)** - extract_list/dict/float/str(), write_to_memory()
5. **[kaizen-agent-execution.md](kaizen-agent-execution.md)** - agent.run(), result handling, async execution
6. **[kaizen-quickstart-template.md](kaizen-quickstart-template.md)** - Complete agent template (copy-paste ready)

**Quick Start**: Begin with `kaizen-baseagent-quick.md` → `kaizen-signatures.md` → `kaizen-quickstart-template.md`

---

### Multi-Agent (5 Skills - HIGH)

Multi-agent coordination and Google A2A protocol:

7. **[kaizen-multi-agent-setup.md](kaizen-multi-agent-setup.md)** - SharedMemoryPool, agent coordination infrastructure
8. **[kaizen-shared-memory.md](kaizen-shared-memory.md)** - write_to_memory(), read_relevant(), patterns
9. **[kaizen-a2a-protocol.md](kaizen-a2a-protocol.md)** - Automatic capability cards, semantic matching (100% Google A2A)
10. **[kaizen-supervisor-worker.md](kaizen-supervisor-worker.md)** - Supervisor-worker pattern, task delegation
11. **[kaizen-agent-patterns.md](kaizen-agent-patterns.md)** - Consensus, debate, specialists, producer-consumer

---

### Multi-Modal (4 Skills - HIGH)

Vision, audio, and multi-modal processing:

12. **[kaizen-vision-processing.md](kaizen-vision-processing.md)** - VisionAgent, OllamaVisionProvider, image analysis
13. **[kaizen-audio-processing.md](kaizen-audio-processing.md)** - Whisper, audio transcription
14. **[kaizen-multimodal-orchestration.md](kaizen-multimodal-orchestration.md)** - MultiModalAgent, vision+audio+text
15. **[kaizen-multimodal-pitfalls.md](kaizen-multimodal-pitfalls.md)** - **CRITICAL**: Common mistakes (kaizen-specialist:301-373)

**IMPORTANT**: Read `kaizen-multimodal-pitfalls.md` FIRST to avoid common API mistakes

---

### Journey Orchestration (1 Skill - HIGH) - NEW in v0.9.0

User journey management with declarative pathways and intent-driven transitions:

16. **[kaizen-journey-orchestration.md](kaizen-journey-orchestration.md)** - Journey, Pathway, Transitions, Context Accumulation, Nexus deployment

**Key Features**: Multi-pathway flows, intent detection (LLM-powered), ReturnToPrevious behavior, context accumulation with merge strategies, Nexus deployment

---

### Advanced Patterns (11 Skills - MEDIUM/HIGH)

Production patterns, enterprise features, tool calling, observability, memory systems, and specialized techniques:

17. **[kaizen-control-protocol.md](kaizen-control-protocol.md)** - Bidirectional agent ↔ client communication
18. **[kaizen-tool-calling.md](kaizen-tool-calling.md)** - Autonomous tool execution with approval workflows
19. **[kaizen-observability.md](kaizen-observability.md)** - Complete observability stack (tracing, metrics, logging, audit)
20. **[kaizen-memory-system.md](kaizen-memory-system.md)** - Persistent memory, learning, and preference adaptation
21. **[kaizen-checkpoint-resume.md](kaizen-checkpoint-resume.md)** - Automatic checkpointing and resume for long-running agents
22. **[kaizen-chain-of-thought.md](kaizen-chain-of-thought.md)** - CoT pattern, step-by-step reasoning
23. **[kaizen-rag-agent.md](kaizen-rag-agent.md)** - RAG implementation with Kaizen
24. **[kaizen-react-pattern.md](kaizen-react-pattern.md)** - ReAct (reasoning + acting)
25. **[kaizen-cost-tracking.md](kaizen-cost-tracking.md)** - Token usage, budget management
26. **[kaizen-streaming.md](kaizen-streaming.md)** - Streaming responses, real-time output
27. **[kaizen-testing-patterns.md](kaizen-testing-patterns.md)** - 3-tier testing, fixtures, standardized tests

**Testing**: All patterns use 3-tier strategy (Unit → Ollama → OpenAI), NO MOCKING in Tiers 2-3

---

## Learning Paths

### Path 1: Basic Agent (15 minutes)
1. `kaizen-baseagent-quick.md` - Core pattern
2. `kaizen-signatures.md` - I/O definitions
3. `kaizen-quickstart-template.md` - Copy template and run

**Output**: Working Q&A agent

---

### Path 2: Production Agent (30 minutes)
1. `kaizen-baseagent-quick.md` - Core pattern
2. `kaizen-config-patterns.md` - Production config
3. `kaizen-ux-helpers.md` - Defensive parsing
4. `kaizen-agent-execution.md` - Error handling
5. `kaizen-testing-patterns.md` - 3-tier testing

**Output**: Production-ready agent with tests

---

### Path 3: Multi-Agent System (45 minutes)
1. `kaizen-baseagent-quick.md` - Core pattern
2. `kaizen-multi-agent-setup.md` - Infrastructure
3. `kaizen-shared-memory.md` - Coordination
4. `kaizen-a2a-protocol.md` - Semantic matching
5. `kaizen-supervisor-worker.md` - Task delegation

**Output**: Multi-agent system with semantic routing

---

### Path 4: Multi-Modal Agent (30 minutes)
1. `kaizen-baseagent-quick.md` - Core pattern
2. **`kaizen-multimodal-pitfalls.md`** - **READ FIRST!**
3. `kaizen-vision-processing.md` - Image analysis
4. `kaizen-audio-processing.md` - Audio transcription
5. `kaizen-multimodal-orchestration.md` - Unified processing

**Output**: Vision + audio agent

---

### Path 5: User Journey Orchestration (45 minutes) - NEW
1. `kaizen-baseagent-quick.md` - Core pattern
2. `kaizen-signatures.md` - Signatures with `__intent__`, `__guidelines__`
3. **`kaizen-journey-orchestration.md`** - Journey, Pathway, Transitions
4. `examples/journey/healthcare_referral/` - Reference implementation

**Output**: Multi-pathway user journey with intent-driven transitions

---

## Critical References

### Comprehensive Documentation (sdk-users/)

**Core Guides** (`sdk-users/apps/kaizen/docs/guides/`):
- **[BaseAgent Architecture](../../../sdk-users/apps/kaizen/docs/guides/baseagent-architecture.md)** - Complete unified agent system (~600 lines)
- **[Multi-Agent Coordination](../../../sdk-users/apps/kaizen/docs/guides/multi-agent-coordination.md)** - Google A2A protocol, 5 patterns (~600 lines)
- **[Signature Programming](../../../sdk-users/apps/kaizen/docs/guides/signature-programming.md)** - Complete signature system
- **[Control Protocol Tutorial](../../../sdk-users/apps/kaizen/docs/guides/control-protocol-tutorial.md)** - Bidirectional communication (13KB)
- **[Integration Patterns](../../../sdk-users/apps/kaizen/docs/guides/integration-patterns.md)** - DataFlow, Nexus, MCP

**Reference Docs** (`sdk-users/apps/kaizen/docs/reference/`):
- **[API Reference](../../../sdk-users/apps/kaizen/docs/reference/api-reference.md)** - Complete API (351 lines)
- **[Control Protocol API](../../../sdk-users/apps/kaizen/docs/reference/control-protocol-api.md)** - Full protocol reference (497 lines)
- **[Memory Patterns Guide](../../../sdk-users/apps/kaizen/docs/reference/memory-patterns-guide.md)** - Memory usage (1,193 lines)
- **[Strategy Selection Guide](../../../sdk-users/apps/kaizen/docs/reference/strategy-selection-guide.md)** - Strategy choice (1,296 lines)
- **[Configuration Guide](../../../sdk-users/apps/kaizen/docs/reference/configuration.md)** - All config options
- **[Troubleshooting](../../../sdk-users/apps/kaizen/docs/reference/troubleshooting.md)** - Common issues

### Quick References
- **Specialist Agent**: `.claude/agents/frameworks/kaizen-specialist.md` (comprehensive reference table)
- **README**: `sdk-users/apps/kaizen/README.md`
- **CLAUDE.md**: `sdk-users/apps/kaizen/CLAUDE.md` (quick start)
- **Examples**: `apps/kailash-kaizen/examples/` (35+ working examples)

### Key Content Sources
- **Multi-Modal Pitfalls**: kaizen-specialist.md lines 301-373 (CRITICAL)
- **A2A Protocol**: kaizen-specialist.md lines 115-165
- **UX Improvements**: kaizen-specialist.md lines 249-298
- **Quickstart Template**: kaizen-specialist.md lines 489-520
- **Test Fixtures**: `apps/kailash-kaizen/tests/conftest.py`

---

## Critical Patterns

### BaseAgent Pattern (Most Common)

```python
from kaizen.core.base_agent import BaseAgent
from kaizen.signatures import Signature, InputField, OutputField
from dataclasses import dataclass

@dataclass
class MyConfig:
    llm_provider: str = "openai"
    model: str = "gpt-4"
    temperature: float = 0.7

class MySignature(Signature):
    question: str = InputField(description="User question")
    answer: str = OutputField(description="Answer")

class MyAgent(BaseAgent):
    def __init__(self, config: MyConfig):
        super().__init__(config=config, signature=MySignature())

    def ask(self, question: str) -> dict:
        return self.run(question=question)
```

### Multi-Agent Pattern

```python
from kaizen.memory.shared_memory import SharedMemoryPool

shared_pool = SharedMemoryPool()

agent1 = ResearcherAgent(config, shared_pool, agent_id="researcher")
agent2 = AnalystAgent(config, shared_pool, agent_id="analyst")

findings = agent1.research("AI trends")
analysis = agent2.analyze(findings)
```

### Vision Pattern (Watch for Pitfalls!)

```python
from kaizen.agents import VisionAgent, VisionAgentConfig

config = VisionAgentConfig(llm_provider="ollama", model="bakllava")
agent = VisionAgent(config=config)

result = agent.analyze(
    image="/path/to/image.png",  # File path, NOT base64
    question="What is this?"     # 'question', NOT 'prompt'
)
print(result['answer'])          # Key is 'answer', NOT 'response'
```

---

## Framework Status (v0.9.0)

**Implementation**: Production-ready
**Performance**: -0.06% overhead (essentially zero), validated with real LLM workloads
**Observability**: Complete stack (tracing, metrics, logging, audit) with Grafana/Prometheus/Jaeger/ELK
**Multi-Modal**: Vision (Ollama + OpenAI) + Audio (Whisper) fully operational
**Multi-Agent**: SupervisorWorkerPattern production-ready
**A2A Protocol**: 100% Google A2A compliant with automatic capability cards
**Journey Orchestration**: Layer 5 with declarative pathways, intent detection, context accumulation (351 tests)

---

## CRITICAL RULES

**ALWAYS:**
- ✅ Use domain configs (e.g., `QAConfig`), let BaseAgent auto-convert
- ✅ Call `self.run()`, not `strategy.execute()`
- ✅ Load `.env` with `load_dotenv()` before creating agents
- ✅ Use extract_*() for result parsing
- ✅ Read `kaizen-multimodal-pitfalls.md` before using vision/audio

**NEVER:**
- ❌ Create BaseAgentConfig manually (use auto-conversion)
- ❌ Use 'prompt' parameter with VisionAgent (use 'question')
- ❌ Pass base64 strings to Ollama (use file paths)
- ❌ Access 'response' key from VisionAgent (use 'answer')
- ❌ Skip real infrastructure testing (NO MOCKING in Tiers 2-3)

---

## Quick References by Task

| Task | Skills |
|------|--------|
| Create basic agent | baseagent-quick, signatures, quickstart-template |
| Production agent | config-patterns, ux-helpers, agent-execution, testing-patterns |
| Production monitoring | **observability** (v0.5.0) - tracing, metrics, logging, audit |
| Interactive agents | **control-protocol** (v0.2.0), baseagent-quick |
| Tool calling | **tool-calling** (v0.2.0), control-protocol |
| Multi-agent system | multi-agent-setup, shared-memory, a2a-protocol, supervisor-worker |
| **User journeys** | **journey-orchestration** (v0.9.0) - pathways, intent detection, context |
| Vision processing | **multimodal-pitfalls** (READ FIRST), vision-processing |
| Audio processing | audio-processing, multimodal-orchestration |
| Chain of thought | chain-of-thought |
| RAG implementation | rag-agent |
| Cost management | cost-tracking |
| Streaming | streaming |

---

**Next Steps**: Start with `kaizen-baseagent-quick.md` for core pattern, then choose a learning path based on your needs.
