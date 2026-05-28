---
name: "i18n-key-manager"
description: "管理翻译键定义与翻译值（校验变量、导入导出、建议发布范围）。当用户要新增/修改i18n键或批量导入翻译时调用。"
---

# 多语言键管理器（i18n Key Manager）

## 适用场景
- 新增/修改 TranslationSchema（分组、字段类型、变量约束）
- 批量导入导出翻译（按 locale）
- 变更后需要判断发布范围（增量 or 全站）

## 输入
- site_id
- storage_mode：flat-key / tree-json
- schema_changes：新增/修改的 key 定义（含 variables）
- translations_patch：按 locale 的增量变更
- import_export：csv/json（如果需要）

## 输出
- 校验结果：变量是否缺失、plural 结构是否合法
- 更新清单：新增 key、修改 key、删除 key
- 发布建议：受影响页面集合（通常 i18n 变更影响全站文案）

## 操作步骤（建议）
1. 校验变更（变量、plural、富文本策略），拒绝不安全输入。
2. 写入 translations 与 schema，生成变更版本号。
3. 触发依赖发布（常见为全站，或按依赖集合增量）。

## 风险与限制
- 不允许把 secrets 写入翻译配置
- 富文本/HTML 类型需要白名单清洗策略，避免 XSS

## 相关文档
- [i18n-management-spec.md](../../documents/02_Technical_Architecture/i18n-management-spec.md)
- [10_SLA与发布体系（99.9_10000页）.md](../../documents/02_Technical_Architecture/10_SLA与发布体系（99.9_10000页）.md)
