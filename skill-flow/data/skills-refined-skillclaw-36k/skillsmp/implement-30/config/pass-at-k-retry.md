# pass@k 重試機制

> implement skill 的失敗重試與成功率計算

## pass@k 概述

### 什麼是 pass@k

pass@k 是衡量程式碼生成成功率的指標：

- **pass@1**: 一次嘗試的成功率
- **pass@3**: 三次嘗試內的成功率
- **pass@k**: k 次嘗試內的成功率

### 計算公式

```
pass@k = 1 - C(n-c, k) / C(n, k)

其中：
  n = 總嘗試次數
  c = 成功次數
  k = 目標嘗試次數
  C(a, b) = 組合數
```

### 範例

```
場景：嘗試 5 次，成功 3 次

pass@1 = 3/5 = 60%
pass@3 = 1 - C(2,3)/C(5,3) = 1 - 0/10 = 100%

解釋：雖然單次成功率只有 60%，但 3 次內成功的機率是 100%
```

## 預設配置

```yaml
pass_at_k:
  k: 3                        # 預設最多嘗試 3 次
  target_threshold: 0.9       # 目標 90% 成功率

  per_attempt:
    timeout: 300s             # 每次嘗試最長 5 分鐘
    include_tests: true       # 包含測試執行

  on_failure:
    analyze: true             # 分析失敗原因
    adjust_approach: true     # 調整方法
    log_attempt: true         # 記錄嘗試
```

## 重試流程

### 嘗試循環

```
┌─────────────────────────────────────────────────────────────┐
│                     pass@k 重試循環                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  嘗試 1                                                      │
│  ┌────────────────┐                                          │
│  │ 實作 + 測試    │ ──► 成功 ──► 完成 ✅                     │
│  └────────────────┘                                          │
│         │                                                    │
│         ▼ 失敗                                               │
│  ┌────────────────┐                                          │
│  │ 分析錯誤       │                                          │
│  │ 調整方法       │                                          │
│  └────────────────┘                                          │
│         │                                                    │
│         ▼                                                    │
│  嘗試 2                                                      │
│  ┌────────────────┐                                          │
│  │ 修正 + 重試    │ ──► 成功 ──► 完成 ✅                     │
│  └────────────────┘                                          │
│         │                                                    │
│         ▼ 失敗                                               │
│  ┌────────────────┐                                          │
│  │ 深度分析       │                                          │
│  │ 變換策略       │                                          │
│  └────────────────┘                                          │
│         │                                                    │
│         ▼                                                    │
│  嘗試 3                                                      │
│  ┌────────────────┐                                          │
│  │ 最終嘗試       │ ──► 成功 ──► 完成 ✅                     │
│  └────────────────┘                                          │
│         │                                                    │
│         ▼ 失敗                                               │
│  ┌────────────────┐                                          │
│  │ 觸發 CP5 驗屍  │ ──► 人工介入                             │
│  └────────────────┘                                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 失敗類型與處理

```yaml
failure_types:
  compilation_error:
    description: "編譯/語法錯誤"
    retry_strategy: fix_syntax
    auto_fixable: true

  test_failure:
    description: "測試失敗"
    retry_strategy: fix_logic
    auto_fixable: partially

  runtime_error:
    description: "運行時錯誤"
    retry_strategy: debug_and_fix
    auto_fixable: partially

  timeout:
    description: "執行超時"
    retry_strategy: optimize_or_simplify
    auto_fixable: false

  integration_error:
    description: "整合失敗"
    retry_strategy: check_dependencies
    auto_fixable: false
```

## 嘗試間的調整

### 嘗試 1 → 嘗試 2

```yaml
attempt_1_to_2:
  analyze:
    - error_message          # 錯誤訊息
    - stack_trace            # 堆疊追蹤
    - test_output            # 測試輸出

  adjustments:
    - fix_direct_error       # 直接修正錯誤
    - add_missing_import     # 添加遺漏的導入
    - correct_type_mismatch  # 修正型別不匹配
