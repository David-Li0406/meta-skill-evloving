---
name: "new-agent"
description: "Use this skill ONLY when creating a new hedge fund agent (e.g., Ray Dalio, Peter Lynch). Do not use for scanners or other components."
---

# Scope Constraint

**CRITICAL:** You are executing from the repository root.

- Agent files go in `src/alpacalyzer/agents/{name}_agent.py`
- Tests go in `tests/test_{name}_agent.py`
- Agents are LangGraph nodes in the hedge fund workflow

# Template Placeholders

- `<agent>` - lowercase with underscores (e.g., `ray_dalio`, `peter_lynch`)
- `<Agent>` - PascalCase (e.g., `RayDalio`, `PeterLynch`)
- `<AGENT>` - uppercase with underscores (e.g., `RAY_DALIO`, `PETER_LYNCH`)

# Procedural Steps

## 1. Review Existing Agent Patterns

Before creating a new agent, understand the established patterns:

```bash
# Look at existing agent implementations
cat src/alpacalyzer/agents/warren_buffet_agent.py
cat src/alpacalyzer/agents/cathie_wood_agent.py
cat src/alpacalyzer/agents/technicals_agent.py
```

**Key patterns to observe**:

- Each agent has a specific investment philosophy/focus
- Agents analyze `TradingSignals` and return recommendations
- Agents use GPT-4 for analysis (via `call_gpt.py`)
- Return values update LangGraph state

## 2. Create Agent File

Location: `src/alpacalyzer/agents/<agent>_agent.py`

**Template structure**:

```python
"""<Agent> investment agent following <philosophy> approach."""

from alpacalyzer.gpt.call_gpt import call_gpt
from alpacalyzer.data.models import AgentResponse


SYSTEM_PROMPT = """You are <Agent Name>, a legendary investor known for <key traits>.

Your investment philosophy:
- <Key principle 1>
- <Key principle 2>
- <Key principle 3>

Analyze the following trading opportunity and provide your assessment."""


def analyze_<agent>(ticker: str, trading_signals: dict, **kwargs) -> dict:
    """
    Analyze trading opportunity using <Agent>'s investment philosophy.

    Args:
        ticker: Stock ticker symbol
        trading_signals: Technical analysis results
        **kwargs: Additional context (company info, fundamentals, etc.)

    Returns:
        Dict with agent recommendation and reasoning
    """

    # Prepare analysis context
    context = f"""
Ticker: {ticker}
Price: ${trading_signals['price']:.2f}
Technical Score: {trading_signals['score']:.2f}
Momentum: {trading_signals['momentum']:.1f}%
Signals: {', '.join(trading_signals['signals'])}

Additional Context:
{kwargs.get('context', 'Not available')}

Provide your analysis and recommendation.
"""

    # Call GPT-4 for analysis
    response = call_gpt(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=context,
        response_model=AgentResponse,
        model="gpt-4"
    )

    return {
        "<agent>_analysis": response.analysis,
        "<agent>_recommendation": response.recommendation,
        "<agent>_confidence": response.confidence
    }
```

## 3. Register Agent in Module

Edit `src/alpacalyzer/agents/__init__.py`:

```python
from alpacalyzer.agents.<agent>_agent import analyze_<agent>

__all__ = [
    # ... existing agents ...
    "analyze_<agent>",
]
```

## 4. Integrate with Hedge Fund Workflow

Edit `src/alpacalyzer/hedge_fund.py` to add the agent to the LangGraph workflow:

```python
from alpacalyzer.agents.<agent>_agent import analyze_<agent>

# In the workflow definition, add a node:
workflow.add_node("<agent>", analyze_<agent>)

# Connect to the graph (typically after other agents, before risk manager):
workflow.add_edge("quant", "<agent>")
workflow.add_edge("<agent>", "risk_manager")
```

**Note**: The exact integration point depends on the agent's role. Review the existing workflow structure first.

## 5. Write Tests

Location: `tests/test_<agent>_agent.py`

**Test template**:

