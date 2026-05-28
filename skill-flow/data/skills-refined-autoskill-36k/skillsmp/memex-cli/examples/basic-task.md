# Basic Task Example

This file demonstrates a simple single-task execution using memex-cli stdin protocol.

## Usage

```bash
memex-cli run --stdin < examples/basic-task.md
```

## Task Definition

---TASK---
id: implement-auth-20260110000000
backend: codex
workdir: ./project
model: gpt-5.2
timeout: 300
retry: 1
---CONTENT---
实现一个用户认证模块，包含以下功能：

1. 用户注册
   - 验证邮箱格式
   - 密码强度检查（至少8位，包含字母和数字）
   - 密码加密存储（使用 bcrypt）

2. 用户登录
   - 邮箱+密码验证
   - 返回 JWT token
   - Token 有效期 24 小时

3. 密码重置
   - 发送重置链接到邮箱
   - 验证重置 token
   - 更新密码

技术栈：
- Python 3.10+
- FastAPI
- SQLAlchemy
- PyJWT
- bcrypt

请生成完整的代码，包括：
- models.py - 用户数据模型
- auth.py - 认证逻辑
- routes.py - API 路由
- schemas.py - Pydantic 模型
- utils.py - 工具函数（密码哈希、token 生成）

确保代码包含错误处理和类型注解。
---END---

## Expected Output

The task will generate:
- `project/models.py` - SQLAlchemy User model
- `project/auth.py` - Authentication logic
- `project/routes.py` - FastAPI routes
- `project/schemas.py` - Pydantic schemas
- `project/utils.py` - Utility functions

## Output Format

Default text format will show:

```
▶ implement-auth-20260110000000 (codex/gpt-5.2)

[AI-generated code output]

» 写入 project/models.py
» 写入 project/auth.py
» 写入 project/routes.py
» 写入 project/schemas.py
» 写入 project/utils.py

✓ implement-auth-20260110000000 12.3s
```

## Customization

Modify the task for different scenarios:

**Change backend:**
```
backend: claude    # For design/architecture tasks
backend: gemini    # For multimodal tasks
```

**Adjust timeout:**
```
timeout: 600       # Allow up to 10 minutes
```

**Add retry:**
```
retry: 2           # Retry twice on failure
```

**Change workdir:**
```
workdir: /path/to/your/project
```

## Save Output as JSONL

For programmatic parsing:

```bash
memex-cli run --stdin --stream-format jsonl < examples/basic-task.md > output.jsonl
```

Parse events:

```bash
cat output.jsonl | jq 'select(.type == "assistant.action")'
```
