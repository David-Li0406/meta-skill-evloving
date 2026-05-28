---
name: langchain-agent-development
description: Build LangChain ReAct agents with tools, caching, and semantic routing for this stock investment assistant. Use for creating new tools, extending agent capabilities, adding semantic routes, debugging LangGraph issues, and following project patterns (CachingTool, ToolRegistry, AgentResponse).
---

# LangChain Agent Development Skill

> **Project**: dp-stock-investment-assistant  
> **Branch Context**: `integrate-langsmith-studio`  
> **Related Instructions**: [backend-python.instructions.md](../../instructions/backend-python.instructions.md)

## Overview

This project uses LangChain with a **ReAct (Reasoning + Acting)** agent pattern for stock investment assistance. The architecture includes:

| Component | Location | Purpose |
|-----------|----------|---------|
| `StockAssistantAgent` | `src/core/stock_assistant_agent.py` | Main ReAct agent with LangGraph |
| `CachingTool` | `src/core/tools/base.py` | Abstract base class with Redis/memory caching |
| `ToolRegistry` | `src/core/tools/registry.py` | Singleton for centralized tool management |
| `StockQueryRouter` | `src/core/stock_query_router.py` | Semantic router for query classification |
| `AgentResponse` | `src/core/types.py` | Frozen dataclass for structured responses |

---

## Creating New Tools

### Step 1: Extend CachingTool

All tools extend `CachingTool` from `src/core/tools/base.py`:

```python
from src.core.tools.base import CachingTool
from typing import Any, Dict, Optional

class MyNewTool(CachingTool):
    """Tool description for LangChain agent."""
    
    name: str = "my_new_tool"
    description: str = "What this tool does and when to use it"
    
    # Caching configuration
    cache_ttl_seconds: int = 60
    enable_cache: bool = True
    
    def __init__(self, cache: Optional["CacheBackend"] = None, logger=None):
        super().__init__(cache=cache, logger=logger)
    
    def _execute(self, action: str, **kwargs) -> Any:
        """
        Implement actual tool logic here.
        
        Args:
            action: The action to perform (e.g., "get_info", "search")
            **kwargs: Additional parameters
            
        Returns:
            Tool output (will be cached automatically)
        """
        if action == "get_info":
            return self._get_info(kwargs.get("symbol"))
        elif action == "search":
            return self._search(kwargs.get("query"))
        else:
            raise ValueError(f"Unknown action: {action}")
    
    def _get_info(self, symbol: str) -> Dict[str, Any]:
        # Implementation
        pass
    
    def _search(self, query: str) -> list:
        # Implementation
        pass
```

### Step 2: Register with ToolRegistry

Register your tool in `src/core/stock_assistant_agent.py`:

```python
from src.core.tools.registry import ToolRegistry
from src.core.tools.my_new_tool import MyNewTool

# In StockAssistantAgent._register_tools():
registry = ToolRegistry.get_instance(logger=self.logger)
registry.register(MyNewTool(cache=self._cache), enabled=True)
```

### Step 3: Add Tests

Create `tests/test_my_new_tool.py`:

```python
import pytest
from unittest.mock import MagicMock
from src.core.tools.my_new_tool import MyNewTool

@pytest.fixture
def mock_cache():
    cache = MagicMock()
    cache.get_json.return_value = None  # Cache miss
    return cache

def test_tool_executes_get_info(mock_cache):
    tool = MyNewTool(cache=mock_cache)
    result = tool._execute(action="get_info", symbol="AAPL")
    assert result is not None

def test_tool_caches_result(mock_cache):
    tool = MyNewTool(cache=mock_cache)
    tool._execute(action="get_info", symbol="AAPL")
    mock_cache.set_json.assert_called_once()
```

---

## Agent Configuration

### ReAct Agent Setup

The agent is built in `src/core/stock_assistant_agent.py`:

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI

def _build_react_agent(self) -> AgentExecutor:
    # Get enabled tools from registry
    tools = ToolRegistry.get_instance().get_enabled_tools()
    
    # Create LLM
    llm = ChatOpenAI(
        model=self._model_name,
        temperature=0.7,
        api_key=self._api_key,
    )
    
    # Create ReAct agent
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=self._build_prompt(),
    )
    
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
    )
```

### System Prompt Pattern

```python
SYSTEM_PROMPT = """You are a professional stock investment assistant.
You help users with stock analysis, price lookups, technical analysis...

When answering questions:
1. Use the appropriate tools when you need real-time data
2. Provide accurate, factual information based on tool outputs
3. Include relevant disclaimers for investment-related advice
4. Be concise but comprehensive in your responses

Available tools: {tool_names}
"""
```

---

## Semantic Routing

### Adding New Routes

Edit `src/core/routes.py`:

```python
from enum import Enum

class StockQueryRoute(str, Enum):
    PRICE_CHECK = "price_check"
    NEWS_ANALYSIS = "news_analysis"
    PORTFOLIO = "portfolio"
    TECHNICAL_ANALYSIS = "technical_analysis"
    FUNDAMENTALS = "fundamentals"
    IDEAS = "ideas"
    MARKET_WATCH = "market_watch"
    GENERAL_CHAT = "general_chat"
    # Add new route here:
    MY_NEW_ROUTE = "my_new_route"

