# New Tool Checklist

Use this checklist when adding a new tool to the LangChain agent.

## Prerequisites

- [ ] Understand what data/action the tool will provide
- [ ] Identify if caching is needed (most tools benefit from caching)
- [ ] Check if similar tool exists in `src/core/tools/`

## Implementation Steps

### 1. Create Tool File

- [ ] Create `src/core/tools/<tool_name>.py`
- [ ] Extend `CachingTool` from `src/core/tools/base.py`
- [ ] Define `name` and `description` class attributes
- [ ] Set `cache_ttl_seconds` appropriate for data freshness needs

### 2. Implement _execute Method

- [ ] Define action types (e.g., "get_info", "search", "list")
- [ ] Implement each action as a private method
- [ ] Return JSON-serializable data (for caching)
- [ ] Handle errors gracefully (don't let exceptions bubble up)

### 3. Register Tool

- [ ] Import tool in `src/core/stock_assistant_agent.py`
- [ ] Add to `_register_tools()` method
- [ ] Pass `cache` and `logger` to constructor
- [ ] Set `enabled=True` (or False for Phase 2 tools)

### 4. Add Configuration (Optional)

- [ ] Add tool config section in `config/config.yaml`
- [ ] Read config in tool constructor
- [ ] Document config options in tool docstring

### 5. Write Tests

- [ ] Create `tests/test_<tool_name>.py`
- [ ] Test each action in isolation
- [ ] Test caching behavior (hit/miss)
- [ ] Test error handling
- [ ] Mock external dependencies (APIs, databases)

### 6. Update Documentation

- [ ] Add tool to file locations table in SKILL.md
- [ ] Update agent docstring if tool adds new capabilities
- [ ] Add example queries that would trigger this tool

### 7. Verify Integration

- [ ] Run `pytest tests/test_<tool_name>.py -v`
- [ ] Test with agent: `python -c "from src.core.stock_assistant_agent import StockAssistantAgent; ..."`
- [ ] Check tool appears in LangGraph Studio

## Example Tool Structure

```
src/core/tools/
├── base.py              # CachingTool base class
├── registry.py          # ToolRegistry singleton
├── stock_symbol.py      # Example: stock lookup tool
├── reporting.py         # Example: report generation
└── <your_new_tool>.py   # Your new tool
```

## Common Pitfalls

| Pitfall | Prevention |
|---------|------------|
| Tool not found by agent | Ensure `enabled=True` in `register()` |
| Cache not working | Pass `cache` parameter to constructor |
| Slow tool execution | Add appropriate `cache_ttl_seconds` |
| Agent can't parse output | Return simple dict/list, not custom objects |
| Tests fail in CI | Mock all external APIs (Yahoo Finance, etc.) |

## Verification Commands

```powershell
# Run tool tests
pytest tests/test_<tool_name>.py -v

# Check tool is registered
python -c "
from src.core.tools.registry import ToolRegistry
registry = ToolRegistry.get_instance()
print([t.name for t in registry.get_enabled_tools()])
"

# Test tool directly
python -c "
from src.core.tools.<tool_name> import <ToolClass>
tool = <ToolClass>()
print(tool._execute(action='get_info', symbol='AAPL'))
"
```
