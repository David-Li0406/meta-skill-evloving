---
id: "O1"
name: "Noēsis"
category: "pure-theorem"
description: "純粋認識 (I-E)。Flow×Value のみの最も抽象的な認識機能。"

triggers:
  - meta-cognition questions
  - knowledge boundary check
  - what-do-we-know inquiry

keywords:
  - meta-cognition
  - pure-recognition
  - knowing
  - epistemic
  - awareness

when_to_use: |
  「何を知っているか」を問う時、知識境界の確認時。
  メタ認知が必要な場合。

when_not_to_use: |
  - 具体的な行動が必要な時（→ T-series）
  - 通常は拡張定理（T1, T3）を通じて具体化

fep_code: "I-E"
layer: "Level 2a 純粋定理"
version: "2.0"
---

# O1: Noēsis (νόησις) — 純粋認識

> **FEP Code:** I-E (Inference × Epistemic)
>
> **問い**: 何を知っているか？何を知らないか？
>
> **役割**: 「知る」こと自体を認識する（メタ認知）

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- 「何を知っているか」という問い
- 知識境界の確認が必要
- 既知/未知の識別が必要
- メタ認知的な自己参照

### ✗ Not Trigger
- 具体的な状況認識（→ T1 Aisthēsis）
- 理論構築（→ T3 Theōria）
- 通常のタスク実行

> **注**: 純粋定理は抽象的であり、通常は拡張定理（T1, T3）を通じて具体化される。

---

## Core Function

**役割:** 「知る」こと自体を認識する

| 項目 | 内容 |
|------|------|
| **FEP役割** | 認識の認識（メタ認知） |
| **本質** | 情報を取得することの純粋形式 |
| **抽象度** | 最高（Tempo軸なし） |

---

## Processing Logic（フロー図）

```
┌─ メタ認知的問いを検出
│
├─ Phase 1: 入力解析
│  └─ 問いの本質を抽出
│
├─ Phase 2: 知識境界確認
│  ├─ 既知の項目を列挙
│  └─ 未知の項目を列挙
│
├─ Phase 3: 具体化判断
│  ├─ 即時認識が必要？ → T1 Aisthēsis (+ Fast)
│  └─ 深い理解が必要？ → T3 Theōria (+ Slow)
│
└─ Phase 4: 出力
   └─ 既知/未知リスト + 具体化先
```

---

## 拡張定理との関係

| 純粋定理 | → 拡張定理 | 追加軸 | 役割 |
|----------|-----------|--------|------|
| O1 Noēsis | T1 Aisthēsis | + Fast | 即時状況認識 |
| O1 Noēsis | T3 Theōria | + Slow | 深い理論構築 |

---

## Edge Cases / Failure Modes

### ⚠️ Failure 1: 無限再帰
**症状**: 「知っていることを知っていることを知っている...」  
**対処**: 2段階で停止

### ⚠️ Failure 2: 過度な抽象化
**症状**: 具体的な行動に繋がらない  
**対処**: T-series に委譲

### ✓ Success Pattern
**事例**: 「この問題について何を知っている？」→ 既知/未知リスト → T1 へ

---

## Test Cases（代表例）

### Test 1: 知識境界確認
**Input**: 「このAPIについて何を知っている？」  
**Expected**: 既知/未知リスト  
**Actual**: ✓ メタ認知実行

### Test 2: 具体化委譲
**Input**: 「今の状況を把握して」  
**Expected**: T1 Aisthēsis へ委譲  
**Actual**: ✓ T1 発動

---

## Output Format

```
┌─[Hegemonikón]──────────────────────┐
│ O1 Noēsis: メタ認知完了            │
│ 既知: [既知の項目リスト]           │
│ 未知: [未知の項目リスト]           │
│ 具体化: → T1/T3 に委譲             │
└────────────────────────────────────┘
```

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **派生** | T1 Aisthēsis | + Fast 軸 |
| **派生** | T3 Theōria | + Slow 軸 |
| **対関係** | O4 Energeia | 認識 ↔ 行為 |

---

*参照: [ousia.md](../../../kernel/ousia.md)*  
*バージョン: 2.0 (2026-01-25)*
