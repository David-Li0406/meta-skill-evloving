---
name: build-report
description: "编译报告模板：build-agent输出编译报告时使用。触发条件：编译成功或失败需要输出报告。"
---

# build-report

编译报告模板，供 build-agent 输出编译结果时使用。

## When to Use This Skill

触发条件（满足任一）：
- build-agent 编译成功，需要输出成功报告
- build-agent 编译失败，需要输出错误追溯报告

## Not For / Boundaries

**不做**：
- 不直接执行编译（由 build-agent 负责）
- 不修改源代码

**使用方式**：
- 按需读取 `references/` 下的模板
- 填充模板后输出报告

## Quick Reference

### 模板文件

```
references/
├── error-report-template.md   # 编译错误报告模板
└── success-report-template.md # 编译成功报告模板
```

### 使用流程

```
1. 编译完成后判断成功/失败
2. 读取对应模板
3. 填充实际数据
4. 输出报告
5. 追加到 Record/record.md
```

## Examples

### Example 1: 编译成功

- **输入**: cargo build --release 成功
- **步骤**:
  1. 读取 `references/success-report-template.md`
  2. 填充编译结果、产出文件、验证结果
  3. 输出报告
  4. 追加到 record.md
- **验收**: 报告包含产出文件清单

### Example 2: 编译失败

- **输入**: 编译出现类型错误
- **步骤**:
  1. 读取 `references/error-report-template.md`
  2. 填充错误详情、责任追溯
  3. 输出报告
  4. 追加到 record.md
- **验收**: 报告包含责任提案和修复流程

### Example 3: 多平台编译

- **输入**: 需要编译 Linux 和 Windows 版本
- **步骤**:
  1. 逐平台编译
  2. 汇总所有平台结果到一份报告
  3. 输出报告
- **验收**: 报告包含所有平台的编译状态

## Maintenance

- 来源：双AI协同开发方案内部规范
- 最后更新：2026-01-05
- 已知限制：仅提供模板，不执行编译
