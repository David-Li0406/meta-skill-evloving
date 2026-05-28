---
id: cost-optimization
name: "Cost Optimization"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Cost Optimization

## Overview

LLM API costs can quickly escalate in production. This methodology covers strategies to reduce costs while maintaining quality, including model selection, caching, prompt optimization, and architectural patterns.

## When to Use

- Production LLM applications
- High-volume use cases
- Budget-constrained projects
- Optimizing existing applications
- Scaling up deployments

## Key Concepts

### Cost Components

| Component | Impact | Optimization Potential |
|-----------|--------|----------------------|
| Model Selection | 10-100x | High |
| Input Tokens | Linear | Medium-High |
| Output Tokens | Linear | Medium |
| API Calls | Fixed overhead | High (caching) |
| Latency | Indirect | Medium |

### Model Pricing Comparison (2024)

| Model | Input (per 1M) | Output (per 1M) | Context |
|-------|----------------|-----------------|---------|
| GPT-4o | $5.00 | $15.00 | 128K |
| GPT-4o-mini | $0.15 | $0.60 | 128K |
| GPT-3.5-turbo | $0.50 | $1.50 | 16K |
| Claude 3.5 Sonnet | $3.00 | $15.00 | 200K |
| Claude 3 Haiku | $0.25 | $1.25 | 200K |
| Gemini 1.5 Pro | $3.50 | $10.50 | 1M |
| Gemini 1.5 Flash | $0.075 | $0.30 | 1M |

## Implementation

### Cost Tracking

```python
from dataclasses import dataclass
from typing import Dict, Optional
import tiktoken
from datetime import datetime

@dataclass
class ModelPricing:
    input_per_1m: float
    output_per_1m: float

PRICING = {
    "gpt-4o": ModelPricing(5.00, 15.00),
    "gpt-4o-mini": ModelPricing(0.15, 0.60),
    "gpt-4-turbo": ModelPricing(10.00, 30.00),
    "gpt-3.5-turbo": ModelPricing(0.50, 1.50),
    "claude-3-5-sonnet-20241022": ModelPricing(3.00, 15.00),
    "claude-3-haiku-20240307": ModelPricing(0.25, 1.25),
}

class CostTracker:
    """Track and analyze LLM API costs."""

    def __init__(self):
        self.calls = []
        self.total_cost = 0.0
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def record(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        metadata: Dict = None
    ):
        """Record an API call."""
        pricing = PRICING.get(model)
        if not pricing:
            cost = 0.0
        else:
            cost = (
                (input_tokens / 1_000_000) * pricing.input_per_1m +
                (output_tokens / 1_000_000) * pricing.output_per_1m
            )

        self.calls.append({
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": cost,
            "metadata": metadata or {}
        })

        self.total_cost += cost
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens

    def get_summary(self) -> Dict:
        """Get cost summary."""
        by_model = {}
        for call in self.calls:
            model = call["model"]
            if model not in by_model:
                by_model[model] = {"calls": 0, "cost": 0.0, "tokens": 0}
            by_model[model]["calls"] += 1
            by_model[model]["cost"] += call["cost"]
            by_model[model]["tokens"] += call["input_tokens"] + call["output_tokens"]

        return {
            "total_cost": self.total_cost,
            "total_calls": len(self.calls),
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "by_model": by_model,
            "avg_cost_per_call": self.total_cost / len(self.calls) if self.calls else 0
        }

# Usage wrapper
class CostAwareClient:
    """OpenAI client wrapper with cost tracking."""

    def __init__(self, client, tracker: CostTracker = None):
        self.client = client
        self.tracker = tracker or CostTracker()

    def chat_complete(self, **kwargs) -> Dict:
        """Make API call and track cost."""
        response = self.client.chat.completions.create(**kwargs)

        self.tracker.record(
            model=kwargs.get("model", "unknown"),
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens,
            metadata={"function": "chat_complete"}
        )

        return response
```

### Response Caching

