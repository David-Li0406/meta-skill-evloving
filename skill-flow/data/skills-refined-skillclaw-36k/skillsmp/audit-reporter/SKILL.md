---
name: "audit-reporter"
description: "生成发布审计报告（版本组合、操作者、耗时、结果），支持评审/复盘。上线评审、事故复盘或合规抽查时调用。"
---

# 审计报告生成器（Audit Reporter）

## 适用场景
- 上线评审：发布前后差异、版本组合、影响范围
- 事故复盘：谁在何时发布了什么、失败点在哪里
- 合规抽查：权限与敏感操作审计

## 输入
- site_id
- time_range
- filters：actor、status、scope、theme_version、feature_versions
- format：markdown / csv

## 输出
- 报告：发布列表、关键指标（成功率、P95耗时、回滚次数）
- 关键结论：Top 失败原因、建议改进项

## 操作步骤（建议）
1. 拉取 publish_job 与相关审计表（按筛选条件）。
2. 生成汇总与明细（按站点/版本/操作者分组）。
3. 输出到 Markdown/CSV 并给出结论。

## 相关文档
- [10_发布审计与回滚流程.md](../../documents/03_DevOps_Risk/10_发布审计与回滚流程.md)
- [10_SLA与发布体系（99.9_10000页）.md](../../documents/02_Technical_Architecture/10_SLA与发布体系（99.9_10000页）.md)