# Add utterances for training
ROUTE_UTTERANCES: Dict[StockQueryRoute, List[str]] = {
    StockQueryRoute.PRICE_CHECK: [
        "What is AAPL trading at?",
        "Get me the price of Tesla",
        "How much is Bitcoin worth?",
    ],
    # Add utterances for new route:
    StockQueryRoute.MY_NEW_ROUTE: [
        "Example query 1",
        "Example query 2",
        "Example query 3",
    ],
}
```

### Router Configuration

In `config/config.yaml`:

```yaml
semantic_router:
  encoder:
    primary: openai
    fallback: huggingface
    openai_model: "text-embedding-3-small"
    huggingface_model: "sentence-transformers/all-MiniLM-L6-v2"
  threshold: 0.7  # Confidence threshold
  cache_embeddings: true
```

---

## Response Types

### AgentResponse Pattern

Always return structured responses using `AgentResponse` from `src/core/types.py`:

```python
from src.core.types import AgentResponse, ResponseStatus, ToolCall

# Success response
response = AgentResponse.success(
    content="AAPL is trading at $150.25",
    provider="openai",
    model="gpt-4",
    tool_calls=(ToolCall(name="stock_symbol", input={"symbol": "AAPL"}, output={"price": 150.25}),),
)

# Error response
response = AgentResponse.error(
    message="Failed to fetch stock data",
    provider="openai",
    model="gpt-4",
)

# Fallback response (when primary model fails)
response = AgentResponse.fallback(
    content="Response from fallback model",
    provider="grok",
    model="grok-4-1-fast-reasoning",
)
```

---

## LangGraph Studio Integration

### Bootstrap Setup

The project uses `langgraph.json` at the root for LangGraph Studio:

```json
{
  "dependencies": ["."],
  "graphs": {
    "stock_assistant": "./src/core/stock_assistant_agent.py:graph"
  },
  "env": ".env"
}
```

### Debugging with LangGraph Studio

1. **Start Studio**: `langgraph dev` or via VS Code extension
2. **View Graph**: Visualize agent → tool → response flow
3. **Trace Execution**: See each ReAct step (Thought → Action → Observation)
4. **Inspect State**: Check tool outputs and intermediate reasoning

### Common Debugging Patterns

```python
# Enable verbose logging for debugging
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # Shows ReAct steps
    return_intermediate_steps=True,  # Captures tool calls
)

# Access intermediate steps
result = agent_executor.invoke({"input": query})
for step in result.get("intermediate_steps", []):
    action, observation = step
    print(f"Tool: {action.tool}, Input: {action.tool_input}")
    print(f"Output: {observation}")
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Tool not found | Not registered | Call `registry.register(tool, enabled=True)` |
| Cache not working | CacheBackend is None | Pass cache in constructor |
| Agent hangs | Infinite ReAct loop | Add `max_iterations` to AgentExecutor |
| Import errors | PYTHONPATH missing src | Set `PYTHONPATH=$PWD/src` or use bootstrap |

### Debug Checklist

1. **Check tool registration**: `registry.get_enabled_tools()` includes your tool
2. **Verify tool schema**: `tool.args_schema` is valid Pydantic model
3. **Test in isolation**: Call `tool._execute()` directly before testing with agent
4. **Check logs**: Enable `logging.DEBUG` for `src.core` module

---

## Quick Reference

### File Locations

| Purpose | File |
|---------|------|
| Main agent | `src/core/stock_assistant_agent.py` |
| Tool base class | `src/core/tools/base.py` |
| Tool registry | `src/core/tools/registry.py` |
| Existing tools | `src/core/tools/stock_symbol.py`, `reporting.py` |
| Route definitions | `src/core/routes.py` |
| Semantic router | `src/core/stock_query_router.py` |
| Type definitions | `src/core/types.py` |
| Model factory | `src/core/model_factory.py` |
| Tests | `tests/test_agent.py`, `tests/test_langchain_adapter.py` |

### Imports Cheat Sheet

```python
# Agent
from src.core.stock_assistant_agent import StockAssistantAgent

# Tools
from src.core.tools.base import CachingTool
from src.core.tools.registry import ToolRegistry

# Types
from src.core.types import AgentResponse, ResponseStatus, ToolCall, TokenUsage

# Routing
from src.core.routes import StockQueryRoute, ROUTE_UTTERANCES
from src.core.stock_query_router import StockQueryRouter

# Model clients
from src.core.model_factory import ModelClientFactory
from src.core.base_model_client import BaseModelClient
```

---

## Related Documentation

- **Testing Patterns**: See [backend-python.instructions.md](../../instructions/backend-python.instructions.md) § Testing with pytest
- **Service Layer**: See [backend-python.instructions.md](../../instructions/backend-python.instructions.md) § Service Layer
- **Architecture**: See [LANGCHAIN_AGENT_ARCHITECTURE.md](../../../docs/High-level%20Design/LANGCHAIN_AGENT_ARCHITECTURE.md)

---

## Checklists

- [New Tool Checklist](checklists/new_tool_checklist.md)
- [Add Semantic Route Checklist](checklists/add_semantic_route_checklist.md)

---

**Skill Version**: 1.0  
**Last Updated**: 2026-01-12
