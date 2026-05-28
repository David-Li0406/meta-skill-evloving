---
date: 2026-01-12
tags: [self-evolution, skill-modification, workflow, source-of-truth]
task: 修改 skill 本身（自我進化）
status: resolved
---

# 自我進化流程：修改 Skill 的正確順序

## 情境

當 AI 需要修改 skill 本身時（例如新增 checkpoint、更新流程），需要遵循特定順序。

## 問題

錯誤順序會導致：
- 專案原始碼與安裝版不同步
- Source of truth 被覆蓋
- 難以追蹤變更歷史

## 正確流程

```
1. 更新專案原始碼
   └─ /Users/user/Workspace/self-evolving-agent/skills/*.md

2. Git commit
   └─ 記錄變更，建立歷史追蹤

3. 更新安裝版（如需要）
   └─ ~/.claude/skills/evolve/SKILL.md
```

## 為什麼這個順序

| 版本 | 角色 | 說明 |
|------|------|------|
| 專案版 | Source of Truth | 模組化、可協作、有 git 歷史 |
| 安裝版 | 衍生物 | 打包版、供執行時使用 |

**原則：永遠先更新 source of truth，再同步衍生物**

## 實際案例

新增 CP1.5 一致性檢查時：
- ❌ 錯誤：先改 `~/.claude/skills/evolve/SKILL.md`
- ✅ 正確：先改 `skills/02-checkpoints/_base/cp1.5-consistency-check.md` + commit

## 為什麼不需要變成 Checkpoint

1. **頻率太低** - 幾週才發生一次
2. **已有社會約束** - 錯了會被指正
3. **複雜度不成比例** - 規範成本 > 收益

## 結論

這是一個「知道就好」的流程，記錄在 Memory 供查閱，而非強制 Checkpoint。
