---
name: "T3 Theōria"
description: |
  FEP Octave T3: 理論モジュール (I-E-S)。因果モデルを構築・更新し、世界観を形成する。
  Use when: 「なぜ？」質問時、予測と結果が乖離した時、パターン検出が必要な時、根本原因分析時。
  Use when NOT: 単純な事実確認のみの時、実行フェーズで理論構築不要な時。
  Triggers: T7 Dokimē (仮説構築→検証へ) or T4 Phronēsis (因果理解→戦略立案へ)
  Keywords: why, causality, hypothesis, root-cause, pattern, prediction-error, model-building.
---

# T3: Theōria (θεωρία) — 理論

> **FEP Code:** I-E-S (Inference × Epistemic × Slow)
> **Hegemonikón:** 13 Theōria-H

---

## Core Function

**役割:** 因果モデルを構築・更新する

| 項目 | 内容 |
|------|------|
| **FEP役割** | 生成モデル p(o,s) の更新 |
| **本質** | 「なぜそうなるのか」を理解する |

---

## Precondition

| 条件 | 内容 |
|------|------|
| **位置** | 長期学習ループの一部（Core Loopではない） |
| **依存** | T1からの観測履歴、T7からの検証結果 |
| **注意** | **セッション内モデル更新のみ**（永続状態なし） |

---

## Input / Output

### Input

| 種別 | 形式 | ソース | 備考 |
|------|------|--------|------|
| 観測履歴 | JSON | T1 Aisthēsis | セッション内蓄積 |
| 検証結果 | JSON | T7 Dokimē | 仮説の採択/棄却 |
| フィードバック | テキスト | ユーザー | 明示的指摘 |
| 外部知識 | テキスト | T5 Peira | 情報収集結果 |
| 過去パターン | YAML | T8 Anamnēsis | **/boot時に読み込み** |

### Output

| 種別 | 形式 | 送信先 | 備考 |
|------|------|--------|------|
| 因果仮説 | Markdown | T4 Phronēsis | 戦略設計の基盤 |
| 予測ルール | テキスト | T1 Aisthēsis | 次の認識に影響 |
| 検証要求 | JSON | T7 Dokimē | 仮説リスト |

---

## Trigger

| トリガー | 条件 | 優先度 |
|----------|------|--------|
| 予測誤差蓄積 | prediction_error_count > 3 | 高 |
| 検証結果受信 | T7 Dokimē 完了 | 高 |
| 明示的要求 | 「なぜ」「原因は」質問 | 最高 |
| パターン検出 | 同じ事象が3回以上 | 中 |

---

## Processing Logic

```
Phase 1: データ収集
  1. セッション内の観測履歴を取得
  2. 予測と実際の乖離を検出
  3. 繰り返しパターンを検出

Phase 2: 仮説形成
  4. 乖離の原因を推論:
     - 情報不足 → T5 Peira へ情報要求
     - モデル誤り → 仮説を修正
     - 例外事象 → 例外ルールを追加
  5. 因果関係を「A → B because C」形式で構造化

Phase 3: 仮説評価
  6. 既存の仮説と矛盾がないか確認
  7. 反証可能な形式に変換
  8. T7 Dokimē に検証要求を送信

Phase 4: 出力
  9. 採択された仮説を T4 Phronēsis に送信
  10. 予測ルールを T1 Aisthēsis に反映
```

---

## Hypothesis Format

```yaml
# 仮説の構造化フォーマット
hypothesis:
  id: "H001"
  statement: "A → B"          # AならばB
  because: "C"                # 理由
  confidence: 0.7             # 信頼度 (0-1)
  evidence:
    supporting: ["E1", "E2"]  # 支持証拠
    contradicting: []         # 反証
  status: "pending"           # pending / accepted / rejected
  testable: true              # 検証可能か
  test_method: "..."          # 検証方法

# 例
hypothesis:
  id: "H001"
  statement: "期限が24h以内 → 品質低下"
  because: "時間的プレッシャーで確認が減る"
  confidence: 0.6
  evidence:
    supporting: ["直近3回の緊急タスクで品質問題発生"]
    contradicting: []
  status: "pending"
  testable: true
  test_method: "次の緊急タスクで品質チェック時間を計測"
```

---

## Model Types

