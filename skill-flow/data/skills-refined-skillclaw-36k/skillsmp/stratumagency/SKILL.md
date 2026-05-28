---
id: "K5"
name: "Stratum→Agency"
category: "abstraction-reasoning"
description: "処理レベルが主体選択を決定する文脈定理"

triggers:
  - level-to-control mapping
  - abstraction-based delegation
  - self vs environment design

keywords:
  - stratum
  - agency
  - abstraction
  - delegation-depth

when_to_use: |
  低次/高次の処理に応じて自己/環境を選ぶ場合。
  例：日常ルーティン（低次）は自己で、組織改革（高次）は環境で。

when_not_to_use: |
  - 主体が既に決まっている場合
  - 処理レベルが未定の場合

version: "2.0"
---

# K5: Stratum → Agency

> **問い**: 処理レベルが主体選択をどう決めるか？
>
> **選択公理**: Stratum (L/H) → Agency (S/E)
>
> **役割**: 抽象度に応じて、自己改善か環境改善かを決定

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- 「自分を変えるか環境を変えるか」という選択が必要
- 処理の深さ（低次/高次）が既に決まっている
- 改善対象の決定が求められている

### ✗ Not Trigger
- 主体が既に決定済み
- 処理レベルが未定（→ K1/K4 を先に）

---

## Core Function

**役割:** 処理深度から「誰が/何を変えるか」を導出する

| 項目 | 内容 |
|------|------|
| **FEP的意味** | 抽象度が高いほど環境への介入が効果的 |
| **本質** | 「低次は自分を変える、高次は環境を変える」 |

---

## Processing Logic（フロー図）

```
┌─ 処理レベル Stratum が決定済み
│
├─ Stratum = L（低次）？
│  ├─ 日常実行？ → K5-LS（ルーティン実行）
│  └─ 環境調整？ → K5-LE（デスク整理等）
│
└─ Stratum = H（高次）？
   ├─ 自己変革？ → K5-HS（価値観見直し）
   └─ 組織変革？ → K5-HE（文化変革）
```

---

## Matrix

|  | 自己 (S) | 環境 (E) |
|-----|----------|----------|
| **低次 (L)** | K5-LS: ルーティン実行 | K5-LE: 環境調整 |
| **高次 (H)** | K5-HS: 自己変革 | K5-HE: 組織改革 |

| セル | 意味 | 適用例 |
|------|------|--------|
| **K5-LS** | 低次＋自己 | 日常ルーティン、習慣実行 |
| **K5-LE** | 低次＋環境 | デスク整理、ツール設定 |
| **K5-HS** | 高次＋自己 | 価値観の見直し、自己変革 |
| **K5-HE** | 高次＋環境 | 組織改革、文化変革 |

---

## 適用ルール（if-then-else）

```
IF 処理レベル = L AND 毎日のルーティン
  THEN K5-LS（自己の習慣として実行）
ELSE IF 処理レベル = L AND 作業環境改善
  THEN K5-LE（物理/デジタル環境を整える）
ELSE IF 処理レベル = H AND 価値観の転換
  THEN K5-HS（深い自己変革）
ELSE IF 処理レベル = H AND 組織・チーム改革
  THEN K5-HE（環境を高次で変える）
```

---

## Edge Cases / Failure Modes

### ⚠️ Failure 1: 高次問題に低次対応
**症状**: 組織文化問題にデスク整理 (K5-LE) → 効果なし  
**対処**: 問題の抽象度を再評価、K5-HE へ

### ⚠️ Failure 2: 低次問題に高次対応
**症状**: ツール設定に組織改革 (K5-HE) → 過剰投資  
**対処**: K5-LE で十分

### ⚠️ Failure 3: 自己変革の回避
**症状**: K5-HE ばかりで自己成長が停滞  
**対処**: 定期的に K5-HS を意識的に選択

### ✓ Success Pattern
**事例**: 朝のルーティン (K5-LS) → 開発プロセス改革 (K5-HE)

### ⚠️ Failure 4: 環境依存
**症状**: 常に環境を変えようとして自己改善しない  
**対処**: K5-LS/K5-HS でバランス

---

## Test Cases（代表例）

### Test 1: 朝のルーティン
**Input**: Stratum=L, タスク=「毎朝のコードレビュー」  
**Expected**: K5-LS（自己の習慣）  
**Actual**: ✓ 習慣として実行

### Test 2: 組織改革
**Input**: Stratum=H, タスク=「開発プロセス変革」  
**Expected**: K5-HE（環境を高次で変える）  
**Actual**: ✓ CI/CD 導入、チーム文化刷新

### Test 3: 価値観見直し
**Input**: Stratum=H, タスク=「キャリアビジョン再構築」  
**Expected**: K5-HS（深い自己変革）  
**Actual**: ✓ 長期的な自己分析

---

## Configuration

```yaml
default_low_stratum: K5-LS  # 低次のデフォルト
default_high_stratum: K5-HE # 高次のデフォルト
self_review_interval_days: 30  # 自己変革レビュー間隔
```

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **対称関係** | K8 (Agency→Stratum) | 逆方向の定理 |
| **Postcondition** | T4 Phronēsis | 戦略設計に反映 |

---

*参照: [kairos.md](../../../kernel/kairos.md)*  
*バージョン: 2.0 (2026-01-25)*
