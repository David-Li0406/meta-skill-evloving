# Synthesis Rules

> plan skill 專屬的共識設計規則

## 概述

plan skill 的 REDUCE 階段需要將 4 個視角的規劃建議整合為一份統一的實作計劃。

此文件定義 plan 專屬的合成規則，基礎規則參見 [shared/synthesis/](../../../shared/synthesis/)。

## 設計共識規則

### 共識分類

| 類型 | 說明 | 處理 |
|------|------|------|
| **強共識** | ≥3 視角同意 | 直接採納 |
| **弱共識** | 2 視角同意 | 標記為建議 |
| **分歧** | 各視角意見不同 | 觸發矛盾解決 |

### 強共識標準

```yaml
strong_consensus:
  min_agreement: 0.75  # 至少 75% 視角同意
  confidence: "★★★★"
  action: "直接採納"
```

### 弱共識標準

```yaml
weak_consensus:
  min_agreement: 0.5   # 50% 視角同意
  confidence: "★★★"
  action: "標記為建議，需進一步驗證"
```

## 設計決策優先順序

當視角建議衝突時，按以下優先順序決策：

### 1. 技術可行性優先

```
architect 意見 > risk-analyst 警告 > 其他
```

如果架構師認為技術上不可行，即使其他視角建議也不採納。

### 2. 風險阻擋

```
if risk-analyst.severity == "Critical":
    必須有緩解策略才能採納
```

### 3. 估算合理性

```
if estimator.concern == "時程不合理":
    需要調整範圍或里程碑
```

### 4. 體驗底線

```
if ux-advocate.rating < "可接受":
    需要改進設計
```

## 矛盾解決策略

### 技術 vs 風險

```yaml
conflict: architect vs risk-analyst
resolution:
  - 採用分階段實施
  - 先實現低風險核心
  - 高風險功能後續迭代
```

### 時程 vs 功能

```yaml
conflict: estimator vs others
resolution:
  - 減少 MVP 範圍
  - 優先核心功能
  - 延後非必要功能
```

### 體驗 vs 技術

```yaml
conflict: ux-advocate vs architect
resolution:
  - 尋找平衡方案
  - 技術限制下的最佳體驗
  - 記錄未來改進項
```

## 輸出整合規則

### implementation-plan.md 結構

```markdown
# 實作計劃：{feature}

## 概述
{從 overview 合成}

## 技術設計
{從 architect 視角提取}

## 風險與緩解
{從 risk-analyst 視角提取}

## 里程碑
{從 estimator 視角提取}

## 體驗設計
{從 ux-advocate 視角提取}

## 待決事項
{未解決的矛盾和待確認項}
```

### 信心指標

每個設計決策標記信心度：

| 符號 | 信心度 | 說明 |
|------|--------|------|
| ★★★★ | 高 | 強共識，可直接執行 |
| ★★★ | 中 | 弱共識，建議驗證 |
| ★★ | 低 | 有分歧，需討論 |
| ★ | 待定 | 需進一步研究 |

## 視角權重配置

可根據專案類型調整視角權重：

### 技術導向

```yaml
weights:
  architect: 1.5
  risk-analyst: 1.2
  estimator: 1.0
  ux-advocate: 0.8
```

### 產品導向

```yaml
weights:
  architect: 1.0
  risk-analyst: 1.0
  estimator: 1.0
  ux-advocate: 1.5
```

### 快速交付

```yaml
weights:
  architect: 1.0
  risk-analyst: 0.8
  estimator: 1.5
  ux-advocate: 1.0
```

## 共用模組參考

- 交叉驗證詳細規則：[shared/synthesis/cross-validation.md](../../../shared/synthesis/cross-validation.md)
- 矛盾解決策略：[shared/synthesis/conflict-resolution.md](../../../shared/synthesis/conflict-resolution.md)