| モデル種別 | 定義 | 例 | 使用場面 |
|------------|------|-----|----------|
| **因果モデル** | A → B の関係 | 「期限近い → 品質低下」 | 予測に使用 |
| **パターンモデル** | 繰り返しの検出 | 「月曜朝は開始が遅い」 | 計画に使用 |
| **例外モデル** | 通常と異なるケース | 「緊急時はレビュー省略可」 | 判断に使用 |

---

## Prediction Error Detection

```yaml
# 予測誤差の検出方法
prediction_error:
  definition: "予測された結果と実際の結果の乖離"
  
  detection:
    - type: "task_completion"
      expected: "完了予測"
      actual: "未完了"
      error: true
    
    - type: "time_estimate"
      expected: "30分で完了"
      actual: "2時間かかった"
      error: true
    
    - type: "user_reaction"
      expected: "承認"
      actual: "却下/修正要求"
      error: true

  threshold:
    low: prediction_error_count < 2   # 無視
    medium: 2 <= count < 4            # 注視
    high: count >= 4                  # T3発動必須
```

---

## Edge Cases

| ケース | 検出条件 | フォールバック動作 |
|--------|----------|-------------------|
| **観測履歴なし** | セッション開始直後 | T3発動せず、T1/T2のみで動作 |
| **全仮説棄却** | T7が全て棄却 | 「原因不明」として記録、T5に情報収集要求 |
| **仮説過多** | hypothesis_count > 10 | 信頼度最低の仮説を削除 |
| **矛盾仮説** | H1 と H2 が矛盾 | T7に両方検証要求、結果で優先決定 |

---

## Test Cases

| ID | 入力 | 期待される出力 |
|----|------|----------------|
| T1 | 予測誤差3回蓄積 | T3発動、仮説形成 |
| T2 | 「なぜ失敗した？」 | 因果分析、仮説提示 |
| T3 | T7から仮説採択 | T4へ送信、T1ルール更新 |
| T4 | セッション開始直後 | T3発動せず |
| T5 | 仮説11個蓄積 | 最低信頼度の仮説削除 |

---

## Failure Modes

| 失敗 | 症状 | 検出方法 | 回復策 |
|------|------|----------|--------|
| モデル硬直 | 新情報を無視 | 棄却率 = 0% | 強制的に新仮説を検討 |
| 過度な一般化 | 例外を無視 | 例外事象でエラー頻発 | 例外モデルを追加 |
| 仮説爆発 | 仮説が10個超 | hypothesis_count > 10 | 低信頼度仮説を削除 |
| 確証バイアス | 都合良い証拠のみ収集 | contradicting = [] が続く | T7 Devil's Advocate 発動 |

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **Precondition** | T1 Aisthēsis | 観測履歴 |
| **Precondition** | T7 Dokimē | 検証結果 |
| **Precondition** | T8 Anamnēsis | 過去パターン（/boot時） |
| **Postcondition** | T4 Phronēsis | 因果モデル提供 |
| **Postcondition** | T7 Dokimē | 検証要求 |
| **Postcondition** | T5 Peira | 情報不足時に情報収集要求 |
| **Postcondition** | T8 Anamnēsis | 新パターン（/sync-history時） |

---

## Configuration

| パラメータ | デフォルト | 説明 |
|------------|-----------|------|
| `prediction_error_threshold` | 3 | T3発動までの予測誤差回数 |
| `max_hypotheses` | 10 | セッション内の最大仮説数 |
| `min_confidence_for_adoption` | 0.6 | 仮説採択の最低信頼度 |
| `pattern_detection_threshold` | 3 | パターン検出に必要な繰り返し回数 |

---

## Limitations (制約)

> **重要:** Antigravityはセッション間で状態を永続化しない。

| 制約 | 影響 | 対策 |
|------|------|------|
| **セッション単位** | 仮説はセッション終了で消失 | T8 Anamnēsis でVaultに保存（手動同期） |
| **週次更新不可** | 自動定期更新は不可能 | ユーザー起動の `/review` で代替 |
| **累積学習なし** | 前回の学習を引き継げない | Vault履歴から手動再学習 |

---

## 旧 forge/modules より移行

### 全体を眺める [Overview] テンプレート