```python
import hashlib
import json
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import redis

class ResponseCache:
    """Cache LLM responses to avoid redundant calls."""

    def __init__(
        self,
        redis_client: redis.Redis = None,
        ttl_hours: int = 24,
        max_memory_items: int = 1000
    ):
        self.redis = redis_client
        self.ttl = timedelta(hours=ttl_hours)
        self.memory_cache: Dict[str, Dict] = {}
        self.max_memory_items = max_memory_items

    def _make_key(self, model: str, messages: list, **kwargs) -> str:
        """Create cache key from request parameters."""
        # Include relevant parameters in key
        key_data = {
            "model": model,
            "messages": messages,
            "temperature": kwargs.get("temperature", 1.0),
            "max_tokens": kwargs.get("max_tokens"),
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_str.encode()).hexdigest()

    def get(self, model: str, messages: list, **kwargs) -> Optional[str]:
        """Get cached response if available."""
        key = self._make_key(model, messages, **kwargs)

        # Check memory cache first
        if key in self.memory_cache:
            entry = self.memory_cache[key]
            if datetime.now() < entry["expires"]:
                return entry["response"]
            else:
                del self.memory_cache[key]

        # Check Redis
        if self.redis:
            cached = self.redis.get(f"llm_cache:{key}")
            if cached:
                return json.loads(cached)

        return None

    def set(self, model: str, messages: list, response: str, **kwargs):
        """Cache a response."""
        key = self._make_key(model, messages, **kwargs)

        # Memory cache
        if len(self.memory_cache) >= self.max_memory_items:
            # Remove oldest entries
            oldest_keys = sorted(
                self.memory_cache.keys(),
                key=lambda k: self.memory_cache[k]["created"]
            )[:100]
            for k in oldest_keys:
                del self.memory_cache[k]

        self.memory_cache[key] = {
            "response": response,
            "created": datetime.now(),
            "expires": datetime.now() + self.ttl
        }

        # Redis cache
        if self.redis:
            self.redis.setex(
                f"llm_cache:{key}",
                int(self.ttl.total_seconds()),
                json.dumps(response)
            )

class CachedLLMClient:
    """LLM client with caching."""

    def __init__(self, client, cache: ResponseCache = None):
        self.client = client
        self.cache = cache or ResponseCache()
        self.cache_hits = 0
        self.cache_misses = 0

    def complete(
        self,
        model: str,
        messages: list,
        use_cache: bool = True,
        **kwargs
    ) -> str:
        """Get completion with caching."""
        # Only cache deterministic requests
        temperature = kwargs.get("temperature", 1.0)
        cacheable = use_cache and temperature == 0

        if cacheable:
            cached = self.cache.get(model, messages, **kwargs)
            if cached:
                self.cache_hits += 1
                return cached

        self.cache_misses += 1

        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        result = response.choices[0].message.content

        if cacheable:
            self.cache.set(model, messages, result, **kwargs)

        return result
```

### Model Routing

```python
from enum import Enum
from dataclasses import dataclass
from typing import Callable, Optional

class TaskComplexity(Enum):
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"

@dataclass
class ModelConfig:
    name: str
    max_tokens: int
    cost_per_1k_input: float
    cost_per_1k_output: float
    capabilities: list

class ModelRouter:
    """Route requests to appropriate models based on task complexity."""

    def __init__(self):
        self.models = {
            TaskComplexity.SIMPLE: ModelConfig(
                name="gpt-4o-mini",
                max_tokens=16384,
                cost_per_1k_input=0.00015,
                cost_per_1k_output=0.0006,
                capabilities=["chat", "simple_reasoning"]
            ),
            TaskComplexity.MEDIUM: ModelConfig(
                name="gpt-4o",
                max_tokens=4096,
                cost_per_1k_input=0.005,
                cost_per_1k_output=0.015,
                capabilities=["chat", "reasoning", "code"]
            ),
            TaskComplexity.COMPLEX: ModelConfig(
                name="gpt-4-turbo",
                max_tokens=4096,
                cost_per_1k_input=0.01,
                cost_per_1k_output=0.03,
                capabilities=["chat", "complex_reasoning", "code", "analysis"]
            )
        }

    def classify_complexity(self, prompt: str) -> TaskComplexity:
        """Classify task complexity heuristically."""
        prompt_lower = prompt.lower()

        # Simple indicators
        simple_indicators = [
            "translate", "summarize briefly", "yes or no",
            "list", "define", "what is"
        ]

        # Complex indicators
        complex_indicators = [
            "analyze", "compare and contrast", "write code",
            "debug", "explain in detail", "step by step",
            "multiple perspectives", "evaluate"
        ]

        simple_score = sum(1 for ind in simple_indicators if ind in prompt_lower)
        complex_score = sum(1 for ind in complex_indicators if ind in prompt_lower)

        if complex_score >= 2 or len(prompt) > 2000:
            return TaskComplexity.COMPLEX
        elif simple_score >= 2 or len(prompt) < 200:
            return TaskComplexity.SIMPLE
        else:
            return TaskComplexity.MEDIUM

    def get_model(
        self,
        prompt: str,
        force_complexity: Optional[TaskComplexity] = None
    ) -> str:
        """Get appropriate model for the task."""
        complexity = force_complexity or self.classify_complexity(prompt)
        return self.models[complexity].name

    def estimate_cost(
        self,
        prompt: str,
        estimated_output_tokens: int = 500
    ) -> Dict:
        """Estimate cost for different model options."""
        import tiktoken
        encoding = tiktoken.get_encoding("cl100k_base")
        input_tokens = len(encoding.encode(prompt))

        estimates = {}
        for complexity, config in self.models.items():
            cost = (
                (input_tokens / 1000) * config.cost_per_1k_input +
                (estimated_output_tokens / 1000) * config.cost_per_1k_output
            )
            estimates[complexity.value] = {
                "model": config.name,
                "cost": cost,
                "input_tokens": input_tokens
            }

        return estimates
```

