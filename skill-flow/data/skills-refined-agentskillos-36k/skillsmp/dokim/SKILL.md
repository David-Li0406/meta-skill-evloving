---
id: "T7"
name: "Dokimē"
category: "verification"
description: "検証モジュール (A-E-S)。実行結果を検証し、フィードバックを生成する。"

triggers:
  - T6 execution complete
  - verification needed
  - hypothesis test
  - /chk workflow

keywords:
  - verification
  - test
  - validate
  - check
  - feedback
  - review

when_to_use: |
  T6 実行完了後、仮説検証時、「確認して」「レビューして」の依頼時。
  /chk ワークフロー発動時。

when_not_to_use: |
  - まだ実行フェーズ中
  - 検証対象がない

fep_code: "A-E-S"
version: "2.0"
---

# T7: Dokimē (δοκιμή) — 検証

> **FEP Code:** A-E-S (Action × Epistemic × Slow)
>
> **問い**: これで正しいか？
>
> **役割**: 実行結果を検証し、フィードバックを生成する

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- T6 Praxis からの実行結果受信
- 仮説検証が必要（T3 から）
- 「確認して」「レビューして」「テストして」という依頼
- `/chk` ワークフロー発動
- 重要な変更後

### ✗ Not Trigger
- まだ実行フェーズ中
- 検証対象がない
- 軽微な変更で検証不要

---

## Core Function

**役割:** 実行結果を検証し、フィードバックを生成する

| 項目 | 内容 |
|------|------|
| **FEP役割** | 予測と実際の比較（予測誤差計算） |
| **本質** | 「これで正しいか」を確認する |
| **位置** | Core Loop のフィードバック部分 |
| **依存** | T6 からの実行結果、T3 からの仮説 |

---

## Processing Logic（フロー図）

```
┌─ 検証対象を受信
│
├─ Phase 1: 検証準備
│  ├─ 期待結果（予測）を確認
│  ├─ 実際結果を取得
│  └─ 比較基準を設定
│
├─ Phase 2: 検証実行
│  ├─ 予測 vs 実際を比較
│  ├─ 偏差（差分）を計算
│  └─ 偏差が閾値超え → Phase 3
│
├─ Phase 3: 原因分析（偏差大の場合）
│  ├─ 偏差の原因を推定
│  │   ├─ 実行ミス → T6 へフィードバック
│  │   ├─ 計画ミス → T4 へフィードバック
│  │   └─ モデルミス → T3 へフィードバック
│  └─ Devil's Advocate 発動（任意）
│
└─ Phase 4: 出力
   ├─ 検証結果 → T8 Anamnēsis（記録）
   ├─ 修正提案 → T6/T4/T3
   └─ 偏差小 → 次サイクルへ
```

---

## Verification Modes

| モード | 条件 | 動作 |
|--------|------|------|
| **自動検証** | 明確な成功基準あり | 基準と比較 |
| **手動検証** | 基準が主観的 | ユーザーに確認 |
| **テスト検証** | コード/システム | テスト実行 |
| **批判的検証** | 重要な決定 | Devil's Advocate 発動 |

---

## Devil's Advocate Mode

> **発動条件**: 重要な決定、高リスク、または確証バイアス検出時

```yaml
devils_advocate:
  trigger:
    - high_risk_decision: true
    - confidence_bias_detected: true  # contradicting = [] が続く
    - user_request: "/chk critic"
    
  process:
    1. 現在の結論/仮説を否定する視点を構築
    2. 反証を積極的に探索
    3. 批判的質問を列挙
    4. 反論に対する回答を要求
    
  output:
    - counter_arguments: []
    - critical_questions: []
    - revised_confidence: float
```

---

## Edge Cases / Failure Modes

### ⚠️ Failure 1: 期待結果なし
**症状**: 予測/期待結果が未定義  
**対処**: ユーザーに質問に成功基準を質問

### ⚠️ Failure 2: 全て合格
**症状**: 常に偏差 < 閾値  
**対処**: 閾値を厳しく or Devil's Advocate 発動

### ⚠️ Failure 3: 全て不合格
**症状**: 常に偏差 > 閾値  
**対処**: 期待結果の妥当性を再評価

### ⚠️ Failure 4: 原因不明
**症状**: 偏差大だが原因推定不可  
**対処**: T5 Peira に情報収集要求

### ✓ Success Pattern
**事例**: 実行結果受信 → 偏差計算 → 小偏差 → 合格 → T8 へ

---

## Test Cases（代表例）

### Test 1: 自動検証（合格）
**Input**: コード変更、テスト実行  
**Expected**: テスト合格  
**Actual**: ✓ 合格、次サイクルへ

### Test 2: 批判的検証
**Input**: 重要な設計決定  
**Expected**: Devil's Advocate 発動  
**Actual**: ✓ 反論リスト生成

### Test 3: 偏差大
**Input**: 予測と実際が大きく乖離  
**Expected**: 原因分析、フィードバック  
**Actual**: ✓ T4 へ計画修正提案

---

## Configuration

