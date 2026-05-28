---
# === Metadata Layer ===
id: "K3"
name: "Tempo→Valence"
category: "temporal-reasoning"
description: "時間制約が動機方向を決定する文脈定理"

triggers:
  - risk assessment under time pressure
  - approach vs avoid decisions
  - opportunity vs threat evaluation

keywords:
  - tempo
  - valence
  - approach
  - avoid
  - risk-reward

when_to_use: |
  短期的な接近/回避か、長期的な戦略かを決める場合。
  例：危険察知時に逃げるか、機会発見時に掴むか。

when_not_to_use: |
  - 動機方向が既に明確な場合
  - リスク/リターンの評価が不要な場合

version: "2.0"
---

# K3: Tempo → Valence

> **問い**: 時間的制約が動機方向をどう決めるか？
>
> **選択公理**: Tempo (F/S) → Valence (+/-)
>
> **役割**: 時間的プレッシャーに応じて、接近（獲得）か回避（防御）かを決定

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- 「攻めるか守るか」という選択が迫られている
- リスク vs リターンの評価が必要
- 危険/機会のいずれかが検出された

### ✗ Not Trigger
- 動機方向が既に決定済み
- 時間制約がなく、両方に対応可能

---

## Core Function

**役割:** 期限から「攻めるか守るか」を導出する

| 項目 | 内容 |
|------|------|
| **FEP的意味** | 時間制約が報酬/損失の評価バランスを変える |
| **本質** | 「急ぐとき危険を避ける、余裕があるとき機会を追う」 |

---

## Processing Logic（フロー図）

```
┌─ 時間制約 T + 動機方向の選択が必要
│
├─ 危険検出？
│  ├─ T < 1時間？ → K3-F-（即時回避）
│  └─ T ≥ 1週間？ → K3-S-（リスク計画）
│
├─ 機会検出？
│  ├─ T < 1時間？ → K3-F+（即時獲得）
│  └─ T ≥ 1週間？ → K3-S+（目標追求）
│
└─ 不明？
   └─ K3-S-（安全側）をデフォルト
```

---

## Matrix

|  | 接近 (+) | 回避 (-) |
|-----|----------|----------|
| **短期 (F)** | K3-F+: 即時獲得行動 | K3-F-: 即時回避行動 |
| **長期 (S)** | K3-S+: 目標追求戦略 | K3-S-: リスク排除計画 |

| セル | 意味 | 適用例 |
|------|------|--------|
| **K3-F+** | 時間がない＋獲得 | 機会の即時把握、限定セール |
| **K3-F-** | 時間がない＋回避 | 危険からの即時逃避、損切り |
| **K3-S+** | 時間がある＋獲得 | キャリア目標、投資 |
| **K3-S-** | 時間がある＋回避 | 保険、リスクヘッジ、予防 |

---

## 適用ルール（if-then-else）

```
IF 危険察知 AND 時間逼迫
  THEN K3-F-（逃げる、止める）
ELSE IF 機会発見 AND 時間逼迫
  THEN K3-F+（今すぐ掴む）
ELSE IF 長期目標追求
  THEN K3-S+（計画的に獲得）
ELSE IF リスク対策・予防
  THEN K3-S-（保険、ヘッジ）
ELSE
  THEN K3-S-（安全側をデフォルト）
```

---

## Edge Cases / Failure Modes

### ⚠️ Failure 1: 危険を機会と誤認
**症状**: リスクを見逃して K3-F+ を適用 → 損失  
**対処**: リスク評価を先に実行

### ⚠️ Failure 2: 機会を危険と誤認
**症状**: チャンスを見逃して K3-F- を適用 → 機会損失  
**対処**: 短期と長期で分離（短期回避、長期接近）

### ⚠️ Failure 3: 回避過多
**症状**: 常に K3-S- で成長停滞  
**対処**: 定期的に K3-S+ を意識的に選択

### ✓ Success Pattern
**事例**: セキュリティ脆弱性発見 → K3-F-（即時停止） → K3-S-（長期対策）

### ⚠️ Failure 4: 衝動的な接近
**症状**: 熟考なしに K3-F+ → 後悔  
**対処**: 重要な接近決定は K3-S+ に移行

---

## Test Cases（代表例）

### Test 1: セキュリティ脆弱性
**Input**: T=即時, 問題=「脆弱性発見」  
**Expected**: K3-F-（即時回避）  
**Actual**: ✓ サービス停止、パッチ適用

### Test 2: キャリアアップ
**Input**: T=2years, 問題=「昇進目標」  
**Expected**: K3-S+（目標追求）  
**Actual**: ✓ スキルロードマップ作成

### Test 3: 保険見直し
**Input**: T=1month, 問題=「リスク対策」  
**Expected**: K3-S-（リスク計画）  
**Actual**: ✓ 保険プラン最適化

---

## Configuration

```yaml
default_selection: K3-S-   # 安全側をデフォルト
risk_priority: true        # リスク評価を先に実行
opportunity_threshold: 0.7 # 機会確信度の閾値
```

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **Precondition** | K1 (Tempo→Stratum) | 時間軸を共有 |
| **Postcondition** | T2 Krisis | 優先度判断に反映 |
| **対称関係** | K10 (Valence→Tempo) | 逆方向の定理 |

---

*参照: [kairos.md](../../../kernel/kairos.md)*  
*バージョン: 2.0 (2026-01-25)*
