# Evaluator Types

## Technical Evaluators

Analyze price, volume, and technical indicators.

### Base Class
```python
from octobot_evaluators.evaluators import TechnicalEvaluator

class TechnicalEvaluator(AbstractEvaluator):
    """Base for technical analysis evaluators"""
    
    async def eval_impl(self):
        """Implement technical analysis logic"""
        raise NotImplementedError
    
    async def get_candles(self, timeframe: str = None) -> list:
        """Get candlestick data"""
        return await self.exchange_data.get_candles(
            self.symbol, timeframe or self.timeframe
        )
    
    def calculate_rsi(self, period: int = 14) -> float:
        """Calculate RSI indicator"""
        # Implementation
        pass
    
    def calculate_sma(self, period: int = 20) -> float:
        """Calculate Simple Moving Average"""
        # Implementation
        pass
```

### Example: RSI Evaluator
```python
class RSIEvaluator(TechnicalEvaluator):
    PERIOD = 14
    OVERBOUGHT = 70
    OVERSOLD = 30
    
    @classmethod
    def get_name(cls):
        return "RSIEvaluator"
    
    async def eval_impl(self):
        candles = await self.get_candles()
        rsi = self.calculate_rsi(candles, self.PERIOD)
        
        if rsi < self.OVERSOLD:
            await self.evaluation_completed(1.0)  # Strong buy
        elif rsi > self.OVERBOUGHT:
            await self.evaluation_completed(-1.0)  # Strong sell
        else:
            # Scale -1 to 1 based on RSI
            normalized = (rsi - 50) / 50
            await self.evaluation_completed(-normalized)
```

## Social Evaluators

Analyze social media, news, sentiment.

### Base Class
```python
from octobot_evaluators.evaluators import SocialEvaluator

class SocialEvaluator(AbstractEvaluator):
    """Base for social/sentiment evaluators"""
    
    async def eval_impl(self):
        """Analyze social data"""
        raise NotImplementedError
```

### Example: News Sentiment
```python
class NewsSentimentEvaluator(SocialEvaluator):
    @classmethod
    def get_name(cls):
        return "NewsSentiment"
    
    async def eval_impl(self):
        # Fetch news articles
        news = await self.fetch_news(self.symbol)
        
        # Analyze sentiment
        positive = sum(1 for n in news if n["sentiment"] == "positive")
        negative = sum(1 for n in news if n["sentiment"] == "negative")
        
        if positive + negative == 0:
            await self.evaluation_completed(0)
        else:
            score = (positive - negative) / (positive + negative)
            await self.evaluation_completed(score)
```

## Real-time Evaluators

React to live market events.

### Base Class
```python
from octobot_evaluators.evaluators import RealtimeEvaluator

class RealtimeEvaluator(AbstractEvaluator):
    """Base for real-time event evaluators"""
    
    async def eval_impl(self):
        """React to real-time events"""
        raise NotImplementedError
```

### Example: Price Jump
```python
class PriceJumpEvaluator(RealtimeEvaluator):
    THRESHOLD = 0.03  # 3% jump
    
    @classmethod
    def get_name(cls):
        return "PriceJump"
    
    async def eval_impl(self):
        current_price = await self.get_current_price()
        previous_price = await self.get_previous_price()
        
        change = (current_price - previous_price) / previous_price
        
        if abs(change) > self.THRESHOLD:
            # Significant price movement
            signal = 1.0 if change > 0 else -1.0
            await self.evaluation_completed(signal)
```
