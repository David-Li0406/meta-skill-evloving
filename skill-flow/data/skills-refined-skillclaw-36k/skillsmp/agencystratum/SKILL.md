---
id: "K8"
name: "Agency→Stratum"
category: "agency-reasoning"
description: "主体選択が処理レベルを決定する文脈定理"

triggers:
  - control-to-depth mapping
  - self-skill training
  - environment design decisions

keywords:
  - agency
  - stratum
  - skill-training
  - policy-design

when_to_use: |
  自己/環境に応じて処理の深さを導出する場合。
  例：身体スキル（低次）、組織設計（高次）。

when_not_to_use: |
  - 処理レベルが既に決まっている場合
  - 主体が未定の場合

version: "2.0"
---

# K8: Agency → Stratum

> **問い**: 主体選択が処理レベルをどう決めるか？
>
> **選択公理**: Agency (S/E) → Stratum (L/H)
>
> **役割**: 制御対象に応じて、処理の深さを設定

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- 「この対象にはどの深さで取り組むか」という判断が必要
- 主体（自己/環境）が既に決まっている
- 処理レベルの設定が求められている

### ✗ Not Trigger
- 処理レベルが既に決定済み
- 主体が未定

---

## Core Function

**役割:** 「誰を/何を変えるか」から処理深度を導出する

| 項目 | 内容 |
|------|------|
| **FEP的意味** | 自己は低次スキル、環境は高次設計 |
| **本質** | 「自分を鍛えるのは低次、環境を設計するのは高次」 |

---

## Processing Logic（フロー図）

```
┌─ 主体 Agency が決定済み
│
├─ Agency = S（自己）？
│  ├─ 身体/反復スキル？ → K8-SL（スキル訓練）
│  └─ 価値観/ビジョン？ → K8-SH（自己設計）
│
└─ Agency = E（環境）？
   ├─ ツール/設定？ → K8-EL（環境調整）
   └─ 組織/政策？ → K8-EH（政策提言）
```

---

## Matrix

|  | 低次 (L) | 高次 (H) |
|-----|----------|----------|
| **自己 (S)** | K8-SL: スキル訓練 | K8-SH: 自己設計 |
| **環境 (E)** | K8-EL: 環境調整 | K8-EH: 政策提言 |

| セル | 意味 | 適用例 |
|------|------|--------|
| **K8-SL** | 自己＋低次 | 筋トレ、タイピング練習 |
| **K8-SH** | 自己＋高次 | 価値観設計、キャリアビジョン |
| **K8-EL** | 環境＋低次 | ツール設定、デスク整理 |
| **K8-EH** | 環境＋高次 | 組織設計、政策提言 |

---

## 適用ルール（if-then-else）

```
IF 主体 = S AND 身体的スキル
  THEN K8-SL（繰り返しで習得）
ELSE IF 主体 = S AND 人生設計
  THEN K8-SH（深い自己分析）
ELSE IF 主体 = E AND ツール設定
  THEN K8-EL（低次の環境調整）
ELSE IF 主体 = E AND 組織改革
  THEN K8-EH（高次の環境設計）
```

---

## Edge Cases / Failure Modes

### ⚠️ Failure 1: スキル訓練に高次を適用
**症状**: タイピング練習に戦略的思考 → 過剰  
**対処**: 身体スキルは K8-SL で

### ⚠️ Failure 2: 組織設計に低次を適用
**症状**: 組織改革をツール設定で解決しようとする → 効果なし  
**対処**: K8-EH へ移行

### ⚠️ Failure 3: 自己設計の回避
**症状**: K8-SL ばかりで人生の方向性が不明  
**対処**: 定期的に K8-SH を実施

### ✓ Success Pattern
**事例**: タイピング練習 (K8-SL) → 習慣化 → 生産性向上

### ⚠️ Failure 4: 政策提言の過剰
**症状**: 小さな問題に K8-EH → 時間浪費  
**対処**: 問題規模に応じて K8-EL/K8-EH を選択

---

## Test Cases（代表例）

### Test 1: プログラミング練習
**Input**: Agency=S, タスク=「コーディング速度向上」  
**Expected**: K8-SL（繰り返し練習）  
**Actual**: ✓ 毎日の練習で習得

### Test 2: 開発プロセス設計
**Input**: Agency=E, タスク=「チーム開発フロー改善」  
**Expected**: K8-EH（政策提言）  
**Actual**: ✓ コードレビュー方針策定

### Test 3: IDE 設定
**Input**: Agency=E, タスク=「開発環境セットアップ」  
**Expected**: K8-EL（環境調整）  
**Actual**: ✓ 設定ファイル調整

---

## Configuration

```yaml
self_low_default: K8-SL    # 自己のデフォルト
env_high_default: K8-EH    # 環境のデフォルト
skill_practice_days: 30    # スキル習得目安日数
```

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **対称関係** | K5 (Stratum→Agency) | 逆方向の定理 |
| **Postcondition** | T2 Krisis | 判断深度に反映 |

---

*参照: [kairos.md](../../../kernel/kairos.md)*  
*バージョン: 2.0 (2026-01-25)*