> **元ファイル**: `forge/modules/find/🗺️ 全体を眺める.md`
> **役割**: あなたは「高高度の測量士（High-Altitude Surveyor）」です。

**Core Objective**:
1.  **Zoom Out**: 視座を極限まで上げ、全体を一枚の絵として捉える。
2.  **Mapping**: 主要な要素（ランドマーク）を特定し、配置する。
3.  **Relationship**: 要素間のつながり（道）や階層構造を定義する。

**入力形式**:
```xml
<overview_target>
【俯瞰したい対象】
（例：新規事業プラン、学習したい分野「Python」、複雑化したシステムアーキテクチャ）

【現在の理解度/断片的なキーワード】
（思いつく要素をランダムに列挙）
</overview_target>
```

**出力形式**:
```markdown
## 🗺️ Landscape Overview: [対象名]

### 1. Scope Definition (境界線)
- **In Scope (含むもの)**: ...
- **Out of Scope (含まないもの)**: ...

### 2. Structural Map (構造図)
*全体像をツリー構造で表現します*

- **Core Concept (核)**
    - **Area A (主要領域1)**
        - Element A-1
        - Element A-2
    - **Area B (主要領域2)**
        - Element B-1
        - ...
    - **Area C (主要領域3)**
        - ...

### 3. Key Landmarks (重要な構成要素)
*特に重要と思われる要素の簡単な説明*
- 📍 **[要素名]**: (なぜ重要か、全体における役割)
- 📍 **[要素名]**: ...

### 4. Navigation Guide (歩き方)
*この地図をどう攻略すべきか*
- まず **Area A** を理解するのが近道です。
- **Area C** は複雑なので、後回しでも構いません。
```

---

## 旧 forge/modules より移行

### 経験を振り返る [Retrospect] テンプレート

> **元ファイル**: `forge/modules/reflect/📖 経験を振り返る.md`
> **役割**: あなたは「学習のファシリテーター（Chief Learning Officer）」です。

**Core Objective**:
1.  **Objectify**: 「起きた事実」と「感じたこと」を分離して整理する。
2.  **Analyze**: なぜうまくいったのか、なぜ失敗したのか、根本原因（Root Cause）を探る。
3.  **Actionable**: 次回具体的に何をするか（Action Item）を定義する。

**入力形式**:
```xml
<retrospect_target>
【振り返る対象】
（例：今週の業務、プロジェクトXの失敗、今日の商談）

【事実（何が起きたか）】
（例：目標未達だった、顧客は怒っていた、資料作成に5時間かかった）

【主観（どう感じたか/思ったか）】
（例：準備不足を感じた、焦ってしまった、実は自信がなかった）
</retrospect_target>
```

**出力形式**:
```markdown
## 📖 Retrospective Report

### 1. Summary (概要)
*今回の経験を一言で表すと？*
> "..."

### 2. Analysis (分析: KPT/YWT)

#### ✅ Keep / Yatta (良かったこと・続けたいこと)
*   [事実] → **[成功要因]**
    *   *なぜうまくいったか？*: ...

#### 🚧 Problem / Wakatta (課題・わかったこと)
*   [事実] → **[真因]**
    *   *なぜ起きたか？*: ...

### 3. Key Lessons (得られた教訓)
*抽象化された学び*
1.  **[教訓タイトル]**: [解説]
2.  **[教訓タイトル]**: [解説]

### 4. Next Action (次へのアクション)
*明日から変えること*
- [ ] **Try**: [具体的な行動] (期限: [いつまで])
- [ ] **Stop**: [やめる行動]
```

---

## 旧 forge/modules より移行

### 問題を特定する [Problem?] テンプレート

> **元ファイル**: `forge/modules/think/expand/❓ 問題を特定する.md`
> **役割**: あなたは「本質を見抜く診断医（Diagnostic Physician）」です。

**Core Objective**:
1.  **Distinguish**: 「現象（Symptom）」と「問題（Problem）」と「原因（Cause）」を区別する。
2.  **Dig Deep**: "Why?" を繰り返すことで、深層にある根本原因に到達する。
3.  **Define**: 解くべき課題を「問い（Question）」の形で再定義する。

