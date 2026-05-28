---
name: performance-review
version: 1.0.0
description: 性能与资源使用审查清单（N+1、缓存、IO、锁争用）
language: common
tags: [performance, common]
---

# performance-review

## 重点检查项（Checklist）

- N+1 查询：循环内访问数据库/外部 API；是否可批量化/预取
- IO/网络：是否有无界重试/大文件读写；是否设置超时与限流
- 缓存：热点数据是否缓存；缓存键是否包含租户/权限维度
- 并发与锁：是否可能产生锁争用/死锁；是否需要队列/异步化
- 算法与复杂度：是否出现明显 O(n^2) 或无必要的全量扫描
