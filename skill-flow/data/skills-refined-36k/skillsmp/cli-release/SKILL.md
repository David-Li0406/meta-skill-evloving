---
name: cli-release
description: "@einja/cli パッケージをビルド・テストし、NPMに公開するSkill"
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - AskUserQuestion
  - TodoWrite
  - TodoRead
  - Task
  - MCPSearch
---

# cli-release Skill: @einja/cli パッケージ公開エンジン

## 役割

`@einja/cli` パッケージをビルド・テストし、NPMに公開します。

## 参照ドキュメント

- `packages/cli/RELEASING.md` - 詳細なリリース手順、トラブルシューティング、NPM_TOKEN設定方法

## 実行手順

### 1. 前提条件の確認

```bash
git branch --show-current    # mainブランチであること
git status --porcelain       # 未コミット変更の確認
```

#### 未コミット変更がある場合

**AskUserQuestion**で対処方法を確認:

- **コミットしてからリリース**: 全ての変更をコミット・プッシュ後にリリース
- **スタッシュしてリリース**: 変更を一時退避してリリース後に復元
- **そのままリリース**: 未コミット変更は放置し、**package.jsonのバージョン更新のみ**コミットしてリリース

### 2. バージョン種別の決定

現在のバージョンと最近の変更を表示後、**AskUserQuestion**で確認:

- patch（推奨）: バグ修正・軽微な改善
- minor: 後方互換性のある機能追加
- major: 破壊的変更

### 3. ビルド・テスト

```bash
pnpm --filter @einja/cli build
pnpm --filter @einja/cli test
pnpm --filter @einja/cli typecheck
```

### 4. バージョン更新・コミット・プッシュ

#### 通常パターン（未コミット変更なし）

```bash
cd packages/cli
npm version {patch|minor|major}
git push origin main
git push origin cli-v{version}
```

#### 未コミット変更ありでそのままリリースする場合

```bash
npm version {patch|minor|major} --no-git-tag-version --prefix packages/cli
```

**重要**: 未コミット変更は放置し、**package.jsonのみ**をコミット:

```bash
# package.jsonのみステージング
git add packages/cli/package.json

# バージョン更新のみコミット
git commit -m "chore(cli): v{version}にバージョンアップ"

# タグ作成
git tag cli-v{version}

# プッシュ
git push origin main
git push origin cli-v{version}
```

task-committer には委託しない（全変更をコミットしてしまうため）。

### 5. GitHub Actions 監視・自律修正

タグプッシュ後、GitHub Actions の完了を監視する。

#### 5.1 監視ループ

```bash
# 最新のワークフロー実行を取得
gh run list --workflow=release-cli.yml --limit=1 --json databaseId,status,conclusion

# 出力例: [{"databaseId":123,"status":"in_progress","conclusion":null}]
```

- `status: in_progress` → 30秒待機して再確認
- `status: completed, conclusion: success` → 成功、ステップ6へ
- `status: completed, conclusion: failure` → 失敗、5.2へ

#### 5.2 失敗時の原因特定

```bash
gh run view {run_id} --log-failed
```

#### 5.3 原因別の自律修正

| 原因 | 対処 |
|------|------|
| ビルドエラー | コードを修正 |
| テストエラー | テストを修正 |
| NPM_TOKEN エラー | ユーザーに設定確認を依頼して終了 |
| バージョン重複 | 次のpatchバージョンで再実行 |

#### 5.4 修正後の再リリース

**重要**: 同じタグ名は使えないため、バージョンを上げて再リリース

```bash
# 1. 修正をコミット
git add -A
git commit -m "fix(cli): CIエラーを修正"

# 2. 新しいバージョンに更新
npm version patch --no-git-tag-version --prefix packages/cli

# 3. バージョン更新をコミット
git add packages/cli/package.json
git commit -m "chore(cli): v{new_version}にバージョンアップ"

# 4. 新しいタグを作成・プッシュ
git tag cli-v{new_version}
git push origin main
git push origin cli-v{new_version}
```

#### 5.5 リトライ制限

最大3回まで自動リトライ。3回失敗したらユーザーに報告して終了。

### 6. 完了報告

```markdown
## 📦 @einja/cli リリース完了

### リリース情報
- **バージョン**: {old} → {new}
- **タグ**: cli-v{version}

### GitHub Actions
- **ステータス**: ✅ SUCCESS
- **URL**: https://github.com/einja-inc/einja-management-template/actions/runs/{run_id}

### 確認コマンド
npm view @einja/cli
npx @einja/cli --version
```

---

**最終更新**: 2025-01-10
