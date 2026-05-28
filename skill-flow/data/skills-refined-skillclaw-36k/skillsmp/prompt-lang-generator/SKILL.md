---
name: prompt-lang-generator
version: 2.0.0
owner: Hegemonikón
last_updated: "2026-01-25"
status: production
description: |
  Prompt-Lang v2.0 コード生成 Skill。自然言語の要件から構造化プロンプト定義を生成する。
  
  **Trigger:**
  - 「Prompt-Lang でスキルを作成」
  - 「〇〇用のプロンプト定義を生成」
  - 「.prompt ファイルを作って」
---

# Prompt-Lang Generator Skill

## Overview

自然言語による要件説明から、Prompt-Lang v2.0 準拠のスキル定義（`.prompt` / `SKILL.md`）を生成する。

## Core Behavior

1. **要件分析**: 入力からドメイン、タスク種別、制約を抽出
2. **テンプレート選択**: `@context` で参照するドメイン別テンプレートを決定
3. **構造生成**: 必須ディレクティブを含む Prompt-Lang コードを出力
4. **自己評価**: `@rubric` に基づきスコアリング、基準未達なら改善版を再生成

## Required Directives

生成物には以下を **必ず** 含める:

| ディレクティブ | 必須 | 説明 |
|:---------------|:----:|:-----|
| `@role` | ✅ | AI の役割定義 |
| `@goal` | ✅ | タスクの目的 |
| `@constraints` | ✅ | 制約条件（3個以上） |
| `@format` | ✅ | 出力構造の定義 |
| `@examples` | ✅ | 入出力例（1個以上） |
| `@rubric` | ⚪ | 自己評価軸（推奨） |
| `@activation` | ⚪ | トリガー条件（Skill用） |
| `@context` | ⚪ | リソース参照 |
| `@if/@else` | ⚪ | 条件分岐（環境依存時） |
| `@extends` | ⚪ | テンプレート継承 |
| `@mixin` | ⚪ | モジュール合成 |

## Quality Standards

| 項目 | 基準 | 検証方法 |
|:-----|:-----|:---------|
| 構文正確性 | パースエラー 0 | `prompt_lang.py parse` |
| 必須網羅 | 5ディレクティブ含む | チェックリスト |
| 曖昧語 | 0件 | 「適切に」「うまく」検出 |
| @constraints | 3個以上 | カウント |
| @examples | 1個以上 | 存在確認 |

## Workflow

```
Phase 0: 要件分析
  - ドメイン検出（技術/RAG/要約/医療/法律...）
  - タスク種別判定（生成/分類/抽出/評価...）
  - リスクレベル判定（高リスク → 免責必須）
    ↓
Phase 1: テンプレート選択
  - base_template.yaml をベースに
  - ドメイン別テンプレートをマージ
    ↓
Phase 2: コード生成
  - 可変部を LLM で埋める
  - @format は具体的な JSON/Markdown 構造で
    ↓
Phase 3: 自己評価 (optional)
  - @rubric 4軸でスコアリング
  - 閾値未達なら再生成（max 2回）
    ↓
Output: .prompt / SKILL.md
```

## @rubric — 評価軸

```yaml
@rubric:
  - completeness:
      description: 必須セクションの網羅度
      scale: 0-10
      criteria:
        10: 全必須ディレクティブ + Error Handling + Limitations
        7: 全必須ディレクティブあり
        5: 一部欠落
        0: 骨格なし

  - syntactic_correctness:
      description: Prompt-Lang v2.0 としてパース可能か
      scale: binary
      criteria:
        yes: prompt_lang.py parse でエラーなし
        no: パースエラーあり

  - semantic_relevance:
      description: 入力要件との適合度
      scale: 0-10
      criteria:
        10: 要件を完全に反映、過不足なし
        7: 主要要件を反映
        5: 部分的に反映
        0: 要件と無関係

  - practical_utility:
      description: 実際に業務で使えるか
      scale: 0-10
      criteria:
        10: 即座に本番利用可能
        7: 軽微な調整で利用可能
        5: 大幅な修正が必要
        0: 使用不可
```

