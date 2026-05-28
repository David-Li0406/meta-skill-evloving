# 思维链提示

## 概述

思维链（CoT）提示从LLM中引发逐步推理，显著提高在复杂推理、数学和逻辑任务上的性能。

## 核心技术

### 零样本CoT
添加简单的触发短语来引发推理：

```python
def zero_shot_cot(query):
    return f"""{query}

让我们一步步思考："""

# 示例
query = "如果一列火车以60英里/小时的速度行驶2.5小时，它能走多远？"
prompt = zero_shot_cot(query)

# 模型输出：
# "让我们一步步思考：
# 1. 速度 = 60英里/小时
# 2. 时间 = 2.5小时
# 3. 距离 = 速度 × 时间
# 4. 距离 = 60 × 2.5 = 150英里
# 答案：150英里"
```

### 少样本CoT
提供带有明确推理链的示例：

```python
few_shot_examples = """
问：罗杰有5个网球。他又买了2罐网球。每罐有3个球。他现在有多少个网球？
答：让我们一步步思考：
1. 罗杰开始时有5个球
2. 他买了2罐，每罐有3个球
3. 罐中的球：2 × 3 = 6个球
4. 总计：5 + 6 = 11个球
答案：11

问：食堂有23个苹果。如果他们用20个做午餐，又买了6个，他们现在有多少个？
答：让我们一步步思考：
1. 开始时有23个苹果
2. 用于午餐：23 - 20 = 3个苹果剩余
3. 买了6个：3 + 6 = 9个苹果
答案：9

问：{user_query}
答：让我们一步步思考："""
```

### 自一致性
生成多个推理路径并采取多数投票：

```python
import openai
from collections import Counter

def self_consistency_cot(query, n=5, temperature=0.7):
    prompt = f"{query}\n\n让我们一步步思考："

    responses = []
    for _ in range(n):
        response = openai.ChatCompletion.create(
            model="gpt-5",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        responses.append(extract_final_answer(response))

    # 采取多数投票
    answer_counts = Counter(responses)
    final_answer = answer_counts.most_common(1)[0][0]

    return {
        'answer': final_answer,
        'confidence': answer_counts[final_answer] / n,
        'all_responses': responses
    }
```

## 高级模式

### 从少到多提示
将复杂问题分解为更简单的子问题：

```python
def least_to_most_prompt(complex_query):
    # 阶段1：分解
    decomp_prompt = f"""将这个复杂问题分解为更简单的子问题：

问题：{complex_query}

子问题："""

    subproblems = get_llm_response(decomp_prompt)

    # 阶段2：顺序解决
    solutions = []
    context = ""

    for subproblem in subproblems:
        solve_prompt = f"""{context}

解决这个子问题：
{subproblem}

解决方案："""
        solution = get_llm_response(solve_prompt)
        solutions.append(solution)
        context += f"\n\n已解决：{subproblem}\n解决方案：{solution}"

    # 阶段3：最终整合
    final_prompt = f"""基于这些子问题的解决方案：
{context}

提供最终答案：{complex_query}

最终答案："""

    return get_llm_response(final_prompt)
```

### 思维树（ToT）
探索多个推理分支：

```python
class TreeOfThought:
    def __init__(self, llm_client, max_depth=3, branches_per_step=3):
        self.client = llm_client
        self.max_depth = max_depth
        self.branches_per_step = branches_per_step

    def solve(self, problem):
        # 生成初始思维分支
        initial_thoughts = self.generate_thoughts(problem, depth=0)

        # 评估每个分支
        best_path = None
        best_score = -1

        for thought in initial_thoughts:
            path, score = self.explore_branch(problem, thought, depth=1)
            if score > best_score:
                best_score = score
                best_path = path

        return best_path

    def generate_thoughts(self, problem, context="", depth=0):
        prompt = f"""问题：{problem}
{context}

生成{self.branches_per_step}个解决此问题的不同下一步：

1."""
        response = self.client.complete(prompt)
        return self.parse_thoughts(response)

    def evaluate_thought(self, problem, thought_path):
        prompt = f"""问题：{problem}

到目前为止的推理路径：
{thought_path}

从0-10分评估此推理路径的：
- 正确性
- 达到解决方案的可能性
- 逻辑一致性

分数："""
        return float(self.client.complete(prompt))
```

### 验证步骤
添加显式验证以捕获错误：

