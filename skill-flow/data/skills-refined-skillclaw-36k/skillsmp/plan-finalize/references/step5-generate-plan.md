# 步骤5：生成确定方案

## 执行

1. 创建`Record/plan/{plan_version}-plan.md`
2. 内容必须包含（见`final-plan-template.md`）：
   - plan_version
   - 需求摘要
   - 最终scope
   - 环境确认结论
   - 子代理分工详情（含运行槽位）
   - 编译配置
   - 用户确认记录

## 运行槽位说明

同一子代理需要多个实例并行时，使用运行槽位标记：
- `python-agent-01`：负责模块A
- `python-agent-02`：负责模块B

运行槽位仅用于分工标记，用户实际操作：开多个子代理会话。

## 更新状态

更新`Record/state.json`：
- 设置`active_plan_version`为当前版本
- 记录冻结时间
