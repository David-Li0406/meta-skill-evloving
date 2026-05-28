# Add Semantic Route Checklist

Use this checklist when adding a new query classification route to the semantic router.

## Prerequisites

- [ ] Identify the new query category (e.g., "earnings_analysis", "dividend_info")
- [ ] Collect 5-10 example queries users might ask
- [ ] Determine which tool(s) should handle this route

## Implementation Steps

### 1. Add Route to Enum

Edit `src/core/routes.py`:

- [ ] Add new value to `StockQueryRoute` enum
- [ ] Use lowercase_with_underscores naming
- [ ] Keep routes logically ordered

```python
class StockQueryRoute(str, Enum):
    PRICE_CHECK = "price_check"
    # ... existing routes ...
    MY_NEW_ROUTE = "my_new_route"  # Add here
    GENERAL_CHAT = "general_chat"  # Keep fallback last
```

### 2. Add Training Utterances

In `src/core/routes.py`, add to `ROUTE_UTTERANCES`:

- [ ] Add 5-10 diverse example queries
- [ ] Include variations (formal, informal, question formats)
- [ ] Avoid overlap with existing route utterances

```python
ROUTE_UTTERANCES: Dict[StockQueryRoute, List[str]] = {
    # ... existing routes ...
    StockQueryRoute.MY_NEW_ROUTE: [
        "Example query 1",
        "Another way to ask the same thing",
        "Different phrasing of the intent",
        "Question format example?",
        "Command format example",
    ],
}
```

### 3. Update Router (If Needed)

Check `src/core/stock_query_router.py`:

- [ ] Verify router rebuilds routes from `ROUTE_UTTERANCES`
- [ ] Check threshold is appropriate (default 0.7)
- [ ] No code changes usually needed (auto-discovers routes)

### 4. Handle Route in Agent

Edit `src/core/stock_assistant_agent.py` if route needs special handling:

- [ ] Add route case in query processing logic (if any)
- [ ] Map route to specific tool(s) if not automatic

### 5. Test Route Classification

- [ ] Test router classifies new queries correctly
- [ ] Test edge cases don't mis-route
- [ ] Verify confidence scores are reasonable

### 6. Update Documentation

- [ ] Add route to routes table in SKILL.md
- [ ] Document what queries trigger this route
- [ ] Note which tool(s) handle the route

## Testing Commands

```powershell
# Test route classification
python -c "
from src.core.stock_query_router import StockQueryRouter
from src.core.routes import StockQueryRoute

router = StockQueryRouter()
result = router.route('Your test query here')
print(f'Route: {result.route}')
print(f'Confidence: {result.confidence}')
"

# Test multiple queries
python -c "
from src.core.stock_query_router import StockQueryRouter

router = StockQueryRouter()
test_queries = [
    'Query 1 that should match MY_NEW_ROUTE',
    'Query 2 that should match MY_NEW_ROUTE',
    'Query that should NOT match MY_NEW_ROUTE',
]
for q in test_queries:
    result = router.route(q)
    print(f'{q[:40]:40} -> {result.route.value:20} ({result.confidence:.2f})')
"
```

## Route Categories Reference

| Route | Description | Example Tools |
|-------|-------------|---------------|
| `PRICE_CHECK` | Current prices, quotes | `stock_symbol` |
| `NEWS_ANALYSIS` | Headlines, earnings news | `news_tool` |
| `PORTFOLIO` | Holdings, P&L | `portfolio_tool` |
| `TECHNICAL_ANALYSIS` | RSI, MACD, charts | `tradingview` |
| `FUNDAMENTALS` | P/E, financials | `fundamentals_tool` |
| `IDEAS` | Stock picks, strategies | `ideas_tool` |
| `MARKET_WATCH` | Index, sector performance | `market_tool` |
| `GENERAL_CHAT` | Fallback for unmatched | Agent default |

## Common Pitfalls

| Pitfall | Prevention |
|---------|------------|
| Low confidence scores | Add more diverse utterances |
| Conflicts with existing routes | Check utterance overlap |
| Route not recognized | Verify enum value matches utterances key |
| Encoder fails | Check OpenAI API key, HuggingFace fallback |

## Configuration

In `config/config.yaml`:

```yaml
semantic_router:
  encoder:
    primary: openai
    fallback: huggingface
  threshold: 0.7  # Lower = more matches, higher = more strict
  cache_embeddings: true
```

## Threshold Guidelines

| Threshold | Behavior |
|-----------|----------|
| 0.5 | Aggressive matching, more false positives |
| 0.7 | Balanced (default) |
| 0.8+ | Conservative, may fall back to GENERAL_CHAT often |
