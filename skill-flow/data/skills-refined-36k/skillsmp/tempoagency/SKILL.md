---
# === Metadata Layer ===
id: "K2"
name: "Tempo→Agency"
category: "temporal-reasoning"
description: "時間制約が主体選択を決定する文脈定理"

triggers:
  - resource allocation decisions
  - self vs environment intervention
  - delegation timing

keywords:
  - tempo
  - agency
  - self-regulation
  - environment-intervention

when_to_use: |
  時間がないとき自己を変えるか環境を変えるかを決める場合。
  例：ストレス下で自分を落ち着かせるか、環境（他者）に働きかけるか。

when_not_to_use: |
  - 主体が既に決まっている場合
  - 時間制約がない場合

version: "2.0"
---

# K2: Tempo → Agency

> **問い**: 時間的制約が主体選択をどう決めるか？
>
> **選択公理**: Tempo (F/S) → Agency (S/E)
>
> **役割**: 時間的プレッシャーに応じて、自己調整か環境介入かを決定

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- 「誰が/何を変えるべきか」という選択が迫られている
- リソース配分（自己投資 vs 環境投資）の判断が必要
- 委任するか自分でやるかの決定が必要

### ✗ Not Trigger
- 主体が既に決定済み
- 時間制約がなく、両方に投資可能

---

## Core Function

**役割:** 期限から「誰が/何を変えるか」を導出する

| 項目 | 内容 |
|------|------|
| **FEP的意味** | 時間制約が制御対象（自己/環境）を制約する |
| **本質** | 「急ぐなら自分を変える、余裕があるなら環境を変える」 |

---

## Processing Logic（フロー図）

```
┌─ 時間制約 T + 主体選択が必要
│
├─ T < 1時間？
│  ├─ ストレス/集中問題？ → K2-FS（即時自己調整）
│  └─ 他者依存タスク？ → K2-FE（即時環境介入）
│
├─ T ≥ 1週間？
│  ├─ スキル習得？ → K2-SS（自己成長戦略）
│  └─ インフラ構築？ → K2-SE（環境構築計画）
│
└─ 中間？
   └─ 状況に応じて K2-FS/FE or K2-SS/SE を選択
```

---

## Matrix

|  | 自己 (S) | 環境 (E) |
|-----|----------|----------|
| **短期 (F)** | K2-FS: 即時自己調整 | K2-FE: 即時環境介入 |
| **長期 (S)** | K2-SS: 自己成長戦略 | K2-SE: 環境構築計画 |

| セル | 意味 | 適用例 |
|------|------|--------|
| **K2-FS** | 時間がない＋自分を変える | ストレス対処、集中回復、気持ち切り替え |
| **K2-FE** | 時間がない＋環境を変える | 緊急の依頼、即時のツール導入 |
| **K2-SS** | 時間がある＋自己成長 | スキル習得、資格取得、習慣形成 |
| **K2-SE** | 時間がある＋環境構築 | チームビルディング、インフラ整備 |

---

## 適用ルール（if-then-else）

```
IF ストレス/集中問題 AND 時間逼迫
  THEN K2-FS（まず自分を落ち着かせる）
ELSE IF 他者依存 AND 時間逼迫
  THEN K2-FE（環境に即時働きかけ）
ELSE IF 長期投資 AND 自己スキル
  THEN K2-SS
ELSE IF 長期投資 AND インフラ
  THEN K2-SE
```

---

## Edge Cases / Failure Modes

### ⚠️ Failure 1: 自己調整で解決できない問題
**症状**: ストレスの原因が環境にあるのに K2-FS を適用  
**対処**: 根本原因を特定し、必要なら K2-SE へ移行

### ⚠️ Failure 2: 環境介入の過信
**症状**: 他者/ツールに依存しすぎて自己成長が停滞  
**対処**: K2-SS でスキル習得を並行

### ⚠️ Failure 3: 両方必要なのに片方だけ
**症状**: 「自己も環境も変える必要がある」のに片方のみ  
**対処**: 短期 K2-FS + 長期 K2-SE の並行戦略

### ✓ Success Pattern
**事例**: 短期的にストレス解消 (K2-FS) → 長期的にチーム改善 (K2-SE)

### ⚠️ Failure 4: 時間見積もり誤り
**症状**: 「自己成長に1ヶ月」と見積もり → 実際は3ヶ月  
**対処**: +50% バッファで計画

---

## Test Cases（代表例）

### Test 1: 集中できない（短期）
**Input**: T=30min, 問題=「集中が切れた」  
**Expected**: K2-FS（深呼吸、休憩）  
**Actual**: ✓ 5分休憩で回復

### Test 2: チーム生産性向上（長期）
**Input**: T=3months, 問題=「チームの生産性」  
**Expected**: K2-SE（プロセス改善、ツール導入）  
**Actual**: ✓ CI/CD パイプライン構築

### Test 3: 新スキル習得
**Input**: T=6months, 問題=「キャリアアップ」  
**Expected**: K2-SS（資格取得、学習）  
**Actual**: ✓ 計画的な学習スケジュール

---

## Configuration

```yaml
default_time_buffer: 1.5    # 自己成長は +50% バッファ
self_priority_threshold: 1  # 1時間以内は自己優先
default_selection: K2-SS    # 不明時は自己成長
```

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **Precondition** | K1 (Tempo→Stratum) | 時間軸を共有 |
| **Postcondition** | T4 Phronēsis | 戦略設計に反映 |
| **対称関係** | K7 (Agency→Tempo) | 逆方向の定理 |

---

*参照: [kairos.md](../../../kernel/kairos.md)*  
*バージョン: 2.0 (2026-01-25)*
