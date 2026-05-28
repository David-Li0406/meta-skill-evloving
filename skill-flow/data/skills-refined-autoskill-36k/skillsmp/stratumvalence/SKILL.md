---
id: "K6"
name: "Stratum→Valence"
category: "abstraction-reasoning"
description: "処理レベルが動機方向を決定する文脈定理"

triggers:
  - instinct vs ethics decisions
  - level-based motivation
  - pleasure vs actualization

keywords:
  - stratum
  - valence
  - instinct
  - ethics

when_to_use: |
  低次/高次の処理に応じて接近/回避を選ぶ場合。
  例：低次は本能的（快楽/恐怖）、高次は倫理的（自己実現/非倫理回避）。

when_not_to_use: |
  - 動機方向が既に明確な場合
  - 処理レベルが未定の場合

version: "2.0"
---

# K6: Stratum → Valence

> **問い**: 処理レベルが動機方向をどう決めるか？
>
> **選択公理**: Stratum (L/H) → Valence (+/-)
>
> **役割**: 抽象度に応じて、本能的/倫理的な接近・回避を決定

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- 「なぜこれを追求/回避するのか」という動機の分析が必要
- 処理の深さ（低次/高次）が既に決まっている
- 動機の性質（本能的 vs 倫理的）を区別する必要がある

### ✗ Not Trigger
- 動機方向が既に決定済み
- 処理レベルが未定

---

## Core Function

**役割:** 処理深度から「攻めるか守るか」を導出する

| 項目 | 内容 |
|------|------|
| **FEP的意味** | 低次は本能的、高次は倫理的判断 |
| **本質** | 「低次は欲望、高次は価値観」 |

---

## Processing Logic（フロー図）

```
┌─ 処理レベル Stratum が決定済み
│
├─ Stratum = L（低次）？
│  ├─ 快楽追求？ → K6-L+（本能的欲求）
│  └─ 痛み回避？ → K6-L-（本能的回避）
│
└─ Stratum = H（高次）？
   ├─ 自己実現？ → K6-H+（倫理的追求）
   └─ 非倫理回避？ → K6-H-（倫理的忌避）
```

---

## Matrix

|  | 接近 (+) | 回避 (-) |
|-----|----------|----------|
| **低次 (L)** | K6-L+: 本能的欲求 | K6-L-: 本能的回避 |
| **高次 (H)** | K6-H+: 倫理的追求 | K6-H-: 倫理的忌避 |

| セル | 意味 | 適用例 |
|------|------|--------|
| **K6-L+** | 低次＋接近 | 食欲、快楽、即時報酬 |
| **K6-L-** | 低次＋回避 | 痛み回避、恐怖反応 |
| **K6-H+** | 高次＋接近 | 自己実現、社会貢献 |
| **K6-H-** | 高次＋回避 | 非倫理的行為の忌避 |

---

## 適用ルール（if-then-else）

```
IF 処理レベル = L AND 快楽/報酬
  THEN K6-L+（本能的接近）
ELSE IF 処理レベル = L AND 痛み/恐怖
  THEN K6-L-（本能的回避）
ELSE IF 処理レベル = H AND 自己実現/貢献
  THEN K6-H+（高次の価値追求）
ELSE IF 処理レベル = H AND 非倫理的行為
  THEN K6-H-（高次の価値回避）
```

---

## Edge Cases / Failure Modes

### ⚠️ Failure 1: 低次欲求の過剰追求
**症状**: K6-L+ ばかりで自己実現が停滞  
**対処**: 定期的に K6-H+ を意識的に選択

### ⚠️ Failure 2: 高次回避の過剰適用
**症状**: K6-H- で何も行動できない  
**対処**: 「倫理的に問題ない」行動を積極的に K6-H+ へ

### ⚠️ Failure 3: 本能と倫理の混同
**症状**: 快楽を「自己実現」と偽って正当化  
**対処**: 処理レベルを明確に区別

### ✓ Success Pattern
**事例**: 不正行為の依頼 → K6-H-（拒否）→ 代替案提示

### ⚠️ Failure 4: 恐怖反応の過大評価
**症状**: K6-L- で合理的なリスクも回避  
**対処**: K6-H+ の観点で再評価

---

## Test Cases（代表例）

### Test 1: おいしいもの
**Input**: Stratum=L, 動機=「食欲」  
**Expected**: K6-L+（本能的欲求）  
**Actual**: ✓ 快楽として認識

### Test 2: 社会貢献
**Input**: Stratum=H, 動機=「OSS 貢献」  
**Expected**: K6-H+（倫理的追求）  
**Actual**: ✓ 自己実現として認識

### Test 3: 不正拒否
**Input**: Stratum=H, 動機=「ユーザー欺瞞機能」  
**Expected**: K6-H-（倫理的忌避）  
**Actual**: ✓ 実装拒否

---

## Configuration

```yaml
ethics_priority: true       # 倫理判断を優先
low_stratum_limit: false    # 低次欲求を制限するか
self_actualization_boost: 0.2  # 自己実現へのバイアス
```

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **対称関係** | K11 (Valence→Stratum) | 逆方向の定理 |
| **Postcondition** | T2 Krisis | 判断基準に反映 |

---

*参照: [kairos.md](../../../kernel/kairos.md)*  
*バージョン: 2.0 (2026-01-25)*
