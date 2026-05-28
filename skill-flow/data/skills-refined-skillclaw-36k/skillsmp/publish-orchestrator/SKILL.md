---
name: "publish-orchestrator"
description: "编排站点发布与回滚（创建job、查询进度、重试/取消、版本切换）。当用户要单页/全站发布、查看发布状态或回滚时调用。"
---

# 发布编排器（Publish Orchestrator）

## 适用场景
- 用户说：发布单页/全站、批量发布、发布卡住/失败重试、取消发布、回滚到某版本
- 需要把“发布”落为：jobId 异步任务 + 版本化产物 + 原子切换 + 可审计

## 输入
- site_id：站点标识
- scope：single / all / dependency-set
- page_ids：当 scope=single 或 dependency-set 时提供
- reason：manual / schedule / webhook / migration
- theme_id@version：站点选用的主题版本
- feature_versions：能力包版本集合（如 commerce/tracking/cookie-consent）
- content_version / config_version：内容与配置版本（或变更集合hash）
- target_release_version：当回滚或指定发布版本时提供

## 输出
- job_id
- 状态：Queued / Building / Deployed / Failed / Cancelled
- 进度摘要：成功页数/失败页数/失败原因Top
- 上线结果：当前版本指针、回滚指针
- 审计摘要：actor、site_id、theme_version、feature_versions、duration、status

## 操作步骤（建议）
1. 计算发布范围（单页/依赖集合/全站）并创建 publish_job（立即返回 job_id）。
2. 轮询/订阅 job 状态；对可恢复错误执行重试；必要时取消。
3. 构建完成后执行原子切换；失败则保持旧版本；需要时一键回滚到上个稳定版本。

## 风险与限制
- 不允许同步等待构建完成（避免占用 API 线程与连接）
- Shopify/外部依赖必须限流与指数退避，避免 429 放大故障
- 回滚优先切换版本指针，不做逐页 CDN Invalidate

## 相关文档
- [10_SLA与发布体系（99.9_10000页）.md](../../documents/02_Technical_Architecture/10_SLA与发布体系（99.9_10000页）.md)
- [10_发布审计与回滚流程.md](../../documents/03_DevOps_Risk/10_发布审计与回滚流程.md)
- [11_全局组件批量发布方案.md](../../documents/03_DevOps_Risk/11_Publishing/11_全局组件批量发布方案.md)