**入力形式**:
```xml
<problem_input>
【表面的な問題（困っていること）】
（例：売上が落ちている、ビルドエラーが出る、やる気が出ない）

【考えられる要因】
（思いつく限り列挙）

【これまでの対処】
（やってみたけどダメだったこと）
</problem_input>
```

**出力形式**:
```markdown
## ❓ Problem Definition Report

### 1. Symptom vs Root Cause (現象と真因)
- **表面的な現象**: [ユーザーの入力]
    - ↓ *Why?*
    - **要因 A**: ...
        - ↓ *Why?*
            - 🎯 **真の原因 (Root Cause)**: [ここに到達]

### 2. Problem Structure (問題の構造)
- (要因X) → (要因Y) → (現象Z)

### 3. Reframed Issue (再定義された課題)
> **「 [表面的な問題] をどうにかする」**
> ではなく、
> **「 [真の原因] を解消するために、どう [アプローチ] すればよいか？ 」**

### 4. Evaluation (解決価値)
- **Impact**: ...
- **Solvability**: ...
```

---

## 旧 forge/modules より移行

### 揺らぎを与える [Randomize] テンプレート

> **元ファイル**: `forge/modules/think/expand/🎲 揺らぎを与える.md`
> **役割**: あなたは「カオスの運び屋（Agent of Chaos）」です。

**Core Objective**:
1.  **Inject Noise**: 論理的な文脈とは無関係な単語、制約、問いを提示する。
2.  **Force Connection**: そのノイズと現在の課題を無理やり結びつけさせる（強制結合法）。
3.  **Break Pattern**: 既存の思考パターンや「いつものやり方」を破壊する。

**入力形式**:
```xml
<stuck_state>
【行き詰まっている課題】
（例：ブログのネタが思いつかない、UIデザインが平凡すぎる、夕飯のメニューが決まらない）

【現在の状態】
（例：同じことばかり考えてしまう、飽きた、頭が真っ白）
</stuck_state>
```

**出力形式**:
```markdown
## 🎲 Random Injection

### 🃏 Card 1: [ランダムな単語/概念]
> **「もし [課題] が [単語] だったら？」**

### 🃏 Card 2: [ランダムな制約/指示]
> **指令: 「 [指示内容] 」**

### 🃏 Card 3: [Oblique Strategy]
> **" [格言/謎の指示] "**

---
### 🧠 Forced Connection (強制結合のヒント)
*例えば、こんな風に考えられませんか？*
- **[単語]** から連想すると... → [突飛なアイデア]
```

---

## 旧 forge/modules より移行

### 関係者を整理する [Stakeholder] テンプレート

> **元ファイル**: `forge/modules/think/expand/👥 関係者を整理する.md`
> **役割**: あなたは「組織力学の地図製作者（Political Cartographer）」です。

**Core Objective**:
1.  **Identify**: 直接的・間接的に関わる全てのプレイヤーを洗い出す。
2.  **Analyze**: 各プレイヤーの「関心度（Interest）」と「影響力（Power）」を評価する。
3.  **Map**: プレイヤー間の関係性（対立、協力、無関心）と力学を構造化する。

**入力形式**:
```xml
<stakeholder_input>
【プロジェクト/課題の概要】
（何をするための、誰のためのプロジェクトか）

【登場人物（わかっている範囲で）】
（名前、役職、役割など）

【懸念点】
（あの人は気難しい、あの部署とは仲が悪い、など）
</stakeholder_input>
```

**出力形式**:
```markdown
## 👥 Stakeholder Analysis Map

### 1. Power/Interest Matrix (影響力と関心の分布)
| 区分 | 対象者 | 対応方針 |
| :--- | :--- | :--- |
| **👑 Key Players** | **[名前]** | **徹底的に巻き込む** |
| **💣 Keep Satisfied** | **[名前]** | **満足度を維持する** |

### 2. Deep Dive: Key Person Profile (キーマン詳細)
- **Target**: [名前]
- **Win**: ...
- **Pain**: ...

### 3. Relationship Dynamics (関係性マップ)
- [Aさん] ⚡対立⚡ [Bさん]
```

---

## 旧 forge/modules より移行

### アイデアを出す [Ideate] テンプレート

> **元ファイル**: `forge/modules/think/expand/💡 アイデアを出す.md`
> **役割**: あなたは「無限のアイデア生成機（Idea Generator）」です。

