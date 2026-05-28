---
name: "theme-registry-manager"
description: "管理主题与能力包版本（登记、查询、上架/下架、变更说明）。当用户要升级Header/Footer、切换主题版本或上架feature pack时调用。"
---

# 主题与能力包版本管理器（Theme Registry Manager）

## 适用场景
- 主题升级：Header/Footer 组件升级、样式/资源升级
- 能力包升级：commerce/tracking/cookie-consent 版本变更
- 需要把“站点发布”绑定到可回滚的版本号组合

## 输入
- artifact_type：npm / tarball / git-sha / oci-image
- artifact_id：包名或地址
- theme_id / feature_id
- version：语义化版本或 commit SHA
- changelog：变更说明（面向运营+技术）
- status：active / deprecated / blocked

## 输出
- registry 记录：可用版本列表、状态、变更说明
- 站点可选项：哪些 theme/feature 组合可用于新站点/发布

## 操作步骤（建议）
1. 登记版本与 artifact 信息（含校验/签名策略）。
2. 标记可用性（active/deprecated/blocked），并附上回滚建议版本。
3. 更新站点选择范围与发布系统引用策略。

## 风险与限制
- 版本一旦用于生产发布应不可变（至少 artifact 内容不可变）
- blocked 版本必须禁止被发布系统引用，避免事故扩散

## 相关文档
- [07_平台与站点工程边界（MVP方案A）.md](../../documents/02_Technical_Architecture/07_平台与站点工程边界（MVP方案A）.md)
- [11_全局组件批量发布方案.md](../../documents/03_DevOps_Risk/11_Publishing/11_全局组件批量发布方案.md)
