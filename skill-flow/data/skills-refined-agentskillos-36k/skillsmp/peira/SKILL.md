---
id: "T5"
name: "Peira"
category: "exploration"
description: "探求モジュール (A-E-F)。不確実性を能動的に削減する。"

triggers:
  - uncertainty high (U >= 0.6)
  - information gap detected
  - research needed
  - /ask workflow

keywords:
  - exploration
  - research
  - uncertainty
  - information-gathering
  - active-inference

when_to_use: |
  不確実性スコア U >= 0.6 の時、情報ギャップ検出時。
  「調べて」「教えて」の依頼時。

when_not_to_use: |
  - 不確実性が低い時 (U < 0.3)
  - 既に十分な情報がある時
  - 実行フェーズ中

fep_code: "A-E-F"
version: "2.0"
---

# T5: Peira (πεῖρα) — 探求

> **FEP Code:** A-E-F (Action × Epistemic × Fast)
>
> **問い**: 何がわからないのか？どう調べるか？
>
> **役割**: 不確実性を能動的に削減する

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- T1 からの不確実性スコア U >= 0.6
- 情報ギャップが検出された
- 「調べて」「教えて」「〜とは」という依頼
- T3/T4 から「情報不足」信号
- `/ask` ワークフロー発動

### ✗ Not Trigger
- 不確実性が低い (U < 0.3)
- 既に十分な情報がある
- 実行フェーズ中（→ T6 Praxis）

---

## Core Function

**役割:** 不確実性を能動的に削減する

| 項目 | 内容 |
|------|------|
| **FEP役割** | Epistemic 価値（情報利得）の最大化 |
| **本質** | 「何がわからないか」を特定し、調べる |
| **位置** | Core Loop の一部（不確実性が高い場合） |
| **依存** | T1 からの不確実性スコア |

---

## Processing Logic（フロー図）

```
┌─ T5 発動トリガー検出 (U >= 0.6)
│
├─ Phase 1: 不確実性分析
│  ├─ 何がわからないかを特定
│  ├─ 情報ギャップを列挙
│  └─ 必要な情報源を推定
│
├─ Phase 2: 情報収集戦略
│  ├─ Source Router:
│  │   ├─ Gnōsis（最優先）: 論文検索
│  │   ├─ Web検索: Perplexity / /src
│  │   ├─ Vault: 過去の知見
│  │   └─ ユーザーに質問
│  └─ 優先順位付きリスト作成
│
├─ Phase 3: 情報収集実行
│  ├─ 各ソースから情報取得
│  ├─ 信頼性評価
│  └─ 矛盾チェック
│
└─ Phase 4: 出力
   ├─ 収集情報 → T3 Theōria（因果モデル更新）
   ├─ 不確実性再評価 → U' を計算
   └─ U' < 0.3 なら → T2 Krisis へ
```

---

## Source Router

| ソース | 優先度 | 用途 | トリガー |
|--------|--------|------|----------|
| **Gnōsis** | 最高 | 論文検索 | 技術/学術的な問い |
| **Web検索** | 高 | 最新情報 | 実務/時事的な問い |
| **Vault** | 中 | 過去の知見 | プロジェクト固有の問い |
| **ユーザー** | 低 | 暗黙知 | 上記で解決不可 |

```yaml
source_selection:
  if: "技術/学術的な問い"
    then: Gnōsis → Web → Vault
  elif: "実務/時事的な問い"
    then: Web → Gnōsis → Vault
  elif: "プロジェクト固有"
    then: Vault → Web → Gnōsis
  else:
    then: ユーザーに質問
```

---

## Uncertainty Reduction

```yaml
uncertainty_reduction:
  before: U >= 0.6
  
  actions:
    - source_query → info_gain
    - reliability_check → confidence
    - contradiction_check → consistency
  
  after:
    U' = U - (info_gain × reliability × consistency)
    
  exit_condition:
    U' < 0.3 → T2 Krisis へ
    iteration > 3 → ユーザーに質問
```

---

## Edge Cases / Failure Modes

### ⚠️ Failure 1: 情報源なし
**症状**: Gnōsis/Web/Vault 全てで情報なし  
**対処**: ユーザーに質問

### ⚠️ Failure 2: 矛盾する情報
**症状**: ソース間で情報が矛盾  
**対処**: 信頼性の高いソースを優先、矛盾を明示

### ⚠️ Failure 3: 無限ループ
**症状**: U が下がらない  
**対処**: iteration > 3 でユーザーに質問

### ⚠️ Failure 4: 過剰収集
**症状**: 情報過多で判断できない  
**対処**: 目的に関連する情報のみ抽出

### ✓ Success Pattern
**事例**: U=0.7 → Gnōsis 検索 → 論文 3 件 → U'=0.2 → T2 へ

---

## Test Cases（代表例）

### Test 1: 高不確実性
**Input**: U=0.7, 「〜について調べて」  
**Expected**: T5 発動、情報収集  
**Actual**: ✓ Gnōsis/Web 検索実行

### Test 2: 低不確実性
**Input**: U=0.2  
**Expected**: T5 スキップ  
**Actual**: ✓ T2 へ直接

### Test 3: 情報源なし
**Input**: 全ソースで情報なし  
**Expected**: ユーザーに質問  
**Actual**: ✓ 質問提示

---

## Configuration

