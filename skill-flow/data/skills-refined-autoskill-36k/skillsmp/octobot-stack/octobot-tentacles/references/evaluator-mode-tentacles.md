# Evaluator & Mode Tentacles

## Technical Evaluators

### Directory Structure
```
Evaluator/TA/my_indicator/
├── __init__.py
├── my_indicator.py
├── metadata.json
└── tests/
```

### Implementation
```python
from octobot_evaluators.evaluators import TechnicalEvaluator

class MyIndicator(TechnicalEvaluator):
    # Configuration
    PERIOD = 14
    
    @classmethod
    def get_name(cls):
        return "MyIndicator"
    
    async def eval_impl(self):
        """Main evaluation logic"""
        # Get candle data
        candles = await self.get_candles(self.timeframe)
        
        # Calculate indicator
        value = self._calculate_indicator(candles)
        
        # Convert to signal (-1 to 1)
        signal = self._normalize_signal(value)
        
        # Publish result
        await self.evaluation_completed(signal)
    
    def _calculate_indicator(self, candles):
        """Calculate technical indicator"""
        closes = [c['close'] for c in candles]
        # Your calculation logic
        return result
    
    def _normalize_signal(self, value):
        """Convert indicator value to -1..1 range"""
        if value > self.OVERBOUGHT:
            return -1.0  # Sell signal
        elif value < self.OVERSOLD:
            return 1.0   # Buy signal
        else:
            return 0.0   # Neutral
```

## Social Evaluators

### Twitter Sentiment Example
```python
from octobot_evaluators.evaluators import SocialEvaluator

class TwitterSentiment(SocialEvaluator):
    API_KEY = None  # Set from config
    
    @classmethod
    def get_name(cls):
        return "TwitterSentiment"
    
    async def eval_impl(self):
        # Fetch tweets
        tweets = await self._fetch_tweets(self.symbol)
        
        # Analyze sentiment
        sentiment = self._analyze_sentiment(tweets)
        
        # Publish result
        await self.evaluation_completed(sentiment)
    
    async def _fetch_tweets(self, symbol):
        """Fetch recent tweets about symbol"""
        # Twitter API integration
        pass
    
    def _analyze_sentiment(self, tweets):
        """Calculate sentiment score"""
        positive = sum(1 for t in tweets if t['sentiment'] == 'positive')
        negative = sum(1 for t in tweets if t['sentiment'] == 'negative')
        
        if positive + negative == 0:
            return 0.0
        
        return (positive - negative) / (positive + negative)
```

## Strategy Evaluators

Combine multiple indicators into complete strategy.

```python
from octobot_evaluators.evaluators import StrategyEvaluator

class TrendFollowing(StrategyEvaluator):
    @classmethod
    def get_name(cls):
        return "TrendFollowing"
    
    async def eval_impl(self):
        # Get sub-evaluator results
        rsi = self.get_evaluator_value("RSI")
        macd = self.get_evaluator_value("MACD")
        volume = self.get_evaluator_value("Volume")
        
        # Combine signals
        if rsi > 0.5 and macd > 0.3 and volume > 0.4:
            final_signal = 0.8  # Strong buy
        elif rsi < -0.5 and macd < -0.3:
            final_signal = -0.8  # Strong sell
        else:
            final_signal = 0.0  # No signal
        
        await self.evaluation_completed(final_signal)
```

## Trading Modes

### Simple Trading Mode
```python
from octobot_trading.modes import AbstractTradingMode

class SimpleTrader(AbstractTradingMode):
    @classmethod
    def get_name(cls):
        return "SimpleTrader"
    
    async def create_new_orders(self, symbol, final_note):
        """Create orders based on evaluation"""
        # final_note is -1 to 1 from evaluators
        
        if final_note > 0.6:
            # Strong buy signal
            await self._create_buy_order(symbol, final_note)
        
        elif final_note < -0.6:
            # Strong sell signal
            await self._create_sell_order(symbol)
    
    async def _create_buy_order(self, symbol, strength):
        """Create buy order"""
        portfolio = await self.get_portfolio()
        available = portfolio.get_currency_available("USDT")
        
        # Use percentage of available funds based on signal strength
        amount = available * 0.1 * strength
        
        await self.create_order({
            "symbol": symbol,
            "side": "buy",
            "type": "market",
            "amount": amount
        })
    
    async def _create_sell_order(self, symbol):
        """Create sell order"""
        portfolio = await self.get_portfolio()
        base_currency = symbol.split("/")[0]
        available = portfolio.get_currency_available(base_currency)
        
        if available > 0:
            await self.create_order({
                "symbol": symbol,
                "side": "sell",
                "type": "market",
                "amount": available
            })
```

### Advanced Trading Mode (DCA)
```python
class DCAMode(AbstractTradingMode):
    """Dollar Cost Averaging mode"""
    
    INTERVAL_HOURS = 24
    AMOUNT_PER_BUY = 100  # USDT
    
    @classmethod
    def get_name(cls):
        return "DCAMode"
    
    async def create_new_orders(self, symbol, final_note):
        """Execute DCA strategy"""
        # Only buy on schedule, ignore evaluator signals
        if self._should_execute_dca():
            await self._execute_dca_order(symbol)
    
    def _should_execute_dca(self):
        """Check if it's time for next DCA purchase"""
        last_order_time = self.get_last_order_time()
        return (time.time() - last_order_time) > (self.INTERVAL_HOURS * 3600)
    
    async def _execute_dca_order(self, symbol):
        """Execute DCA buy order"""
        await self.create_order({
            "symbol": symbol,
            "side": "buy",
            "type": "market",
            "cost": self.AMOUNT_PER_BUY
        })
```

## Metadata Examples

### Evaluator Metadata
```json
{
    "version": "1.2.0",
    "origin_package": "OctoBot-Default-Tentacles",
    "tentacles": ["MyIndicator"],
    "tentacles-requirements": [],
    "requirements": ["pandas>=1.3.0"]
}
```

### Trading Mode Metadata
```json
{
    "version": "2.0.0",
    "origin_package": "OctoBot-Default-Tentacles",
    "tentacles": ["SimpleTrader"],
    "tentacles-requirements": ["RSI", "MACD"],
    "requirements": []
}
```

## Testing Patterns

### Test Evaluator
```python
import pytest
from ...my_indicator import MyIndicator

@pytest.mark.asyncio
async def test_evaluation():
    evaluator = MyIndicator()
    # Mock data
    evaluator.get_candles = lambda tf: [
        {'close': 100}, {'close': 101}, {'close': 102}
    ]
    
    await evaluator.eval_impl()
    # Verify signal was published
    assert evaluator.eval_note is not None
```

### Test Trading Mode
```python
import pytest
from ...simple_trader import SimpleTrader

@pytest.mark.asyncio
async def test_order_creation():
    mode = SimpleTrader()
    # Mock portfolio
    mode.get_portfolio = lambda: MockPortfolio()
    
    await mode.create_new_orders("BTC/USDT", 0.8)
    
    # Verify order was created
    orders = mode.get_created_orders()
    assert len(orders) == 1
    assert orders[0]['side'] == 'buy'
```
