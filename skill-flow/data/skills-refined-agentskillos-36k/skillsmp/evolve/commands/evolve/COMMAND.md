---
name: evolve
description: 自我進化 Agent - 給定目標，自主學習並迭代改進直到完成
arguments:
  - name: goal
    description: 目標描述
    required: false
  - name: --explore
    description: 探索模式 - 允許自主選擇方向
    required: false
  - name: --emergence
    description: 涌現模式 - 啟用跨領域連結探索
    required: false
  - name: --autonomous
    description: 自主模式 - 完全自主，追求系統性創新
    required: false
  - name: --new-skill
    description: 建立新 Skill（完整工作流）
    required: false
---

# /evolve

執行 Self-Evolving Agent 流程。

## 流程

1. **CP0: 北極星錨定** — 建立或讀取專案願景
2. **PSB System** — Plan → Setup → Build（環境準備）
3. **目標分析** — 深度訪談 + 架構等級判斷
4. **能力評估 → Skill 習得**
5. **PDCA Cycle** — Plan → Do → Check → Act（含方向校正）
6. **Memory 記錄** — Git-based 學習記錄
7. **CP6: 專案健檢** — 每 5 次迭代檢查

## 使用範例

```bash
# 基本使用
/evolve 建立一個 ComfyUI 工作流程

# 探索模式
/evolve --explore 優化這段程式碼

# 建立新 Skill
/evolve --new-skill "git commit helper"
```

## 詳細文件

參見 `skills/SKILL.md` 和各模組目錄。
