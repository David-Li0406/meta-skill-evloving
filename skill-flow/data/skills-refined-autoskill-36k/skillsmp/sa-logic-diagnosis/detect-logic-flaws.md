# 逻辑漏洞排查指南 (Logic Flaw Detection Guide)

本指南用于系统性地定位和修复学术论文中的逻辑漏洞（Logic Flaws），类似于代码中的 Bug 定位。

## 核心理念：二分法定位 (Bisection)

当你的论证出现矛盾或被指出逻辑不通时，不要随意修补。使用二分法找到逻辑断裂的确切位置。

## 步骤 1：重现矛盾 (Reproduce the Contradiction)

明确“预期结论”与“实际推导”之间的冲突。

- **预期结论**：根据前提 A，应该得出结论 C。
- **实际情况**：审稿人指出反例 R，或者数据 D 不支持 C。

## 步骤 2：隔离范围 (Isolate the Scope)

将论证链条拆解为独立的部分。

1.  **检查前提 (Premises)**：
    - 前提 A 是否真的成立？
    - 引用文献是否支持前提 A？
2.  **检查中间推导 (Inference Steps)**：
    - 从 A 到 B 的推导是否严密？
    - 是否隐含了未声明的假设？
3.  **检查结论 (Conclusion)**：
    - 结论 C 是否过度概括 (Overclaiming)？

## 步骤 3：最小化验证 (Minimal Verification)

创建一个“最小论证单元”进行测试。

- 尝试用最简单的语言重述论证。
- 如果无法用一句话解释清楚，说明逻辑本身太复杂或混乱。
- 对每个关键术语进行定义检查 (Definition Check)。

## 常见逻辑污染源 (Common Logic Polluters)

- **概念漂移 (Concept Drift)**：在开头定义的术语，在后文中含义发生了微妙变化。
- **循环论证 (Circular Reasoning)**：结论被隐含在前提中。
- **以偏概全 (Hasty Generalization)**：从有限的样本得出普遍结论。
- **稻草人谬误 (Strawman)**：攻击了一个弱化版的反方观点，而非真正的挑战。

## 修复策略

一旦找到漏洞位置：
1.  **收缩主张**：将“总是”改为“在特定条件下”。
2.  **增强前提**：补充必要的背景或引用。
3.  **显式承认局限**：在 Discussion 中主动讨论反例，将其转化为 Future Work。
