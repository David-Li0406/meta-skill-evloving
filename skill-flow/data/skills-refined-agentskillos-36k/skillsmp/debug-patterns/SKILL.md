---
name: debug-patterns
description: 快速诊断手册，解决常见技术报错（API 失败、代理问题、编码错误、JSON 解析）。
当遇到明确的错误信息时使用。复杂问题请使用 systematic-debugging。
Use when encountering specific technical errors like API failures, proxy issues, or parse errors.
For complex issues, use systematic-debugging instead.
allowed-tools: "Bash,Read,Write,mcp__tavily__tavily-search"
---

# Debug Patterns - 快速诊断手册

常见技术问题的快速诊断和解决方案。

## 🎯 适用范围

**使用此技能**：
- ✅ 有明确错误信息（curl 报错、编码错误、JSON 解析失败）
- ✅ 快速诊断，秒级解决
- ✅ 技术层面问题（网络、编码、格式）

**升级到 systematic-debugging**：
- ❌ 错误信息模糊或不明确
- ❌ 问题时好时坏、难以复现
- ❌ 多次尝试仍无法解决
- ❌ 需要深度分析根因

---

## 🔧 网络诊断

### 首先检查：代理

响应为空或超时时：

```bash
# 检查代理是否干扰
curl -v "https://api.example.com" 2>&1 | grep -i proxy

# 检查环境变量
echo $http_proxy $https_proxy $HTTP_PROXY $HTTPS_PROXY
```

### 绕过代理测试

```bash
# 不使用代理测试
curl -s --noproxy "*" "https://api.example.com"

# 临时取消代理
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
curl "https://api.example.com"
```

### 常见 curl 错误

```bash
# 超时
curl: (28) Operation timed out
→ 检查网络、代理、防火墙

# DNS 解析失败
curl: (6) Could not resolve host
→ 检查 DNS、URL 拼写

# SSL 证书问题
curl: (60) SSL certificate problem
→ curl -k 跳过验证（仅测试用）

# 连接拒绝
curl: (7) Failed to connect
→ 检查端口、服务是否运行
```

---

## 📄 JSON 安全解析

### 问题：嵌套 get() 遇到 None 仍报错

```bash
# ❌ 错误：遇到 None 仍崩溃
curl "url" | python3 -c 'import json,sys; r=json.load(sys.stdin); print(r.get("a", {}).get("b", {}).get("c"))'

# ✅ 正确：保存文件 + 独立脚本
curl "url" > /tmp/data.json && python3 << 'EOF'
import json
d = json.load(open("/tmp/data.json"))
# 多行安全处理
value = d.get("a", {}) or {}
value = value.get("b", {}) or {}
print(value.get("c"))
EOF
```

### jq 安全解析

```bash
# 检查字段是否存在
curl "api.json" | jq 'if .a.b.c then .a.b.c else "null" end'

# 或使用 // 提供默认值
curl "api.json" | jq '.a.b.c // "default"'
```

---

## 🔤 编码错误

### 问题：中文内容的非 UTF-8 编码

```bash
# ❌ 错误：编码错误
echo "中文" | python3 -c 'import sys; print(sys.stdin.read())'

# ✅ 正确：声明 UTF-8
python3 << 'EOF'
# -*- coding: utf-8 -*-
import sys
sys.stdin.reconfigure(encoding='utf-8')
print(sys.stdin.read())
EOF
```

### curl 中文乱码

```bash
# 添加编码头
curl -H "Accept-Charset: utf-8" "url"

# 或用 iconv 转换
curl "url" | iconv -f gbk -t utf-8
```

---

## 📚 API 特定模式

### DBLP 空结果处理

```python
# ❌ 错误：无结果时 KeyError
hits = d['result']['hits']['hit']

# ✅ 正确：先检查 @total
total = d['result']['hits'].get('@total', '0')
hits = d['result']['hits'].get('hit', []) if total != '0' else []
```

### OpenAlex 精确搜索

```bash
# ❌ 太宽泛：38,289 条不相关结果
curl "api.openalex.org/works?search=ccAI"

# ✅ filter 精确匹配
curl "api.openalex.org/works?filter=title.search:Compatible%20and%20Confidential"
```

---

## 🚨 错误捕获

### 始终捕获 stderr

```bash
# ❌ 错误：遗漏错误信息
command

# ✅ 正确：完整错误输出
command 2>&1

# ✅ 更好：分别保存
command > output.txt 2> error.txt
```

### Shell 脚本错误处理

```bash
# 遇到错误立即退出
set -e

# 显示执行的命令
set -x

# 管道中任何命令失败都退出
set -o pipefail
```

---

## 🔄 调试流程

```
遇到错误
  ↓
错误信息明确？
  ├─ 是 → 使用本 skill（debug-patterns）
  │         快速诊断 → 解决
  │
  └─ 否 / 多次尝试失败
            ↓
    切换 systematic-debugging
            ↓
    五步法深度分析
```

---

## 常见触发场景

使用此技能时，你会听到：
- "API 调用失败"
- "代理不工作"
- "JSON 解析错误"
- "编码问题"
- "curl 报错"
- "API timeout"
- "Proxy not working"
- "Parse error"
- "Encoding error"