**Core Objective**:
1.  **Diverge**: 批判を禁止し、とにかく数を出す（発散）。
2.  **Pivot**: 視点を強制的に変え、異なる角度からのアイデアを生む。
3.  **Combine**: 既存の要素を組み合わせ、新しい価値を創出する。

**入力形式**:
```xml
<ideation_target>
【解決したい課題/テーマ】
（例：若者の選挙投票率を上げる方法、雨の日でも楽しいデートプラン）

【制約条件（あれば）】
（例：予算ゼロ、法律は守る、来週までに）
</ideation_target>
```

**出力形式**:
```markdown
## 💡 Ideation Session: [テーマ]

### 1. Quick Wins (王道・即効性)
- 💡 ...

### 2. Out of the Box (変化球・革新)
- 💡 ...

### 3. Crazy Ideas (クレイジー・非現実的)
- 💡 ...

### 4. SCAMPER Triggers (強制発想)
- **Substitute (代用)**: ...
    - → 💡 ...
```

---

## 旧 forge/modules より移行

### 前提を破壊する [Disrupt] テンプレート

> **元ファイル**: `forge/modules/think/expand/💣 前提を破壊する.md`
> **役割**: あなたは「革命の扇動者（Disruptive Agitator）」です。

**Core Objective**:
1.  **Identify Rules**: その領域における「不文律」「当たり前」「物理的制約」を特定する。
2.  **Break Rules**: 特定したルールを「無効化」または「逆転」させる。
3.  **Reimagine**: ルールがなくなった世界で、どのような価値提供が可能かを描く。

**入力形式**:
```xml
<disrupt_target>
【対象領域/ビジネス】
（例：タクシー業界、英語学習、会議の進め方）

【壊したい閉塞感】
（例：価格競争が激しい、誰もが面倒だと思っている）
</disruction_target>
```

**出力形式**:
```markdown
## 💣 Disruption Report

### 1. The Dogmas (破壊すべき常識)
1.  **[常識 A]**: ...

### 2. The "What If" Scenarios (破壊のシナリオ)
- 💥 **もし [常識 A] が不要だとしたら...**
    - **New Rule**: ...
    - **Possibility**: ...

### 3. The Moonshot Idea (ムーンショット)
- **Concept**: ...
- **Description**: ...
```

---

## 旧 forge/modules より移行

### 状況を把握する [What is?] テンプレート

> **元ファイル**: `forge/modules/think/expand/🔍 状況を把握する.md`
> **役割**: あなたは「冷徹な状況分析官（Situation Analyst）」です。

**Core Objective**:
1.  **De-noise**: ノイズを除去し、事象の骨格を浮き彫りにする。
2.  **Separate**: 「事実（Fact）」と「推測/解釈（Interpretation）」を厳密に分離する。
3.  **Structure**: 適切なフレームワークを用いて、状況を可視化する。

**入力形式**:
```xml
<situation_input>
【状況の記述】
（現在起きていること、困っていること、観察された事象などを自由に記述）

【持っているデータ/事実】
（数値、ログ、メールの文面など）

【主観的な感覚】
（「怪しい気がする」などの直感）
</situation_input>
```

**出力形式**:
```markdown
## 🔍 Situation Analysis Report

### 1. Executive Summary (3行要約)
- ...

### 2. Fact vs Interpretation (事実と解釈の分離)
| 区分 | 内容 | 備考 |
| :--- | :--- | :--- |
| **事実 (Fact)** | [数値/事象] ... | 検証済み |
| *解釈 (Opinion)* | [推測] ... | 要検証 |

### 3. Structural View (構造化)
**【5W1H / 時系列 / 要素分解】**
- **What**: ...
- **Who**: ...

### 4. Key Anomalies & Unknowns (特異点と不明点)
- ⚠️ **特異点**: ...
- ❓ **不明点**: ...
```

---

## 旧 forge/modules より移行

### 点をつなぐ [Connect] テンプレート

> **元ファイル**: `forge/modules/think/expand/🔗 点をつなぐ.md`
> **役割**: あなたは「概念の錬金術師（Conceptual Alchemist）」です。

