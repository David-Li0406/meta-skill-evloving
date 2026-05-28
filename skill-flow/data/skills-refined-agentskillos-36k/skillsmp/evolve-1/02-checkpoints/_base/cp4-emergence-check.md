# Checkpoint 4: 涌現檢查 (Optional)

> 迭代完成後，檢查是否有涌現機會

## 觸發時機

- 每次迭代完成後（可選）
- 連續成功 3+ 次後（建議）
- 用戶開啟 `--emergence` 或 `--explore` 模式

## 檢查項目

### 1. 模式識別

是否發現可重用的模式？

```
問自己：
- 這個解決方案適用於其他類似問題嗎？
- 有沒有步驟可以抽象成通用流程？
- 這個 pattern 出現過幾次了？
```

### 2. 跨領域連結

是否發現領域之間的連結？

```
問自己：
- 這個任務涉及哪些領域？
- 這些領域的組合是否創造新價值？
- 有沒有「意料之外」的發現？
```

### 3. 技能蒸餾

是否值得創建新 skill？

```
蒸餾條件：
- 同類型任務成功 5+ 次
- 形成了可複用的流程
- 現有 skill 不完全匹配
```

## 記錄發現

若有值得記錄的涌現，寫入 `.claude/memory/discoveries/`：

```markdown
---
date: YYYY-MM-DD
type: connection | pattern | insight | hypothesis
confidence: high | medium | low
related_skills: [skill-a, skill-b]
---

## 發現
[描述發現的內容]

## 觸發情境
[什麼情況下發現的]

## 潛在應用
[可能的應用方向]
```

## 涌現等級

詳見 [emergence-levels.md](../../04-emergence/_base/emergence-levels.md)
