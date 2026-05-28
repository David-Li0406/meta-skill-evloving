---
name: conflict-resolver
description: "gitコンフリクトを解消するSkill（rebase/merge/stash/cherry-pick等に対応）"
invocation: "agent-requested"
allowed-tools:
  - Bash
  - Read
  - Edit
  - Grep
  - AskUserQuestion
---

# conflict-resolver Skill: コンフリクト解消エンジン

## 役割

gitコンフリクト（rebase/merge/stash/cherry-pick等）を1ファイルずつユーザーに確認しながら安全に解消します。

---

## 実行手順

### ステップ1: コンフリクト状態の確認

1. コンフリクトファイルの一覧を表示:
   ```bash
   git diff --name-only --diff-filter=U
   ```

2. 操作タイプを判定（rebase/merge/cherry-pick/stash）:
   ```bash
   # rebase中かどうか
   test -d .git/rebase-merge || test -d .git/rebase-apply

   # merge中かどうか
   test -f .git/MERGE_HEAD

   # cherry-pick中かどうか
   test -f .git/CHERRY_PICK_HEAD
   ```

3. **10件以上の場合**: 一覧を表示し、継続するか中断するか確認

---

### ステップ2: 各ファイルについて1ファイルずつユーザーに確認

各コンフリクトファイルに対して以下を実行:

1. **双方の差分を表示**:
   ```bash
   git diff --ours -- <file>   # HEAD側（現在のブランチ）の変更
   git diff --theirs -- <file> # マージ元の変更
   ```

2. **バイナリファイルの場合**: diff表示が困難な旨を通知

3. **ファイル内容を読み、両方の変更箇所を理解**

4. **AskUserQuestionで各ファイルの解消方針を確認**

   まず、差分内容を説明した後、以下の形式でAskUserQuestionを使用:

   ```yaml
   AskUserQuestion:
     question: "{ファイル名}のコンフリクト解消方法を選択してください"
     header: "コンフリクト解消"
     options:
       - label: "HEAD側を優先"
         description: "現在のブランチの変更を採用。メリット: 現在の実装を維持。デメリット: マージ元の変更が失われる"
       - label: "マージ元を優先"
         description: "マージ元の変更を採用。メリット: 新しい変更を取り込める。デメリット: 現在の実装が上書きされる"
       - label: "マージ案A（両方の変更を統合）"
         description: "{具体的なマージ内容の説明}。メリット: 両方の変更を活かせる。デメリット: 統合による意図しない動作のリスク"
       - label: "マージ案B（別の統合方法）"
         description: "{具体的なマージ内容の説明}。メリット: {利点}。デメリット: {欠点}"
       - label: "このファイルをスキップ"
         description: "後で手動で解消する。メリット: 判断を保留できる。デメリット: 後で対応が必要"
       - label: "操作全体を中断"
         description: "rebase/merge/cherry-pickを中断する。メリット: 安全に元の状態に戻せる。デメリット: これまでの解消作業が無効になる"
   ```

   **重要**: 必ず各ファイルごとにAskUserQuestionを実行し、ユーザーの選択を待つこと。複数ファイルをまとめて質問しない。

---

### ステップ3: 確認後に解消を実行

1. ユーザーが選択した案に従ってファイルを編集
2. `git add <file>` でステージング
3. 編集結果をユーザーに表示して最終確認

---

### ステップ4: 全ファイル解消後

1. **残りコンフリクトの検証**:
   ```bash
   git diff --check
   ```

2. **操作タイプに応じて継続**:
   | 操作タイプ | 継続コマンド |
   |-----------|-------------|
   | rebase | `git rebase --continue` |
   | merge | `git commit` |
   | cherry-pick | `git cherry-pick --continue` |
   | stash | `git stash drop`（解消後） |

3. 追加のコンフリクトがあればステップ2に戻る

---

### ステップ5: 中断・やり直しオプション

ユーザーが中断を希望した場合、操作タイプに応じて中断:

| 操作タイプ | 中断コマンド |
|-----------|-------------|
| rebase | `git rebase --abort` |
| merge | `git merge --abort` |
| cherry-pick | `git cherry-pick --abort` |
| stash | `git checkout -- .` でリセット |

---

## ⚠️ 禁止事項

以下の操作は**絶対に行わない**:

- ユーザー確認なしでのコンフリクト自動解消
- `--ours`や`--theirs`オプションの無断使用
- コンフリクトマーカー（`<<<<<<<`、`=======`、`>>>>>>>`）を残したままのコミット

---

## 出力形式

### 成功時

```markdown
## 🔧 コンフリクト解消完了

### 解消サマリー
- **コンフリクトファイル数**: {count}個
- **操作タイプ**: [rebase / merge / cherry-pick / stash]

### 解消ファイル一覧
| # | ファイル | 解消方法 |
|---|---------|---------|
| 1 | src/auth/login.ts | 両方の変更を取り込み |
| 2 | src/config.ts | HEAD側を優先 |

### ステータス: ✅ SUCCESS
```

### 中断時

```markdown
## 🔧 コンフリクト解消

### ステータス: ⏹️ ABORTED

**理由**: [ユーザーが中断を選択 / 手動解消を希望]

操作は中断されました。以下のコマンドで状態を確認できます:
\`\`\`bash
git status
\`\`\`
```

### 失敗時

```markdown
## 🔧 コンフリクト解消

### ステータス: ❌ FAILURE

**エラー**: [エラー内容]

\`\`\`
[エラー詳細]
\`\`\`

[推奨される対処方法]
```

---

**最終更新**: 2025-01-05
