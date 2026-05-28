---
name: OctoBot-Tentacles
description: Plugin repository for OctoBot exchanges, evaluators, trading modes, and services
version: 1.0.0
license: GPL-3.0
---

# OctoBot-Tentacles Development

## Overview

OctoBot-Tentacles is the main plugin repository containing all exchange connectors, technical evaluators, social evaluators, trading modes, and service integrations. Each tentacle is a self-contained plugin with its own metadata, tests, and resources.

## References

- **[Tentacle Structure](references/tentacle-structure.md)**: Directory layout, metadata.json, requirements
- **[Exchange Tentacles](references/exchange-tentacles.md)**: Creating exchange connectors, CCXT integration
- **[Evaluator & Mode Tentacles](references/evaluator-mode-tentacles.md)**: Technical/social evaluators, trading modes

## Key Concepts

### Tentacle Categories
- **Trading/Exchange**: Exchange connectors (Binance, Coinbase, etc.)
- **Evaluator/TA**: Technical analysis evaluators (RSI, MACD, etc.)
- **Evaluator/Social**: Social/sentiment evaluators
- **Evaluator/Strategies**: Complete trading strategies
- **Trading/Mode**: Trading modes (DCA, Grid, Market Making)
- **Services**: Webhooks, notifications, integrations

### Metadata Schema
Every tentacle requires `metadata.json` with version, origin_package, tentacles list, and requirements.

### Testing Pattern
Use relative imports: `from ...binance import Binance`

## Common Tasks

### Create Exchange Tentacle
```python
# Trading/Exchange/my_exchange/my_exchange.py
from octobot_trading.exchanges import RestExchange

class MyExchange(RestExchange):
    DESCRIPTION = "My Exchange connector"
    
    @classmethod
    def get_name(cls):
        return "my_exchange"
    
    @property
    def connector_class(self):
        from octobot_trading.exchanges.connectors import CCXTConnector
        return CCXTConnector
```

### Create Technical Evaluator
```python
# Evaluator/TA/my_indicator/my_indicator.py
from octobot_evaluators.evaluators import TechnicalEvaluator

class MyIndicator(TechnicalEvaluator):
    @classmethod
    def get_name(cls):
        return "MyIndicator"
    
    async def eval_impl(self):
        candles = await self.get_candles()
        # Calculate indicator
        signal = self.calculate_signal(candles)
        await self.evaluation_completed(signal)
```

### Create Trading Mode
```python
# Trading/Mode/my_mode/my_mode.py
from octobot_trading.modes import AbstractTradingMode

class MyMode(AbstractTradingMode):
    @classmethod
    def get_name(cls):
        return "MyMode"
    
    async def create_new_orders(self, symbol, final_note):
        if final_note > 0.5:
            await self.create_order(symbol, "buy")
        elif final_note < -0.5:
            await self.create_order(symbol, "sell")
```

### Add Tentacle Metadata
```json
{
    "version": "1.0.0",
    "origin_package": "OctoBot-Default-Tentacles",
    "tentacles": ["MyExchange"],
    "tentacles-requirements": [],
    "requirements": []
}
```

## Integration Points

- **OctoBot-Trading**: Exchange tentacles integrate with trading engine
- **OctoBot-Evaluators**: Evaluator tentacles plug into evaluation framework
- **OctoBot-Services**: Service tentacles connect to notification systems
- **CCXT**: Exchange tentacles wrap CCXT exchange implementations

## Quick Reference

### Directory Structure
```
Trading/
  Exchange/
    binance/
      __init__.py
      binance.py
      metadata.json
      tests/
Evaluator/
  TA/
    rsi/
      __init__.py
      rsi.py
      metadata.json
      tests/
  Strategies/
    dip_analyzer/
```

### Testing Convention
```python
# tests/test_my_tentacle.py
import pytest
from ...my_tentacle import MyTentacle

@pytest.mark.asyncio
async def test_functionality():
    tentacle = MyTentacle()
    result = await tentacle.do_something()
    assert result is not None
```

### Export Tentacles
```bash
cd OctoBot
python start.py tentacles -p ../../tentacles_default_export.zip -d ../OctoBot-Tentacles
```

## Checklist

- [ ] Create proper directory structure under appropriate category
- [ ] Add `__init__.py` with tentacle class import
- [ ] Implement main tentacle file with get_name() classmethod
- [ ] Create metadata.json with correct origin_package
- [ ] Add tests/ directory with relative imports
- [ ] Test tentacle with pytest
- [ ] Export tentacles using start.py command
- [ ] Verify tentacle loads in OctoBot
- [ ] Document tentacle configuration options
- [ ] Add resources/ folder if needed (icons, configs)
