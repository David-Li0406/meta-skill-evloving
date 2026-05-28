# 小样本学习指南

## 概述

小样本学习使LLM能够通过在提示中提供少量示例（通常1-10个）来执行任务。这种技术在需要特定格式、风格或领域知识的任务中非常有效。

## 示例选择策略

### 1. 语义相似性
使用基于嵌入的检索选择与输入查询最相似的示例。

```python
from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticExampleSelector:
    def __init__(self, examples, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.examples = examples
        self.example_embeddings = self.model.encode([ex['input'] for ex in examples])

    def select(self, query, k=3):
        query_embedding = self.model.encode([query])
        similarities = np.dot(self.example_embeddings, query_embedding.T).flatten()
        top_indices = np.argsort(similarities)[-k:][::-1]
        return [self.examples[i] for i in top_indices]
```

**最适用于**：问答、文本分类、提取任务

### 2. 多样性采样
最大化不同模式和边界情况的覆盖范围。

```python
from sklearn.cluster import KMeans

class DiversityExampleSelector:
    def __init__(self, examples, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.examples = examples
        self.embeddings = self.model.encode([ex['input'] for ex in examples])

    def select(self, k=5):
        # 使用k-means找到多样化的簇中心
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(self.embeddings)

        # 选择每个簇中心最近的示例
        diverse_examples = []
        for center in kmeans.cluster_centers_:
            distances = np.linalg.norm(self.embeddings - center, axis=1)
            closest_idx = np.argmin(distances)
            diverse_examples.append(self.examples[closest_idx])

        return diverse_examples
```

**最适用于**：演示任务可变性、边界情况处理

### 3. 基于难度选择
逐步增加示例复杂性以搭建学习支架。

```python
class ProgressiveExampleSelector:
    def __init__(self, examples):
        # 示例应该有'difficulty'分数（0-1）
        self.examples = sorted(examples, key=lambda x: x['difficulty'])

    def select(self, k=3):
        # 选择线性递增难度的示例
        step = len(self.examples) // k
        return [self.examples[i * step] for i in range(k)]
```

**最适用于**：复杂推理任务、代码生成

### 4. 基于错误选择
包含处理常见失败模式的示例。

```python
class ErrorGuidedSelector:
    def __init__(self, examples, error_patterns):
        self.examples = examples
        self.error_patterns = error_patterns  # 要避免的常见错误

    def select(self, query, k=3):
        # 选择演示正确处理错误模式的示例
        selected = []
        for pattern in self.error_patterns[:k]:
            matching = [ex for ex in self.examples if pattern in ex['demonstrates']]
            if matching:
                selected.append(matching[0])
        return selected
```

**最适用于**：具有已知失败模式的任务、安全关键应用

## 示例构建最佳实践

### 格式一致性
所有示例应遵循相同的格式：

```python
# 好：一致格式
examples = [
    {
        "input": "法国的首都是什么？",
        "output": "巴黎"
    },
    {
        "input": "德国的首都是什么？",
        "output": "柏林"
    }
]

# 差：不一致格式
examples = [
    "问：法国的首都是什么？答：巴黎",
    {"question": "德国的首都是什么？", "answer": "柏林"}
]
```

### 输入输出对齐
确保示例演示你希望模型执行的确切任务：

```python
# 好：清晰的输入输出关系
example = {
    "input": "情感：这部电影很糟糕而且无聊。",
    "output": "负面"
}

# 差：模糊关系
example = {
    "input": "这部电影很糟糕而且无聊。",
    "output": "这篇评论表达了对电影的负面情感。"
}
```

### 复杂性平衡
包含涵盖预期难度范围的示例：

```python
examples = [
    # 简单情况
    {"input": "2 + 2", "output": "4"},

    # 中等情况
    {"input": "15 * 3 + 8", "output": "53"},

    # 复杂情况
    {"input": "(12 + 8) * 3 - 15 / 5", "output": "57"}
]
```

## 上下文窗口管理

### Token预算分配
4K上下文窗口的典型分布：

```
系统提示：        500 tokens  (12%)
小样本示例：     1500 tokens  (38%)
用户输入：        500 tokens  (12%)
响应：           1500 tokens  (38%)
```

### 动态示例截断
```python
class TokenAwareSelector:
    def __init__(self, examples, tokenizer, max_tokens=1500):
        self.examples = examples
        self.tokenizer = tokenizer
        self.max_tokens = max_tokens

    def select(self, query, k=5):
        selected = []
        total_tokens = 0

        # 从最相关的示例开始
        candidates = self.rank_by_relevance(query)

        for example in candidates[:k]:
            example_tokens = len(self.tokenizer.encode(
                f"输入：{example['input']}\n输出：{example['output']}\n\n"
            ))

            if total_tokens + example_tokens <= self.max_tokens:
                selected.append(example)
                total_tokens += example_tokens
            else:
                break

        return selected
```

