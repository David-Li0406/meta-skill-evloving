# 03-execution

PDCA 執行循環模組。

## 內容

| 文件 | 說明 |
|------|------|
| [pdca-loop.md](./_base/pdca-loop.md) | Plan-Do-Check-Act 循環實作 |

## 核心功能

1. **Plan** — 規劃實作方案
2. **Do** — 執行程式碼變更
3. **Check** — 驗證變更（測試、lint、build）
4. **Act** — 調整或提交

## 整合 Subagents

- verify-app
- build-validator
- code-simplifier
