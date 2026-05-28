# 知識蒸餾 (Knowledge Distillation)

> 將累積的經驗蒸餾為可重用的 Skill 或 Pattern

## 蒸餾流程

```
成功經驗 (memory/learnings/)
         ↓
模式識別 (多次成功的共同點)
         ↓
蒸餾為:
├─ 新的 SKILL.md (小而深)
│   例: "comfyui-game-assets" skill
│
├─ 既有 skill 的增補
│   - Examples 區塊
│   - Pitfalls 區塊
│   - Checklist 區塊
│
└─ 策略池更新
    - 新策略加入
    - 成功率數據
```

## 蒸餾觸發條件

### 新 Skill 創建

當以下條件滿足時，建議創建新 skill：

| 條件 | 閾值 |
|------|------|
| 同類型任務成功次數 | 5+ 次 |
| 形成可複用模式 | 是 |
| 現有 skill 匹配度 | < 70% |

### 既有 Skill 增補

當以下條件滿足時，增補現有 skill：

| 條件 | 行動 |
|------|------|
| 發現新 pitfall (3+ 次) | 添加 Pitfalls 區塊 |
| 發現更好方法 | 添加 Examples 區塊 |
| 成功率顯著提升 | 更新最佳實踐 |

### 策略池更新

當以下條件滿足時，更新策略池：

| 條件 | 行動 |
|------|------|
| 新策略成功 3+ 次 | 加入策略池 |
| 現有策略成功率下降 | 降低優先級 |
| 發現適用條件需調整 | 更新條件說明 |

## 蒸餾範例

### 從經驗到 Skill

```
經驗 1: ComfyUI + RemBG 生成透明背景成功
經驗 2: ComfyUI + RemBG 批量處理成功
經驗 3: ComfyUI + ControlNet 姿態控制成功
經驗 4: ComfyUI 記憶體洩漏解決方案
經驗 5: ComfyUI 工作流程優化

↓ 蒸餾

新 Skill: comfyui-game-assets
├── 工作流程模板
├── 常見問題解決
├── 效能優化技巧
└── 批量處理指南
```

## SKILL.md 模板

```markdown
---
name: [skill-name]
version: "1.0.0"
description: [一句話描述]
triggers: [觸發詞列表]
keywords: [關鍵字列表]
---

# [Skill 名稱]

## 使用場景
[何時使用這個 skill]

## 核心流程
[主要步驟]

## 最佳實踐
[從經驗中蒸餾的建議]

## 常見陷阱
[失敗經驗中學到的教訓]

## 範例
[具體使用範例]
```