## 边界情况处理

### 包含边界示例
```python
edge_case_examples = [
    # 空输入
    {"input": "", "output": "请提供输入文本。"},

    # 非常长的输入（在示例中截断）
    {"input": "..." + "word " * 1000, "output": "输入超过最大长度。"},

    # 模糊输入
    {"input": "bank", "output": "模糊：可能指金融机构或河岸。"},

    # 无效输入
    {"input": "!@#$%", "output": "无效输入格式。请提供有效文本。"}
]
```

## 小样本提示模板

### 分类模板
```python
def build_classification_prompt(examples, query, labels):
    prompt = f"将文本分类到以下类别之一：{', '.join(labels)}\n\n"

    for ex in examples:
        prompt += f"文本：{ex['input']}\n类别：{ex['output']}\n\n"

    prompt += f"文本：{query}\n类别："
    return prompt
```

### 提取模板
```python
def build_extraction_prompt(examples, query):
    prompt = "从文本中提取结构化信息。\n\n"

    for ex in examples:
        prompt += f"文本：{ex['input']}\n提取的：{json.dumps(ex['output'])}\n\n"

    prompt += f"文本：{query}\n提取的："
    return prompt
```

### 转换模板
```python
def build_transformation_prompt(examples, query):
    prompt = "按照示例中显示的模式转换输入。\n\n"

    for ex in examples:
        prompt += f"输入：{ex['input']}\n输出：{ex['output']}\n\n"

    prompt += f"输入：{query}\n输出："
    return prompt
```

## 评估和优化

### 示例质量指标
```python
def evaluate_example_quality(example, validation_set):
    metrics = {
        'clarity': rate_clarity(example),  # 0-1分数
        'representativeness': calculate_similarity_to_validation(example, validation_set),
        'difficulty': estimate_difficulty(example),
        'uniqueness': calculate_uniqueness(example, other_examples)
    }
    return metrics
```

### A/B测试示例集
```python
class ExampleSetTester:
    def __init__(self, llm_client):
        self.client = llm_client

    def compare_example_sets(self, set_a, set_b, test_queries):
        results_a = self.evaluate_set(set_a, test_queries)
        results_b = self.evaluate_set(set_b, test_queries)

        return {
            'set_a_accuracy': results_a['accuracy'],
            'set_b_accuracy': results_b['accuracy'],
            'winner': 'A' if results_a['accuracy'] > results_b['accuracy'] else 'B',
            'improvement': abs(results_a['accuracy'] - results_b['accuracy'])
        }

    def evaluate_set(self, examples, test_queries):
        correct = 0
        for query in test_queries:
            prompt = build_prompt(examples, query['input'])
            response = self.client.complete(prompt)
            if response == query['expected_output']:
                correct += 1
        return {'accuracy': correct / len(test_queries)}
```

## 高级技术

### 元学习（学习选择）
训练一个小模型来预测哪些示例最有效：

```python
from sklearn.ensemble import RandomForestClassifier

class LearnedExampleSelector:
    def __init__(self):
        self.selector_model = RandomForestClassifier()

    def train(self, training_data):
        # training_data: (查询, 示例, 成功)元组列表
        features = []
        labels = []

        for query, example, success in training_data:
            features.append(self.extract_features(query, example))
            labels.append(1 if success else 0)

        self.selector_model.fit(features, labels)

    def extract_features(self, query, example):
        return [
            semantic_similarity(query, example['input']),
            len(example['input']),
            len(example['output']),
            keyword_overlap(query, example['input'])
        ]

    def select(self, query, candidates, k=3):
        scores = []
        for example in candidates:
            features = self.extract_features(query, example)
            score = self.selector_model.predict_proba([features])[0][1]
            scores.append((score, example))

        return [ex for _, ex in sorted(scores, reverse=True)[:k]]
```

### 自适应示例数量
根据任务难度动态调整示例数量：

```python
class AdaptiveExampleSelector:
    def __init__(self, examples):
        self.examples = examples

    def select(self, query, max_examples=5):
        # 从1个示例开始
        for k in range(1, max_examples + 1):
            selected = self.get_top_k(query, k)

            # 快速置信度检查（可以使用轻量级模型）
            if self.estimated_confidence(query, selected) > 0.9:
                return selected

        return selected  # 如果始终不够自信则返回max_examples
```

## 常见错误

1. **示例过多**：更多不总是更好；可能会稀释焦点
2. **不相关示例**：示例应与目标任务紧密匹配
3. **格式不一致**：使模型对输出格式感到困惑
4. **过度拟合示例**：模型过于字面地复制示例模式
5. **忽略Token限制**：为实际输入/输出耗尽空间

## 资源

- 示例数据集仓库
- 常见任务的预构建示例选择器
- 小样本性能评估框架
- 不同模型的token计数实用程序