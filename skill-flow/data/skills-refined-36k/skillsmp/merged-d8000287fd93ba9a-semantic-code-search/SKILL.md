---
name: semantic-code-search
description: Use this skill for semantic code searching to understand business logic and locate specific code functionalities.
---

# Semantic Code Search Skill (Augment Context Engine)

This skill is designed for semantic code searching, making it the preferred tool during the R1 phase.

## Core Principle

> **Deep Analysis**: Understand the context before coding.

Follow a progressive development approach: complete preliminary research before starting any design or coding work.

## Priority

```
1. sou (augment-context-engine) — Semantic search, preferred
2. grep — Exact text matching
3. read_file — Last resort
```

## Invocation

### Semantic Search
```javascript
sou.search("用户认证逻辑")
sou.search("JWT token 验证")
sou.search("数据库连接配置")
```

### Keyword Search
```javascript
sou.search("handleSubmit")
sou.search("useEffect cleanup")
```

## Use Cases

| Scenario | Search Example |
|:---|:---|
| Understand business logic | `sou.search("订单状态流转")` |
| Locate functional code | `sou.search("用户登录处理")` |
| Find patterns | `sou.search("错误处理方式")` |
| API definitions | `sou.search("API 接口定义")` |

## R1 Phase Standard Process

```
1. memory.recall(project_path)     // Load memory
2. sou.search("<核心关键词>")      // Semantic search for code
3. Only read directly related files; avoid full scans
```

## Best Practices

### ✅ Good Searches
```javascript
sou.search("用户注册验证逻辑")     // Semantically clear
sou.search("支付回调处理")         // Business relevant
```

### ❌ Avoided Searches
```javascript
sou.search("function")            // Too generic
sou.search("const")               // Meaningless
```

## Degradation Plan

When sou is unavailable:
```bash
grep -r "关键词" --include="*.ts" ./src
find . -name "*.ts" -exec grep -l "关键词" {} \;
```