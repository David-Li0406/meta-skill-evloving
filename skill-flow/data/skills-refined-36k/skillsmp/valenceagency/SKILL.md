---
id: "K12"
name: "Valence→Agency"
category: "valence-reasoning"
description: "動機方向が主体選択を決定する文脈定理"

triggers:
  - motivation-to-control mapping
  - approach-avoid target selection
  - self vs environment motivation

keywords:
  - valence
  - agency
  - motivation
  - target-selection

when_to_use: |
  接近/回避に応じて自己/環境を選ぶ場合。
  例：学習意欲（自己接近）、有害環境排除（環境回避）。

when_not_to_use: |
  - 主体が既に決まっている場合
  - 動機方向が未定の場合

version: "2.0"
---

# K12: Valence → Agency

> **問い**: 動機方向が主体選択をどう決めるか？
>
> **選択公理**: Valence (+/-) → Agency (S/E)
>
> **役割**: 接近/回避に応じて、自己か環境かを決定

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- 「何に向かうか、何から離れるか」という選択が必要
- 動機方向（接近/回避）が既に決まっている
- 主体の決定が求められている

### ✗ Not Trigger
- 主体が既に決定済み
- 動機方向が未定

---

## Core Function

**役割:** 動機方向から「誰を/何を変えるか」を導出する

| 項目 | 内容 |
|------|------|
| **FEP的意味** | 接近/回避の対象が自己か環境か |
| **本質** | 「何に向かうか、何から離れるか」 |

---

## Processing Logic（フロー図）

```
┌─ 動機方向 Valence が決定済み
│
├─ Valence = +（接近）？
│  ├─ 自己成長？ → K12-+S（学習意欲）
│  └─ 関係構築？ → K12-+E（環境への接近）
│
└─ Valence = -（回避）？
   ├─ 悪習離脱？ → K12--S（自己からの回避）
   └─ 有害排除？ → K12--E（環境からの回避）
```

---

## Matrix

|  | 自己 (S) | 環境 (E) |
|-----|----------|----------|
| **接近 (+)** | K12-+S: 学習意欲 | K12-+E: 関係構築 |
| **回避 (-)** | K12--S: 自己否定 | K12--E: 有害関係排除 |

| セル | 意味 | 適用例 |
|------|------|--------|
| **K12-+S** | 接近＋自己 | 新スキル習得、自己投資 |
| **K12-+E** | 接近＋環境 | 人脈拡大、良い環境づくり |
| **K12--S** | 回避＋自己 | 悪習を断つ、弱点克服 |
| **K12--E** | 回避＋環境 | 有害関係から離れる |

---

## 適用ルール（if-then-else）

```
IF 動機 = + AND 学習意欲
  THEN K12-+S（自己への接近）
ELSE IF 動機 = + AND ネットワーク
  THEN K12-+E（環境への接近）
ELSE IF 動機 = - AND 悪習断ち
  THEN K12--S（自己からの回避）
ELSE IF 動機 = - AND 有害関係
  THEN K12--E（環境からの回避）
```

---

## Edge Cases / Failure Modes

### ⚠️ Failure 1: 自己否定の過剰
**症状**: K12--S ばかりで自己肯定感低下  
**対処**: K12-+S でポジティブな自己成長を

### ⚠️ Failure 2: 有害環境への固執
**症状**: 明らかに有害なのに K12-+E を適用  
**対処**: 環境の評価を再実施、必要なら K12--E

### ⚠️ Failure 3: 接近のみで回避しない
**症状**: K12-+S と K12-+E ばかりで有害なものを放置  
**対処**: 定期的に K12--S と K12--E を評価

### ✓ Success Pattern
**事例**: 新技術学習 (K12-+S) + レガシー脱却 (K12--E)

### ⚠️ Failure 4: 主体と動機の混同
**症状**: 「自分を変えたい」と言いながら環境に文句  
**対処**: 真の動機と主体を明確に

---

## Test Cases（代表例）

### Test 1: 新技術学習
**Input**: Valence=+, 動機=「Kubernetes を学びたい」  
**Expected**: K12-+S（学習意欲）  
**Actual**: ✓ 学習計画作成

### Test 2: レガシー脱却
**Input**: Valence=-, 動機=「古い依存関係を削除」  
**Expected**: K12--E（有害関係排除）  
**Actual**: ✓ 依存関係の整理

### Test 3: 悪い習慣
**Input**: Valence=-, 動機=「夜更かしをやめる」  
**Expected**: K12--S（自己からの回避）  
**Actual**: ✓ 睡眠習慣改善

---

## Configuration

```yaml
default_approach: K12-+S   # 接近のデフォルトは自己
default_avoid: K12--E      # 回避のデフォルトは環境
toxic_detection: true      # 有害環境の自動検出
```

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **対称関係** | K9 (Agency→Valence) | 逆方向の定理 |
| **Postcondition** | T2 Krisis | 判断基準に反映 |

---

*参照: [kairos.md](../../../kernel/kairos.md)*  
*バージョン: 2.0 (2026-01-25)*
