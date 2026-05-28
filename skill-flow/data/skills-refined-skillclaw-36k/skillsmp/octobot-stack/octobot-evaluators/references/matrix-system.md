# Matrix System

## Evaluation Matrix

The matrix aggregates evaluations from multiple sources.

### Matrix Structure
```python
from octobot_evaluators.matrix import Matrix

class Matrix:
    """Evaluation aggregation matrix"""
    
    def __init__(self):
        self.matrix = {}  # {symbol: {evaluator: value}}
    
    def set_tentacle_value(self, evaluator_name: str, 
                          symbol: str, value: float):
        """Set evaluation value"""
        if symbol not in self.matrix:
            self.matrix[symbol] = {}
        self.matrix[symbol][evaluator_name] = value
    
    def get_matrix_average(self, symbol: str) -> float:
        """Get average evaluation for symbol"""
        if symbol not in self.matrix:
            return 0.0
        
        values = list(self.matrix[symbol].values())
        return sum(values) / len(values) if values else 0.0
    
    def get_weighted_average(self, symbol: str, 
                            weights: dict) -> float:
        """Get weighted evaluation"""
        if symbol not in self.matrix:
            return 0.0
        
        total_weight = 0
        weighted_sum = 0
        
        for evaluator, value in self.matrix[symbol].items():
            weight = weights.get(evaluator, 1.0)
            weighted_sum += value * weight
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
```

### Usage Example
```python
# Create matrix
matrix = Matrix()

# Add evaluations
matrix.set_tentacle_value("RSI", "BTC/USDT", 0.8)
matrix.set_tentacle_value("MACD", "BTC/USDT", 0.6)
matrix.set_tentacle_value("Volume", "BTC/USDT", 0.4)

# Get simple average
avg = matrix.get_matrix_average("BTC/USDT")  # 0.6

# Get weighted average
weights = {"RSI": 2.0, "MACD": 1.5, "Volume": 1.0}
weighted = matrix.get_weighted_average("BTC/USDT", weights)
```

## Signal Aggregation

### Decision Making
```python
def make_trading_decision(matrix: Matrix, symbol: str) -> str:
    """Make trading decision based on matrix"""
    evaluation = matrix.get_matrix_average(symbol)
    
    if evaluation > 0.5:
        return "STRONG_BUY"
    elif evaluation > 0.2:
        return "BUY"
    elif evaluation < -0.5:
        return "STRONG_SELL"
    elif evaluation < -0.2:
        return "SELL"
    else:
        return "NEUTRAL"
```
