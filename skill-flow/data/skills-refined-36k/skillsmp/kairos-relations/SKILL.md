---
id: "X-K"
name: "Kairos Relations"
category: "relation-layer"
description: "K-series（文脈定理）間の従属関係を定義する。"

triggers:
  - context theorem symmetry check
  - kairos dependency analysis
  - constraint conflict detection

keywords:
  - kairos-relations
  - context-theorem-dependencies
  - k-series-chain
  - symmetry

when_to_use: |
  文脈定理間の相互制約を可視化したいとき。
  K-series を複数適用する際に矛盾検出する場合。

when_not_to_use: |
  - 純粋定理間の関係を見る時（→ X-O）
  - T-series の処理フローを見る時（→ X-T）

layer: "Level 2' 関係層"
version: "2.0"
---

# X-K: Kairos Relations

> **定義**: K-series（文脈定理）間の従属関係
>
> **目的**: 選択公理間の対称関係を可視化し、矛盾を検出

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- 文脈定理間の相互制約を可視化したい
- K-series を複数適用する際に矛盾検出
- 選択公理の対称性を確認

### ✗ Not Trigger
- 純粋定理間の関係（→ X-O）
- T-series の処理フロー（→ X-T）

---

## 対称関係

K-series 間の従属は「軸の対称性」に基づく。
例: K1 (Tempo→Stratum) と K4 (Stratum→Tempo) は対称的。

| ID | 関係 | 意味 |
|----|------|------|
| X-K1 | K1 ↔ K4 | Tempo→Stratum と Stratum→Tempo の相互制約 |
| X-K2 | K2 ↔ K7 | Tempo→Agency と Agency→Tempo の相互制約 |
| X-K3 | K3 ↔ K10 | Tempo→Valence と Valence→Tempo の相互制約 |
| X-K4 | K5 ↔ K8 | Stratum→Agency と Agency→Stratum の相互制約 |
| X-K5 | K6 ↔ K11 | Stratum→Valence と Valence→Stratum の相互制約 |
| X-K6 | K9 ↔ K12 | Agency→Valence と Valence→Agency の相互制約 |

---

## 対称構造（フロー図）

```
        Tempo
       /     \
   K1/K4   K2/K7  K3/K10
     /         \      \
Stratum ─────── Agency ─── Valence
  K5/K8   K6/K11   K9/K12
```

---

## 制約の性質

| 性質 | 説明 | 例 |
|------|------|-----|
| **相互的** | A↔B が双方向に影響 | 時間制約がレベルを決め、レベルが時間を決める |
| **優先的** | 一方が他方を優先して制約 | 緊急時は Tempo が優先 |
| **文脈的** | 状況によって優先が変わる | 通常時は Stratum が優先 |

---

## 矛盾検出

K-series を複数適用する際、X-K を参照して矛盾を検出：

```
例: K1-FL (即時低次) + K4-HS (長期高次)
  → 矛盾検出（X-K1）
  → 状況に応じてどちらを優先するか決定

解決方法:
1. 時間軸で分離（短期は K1、長期は K4）
2. 優先度を明示（緊急なら K1 優先）
```

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **対象** | K1-K12 | 文脈定理間の関係を定義 |
| **関連** | X-O | O-series の純粋版 |
| **関連** | X-T | T-series の処理フロー |

---

*参照: [taxis.md](../../../kernel/taxis.md)*  
*バージョン: 2.0 (2026-01-25)*
