---
name: security-scanner
description: 安全扫描器。检测 Claude Code 自定义 skills 中的潜在恶意代码。当用户提到"安全扫描"、"检测恶意代码"、"skill 安全"或需要扫描 skill 时使用。
allowed-tools: Read, Bash
---

# Security Scanner - Skill 安全扫描器

防御性安全工具，用于检测自定义 skills 中的潜在恶意代码。

## 功能

- 静态代码分析（AST）
- 危险函数检测
- 网络操作检测
- 文件操作检测
- 代码混淆检测
- 数据外泄检测

## 使用方法

```bash
# 扫描所有 skills
python ~/.claude/skills/security-scanner/scripts/scanner.py

# 扫描指定 skill
python ~/.claude/skills/security-scanner/scripts/scanner.py --skill descriptive-stats
```
