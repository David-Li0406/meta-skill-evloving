---
name: reviewing-code
description: Use when executing /code:review-uncommited, /code:review-unpushed, or /code:review-pr commands. Triggers: code review request, PR review, uncommited changes review. Defines 12 parallel review agents covering security, performance, quality, consistency, and more.
---

# Reviewing Code

コードレビューコマンド共通のエージェント定義・起動ルール・結果フォーマット。

## 12 Review Agents

**必ず12個すべてについて起動/スキップを判断し報告すること。**

### pr-review-toolkit（6個）

| # | subagent_type | 用途 | 起動条件 |
|---|---------------|------|----------|
| 1 | `pr-review-toolkit:code-reviewer` | コード品質、バグ検出 | 常に |
| 2 | `pr-review-toolkit:comment-analyzer` | コメント正確性 | 常に |
| 3 | `pr-review-toolkit:pr-test-analyzer` | テストカバレッジ | テストファイル変更時 |
| 4 | `pr-review-toolkit:silent-failure-hunter` | サイレントエラー | 常に |
| 5 | `pr-review-toolkit:type-design-analyzer` | 型設計 | 型定義変更時 |
| 6 | `pr-review-toolkit:code-simplifier` | コード簡素化 | 常に |

### カスタム（6個）

| # | subagent_type | 用途 | 起動条件 |
|---|---------------|------|----------|
| 7 | `code:reinvention-checker` | 車輪の再発明 | 新規関数/クラス追加時 |
| 8 | `code:codebase-alignment-checker` | 整合性・ドメイン・依存関係 | 常に |
| 9 | `code:rules-checker` | プロジェクト固有ルール | skills/rules/存在時 |
| 10 | `code:code-quality-advisor` | AI臭・可読性・デッドコード | 常に |
| 11 | `code:security-checker` | セキュリティ脆弱性 | 常に |
| 12 | `code:performance-checker` | パフォーマンス問題 | 常に |

## 起動ルール

1. **並列実行**: 引数に`parallel`があれば全エージェントを単一メッセージで起動
2. **スキップ報告**: 条件を満たさない場合は理由を明示
3. **起動前報告**: エージェント起動前に起動状況テーブルを表示

## 結果フォーマット

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 [REVIEW TYPE] REVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 起動エージェント: X/12
| エージェント | ステータス | 理由 |
|-------------|-----------|------|
| code-reviewer | 完了 | - |
| pr-test-analyzer | スキップ | テストファイルなし |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 CRITICAL (X件)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### [agent-name] 問題タイトル
📍 `path/to/file.ts:42`
問題のコード
💡 **修正案**: 具体的な修正

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 IMPORTANT (X件)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### [agent-name] 問題タイトル
📍 `path/to/file.ts:42`
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 SUGGESTIONS (X件)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### [agent-name] 提案タイトル
📍 `path/to/file.ts:42`
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GOOD PRACTICES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- [agent-name] 良い点 in `path/to/file.ts`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 ACTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 🔴 [agent] 要約
2. 🟠 [agent] 要約
3. 🟡 [agent] 要約
```

## 必須ルール

- **すべての指摘に `[agent-name]` を付与**
- **ファイルパスは `path:line` 形式**
- **12個全てについて起動/スキップを報告**

## 結果統合ルール（truncation防止）

オーケストレーターは各エージェントの結果を**そのまま**出力する。

**禁止:**
- エージェント結果の要約・省略
- 「同様の指摘が複数あります」等のまとめ
- 指摘数の丸め（「約10件」ではなく「12件」）
- 重複排除による指摘の削除

**必須:**
- 全CRITICAL/IMPORTANTを個別に列挙
- 各指摘のファイル:行番号を保持
- エージェント名の帰属を維持
- スコア閾値未満の指摘は除外してよいが、閾値以上は全て出力
