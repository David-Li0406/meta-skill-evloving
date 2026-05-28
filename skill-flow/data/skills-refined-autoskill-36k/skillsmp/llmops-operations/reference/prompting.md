# プロンプトエンジニアリング

## 目次
- プロンプト構造
- プロンプトテクニック
- バージョン管理
- テンプレート管理
- アンチパターン

## プロンプト構造

### 基本テンプレート

```xml
<system>
あなたは{role}です。

## 制約
- {constraint_1}
- {constraint_2}

## 出力形式
{output_format}
</system>

<user>
{user_input}
</user>
```

### 構造化プロンプト

```python
SYSTEM_PROMPT = """あなたは技術文書のレビューアシスタントです。

## タスク
与えられた文書をレビューし、改善点を指摘してください。

## レビュー観点
1. 技術的正確性
2. 可読性・明確性
3. 一貫性
4. 完全性

## 出力形式
各観点について以下の形式で出力してください：

### [観点名]
- 評価: [良好/要改善/問題あり]
- コメント: [具体的な指摘]
- 提案: [改善案（あれば）]
"""
```

## プロンプトテクニック

### Few-shot プロンプティング

```python
def build_few_shot_prompt(examples: list[dict], query: str) -> str:
    prompt = "以下の例を参考に、タスクを実行してください。\n\n"
    
    for i, ex in enumerate(examples, 1):
        prompt += f"例{i}:\n"
        prompt += f"入力: {ex['input']}\n"
        prompt += f"出力: {ex['output']}\n\n"
    
    prompt += f"タスク:\n入力: {query}\n出力:"
    return prompt
```

### Chain of Thought

```python
COT_PROMPT = """問題を解く前に、step by stepで考えてください。

<thinking>
ここで思考プロセスを記述
</thinking>

<answer>
最終的な回答
</answer>
"""
```

### Self-consistency

```python
import asyncio
from collections import Counter

async def self_consistency(prompt: str, n: int = 5) -> str:
    """複数回生成して最も一貫性のある回答を選択"""
    tasks = [generate_async(prompt, temperature=0.7) for _ in range(n)]
    responses = await asyncio.gather(*tasks)
    
    # 回答を正規化して集計
    normalized = [normalize_answer(r) for r in responses]
    most_common = Counter(normalized).most_common(1)[0][0]
    
    return most_common
```

### Tool Use

```python
tools = [
    {
        "name": "search_database",
        "description": "データベースを検索して情報を取得します",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "検索クエリ"
                },
                "limit": {
                    "type": "integer",
                    "description": "取得件数上限",
                    "default": 10
                }
            },
            "required": ["query"]
        }
    }
]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    tools=tools,
    messages=[{"role": "user", "content": "最新の売上データを教えて"}]
)
```

## バージョン管理

### プロンプトファイル構造

```
prompts/
├── v1/
│   ├── system.txt
│   └── metadata.yaml
├── v2/
│   ├── system.txt
│   └── metadata.yaml
└── current -> v2/
```

### metadata.yaml

```yaml
version: "2.0"
created_at: "2025-01-15"
author: "ooyama"
description: "レビュー精度向上のため、観点を細分化"
model: "claude-sonnet-4-20250514"
temperature: 0.3
max_tokens: 4096

evaluation:
  dataset: "test_cases_v2.jsonl"
  metrics:
    accuracy: 0.92
    latency_p95_ms: 1500

changes:
  - "レビュー観点を4→6に細分化"
  - "出力形式をJSON化"
```

### プロンプトローダー

```python
from pathlib import Path
import yaml

class PromptManager:
    def __init__(self, base_dir: str = "prompts"):
        self.base_dir = Path(base_dir)
    
    def load(self, version: str = "current") -> dict:
        prompt_dir = self.base_dir / version
        if prompt_dir.is_symlink():
            prompt_dir = prompt_dir.resolve()
        
        with open(prompt_dir / "system.txt") as f:
            system = f.read()
        
        with open(prompt_dir / "metadata.yaml") as f:
            metadata = yaml.safe_load(f)
        
        return {
            "system": system,
            "metadata": metadata
        }
    
    def list_versions(self) -> list[str]:
        return [
            d.name for d in self.base_dir.iterdir()
            if d.is_dir() and not d.is_symlink()
        ]
```

## テンプレート管理

### Jinja2テンプレート

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("prompts/templates"))

def render_prompt(template_name: str, **kwargs) -> str:
    template = env.get_template(template_name)
    return template.render(**kwargs)

# 使用例
prompt = render_prompt(
    "review.j2",
    document_type="API仕様書",
    focus_areas=["セキュリティ", "パフォーマンス"],
    max_issues=10
)
```

### テンプレート例（review.j2）

```jinja2
あなたは{{ document_type }}のレビュー専門家です。

## 重点レビュー領域
{% for area in focus_areas %}
- {{ area }}
{% endfor %}

## 制約
- 指摘は最大{{ max_issues }}件まで
- 各指摘には改善案を含めること

## 出力形式
JSON形式で出力してください：
{
  "issues": [
    {
      "severity": "high|medium|low",
      "location": "該当箇所",
      "description": "問題の説明",
      "suggestion": "改善案"
    }
  ]
}
```

## アンチパターン

### 避けるべきパターン

```python
# ❌ 曖昧な指示
"良いレビューをしてください"

# ✅ 具体的な指示
"以下の観点でレビューし、各観点について1-3個の改善点を指摘してください：
1. コードの可読性
2. エラーハンドリング
3. パフォーマンス"
```

```python
# ❌ 過度に長いプロンプト（トークン浪費）
"あなたは非常に優秀で経験豊富なソフトウェアエンジニアで..."

# ✅ 簡潔で効果的
"あなたはシニアソフトウェアエンジニアです。"
```

```python
# ❌ ハードコードされたプロンプト
response = client.messages.create(
    system="あなたは..."  # コード内に直接記述
)

# ✅ 外部ファイルで管理
prompt_manager = PromptManager()
prompt = prompt_manager.load("current")
response = client.messages.create(system=prompt["system"])
```
