# 学术逻辑诊断技能集设计日志 (Academic Logic Diagnosis Skillset Design Log)

**最后更新：** 2026-01-23
**目的：** 记录从通用逻辑诊断技术到学术论文写作场景的迁移与适配过程。

## 设计理念 (Design Philosophy)

本技能集旨在将软件工程中成熟的“调试 (Debugging)”和“系统安全 (System Security)”思想，迁移并适配到学术研究领域。学术论文的逻辑构建与复杂软件系统的构建有异曲同工之妙：都需要严密的逻辑链、对异常情况（反例）的处理以及多层次的稳健性设计。

## 核心概念映射 (Concept Mapping)

我们将三个核心工程概念映射为学术写作技能：

| 原工程概念 | 学术适配概念 | 核心价值 |
| :--- | :--- | :--- |
| **Root Cause Analysis**<br>(根因分析) | **[研究问题的根源剖析](research-root-analysis.md)**<br>(Research Problem Root Analysis) | 解决论文“逻辑不连贯”的问题。不仅仅修补结论的措辞，而是追溯到理论假设和文献基础的源头错误。 |
| **Defense in Depth**<br>(纵深防御) | **[论证的多层次校验](multi-layered-verification.md)**<br>(Multi-layered Argument Verification) | 解决论文“易被攻击”的问题。在理论、方法、边界和反思四个层面建立防线，预判并抵御审稿人的质疑。 |
| **Race Condition / Async**<br>(竞态条件/异步等待) | **[基于证据的审慎推论](evidence-based-inference.md)**<br>(Evidence-based Cautious Inference) | 解决论文“过度概括”的问题。像等待异步数据返回一样，强制论点等待充分的证据支持，避免仓促下结论。 |

## 修订记录与决策 (Revision Log & Decisions)

### 阶段 1：学术化术语替换
- **决策：** 将所有工程隐喻（如“Bug”、“补丁”、“系统崩溃”）替换为学术界通用术语（如“逻辑谬误”、“修正”、“拒稿”）。
- **理由：** 降低认知摩擦，使研究人员能立即将技能应用于写作流程，无需进行心理转译。

### 阶段 2：引入“同行评审”视角
- **新增：** 在 `multi-layered-verification.md` 中引入了“审稿人视角”，模拟常见的审稿意见（如“样本量不足”、“因果关系不清”）。
- **目的：** 增强技能的实战性，直接对接学术发表的需求。

### 阶段 3：强化“限定词 (Hedging)”策略
- **新增：** 在 `evidence-based-inference.md` 中增加了具体的词汇表（Demonstrate vs. Suggest）。
- **理由：** 学术写作的精确性往往体现在对确定性程度的把控上，这是新手作者最容易犯错的地方。

## 如何使用本技能集 (How to Use)

这套技能构成了一个完整的逻辑质量保障闭环：

1.  **诊断 (Diagnosis)：** 当你感觉论证无力或收到负面反馈时，使用 **[研究问题的根源剖析](research-root-analysis.md)** 找到问题的根源（是假设错了，还是引用错了？）。
2.  **修复 (Fix)：** 在源头修正错误后，使用 **[基于证据的审慎推论](evidence-based-inference.md)** 重新撰写结论，确保论点不过度延伸。
3.  **加固 (Fortification)：** 最后，使用 **[论证的多层次校验](multi-layered-verification.md)** 在整篇论文中植入防御性论述，确保逻辑链无懈可击。

---

*本日志用于追踪技能集的设计意图与演变，确保后续维护者理解每个文件的定位。*
