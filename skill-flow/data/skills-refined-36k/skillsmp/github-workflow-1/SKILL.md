---
name: github-workflow
description: Understand Conventional Commits, GitHub issue management, and Pull Request workflows. Apply best practices for collaborative development.
metadata:
  author: Bingify
  version: "1.0"
---

# GitHub Workflow & Conventions

このスキルは、Bingifyの開発プロセス・GitHub管理・コミット規約をカバーします。

## 概要

BingifyはConventionalCommitsとGitHubFlowを採用し、チーム開発の効率と品質を保証します。

## Conventional Commits

### コミットメッセージの形式

```text
type(scope): subject
```

### type

- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメント
- `refactor`: リファクタリング
- `perf`: パフォーマンス改善
- `test`: テスト
- `ci`: CI/CD
- `chore`: その他

### 例

```bash
git commit -m "feat(dashboard): add space creation form"
git commit -m "fix(space): resolve slug validation error"
git commit -m "docs: update setup instructions"
```

## ブランチ戦略

```text
main                    # 本番用
feat/dashboard-spaces   # 新機能
fix/auth-redirect       # バグ修正
refactor/api-routes     # リファクタリング
```

## PRワークフロー

1. フィーチャーブランチを作成
2. コミットを積み重ねる
3. PRを作成してレビュー
4. ApprovalをもらってSquash merge

```bash
git switch -c feat/dashboard-spaces
# ... コーディング ...
git commit -m "feat(dashboard): add form"
git push origin feat/dashboard-spaces
# GitHub: Create Pull Request
```

## CI/CDチェック

プルリクエスト作成前に、以下を実行してすべてが成功することを確認してください：

```bash
pnpm check       # Lint + Format（Biome）
pnpm type-check  # TypeScript
pnpm test        # Vitest
```

詳細は [testing スキル](../testing/SKILL.md) を参照してください。

## ドキュメント編集

SKILL.mdを含むMarkdownドキュメント編集後は、コミット前に以下を実行してください：

```bash
pnpm format:docs
```

## GitHub Actions

GitHub Actionsでアクションを使用する際は、以下のルールに従ってください：

- タグ指定（例: `@v4`）ではなく、**フルコミットSHA** を使用
- 末尾に `# vX.Y.Z` の形式でバージョンコメント付与
- Renovateが `helpers:pinGitHubActionDigests` プリセットで自動更新

**例:**

```yaml
- uses: actions/checkout@8e8c483db84b4bee98b60c0593521ed34d9990e8 # v6.0.1
```

**理由:**

- セキュリティ: タグ変更による意図しない挙動変更を防止
- 再現性: ワークフロー実行の厳密な再現が可能
- 監査可能性: 使用されたアクション版を明確に記録

## 参考

- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
