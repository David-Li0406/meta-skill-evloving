---
name: test-coverage-review
version: 1.0.0
description: 测试覆盖审查（单测/集成测试、边界与异常用例）
language: common
tags: [testing, common]
---

# test-coverage-review

## 重点检查项（Checklist）

- 是否新增/更新了对应单测或集成测试
- 边界条件：空值、极值、超长输入、并发、权限边界
- 异常路径：超时、第三方失败、重试/回滚、幂等性
- 回归风险：是否补充了容易复现的问题用例（防止反复出现）
