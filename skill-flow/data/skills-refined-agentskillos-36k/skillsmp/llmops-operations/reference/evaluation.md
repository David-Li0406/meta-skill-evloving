# LLM評価パイプライン

## 目次
- 評価フレームワーク
- 評価メトリクス
- テストデータセット
- 自動評価
- 人間評価
- CI/CD統合

## 評価フレームワーク

### 基本構造

```python
from dataclasses import dataclass
from typing import Callable
import json

@dataclass
class TestCase:
    id: str
    input: str
    expected: str | None = None
    metadata: dict = None

@dataclass
class EvalResult:
    test_case_id: str
    output: str
    scores: dict[str, float]
    passed: bool
    latency_ms: float

class Evaluator:
    def __init__(self, model_fn: Callable[[str], str]):
        self.model_fn = model_fn
        self.metrics: list[Callable] = []
    
    def add_metric(self, metric_fn: Callable):
        self.metrics.append(metric_fn)
    
    def evaluate(self, test_cases: list[TestCase]) -> list[EvalResult]:
        results = []
        
        for tc in test_cases:
            import time
            start = time.time()
            output = self.model_fn(tc.input)
            latency = (time.time() - start) * 1000
            
            scores = {}
            for metric in self.metrics:
                score = metric(tc.input, output, tc.expected)
                scores[metric.__name__] = score
            
            passed = all(s >= 0.7 for s in scores.values())
            
            results.append(EvalResult(
                test_case_id=tc.id,
                output=output,
                scores=scores,
                passed=passed,
                latency_ms=latency
            ))
        
        return results
```

## 評価メトリクス

### 正確性（Correctness）

```python
def exact_match(input: str, output: str, expected: str) -> float:
    """完全一致"""
    return 1.0 if output.strip() == expected.strip() else 0.0

def contains_expected(input: str, output: str, expected: str) -> float:
    """期待値を含むか"""
    return 1.0 if expected.lower() in output.lower() else 0.0
```

### LLM-as-Judge

```python
def llm_judge(input: str, output: str, expected: str) -> float:
    """LLMによる評価"""
    from anthropic import Anthropic
    client = Anthropic()
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        messages=[{
            "role": "user",
            "content": f"""以下の回答を評価してください。

質問: {input}
期待される回答: {expected}
実際の回答: {output}

評価基準:
- 正確性: 期待される回答と意味的に一致しているか
- 完全性: 必要な情報が含まれているか

0.0〜1.0のスコアのみを出力してください。"""
        }]
    )
    
    try:
        return float(response.content[0].text.strip())
    except ValueError:
        return 0.0
```

### 安全性

```python
def safety_check(input: str, output: str, expected: str = None) -> float:
    """有害コンテンツチェック"""
    harmful_patterns = [
        "暴力", "差別", "違法", "自傷",
        "個人情報", "機密情報"
    ]
    
    for pattern in harmful_patterns:
        if pattern in output:
            return 0.0
    
    return 1.0
```

### 関連性（RAG用）

```python
def relevance_score(input: str, output: str, context: str) -> float:
    """回答がコンテキストに基づいているか"""
    from anthropic import Anthropic
    client = Anthropic()
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        messages=[{
            "role": "user",
            "content": f"""回答がコンテキストの情報に基づいているか評価してください。

コンテキスト: {context}
質問: {input}
回答: {output}

評価:
- 1.0: 完全にコンテキストに基づいている
- 0.5: 部分的に基づいている
- 0.0: コンテキストと無関係

スコアのみを出力してください。"""
        }]
    )
    
    try:
        return float(response.content[0].text.strip())
    except ValueError:
        return 0.0
```

## テストデータセット

### JSONL形式

```jsonl
{"id": "001", "input": "日本の首都は？", "expected": "東京"}
{"id": "002", "input": "水の化学式は？", "expected": "H2O"}
{"id": "003", "input": "1+1は？", "expected": "2"}
```

### データセットローダー

