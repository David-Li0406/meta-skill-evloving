---
name: claude-code-command-author
description: >
  Claude Codeのカスタムslash command（Commands）を設計・生成・更新する。
  「/コマンドを作りたい」「この作業を毎回同じ手順でやりたいのでコマンド化したい」「.claude/commandsにテンプレを追加したい」
  「Claude Codeのcommands作って」「スラッシュコマンド作成」「引数付きコマンド」「allowed-toolsを設定したい」などの依頼で発動する。
  プロジェクト用(.claude/commands)・個人用(~/.claude/commands)・サブディレクトリ(namespacing)・引数($ARGUMENTS/$1..)・bash事前実行(!)・ファイル参照(@)・context:fork などに対応する。
---

# Claude Code Command Author

ユーザーの要望を **Claude Code の Custom slash command（Markdownファイル）** に落とし込み、再利用可能なコマンドとして追加できる状態にする。

## Goals
- ユーザーの依頼から **コマンドの目的・引数・出力**を明確化する
- **正しいコマンドファイル（YAML frontmatter + Markdown本文）**を生成する
- 置き場所・命名・引数設計・事前コンテキストなどを適切に選定する
- ユーザーがそのまま `.claude/commands/` または `~/.claude/commands/` に置ける形で出力する

## Non-goals
- Skillの作成（それは`skill-skillsmith`の役割）
- コマンド自体を実行すること（生成・設計まで）

---

## Inputs
- コマンドで何をしたいか（目的）
- コマンド名の候補（任意、なければ提案）
- スコープ（project / personal、任意）
- 引数の要件（任意）
- 事前に埋め込みたいコンテキスト（任意、git status/diff等）

## Outputs
1. **作成/更新するファイルパス**（例: `.claude/commands/review-pr.md`）
2. **ファイル内容（完成版Markdown）**
3. **利用例＆テスト手順**（`/help`で確認、実行例）

---

## Instructions

### Step 0: 要件の最小セットを確定する
不足している場合は **最小限だけ** 確認する（質問攻めにしない）。

確認項目：
- コマンド目的（何をしたい？何を出力したい？）
- コマンド名候補（`/review-pr` 的なやつ）
- スコープ: project (`.claude/commands/`) or personal (`~/.claude/commands/`)
- 引数設計: フリーフォーム(`$ARGUMENTS`) or 位置引数(`$1`, `$2`, ...)
- 事前コンテキスト: bash埋め込み(!) / ファイル参照(@)
- 安全性: 読み取り中心？書き換えあり？

**デフォルト方針**（ユーザーが指定しない場合）：
- スコープ: project（`.claude/commands/`）
- コマンド性質: 読み取り中心（安全）
- 引数: 1つなら `$ARGUMENTS`、複数の役割があるなら `$1..`

### Step 1: パスと命名を決める
- コマンド名は **ファイル名（`.md`除く）** で決まる
- 命名は **kebab-case**（例: `review-pr.md` → `/review-pr`）
- namespacingしたい場合はサブディレクトリ
  - 例: `.claude/commands/frontend/test.md`
  - ※サブディレクトリはコマンド名に影響しない（表示上の区別）
- 衝突回避: projectとpersonalが同名ならprojectが優先

### Step 2: frontmatter を設計する
必須：
- `description`: 何をするコマンドか（`/help`で表示される）

推奨：
- `argument-hint`: 補完時に出る引数ヒント（引数ありの場合）

必要に応じて：
- `allowed-tools`: ! bash実行を使うなら必要（最小権限で）
- `model`: 特定モデル固定したい場合
- `context: fork` + `agent`: 会話を汚したくない/重い作業を分離
- `disable-model-invocation: true`: Skill toolからの自動呼び出しを避けたい

### Step 3: 引数の受け取り設計
- まとめて扱う: `$ARGUMENTS`
- 役割がある: `$1`, `$2`, `$3`（PR番号、優先度、担当など）
- `argument-hint`でユーザーが迷わない形にする

### Step 4: コマンド本文を設計する
本文は「Claudeにやってほしいこと」を **手順＋出力仕様** で書く。

推奨構造：
- 目的（何を達成するか）
- 入力（引数、参照ファイル、前提）
- 手順（箇条書き）
- 出力形式（Markdown、チェックリスト、差分提案など）
- 制約（例: 「ファイル編集は禁止」「提案のみ」など）
- 完了条件（DoD）

### Step 5: 事前コンテキスト埋め込み（必要なら）
#### bash事前実行（!）
```
!`git status`
!`git diff HEAD`
```
- `allowed-tools`で`Bash(...)`を許可する
- 危険なコマンドは許可しない（`rm`, `curl`, `deploy`等は原則不可）

#### ファイル参照（`@path`）
- `@src/...`のように書くとファイル内容をコンテキストに含められる
- コマンド目的に直結する最小限のファイルだけ参照する

### Step 6: 最終アウトプットを生成する
以下の3点をユーザーに渡す：
1. 作成/更新するファイルパス
2. ファイル内容（完成版）
3. 利用例＆テスト手順

---

## Output format (MUST)

```md
## Files
- .claude/commands/<command-name>.md

## .claude/commands/<command-name>.md
\```md
---
description: <short description>
argument-hint: [optional-args]
---

# <Command Title>

## Your task
- ...

## Constraints
- ...

## Output
- ...
\```

## Usage
- `/command-name [args]`
- 確認: `/help` で description が表示されるか
```

---

## Quality Checklist
- [ ] 置き場所は正しいか（project `.claude/commands/` / personal `~/.claude/commands/`）
- [ ] ファイル名がコマンド名として適切か（`kebab-case`）
- [ ] `description` が入っているか（/helpで分かる）
- [ ] 引数があるなら `argument-hint` があるか
- [ ] `$ARGUMENTS` / `$1..` の設計が目的に合っているか
- [ ] ! を使うなら `allowed-tools` に Bash が適切に絞られているか
- [ ] `@file` 参照は最小限か
- [ ] 制約（編集禁止など）が明記されているか
- [ ] `/help` と実行例のテスト手順が書かれているか

---

## Examples

### Example 1
ユーザー: 「PRレビューを毎回同じ観点でやりたいから `/review-pr` 作って。引数はPR番号と優先度と担当。」

→ `.claude/commands/review-pr.md` を生成。`$1..` + `argument-hint` あり。

### Example 2
ユーザー: 「コミットメッセージ作成をコマンド化したい。実行前にgit statusとdiffを入れて。」

→ `allowed-tools` + ! を使うコマンドを生成（危険コマンドは許可しない）。

### Example 3
ユーザー: 「このリポジトリの特定ファイルを説明する `/explain-file` を作って。パスを引数で渡す。」

→ `$ARGUMENTS` で受け、@参照を使う運用を提案。

### Example 4（非対象）
ユーザー: 「このPRをレビューして」

→ これは "コマンド生成" ではなく "レビュー実行"。本Skillは発動せず、通常対応。

---

## Guardrails
- 破壊的操作（削除/デプロイ/課金リソース作成など）を含むコマンドは、明示的なユーザー同意がある場合のみ設計する
- `allowed-tools` は最小権限。可能なら read-only（`git status`, `git diff`）に限定
- ファイル編集を伴う用途では「編集範囲」「バックアップ方針」「確認ステップ」をコマンド本文に含める

---

## References
- [Slash commands - Claude Code Docs](https://code.claude.com/docs/en/slash-commands)
- [Agent Skills - Claude Code Docs](https://code.claude.com/docs/en/skills)
- 詳細仕様: @reference.md
- テンプレート: @templates/