```

### 嘗試 2 → 嘗試 3

```yaml
attempt_2_to_3:
  analyze:
    - pattern_of_failures    # 失敗模式
    - common_root_cause      # 共同根因
    - assumption_validation  # 假設驗證

  adjustments:
    - change_approach        # 改變方法
    - simplify_logic         # 簡化邏輯
    - add_defensive_code     # 添加防禦性程式碼
    - consult_documentation  # 查閱文檔
```

### 嘗試 3 失敗

```yaml
attempt_3_failed:
  actions:
    - generate_failure_report  # 生成失敗報告
    - identify_blockers        # 識別阻擋因素
    - suggest_human_review     # 建議人工審查
    - trigger_cp5              # 觸發 CP5 驗屍
```

## 失敗分析

### 分析模板

```markdown
## 嘗試 {n} 失敗分析

### 錯誤摘要
- 類型：{error_type}
- 訊息：{error_message}
- 位置：{location}

### 根因分析
{root_cause_analysis}

### 嘗試修正
{attempted_fixes}

### 下一步建議
{next_step_suggestions}
```

### 累積分析

```yaml
cumulative_analysis:
  track:
    - all_errors             # 所有錯誤
    - fix_attempts           # 修正嘗試
    - what_worked            # 有效方法
    - what_failed            # 無效方法

  at_final_failure:
    - summarize_all_attempts
    - identify_pattern
    - suggest_alternative_approaches
```

## 成功率報告

### pass@k 統計表

```markdown
## pass@k 統計

### 總覽

| 指標 | 值 |
|------|-----|
| 總任務數 | {total_tasks} |
| pass@1 | {pass_at_1}% |
| pass@3 | {pass_at_3}% |
| 平均嘗試次數 | {avg_attempts} |

### 任務明細

| 任務 | 嘗試次數 | 結果 | 失敗類型（如有） |
|------|----------|------|------------------|
| {task_1} | {attempts} | {result} | {failure_type} |
| {task_2} | {attempts} | {result} | {failure_type} |

### 失敗分布

| 失敗類型 | 次數 | 佔比 |
|----------|------|------|
| 編譯錯誤 | {n} | {%} |
| 測試失敗 | {n} | {%} |
| 運行時錯誤 | {n} | {%} |
| 超時 | {n} | {%} |
```

## 閾值配置

### 預設閾值

```yaml
thresholds:
  pass_at_1_target: 0.7     # pass@1 目標 70%
  pass_at_3_target: 0.9     # pass@3 目標 90%

  acceptable:
    pass_at_1: 0.5          # pass@1 可接受 50%
    pass_at_3: 0.8          # pass@3 可接受 80%

  warning:
    pass_at_1_below: 0.3    # pass@1 低於 30% 警告
    pass_at_3_below: 0.7    # pass@3 低於 70% 警告
```

### 任務類型調整

```yaml
task_type_adjustments:
  simple:                   # 簡單任務
    k: 2
    threshold: 0.95

  normal:                   # 一般任務
    k: 3
    threshold: 0.9

  complex:                  # 複雜任務
    k: 5
    threshold: 0.8

  experimental:             # 實驗性任務
    k: 10
    threshold: 0.6
```

## Checkpoint 整合

### CP5 驗屍觸發

```yaml
cp5_trigger:
  condition: pass_at_k_failed
  actions:
    - collect_all_attempts
    - generate_failure_report
    - analyze_root_causes
    - document_lessons_learned
    - update_memory
```

### 失敗報告模板

```markdown
## CP5 驗屍報告：{task_name}

### 摘要
- 嘗試次數：{k}
- 全部失敗
- 觸發時間：{timestamp}

### 嘗試歷史

#### 嘗試 1
- 方法：{approach}
- 結果：{result}
- 錯誤：{error}

#### 嘗試 2
...

### 根因分析
{root_cause}

### 教訓
{lessons_learned}

### 建議後續行動
{recommended_actions}
```

## 相關資源

- [監督模式說明](./supervision-mode.md)
- [回饋循環配置](./feedback-loop.md)
- [evolve Checkpoint 整合](../../../shared/integration/evolve-checkpoints.md)
