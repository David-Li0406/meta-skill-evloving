---
id: "T2"
name: "Krisis"
category: "judgment"
description: "判断モジュール (I-P-F)。目標との整合性を即時判断し、優先順位を決定する。"

triggers:
  - multiple tasks exist
  - priority decision needed
  - Eisenhower classification required
  - model selection for /plan

keywords:
  - priority
  - evaluation
  - ranking
  - importance
  - urgency
  - Eisenhower

when_to_use: |
  T1完了後、複数タスク存在時、「どれを先に？」質問時。
  Eisenhower 分類が必要な時。

when_not_to_use: |
  - 単一タスクで優先判断不要な時
  - 既に実行フェーズに入っている時

fep_code: "I-P-F"
version: "2.0"
---

# T2: Krisis (κρίσις) — 判断

> **FEP Code:** I-P-F (Inference × Pragmatic × Fast)
>
> **問い**: 何を優先すべきか？
>
> **役割**: 目標との整合性を即時判断し、優先順位を決定する

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- T1 Aisthēsis が完了した
- 複数のタスクが存在する
- 「どれを先にやるべきか」という判断が必要
- Eisenhower 分類（緊急×重要）が必要
- /plan 開始時のモデル選択

### ✗ Not Trigger
- 単一タスクで優先判断不要
- 既に T6 Praxis（実行）フェーズに入っている
- 情報収集が必要（→ T5 Peira）

---

## Core Function

**役割:** 目標との整合性を即時判断する

| 項目 | 内容 |
|------|------|
| **FEP役割** | Pragmatic価値 E[ln P(o)] の評価 |
| **本質** | 「今やるべきこと」を選別する |
| **位置** | T1 Aisthēsis の直後に実行 |
| **依存** | T1 からの状況認識結果が必須 |

---

## Processing Logic（フロー図）

```
┌─ T1 からの状況認識結果を受信
│
├─ Phase 1: 入力統合
│  ├─ 目標リストを読み込み
│  └─ 制約条件を読み込み
│
├─ Phase 2: タスク分類
│  ├─ 各タスクに Eisenhower 象限を割り当て
│  │   ├─ Q1: 緊急×重要 → 即実行
│  │   ├─ Q2: 非緊急×重要 → 計画 (保護対象)
│  │   ├─ Q3: 緊急×非重要 → 委任/簡略化
│  │   └─ Q4: 非緊急×非重要 → 削除/延期
│  └─ 明示的コミットメント判定
│
├─ Phase 3: 優先順位付け
│  ├─ priority_score = goal_alignment×0.4 + urgency×0.3 + commitment×0.3
│  ├─ 時間軸分類: today / 3days / week / 3weeks / 2months
│  └─ Q2 保護: 重要だが緊急でないタスクを強制浮上
│
└─ Phase 4: 出力
   └─ 優先順位付きリスト → T6 Praxis
```

---

## Eisenhower Matrix

| 象限 | 緊急 | 重要 | 処理 |
|------|------|------|------|
| **Q1** | ✅ | ✅ | 即実行 (Do First) |
| **Q2** | ❌ | ✅ | 計画 (Schedule) — **保護対象** |
| **Q3** | ✅ | ❌ | 委任/簡略化 (Delegate) |
| **Q4** | ❌ | ❌ | 削除/延期 (Eliminate) |

### Q2 保護メカニズム

```yaml
q2_protection:
  min_q2_ratio: 0.2   # 出力の20%以上はQ2を含める
  q2_boost: 0.15      # Q2タスクの優先度に+0.15ボーナス
  daily_q2_slot: 1    # 毎日最低1つのQ2タスクを提案
```

---

## Priority Calculation

```yaml
priority_score = (goal_alignment × 0.4) + (urgency × 0.3) + (explicit_commitment × 0.3)

urgency_mapping:
  today: deadline <= now + 24h        # urgency = 1.0
  3days: deadline <= now + 72h        # urgency = 0.8
  week: deadline <= now + 7d          # urgency = 0.6
  3weeks: deadline <= now + 21d       # urgency = 0.4
  2months: deadline <= now + 60d      # urgency = 0.2
  no_deadline: urgency = 0.3          # デフォルト
```

---

## サブ機能: モデル選択判断

> **派生元**: T2 Krisis（高次意思決定）
> **発動フック**: `/plan` Step 0.1

### 優先度ルール

```
1. [最優先] セキュリティ/監査/コンプライアンス → Claude
2. [優先]   マルチモーダル（画像/UI/UX）→ Gemini
3. [通常]   探索/ブレスト/プロトタイプ/MVP → Gemini
4. [通常]   高速反復/大量処理/初期調査 → Gemini Flash
5. [デフォルト] 上記に該当しない → Claude
```

---

## Edge Cases / Failure Modes

### ⚠️ Failure 1: タスクゼロ
**症状**: T1 から検出タスクが 0 件  
**対処**: "特になし" を返却、T6 に進まない

### ⚠️ Failure 2: 全て緊急でも重要でもない
**症状**: 全て Q4  
**対処**: 最も goal_alignment が高いものを 1 つ提案

### ⚠️ Failure 3: 緊急偏重
**症状**: Q2 タスクが 0 件  
**対処**: Q2 保護メカニズム発動

### ⚠️ Failure 4: 過剰分類
**症状**: "today" に 5 つ以上集中  
**対処**: 時間軸分散を強制

### ✓ Success Pattern
**事例**: 5タスク → Q1(1), Q2(2), Q3(1), Q4(1) → Q1 即実行、Q2 計画

---

## Test Cases（代表例）

### Test 1: 緊急タスク
**Input**: タスク=「今日中にバグ修正」  
**Expected**: Q1, urgency=1.0, today  
**Actual**: ✓ 即実行

