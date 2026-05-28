---
name: "schema-validator"
description: "校验页面实例与Schema定义的一致性（类型/约束/安全），并给出可发布结论。保存页面、预发布检查或批量体检时调用。"
---

# Schema 校验器（Schema Validator）

## 适用场景
- 保存页面前：防止无效 JSON/字段类型错误进入数据库
- 预发布：批量校验受影响页面集合，降低发布失败率
- 安全检查：处理 html/liquid 等高风险字段策略

## 输入
- component_definitions：组件定义集合（ComponentDefinition/SettingDefinition）
- page_instances：单页或多页（PageInstance JSON）
- policy：
  - html：allow / sanitize / deny
  - liquid：deny（MVP默认）/ allow-placeholder
  - unknown_fields：deny / warn

## 输出
- errors：阻断发布的错误列表
- warnings：可发布但需注意的问题
- autofix_suggestions：可自动修复项（如缺失默认值）
- publishable：true/false

## 操作步骤（建议）
1. 结构校验：sections/order/blocks/block_order、字段类型一致性。
2. 约束校验：min/max/options/accept 等。
3. 安全校验：html/liquid 策略、富文本白名单、URL/资源引用检查。

## 相关文档
- [07_Schema设计规范_Shopify兼容版.md](../../documents/02_Technical_Architecture/07_Schema设计规范_Shopify兼容版.md)
- [07_ContentTypeBuilder_数据流说明.md](../../documents/02_Technical_Architecture/07_ContentTypeBuilder_数据流说明.md)
