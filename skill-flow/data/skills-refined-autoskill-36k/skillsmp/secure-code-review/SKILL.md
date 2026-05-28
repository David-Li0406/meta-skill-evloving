---
name: secure-code-review
version: 1.0.0
description: 通用安全审查清单（输入验证、认证授权、敏感信息、错误处理与审计）
language: common
tags: [security, owasp, cwe, common]
---

# secure-code-review

## 重点检查项（Checklist）

- 输入验证：外部输入是否经过校验/白名单/长度限制/类型转换
- 输出编码：是否存在 XSS/HTML 注入（模板渲染、拼接 HTML、富文本）
- 认证与授权：是否存在越权（IDOR）、缺少鉴权、权限绕过
- 注入类：SQL/命令/模板/表达式/路径注入是否可达
- 文件与路径：上传、解压、路径拼接是否可穿越；是否校验 MIME/扩展名/大小
- SSRF：是否允许访问内网/metadata；是否校验 URL scheme/host
- 反序列化：是否反序列化不可信数据；是否启用安全类型白名单
- 错误处理：是否泄露堆栈、密钥、内部路径；是否吞异常导致安全逻辑失效
- 日志与审计：关键操作是否有审计日志；日志是否避免记录敏感信息

## 常见证据（Evidence）

- 出现 `eval/exec`, `os.system/subprocess`, SQL 字符串拼接，或直接使用用户输入构造 URL/文件路径
