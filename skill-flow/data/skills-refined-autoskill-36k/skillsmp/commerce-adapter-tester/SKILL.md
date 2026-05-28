---
name: "commerce-adapter-tester"
description: "自测电商闭环（cart/checkout/webhook）与限流幂等表现。上线前验收电商或排障Shopify 429/回放失败时调用。"
---

# 电商适配自测器（Commerce Adapter Tester）

## 适用场景
- 展示+销售站点上线前，验证购物车/结算/订单 webhook 闭环
- 发生 429、重试风暴、webhook 重放/幂等异常时定位问题

## 输入
- site_id
- scenarios：add-to-cart、update-cart、checkout、webhook-order-created、webhook-payment-succeeded
- storefront_context：店铺域、渠道、区域（不在输出中回显敏感信息）
- rate_limit_profile：并发上限、退避参数

## 输出
- 用例结果（通过/失败）
- 限流与重试统计（429 次数、重试次数、最终成功率）
- 幂等命中率（webhook/订单写入）
- 问题定位建议（落点：Java 代理、缓存、队列、签名校验）

## 风险与限制
- 不在日志中输出密钥/令牌
- 测试 webhook 需使用脱敏 payload 或测试环境

## 相关文档
- [11_开发重难点清单.md](../../documents/02_Technical_Architecture/11_开发重难点清单.md)
- [10_核心风险与应对策略.md](../../documents/03_DevOps_Risk/10_核心风险与应对策略.md)