```python
def cot_with_verification(query):
    # 步骤1：生成推理和答案
    reasoning_prompt = f"""{query}

让我们一步步解决这个问题："""

    reasoning_response = get_llm_response(reasoning_prompt)

    # 步骤2：验证推理
    verification_prompt = f"""原始问题：{query}

提出的解决方案：
{reasoning_response}

通过以下方式验证此解决方案：
1. 检查每个步骤的逻辑错误
2. 验证算术计算
3. 确保最终答案合理

此解决方案是否正确？如果不正确，有什么问题？

验证："""

    verification = get_llm_response(verification_prompt)

    # 步骤3：如需要则修改
    if "incorrect" in verification.lower() or "error" in verification.lower():
        revision_prompt = f"""之前的解决方案有错误：
{verification}

请提供修正后的解决方案：{query}

修正后的解决方案："""
        return get_llm_response(revision_prompt)

    return reasoning_response
```

## 特定领域CoT

### 数学问题
```python
math_cot_template = """
问题：{problem}

解决方案：
步骤1：识别我们已知的内容
- {list_known_values}

步骤2：识别我们需要找到的内容
- {target_variable}

步骤3：选择相关公式
- {formulas}

步骤4：代入值
- {substitution}

步骤5：计算
- {calculation}

步骤6：验证并说明答案
- {verification}

答案：{final_answer}
"""
```

### 代码调试
```python
debug_cot_template = """
有错误的代码：
{code}

错误信息：
{error}

调试过程：
步骤1：理解错误信息
- {interpret_error}

步骤2：定位有问题的行
- {identify_line}

步骤3：分析此行失败的原因
- {root_cause}

步骤4：确定修复方案
- {proposed_fix}

步骤5：验证修复是否解决错误
- {verification}

修复后的代码：
{corrected_code}
"""
```

### 逻辑推理
```python
logic_cot_template = """
前提：
{premises}

问题：{question}

推理：
步骤1：列出所有给定事实
{facts}

步骤2：识别逻辑关系
{relationships}

步骤3：应用演绎推理
{deductions}

步骤4：得出结论
{conclusion}

答案：{final_answer}
"""
```

## 性能优化

### 缓存推理模式
```python
class ReasoningCache:
    def __init__(self):
        self.cache = {}

    def get_similar_reasoning(self, problem, threshold=0.85):
        problem_embedding = embed(problem)

        for cached_problem, reasoning in self.cache.items():
            similarity = cosine_similarity(
                problem_embedding,
                embed(cached_problem)
            )
            if similarity > threshold:
                return reasoning

        return None

    def add_reasoning(self, problem, reasoning):
        self.cache[problem] = reasoning
```

### 自适应推理深度
```python
def adaptive_cot(problem, initial_depth=3):
    depth = initial_depth

    while depth <= 10:  # 最大深度
        response = generate_cot(problem, num_steps=depth)

        # 检查解决方案是否看似完整
        if is_solution_complete(response):
            return response

        depth += 2  # 增加推理深度

    return response  # 返回最佳尝试
```

## 评估指标

```python
def evaluate_cot_quality(reasoning_chain):
    metrics = {
        'coherence': measure_logical_coherence(reasoning_chain),
        'completeness': check_all_steps_present(reasoning_chain),
        'correctness': verify_final_answer(reasoning_chain),
        'efficiency': count_unnecessary_steps(reasoning_chain),
        'clarity': rate_explanation_clarity(reasoning_chain)
    }
    return metrics
```

## 最佳实践

1. **清晰的步骤标记**：使用编号步骤或清晰的分隔符
2. **显示所有工作**：不要跳过步骤，即使是显而易见的
3. **验证计算**：添加显式验证步骤
4. **说明假设**：使隐含假设变为显式
5. **检查边界情况**：考虑边界条件
6. **使用示例**：首先用示例展示推理模式

## 常见陷阱

- **过早结论**：没有完整推理就跳到答案
- **循环逻辑**：用结论来证明推理
- **遗漏步骤**：跳过中间计算
- **过度复杂**：添加令人困惑的不必要步骤
- **格式不一致**：推理过程中改变步骤结构

## 何时使用CoT

**使用CoT用于：**
- 数学和算术问题
- 逻辑推理任务
- 多步骤规划
- 代码生成和调试
- 复杂决策制定

**跳过CoT用于：**
- 简单事实查询
- 直接查找
- 创意写作
- 需要简洁的任务
- 实时、延迟敏感的应用

## 资源

- 用于CoT评估的基准数据集
- 预构建的CoT提示模板
- 推理验证工具
- 步骤提取和解析实用程序