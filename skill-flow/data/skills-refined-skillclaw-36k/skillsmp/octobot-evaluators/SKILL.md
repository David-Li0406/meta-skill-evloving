---
name: octobot-evaluators
description: Strategy evaluation and signal generation framework for OctoBot. Handles technical indicators, matrix evaluations, and trading signals. Use when creating evaluators, implementing indicators, or building signal systems.
version: 1.0.0
license: MIT
---

# OctoBot-Evaluators Development

Help developers work with OctoBot's evaluation framework - the system for analyzing market data and generating trading signals.

## References

Consult these resources as needed:
- ./references/evaluator-types.md -- Technical, Social, Real-time evaluators and their implementations
- ./references/matrix-system.md -- Evaluation matrix, signal aggregation, decision making
- ./references/creating-evaluators.md -- Building custom evaluators, testing, integration

## Overview

OctoBot-Evaluators is a **Core Layer** library providing:
- Technical analysis evaluators (indicators, patterns)
- Social evaluators (sentiment, news)
- Real-time evaluators (price action, volume)
- Evaluation matrix for signal aggregation
- Decision-making framework
- Strategy evaluation coordination

**Layer Position**: Core (no dependencies on Application or Extension layers)
**Used By**: OctoBot, trading modes, strategy optimizers

## Module Structure

```
octobot_evaluators/
├── evaluators/             # Base evaluator classes
│   ├── abstract_evaluator.py
│   ├── technical_evaluator.py
│   ├── social_evaluator.py
│   └── realtime_evaluator.py
├── matrix/                 # Evaluation matrix
│   ├── matrix.py
│   └── matrix_manager.py
├── util/                   # Evaluation utilities
└── api/                    # Public API
```

## Key Concepts

### Evaluator Types

**Technical Evaluators**: Analyze price/volume data
```python
from octobot_evaluators import TechnicalEvaluator

class RSIEvaluator(TechnicalEvaluator):
    async def eval_impl(self):
        rsi = self.calculate_rsi()
        if rsi < 30:
            await self.evaluation_completed(1)  # Buy signal
        elif rsi > 70:
            await self.evaluation_completed(-1)  # Sell signal
```

**Social Evaluators**: Analyze sentiment, news, social media
```python
class TwitterSentimentEvaluator(SocialEvaluator):
    async def eval_impl(self):
        sentiment = await self.analyze_tweets()
        await self.evaluation_completed(sentiment)  # -1 to 1
```

**Real-time Evaluators**: Analyze live price action
```python
class PriceJumpEvaluator(RealtimeEvaluator):
    async def eval_impl(self):
        price_change = self.calculate_price_change()
        if abs(price_change) > 0.05:  # 5% move
            await self.trigger_evaluation()
```

### Evaluation Matrix

Aggregates signals from multiple evaluators:
```python
from octobot_evaluators.matrix import Matrix

matrix = Matrix()
matrix.set_tentacle_value("RSIEvaluator", "BTC/USDT", 0.8)  # Buy
matrix.set_tentacle_value("MACDEvaluator", "BTC/USDT", 0.6)  # Buy
matrix.set_tentacle_value("VolumeEvaluator", "BTC/USDT", -0.3)  # Sell

final_eval = matrix.get_matrix_average("BTC/USDT")  # Aggregate
```

## Common Tasks

### Create Technical Evaluator
```python
from octobot_evaluators import TechnicalEvaluator

class MyIndicatorEvaluator(TechnicalEvaluator):
    @classmethod
    def get_name(cls):
        return "MyIndicator"
    
    async def eval_impl(self):
        # Get candle data
        candles = await self.get_candles()
        
        # Calculate indicator
        value = self.calculate_indicator(candles)
        
        # Generate signal (-1 to 1)
        if value > threshold:
            await self.evaluation_completed(1)
        elif value < -threshold:
            await self.evaluation_completed(-1)
        else:
            await self.evaluation_completed(0)
```

### Subscribe to Evaluator Results
```python
from octobot_evaluators.api import subscribe_to_evaluator

async def on_evaluation(evaluator_name, symbol, value):
    print(f"{evaluator_name} evaluated {symbol}: {value}")

await subscribe_to_evaluator("RSIEvaluator", on_evaluation)
```

### Access Matrix Values
```python
from octobot_evaluators.api import get_matrix_value

eval_value = await get_matrix_value("BTC/USDT")
if eval_value > 0.5:
    # Strong buy signal
    pass
```

## Integration Points

### OctoBot-Trading Integration
Evaluators communicate with trading modes via matrix:
```
Evaluators → Matrix → Trading Mode → Orders
```

### Async-Channel Integration
Evaluators publish results via channels:
```python
await evaluator_producer.send({
    "evaluator": "RSIEvaluator",
    "symbol": "BTC/USDT",
    "value": 0.8,
    "timestamp": time.time()
})
```

## Quick Reference

### Import Patterns
```python
# Base evaluators
from octobot_evaluators.evaluators import (
    AbstractEvaluator,
    TechnicalEvaluator,
    SocialEvaluator,
    RealtimeEvaluator
)

# Matrix
from octobot_evaluators.matrix import Matrix

# API
from octobot_evaluators.api import (
    create_evaluator,
    get_matrix_value,
    subscribe_to_evaluator
)
```

### Evaluation Values
- `-1.0` to `-0.5`: Strong sell
- `-0.5` to `0.0`: Weak sell
- `0.0`: Neutral
- `0.0` to `0.5`: Weak buy
- `0.5` to `1.0`: Strong buy

## Checklist

Before committing changes:
- [ ] Evaluator inherits from correct base class
- [ ] `get_name()` classmethod implemented
- [ ] `eval_impl()` calls `evaluation_completed()`
- [ ] Evaluation values between -1 and 1
- [ ] Matrix integration tested
- [ ] Channel subscriptions properly handled
- [ ] Tests cover edge cases
- [ ] Documentation updated