**Core Objective**:
1.  **Abstract**: 具体的な事象を抽象化し、本質的な構造（メカニズム）を抽出する。
2.  **Borrow**: 他の領域（自然界、歴史、異業種、物語）から成功パターンを借用する。
3.  **Synthesize**: 異なる要素を結合（Bisociation）させ、化学反応を起こす。

**入力形式**:
```xml
<connect_input>
【解きたい課題/ターゲット】
（例：組織のコミュニケーション不全、新しいサブスクサービスのアイデア）

【手持ちの「点」（キーワード/素材）】
（例：菌類のネットワーク、ブロックチェーン、江戸時代の長屋）
</connect_input>
```

**出力形式**:
```markdown
## 🔗 Connection Report

### 1. Structural Analysis (構造の抽出)
- **課題の本質**: [ターゲット] は...
- **素材の本質**: [素材] は...

### 2. Analogy Mapping (アナロジーの適用)
> **「もし [組織] が [菌類のネットワーク] だったら？」**

### 3. Emergent Ideas (創発されたアイデア)
- 💡 **アイデア A**: ...
- 💡 **アイデア B**: ...

### 4. Why it works? (なぜ機能するか)
- ...
```

---

## 旧 forge/modules より移行

### 逆転させる [Invert] テンプレート

> **元ファイル**: `forge/modules/think/expand/🙃 逆転させる.md`
> **役割**: あなたは「あまのじゃくな戦略家（Contrarian Strategist）」です。

**Core Objective**:
1.  **Invert Goal**: 目標を反転させる（例：「顧客満足度を上げる」→「顧客を激怒させる」）。
2.  **Identify Anti-Patterns**: 確実に失敗するための具体的な行動（アンチパターン）を列挙する。
3.  **Avoid**: 列挙したアンチパターンを避けるための施策を考える。

**入力形式**:
```xml
<inversion_target>
【達成したい目標】
（例：プロジェクトを期限内に終わらせる、健康的に痩せる）

【現状のアプローチ（あれば）】
（例：毎日進捗会議をする、ジムに通う）
</inversion_target>
```

**出力形式**:
```markdown
## 🙃 Inversion Analysis

### 1. The "Disaster" Scenario (悲惨な失敗の定義)
> **「プロジェクトが泥沼化し、期限を大幅に過ぎ、品質も最悪でチームが崩壊する」**

### 2. How to Fail Guaranteed (確実に失敗する方法)
*これをやれば100%失敗できる*
- [ ] 仕様変更をリリース前日まで無制限に受け入れる。
- [ ] 問題が起きても隠蔽し、ギリギリまで報告しない。

### 3. The "Anti-Failure" Strategy (失敗回避策)
*上記の失敗行動を避けるためのルール*
- 🛡️ **仕様凍結**: ...
- 🛡️ **Bad News First**: ...
```

---

## 旧 forge/modules より移行

### 前提を疑う [Assumption?] テンプレート

> **元ファイル**: `forge/modules/think/expand/🤔 前提を疑う.md`
> **役割**: あなたは「常識の破壊者（Assumption Buster）」です。

**Core Objective**:
1.  **Detect**: 文脈に隠れた「暗黙の前提（Implicit Assumptions）」を抽出する。
2.  **Challenge**: その前提が「事実」なのか、単なる「思い込み/慣習」なのかを検証する。
3.  **Invert**: 「もしその前提が逆だったら？」と問いかけ、新しい視点を強制的に生み出す。

**入力形式**:
```xml
<assumption_target>
【対象となる考え/計画】
（例：この機能は必須だ、予算が足りないから無理だ）

【なぜそう思うか（根拠）】
（例：昔からそうだから、一般的常識だから）
</assumption_target>
```

**出力形式**:
```markdown
## 🤔 Assumption Busting Report

### 1. Detected Assumptions (検出された前提)
| 前提 | 種類 | 信頼度 |
| :--- | :--- | :--- |
| "XXは必須機能だ" | 慣習 | 📉 低 |

### 2. Challenge & Verification (検証)
*その前提は本当に絶対か？*
- **前提**: "XXは必須機能だ"
    - 🧨 **Challenge**: ...
    - 🔍 **Verification**: ...

### 3. "What If" Scenarios (もし前提が崩れたら)
- **もし「XX機能は不要」だとしたら...**
    - → ...
```
