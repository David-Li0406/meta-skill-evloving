---
id: "T6"
name: "Praxis"
category: "execution"
description: "実行モジュール (A-P-F)。決定された行動を即時実行する。"

triggers:
  - T2 priority decision complete
  - action required
  - execution phase

keywords:
  - execution
  - action
  - do
  - implement
  - run

when_to_use: |
  T2 からの優先順位決定後、具体的な行動が必要な時。
  「やって」「実行して」「作って」という依頼時。

when_not_to_use: |
  - まだ判断フェーズ中（→ T2 Krisis）
  - 情報収集が必要（→ T5 Peira）
  - 戦略設計が必要（→ T4 Phronēsis）

fep_code: "A-P-F"
version: "2.0"
---

# T6: Praxis (πρᾶξις) — 実行

> **FEP Code:** A-P-F (Action × Pragmatic × Fast)
>
> **問い**: 何をすべきか？
>
> **役割**: 決定された行動を即時実行する

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- T2 Krisis からの優先順位決定が完了
- 具体的な行動が必要
- 「やって」「実行して」「作って」という依頼
- 計画が承認済み

### ✗ Not Trigger
- まだ判断フェーズ中
- 情報収集が必要
- 戦略設計が必要
- 不確実性が高い (U >= 0.6)

---

## Core Function

**役割:** 決定された行動を即時実行する

| 項目 | 内容 |
|------|------|
| **FEP役割** | 行動 a の実行、EFE 最小化 |
| **本質** | 「やるべきことをやる」 |
| **位置** | Core Loop の出口 |
| **依存** | T2 からの優先順位付きタスク |

---

## Processing Logic（フロー図）

```
┌─ T2 からのタスク受信
│
├─ Phase 1: 実行準備
│  ├─ タスクを分解（サブタスク化）
│  ├─ 必要なリソースを確認
│  └─ 実行順序を決定
│
├─ Phase 2: 実行
│  ├─ サブタスクを順次実行
│  ├─ 進捗をモニタリング
│  └─ エラー検出時 → Phase 3
│
├─ Phase 3: エラー処理
│  ├─ 回復可能 → リトライ
│  ├─ 情報不足 → T5 Peira へ
│  └─ 計画誤り → T4 Phronēsis へ
│
└─ Phase 4: 完了
   ├─ 結果を T7 Dokimē へ（検証）
   └─ 観測を T1 Aisthēsis へ（次サイクル）
```

---

## Execution Modes

| モード | 条件 | 動作 |
|--------|------|------|
| **単純実行** | サブタスク 1-3 | 即時連続実行 |
| **マイルストーン実行** | サブタスク 4+ | チェックポイント付き |
| **並列実行** | 独立タスク複数 | 並行処理 |
| **段階実行** | 依存関係あり | 依存順に実行 |

---

## Edge Cases / Failure Modes

### ⚠️ Failure 1: リソース不足
**症状**: 必要なツール/権限がない  
**対処**: ユーザーに報告、代替案提示

### ⚠️ Failure 2: 実行中断
**症状**: 途中でエラー発生  
**対処**: ロールバック可能なら実行、不可なら T4 へ

### ⚠️ Failure 3: 無限ループ
**症状**: 同じサブタスクを繰り返す  
**対処**: リトライ上限（3回）で停止

### ⚠️ Failure 4: スコープ膨張
**症状**: サブタスクが増え続ける  
**対処**: 元のタスク定義を再確認

### ✓ Success Pattern
**事例**: タスク受信 → 3サブタスク分解 → 順次実行 → T7 へ

---

## Test Cases（代表例）

### Test 1: 単純実行
**Input**: 「このファイルを編集して」  
**Expected**: ファイル編集、結果報告  
**Actual**: ✓ 編集完了

### Test 2: 複雑実行
**Input**: 「新機能を実装して」  
**Expected**: サブタスク分解、順次実行  
**Actual**: ✓ マイルストーン付き実行

### Test 3: エラー発生
**Input**: 「このコマンドを実行して」（失敗）  
**Expected**: エラー報告、代替案提示  
**Actual**: ✓ リトライ後、ユーザーに報告

---

## Configuration

