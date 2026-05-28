# 复审工作流（draft-plan-review）

## 0) 定位与读取（最小化）

1) 确认项目根目录
   - 默认项目根目录=你当前会话所在目录；如果不确定，必须先 AskUserQuestion 让用户确认

2) 定位草案文件
   - 目标文件：`Record/plan/draft-plan.md`
   - 如果不存在：AskUserQuestion 让用户给出正确路径，或让用户先让 plan-agent 生成该文件

3) 最小读取策略（避免上下文爆炸）
   - 先定位关键段落（例如：需求摘要、环境检查、子代理需求、scope 轮廓、用户确认选项）
   - 只读取与复审相关的段落；不要整文件全量灌入

## 1) 先问清楚（AskUserQuestion）

当以下信息缺失或含糊时，必须先问用户再进入分析与回写：
- 需求的关键目标/非目标（避免跑题）
- 目标交付形态（输出是什么：库/服务/脚本/文档等）
- 约束是否存在：不允许自动分发修改、永远不需要测试、以及任何关键安全/合规要求
- 项目根目录是否正确（避免写错目录）

## 2) 复审维度（必须覆盖）

对 `draft-plan.md` 至少输出并回写以下内容：
- 流程闭环：循环A/循环B是否完整，确认点是否可执行
- 环境对照：对照 `~/environment.md` 标注已具备/缺失项，缺失项的安装负责人、校验方式
- 子代理与分工：对照 `~/.claude/agents/plan-agent/skills/agents-registry/references/registry.yaml` 做存在性确认；禁止"凑合替代"
- scope 落地性：allowed_paths/forbidden_patterns/dependencies/inputs/outputs/max_review_rounds 是否能实际 gate
- 风险与冲突点：流程漏洞、命名冲突、排序/稳定性问题、以及需要用户决策的点
- 下一步：明确用户的三选一确认，以及需要先补齐的阻塞项（blocked 原因用中文）

## 3) 回写策略（必须遵守）

- 未得到用户答复前：只允许写入"待确认问题清单"，不得把猜测当结论写入
- 得到用户答复后：把结论写入"analysis-agent复审补充"章节，并同步更新草案中的相关段落（尽量最小修改）
