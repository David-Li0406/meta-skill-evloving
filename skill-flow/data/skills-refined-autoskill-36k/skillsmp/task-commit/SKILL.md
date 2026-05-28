---
name: task-commit
description: "コミット・プッシュを実行するSkill。docs/einja/steering/commit-rules.mdのルールに従い、分割コミットを実施。直接呼び出し可能（確認あり）、task-exec経由では自動実行"
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - AskUserQuestion
  - TodoWrite
  - TodoRead
---

# task-commit Skill: コミット・プッシュ実行エンジン

## 役割

変更をコミット・プッシュします。`docs/einja/steering/commit-rules.md` のコミットルールに厳格に従い、適切な粒度でコミットを分割します。

## 実行手順（6ステップ）

### ステップ1: 最新化（必要な場合のみ）

**⚠️ 重要**: 毎回 `git pull --rebase` を実行するのは非効率。リモートに新しいコミットがある場合のみ実行する。

#### 手順

```bash
# 1. リモートの最新情報を取得（ローカルは変更しない）
git fetch origin

# 2. リモートとの差分を確認
git rev-list HEAD..origin/main --count
```

- **差分が0の場合**: 最新なので何もしない（次のステップへ）
- **差分がある場合**: 以下を実行

```bash
# ローカル変更を一時退避
git stash

# リモートの変更を取り込み
git pull --rebase

# ローカル変更を復元
git stash pop
```

#### コンフリクト発生時

1. **conflict-resolver エージェント** を Task ツールで呼び出して解消
2. 解消できない場合は以下を出力して終了:

```markdown
## 🚀 コミット・プッシュ

### ステータス: ❌ FAILURE

**エラー**: git pull --rebase でコンフリクトが発生し、解消できませんでした。

手動でコンフリクトを解決してください。

\`\`\`
[コンフリクト詳細]
\`\`\`
```

---

### ステップ2: 変更確認

1. `git status` で変更ファイルを確認
2. `git diff` で差分内容を確認
3. **変更がない場合**: 以下を出力して正常終了

```markdown
## 🚀 コミット・プッシュ完了

### ステータス: ✅ SUCCESS（変更なし）

コミット対象の変更がありませんでした。
```

---

### ステップ3: コミット分割方針の決定

**⚠️ 重要**: `docs/einja/steering/commit-rules.md` の「コミットの分割方針」を**必ず**参照すること。

#### 分割基準

以下の場合は**必ず別々のコミットに分割**:

1. **異なる目的や種類の変更**
   - ソースコードの変更とドキュメントの更新
   - 機能追加と設定ファイルの変更
   - リファクタリングとバグ修正

2. **異なるコンポーネントやモジュールの変更**
   - 複数のマイクロサービスやコンポーネントの変更
   - フロントエンドとバックエンドの変更

3. **レビューの容易さを考慮した分割**
   - 大規模な変更は小さな論理的なまとまりに分割
   - テストコードの追加・更新は実装とは別のコミット

#### ユーザーへの確認（必須）

**AskUserQuestionツール**を使用して、コミット分割案の承認を得る。

**⚠️ 重要**: `question` パラメータに**具体的なコミット分割内容を必ず記載**すること。「コミット分割案を確認してください」のような抽象的な質問は**禁止**。

```
AskUserQuestion:
  question: |
    以下のコミット分割案で実行してよろしいですか？

    【コミット1】feat: ユーザー認証機能の追加
    対象: src/auth/login.ts, src/auth/logout.ts, src/auth/middleware.ts

    【コミット2】test: 認証機能のテスト追加
    対象: src/auth/__tests__/login.test.ts, src/auth/__tests__/logout.test.ts
  header: "分割案"
  options:
    - label: "承認"
      description: "この分割案でコミットを実行"
    - label: "1コミットにまとめる"
      description: "すべての変更を1つのコミットにまとめる"
```

**question記載必須項目**:
- 各コミットのメッセージ（プレフィックス付き）
- 各コミットの対象ファイル一覧

ユーザーが「Other」で修正指示を出した場合は、その指示に従って分割案を修正し、再度確認を取る。

---

### ステップ4: 品質チェック

#### task-exec経由での呼び出しの場合

task-exec経由でQA合格後に呼び出されるため、品質チェック（lint/typecheck/test/build）は**スキップ**します。

QAフェーズで既に実行済みのため、重複実行は不要です。

#### 直接呼び出しの場合

コミット前に `pnpm prepush` を実行して以下のチェックを行います:

1. **lint**: lint-staged による変更ファイルの lint チェック
2. **typecheck**: TypeScript の型チェック
3. **test**: 変更ファイルに関連するテストのみ実行（vitest related --run）

`pnpm prepush` が失敗した場合は、エラー内容を報告して終了します。

---

### ステップ5: コミット実行

合意した分割方針に従って順次コミットを実行。

#### コミットメッセージ形式

`docs/einja/steering/commit-rules.md` に従い:

- **プレフィックス**: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`
- **言語**: 日本語
- **形式**: 1行目に概要、2行目以降に詳細

#### コミットコマンド

**task-exec経由での呼び出しの場合**（QA済み）:

```bash
git add src/auth/login.ts src/auth/logout.ts && git commit -m "$(cat <<'EOF'
feat: ユーザー認証機能の追加

- JWT認証の実装
- ログイン・ログアウトエンドポイントの追加
- 認証ミドルウェアの実装
EOF
)"
```

**直接呼び出しの場合**（prepush実行）:

```bash
git add src/auth/login.ts src/auth/logout.ts && pnpm prepush && git commit -m "$(cat <<'EOF'
feat: ユーザー認証機能の追加

- JWT認証の実装
- ログイン・ログアウトエンドポイントの追加
- 認証ミドルウェアの実装
EOF
)"
```

---

### ステップ6: プッシュ実行

1. `git push` を実行
2. 結果を出力

---

## 出力形式

### 成功時

```markdown
## 🚀 コミット・プッシュ完了

### コミットサマリー
- **コミット数**: {count}個
- **変更ファイル数**: {files}個

### コミット一覧
| # | メッセージ | ファイル数 |
|---|----------|----------|
| 1 | feat: ユーザー認証機能の追加 | 3 |
| 2 | test: 認証機能のテスト追加 | 2 |

### プッシュ結果
\`\`\`
[git push の出力]
\`\`\`

### ステータス: ✅ SUCCESS
```

### 失敗時

```markdown
## 🚀 コミット・プッシュ

### ステータス: ❌ FAILURE

**エラー**: [エラーの種類]

\`\`\`
[エラー詳細]
\`\`\`

[推奨される対処方法]
```

---

## エラーハンドリング

| エラー種別 | 対処 |
|-----------|------|
| git pull コンフリクト | conflict-resolver エージェントを Task ツールで呼び出して解消を試行 |
| コンフリクト解消失敗 | 報告して終了、手動解決を依頼 |
| git commit 失敗 | エラー内容を報告 |
| git push 失敗 | エラー内容を報告、原因を説明 |

---

## 参考資料

- `docs/einja/steering/commit-rules.md` - コミットルール、分割方針、メッセージ形式の詳細

---

**最終更新**: 2026-01-10
