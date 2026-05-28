---
id: "K7"
name: "Agency→Tempo"
category: "agency-reasoning"
description: "主体選択が時間スコープを決定する文脈定理"

triggers:
  - control-to-time mapping
  - self-recovery timing
  - environment-building horizon

keywords:
  - agency
  - tempo
  - self-recovery
  - infrastructure

when_to_use: |
  自己/環境に応じて適切な時間枠を導出する場合。
  例：自己回復は短期、インフラ構築は長期。

when_not_to_use: |
  - 時間枠が既に決まっている場合
  - 主体が未定の場合

version: "2.0"
---

# K7: Agency → Tempo

> **問い**: 主体選択が時間スコープをどう決めるか？
>
> **選択公理**: Agency (S/E) → Tempo (F/S)
>
> **役割**: 制御対象に応じて、適切な時間枠を設定

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- 「この対象を変えるにはどれくらいかかるか」という見積もりが必要
- 主体（自己/環境）が既に決まっている
- 時間枠の設定が求められている

### ✗ Not Trigger
- 時間が既に外部から与えられている
- 主体が未定

---

## Core Function

**役割:** 「誰を/何を変えるか」から時間枠を導出する

| 項目 | 内容 |
|------|------|
| **FEP的意味** | 自己変容は早い、環境変容は遅い |
| **本質** | 「自分を変えるのは速い、環境を変えるには時間がかかる」 |

---

## Processing Logic（フロー図）

```
┌─ 主体 Agency が決定済み
│
├─ Agency = S（自己）？
│  ├─ 即時回復？ → K7-SF（休憩、気分転換）
│  └─ 長期成長？ → K7-SS（スキル習得）
│
└─ Agency = E（環境）？
   ├─ 緊急対応？ → K7-EF（ツール調整）
   └─ インフラ構築？ → K7-ES（チームビルディング）
```

---

## Matrix

|  | 短期 (F) | 長期 (S) |
|-----|----------|----------|
| **自己 (S)** | K7-SF: 即時自己回復 | K7-SS: 自己成長 |
| **環境 (E)** | K7-EF: 即時環境対応 | K7-ES: インフラ構築 |

| セル | 意味 | 適用例 |
|------|------|--------|
| **K7-SF** | 自己＋短期 | 休憩、気分転換、集中回復 |
| **K7-SS** | 自己＋長期 | スキル習得、健康管理 |
| **K7-EF** | 環境＋短期 | 緊急のツール調整 |
| **K7-ES** | 環境＋長期 | インフラ構築、チームビルディング |

---

## 適用ルール（if-then-else）

```
IF 主体 = S AND 集中力低下
  THEN K7-SF（自己の即時回復）
ELSE IF 主体 = S AND スキル習得
  THEN K7-SS（長期的な自己投資）
ELSE IF 主体 = E AND ツール不足
  THEN K7-EF（環境の即時対応）
ELSE IF 主体 = E AND インフラ構築
  THEN K7-ES（環境の長期投資）
```

---

## Edge Cases / Failure Modes

### ⚠️ Failure 1: 自己変容を過大評価
**症状**: 「自分を変えれば1日で」→ 実際は1ヶ月  
**対処**: 自己変容も +50% バッファ

### ⚠️ Failure 2: 環境変容を過小評価
**症状**: 「インフラは1週間で」→ 実際は3ヶ月  
**対処**: 環境変容は +100% バッファ

### ⚠️ Failure 3: 即時回復の繰り返し
**症状**: K7-SF ばかりで根本解決しない  
**対処**: 3回連続で K7-SF なら K7-SS へ移行

### ✓ Success Pattern
**事例**: 5分休憩 (K7-SF) → 集中回復 → 生産性向上

### ⚠️ Failure 4: インフラ投資の先送り
**症状**: K7-EF ばかりで技術的負債が蓄積  
**対処**: 定期的に K7-ES を計画

---

## Test Cases（代表例）

### Test 1: 集中力回復
**Input**: Agency=S, タスク=「集中切れ」  
**Expected**: K7-SF（5分休憩）  
**Actual**: ✓ 即時回復

### Test 2: CI/CD 構築
**Input**: Agency=E, タスク=「パイプライン構築」  
**Expected**: K7-ES（2-3ヶ月）  
**Actual**: ✓ 長期計画で実装

### Test 3: ツール設定
**Input**: Agency=E, タスク=「IDE 設定」  
**Expected**: K7-EF（即時）  
**Actual**: ✓ 30分で完了

---

## Configuration

```yaml
self_recovery_max_minutes: 15   # 即時自己回復の最大時間
environment_buffer: 2.0         # 環境変容の時間バッファ
repeated_sf_threshold: 3        # K7-SF 連続回数の閾値
```

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **対称関係** | K2 (Tempo→Agency) | 逆方向の定理 |
| **Postcondition** | T4 Phronēsis | 時間計画に反映 |

---

*参照: [kairos.md](../../../kernel/kairos.md)*  
*バージョン: 2.0 (2026-01-25)*
