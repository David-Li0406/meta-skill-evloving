---
id: "K9"
name: "Agency→Valence"
category: "agency-reasoning"
description: "主体選択が動機方向を決定する文脈定理"

triggers:
  - control-to-motivation mapping
  - self-improvement vs environment-change
  - approach-avoid for self/environment

keywords:
  - agency
  - valence
  - self-motivation
  - environment-attitude

when_to_use: |
  自己/環境に対して接近/回避を選ぶ場合。
  例：スキル習得（自己接近）、有害環境からの離脱（環境回避）。

when_not_to_use: |
  - 動機方向が既に明確な場合
  - 主体が未定の場合

version: "2.0"
---

# K9: Agency → Valence

> **問い**: 主体選択が動機方向をどう決めるか？
>
> **選択公理**: Agency (S/E) → Valence (+/-)
>
> **役割**: 制御対象に応じて、接近か回避かを決定

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- 「この対象に近づくか離れるか」という選択が必要
- 主体（自己/環境）が既に決まっている
- 動機方向の決定が求められている

### ✗ Not Trigger
- 動機方向が既に決定済み
- 主体が未定

---

## Core Function

**役割:** 「誰を/何を変えるか」から動機方向を導出する

| 項目 | 内容 |
|------|------|
| **FEP的意味** | 自己/環境それぞれへの接近・回避 |
| **本質** | 「自己を高めるか離れるか、環境を良くするか離れるか」 |

---

## Processing Logic（フロー図）

```
┌─ 主体 Agency が決定済み
│
├─ Agency = S（自己）？
│  ├─ スキル/健康増進？ → K9-S+（スキル習得）
│  └─ 悪習/弱点？ → K9-S-（悪習離脱）
│
└─ Agency = E（環境）？
   ├─ 良い関係/ツール？ → K9-E+（関係構築）
   └─ 有害関係/環境？ → K9-E-（有害関係排除）
```

---

## Matrix

|  | 接近 (+) | 回避 (-) |
|-----|----------|----------|
| **自己 (S)** | K9-S+: スキル習得 | K9-S-: 悪習離脱 |
| **環境 (E)** | K9-E+: 関係構築 | K9-E-: 有害関係排除 |

| セル | 意味 | 適用例 |
|------|------|--------|
| **K9-S+** | 自己＋接近 | 新スキル習得、健康増進 |
| **K9-S-** | 自己＋回避 | 悪い習慣をやめる |
| **K9-E+** | 環境＋接近 | 良い人間関係、良いツール |
| **K9-E-** | 環境＋回避 | 有害な関係・環境から離れる |

---

## 適用ルール（if-then-else）

```
IF 主体 = S AND スキル習得/健康
  THEN K9-S+（自己への接近）
ELSE IF 主体 = S AND 悪習を断つ
  THEN K9-S-（自己からの回避）
ELSE IF 主体 = E AND ネットワーク/ツール
  THEN K9-E+（環境への接近）
ELSE IF 主体 = E AND 有害環境
  THEN K9-E-（環境からの回避）
```

---

## Edge Cases / Failure Modes

### ⚠️ Failure 1: 回避ばかりで成長停滞
**症状**: K9-S- と K9-E- ばかりで新しいことに挑戦しない  
**対処**: 定期的に K9-S+ と K9-E+ を意識的に選択

### ⚠️ Failure 2: 有害環境への固執
**症状**: 明らかに有害なのに K9-E+ を適用  
**対処**: 環境の評価を再実施、必要なら K9-E-

### ⚠️ Failure 3: 自己否定の過剰
**症状**: K9-S- ばかりで自己肯定感低下  
**対処**: K9-S+ でポジティブな自己成長を

### ✓ Success Pattern
**事例**: 健康的な食習慣 (K9-S+) + 有害な依存関係削除 (K9-E-)

### ⚠️ Failure 4: 接近と回避の混同
**症状**: 「離れたい」と言いながら近づく  
**対処**: 行動と意図の整合性を確認

---

## Test Cases（代表例）

### Test 1: 新言語学習
**Input**: Agency=S, 動機=「Rust を学びたい」  
**Expected**: K9-S+（スキル習得）  
**Actual**: ✓ 学習計画作成

### Test 2: レガシー脱却
**Input**: Agency=E, 動機=「古いシステムから移行」  
**Expected**: K9-E-（有害関係排除）  
**Actual**: ✓ マイグレーション計画

### Test 3: 悪習断ち
**Input**: Agency=S, 動機=「夜更かしをやめる」  
**Expected**: K9-S-（悪習離脱）  
**Actual**: ✓ 睡眠習慣改善

---

## Configuration

```yaml
default_self: K9-S+        # 自己のデフォルトは接近
default_env: K9-E+         # 環境のデフォルトは接近
toxic_detection: true      # 有害環境の自動検出
```

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **対称関係** | K12 (Valence→Agency) | 逆方向の定理 |
| **Postcondition** | T2 Krisis | 判断基準に反映 |

---

*参照: [kairos.md](../../../kernel/kairos.md)*  
*バージョン: 2.0 (2026-01-25)*