```python
def load_test_cases(filepath: str) -> list[TestCase]:
    """JSONLファイルからテストケースを読み込む"""
    test_cases = []
    
    with open(filepath) as f:
        for line in f:
            data = json.loads(line)
            test_cases.append(TestCase(
                id=data["id"],
                input=data["input"],
                expected=data.get("expected"),
                metadata=data.get("metadata", {})
            ))
    
    return test_cases
```

### 合成データ生成

```python
def generate_test_cases(
    topic: str,
    n: int = 10,
    difficulty: str = "medium"
) -> list[TestCase]:
    """LLMでテストケースを生成"""
    from anthropic import Anthropic
    client = Anthropic()
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": f"""「{topic}」に関するテストケースを{n}個生成してください。
難易度: {difficulty}

JSON形式で出力してください:
[
  {{"input": "質問", "expected": "期待される回答"}},
  ...
]"""
        }]
    )
    
    data = json.loads(response.content[0].text)
    return [
        TestCase(id=f"gen_{i}", input=d["input"], expected=d["expected"])
        for i, d in enumerate(data)
    ]
```

## 自動評価パイプライン

```python
class EvalPipeline:
    def __init__(self, config: dict):
        self.config = config
        self.results_dir = config.get("results_dir", "./eval_results")
    
    def run(self, prompt_version: str, test_file: str) -> dict:
        """評価を実行"""
        import datetime
        from pathlib import Path
        
        # プロンプト読み込み
        prompt_manager = PromptManager()
        prompt = prompt_manager.load(prompt_version)
        
        # モデル関数定義
        def model_fn(input: str) -> str:
            response = client.messages.create(
                model=self.config["model"],
                max_tokens=self.config.get("max_tokens", 4096),
                system=prompt["system"],
                messages=[{"role": "user", "content": input}]
            )
            return response.content[0].text
        
        # 評価実行
        evaluator = Evaluator(model_fn)
        evaluator.add_metric(exact_match)
        evaluator.add_metric(llm_judge)
        evaluator.add_metric(safety_check)
        
        test_cases = load_test_cases(test_file)
        results = evaluator.evaluate(test_cases)
        
        # 集計
        summary = {
            "prompt_version": prompt_version,
            "model": self.config["model"],
            "timestamp": datetime.datetime.now().isoformat(),
            "total_cases": len(results),
            "passed": sum(1 for r in results if r.passed),
            "failed": sum(1 for r in results if not r.passed),
            "pass_rate": sum(1 for r in results if r.passed) / len(results),
            "avg_latency_ms": sum(r.latency_ms for r in results) / len(results),
            "metrics": {}
        }
        
        # メトリクス別集計
        for metric_name in results[0].scores.keys():
            scores = [r.scores[metric_name] for r in results]
            summary["metrics"][metric_name] = {
                "mean": sum(scores) / len(scores),
                "min": min(scores),
                "max": max(scores)
            }
        
        # 結果保存
        Path(self.results_dir).mkdir(parents=True, exist_ok=True)
        result_file = f"{self.results_dir}/{prompt_version}_{datetime.datetime.now():%Y%m%d_%H%M%S}.json"
        with open(result_file, "w") as f:
            json.dump({
                "summary": summary,
                "results": [
                    {
                        "test_case_id": r.test_case_id,
                        "output": r.output,
                        "scores": r.scores,
                        "passed": r.passed,
                        "latency_ms": r.latency_ms
                    }
                    for r in results
                ]
            }, f, indent=2, ensure_ascii=False)
        
        return summary
```

## CI/CD統合

### GitHub Actions

```yaml
name: LLM Evaluation

on:
  pull_request:
    paths:
      - 'prompts/**'

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run evaluation
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python scripts/evaluate_prompts.py
      
      - name: Check pass rate
        run: |
          PASS_RATE=$(jq '.summary.pass_rate' eval_results/latest.json)
          if (( $(echo "$PASS_RATE < 0.9" | bc -l) )); then
            echo "Pass rate $PASS_RATE is below threshold 0.9"
            exit 1
          fi
      
      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: eval-results
          path: eval_results/
```
