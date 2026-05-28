---
name: create-branch
description: プロジェクトのブランチ命名規則に従ってGitブランチを作成。「ブランチお願い」「ブランチを作って」「ブランチ作って」「ブランチを切って」「新しいブランチで作業」などと言われた時、または新しい作業・機能開発・バグ修正を開始する前に使用
allowed-tools:
  - Read
  - Bash
---

# Create Branch

このスキルはプロジェクトのブランチ命名規則に従って新しいGitブランチを作成します。

## 実行手順

### 1. ブランチ戦略の確認

まず`README.md`を読み込んで、プロジェクトのブランチ命名規則を理解してください：

```bash
Read README.md
```

特に「ブランチ戦略とPull Request運用」セクションの「ブランチ構成」を確認します。

**許可されるブランチプレフィックス**：
- `feature/*`: 新機能開発用
- `bugfix/*`: 通常のバグ修正用
- `hotfix/*`: 緊急修正用
- `refactor/*`: リファクタリング用
- `chore/*`: 設定変更・ビルド関連用
- `test/*`: テストコード追加・修正用
- `tmp/*`: 一時作業用

### 2. 現在のブランチと利用可能なブランチの確認

```bash
git branch --show-current
git branch -a
```

で現在のブランチと利用可能なブランチを確認します。

**分岐元ブランチの選択**：
- `hotfix/*`: `main`から分岐
- **その他すべて**: `staging`が存在する場合は`staging`、存在しない場合は`main`から分岐

### 3. ブランチ名の決定

ユーザーの要望に基づいて適切なブランチ名を決定：

**命名規則**：
- プレフィックス + `/` + 説明（kebab-case）
- 例:
  - `feature/add-user-profile`
  - `bugfix/fix-login-error`
  - `refactor/improve-database-queries`
  - `chore/update-dependencies`
  - `test/add-user-controller-tests`

**判断基準**：
- 新機能追加 → `feature/*`
- バグ修正 → `bugfix/*`
- 緊急修正 → `hotfix/*`
- コードの改善（動作は変わらない） → `refactor/*`
- 設定変更、依存関係更新、ビルド関連 → `chore/*`
- テスト追加・修正 → `test/*`
- 試行錯誤、一時的な作業 → `tmp/*`

### 4. ユーザー確認

以下の git checkout コマンド形式でユーザーに提示し、ブランチ作成の許可を得てください：

```bash
git checkout -b feature/add-user-search
```

**分岐元ブランチ**: staging (または main)
**判断根拠**: 新機能追加のため `feature/*` プレフィックスを使用

**重要**: ユーザーの許可なしにブランチを作成しないでください。

### 5. ブランチ作成

**必要に応じて分岐元ブランチに移動**：
```bash
# stagingが存在し、hotfix以外の場合
git checkout staging

# stagingが存在しない場合、またはhotfixの場合
git checkout main
```

**新しいブランチを作成**：
```bash
git checkout -b <branch-name>
```

プロジェクトにはGit Hooksが設定されており、ブランチ名が命名規則に従っているかチェックされます。

もし拒否された場合は、エラーメッセージを確認して適切な名前に修正してください：

```bash
git branch -m <new-branch-name>
```

### 6. 確認

```bash
git branch --show-current
```

で新しいブランチに切り替わったことを確認します。

## チェックリスト

- [ ] README.mdを読み込んでブランチ命名規則を確認した
- [ ] `git branch -a`で利用可能なブランチを確認した
- [ ] 分岐元ブランチを正しく選択した（`staging`が存在する場合は`staging`、存在しない場合やhotfixの場合は`main`）
- [ ] 作業内容に適したプレフィックスを選択した
- [ ] kebab-case形式でブランチ名を決定した
- [ ] ブランチ名と分岐元をユーザーに提示した
- [ ] ユーザーの許可を得てからブランチを作成した
- [ ] ブランチが正常に作成されたことを確認した

## よくある間違い

❌ **間違い**: `git branch -a`でブランチ確認せずに`staging`から分岐
✅ **正解**: 必ず`git branch -a`で`staging`の存在を確認してから分岐

❌ **間違い**: `fix-login-error`（プレフィックスなし）
✅ **正解**: `bugfix/fix-login-error`

❌ **間違い**: `feature/AddUserProfile`（PascalCase）
✅ **正解**: `feature/add-user-profile`（kebab-case）

❌ **間違い**: `bug/fix-error`（bugではなくbugfix）
✅ **正解**: `bugfix/fix-error`

## 使用例

### 例1: 新機能開発の場合（stagingあり）

**ステップ1**: ブランチ確認
```bash
git branch -a
# staging が存在することを確認
```

**ステップ2**: ユーザーに提示
```bash
git checkout -b feature/add-user-profile
```

**分岐元ブランチ**: staging
**判断根拠**: 新機能追加のため `feature/*` プレフィックスを使用

**ステップ3**: ユーザーの許可を待つ

**ステップ4**: 許可後にブランチ作成
```bash
git checkout staging
git checkout -b feature/add-user-profile
```

### 例2: バグ修正の場合（stagingなし）

**ステップ1**: ブランチ確認
```bash
git branch -a
# staging が存在しないことを確認
```

**ステップ2**: ユーザーに提示
```bash
git checkout -b bugfix/fix-login-error
```

**分岐元ブランチ**: main
**判断根拠**: バグ修正のため `bugfix/*` プレフィックスを使用

**ステップ3**: ユーザーの許可を待つ

**ステップ4**: 許可後にブランチ作成
```bash
git checkout main
git checkout -b bugfix/fix-login-error
```

### 例3: リファクタリングの場合（stagingあり）

**ステップ1**: ブランチ確認
```bash
git branch -a
# staging が存在することを確認
```

**ステップ2**: ユーザーに提示
```bash
git checkout -b refactor/improve-database-queries
```

**分岐元ブランチ**: staging
**判断根拠**: リファクタリングのため `refactor/*` プレフィックスを使用

**ステップ3**: ユーザーの許可を待つ

**ステップ4**: 許可後にブランチ作成
```bash
git checkout staging
git checkout -b refactor/improve-database-queries
```

### 例4: 緊急修正の場合

**ステップ1**: ブランチ確認
```bash
git branch -a
```

**ステップ2**: ユーザーに提示
```bash
git checkout -b hotfix/fix-security-issue
```

**分岐元ブランチ**: main
**判断根拠**: 緊急修正のため `hotfix/*` プレフィックスを使用（hotfixは常にmainから分岐）

**ステップ3**: ユーザーの許可を待つ

**ステップ4**: 許可後にブランチ作成
```bash
git checkout main
git checkout -b hotfix/fix-security-issue
```

## 注意事項

- ブランチ作成前に必ず`git branch -a`で利用可能なブランチを確認してください
- `hotfix/*`ブランチは常に`main`から分岐し、`main`へマージします
- その他のブランチは`staging`が存在する場合は`staging`から分岐し`staging`へマージ、存在しない場合は`main`から分岐し`main`へマージします
