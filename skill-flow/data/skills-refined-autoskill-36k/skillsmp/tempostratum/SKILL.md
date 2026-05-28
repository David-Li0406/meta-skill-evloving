---
# === Metadata Layer ===
id: "K1"
name: "Tempo→Stratum"
category: "temporal-reasoning"
description: "時間制約が処理レベルを決定する文脈定理"

# 早期判定（検証ファースト）
triggers:
  - time-constrained tasks
  - deadline-driven decisions
  - processing-level optimization

keywords:
  - tempo
  - temporal constraint
  - stratum level
  - deadline

when_to_use: |
  タスク実行の時間余裕が処理詳細度を決定する場合。
  例：企画会議（3時間）vs 通常検討（2週間）で同じ問題を異なる深さで分析。

when_not_to_use: |
  - 時間制約のない理論的分析
  - 人員/ツール制約が支配的な場合

version: "2.0"
---

# K1: Tempo → Stratum

> **問い**: なぜ同じ問題でも、締め切りの長さで分析深度が変わるのか？
>
> **選択公理**: Tempo (F/S) → Stratum (L/H)
>
> **役割**: 時間的プレッシャーに応じて、低次処理（直感）か高次処理（熟考）かを決定

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- 「この問題を深掘りしたい気持ちはあるが、時間がない」という緊張関係がある
- 分析レベル（データ集計 vs 因果推論 vs 戦略提案）の選択が迫られている
- 既存の「標準的手順」では時間超過が見込まれている
- 期限が明示的に与えられている

### ✗ Not Trigger
- 時間が十分にあり、品質追求が最優先
- 時間制約は存在するが、人員やツール不足が本質的制約である
- 処理レベルが既に決定済み

---

## Core Function

**役割:** 与えられた時間 T に対し、分析のレイヤー（Stratum）を最適配置する

| 項目 | 内容 |
|------|------|
| **FEP的意味** | 時間制約が情報処理の階層を制約する |
| **本質** | 「急ぐなら考えない、余裕があるなら考える」 |

---

## Processing Logic（フロー図）

```
┌─ 時間制約 T が与えられた
│
├─ T < 1時間？
│  └─ YES → Stratum L-F（即時パターン認識）
│
├─ 1h ≤ T < 24h？
│  └─ YES → Stratum H-F（即時抽象判断）
│
├─ 1日 ≤ T < 1週間？
│  └─ YES → Stratum L-S/H-S（状況次第）
│
└─ T ≥ 1週間？
   └─ YES → Stratum H-S（戦略的思考）
```

---

## Matrix

|  | 低次 (L) | 高次 (H) |
|-----|----------|----------|
| **短期 (F)** | K1-FL: 即時パターン認識 | K1-FH: 即時抽象判断 |
| **長期 (S)** | K1-SL: 習慣形成・技能訓練 | K1-SH: 戦略的思考・計画 |

| セル | 意味 | 適用例 |
|------|------|--------|
| **K1-FL** | 時間がない＋パターンマッチ | バグ修正中の即時判断、緊急対応 |
| **K1-FH** | 時間がない＋抽象判断 | 締切直前の重要決定 |
| **K1-SL** | 時間がある＋繰り返し | スキル習得、習慣化、練習 |
| **K1-SH** | 時間がある＋深い思考 | キャリア計画、アーキテクチャ設計 |

---

## 適用ルール（if-then-else）

```
IF 時間余裕あり AND 問題が戦略的
  THEN Stratum を1段上げる（余裕分を深掘りに使う）
ELSE IF 時間逼迫 AND 意思決定が差し迫っている
  THEN Stratum を1段下げる + 優先項目を明示
ELSE
  THEN Matrix から推奨 Stratum を採択
```

| 条件 | 選択 | 理由 | T-series連携 |
|------|------|------|--------------|
| 期限 < 1h | K1-FL | 考える時間がない | T1→T6 (即実行) |
| 期限 < 24h | K1-FH | 抽象判断は可能 | T2→T6 |
| 期限 1d-7d | K1-SL/SH | 状況による | T2→T4→T6 |
| 期限 > 1week | K1-SH | 戦略的余裕あり | T4→T7 |
| 反復タスク | K1-SL | 習慣化 | T8 |

---

## Edge Cases / Failure Modes

### ⚠️ Failure 1: Stratum 低すぎて誤判断
**症状**: T=8時間だが K1-FL（集計のみ）で判断 → 表面的な見誤り  
**対処**: 最低でも K1-FH（抽象判断）は必須

### ⚠️ Failure 2: 時間見積もり誤り
**症状**: 「1日あれば充分」と思い K1-SH → 実際には 2日要する  
**対処**: 各 Stratum の実作業時間を +30% バッファで見積もる

### ⚠️ Failure 3: Stratum 高すぎて時間超過
**症状**: 野心的に K1-SH を選択 → 締め切りミス  
**対処**: 最初は低め Stratum で開始し、段階的に上昇

### ✓ Success Pattern
**事例**: 戦略会議まで 1 日 → K1-FH で意思決定に必要な根拠を用意  
**後続**: 会議後、1 週間かけて K1-SH で検証・提案へ

### ⚠️ Failure 4: 反復タスクに高次を適用
**症状**: 毎日のルーティンに K1-SH → 時間浪費  
**対処**: 反復タスクは K1-SL で習慣化

---

## Test Cases（代表例）

### Test 1: 企画会議（3時間）
**Input**: T=3h, 問題=「新サービス企画の価値提案」  
**Expected**: K1-FH（即時抽象判断）  
**Actual**: ✓ テーブル形式で市場セグメント化

### Test 2: 長期戦略会議（1週間）
**Input**: T=5days, 問題=「3年中期経営計画」  
**Expected**: K1-SH（戦略的思考）  
**Actual**: ✓ 詳細な財務シミュレーション

### Test 3: 緊急バグ修正
**Input**: T=30min, 問題=「本番障害」  
**Expected**: K1-FL（即時パターン認識）  
**Actual**: ✓ 既知パターンで即時対応

---

## Configuration

```yaml
# K1 の実行パラメータ
default_time_buffer: 1.3    # 見積もり時間に 30% バッファを追加
stratum_levels: 4           # FL, FH, SL, SH
urgent_threshold_hours: 1   # K1-FL への閾値
short_term_threshold_hours: 24  # K1-FH への閾値
default_selection: K1-SH    # 期限不明時のデフォルト
```

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **Precondition** | T1 Aisthēsis | 状況認識結果（期限情報） |
| **Postcondition** | T2 Krisis | 処理レベルを渡す |
| **Postcondition** | T4 Phronēsis | 戦略設計の基準を渡す |
| **対称関係** | K4 (Stratum→Tempo) | 逆方向の定理 |

---

*参照: [kairos.md](../../../kernel/kairos.md)*  
*バージョン: 2.0 (2026-01-25, 構造最適化)*
