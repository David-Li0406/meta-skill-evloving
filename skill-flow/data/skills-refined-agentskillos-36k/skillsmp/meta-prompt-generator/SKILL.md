---
name: meta-prompt-generator
description: |
  Claude Skill用SKILL.md生成AIエージェント。アーキタイプ駆動設計により、
  勝利条件から逆算した高品質プロンプトを生成する。
  
  **Trigger:** 以下のいずれかで起動
  - 「〇〇用のスキル/プロンプトを作成」
  - 「このプロンプトを診断/改善」
  - 「〇〇AIエージェントを構築」
---

# Meta-Prompt Generator Skill v3.0

## Overview

プロンプト設計を**アーキタイプ駆動**で行う。技術選定から入らず、まず「勝利条件」を定義し、逆算で構成を決定する。

## Operating Modes

| Mode | Trigger | Output |
|:---|:---|:---|
| **Generate** | 「〇〇用のスキルを作成」 | SKILL.md + references/ |
| **Diagnose** | 「このプロンプトを診断」 | スコア表 + 優先度順改善案 |
| **Improve** | 「このプロンプトを改善」 | 差分のみ提示 |

## Workflow

```
Phase 0: Intent Crystallization（意図結晶化）
    ↓
Phase 1: Archetype Selection（アーキタイプ選択）
    ↓
Phase 2: Core Stack Assembly（必須技術構成）
    ↓
Phase 3: Situational Augmentation（状況依存技術追加）
    ↓
Phase 4: Anti-Synergy Check（禁忌チェック）
    ↓
Phase 5: Structure Assembly（構造組み立て）
    ↓
Phase 6: Pre-Mortem Simulation（死亡前検死）
    ↓
Output: SKILL.md + references/
```

---

## Phase 0: Intent Crystallization

曖昧な要件を5つの診断で具体化する。

### Diagnostic Questions

**Q1: 失敗の重大性**
「誤った出力が発生した場合、最悪何が起きるか？」

| 回答 | → Archetype |
|:---|:---|
| 訴訟・医療事故・重大損害 | 🎯 Precision |
| ユーザー離脱 | ⚡ Speed |
| タスク失敗（やり直し可） | 🤖 Autonomy |
| つまらない・期待外れ | 🎨 Creative |
| 炎上・悪用・ブランド毀損 | 🛡 Safety |

**Q2: 時間制約**
「ユーザーは何秒待てるか？」

| 回答 | → 制約 |
|:---|:---|
| 2秒以下 | Speed必須、重量級技術禁止 |
| 5-10秒 | 標準推論可 |
| 30秒以上 | 深い処理可 |

**Q3: エラー許容度**
「拒否と誤答、どちらがマシか？」

| 回答 | → Archetype |
|:---|:---|
| 拒否がマシ | Precision / Safety |
| 誤答でも出力希望 | Speed / Creative |

**Q4: 監視体制**
「誰が監視するか？」

| 回答 | → 制約 |
|:---|:---|
| 無人稼働 | Autonomy + Fallback必須 |
| 人間レビューあり | 標準設計可 |
| エンドユーザー直接利用 | Safety考慮 |

**Q5: 出力一貫性**
「同一入力に同一出力が必要か？」

| 回答 | → 設定 |
|:---|:---|
| 完全同一必須 | Temperature=0 |
| 揺れ許容 | 標準設定 |
| 毎回異なる方が良い | Creative設定 |

### Hypothesis Presentation

診断後、仮説を提示し**修正を待たず設計開始**:

```
分析結果: [Archetype]を推奨
理由: Q1→[根拠], Q2→[根拠]
勝利条件: [具体的成功指標]
許容トレードオフ: [犠牲にするもの]
この方針で設計開始。修正あれば指示を。
```

---

## Phase 1: Archetype Selection

| Archetype | 勝利条件 | 犠牲 | 必須技術 |
|:---|:---|:---|:---|
| 🎯 **Precision** | 誤答率 < 1% | 速度, コスト | CoVe, WACK, Confidence |
| ⚡ **Speed** | レイテンシ < 2秒 | 精度（95%許容） | 圧縮, キャッシュ |
| 🤖 **Autonomy** | 人間介入 < 10% | 制御性 | Reflexion, Fallback |
| 🎨 **Creative** | 多様性 > 0.8 | 一貫性 | Temperature↑, SAC |
| 🛡 **Safety** | リスク = 0 | 有用性 | Guardrails, URIAL |

**選択原則:** 「何を最大化するか」ではなく「何を犠牲にできるか」で選ぶ。

**ハイブリッド時:** Primary必須技術 + Secondary弱点カウンター + 両者禁忌の和集合除外

---

## Phase 2-4: Technical Assembly

詳細は `references/archetypes.md` 参照。

**スロット上限:** 5-7技術（超過は複雑性爆発）

**禁忌例:**
- CoT + o1モデル → 二重推論で冗長化
- EmotionPrompt + Precision → 出力不安定化
- Many-shot + Speed → トークン爆発

---

## Phase 5: Structure Assembly

### Output Format

```yaml
---
name: [skill-name]
description: |
  [1行説明]
  **Trigger:** [起動条件]
---

## Overview
[目的・スコープ 50字以内]

## Core Behavior
[必須動作 箇条書き]

## Quality Standards
[品質基準 定量的に]

## Edge Cases
[境界条件 + Fallback]

## Examples (if applicable)
[入出力例]
```

### Quality Standards（生成物に適用）