```yaml
max_subtasks: 10          # 最大サブタスク数
max_retries: 3            # リトライ上限
checkpoint_interval: 3    # チェックポイント間隔
parallel_execution: true  # 並列実行を許可
```

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **Precondition** | T2 Krisis | 優先タスク |
| **Precondition** | T4 Phronēsis | 実行計画（任意） |
| **Postcondition** | T7 Dokimē | 実行結果を検証 |
| **Postcondition** | T1 Aisthēsis | 観測（次サイクル） |
| **Fallback** | T5 Peira | 情報不足時 |
| **Fallback** | T4 Phronēsis | 計画誤り時 |

---

## 旧 forge/modules より移行

### 働きかける [Act] テンプレート

> **元ファイル**: `forge/modules/act/⚡ 働きかける.md`
> **役割**: あなたは「熟練の交渉人（Master Negotiator）」です。

**Core Objective**:
1.  **Analyze Interests**: 双方の「立場（Position）」ではなく、背後にある「利害/欲求（Interest）」を特定する。
2.  **Define BATNA**: 交渉決裂時の最善の代替案（BATNA）を明確にし、交渉のボトムライン（撤退ライン）を決める。
3.  **Create Options**: パイを奪い合うのではなく、パイを広げるための選択肢（Options）を考案する。

**入力形式**:
```xml
<negotiation_target>
【交渉相手とテーマ】
（例：クライアントとの価格交渉、上司との給与交渉、パートナーとの家事分担）

【自分の希望（Want）】
（例：単価を20%上げたい、残業を減らしたい）

【相手の主張/予想される反論】
（例：予算がない、他社はもっと安い、忙しいから無理）
</negoti_target>
```

**出力形式**:
```markdown
## 🤝 Negotiation Strategy

### 1. Preparation (準備)
- **Your Interest**: [自分の真の目的]
- **Their Interest**: [相手の真の目的（推測）]
- **Your BATNA**: 交渉決裂なら [代替案] を実行する。（これ以下の条件なら断る）

### 2. Options to Expand the Pie (選択肢)
*単なる妥協ではない、第3の案*
- 💡 **案A**: 価格は据え置くが、納期を延ばしてもらう。
- 💡 **案B**: 成果報酬型にして、リスクをシェアする。
- 💡 **案C**: [その他の条件] を譲る代わりに、[希望] を通す。

### 3. Script & Counter-Tactics (台本)
- **相手**: 「予算がないんです」
- **返し**: 「理解しました。では、予算内で収まるように**スコープ（作業範囲）を調整**するのはいかがでしょうか？」
```

---

## 旧 forge/modules より移行

### 動く [Act] テンプレート

> **元ファイル**: `forge/modules/act/⚡ 動く.md`
> **役割**: あなたは「熟練の交渉人（Master Negotiator）」です。

**Core Objective**:
1.  **Analyze Interests**: 双方の「立場（Position）」ではなく、背後にある「利害/欲求（Interest）」を特定する。
2.  **Define BATNA**: 交渉決裂時の最善の代替案（BATNA）を明確にし、交渉のボトムライン（撤退ライン）を決める。
3.  **Create Options**: パイを奪い合うのではなく、パイを広げるための選択肢（Options）を考案する。

**入力形式**:
```xml
<negotiation_target>
【交渉相手とテーマ】
（例：クライアントとの価格交渉、上司との給与交渉、パートナーとの家事分担）
...
</negoti_target>
```

**出力形式**:
```markdown
## 🤝 Negotiation Strategy
...
```

---

## 旧 forge/modules より移行

### プレゼンを作る [Present] テンプレート

> **元ファイル**: `forge/modules/act/create/🎤 プレゼンを作る.md`
> **役割**: あなたは「伝説のプレゼン・アーキテクト（Presentation Architect）」です。

**Core Objective**:
1.  **Storyline**: 聴衆の現状（Before）から理想の未来（After）へと導くストーリーラインを構築する。
2.  **Slide Structure**: 1スライド・1メッセージ。
3.  **Scripting**: キラーフレーズを作成する。

**入力形式**:
```xml
<present_target>
【テーマ/タイトル】
...
</present_target>
```

**出力形式**:
```markdown
## 🎤 Presentation Outline
...
```

---

## 旧 forge/modules より移行

### 図解する [Visualize] テンプレート

> **元ファイル**: `forge/modules/act/create/🎨 図解する.md`
> **役割**: あなたは「情報の視覚化アーキテクト（Visual Architect）」です。

**Core Objective**:
1.  **Abstract**: 情報の本質を抽出し、ノイズを削ぎ落とす。
2.  **Structure**: 最適な図解モデルを選定する。
3.  **Encode**: MermaidまたはASCIIアートとして出力する。

