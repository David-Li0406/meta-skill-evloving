---
date: "2026-01-13"
tags: [galgame, skill-creation, abstraction, design-pattern]
---

# Galgame Skill 通用化經驗

> 將專案專用 skill 抽象為通用框架的設計模式

## 背景

從 Dead Romance 專案的 `galgame-creator` skill (v3.0.0) 提煉出通用的 `galgame-master` skill (v1.0.0)。

## 關鍵決策

### 1. 移除專案綁定

| 專案專用 | 通用化 |
|----------|--------|
| 固定角色 (medic_lin, mechanic_wu) | 角色創建模板 |
| 殭屍末日設定 | 世界觀模板系統 |
| 固定檔案路徑 | 建議目錄結構 |
| R15 固定分級 | 可選分級系統 |

### 2. 保留核心價值

- **34 種角色類型庫**：這是最有價值的資產，完整保留
- **角色公式**：`Dere + 關係 + 身份 + 特殊屬性`
- **好感度進展系統**：Lv0-Lv5 的對話變化
- **反差設計原則**：表面 vs 私底下

### 3. 新增通用模組

- 世界觀初始化模板
- 劇本架構系統（共通路線 → 個人路線 → 多結局）
- 內容分級系統（G/R15/R15+/R18 可選）
- 專案目錄結構建議

## 設計模式

### 從專用到通用的抽象步驟

1. **識別硬編碼**：找出所有專案特定的內容
2. **提取參數**：將固定值改為可配置選項
3. **保留核心**：確保核心價值（角色類型庫）完整
4. **添加框架**：補充通用場景所需的模板
5. **文檔完善**：讓任何專案都能快速上手

### Skill 分層策略

```
全域 Skill (galgame-master)
├── 角色類型庫（34 種）
├── 劇本架構模板
├── 對話生成系統
└── 美術指示框架

專案 Skill (galgame-creator)
├── 繼承全域 Skill
├── 專案專屬角色
├── 特定世界觀設定
└── 自訂內容分級
```

## 檔案位置

- 全域 Skill: `~/.claude/skills/galgame-master/SKILL.md`
- 專案 Skill: `<project>/.claude/skills/galgame-creator/SKILL.md`

## 標籤

skill-design, generalization, galgame, character-design, abstraction
