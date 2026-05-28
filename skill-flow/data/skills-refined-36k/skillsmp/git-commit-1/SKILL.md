---
name: git-commit
description: このプロジェクトにおけるGitコミットの手順とコミットメッセージの規約を理解し、適切にコミットできる。
---

# Git Commit

## Workflow

### 1. Pre-commit Checks

コミット前に、コードのフォーマット、静的解析、テストを実行してコードの品質を確保します。

```bash
mise run fix
mise run check
mise run test
```

### 2. Check Staged Changes

コミット可能かどうかを確認するため、まずステージされた変更を確認します。

```bash
git diff --cached --stat
```

もし変更がない場合は、ユーザーに `git add` した上で続行するかを確認します。

### 3. Analyze Diff

変更内容を詳細に確認します。

```bash
git diff --cached
```

### 4. Generate Commit Message

[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) に従ってコミットメッセージを生成します。

#### Format

```
<type>[(scope)]: <subject>

[body]
```

#### Types

- `feat:` - 新機能の追加
- `fix:` - バグ修正
- `refactor:` - リファクタリング
- `docs:` - ドキュメントの追加・更新
- `style:` - フォーマット修正 (コードの動作に影響しない変更)
- `perf:` - パフォーマンス改善
- `test:` - テストコードの追加・修正
- `chore:` - メンテナンス作業

**Common Scopes**: `server`, `config`, `chroma-cli`, `chromad-cli`, `deps`

#### Subject

変更内容を元に「どのような変更を行ったか」を簡潔に伝えます。

- **常に** 現在形の命令形で始める (e.g. `add`, `implement`, `fix`, `improve`, `enhance`, `refactor`, `remove`)
- **常に** タイトルは50文字以内
- **決して** 大文字で始めない
- **決して** ピリオドで終わらせない
- **決して** 内容のないコミットメッセージにしない (e.g. `update`, `fix bugs`)

### 5. Commit Changes

生成したコミットメッセージを使用して変更をコミットします。

```bash
# Simple
git commit -m "<type>[(scope)]: <subject>"
```

```bash
# With Body
git commit -m "$(cat <<'EOF'
<type>[(scope)]: <subject>

[body]
EOF
)"
```

## Commit Message Examples

- `feat(chroma-cli): add new options for foobar`
- `fix(server): resolve validation issue in user input`
- `chore(deps): update Deno to X.Y.Z`
