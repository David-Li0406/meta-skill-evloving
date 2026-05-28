---
date: "2026-01-12"
tags: [evolve, token, optimization, skillpkg, context-window, performance]
task: 研究 evolve skill token 使用量過高問題
status: resolved
---

# Evolve Skill Token 使用量優化研究

## 情境
用戶反饋使用 evolve skill 的專案 token 使用量過高，需要研究優化方式。

## 問題發現

### 數據對比
| 項目 | 源碼 (skills/) | 安裝後 (~/.claude/skills/evolve/) |
|------|---------------|-----------------------------------|
| SKILL.md 大小 | 14.7 KB | 106.8 KB (7x 膨脹) |
| 行數 | ~300 行 | 3,452 行 |
| 估算 tokens | ~3,600 | ~26,750 |

### 根本原因
`skillpkg` 在安裝 skill 時，會將所有子模組內容**內嵌合併**到單一 SKILL.md：
- 原始結構：原子化模組（多個目錄/檔案）
- 安裝後：所有內容合併到一個巨大 SKILL.md
- 結果：每次 `/evolve` 都載入 ~27K tokens 的 context

### Token 分佈（主要消耗）
1. 檢查點模組 (02-checkpoints)：~6 個檔案，含詳細流程圖
2. 核心流程 (01-core)：PDCA、目標分析等完整說明
3. 整合模組 (05-integration)：各種 MCP 整合說明
4. ASCII 圖表：多處重複的流程圖

## 優化方案

### 方案 1：分層載入架構（推薦 ⭐）
```
SKILL.md (精簡核心 ~3KB)
├── 只保留：基本流程、檢查點列表、模組索引
└── 其他內容按需載入

執行時按需讀取：
├── 遇到 CP1 → Read(02-checkpoints/_base/cp1-memory-search.md)
├── 遇到 PDCA → Read(01-core/_base/pdca-cycle.md)
└── 需要整合 → Read(05-integration/_base/xxx.md)
```
預期效果：初始載入從 27K → ~1K tokens (96% 降低)

### 方案 2：skillpkg 配置
```yaml
# SKILL.md frontmatter
inline_modules: false  # 告訴 skillpkg 不要合併子模組
```
需要 skillpkg 支援此功能。

### 方案 3：內容精簡
- 移除重複 ASCII 流程圖
- 合併相似範例
- 使用引用替代內嵌

### 方案 4：動態載入機制
```python
load_skill("evolve", mode="minimal")  # 只載入核心
# 執行中按需載入模組
```

## 建議行動優先級
1. **短期**：精簡 SKILL.md 主文件
2. **中期**：實作分層載入邏輯
3. **長期**：修改 skillpkg 支援不合併模式

## 驗證
✅ 確認問題根因：skillpkg 合併機制
✅ 提出多個可行優化方案
✅ 估算預期改善效果

## 相關檔案
- `skills/SKILL.md` - 源碼版本（14.7 KB）
- `~/.claude/skills/evolve/SKILL.md` - 安裝版本（106.8 KB）