## @activation — トリガー条件

```yaml
@activation:
  mode: model_decision
  conditions:
    - input_contains: ["prompt-lang", "プロンプト定義", ".prompt", "スキル作成"]
    - input_length: "> 30"
    - intent: "generate structured prompt definition"
  priority: 3
```

## @context — リソース参照

```yaml
@context:
  - file:"templates/base_template.yaml" [priority=HIGH]
  - dir:"templates/domain_templates/"(filter="*.yaml") [priority=MEDIUM]
  - file:"rubric_standards.yaml" [priority=MEDIUM]
  - file:"anti_patterns.md" [priority=LOW]
```

## Edge Cases

| 状況 | 対応 |
|:-----|:-----|
| 入力が曖昧（「いい感じのプロンプト」） | REJECT + 追加質問（ドメイン/タスク/出力形式） |
| 高リスクドメイン（医療/法律） | 免責注記を @constraints に自動追加 |
| 不明なディレクティブ要求 | 「@foo は未対応」と明示し、代替案提示 |
| 出力形式未指定 | デフォルト JSON 形式を適用 |

## Error Handling

1. **構文エラー検出時**: パーサー出力を添えて「この箇所にエラー」と明示
2. **要件不足時**: 不足項目をリストアップし、追加入力を促す
3. **ドメイン外**: 「このドメインは対応外」+ 類似 Skill 提案

## Limitations

- `@extends` / `@mixin` は v2.1 で実装予定（構文は認識するが実行不可）
- MCP 連携（`@context` の `mcp:` 参照）は Phase C で実装予定
- 自動メタ学習ループは未実装

## Examples

### Good Example

**入力**:
```
医療記録から患者の基本属性（氏名、年齢、性別、診断名）を抽出するスキルを作って
```

**出力**:
```prompt-lang
#prompt medical_record_extractor

@role:
  医療記録解析エキスパート

@goal:
  医療記録テキストから患者の基本属性情報を構造化抽出する

@constraints:
  - 診療ガイドラインに準拠すること
  - 推測は禁止、記載されていない情報は null とする
  - 「本情報はAI抽出であり、医療判断に使用しないこと」免責を出力に含める

@format:
  ```json
  {
    "patient_name": "string | null",
    "age": "number | null",
    "gender": "male | female | other | null",
    "diagnosis": ["string"],
    "disclaimer": "本情報はAI抽出であり..."
  }
  ```

@rubric:
  - accuracy:
      description: 抽出精度
      scale: 1-5

@examples:
  - input: "患者: 山田太郎、45歳男性。主訴: 頭痛。診断: 緊張型頭痛"
    output: {"patient_name": "山田太郎", "age": 45, "gender": "male", "diagnosis": ["緊張型頭痛"]}
```

### Bad Example (REJECT)

**入力**:
```
なんかいい感じのプロンプト作って
```

**出力**:
```
❌ REJECT: 情報不足

以下を教えてください:
1. ドメイン（技術/医療/法律/マーケティング/...）
2. タスク種別（生成/分類/抽出/評価/...）
3. 期待する出力形式（JSON/Markdown/自由文/...）
```

---

## MCP Integration (TODO: Phase C)

<!-- 
TODO: Phase C で以下を実装

1. MCP サーバとして公開
   - prompt-lang-generator を MCP tool として登録
   - 入力: 自然言語要件
   - 出力: Prompt-Lang コード

2. @context の mcp: 参照実装
   - mcp:gnosis.tool("search") で関連 Skill 検索
   - mcp:prompt-lang-generator.tool("generate") で再帰生成

3. メタ学習ループ
   - 実行ログ蓄積 → パターン抽出 → テンプレート更新
-->

---

## Version History

| Version | Date | Changes |
|:--------|:-----|:--------|
| 1.0.0 | 2026-01-25 | 初版（Plan B 基盤） |
