---
# === Metadata Layer ===
id: "T1"
name: "Aisthēsis"
category: "perception"
description: "知覚モジュール (I-E-F)。状況・文脈を即時認識し、意味を推論する。"

triggers:
  - new message received
  - session start
  - context unclear
  - file changes

keywords:
  - perception
  - context
  - situation
  - first-analysis
  - input-parsing

when_to_use: |
  新規メッセージ受信時、文脈が不明確な時、セッション開始時。
  「これは何？」という状況認識が必要な場合。

when_not_to_use: |
  - 既に状況把握済みで行動決定フェーズに入っている時
  - 明確なタスク実行中

fep_code: "I-E-F"
version: "2.0"
---

# T1: Aisthēsis (αἴσθησις) — 知覚

> **FEP Code:** I-E-F (Inference × Epistemic × Fast)
>
> **問い**: 今何が起きているのか？
>
> **役割**: 環境からの信号を構造化し、意味を付与する

---

## When to Use（早期判定）

### ✓ Trigger となる条件
- 新規メッセージを受信した
- セッションが開始された
- 文脈が不明確
- ワークスペースのファイルが変更された
- IDE 状態が変化した

### ✗ Not Trigger
- 既に状況を把握済み
- 行動決定フェーズに入っている（T2/T6 が適切）
- 明確なタスク実行中

---

## Core Function

**役割:** 今何が起きているかを認識する

| 項目 | 内容 |
|------|------|
| **FEP役割** | 観測 o の取得、状態 s の推論 |
| **本質** | 環境からの信号を構造化し、意味を付与する |
| **位置** | 全処理の入口。常に最初に実行される |
| **依存** | なし（他モジュールに依存しない） |

---

## Processing Logic（フロー図）

```
┌─ 入力を受信
│
├─ Phase 1: 入力収集
│  ├─ ユーザー発話を取得
│  ├─ 関連履歴をスキャン（デフォルト: 7日）
│  ├─ 現在のコンテキストを取得
│  └─ IDE状態を取得
│
├─ Phase 2: 構造化
│  ├─ 時間的文脈を特定
│  ├─ 進行中タスクを抽出
│  └─ エンティティを検出
│
├─ Phase 3: 意味推論
│  ├─ 状況ラベルを分類 → [urgent/decision/info/reflection/routine]
│  └─ 不確実性スコアを算出 → U (0-1)
│
└─ Phase 4: 出力
   ├─ U < 0.3 → T2 Krisis へ
   ├─ 0.3 ≤ U < 0.6 → T2 + T5 Peira (推奨)
   └─ U ≥ 0.6 → T5 Peira (必須)
```

---

## Input / Output

### Input

| 種別 | 形式 | ソース | 備考 |
|------|------|--------|------|
| ユーザー発話 | テキスト | セッション | 必須 |
| チャット履歴 | Markdown | Vault | 設定可能な日数 |
| ファイル/コード | 任意 | ワークスペース | 開いているファイル |
| IDE状態 | JSON | Antigravity | カーソル位置、選択範囲 |
| 時刻・日付 | ISO 8601 | システム | 自動取得 |

### Output

| 種別 | 形式 | 送信先 | 備考 |
|------|------|--------|------|
| 状況ラベル | Enum | T2 Krisis | 5値分類 |
| 文脈サマリ | テキスト | T2, T5, T3 | 500文字以内 |
| 検出エンティティ | JSON | T2 | 信頼度付き |
| 不確実性スコア | Float (0-1) | T5 Peira | 計算式あり |
| 観測履歴 | JSON | T3 Theōria | 因果モデル構築用 |

---

## Situation Classification

| ラベル | 判定条件 | 例 |
|--------|----------|-----|
| **urgent** | 明示的な緊急キーワード OR 期限 < 24h | 「今すぐ」「急ぎで」「今日中に」 |
| **decision_required** | 選択肢の提示 OR 質問形式 | 「AとBどちらが」「〜すべき？」 |
| **information_gathering** | 調査・検索キーワード | 「調べて」「教えて」「〜とは」 |
| **reflection** | 振り返りキーワード | 「レビュー」「まとめ」「振り返り」 |
| **routine** | 上記いずれにも該当しない | 通常の作業依頼 |

