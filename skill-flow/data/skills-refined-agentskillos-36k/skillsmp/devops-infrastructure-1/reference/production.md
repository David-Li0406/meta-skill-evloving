# LLM本番運用ガイド

## 目次
- アーキテクチャパターン
- エラーハンドリング
- レート制限対策
- コスト管理
- モニタリング
- ガードレール

## アーキテクチャパターン

### 本番向け基本構成

```python
import asyncio
from anthropic import Anthropic, AsyncAnthropic
from tenacity import retry, stop_after_attempt, wait_exponential
import structlog

logger = structlog.get_logger()

class LLMService:
    def __init__(self):
        self.client = Anthropic()
        self.async_client = AsyncAnthropic()
        self.model = "claude-sonnet-4-20250514"
        self.fallback_model = "claude-haiku-4-5-20251001"
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    def chat(
        self,
        messages: list[dict],
        system: str = None,
        max_tokens: int = 4096
    ) -> str:
        """同期呼び出し（リトライ付き）"""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system,
                messages=messages
            )
            
            logger.info(
                "llm_request_success",
                model=self.model,
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens
            )
            
            return response.content[0].text
            
        except Exception as e:
            logger.error("llm_request_failed", error=str(e))
            raise
    
    async def chat_async(
        self,
        messages: list[dict],
        system: str = None,
        max_tokens: int = 4096
    ) -> str:
        """非同期呼び出し"""
        response = await self.async_client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=messages
        )
        return response.content[0].text
    
    def chat_with_fallback(
        self,
        messages: list[dict],
        system: str = None
    ) -> str:
        """フォールバック付き呼び出し"""
        try:
            return self.chat(messages, system)
        except Exception as e:
            logger.warning(
                "falling_back_to_haiku",
                primary_error=str(e)
            )
            response = self.client.messages.create(
                model=self.fallback_model,
                max_tokens=4096,
                system=system,
                messages=messages
            )
            return response.content[0].text
```

### ストリーミング

```python
def chat_stream(self, messages: list[dict], system: str = None):
    """ストリーミングレスポンス"""
    with self.client.messages.stream(
        model=self.model,
        max_tokens=4096,
        system=system,
        messages=messages
    ) as stream:
        for text in stream.text_stream:
            yield text
```

## エラーハンドリング

```python
from anthropic import (
    APIConnectionError,
    RateLimitError,
    APIStatusError
)

def handle_llm_error(func):
    """エラーハンドリングデコレータ"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        
        except RateLimitError as e:
            logger.warning("rate_limit_hit", retry_after=e.response.headers.get("retry-after"))
            # レート制限時は待機してリトライ
            time.sleep(60)
            return func(*args, **kwargs)
        
        except APIConnectionError as e:
            logger.error("api_connection_error", error=str(e))
            raise ServiceUnavailableError("LLMサービスに接続できません")
        
        except APIStatusError as e:
            if e.status_code == 529:  # Overloaded
                logger.warning("api_overloaded")
                time.sleep(30)
                return func(*args, **kwargs)
            raise
        
        except Exception as e:
            logger.error("unexpected_error", error=str(e), exc_info=True)
            raise
    
    return wrapper
```

## レート制限対策

### トークンバケット

```python
import time
from threading import Lock

class TokenBucket:
    def __init__(self, tokens_per_minute: int):
        self.capacity = tokens_per_minute
        self.tokens = tokens_per_minute
        self.last_refill = time.time()
        self.lock = Lock()
    
    def acquire(self, tokens: int) -> bool:
        """トークンを取得（取得できない場合は待機）"""
        with self.lock:
            self._refill()
            
            if tokens <= self.tokens:
                self.tokens -= tokens
                return True
            
            # 待機時間計算
            tokens_needed = tokens - self.tokens
            wait_time = tokens_needed / (self.capacity / 60)
            time.sleep(wait_time)
            
            self._refill()
            self.tokens -= tokens
            return True
    
    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        refill = elapsed * (self.capacity / 60)
        self.tokens = min(self.capacity, self.tokens + refill)
        self.last_refill = now

# 使用例
bucket = TokenBucket(tokens_per_minute=40000)

def rate_limited_call(messages, estimated_tokens):
    bucket.acquire(estimated_tokens)
    return client.messages.create(...)
```

### バッチ処理

```python
import asyncio
from asyncio import Semaphore

async def batch_process(
    items: list,
    process_fn,
    max_concurrent: int = 5
) -> list:
    """並行数を制限したバッチ処理"""
    semaphore = Semaphore(max_concurrent)
    
    async def process_with_limit(item):
        async with semaphore:
            return await process_fn(item)
    
    tasks = [process_with_limit(item) for item in items]
    return await asyncio.gather(*tasks)
```

## コスト管理

