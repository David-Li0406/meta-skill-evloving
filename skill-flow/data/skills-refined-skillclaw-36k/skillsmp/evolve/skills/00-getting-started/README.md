# 00-getting-started

> 入門與環境設定

## 本模組包含

| 文件 | 用途 | 建議閱讀順序 |
|------|------|-------------|
| [init.md](./_base/init.md) | 初始化指南、記憶系統建立 | 1️⃣ 第一個讀 |
| [psb-setup.md](./_base/psb-setup.md) | PSB 環境檢查清單 | 2️⃣ 第二個讀 |
| [version-check.md](./_base/version-check.md) | 版本檢查與自動更新 | 🔄 自動執行 |

## 快速開始

```bash
# 1. 檢查環境
git status && ls CLAUDE.md 2>/dev/null || echo "建議建立 CLAUDE.md"

# 2. 初始化記憶系統
ls .claude/memory/ 2>/dev/null || echo "需要初始化記憶系統"

# 3. 開始使用
/evolve [你的目標]
```

## 社群貢獻

