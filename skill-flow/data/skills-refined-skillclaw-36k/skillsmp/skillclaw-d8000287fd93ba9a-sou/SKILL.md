---
name: sou
description: Use this skill when you need to perform semantic code searches to understand business logic or locate specific functionality within your codebase.
---

# Sou Skill (Augment Context Engine)

## Core Concept

> **Deep Analysis**: Understand the context before diving into coding.

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
sou.search("用户认证逻辑") // User authentication logic
sou.search("订单状态流转") // Order status flow
```

### Keyword Search
```javascript
sou.search("handleSubmit")
sou.search("useEffect cleanup")
```

## Use Cases

| Scenario          | Search Example                     |
|-------------------|------------------------------------|
| Understand business logic | `sou.search("订单状态流转")` |
| Locate functionality code | `sou.search("用户登录处理")` |
| Find patterns      | `sou.search("错误处理方式")`     |
| API definitions    | `sou.search("API 接口定义")`     |

## Standard Process for R1 Phase

```
1. memory.recall(project_path)     // Load memory
2. sou.search("<keyword>")          // Perform semantic search
3. Read only directly related files; avoid full scans
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
sou.search("const")               // No meaningful value
```

## Downgrade Plan

If sou is unavailable:
```bash
grep -r "关键词" --include="*.ts" ./src
find . -name "*.ts" -exec grep -l "关键词" {} \;
```