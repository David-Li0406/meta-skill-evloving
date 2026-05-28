---
id: "O2"
name: "Boulēsis"
category: "pure-theorem"
description: "純粋意志 (I-P)。Flow×Value のみの最も抽象的な意志機能。"

triggers:
  - goal clarification
  - what-do-we-want inquiry
  - value alignment check

keywords:
  - will
  - intention
  - desire
  - goal
  - pragmatic

when_to_use: |
  「何を達成したいか」を問う時、目標の本質を確認する時。
  意志の純粋形式を問う場合。

when_not_to_use: |
  - 具体的な判断が必要な時（→ T-series）
  - 通常は拡張定理（T2, T4）を通じて具体化

fep_code: "I-P"
layer: "Level 2a 純粋定理"
version: "2.0"
---

# O2: Boulēsis (βούλησις) — 純粋意志

> **FEP Code:** I-P (Inference × Pragmatic)
>
> **問い**: 何を達成したいか？何を望むか？
>
> **役割**: 「望む」こと自体を認識する

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- 「何を達成したいか」という問い
- 目標の本質を確認する必要
- 価値観・意図の確認
- 意志のメタ分析

### ✗ Not Trigger
- 具体的な優先判断（→ T2 Krisis）
- 戦略設計（→ T4 Phronēsis）
- 通常のタスク実行

> **注**: 純粋定理は抽象的であり、通常は拡張定理（T2, T4）を通じて具体化される。

---

## Core Function

**役割:** 「望む」こと自体を認識する

| 項目 | 内容 |
|------|------|
| **FEP役割** | 意志の認識（メタ意志） |
| **本質** | 目標を持つことの純粋形式 |
| **抽象度** | 最高（Tempo軸なし） |

---

## Processing Logic（フロー図）

```
┌─ 意志的問いを検出
│
├─ Phase 1: 入力解析
│  └─ 問いの本質を抽出
│
├─ Phase 2: 目標境界確認
│  ├─ 明示的目標を列挙
│  └─ 暗黙的目標を推定
│
├─ Phase 3: 具体化判断
│  ├─ 即時判断が必要？ → T2 Krisis (+ Fast)
│  └─ 戦略設計が必要？ → T4 Phronēsis (+ Slow)
│
└─ Phase 4: 出力
   └─ 目標リスト + 具体化先
```

---

## 拡張定理との関係

| 純粋定理 | → 拡張定理 | 追加軸 | 役割 |
|----------|-----------|--------|------|
| O2 Boulēsis | T2 Krisis | + Fast | 即時優先判断 |
| O2 Boulēsis | T4 Phronēsis | + Slow | 戦略設計 |

---

## Edge Cases / Failure Modes

### ⚠️ Failure 1: 目標不明
**症状**: 「何を望むか」が明確にならない  
**対処**: ユーザーに質問

### ⚠️ Failure 2: 目標矛盾
**症状**: 複数目標が矛盾  
**対処**: 優先順位を確認

### ✓ Success Pattern
**事例**: 「何を達成したい？」→ 目標リスト → T4 へ

---

## Test Cases（代表例）

### Test 1: 目標確認
**Input**: 「このプロジェクトの目的は？」  
**Expected**: 目標リスト  
**Actual**: ✓ 目標抽出

### Test 2: 具体化委譲
**Input**: 「どれを優先すべき？」  
**Expected**: T2 Krisis へ委譲  
**Actual**: ✓ T2 発動

---

## Output Format

```
┌─[Hegemonikón]──────────────────────┐
│ O2 Boulēsis: 意志分析完了          │
│ 明示目標: [目標リスト]             │
│ 暗黙目標: [推定目標リスト]         │
│ 具体化: → T2/T4 に委譲             │
└────────────────────────────────────┘
```

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **派生** | T2 Krisis | + Fast 軸 |
| **派生** | T4 Phronēsis | + Slow 軸 |
| **対関係** | O1 Noēsis | 認識 ↔ 意志 |

---

*参照: [ousia.md](../../../kernel/ousia.md)*  
*バージョン: 2.0 (2026-01-25)*
