---
date: "2026-01-12"
tags: [skillpkg, token-optimization, research, evolve]
---

# skillpkg 分層載入機制研究

> 目的：找出 evolve skill token 優化方案

## 背景問題

安裝後的 evolve skill 從源碼 8.9KB 膨脹到 106.8KB（12 倍）

## 核心發現

### 1. 膨脹原因

| 原因 | 佔比 | 說明 |
|------|------|------|
| **完整目錄複製** | ~70% | `syncer.ts` 使用 `cp(recursive: true)` 複製整個 skill 目錄 |
| **依賴傳遞** | ~20% | 安裝所有 transitive dependencies |
| **重複存儲** | ~10% | `.skillpkg/` + `.claude/skills/` 雙份存儲 |

### 2. skillpkg 已支援的功能

✅ **子目錄安裝**
```bash
skillpkg install user/repo#path/to/skill
```

✅ **依賴管理**
```yaml
# SKILL.md frontmatter
dependencies:
  skills:
    - user/other-skill
```

✅ **循環依賴檢測**

✅ **反向依賴追蹤**（防止誤刪被依賴 skill）

### 3. 尚未支援（需要 PR 貢獻）

❌ **按需載入** - 無法只載入 SKILL.md 主檔
❌ **文件過濾** - 無法排除 `.md` 文檔、測試檔
❌ **去重機制** - 無 symlink 或 hardlink 優化

## 可行方案

### 方案 A：子目錄拆分（無需改 skillpkg）

```
self-evolving-agent/
├── skills/
│   ├── SKILL.md              # 核心 (8.9KB)
│   ├── checkpoints/
│   │   └── SKILL.md          # 獨立 skill
│   └── integration/
│       └── SKILL.md          # 獨立 skill
```

使用方式：
```bash
skillpkg install miles990/self-evolving-agent#skills           # 只裝核心
skillpkg install miles990/self-evolving-agent#skills/checkpoints  # 需要時加裝
```

### 方案 B：貢獻 skillpkg PR

在 `SkillInstallOptions` 加入：
```typescript
{
  essentialOnly: true,          // 只裝 SKILL.md
  skipPatterns: ['*.md'],       // 跳過文檔
  categories: ['instruction']   // 只要特定分類
}
```

### 方案 C：手動管理（當前做法）

直接複製 SKILL.md 到 `~/.claude/skills/evolve/`

## 建議

1. **短期**：使用方案 C（手動同步源碼 SKILL.md）
2. **中期**：重構為方案 A 架構（子目錄拆分）
3. **長期**：向 skillpkg 提交 PR 支援分層載入

## 相關文件

- `/Users/user/Workspace/skillpkg/packages/core/src/sync/syncer.ts` - 同步邏輯
- `/Users/user/Workspace/skillpkg/packages/core/src/dependency/dependency-resolver.ts` - 依賴解析
- `/Users/user/Workspace/skillpkg/packages/core/src/store/store-manager.ts` - 存儲管理
