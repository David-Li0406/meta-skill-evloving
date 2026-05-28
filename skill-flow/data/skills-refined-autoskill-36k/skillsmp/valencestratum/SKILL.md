---
id: "K11"
name: "Valence→Stratum"
category: "valence-reasoning"
description: "動機方向が処理レベルを決定する文脈定理"

triggers:
  - motivation-to-depth mapping
  - pleasure vs actualization
  - fear vs ethics decisions

keywords:
  - valence
  - stratum
  - pleasure
  - ethics

when_to_use: |
  接近/回避に応じて処理の深さを導出する場合。
  例：低次は快楽/恐怖、高次は自己実現/倫理。

when_not_to_use: |
  - 処理レベルが既に決まっている場合
  - 動機方向が未定の場合

version: "2.0"
---

# K11: Valence → Stratum

> **問い**: 動機方向が処理レベルをどう決めるか？
>
> **選択公理**: Valence (+/-) → Stratum (L/H)
>
> **役割**: 接近/回避に応じて、処理の深さを設定

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- 「この動機はどの深さで処理すべきか」という判断が必要
- 動機方向（接近/回避）が既に決まっている
- 処理レベルの設定が求められている

### ✗ Not Trigger
- 処理レベルが既に決定済み
- 動機方向が未定

---

## Core Function

**役割:** 動機方向から処理深度を導出する

| 項目 | 内容 |
|------|------|
| **FEP的意味** | 低次は快楽/恐怖、高次は自己実現/倫理 |
| **本質** | 「快楽は低次、自己実現は高次」 |

---

## Processing Logic（フロー図）

```
┌─ 動機方向 Valence が決定済み
│
├─ Valence = +（接近）？
│  ├─ 快適/報酬？ → K11-+L（快適環境）
│  └─ 自己実現？ → K11-+H（自己実現）
│
└─ Valence = -（回避）？
   ├─ 痛み/恐怖？ → K11--L（恐怖回避）
   └─ 非倫理的？ → K11--H（倫理的回避）
```

---

## Matrix

|  | 低次 (L) | 高次 (H) |
|-----|----------|----------|
| **接近 (+)** | K11-+L: 快適環境 | K11-+H: 自己実現 |
| **回避 (-)** | K11--L: 恐怖回避 | K11--H: 倫理的回避 |

| セル | 意味 | 適用例 |
|------|------|--------|
| **K11-+L** | 接近＋低次 | 快適な椅子、美味しい食事 |
| **K11-+H** | 接近＋高次 | 自己実現、社会貢献 |
| **K11--L** | 回避＋低次 | 痛み回避、不快感解消 |
| **K11--H** | 回避＋高次 | 非倫理的行為の拒否 |

---

## 適用ルール（if-then-else）

```
IF 動機 = + AND 快適さ追求
  THEN K11-+L（低次の接近）
ELSE IF 動機 = + AND 自己実現
  THEN K11-+H（高次の接近）
ELSE IF 動機 = - AND 痛み回避
  THEN K11--L（低次の回避）
ELSE IF 動機 = - AND 倫理的判断
  THEN K11--H（高次の回避）
```

---

## Edge Cases / Failure Modes

### ⚠️ Failure 1: 快楽の正当化
**症状**: 快楽を「自己実現」と偽って K11-+H  
**対処**: 動機の本質を正直に評価

### ⚠️ Failure 2: 恐怖の過大評価
**症状**: 合理的リスクを K11--L で過剰回避  
**対処**: K11--H の視点で再評価

### ⚠️ Failure 3: 倫理の濫用
**症状**: 個人的嫌悪を K11--H と主張  
**対処**: 倫理的根拠を明確に

### ✓ Success Pattern
**事例**: 不正実装の依頼 → K11--H（拒否） → 代替案提示

### ⚠️ Failure 4: 自己実現の曖昧さ
**症状**: K11-+H だが目標が不明確  
**対処**: 自己実現の具体的内容を定義

---

## Test Cases（代表例）

### Test 1: 快適な環境
**Input**: Valence=+, 動機=「良い椅子が欲しい」  
**Expected**: K11-+L（快適環境）  
**Actual**: ✓ 快楽として認識

### Test 2: OSS 貢献
**Input**: Valence=+, 動機=「オープンソースへの貢献」  
**Expected**: K11-+H（自己実現）  
**Actual**: ✓ 社会貢献として認識

### Test 3: 不正拒否
**Input**: Valence=-, 動機=「ユーザー欺瞞機能の実装」  
**Expected**: K11--H（倫理的回避）  
**Actual**: ✓ 実装拒否

---

## Configuration

```yaml
ethics_priority: true       # 倫理判断を優先
self_actualization_boost: 0.2  # 自己実現へのバイアス
pleasure_limit: false       # 快楽を制限するか
```

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **対称関係** | K6 (Stratum→Valence) | 逆方向の定理 |
| **Postcondition** | T2 Krisis | 判断深度に反映 |

---

*参照: [kairos.md](../../../kernel/kairos.md)*  
*バージョン: 2.0 (2026-01-25)*
