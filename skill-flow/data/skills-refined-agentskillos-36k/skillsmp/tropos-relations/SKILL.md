---
id: "X-T"
name: "Tropos Relations"
category: "relation-layer"
description: "T-series（拡張定理）間の従属関係を定義する。"

triggers:
  - extended theorem chain visualization
  - tropos dependency analysis
  - workflow flow design

keywords:
  - tropos-relations
  - extended-theorem-dependencies
  - t-series-chain
  - core-loop

when_to_use: |
  拡張定理間の処理フローを可視化したいとき。
  Workflow 設計時に T-series の連鎖を確認する場合。

when_not_to_use: |
  - 純粋定理間の関係を見る時（→ X-O）
  - K-series の相互制約を見る時（→ X-K）

layer: "Level 2' 関係層"
version: "2.0"
---

# X-T: Tropos Relations

> **定義**: T-series（拡張定理）間の従属関係
>
> **目的**: Core Loop（T1→T2→T6）と Learning Loop（T3, T4, T5, T7, T8）の処理フローを可視化

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- 拡張定理間の処理フローを可視化したい
- Workflow 設計時に T-series の連鎖を確認する
- Core Loop と Learning Loop の関係を理解する

### ✗ Not Trigger
- 純粋定理間の関係（→ X-O）
- K-series の相互制約（→ X-K）

---

## 従属関係

| ID | 関係 | 意味 | 性質 |
|----|------|------|------|
| X-T1 | T1 → T2 | 知覚 → 判断 | 因果的（Core Loop） |
| X-T2 | T2 → T4 | 判断 → 戦略 | 因果的 |
| X-T3 | T3 → T4 | 内省 → 戦略（自己評価が計画を改善） | 促進的 |
| X-T4 | T4 → T6 | 戦略 → 実行 | 因果的（Core Loop） |
| X-T5 | T5 → T3 | 探索 → 内省（新情報で自己更新） | 促進的 |
| X-T6 | T6 → T7 | 実行 → 検証 | 因果的 |
| X-T7 | T7 → T8 | 検証 → 記憶（結果を保存） | 因果的 |
| X-T8 | T8 → T1 | 記憶 → 知覚（過去経験がフィルタリング） | 循環的 |

---

## 処理フロー（フロー図）

```
         T1 (Aisthēsis) ──知覚
         ↓ X-T1
         T2 (Krisis) ──判断
         ↓ X-T2
    ┌────┴────┐
    ↓         ↓
T3 (Theōria)  T4 (Phronēsis) ──戦略
    │         ↓ X-T4
    │    T6 (Praxis) ──実行
    │         ↓ X-T6
    │    T7 (Dokimē) ──検証
    │         ↓ X-T7
    │    T8 (Anamnēsis) ──記憶
    │         ↓ X-T8
    └────────►T1 (循環)
    
    T5 (Peira) → T3 (X-T5)
```

---

## Workflow への適用

| Workflow | 従属関係の活用 | 説明 |
|----------|---------------|------|
| `/boot` | X-T8 | 記憶 → 知覚（過去履歴読み込み） |
| `/plan` | X-T1, X-T2, X-T4 | 知覚→判断→戦略→実行 |
| `/code` | X-T4, X-T6, X-T7 | 戦略→実行→検証 |
| `/rev` | X-T6, X-T7, X-T3 | 実行→検証→内省 |
| `/hist` | X-T7, X-T8 | 検証→記憶 |

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **対象** | T1-T8 | 拡張定理間の関係を定義 |
| **関連** | X-O | O-series の抽象版 |
| **関連** | X-K | K-series の相互制約 |

---

*参照: [taxis.md](../../../kernel/taxis.md)*  
*バージョン: 2.0 (2026-01-25)*
