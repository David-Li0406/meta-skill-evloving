---
name: "preview-runner"
description: "触发并汇总预览结果（Java转发到Node Preview），输出预览链接与渲染耗时/错误快照。用户要预览或验收预览时调用。"
---

# 预览执行器（Preview Runner）

## 适用场景
- 单页预览（运营验收）
- 批量预览（上线前抽样）
- 预览异常排障（渲染失败/数据缺失）

## 输入
- site_id
- page_id（或 page_ids）
- locale
- device：desktop/mobile
- preview_mode：draft/published

## 输出
- preview_url
- render_metrics：耗时、错误率（如可采集）
- error_snapshot：关键错误摘要（不包含 secrets）

## 操作步骤（建议）
1. Java API 做鉴权与参数校验，转发到 Node Preview 渲染。
2. 汇总渲染结果与耗时，返回前端展示。
3. 失败时输出可定位的错误摘要与建议（缺失 schema/缺失 data）。

## 相关文档
- [07_技术架构文档.md](../../documents/02_Technical_Architecture/07_技术架构文档.md)
- [09_架构设计图表.md](../../documents/02_Technical_Architecture/09_架构设计图表.md)