### トークンカウント

```python
import anthropic

def estimate_tokens(text: str) -> int:
    """トークン数を推定"""
    client = anthropic.Anthropic()
    return client.count_tokens(text)

def calculate_cost(
    input_tokens: int,
    output_tokens: int,
    model: str = "claude-sonnet-4-20250514"
) -> float:
    """コスト計算（USD）"""
    pricing = {
        "claude-opus-4-5-20251101": {"input": 15.0, "output": 75.0},
        "claude-sonnet-4-20250514": {"input": 3.0, "output": 15.0},
        "claude-haiku-4-5-20251001": {"input": 0.80, "output": 4.0},
    }
    
    rates = pricing.get(model, pricing["claude-sonnet-4-20250514"])
    
    input_cost = (input_tokens / 1_000_000) * rates["input"]
    output_cost = (output_tokens / 1_000_000) * rates["output"]
    
    return input_cost + output_cost
```

### コスト監視

```python
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class UsageRecord:
    timestamp: datetime
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    request_id: str

class CostTracker:
    def __init__(self, daily_limit_usd: float = 100.0):
        self.daily_limit = daily_limit_usd
        self.records: list[UsageRecord] = []
    
    def record(self, response, request_id: str):
        """使用量を記録"""
        cost = calculate_cost(
            response.usage.input_tokens,
            response.usage.output_tokens,
            response.model
        )
        
        record = UsageRecord(
            timestamp=datetime.now(),
            model=response.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            cost_usd=cost,
            request_id=request_id
        )
        
        self.records.append(record)
        
        # 日次制限チェック
        daily_cost = self.get_daily_cost()
        if daily_cost > self.daily_limit:
            logger.warning(
                "daily_cost_limit_exceeded",
                daily_cost=daily_cost,
                limit=self.daily_limit
            )
    
    def get_daily_cost(self) -> float:
        today = datetime.now().date()
        return sum(
            r.cost_usd for r in self.records
            if r.timestamp.date() == today
        )
```

## モニタリング

### Prometheusメトリクス

```python
from prometheus_client import Counter, Histogram, Gauge

# メトリクス定義
llm_requests_total = Counter(
    "llm_requests_total",
    "Total LLM API requests",
    ["model", "status"]
)

llm_request_duration = Histogram(
    "llm_request_duration_seconds",
    "LLM request duration",
    ["model"],
    buckets=[0.5, 1, 2, 5, 10, 30, 60]
)

llm_tokens_used = Counter(
    "llm_tokens_used_total",
    "Total tokens used",
    ["model", "type"]  # type: input/output
)

llm_cost_usd = Counter(
    "llm_cost_usd_total",
    "Total cost in USD",
    ["model"]
)

# 使用
def instrumented_call(messages, system):
    import time
    
    start = time.time()
    try:
        response = client.messages.create(...)
        
        duration = time.time() - start
        llm_request_duration.labels(model=response.model).observe(duration)
        llm_requests_total.labels(model=response.model, status="success").inc()
        llm_tokens_used.labels(model=response.model, type="input").inc(response.usage.input_tokens)
        llm_tokens_used.labels(model=response.model, type="output").inc(response.usage.output_tokens)
        
        return response
        
    except Exception as e:
        llm_requests_total.labels(model="unknown", status="error").inc()
        raise
```

## ガードレール

### 入力バリデーション

```python
def validate_input(text: str) -> tuple[bool, str]:
    """入力テキストの検証"""
    # 長さチェック
    if len(text) > 100000:
        return False, "入力が長すぎます"
    
    # 空チェック
    if not text.strip():
        return False, "入力が空です"
    
    # 禁止パターン
    forbidden = ["ignore previous instructions", "system prompt"]
    for pattern in forbidden:
        if pattern.lower() in text.lower():
            return False, "禁止パターンが含まれています"
    
    return True, ""
```

### 出力フィルタリング

```python
def filter_output(text: str) -> str:
    """出力のフィルタリング"""
    import re
    
    # PII除去（簡易版）
    patterns = [
        (r"\b\d{3}-\d{4}-\d{4}\b", "[電話番号]"),  # 電話番号
        (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[メール]"),  # メール
    ]
    
    filtered = text
    for pattern, replacement in patterns:
        filtered = re.sub(pattern, replacement, filtered)
    
    return filtered
```

### コンテンツモデレーション

```python
async def moderate_content(text: str) -> dict:
    """コンテンツモデレーション"""
    response = await client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[{
            "role": "user",
            "content": f"""以下のテキストを分析し、問題があるか判定してください。

テキスト: {text[:1000]}

JSON形式で回答:
{{"safe": true/false, "reason": "理由", "category": "カテゴリ"}}"""
        }]
    )
    
    return json.loads(response.content[0].text)
```
