---
name: style-and-consistency
version: 1.0.0
description: 规范与一致性审查（命名、接口契约、错误码、可读性）
language: common
tags: [style, common]
---

# style-and-consistency

## 重点检查项（Checklist）

- 命名一致：变量/函数/接口命名是否表达意图；是否与项目约定一致
- 接口契约：输入输出字段、错误码、返回结构是否稳定；是否破坏兼容性
- 日志可观测：关键路径是否可追踪；是否包含 trace_id/request_id
- 可读性：复杂逻辑是否拆分；是否增加必要注释/文档
