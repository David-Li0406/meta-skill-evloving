---
id: "O3"
name: "Zētēsis"
category: "pure-theorem"
description: "純粋探求 (A-E)。Flow×Value のみの最も抽象的な探求機能。"

triggers:
  - pure exploration need
  - what-should-we-explore inquiry
  - curiosity-driven questions

keywords:
  - exploration
  - search
  - curiosity
  - discovery
  - epistemic-action

when_to_use: |
  「何を探求すべきか」を問う時、探求の本質を確認する時。
  好奇心駆動の問い。

when_not_to_use: |
  - 具体的な情報収集が必要な時（→ T-series）
  - 通常は拡張定理（T5, T7）を通じて具体化

fep_code: "A-E"
layer: "Level 2a 純粋定理"
version: "2.0"
---

# O3: Zētēsis (ζήτησις) — 純粋探求

> **FEP Code:** A-E (Action × Epistemic)
>
> **問い**: 何を探求すべきか？何を発見すべきか？
>
> **役割**: 「探す」こと自体を認識する

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- 「何を探求すべきか」という問い
- 探求の本質を確認する必要
- 好奇心駆動の問い
- 発見の方向性を決める

### ✗ Not Trigger
- 具体的な情報収集（→ T5 Peira）
- 仮説検証（→ T7 Dokimē）
- 通常のタスク実行

> **注**: 純粋定理は抽象的であり、通常は拡張定理（T5, T7）を通じて具体化される。

---

## Core Function

**役割:** 「探す」こと自体を認識する

| 項目 | 内容 |
|------|------|
| **FEP役割** | 探求の認識（メタ探求） |
| **本質** | 情報を能動的に取得することの純粋形式 |
| **抽象度** | 最高（Tempo軸なし） |

---

## Processing Logic（フロー図）

```
┌─ 探求的問いを検出
│
├─ Phase 1: 入力解析
│  └─ 問いの本質を抽出
│
├─ Phase 2: 探求境界確認
│  ├─ 探求すべき領域を列挙
│  └─ 探求不要な領域を列挙
│
├─ Phase 3: 具体化判断
│  ├─ 情報収集が必要？ → T5 Peira (+ Fast)
│  └─ 仮説検証が必要？ → T7 Dokimē (+ Slow)
│
└─ Phase 4: 出力
   └─ 探求領域リスト + 具体化先
```

---

## 拡張定理との関係

| 純粋定理 | → 拡張定理 | 追加軸 | 役割 |
|----------|-----------|--------|------|
| O3 Zētēsis | T5 Peira | + Fast | 即時情報収集 |
| O3 Zētēsis | T7 Dokimē | + Slow | 仮説検証 |

---

## Edge Cases / Failure Modes

### ⚠️ Failure 1: 無限探求
**症状**: 探求が収束しない  
**対処**: 探求範囲を限定

### ⚠️ Failure 2: 探求過多
**症状**: 探求領域が多すぎる  
**対処**: 優先順位付け

### ✓ Success Pattern
**事例**: 「何を調べるべき？」→ 探求領域リスト → T5 へ

---

## Test Cases（代表例）

### Test 1: 探求方向確認
**Input**: 「何を調べればいい？」  
**Expected**: 探求領域リスト  
**Actual**: ✓ 探求分析

### Test 2: 具体化委譲
**Input**: 「詳しく調べて」  
**Expected**: T5 Peira へ委譲  
**Actual**: ✓ T5 発動

---

## Output Format

```
┌─[Hegemonikón]──────────────────────┐
│ O3 Zētēsis: 探求分析完了           │
│ 探求領域: [領域リスト]             │
│ 優先度: [優先順位]                 │
│ 具体化: → T5/T7 に委譲             │
└────────────────────────────────────┘
```

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **派生** | T5 Peira | + Fast 軸 |
| **派生** | T7 Dokimē | + Slow 軸 |
| **対関係** | O2 Boulēsis | 意志 ↔ 探求 |

---

*参照: [ousia.md](../../../kernel/ousia.md)*  
*バージョン: 2.0 (2026-01-25)*
