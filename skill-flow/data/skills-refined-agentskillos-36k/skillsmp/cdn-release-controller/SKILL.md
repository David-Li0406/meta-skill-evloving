---
name: "cdn-release-controller"
description: "控制静态站上线与回滚（版本指针切换、可选边缘重写开关、回滚预案）。发布完成切换版本或需要快速回滚时调用。"
---

# CDN 发布控制器（CDN Release Controller）

## 适用场景
- 发布完成后切换当前版本指针
- 线上异常需要分钟级回滚
- 评估/启用边缘重写（用于全局片段高频小改动）

## 输入
- site_id
- release_version（将要上线）
- previous_version（用于回滚）
- rewrite_switch：on/off（如果采用边缘重写方案）
- cache_policy：HTML 缓存策略摘要（如有）

## 输出
- 切换结果：当前指针、上一个指针
- 回滚预案：步骤与预估耗时
- 风险提示：边缘重写开销/缓存错配风险

## 操作步骤（建议）
1. 校验 release_version 完整性（manifest、路由清单、校验和）。
2. 原子切换“当前版本指针”到新版本。
3. 监控异常则切回 previous_version 并生成审计记录。

## 相关文档
- [10_发布审计与回滚流程.md](../../documents/03_DevOps_Risk/10_发布审计与回滚流程.md)
- [10_媒体与CDN策略规范.md](../../documents/03_DevOps_Risk/10_媒体与CDN策略规范.md)
