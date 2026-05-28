---
id: "K4"
name: "Stratum→Tempo"
category: "abstraction-reasoning"
description: "処理レベルが時間スコープを決定する文脈定理"

triggers:
  - depth-to-time mapping
  - abstraction level decisions
  - processing horizon planning

keywords:
  - stratum
  - tempo
  - abstraction
  - processing-depth

when_to_use: |
  処理の深さから適切な時間枠を導出する場合。
  例：アーキテクチャ設計（高次）には長期が必要。

when_not_to_use: |
  - 時間が既に決まっている場合
  - 処理レベルが固定されている場合

version: "2.0"
---

# K4: Stratum → Tempo

> **問い**: 処理レベルが時間スコープをどう決めるか？
>
> **選択公理**: Stratum (L/H) → Tempo (F/S)
>
> **役割**: 処理の深さに応じて、適切な時間枠を設定

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- 「この処理にはどれくらい時間がかかるか？」という見積もりが必要
- 処理の深さ（低次/高次）が既に決まっている
- 時間枠の設定が求められている

### ✗ Not Trigger
- 時間が既に外部から与えられている（→ K1 を使用）
- 処理レベルが未定

---

## Core Function

**役割:** 処理深度から時間枠を導出する

| 項目 | 内容 |
|------|------|
| **FEP的意味** | 抽象度が高いほど長期的視点が必要 |
| **本質** | 「深く考えるなら時間をかける、表面的なら即時」 |

---

## Processing Logic（フロー図）

```
┌─ 処理レベル Stratum が決定済み
│
├─ Stratum = L（低次）？
│  ├─ 反射的タスク？ → K4-LF（即時反応）
│  └─ 習慣化タスク？ → K4-LS（長期繰り返し）
│
└─ Stratum = H（高次）？
   ├─ 経験者の直感？ → K4-HF（即時抽象判断）
   └─ 戦略的設計？ → K4-HS（長期計画）
```

---

## Matrix

|  | 短期 (F) | 長期 (S) |
|-----|----------|----------|
| **低次 (L)** | K4-LF: 反射的反応 | K4-LS: 習慣化 |
| **高次 (H)** | K4-HF: 直感的判断 | K4-HS: 戦略的計画 |

| セル | 意味 | 適用例 |
|------|------|--------|
| **K4-LF** | 低次＋短期 | 運転中の反射、タイポ修正 |
| **K4-LS** | 低次＋長期 | スキルの習慣化、筋トレ |
| **K4-HF** | 高次＋短期 | 経験に基づく直感判断 |
| **K4-HS** | 高次＋長期 | アーキテクチャ設計、人生計画 |

---

## 適用ルール（if-then-else）

```
IF 処理レベル = L AND 反射的
  THEN K4-LF（考える暇がない）
ELSE IF 処理レベル = L AND 習慣化目的
  THEN K4-LS（繰り返しで定着）
ELSE IF 処理レベル = H AND 経験者
  THEN K4-HF（直感が信頼できる）
ELSE IF 処理レベル = H AND 重要設計
  THEN K4-HS（深い思考に時間が必要）
```

---

## Edge Cases / Failure Modes

### ⚠️ Failure 1: 高次処理に短期を割り当て
**症状**: アーキテクチャ設計を1日で → 設計不良  
**対処**: 高次処理には最低 K4-HS を適用

### ⚠️ Failure 2: 低次処理に長期を割り当て
**症状**: タイポ修正に1週間 → 時間浪費  
**対処**: 低次処理は K4-LF で即時対応

### ⚠️ Failure 3: 直感の過信
**症状**: 未経験なのに K4-HF を適用 → 判断ミス  
**対処**: 経験がなければ K4-HS に移行

### ✓ Success Pattern
**事例**: システム設計（高次）→ K4-HS で2週間確保 → 品質向上

### ⚠️ Failure 4: 習慣化を急ぐ
**症状**: 新習慣を1週間で定着させようとする → 失敗  
**対処**: K4-LS には最低2-3ヶ月を見積もる

---

## Test Cases（代表例）

### Test 1: 運転中の反応
**Input**: Stratum=L, タスク=「急ブレーキ」  
**Expected**: K4-LF（即時反応）  
**Actual**: ✓ 反射的に対応

### Test 2: アーキテクチャ設計
**Input**: Stratum=H, タスク=「マイクロサービス設計」  
**Expected**: K4-HS（長期計画）  
**Actual**: ✓ 2週間の設計期間確保

### Test 3: 習慣形成
**Input**: Stratum=L, タスク=「毎日のコードレビュー」  
**Expected**: K4-LS（長期繰り返し）  
**Actual**: ✓ 3ヶ月で習慣化

---

## Configuration

```yaml
high_stratum_min_days: 7    # 高次処理の最低日数
low_stratum_max_hours: 1    # 低次処理の最大時間
habit_formation_weeks: 12   # 習慣化に必要な週数
```

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **対称関係** | K1 (Tempo→Stratum) | 逆方向の定理 |
| **Postcondition** | T4 Phronēsis | 時間枠設定に反映 |

---

*参照: [kairos.md](../../../kernel/kairos.md)*  
*バージョン: 2.0 (2026-01-25)*
