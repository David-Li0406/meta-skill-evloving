---
id: "K10"
name: "Valence→Tempo"
category: "valence-reasoning"
description: "動機方向が時間スコープを決定する文脈定理"

triggers:
  - motivation-to-time mapping
  - approach-avoid timing
  - reward-risk horizon

keywords:
  - valence
  - tempo
  - approach
  - avoid
  - timing

when_to_use: |
  接近/回避に応じて時間枠を導出する場合。
  例：欲しいものは今すぐ、危険は計画的に避ける。

when_not_to_use: |
  - 時間枠が既に決まっている場合
  - 動機方向が未定の場合

version: "2.0"
---

# K10: Valence → Tempo

> **問い**: 動機方向が時間スコープをどう決めるか？
>
> **選択公理**: Valence (+/-) → Tempo (F/S)
>
> **役割**: 接近/回避に応じて、適切な時間枠を設定

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- 「この動機にはどれくらいの時間枠が適切か」という見積もりが必要
- 動機方向（接近/回避）が既に決まっている
- 時間枠の設定が求められている

### ✗ Not Trigger
- 時間が既に外部から与えられている
- 動機方向が未定

---

## Core Function

**役割:** 動機方向から時間枠を導出する

| 項目 | 内容 |
|------|------|
| **FEP的意味** | 接近は即時、回避は計画的 |
| **本質** | 「欲しいものは今すぐ、危険は計画的に避ける」 |

---

## Processing Logic（フロー図）

```
┌─ 動機方向 Valence が決定済み
│
├─ Valence = +（接近）？
│  ├─ 衝動的？ → K10-+F（即時獲得）
│  └─ 計画的？ → K10-+S（目標計画）
│
└─ Valence = -（回避）？
   ├─ 緊急危険？ → K10--F（即時逃避）
   └─ 予防的？ → K10--S（リスク計画）
```

---

## Matrix

|  | 短期 (F) | 長期 (S) |
|-----|----------|----------|
| **接近 (+)** | K10-+F: 衝動買い | K10-+S: 目標計画 |
| **回避 (-)** | K10--F: 即時逃避 | K10--S: リスク計画 |

| セル | 意味 | 適用例 |
|------|------|--------|
| **K10-+F** | 接近＋短期 | 衝動買い、即時獲得 |
| **K10-+S** | 接近＋長期 | キャリア目標、投資 |
| **K10--F** | 回避＋短期 | 即時逃避、緊急停止 |
| **K10--S** | 回避＋長期 | 保険、リスクヘッジ |

---

## 適用ルール（if-then-else）

```
IF 動機 = + AND 今すぐ欲しい
  THEN K10-+F（接近の即時）
ELSE IF 動機 = + AND キャリア目標
  THEN K10-+S（接近の長期）
ELSE IF 動機 = - AND 危険察知
  THEN K10--F（回避の即時）
ELSE IF 動機 = - AND 保険見直し
  THEN K10--S（回避の長期）
```

---

## Edge Cases / Failure Modes

### ⚠️ Failure 1: 衝動の過剰
**症状**: K10-+F ばかりで計画的行動がない  
**対処**: 重要な接近は K10-+S に移行

### ⚠️ Failure 2: 即時逃避の誤用
**症状**: 小さなリスクに K10--F → 過剰反応  
**対処**: リスク評価を実施、必要なら K10--S

### ⚠️ Failure 3: リスク計画の先送り
**症状**: K10--S を「いつか」と延期  
**対処**: 期限を設定して K10--S を実行

### ✓ Success Pattern
**事例**: セキュリティ脆弱性 → K10--F（即時停止） → K10--S（長期対策）

### ⚠️ Failure 4: 目標の曖昧さ
**症状**: K10-+S だが目標が不明確  
**対処**: 目標を具体化してから時間枠を設定

---

## Test Cases（代表例）

### Test 1: セール品
**Input**: Valence=+, 状況=「限定セール」  
**Expected**: K10-+F（即時獲得）  
**Actual**: ✓ 即時購入

### Test 2: キャリアアップ
**Input**: Valence=+, 状況=「昇進目標」  
**Expected**: K10-+S（目標計画）  
**Actual**: ✓ 2年計画作成

### Test 3: 保険見直し
**Input**: Valence=-, 状況=「リスク対策」  
**Expected**: K10--S（リスク計画）  
**Actual**: ✓ 保険プラン最適化

---

## Configuration

```yaml
default_approach: K10-+S   # 接近のデフォルトは長期
default_avoid: K10--S      # 回避のデフォルトは長期
impulse_cooling_minutes: 30  # 衝動抑制の冷却期間
```

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **対称関係** | K3 (Tempo→Valence) | 逆方向の定理 |
| **Postcondition** | T4 Phronēsis | 時間計画に反映 |

---

*参照: [kairos.md](../../../kernel/kairos.md)*  
*バージョン: 2.0 (2026-01-25)*