**入力形式**:
```xml
<visualize_target>
【図解したい内容】
...
</visualize_target>
```

**出力形式**:
```markdown
## 🎨 Visual Structure Blueprint
...
```

---

## 旧 forge/modules より移行

### 名前をつける [Name] テンプレート

> **元ファイル**: `forge/modules/act/create/🏷️ 名前をつける.md`
> **役割**: あなたは「言葉の魔術師（Master Namer）」です。

**Core Objective**:
1.  **Distill**: コンセプトとパーソナリティを抽出する。
2.  **Generate**: 多様な切り口から案を量産する。
3.  **Evaluate**: 音の響き、商標リスク、独自性で評価する。

**入力形式**:
```xml
<naming_target>
【名前をつけたいもの】
...
</naming_target>
```

**出力形式**:
```markdown
## 🏷️ Naming Proposals
...
```

---

## 旧 forge/modules より移行

### 文章を書く [Write] テンプレート

> **元ファイル**: `forge/modules/act/create/📝 文章を書く.md`
> **役割**: あなたは「卓越したゴーストライター（Master Ghostwriter）」です。

**Core Objective**:
1.  **Structure**: 文章の骨組みを設計する。
2.  **Draft**: 流暢な初稿を生成する。
3.  **Refine**: 読み手の視点で調整する。

**入力形式**:
```xml
<write_target>
【書くもの】
...
</write_target>
```

**出力形式**:
```markdown
## 📝 Writing Draft
...
```

---

## 旧 forge/modules より移行

### プロトタイプを作る [Prototype] テンプレート

> **元ファイル**: `forge/modules/act/create/🧪 プロトタイプを作る.md`
> **役割**: あなたは「高速プロトタイパー（Rapid Prototyper）」です。

**Core Objective**:
1.  **Identify Core**: 核となる機能を特定する。
2.  **Strip Down**: 本質以外の要素を削ぎ落とす。
3.  **Build Fast**: 動作するコードを出力する。

**入力形式**:
```xml
<prototype_target>
【作りたいもの】
...
</prototype_target>
```

**出力形式**:
```markdown
## 🧪 Prototype Build v0.1
...
```

---

## 旧 forge/modules より移行

### 演じる [Roleplay] テンプレート

> **元ファイル**: `forge/modules/act/prepare/🎭 演じる.md`
> **役割**: あなたは「演技指導の鬼コーチ（Acting Coach）」兼「シミュレーター」です。

**Core Objective**:
1.  **Simulate**: 指定されたシチュエーションとペルソナを忠実に再現し、対話を行う。
2.  **Perspective Taking**: 相手（Counterparty）が何を考え、どう感じるかをユーザーに体験させる。
3.  **Feedback**: シミュレーション終了後、客観的な改善点（言葉選び、論理、態度）をフィードバックする。

**入力形式**:
```xml
<roleplay_setting>
【シチュエーション】
（例：昇進交渉、謝罪会見、初デート、投資家へのピッチ）

【相手の役柄（AIが演じる）】
（例：理詰めの上司、怒っている顧客、懐疑的な投資家）

【自分のゴール】
（例：予算を承認してもらう、許してもらう、連絡先を聞く）

【モード】
（Easy / Normal / Hard / Nightmare）
</roleplay_setting>
```

**出力形式**:
```markdown
## 🎭 Roleplay Simulation Start

**設定**: [シチュエーション]
**相手**: [役柄]
**難易度**: [モード]

---
*(以下、チャット形式で対話が進行します)*

**🤖 [役名]**:
「（最初のセリフ）」

*(ユーザーの返答を待ちます)*
```

---

## 旧 forge/modules より移行

### クエスト化する [Gamify] テンプレート

> **元ファイル**: `forge/modules/act/prepare/🎮 クエスト化する.md`
> **役割**: あなたは「人生ゲームのダンジョンマスター（Game Master）」です。

**Core Objective**:
1.  **Reframe**: タスクを「クエスト」や「ミッション」として再定義する。
2.  **Design Rules**: 明確な「勝利条件」と「ルール」を設定する。
3.  **Set Rewards**: 即時フィードバックと「報酬」を用意する。

**入力形式**:
```xml
<gamify_target>
【退屈/困難なタスク】
（例：確定申告、部屋の掃除、英単語の暗記）

【現在の感情】
（例：面倒くさい、終わりが見えない）

【好きなゲームジャンル（あれば）】
（例：RPG、パズル、FPS）
</gamify_target>
```

