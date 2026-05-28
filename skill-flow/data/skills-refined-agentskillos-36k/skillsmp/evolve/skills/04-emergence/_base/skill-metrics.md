# 技能效果記分板 (Skill Metrics)

> 追蹤各 skill 的使用效果，為未來決策提供數據

## 目錄結構

```
.claude/memory/skill-metrics/
├── index.md              # 總覽
├── by-task-type/         # 按任務類型
│   ├── code-generation.md
│   └── debugging.md
└── by-skill/             # 按 skill
    ├── quant-trading.md
    └── comfyui.md
```

## 指標定義

| 指標 | 說明 | 計算方式 |
|------|------|----------|
| **使用次數** | skill 被載入的總次數 | count |
| **成功率** | 任務成功的比例 | success / total |
| **平均迭代** | 完成任務平均所需迭代 | sum(iterations) / count |
| **推薦度** | 綜合評分 | weighted score |

## 記錄格式

```yaml
# .claude/memory/skill-metrics/by-skill/quant-trading.md
skill: quant-trading
last_updated: 2026-01-11

stats:
  total_uses: 15
  successes: 12
  failures: 3
  success_rate: 80%
  avg_iterations: 4.2

by_task_type:
  backtesting:
    uses: 8
    success_rate: 87.5%
  strategy_development:
    uses: 5
    success_rate: 80%
  risk_analysis:
    uses: 2
    success_rate: 50%

notes:
  - "對於簡單回測任務效果最好"
  - "風險分析需要額外的 finance 知識"
```

## 使用場景

### 1. Skill 選擇優化

```python
# 當有多個 skill 可選時，參考歷史數據
if task_type == "backtesting":
    # 檢查 skill-metrics
    # quant-trading: 87.5% success
    # finance-analysis: 60% success
    preferred_skill = "quant-trading"
```

### 2. 策略調整

```python
# 當某 skill 在特定任務類型失敗率高時
if skill_metrics[skill][task_type].success_rate < 50%:
    # 考慮替代方案或降級策略
    suggest_alternative_approach()
```

### 3. 涌現觸發

```python
# 當 skill 組合表現異常好時
if combined_success_rate > individual_average:
    record_emergence("skill-synergy", [skill_a, skill_b])
```
