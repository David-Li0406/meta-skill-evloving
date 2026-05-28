# 04-emergence

> 涌現機制：跨領域連結、知識蒸餾、自動路由

## 本模組包含

| 文件 | 用途 | 建議閱讀順序 |
|------|------|-------------|
| [emergence-levels.md](./_base/emergence-levels.md) | 4 級涌現等級定義 | 1️⃣ |
| [multi-stage-routing.md](./_base/multi-stage-routing.md) | 信心度路由決策 | 2️⃣ |
| [skill-metrics.md](./_base/skill-metrics.md) | 技能效果追蹤 | 3️⃣ |
| [knowledge-distillation.md](./_base/knowledge-distillation.md) | 經驗蒸餾為 Skill | 4️⃣ |

## 涌現等級

| Level | 名稱 | 觸發 |
|-------|------|------|
| 0 | 基礎 | 預設 |
| 1 | 探索 | `--explore` |
| 2 | 涌現 | `--emergence` |
| 3 | 自主 | `--autonomous` |

## 觸發涌現

```bash
# 探索模式
/evolve [目標] --explore

# 涌現模式
/evolve [目標] --emergence --max-iterations 10
```

## 社群貢獻

