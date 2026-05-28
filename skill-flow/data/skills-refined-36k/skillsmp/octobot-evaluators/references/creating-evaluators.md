# Creating Evaluators

## Step-by-Step Guide

### 1. Choose Evaluator Type
- Technical: Price/volume analysis
- Social: Sentiment/news
- Real-time: Live events

### 2. Create Tentacle Structure
```
my_evaluator/
├── __init__.py
├── my_evaluator.py
├── metadata.json
└── tests/
    └── test_my_evaluator.py
```

### 3. Implement Evaluator
```python
from octobot_evaluators.evaluators import TechnicalEvaluator

class MyEvaluator(TechnicalEvaluator):
    @classmethod
    def get_name(cls):
        return "MyEvaluator"
    
    async def eval_impl(self):
        # Your logic here
        value = self.calculate_value()
        await self.evaluation_completed(value)
```

### 4. Create metadata.json
```json
{
    "version": "1.0.0",
    "origin_package": "OctoBot-Default-Tentacles",
    "tentacles": ["MyEvaluator"],
    "tentacles-requirements": []
}
```

### 5. Test Evaluator
```python
import pytest
from ...my_evaluator import MyEvaluator

@pytest.mark.asyncio
async def test_evaluation():
    evaluator = MyEvaluator()
    await evaluator.eval_impl()
    # Verify results
```