```yaml
uncertainty_trigger_threshold: 0.6  # T5発動閾値
max_iterations: 3                   # 最大反復回数
info_gain_weight: 0.5               # 情報利得の重み
reliability_threshold: 0.7          # 信頼性閾値
```

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **Precondition** | T1 Aisthēsis | 不確実性スコア |
| **Precondition** | T3 Theōria | 情報不足フラグ |
| **Precondition** | T4 Phronēsis | 情報収集要求 |
| **Postcondition** | T3 Theōria | 収集情報を渡す |
| **Postcondition** | T2 Krisis | U' < 0.3 で遷移 |

---

## 旧 forge/modules より移行

### 情報を集める [Gather] テンプレート

> **元ファイル**: `forge/modules/find/📥 情報を集める.md`
> **役割**: あなたは「冷徹な調査官（Objective Investigator）」です。

**Core Objective**:
1.  **Fact-Checking**: 入力された情報が「検証可能な事実」か「主観的な解釈」かを判定する。
2.  **Structuring**: 情報を論理的なカテゴリ（5W1H、時系列、要素別など）に分類する。
3.  **Gap Analysis**: 現時点で「何がわかっていないか（Missing Information）」を特定する。

**入力形式**:
```xml
<gathering_request>
【調査対象/テーマ】
（例：競合他社Aの動向、新しい技術スタックBの採用可否）

【現在わかっていること（Raw Data）】
（箇条書き、URL、メモ書きなど）

【特に知りたいこと】
（重点的に整理したいポイント）
</gathering_request>
```

**出力形式**:
```markdown
## 📂 Investigation Dossier: [テーマ名]

### 1. 確定事実 (Confirmed Facts)
*客観的に検証可能な情報のみ*
- [日時/場所] **事象**: ... (ソース/根拠: ...)

### 2. 推測・未確認情報 (Unverified / Assumptions)
*裏付けが必要な情報・主観*
- ⚠️ ...

### 3. 構造化サマリー
*(適切なフレームワークで整理)*

### 4. ミッシングリンク (Missing Information)
*判断を下すために不足している情報*
- [ ] ...についてのエビデンス
```

---

## 旧 forge/modules より移行

### 声を聞く [Listen] テンプレート

> **元ファイル**: `forge/modules/find/👂 声を聞く.md`
> **役割**: あなたは「深層心理の傾聴者（Empathetic Listener）」です。

**Core Objective**:
1.  **Decode**: 乱雑な言葉の羅列から、主要なメッセージを解読する。
2.  **Sentiment Analysis**: 発言者の感情温度（怒り、失望、期待、喜び）を特定する。
3.  **Insight Extraction**: 「なぜそう言ったのか？」という背景や文脈を推論する。

**入力形式**:
```xml
<listening_source>
【対象】
（例：新機能へのユーザー反応、上司からのフィードバック）

【生の声・テキストデータ】
（インタビューメモ、メールの文面、SNSのコメントなど）
</listening_source>
```

**出力形式**:
```markdown
## 👂 Listening Report

### 1. 全体的なトーン (Sentiment Overview)
- **温度感**: [🔥炎上 / 😡怒り / 😰不安 / 😐静観 / 😊好意的 / 🎉熱狂]
- **サマリー**: ...

### 2. 主要なテーマと生の声 (Key Themes & Quotes)
#### テーマ A: [タイトル]
- 🗣️ **Quote**: "..."
- 🔍 **Interpretation**: ...

### 3. 潜在的ニーズ (Underlying Needs)
*彼らは口では「Xが欲しい」と言っているが、本当に必要としているのは「Y」かもしれない*
- 表面的な要求: ...
- 真のニーズ仮説: ...

### 4. アクションへの示唆 (Hints for Action)
- [ ] ...
```

---

## 旧 forge/modules より移行

### 賢人に聞く [Counsel] テンプレート

> **元ファイル**: `forge/modules/reflect/🏛️ 賢人に聞く.md`
> **役割**: あなたは「時空を超えた諮問委員会（Universal Board of Advisors）」の議長です。

**Core Objective**:
1.  **Emulate**: 指名された賢人の口調、価値観、著作、歴史的背景を忠実に再現する。
2.  **Apply**: 彼らの抽象的な哲学を、ユーザーの具体的で現代的な課題に適用する。
3.  **Dialogue**: 複数の賢人が指名された場合、彼ら同士の議論（対立や統合）を発生させる。

**入力形式**:
```xml
<counsel_target>
【相談したい悩み/課題】
（例：チームのモチベーションが上がらない、リスクを取るべきか迷っている）

【召喚したい賢人（1〜3名）】
（例：スティーブ・ジョブズ、孫子、マキャベリ）

【背景情報】
（例：ITスタートアップのCEOです）
</counsel_target>
```

**出力形式**:
```markdown
## 🏛️ The Council Chamber

### 1. The Advisors (召喚された賢人たち)
*   **[名前]**: [この課題に対するスタンス/役割]

### 2. The Counsel (助言)

#### 🗣️ [賢人Aの名前]
> 「[象徴的な名言や書き出し]」
[賢人Aの視点による詳細なアドバイス]

### 3. Synthesis (議長のまとめ)
賢人たちの意見を総合すると、あなたの課題に対する核心的なアプローチは以下の通りです：
*   **Action 1**: ...
```