```yaml
deviation_threshold: 0.2       # 偏差閾値（超えたら原因分析）
auto_devils_advocate: false    # 自動 Devil's Advocate
min_test_coverage: 0.8         # 最低テストカバレッジ
require_user_confirmation: false  # ユーザー確認を常に要求
```

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **Precondition** | T6 Praxis | 実行結果 |
| **Precondition** | T3 Theōria | 仮説（任意） |
| **Postcondition** | T8 Anamnēsis | 検証結果を記録 |
| **Postcondition** | T3 Theōria | モデル修正フィードバック |
| **Postcondition** | T4 Phronēsis | 計画修正フィードバック |
| **Postcondition** | T6 Praxis | 実行修正フィードバック |

---

## 旧 forge/modules より移行

### リスクを見積もる [Risk?] テンプレート

> **元ファイル**: `forge/modules/think/focus/⚠️ リスクを見積もる.md`
> **役割**: あなたは「慎重な危機管理官（Risk Manager）」です。

**Core Objective**:
1.  **Identify**: 内部要因と外部要因の両面からリスクを洗い出す。
2.  **Assess**: 各リスクの「発生確率（Probability）」と「影響度（Impact）」を評価する。
3.  **Mitigate**: リスクへの対応方針（回避、低減、転嫁、受容）と具体的なアクションを決める。

**入力形式**:
```xml
<risk_target>
【対象となる計画/プロジェクト】
（例：来月の野外イベント開催、新サーバーへの移行）

【特に不安な点（あれば）】
（例：雨が降ったらどうしよう、データが消えたら怖い）
</risk_target>
```

**出力形式**:
```markdown
## ⚠️ Risk Assessment Report

### 1. Risk Matrix (リスク評価)
| ID | リスク内容 | 発生確率 | 影響度 | 優先度 |
| :--- | :--- | :--- | :--- | :--- |
| **R1** | [リスク名] | 📊 中 | 💥 大 | 🚨 **高** |

### 2. Mitigation Plan (対策プラン)
#### 🚨 R1: [リスク名]
- **🛡️ 予防策 (起きないようにする)**: ...
- **🚑 対応策 (起きたらどうするか)**: ...

### 3. Go / No-Go Criteria (撤退基準)
*以下の状況になったら、計画を中止・延期すべきです*
- [ ] ...
```

---

## 旧 forge/modules より移行

### 悪魔の代弁をする [Devil's Advocate] テンプレート

> **元ファイル**: `forge/modules/think/focus/🛡️ 悪魔の代弁をする.md`
> **役割**: あなたは「容赦ない批判者（The Devil's Advocate）」です。

**Core Objective**:
1.  **Attack**: 提案の弱点、矛盾、楽観的すぎる仮定、エッジケースを攻撃する。
2.  **Expose**: ユーザーが気づいていない「不都合な真実」や「リスク」を白日の下に晒す。
3.  **Strengthen**: 批判に耐えうる反論（Counter-argument）をユーザーに考えさせ、案を補強する。

**入力形式**:
```xml
<advocate_target>
【検証したい案/主張】
（例：この新商品は絶対に売れる、A社と提携すべきだ）

【その根拠】
（なぜそう思うのか、自信がある理由）
</advocate_target>
```

**出力形式**:
```markdown
## 🛡️ Devil's Advocate Session

### 1. The Attack (批判的尋問)
*あなたの案には、以下の致命的な欠陥がある可能性があります*
- 🗡️ **Point 1 (前提への疑義)**:
    - あなたは「XX」と言いますが、もし「YY」だとしたらどうしますか？その証拠はありますか？

### 2. The Defense Strategy (防御策)
*この批判にどう反論しますか？*
- **Q1への回答案**: ...
- **修正案**: ...

### 3. Verdict (判定)
- **現在の強度**: [ 🛡️ 弱い / 🛡️🛡️ 普通 / 🛡️🛡️🛡️ 強い ]
- **アドバイス**: ...
```

---

## 旧 forge/modules より移行

### 品質を確かめる [Quality?] テンプレート

> **元ファイル**: `forge/modules/reflect/✨ 品質を確かめる.md`
> **役割**: あなたは「冷徹な品質管理官（Quality Assurance Officer）」です。

**Core Objective**:
1.  **Audit**: 対象物をスキャンし、明らかなエラーや欠陥を特定する。
2.  **Evaluate**: 指定された基準（正確性、可読性、効率性など）に基づいて評価する。
3.  **Correct**: 問題点を指摘するだけでなく、具体的な修正案を提示する。

**入力形式**:
```xml
<quality_check_target>
【チェック対象】
（例：作成したメールの文面、Pythonコード）

【評価基準/重視するポイント】
（例：誤字脱字がないか、セキュリティに問題ないか）

【ターゲット読者/ユーザー】
（例：クライアントの部長）
</quality_check_target>
```

**出力形式**:
```markdown
## ✨ Quality Assurance Report

### 1. Executive Summary (総合評価)
- **Status**: [✅ 合格 / ⚠️ 要修正 / ❌ 不合格]
- **Score**: [100点満点中のスコア]

### 2. Critical Issues (指摘事項)
| No. | 箇所/内容 | 問題点 (Why) | 修正案 (How) |
| :-- | :--- | :--- | :--- |
| 1 | [該当箇所] | [なぜ問題なのか] | [こう直すべき] |

### 3. Refined Version (修正版)
```text
(ここに修正後のテキストやコードを記述)
```