### Prompt Optimization

```python
import tiktoken
from typing import List, Dict

class PromptOptimizer:
    """Optimize prompts for cost efficiency."""

    def __init__(self, model: str = "gpt-4o"):
        self.encoding = tiktoken.encoding_for_model(model)

    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return len(self.encoding.encode(text))

    def truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """Truncate text to max tokens."""
        tokens = self.encoding.encode(text)
        if len(tokens) <= max_tokens:
            return text
        return self.encoding.decode(tokens[:max_tokens])

    def compress_prompt(self, prompt: str) -> str:
        """Apply basic compression techniques."""
        # Remove extra whitespace
        import re
        compressed = re.sub(r'\s+', ' ', prompt)

        # Remove redundant phrases
        redundant = [
            "please ", "kindly ", "could you please ",
            "I would like you to ", "I need you to "
        ]
        for phrase in redundant:
            compressed = compressed.replace(phrase, "")

        return compressed.strip()

    def optimize_system_prompt(self, system_prompt: str) -> str:
        """Optimize system prompt for brevity."""
        # Remove verbose instructions
        optimized = system_prompt

        verbose_to_concise = {
            "You are a helpful assistant that": "You are an assistant that",
            "Please make sure to": "",
            "It is important that you": "",
            "Remember to always": "",
        }

        for verbose, concise in verbose_to_concise.items():
            optimized = optimized.replace(verbose, concise)

        return optimized.strip()

    def summarize_context(
        self,
        context: str,
        max_tokens: int,
        client
    ) -> str:
        """Summarize long context to reduce tokens."""
        current_tokens = self.count_tokens(context)

        if current_tokens <= max_tokens:
            return context

        # Use cheaper model to summarize
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"Summarize the following text in approximately {max_tokens} tokens, preserving key information."
                },
                {"role": "user", "content": context}
            ],
            max_tokens=max_tokens
        )

        return response.choices[0].message.content
```

### Batching Requests

```python
import asyncio
from typing import List, Dict
from openai import AsyncOpenAI

class BatchProcessor:
    """Process multiple requests efficiently."""

    def __init__(
        self,
        client: AsyncOpenAI,
        batch_size: int = 10,
        delay_between_batches: float = 0.1
    ):
        self.client = client
        self.batch_size = batch_size
        self.delay = delay_between_batches

    async def process_batch(
        self,
        prompts: List[str],
        model: str = "gpt-4o-mini",
        **kwargs
    ) -> List[str]:
        """Process multiple prompts in parallel batches."""
        results = []

        for i in range(0, len(prompts), self.batch_size):
            batch = prompts[i:i + self.batch_size]

            # Process batch in parallel
            tasks = [
                self._single_request(prompt, model, **kwargs)
                for prompt in batch
            ]

            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            results.extend(batch_results)

            # Rate limiting
            if i + self.batch_size < len(prompts):
                await asyncio.sleep(self.delay)

        return results

    async def _single_request(
        self,
        prompt: str,
        model: str,
        **kwargs
    ) -> str:
        """Make a single async request."""
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {e}"
```

### Production Cost Optimization Service