```python
"""Tests for <Agent> investment agent."""

from unittest.mock import MagicMock
import pytest

from alpacalyzer.agents.<agent>_agent import analyze_<agent>
from alpacalyzer.data.models import AgentResponse


def test_<agent>_analysis_bullish(mock_openai_client):
    """Test <Agent> analysis with bullish signals."""

    # Mock GPT response
    mock_response = AgentResponse(
        analysis="Strong fundamentals with <key metric>...",
        recommendation="buy",
        confidence=85
    )
    mock_openai_client.chat.completions.create.return_value = mock_response

    # Prepare test data
    trading_signals = {
        "symbol": "AAPL",
        "price": 150.00,
        "score": 0.75,
        "momentum": 5.2,
        "signals": ["Golden Cross", "RSI Bullish"]
    }

    # Execute
    result = analyze_<agent>("AAPL", trading_signals)

    # Assertions
    assert "<agent>_analysis" in result
    assert "<agent>_recommendation" in result
    assert "<agent>_confidence" in result
    assert result["<agent>_recommendation"] in ["buy", "sell", "hold"]
    assert 0 <= result["<agent>_confidence"] <= 100


def test_<agent>_analysis_bearish(mock_openai_client):
    """Test <Agent> analysis with bearish signals."""

    # Mock GPT response
    mock_response = AgentResponse(
        analysis="Concerning indicators suggest...",
        recommendation="sell",
        confidence=70
    )
    mock_openai_client.chat.completions.create.return_value = mock_response

    # Prepare test data
    trading_signals = {
        "symbol": "AAPL",
        "price": 150.00,
        "score": 0.35,
        "momentum": -8.5,
        "signals": ["Death Cross", "RSI Bearish"]
    }

    # Execute
    result = analyze_<agent>("AAPL", trading_signals)

    # Assertions
    assert result["<agent>_recommendation"] in ["buy", "sell", "hold"]


def test_<agent>_handles_missing_context(mock_openai_client):
    """Test agent handles missing optional context gracefully."""

    mock_response = AgentResponse(
        analysis="Limited data available...",
        recommendation="hold",
        confidence=50
    )
    mock_openai_client.chat.completions.create.return_value = mock_response

    trading_signals = {
        "symbol": "AAPL",
        "price": 150.00,
        "score": 0.55,
        "momentum": 0.0,
        "signals": []
    }

    # Should not raise error even with minimal data
    result = analyze_<agent>("AAPL", trading_signals)
    assert result is not None
```

## 6. Run Tests and Verify

```bash
# Run new agent tests
uv run pytest tests/test_<agent>_agent.py -v

# Run all agent tests to ensure no regression
uv run pytest tests/test_*_agent.py

# Integration test (if hedge fund workflow updated)
uv run pytest tests/test_hedge_fund.py
```

## 7. Document the Agent

Add documentation about the agent's philosophy and approach:

**In the agent file docstring**:

```python
"""
<Agent Name> Investment Agent

Philosophy:
    <Agent> is known for <investment approach>. Key principles include:
    - <Principle 1>
    - <Principle 2>
    - <Principle 3>

Focus Areas:
    - <Focus area 1>
    - <Focus area 2>

Examples:
    >>> signals = {...}
    >>> result = analyze_<agent>("AAPL", signals)
    >>> result['<agent>_recommendation']
    'buy'
"""
```

# Reference: Existing Examples

- `src/alpacalyzer/agents/warren_buffet_agent.py` - Value investing, long-term focus
- `src/alpacalyzer/agents/cathie_wood_agent.py` - Innovation/disruptive tech focus
- `src/alpacalyzer/agents/ben_graham_agent.py` - Fundamental analysis, margin of safety
- `src/alpacalyzer/agents/bill_ackman_agent.py` - Activist investing approach
- `src/alpacalyzer/agents/charlie_munger.py` - Quality business analysis
- `src/alpacalyzer/agents/technicals_agent.py` - Pure technical analysis focus
- `src/alpacalyzer/agents/sentiment_agent.py` - Social media sentiment analysis

# Special Considerations

1. **GPT-4 Usage**: Agents use GPT-4 for nuanced analysis. Tests must mock the OpenAI client (already done automatically in `conftest.py`).

2. **State Management**: Agents are LangGraph nodes. They receive state and return updates. The hedge fund workflow aggregates all agent opinions.

3. **Agent Philosophy**: Each agent should have a distinct investment philosophy or focus area. Avoid creating agents that duplicate existing perspectives.

4. **Performance**: Agents make real API calls to OpenAI. In production, consider caching and rate limiting.

5. **Testing**: Always test both bullish and bearish scenarios, plus edge cases with missing data.