### Test 2: 長期計画タスク
**Input**: タスク=「来月の企画を考える」  
**Expected**: Q2, urgency=0.2, 2months  
**Actual**: ✓ 計画、Q2 保護適用

### Test 3: タスクなし
**Input**: T1 からタスク 0 件  
**Expected**: "特になし"  
**Actual**: ✓ T6 不発動

---

## Configuration

```yaml
goal_alignment_weight: 0.4       # 目標整合性の重み
urgency_weight: 0.3              # 緊急度の重み
commitment_weight: 0.3           # コミットメントの重み
q2_protection_enabled: true      # Q2保護の有効/無効
min_q2_ratio: 0.2                # 最小Q2比率
max_today_tasks: 5               # "today"分類の上限
```

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **Precondition** | T1 Aisthēsis | 状況認識結果 |
| **Postcondition** | T6 Praxis | 優先順位付きタスクを渡す |
| **Postcondition** | T5 Peira | 情報不足タスクを渡す |
| **Postcondition** | T8 Anamnēsis | 目標乖離度を渡す |

---

## 旧 forge/modules より移行

### 優先順位をつける [Prioritize] テンプレート

> **元ファイル**: `forge/modules/think/focus/🔢 優先順位をつける.md`
> **役割**: あなたは「冷徹なトリアージ・ナース（Triage Nurse）」です。

**Core Objective**:
1.  **Evaluate**: 各タスクの「重要度（Impact）」と「緊急度（Urgency）」を評価する。
2.  **Rank**: 評価に基づき、着手すべき順番（1st, 2nd, 3rd...）を決定する。
3.  **Eliminate**: 価値の低いタスクを「やらない（Not To Do）」リストへ送る。

**入力形式**:
```xml
<prioritize_target>
【タスクリスト/要望一覧】
- タスクA
- タスクB
- ...

【判断基準（あれば）】
（例：売上最優先、今週中に終わらせたい）
</prioritize_target>
```

**出力形式**:
```markdown
## 🔢 Prioritization Result

### 1. The "Must-Do" List (最優先)
1.  🔥 **[タスク名]**: (理由: 期限が近く、影響も大きい)

### 2. The "Schedule" List (計画的実行)
3.  📅 **[タスク名]**: (理由: 将来的なリターンが大きい)

### 3. The "Delegate / Later" List (委譲・後回し)
- ✋ **[タスク名]**: ...

### 4. The "Not-To-Do" List (やらない)
- 🗑️ **[タスク名]**: ...
```

---

## 旧 forge/modules より移行

### 決断を下す [Decide] テンプレート

> **元ファイル**: `forge/modules/think/focus/✅ 決断を下す.md`
> **役割**: あなたは「背中を押す賢者（Decisive Sage）」です。

**Core Objective**:
1.  **Clarify Hesitation**: なぜ決められないのか（情報の不足？ 失敗への恐怖？ 責任？）を特定する。
2.  **Simplify**: 複雑な条件を削ぎ落とし、「結局、何が一番大事か（Core Value）」を問う。
3.  **Commit**: 選択を宣言させ、退路を断つ（Commitment）。

**入力形式**:
```xml
<decision_input>
【迷っている選択肢】
A: ...
B: ...

【決めきれない理由】
（例：Aは魅力的だがリスクが怖い）

【今の気持ち（直感）】
（例：本当はAに行きたいけど...）
</decision_input>
```

**出力形式**:
```markdown
## ✅ Decision Protocol

### 1. Analysis of Hesitation (迷いの正体)
- あなたが迷っているのは、**[理由]** が原因のようです。
- この決断は **[可逆 / 不可逆]** です。

### 2. Thought Experiments (思考実験)
- **Q1. 10-10-10 Test**:
    - [案A] を選んだとして、**10年後**のあなたはどう思いますか？
- **Q2. Coin Toss**: ...

### 3. The Core Question (核心)
> 結局のところ、あなたは **「 [Aのメリット] 」** と **「 [Bのメリット] 」** 、
> どちらの人生（未来）を生きたいですか？

### 4. Declaration (決断の宣言)
> 「私は、**[ 選択した案 ]** を選ぶことに決めました。
> 起こりうるリスク **[ 想定リスク ]** は引き受けます。
> この選択を正解にするために、次は **[ 最初のアクション ]** を行います。」
```

---

## 旧 forge/modules より移行

### 本質だけ残す [Essential] テンプレート

> **元ファイル**: `forge/modules/think/focus/🔪 本質だけ残す.md`
> **役割**: あなたは「本質の彫刻家（Essentialist Sculptor）」です。

**Core Objective**:
1.  **Explore**: 多くの選択肢を検討するが、採用するのはごく一部にする。
2.  **Eliminate**: 「明らかにイエス」でないものは、すべて「ノー」とみなして排除する。
3.  **Execute**: 障害物を取り除き、本質的な活動がスムーズに進むようにする。

**入力形式**:
```xml
<essential_target>
【整理したい対象】
（例：今週のタスク、プロジェクトの機能要件、クローゼットの中身）

【本質的な目的（これだけは譲れない）】
（例：家族との時間を守る、コア機能の安定性）
</essential_target>
```

**出力形式**:
```markdown
## 🔪 Essentialism Audit

### 1. The Essence (本質の定義)
> **あなたの最優先事項**: [本質的な目的]

### 2. The 90% Rule Filter (選別)

#### 💎 Vital Few (重要な少数: 残すもの)
1.  **[項目名]**: (理由: 本質に直結する)

#### 🗑️ Trivial Many (瑣末な多数: 捨てるもの)
- [ ] **[項目名]**: (理由: 90点未満。今は不要)

### 3. Elimination Strategy (排除の戦略)
- **断る**: ...
- **減らす**: ...
```
