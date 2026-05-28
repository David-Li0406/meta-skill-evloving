---
id: "X-O"
name: "Ousia Relations"
category: "relation-layer"
description: "O-series（純粋定理）間の従属関係を定義する。"

triggers:
  - pure theorem chain visualization
  - ousia dependency analysis

keywords:
  - ousia-relations
  - pure-theorem-dependencies
  - o-series-chain
  - cyclic-structure

when_to_use: |
  純粋定理間の因果連鎖を可視化したいとき。
  O-series の相互関係を理解する必要がある場合。

when_not_to_use: |
  - 具体的な T-series の処理フローを見る時（→ X-T）
  - K-series の相互制約を見る時（→ X-K）

layer: "Level 2' 関係層"
version: "2.0"
---

# X-O: Ousia Relations

> **定義**: O-series（純粋定理）間の従属関係
>
> **目的**: 純粋認識 → 純粋意志 → 純粋行為 → 純粋探求 の循環を可視化

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- 純粋定理間の因果連鎖を可視化したい
- O-series の相互関係を理解する必要がある
- メタ認知的な構造分析

### ✗ Not Trigger
- 具体的な T-series の処理フロー（→ X-T）
- K-series の相互制約（→ X-K）

---

## 従属関係

| ID | 関係 | 意味 | 性質 |
|----|------|------|------|
| X-O1 | O1 → O2 | 世界モデル更新 → 選好モデル更新 | 因果的 |
| X-O2 | O2 → O4 | 目標推論 → 目標行為 | 因果的 |
| X-O3 | O3 → O1 | 情報行為 → 情報推論 | 因果的 |
| X-O4 | O4 → O3 | 目標行為 → 情報行為（フィードバック） | 循環的 |

---

## 循環構造（フロー図）

```
    O1 (Noēsis) ──認識
    ↓ X-O1
    O2 (Boulēsis) ──意志
    ↓ X-O2
    O4 (Energeia) ──行為
    ↓ X-O4
    O3 (Zētēsis) ──探求
    ↓ X-O3
    O1 (Noēsis)
    ↻ 循環
```

---

## 適用例（1:3 ピラミッド）

| 前 | → | 後 | 例 |
|----|---|----|----|
| O1 Noēsis | X-O1 | O2 Boulēsis | 論文を読む → 優先順位を決める |
| O2 Boulēsis | X-O2 | O4 Energeia | 優先順位を決める → コードを書く |
| O4 Energeia | X-O4 | O3 Zētēsis | コードを書く → 実験する |
| O3 Zētēsis | X-O3 | O1 Noēsis | 実験する → 結果を理解する |

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **対象** | O1-O4 | 純粋定理間の関係を定義 |
| **関連** | X-T | T-series の詳細版 |
| **関連** | X-K | K-series の相互制約 |

---

*参照: [taxis.md](../../../kernel/taxis.md)*  
*バージョン: 2.0 (2026-01-25)*