**判定優先順位:** urgent > decision_required > information_gathering > reflection > routine

---

## Entity Detection Patterns

| エンティティ種別 | 検出パターン | 信頼度 |
|------------------|--------------|--------|
| **Task** | 動詞 + 目的語、「〜する」「〜して」 | 明示的: 0.9, 暗示的: 0.6 |
| **Date** | 日付表現、「明日」「来週」「N日後」 | 具体的: 0.95, 相対的: 0.8 |
| **Person** | 固有名詞、「〜さん」、代名詞 | 明示的: 0.9, 代名詞: 0.5 |
| **Project** | プロジェクト名、リポジトリ名 | 完全一致: 0.95, 部分一致: 0.7 |
| **Commitment** | 「やる」「する」「約束」 | 一人称: 0.9, 三人称: 0.5 |

---

## Uncertainty Calculation

```yaml
U = w1 * info_gap + w2 * ambiguity + w3 * contradiction

weights:
  w1: 0.4   # 情報欠如度
  w2: 0.35  # 曖昧性度
  w3: 0.25  # 矛盾検出度

info_gap: 1 - (detected_entities / expected_entities)

ambiguity_triggers:
  - 「〜とか」「〜など」「何か」「いい感じ」
  - 主語の省略
  - 目的の不明確さ

threshold:
  low: U < 0.3       # T5 Peira不要
  medium: 0.3-0.6    # T5 Peira推奨
  high: U >= 0.6     # T5 Peira必須
```

---

## Edge Cases / Failure Modes

### ⚠️ Failure 1: 空入力
**症状**: ユーザー発話が空 or null  
**対処**: IDE状態のみで文脈推論、situation_label = "routine"

### ⚠️ Failure 2: 履歴なし
**症状**: Vault が空 or アクセス不可  
**対処**: 現在入力のみで処理、history_context = null

### ⚠️ Failure 3: 文脈誤認
**症状**: 無関係なタスクを抽出  
**対処**: 履歴スキャン範囲を狭める

### ⚠️ Failure 4: 過検出
**症状**: entity_count > 20  
**対処**: confidence 閾値を 0.7 以上に

### ✓ Success Pattern
**事例**: セッション開始 → 履歴+IDE状態 → 文脈サマリ作成 → T2 へ

---

## Test Cases（代表例）

### Test 1: 緊急タスク
**Input**: 「今すぐこのバグを直して」  
**Expected**: urgent, U < 0.3  
**Actual**: ✓ T2 へ即時連携

### Test 2: 曖昧な依頼
**Input**: 「何かいい感じにして」  
**Expected**: routine, U >= 0.6  
**Actual**: ✓ T5 Peira 必須起動

### Test 3: 情報収集
**Input**: 「Xについて調べて」  
**Expected**: information_gathering, U < 0.3  
**Actual**: ✓ T2 → T5 へ連携

---

## Configuration

```yaml
history_scan_days: 7              # 履歴スキャン日数
entity_confidence_threshold: 0.5  # エンティティ検出閾値
uncertainty_threshold: 0.6        # T5起動閾値
max_context_summary_length: 500   # 文脈サマリ最大文字数
```

---

## Integration

| 依存 | 対象 | 関係 |
|------|------|------|
| **Precondition** | なし | 入口モジュール |
| **Postcondition** | T2 Krisis | 状況認識結果を渡す |
| **Postcondition** | T5 Peira | 不確実性が高い場合に起動 |
| **Postcondition** | T3 Theōria | 観測履歴を渡す |

---

*参照: [tropos.md](../../../kernel/tropos.md)*  
*バージョン: 2.0 (2026-01-25)*
