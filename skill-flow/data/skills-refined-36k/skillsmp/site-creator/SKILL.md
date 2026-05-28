---
name: "site-creator"
description: "创建站点实例并完成装配（选theme版本、启用能力包、初始化域名/i18n）。当用户要新建品牌站或品牌展示+销售站时调用。"
---

# 站点创建器（Site Creator）

## 适用场景
- 新建品牌展示站（多个）
- 新建品牌展示+销售站（多个）
- 从模板/seed 快速初始化站点，并确保可发布、可回滚

## 输入
- site_id / site_key
- site_type：showcase / commerce
- theme_id@version
- enabled_features：示例：["tracking","cookie-consent"] 或加上 "commerce"
- locales：default_locale、published_locales
- domain：主域名与证书策略（如需要）
- initial_content_seed：是否导入默认首页/导航/页脚

## 输出
- 站点实例配置清单（可审计）
- 站点装配结果：theme 与 feature 列表、版本号
- 下一步建议：创建首页、配置导航、预览、发布

## 操作步骤（建议）
1. 生成站点实例与基础配置（site_id、domain、locales、feature flags）。
2. 绑定 theme@version 与 enabled_features，并写入站点配置中心。
3. 导入 seed 内容（可选），并触发一次预览校验。

## 风险与限制
- site 工程不是独立仓库；站点实例=配置+内容+选用版本的组合
- commerce 站点必须校验 Shopify 集成所需配置是否齐备（域名、API 权限、webhook）

## 相关文档
- [07_平台与站点工程边界（MVP方案A）.md](../../documents/02_Technical_Architecture/07_平台与站点工程边界（MVP方案A）.md)
- [07_技术架构文档.md](../../documents/02_Technical_Architecture/07_技术架构文档.md)
