# Testing Patterns

Agent testing, fixtures, standardized tests from conftest.py.

## 3-Tier Testing Strategy

1. **Tier 1 (Unit)**: Fast, mocked LLM providers
2. **Tier 2 (Integration)**: Real Ollama inference (local, free)
3. **Tier 3 (E2E)**: Real OpenAI/Ollama inference with real infrastructure

**CRITICAL**: NO MOCKING in Tiers 2-3

## E2E Testing for Autonomous Agents

**What E2E Tests Validate:**
- Real LLM inference (Ollama llama3.2:1b - FREE)
- Real database operations (DataFlow with SQLite/PostgreSQL)
- Real tool execution (file system, HTTP, bash)
- Complete autonomous workflows end-to-end

**How to Run:**
```bash
# Install Ollama and pull model (first time only)
ollama pull llama3.2:1b

# Run all E2E tests
pytest tests/e2e/autonomy/ -v

# Run specific systems
pytest tests/e2e/autonomy/test_tool_calling_e2e.py -v
pytest tests/e2e/autonomy/test_planning_e2e.py -v
pytest tests/e2e/autonomy/test_meta_controller_e2e.py -v
pytest tests/e2e/autonomy/test_memory_e2e.py -v
pytest tests/e2e/autonomy/checkpoints/ -v
```

**Writing E2E Tests:**
```python
import pytest
from kaizen.agents.autonomous.base import BaseAutonomousAgent
from kaizen.agents.autonomous.config import AutonomousConfig

@pytest.mark.e2e  # Mark as E2E test
@pytest.mark.asyncio  # Async test
async def test_autonomous_workflow():
    """Test with real LLM and infrastructure."""

    config = AutonomousConfig(
        llm_provider="ollama",
        model="llama3.2:1b",
        enable_interrupts=True
    )

    agent = BaseAutonomousAgent(config=config, signature=MySignature())
    result = await agent.run_autonomous(task="Test task")

    assert result is not None
    assert "result" in result
```

**Available E2E Test Suites:**

| Test Suite | Tests | What It Validates |
|------------|-------|-------------------|
| **Tool Calling** | 4 | File/HTTP/bash tools with permission policies |
| **Planning** | 3 | Planning/PEV/ToT agents with multi-step decomposition |
| **Meta-Controller** | 3 | Semantic routing, fallback strategies |
| **Memory** | 4 | Hot/warm/cold tier persistence |
| **Checkpoints** | 3 | Auto-checkpoint, resume, compression |

**Cost:** $0.00 (Ollama is FREE)

## Standard Fixtures

```python
def test_qa_agent(simple_qa_example, assert_async_strategy, test_queries):
    QAConfig = simple_qa_example.config_classes["QAConfig"]
    QAAgent = simple_qa_example.agent_classes["SimpleQAAgent"]

    agent = QAAgent(config=QAConfig())
    assert_async_strategy(agent)

    result = agent.ask(test_queries["simple"])
    assert isinstance(result, dict)
```

## Available Fixtures

**Example Loading**: `load_example()`, `simple_qa_example`, `code_generation_example`
**Assertions**: `assert_async_strategy()`, `assert_agent_result()`, `assert_shared_memory()`
**Test Data**: `test_queries`, `test_documents`, `test_code_snippets`

## References
- **Source**: `apps/kailash-kaizen/tests/conftest.py`
- **Specialist**: `.claude/agents/frameworks/kaizen-specialist.md` lines 382-404