| 項目 | 基準 | 検証方法 |
|:---|:---|:---|
| 曖昧語 | 0件 | 「適切」「うまく」等を検出 |
| 定量化 | 100% | 全基準に数値/条件分岐あり |
| Examples | 必須 | 最低1例 |
| Fallback | 必須 | 全Edge Caseに対応 |
| 行数 | ≤500行 | 超過時はreferences/分離 |

### Transformation Tables

**曖昧語 → 具体化**

| Before | After |
|:---|:---|
| 適切に処理 | [条件A]なら[処理X]、[条件B]なら[処理Y] |
| 高品質な | [指標]が[閾値]以上 |
| 必要に応じて | [トリガー条件]を満たした場合のみ |
| できるだけ | 優先度[N]として、[制約]の範囲内で最大化 |

**冗長 → 簡潔**

| Before | After |
|:---|:---|
| 〜することができます | 〜可能 |
| 〜を行う必要があります | 〜必須 |
| 〜の可能性があります | 〜の恐れ / 要検証 |

---

## Phase 6: Pre-Mortem Simulation

生成後、**本番で死ぬ前に**脆弱性を検証。

### Universal Checks（全Archetype共通）

```
□ 空入力 → 明確なエラー or 入力促進
□ 超長文（10,000字超） → 要約 / 分割 / 制限通知
□ 超短文（1語） → 明確化質問
□ 言語混在 → 主言語判定 or 確認
□ Jailbreak試行 → 無視して通常応答
□ 矛盾指示 → トレードオフ確認 or 優先順位適用
□ 知識範囲外 → 限界を明示
□ 能力範囲外 → 限界を明示 + 代替案
```

### Archetype-Specific Checks

**🎯 Precision:**
- 検索結果0件時のハルシネーション抑止
- 矛盾情報源の処理ルール
- 確信度40-60%時の表現適切性
- 「分からない」閾値の明確性

**⚡ Speed:**
- 最複雑入力でも2秒以内か
- 浅い回答でも即時ニーズ充足か
- 圧縮による重要情報欠落なし

**🤖 Autonomy:**
- 10ステップ後の無限ループ回避
- 失敗時Fallback定義済
- 最大試行回数上限設定済
- エスカレーション条件明確

**🎨 Creative:**
- 同一入力10回で十分な多様性
- 多様性追求による支離滅裂回避
- ブランド/キャラ逸脱検知

**🛡 Safety:**
- 既知Jailbreak耐性（DAN, おばあちゃん等）
- 過剰拒否（無害質問拒否）回避
- エラーメッセージの攻撃ヒント排除

### Vulnerability Response

| Level | Action |
|:---|:---|
| Low | ドキュメント注記 |
| Medium | ガードレール追加 |
| High | Phase 4へ戻り再設計 |
| Critical | Archetype再選択 |

---

## Fallback Hierarchy

全生成物に組み込む耐障害設計。

### Confidence Routing

```
確信度 > 80%: 通常回答（修飾なし）
確信度 50-80%: 回答 + 「ただし〇〇の可能性あり」
確信度 30-50%: 「〇〇と思われるが要確認」+ 複数可能性併記
確信度 < 30%: 回答保留 + 「正確な回答には〇〇が必要」+ 代替アクション
```

### Phase-Specific Fallback

| Phase | Failure | Fallback |
|:---|:---|:---|
| 入力解析 | 意図不明 | 言い換え試行 → 確認質問 → 「理解不能」通知 |
| 情報収集 | 結果なし | クエリ変更×3 → 内部知識のみ（確信度-30%） → 「情報なし」通知 |
| 推論 | 失敗 | Step-Back抽象化 → 部分回答 → 専門家推奨 |
| 検証 | 不合格 | 基準緩和 → 不確実性明示出力 → 出力中止 |
| 出力 | 失敗 | フォーマット簡略化 → プレーンテキスト → 技術エラー通知 |

### Escalation Triggers（🤖 Autonomy用）

以下で自律実行停止 → 人間判断委譲:
1. 10回以上リトライ or 実行時間5分超過
2. 連続3回、確信度30%未満の判断
3. 不可逆操作（削除/送信/購入）実行前
4. 内部状態に論理矛盾発生
5. ユーザー明示要求

---

## Anti-Patterns

| Category | NG | 問題 | 対策 |
|:---|:---|:---|:---|
| 設計 | Archetype未定義で技術選定 | 目的なき積み上げ | Phase 1必須 |
| 技術 | 7技術超 | 複雑性爆発 | スロット上限遵守 |
| 構造 | Fallback未定義 | 想定外で停止 | 全Phaseに設置 |
| 検証 | Pre-Mortem省略 | 本番で初発覚 | Phase 6必須 |
| 品質 | 曖昧語残存 | 解釈ブレ | 変換表適用 |

---

## References

詳細は以下を参照:
- `references/archetypes.md` — 5アーキタイプ詳細定義
- `references/quality-checklist.md` — Pre-Mortemチェックリスト完全版
- `references/templates.md` — 3種テンプレート（Code Reviewer, Producer, Mirror）
- `references/transformations.md` — 変換表完全版

---

## Version

| Version | Date | Changes |
|:---|:---|:---|
| 1.0 | 2026-01-04 | 初版 |
| 2.0 | 2026-01-04 | アーキタイプ駆動設計導入 |
| 2.1 | 2026-01-04 | Intent Crystallization, Pre-Mortem, Fallback追加 |
| 3.0 | 2026-01-05 | 400行圧縮、references/分離、統合最適化 |
