# Claude Code Command Author Reference

このファイルは SKILL.md を薄く保つための詳細資料。

---

## Claude Code Commands 仕様（公式準拠）

### 配置場所
| スコープ | パス | 用途 |
|---------|------|------|
| project | `.claude/commands/` | チーム共有、リポジトリにコミット |
| personal | `~/.claude/commands/` | 個人用、マシン固有 |

**優先度**: 同名の場合、project が personal を上書きする

### ファイル名 → コマンド名
- `review-pr.md` → `/review-pr`
- `frontend/test.md` → `/test`（サブディレクトリは表示上の区別のみ）
- kebab-case 推奨

---

## Frontmatter 項目一覧

### 必須（強く推奨）
| 項目 | 説明 | 例 |
|------|------|-----|
| `description` | `/help` で表示。Skill tool からの発動判定にも使用 | `PR を security/performance/style でレビュー` |

### 推奨
| 項目 | 説明 | 例 |
|------|------|-----|
| `argument-hint` | 補完時に表示される引数ヒント | `[pr-number] [priority]` |
| `allowed-tools` | `!` bash実行で許可するツール | `Bash(git status:*), Bash(git diff:*)` |

### 任意
| 項目 | 説明 | 例 |
|------|------|-----|
| `model` | 使用モデルを固定 | `claude-sonnet-4-20250514` |
| `context` | `fork` で会話を分離 | `fork` |
| `agent` | fork時のエージェントタイプ | `general-purpose` |
| `disable-model-invocation` | Skill tool からの自動呼び出しを無効化 | `true` |
| `hooks` | コマンド実行中のフック | （hooks仕様参照） |

---

## 引数の受け取り方

### $ARGUMENTS（フリーフォーム）
```md
Review the following: $ARGUMENTS
```
- 引数全体を1つの文字列として受け取る
- シンプルな用途に最適

### 位置引数（$1, $2, ...）
```md
---
argument-hint: [pr-number] [priority] [assignee]
---

Review PR #$1 with priority $2 and assign to $3.
```
- 役割が明確な複数引数に最適
- 未指定の引数は空文字になる

---

## 事前コンテキスト埋め込み

### bash事前実行（`!`）
コマンド本文で `!` を使うと、実行前にbashを走らせて出力を埋め込める。

```md
---
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*)
---

## Context
- status: !`git status`
- diff: !`git diff HEAD`
- recent commits: !`git log --oneline -10`
```

**重要**:
- `allowed-tools` でBashを許可する必要がある
- read-onlyコマンドに限定（`rm`, `curl`, `deploy` 等は許可しない）

### ファイル参照（`@path`）
```md
Review the following file: @src/main.ts

Or dynamically:
Review the file at: @$1
```
- ファイル内容がコンテキストに含まれる
- コマンド目的に直結する最小限のファイルだけ参照

---

## allowed-tools の書き方

### パターン
```yaml
# 特定コマンド
allowed-tools: Bash(git status:*)

# 複数コマンド
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*)

# 引数パターン
allowed-tools: Bash(npm test:*)
```

### 安全なコマンド例（許可OK）
- `git status`, `git diff`, `git log`, `git branch`
- `ls`, `cat`, `head`, `tail`（読み取り系）
- `npm test`, `npm run lint`（テスト系）
- `echo`, `date`, `pwd`

### 危険なコマンド例（原則許可しない）
- `rm`, `rmdir`, `mv`（破壊系）
- `curl`, `wget`（外部通信）
- `npm install`, `pip install`（パッケージ変更）
- `git push`, `git commit`（リポジトリ変更）
- `deploy`, `kubectl apply`（インフラ変更）

---

## context: fork の使い方

会話を汚したくない、または重い処理を分離したい場合：

```md
---
description: 重い分析タスク
context: fork
agent: general-purpose
---

<やること>
```

**agent の選択肢**:
- `general-purpose`: 汎用（デフォルト）
- `explore`: コードベース探索
- 他のカスタムエージェント

---

## トリガー語（description に入れる）

description に以下の語を含めると発動しやすくなる：

### コマンド作成依頼
- 「コマンド作って」「commands作成」「スラッシュコマンド」
- 「毎回同じ手順で」「コマンド化」「再利用」
- 「.claude/commands」「~/.claude/commands」
- 「/xxx を作って」

### コマンド機能キーワード
- 「引数付き」「$ARGUMENTS」「$1」
- 「git statusを埋め込み」「!` で実行」
- 「@ファイル参照」「ファイル内容を含める」
- 「fork」「会話を分離」

---

## よくあるパターン

### パターン1: シンプルなレビュー系
- 読み取り専用
- 引数は `$ARGUMENTS` で受け取り
- 出力はMarkdown

### パターン2: git状態を使う系
- `allowed-tools` で git コマンドを許可
- `!` で status/diff/log を埋め込み
- コミットメッセージ生成、差分レビューなど

### パターン3: ファイル分析系
- `@` でファイル参照
- 引数でパスを受け取り
- 説明、リファクタ提案など

### パターン4: 分離実行系
- `context: fork` で会話を汚さない
- 重い分析、長いタスク向け
- 結果だけ返す

---

## 命名規則

### コマンド名（ファイル名）
- kebab-case: `review-pr`, `explain-file`, `generate-commit`
- 動詞-名詞 または 名詞-動詞
- 短く、意図が分かる

### 避けるべき名前
- 既存の組み込みコマンドと衝突（`/help`, `/clear` 等）
- 一般的すぎる（`/do`, `/run`, `/go`）
- 長すぎる（20文字超）

---

## デバッグ・テスト手順

1. **配置確認**
   ```bash
   ls -la .claude/commands/
   ```

2. **`/help` で表示確認**
   - description が表示されるか
   - argument-hint が表示されるか

3. **実行テスト**
   ```
   /command-name test-arg
   ```
   - 期待通りの動作か
   - エラーがないか

4. **引数テスト**
   - 引数なしで実行
   - 引数ありで実行
   - 複数引数で実行

---

## 参考リンク
- [Slash commands - Claude Code Docs](https://code.claude.com/docs/en/slash-commands)
- [Agent Skills - Claude Code Docs](https://code.claude.com/docs/en/skills)