```python
from dataclasses import dataclass
from typing import Optional, Dict, Any
import logging

@dataclass
class CostOptimizationConfig:
    enable_caching: bool = True
    enable_model_routing: bool = True
    enable_prompt_compression: bool = True
    cache_ttl_hours: int = 24
    default_model: str = "gpt-4o-mini"
    fallback_model: str = "gpt-4o"
    max_retries: int = 3
    budget_limit_per_day: Optional[float] = None

class CostOptimizedLLM:
    """Production LLM service with cost optimization."""

    def __init__(
        self,
        client,
        config: Optional[CostOptimizationConfig] = None
    ):
        self.client = client
        self.config = config or CostOptimizationConfig()
        self.logger = logging.getLogger(__name__)

        # Initialize components
        self.cache = ResponseCache(ttl_hours=self.config.cache_ttl_hours)
        self.router = ModelRouter()
        self.optimizer = PromptOptimizer()
        self.tracker = CostTracker()

    def complete(
        self,
        prompt: str,
        system_prompt: str = "",
        force_model: Optional[str] = None,
        use_cache: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """Get completion with all optimizations."""
        # Check budget
        if self._is_over_budget():
            raise Exception("Daily budget limit exceeded")

        # Optimize prompts
        if self.config.enable_prompt_compression:
            prompt = self.optimizer.compress_prompt(prompt)
            system_prompt = self.optimizer.optimize_system_prompt(system_prompt)

        # Build messages
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        # Select model
        if force_model:
            model = force_model
        elif self.config.enable_model_routing:
            model = self.router.get_model(prompt)
        else:
            model = self.config.default_model

        # Check cache
        if self.config.enable_caching and use_cache:
            cached = self.cache.get(model, messages, **kwargs)
            if cached:
                self.logger.info(f"Cache hit for model {model}")
                return {
                    "content": cached,
                    "model": model,
                    "from_cache": True,
                    "cost": 0.0
                }

        # Make API call
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                **kwargs
            )
        except Exception as e:
            # Fallback to different model
            self.logger.warning(f"Model {model} failed, trying fallback")
            response = self.client.chat.completions.create(
                model=self.config.fallback_model,
                messages=messages,
                **kwargs
            )
            model = self.config.fallback_model

        content = response.choices[0].message.content

        # Track cost
        self.tracker.record(
            model=model,
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens
        )

        # Cache response
        if self.config.enable_caching and use_cache:
            temperature = kwargs.get("temperature", 1.0)
            if temperature == 0:
                self.cache.set(model, messages, content, **kwargs)

        # Calculate cost
        pricing = PRICING.get(model)
        cost = 0.0
        if pricing:
            cost = (
                (response.usage.prompt_tokens / 1_000_000) * pricing.input_per_1m +
                (response.usage.completion_tokens / 1_000_000) * pricing.output_per_1m
            )

        return {
            "content": content,
            "model": model,
            "from_cache": False,
            "cost": cost,
            "tokens": {
                "input": response.usage.prompt_tokens,
                "output": response.usage.completion_tokens
            }
        }

    def _is_over_budget(self) -> bool:
        """Check if daily budget is exceeded."""
        if self.config.budget_limit_per_day is None:
            return False
        return self.tracker.total_cost >= self.config.budget_limit_per_day

    def get_cost_report(self) -> Dict:
        """Get cost report."""
        return self.tracker.get_summary()
```

## Best Practices

1. **Model Selection**
   - Start with cheapest model that works
   - Use routing for mixed workloads
   - Reserve expensive models for complex tasks

2. **Caching**
   - Cache deterministic responses (temperature=0)
   - Use content-based cache keys
   - Set appropriate TTLs

3. **Prompt Engineering**
   - Keep prompts concise
   - Remove redundant instructions
   - Use structured outputs to reduce tokens

4. **Batching**
   - Group similar requests
   - Use async for parallel processing
   - Balance batch size and latency

5. **Monitoring**
   - Track cost per feature/endpoint
   - Set budget alerts
   - Analyze token usage patterns

## Common Pitfalls

1. **Over-caching** - Stale responses for dynamic content
2. **Wrong Model** - Using expensive models for simple tasks
3. **No Monitoring** - Surprise bills at month end
4. **Ignoring Output Tokens** - They cost more than input
5. **No Budget Limits** - Runaway costs in production
6. **Premature Optimization** - Sacrificing quality for cost

## References

- [OpenAI Pricing](https://openai.com/pricing)
- [Anthropic Pricing](https://www.anthropic.com/pricing)
- [tiktoken Library](https://github.com/openai/tiktoken)
