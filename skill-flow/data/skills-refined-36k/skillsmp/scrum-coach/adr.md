---
name: adr
description: Use when recording significant technical or process decisions. Creates Architecture Decision Record for future reference and team alignment.
allowed-tools: Read, Write
---

# ADR (Architecture Decision Record) 作成

重要な技術的・プロセス的な意思決定を記録する。
将来の参照と、チームの意思決定の透明性確保が目的。

## ADRとは

Architecture Decision Record は、重要な意思決定とその背景を記録するドキュメント。
「なぜその決定をしたか」を将来の自分やチームメンバーが理解できるようにする。

## いつADRを書くか

- 技術スタックの選定（言語、フレームワーク、ライブラリ）
- アーキテクチャパターンの採用
- 外部サービスの選定
- 開発プロセスの変更
- セキュリティポリシーの決定
- 性能要件に関する決定
- その他、後から「なぜこうなった？」と聞かれそうな決定

## 入力

1. **タイトル**: 決定事項の概要
2. **コンテキスト**: 背景、解決したい問題
3. **検討した選択肢**: 比較検討した案
4. **決定内容**: 選んだ案とその理由
5. **関係者**: 決定に関わった人

## 出力フォーマット

```markdown
# ADR: {日本語タイトル}

## メタデータ
- **Status**: Proposed / Accepted / Deprecated / Superseded
- **Date**: {YYYY-MM-DD}
- **Deciders**: {決定に関わった人}
- **Technical Story**: {関連するPBIやIssue番号}

## Context

{この決定が必要になった背景}
{解決したい問題や達成したい目標}

## Decision Drivers

決定の際に重視した基準:
- {基準1}: {説明}
- {基準2}: {説明}
- {基準3}: {説明}

## Considered Options

### Option 1: {選択肢A}
{概要説明}

**Pros:**
- {メリット1}
- {メリット2}

**Cons:**
- {デメリット1}
- {デメリット2}

### Option 2: {選択肢B}
...

### Option 3: {選択肢C}
...

## Decision

**{選択肢X}** を採用する。

## Rationale

{決定の理由}
{Decision Driversに照らしてなぜこの選択肢が最適か}

## Consequences

### Positive
- {ポジティブな影響1}
- {ポジティブな影響2}

### Negative
- {ネガティブな影響1}
- {許容する理由やミティゲーション}

### Risks
- {潜在的なリスク}
- {モニタリング方法}

## Compliance

{セキュリティ、法規制、社内ポリシーへの影響があれば}

## Related

- {関連するADR: ADR-XXX}
- {関連するドキュメント}
- {参考にした外部リソース}

## Notes

{その他の補足情報}
```

## 保存先

```
.claude/docs/adr/{YYYYMMDD}-{日本語タイトル}.md
```

**注意:** このファイルはプロジェクト固有です。
プロジェクトルートの相対パスで保存されます。

例: `.claude/docs/adr/20260118-認証方式の選定.md`

## ADRのステータス

| Status | 意味 |
|--------|-----|
| Proposed | 提案中、まだ承認されていない |
| Accepted | 承認済み、有効 |
| Deprecated | 非推奨、新規には適用しない |
| Superseded | 別のADRで置き換えられた |

## ファイル名の管理

- 日付プレフィックス（YYYYMMDD）で時系列を管理
- 同日に複数作成する場合は末尾に連番を追加（例: `20260118-認証方式-2.md`）

## 良いADRの特徴

- **簡潔**: 必要な情報に絞る
- **客観的**: 事実と根拠に基づく
- **追跡可能**: 関連ドキュメントへのリンク
- **タイムリー**: 決定直後に書く（記憶が新しいうちに）

## 注意事項

- 全ての決定をADRにする必要はない
- 「重要な」「後から理由を聞かれそうな」決定に絞る
- ADRは生きたドキュメント。状況が変われば更新する
- チームで共有し、レビューを受けることが望ましい
