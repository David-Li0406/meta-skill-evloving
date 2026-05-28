---
id: "O4"
name: "Energeia"
category: "pure-theorem"
description: "純粋行為 (A-P)。Flow×Value のみの最も抽象的な行為機能。"

triggers:
  - action clarification
  - what-should-we-do inquiry
  - pure action questions

keywords:
  - action
  - doing
  - execution
  - pragmatic-action

when_to_use: |
  「何をすべきか」を問う時、行為の本質を確認する時。
  行為の純粋形式を問う場合。

when_not_to_use: |
  - 具体的な実行が必要な時（→ T-series）
  - 通常は拡張定理（T6, T8）を通じて具体化

fep_code: "A-P"
layer: "Level 2a 純粋定理"
version: "2.0"
---

# O4: Energeia (ἐνέργεια) — 純粋行為

> **FEP Code:** A-P (Action × Pragmatic)
>
> **問い**: 何をすべきか？どう行動すべきか？
>
> **役割**: 「行う」こと自体を認識する

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- 「何をすべきか」という問い
- 行為の本質を確認する必要
- 行動の方向性を決める
- 実行のメタ分析

### ✗ Not Trigger
- 具体的な実行（→ T6 Praxis）
- 記録・保存（→ T8 Anamnēsis）
- 通常のタスク実行

> **注**: 純粋定理は抽象的であり、通常は拡張定理（T6, T8）を通じて具体化される。

---

## Core Function

**役割:** 「行う」こと自体を認識する

| 項目 | 内容 |
|------|------|
| **FEP役割** | 行為の認識（メタ行為） |
| **本質** | 環境に働きかけることの純粋形式 |
| **抽象度** | 最高（Tempo軸なし） |

---

## Processing Logic（フロー図）

```
┌─ 行為的問いを検出
│
├─ Phase 1: 入力解析
│  └─ 問いの本質を抽出
│
├─ Phase 2: 行為境界確認
│  ├─ 可能な行為を列挙
│  └─ 不可能・禁止な行為を列挙
│
├─ Phase 3: 具体化判断
│  ├─ 即時実行が必要？ → T6 Praxis (+ Fast)
│  └─ 記録・蓄積が必要？ → T8 Anamnēsis (+ Slow)
│
└─ Phase 4: 出力
   └─ 行為リスト + 具体化先
```

---

## 拡張定理との関係

| 純粋定理 | → 拡張定理 | 追加軸 | 役割 |
|----------|-----------|--------|------|
| O4 Energeia | T6 Praxis | + Fast | 即時実行 |
| O4 Energeia | T8 Anamnēsis | + Slow | 記録・蓄積 |

---

## Edge Cases / Failure Modes

### ⚠️ Failure 1: 行為不明
**症状**: 「何をすべきか」が明確にならない  
**対処**: T2 Krisis に委譲

### ⚠️ Failure 2: 行為矛盾
**症状**: 複数行為が矛盾  
**対処**: 優先順位を確認

### ✓ Success Pattern
**事例**: 「何をすべき？」→ 行為リスト → T6 へ

---

## Test Cases（代表例）

### Test 1: 行為確認
**Input**: 「次に何をすればいい？」  
**Expected**: 行為リスト  
**Actual**: ✓ 行為分析

### Test 2: 具体化委譲
**Input**: 「これを実行して」  
**Expected**: T6 Praxis へ委譲  
**Actual**: ✓ T6 発動

---

## Output Format

```
┌─[Hegemonikón]──────────────────────┐
│ O4 Energeia: 行為分析完了          │
│ 可能な行為: [行為リスト]           │
│ 禁止・不可: [除外リスト]           │
│ 具体化: → T6/T8 に委譲             │
└────────────────────────────────────┘
```

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **派生** | T6 Praxis | + Fast 軸 |
| **派生** | T8 Anamnēsis | + Slow 軸 |
| **対関係** | O1 Noēsis | 認識 ↔ 行為 |

---

*参照: [ousia.md](../../../kernel/ousia.md)*  
*バージョン: 2.0 (2026-01-25)*