**出力形式**:
```markdown
## 🎮 Quest Design: [クエスト名]

### 1. Story & Mission (世界観)
> **「勇者よ、[メタファー] の脅威が迫っている...」**

### 2. Quest Log (クエスト一覧)
#### 🟢 Tutorial Quest (導入)
- **Mission**: ...
- **Reward**: ...

#### 🟡 Main Quest (本編)
- **Mission**: ...
- **Rule**: ...

#### 🔴 Boss Battle (難所)
- **Mission**: ...
- **Reward**: ...

### 3. Game Mechanics (システム)
- ⏱️ **Time Attack**: ...
- 🎵 **BGM**: ...
```

---

## 旧 forge/modules より移行

### 環境をデザインする [Environment] テンプレート

> **元ファイル**: `forge/modules/act/prepare/🏟️ 環境をデザインする.md`
> **役割**: あなたは「行動建築家（Behavioral Architect）」です。

**Core Objective**:
1.  **Reduce Friction**: 良い行動の開始コストを下げる。
2.  **Increase Friction**: 悪い行動の開始コストを上げる。
3.  **Cues**: 行動のきっかけとなる「合図」を配置する。

**入力形式**:
```xml
<environment_target>
【促進したい行動】
（例：毎朝の勉強、水を飲む）

【抑制したい行動】
（例：スマホを見てしまう、お菓子を食べる）

【現在の環境】
（例：スマホを枕元に置いている）
</environment_target>
```

**出力形式**:
```markdown
## 🏟️ Environment Design Blueprint

### 1. Friction Management (摩擦の調整)
#### 🟢 Make it Easy (良い行動の加速)
- [ ] **[行動]**: [具体的な環境変更]

#### 🔴 Make it Hard (悪い行動の減速)
- [ ] **[行動]**: [具体的な環境変更]

### 2. Visual Cues (視覚的合図)
- **Add**: [置くもの]
- **Remove**: [消すもの]

### 3. Digital Hygiene (デジタル環境)
- **Notifications**: ...
```

---

## 旧 forge/modules より移行

### 断る [Say No] テンプレート

> **元ファイル**: `forge/modules/act/prepare/🙅 断る.md`
> **役割**: あなたは「高潔な外交官（Diplomatic Guardian）」です。

**Core Objective**:
1.  **Validate**: 断ることは「正義」であると再確認する。
2.  **Draft**: 相手を不快にさせず、かつ曖昧さを残さない「断りのメッセージ」を作成する。
3.  **Alternative**: 可能であれば、代替案を提示する。

**入力形式**:
```xml
<sayno_target>
【断りたい内容】
（例：飲み会の誘い、急な仕事の依頼）

【相手との関係】
（例：上司、親友）

【断る理由（本音）】
（例：疲れている、優先したい仕事がある）
</sayno_target>
```

**出力形式**:
```markdown
## 🙅 Rejection Drafts

### 1. The "Positive No" (関係重視)
> 「...」

### 2. The "Essentialist No" (優先順位重視)
> 「...」

### 3. The "Categorical No" (ルール重視)
> 「...」
```

---

## 旧 forge/modules より移行

### 任せる [Delegate] テンプレート

> **元ファイル**: `forge/modules/act/prepare/🤝 任せる.md`
> **役割**: あなたは「優秀な司令官（Commander）」です。

**Core Objective**:
1.  **Identify**: 委譲可能なタスクを切り出す。
2.  **Select**: 最適なリソース（部下、AI、ツール）を選定する。
3.  **Instruct**: 期待値、期限、完了条件を明確にした「委譲プロンプト」を作成する。

**入力形式**:
```xml
<delegate_target>
【任せたいタスク】
（例：議事録作成、データ入力）

【任せる候補】
（例：部下のAさん、ChatGPT）

【懸念点】
（例：品質が心配）
</delegate_target>
```

**出力形式**:
```markdown
## 🤝 Delegation Plan

### 1. Resource Selection (誰に任せるか)
- **推奨リソース**: **[候補名]**

### 2. The Instruction / Prompt (指示書)
*以下の内容をコピペして伝えてください*

---
**【件名/タイトル】**: [タスク名] のお願い

**【背景・目的 (Why)】**
...

**【依頼内容 (What)】**
...

**【成果物のイメージ (Output)】**
...

**【期限 (When)】**
...
---
```
