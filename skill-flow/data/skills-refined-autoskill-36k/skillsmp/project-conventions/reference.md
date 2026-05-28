# Project Conventions リファレンス

## Pre-commit Hooks詳細

### 設定されているHooks

Polibaseでは以下のpre-commit hooksが設定されています：

#### 1. Ruff (Linter & Formatter)
```yaml
# .pre-commit-config.yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  hooks:
    - id: ruff
      args: [--fix]
    - id: ruff-format
```

**チェック内容:**
- コードスタイル違反
- 未使用インポート
- 未使用変数
- コードの複雑度
- 自動修正可能なエラー

**修正方法:**
```bash
# 自動修正
uv run ruff check --fix .
uv run ruff format .
```

#### 2. Pyright (Type Checker)
```bash
# 型チェック
uv run pyright
```

**チェック内容:**
- 型アノテーションの正確性
- 型の不整合
- None チェック
- 未定義変数

**修正方法:**
```python
# ❌ 型エラー
def process(data):
    return data.upper()

# ✅ 型アノテーション追加
def process(data: str) -> str:
    return data.upper()
```

#### 3. Prettier (Markdown, JSON, YAML)
```yaml
- repo: https://github.com/pre-commit/mirrors-prettier
  hooks:
    - id: prettier
```

**チェック内容:**
- Markdownフォーマット
- JSONフォーマット
- YAMLフォーマット

**修正方法:**
```bash
# 自動修正
npx prettier --write "**/*.{md,json,yaml,yml}"
```

### Hooks失敗時の対処法

#### パターン1: Ruff違反

**エラー例:**
```
ruff....................................................................Failed
- hook id: ruff
- exit code: 1

src/example.py:10:5: F841 Local variable `unused_var` is assigned to but never used
```

**修正方法:**
```python
# ❌ 未使用変数
def process():
    unused_var = "test"  # 使われていない
    return "result"

# ✅ 修正
def process():
    return "result"
```

#### パターン2: Pyright型エラー

**エラー例:**
```
pyright.................................................................Failed
  error: Argument of type "None" cannot be assigned to parameter "name" of type "str"
```

**修正方法:**
```python
# ❌ None許可していない
def greet(name: str) -> str:
    return f"Hello, {name}"

result = greet(None)  # エラー

# ✅ Optionalを使用
from typing import Optional

def greet(name: Optional[str]) -> str:
    if name is None:
        return "Hello, Guest"
    return f"Hello, {name}"

result = greet(None)  # OK
```

#### パターン3: Prettier違反

**エラー例:**
```
prettier................................................................Failed
README.md needs formatting
```

**修正方法:**
```bash
# 自動修正
npx prettier --write README.md
```

### 設定ファイルでの除外

一時的に特定のファイルやルールを除外する必要がある場合：

#### Ruffの除外

```toml
# pyproject.toml
[tool.ruff]
# ファイル除外
exclude = [
    "legacy_code.py",
    "generated/**/*",
]

# ルール除外
ignore = [
    "E501",  # Line too long
]
```

#### Pyrightの除外

```toml
# pyproject.toml
[tool.pyright]
exclude = [
    "legacy/",
    "**/__pycache__",
]
```

#### Pre-commit全体の除外

```yaml
# .pre-commit-config.yaml
exclude: ^(legacy/|generated/)
```

## CI/CD運用

### テストスキップのガイドライン

#### スキップが許可される場合

1. **既知のバグで修正作業中**
   - 修正PRが既に作成されている
   - Issue番号が明記されている

2. **外部依存の一時的な問題**
   - APIサービスのダウン
   - 外部ライブラリのバグ

3. **パフォーマンステスト（時間がかかる）**
   - nightly buildで実行予定
   - リソース制約

#### スキップ手順

##### 1. GitHub Actions設定
```yaml
# .github/workflows/test.yml
- name: Run integration tests
  run: pytest tests/integration/
  continue-on-error: true  # スキップ
  id: integration-tests

- name: Comment on failure
  if: steps.integration-tests.outcome == 'failure'
  run: |
    echo "Integration tests failed. See issue #123"
```

##### 2. Issue作成
```bash
gh issue create \
  --title "[CI] Integration tests skipped" \
  --body "$(cat <<'EOF'
## 問題
CI/CDで Integration tests をスキップしています

## スキップ理由
外部APIサービスのレート制限により、CI環境でテストが不安定

## 修正方法
1. テストをモック化する
2. 外部APIへの依存を減らす
3. リトライロジックを追加

## 関連
- PR: #456
- Workflow: https://github.com/user/repo/actions/runs/123

## 優先度
高
EOF
)" \
  --label "ci,high-priority"
```

### CI/CD失敗時のデバッグ

#### ログ確認
```bash
# GitHub Actions ログ確認
gh run view <run-id> --log

# 特定ステップのログ
gh run view <run-id> --log --job <job-id>
```

#### ローカル再現
```bash
# GitHub Actions をローカルで実行
act -j test

# 特定のワークフローのみ
act -j test -W .github/workflows/test.yml
```

## ファイル管理

### tmp/ ディレクトリ構造

```
tmp/
├── planning/          # 計画書、設計書
│   ├── 2025-01-15_feature_planning.md
│   └── 2025-01-16_architecture_decision.md
├── analysis/          # 分析結果
│   ├── performance_analysis.md
│   └── code_coverage_report.html
├── experiments/       # 実験用スクリプト
│   ├── test_api.py
│   └── benchmark.py
├── debug/             # デバッグ用ファイル
│   └── error_log_2025-01-15.txt
└── generated/         # 生成ファイル
    └── diagram.png
```

### _docs/ ディレクトリ詳細

#### thinking/ (技術判断の記録)

**例: API設計の判断**
```markdown
# 2025-01-15_api_design_decision.md

## 状況
新しいREST APIエンドポイントの設計

## 検討した選択肢
1. GraphQL
   - 利点: 柔軟なクエリ、over-fetching防止
   - 欠点: 学習コスト、複雑性

2. REST API
   - 利点: シンプル、既存システムと統一
   - 欠点: 複数エンドポイント必要

## 決定
REST APIを採用

## 理由
- チーム全員がRESTに慣れている
- 既存システムとの一貫性
- シンプルなユースケース

## 影響
- src/interfaces/api/ に新しいエンドポイント追加
- OpenAPIスキーマ更新
```

#### features/ (機能の記録)

**例: 新機能実装**
```markdown
# 2025-01-15_議員団管理機能.md

## 機能概要
議員団（会派）の管理機能を実装

## 実装内容
- Entity: ParliamentaryGroup
- Repository: IParliamentaryGroupRepository
- UseCase: ManageParliamentaryGroupUseCase

## 完了条件
- [x] エンティティ定義
- [x] リポジトリ実装
- [x] ユースケース実装
- [x] テスト作成
- [x] UI追加

## 参考
- PR: #789
- Issue: #750
```

#### deleted/ (削除の記録)

**例: レガシーコード削除**
```markdown
# 2025-01-15_legacy_politician_model削除.md

## 削除したもの
src/models/politician.py

## 削除理由
- Clean Architectureへの移行完了
- src/domain/entities/politician.py に移行済み
- 重複コードの解消

## 影響
- なし（すべての参照を更新済み）
- テストもすべて移行済み

## 関連
- PR: #640
- Migration Guide: docs/CLEAN_ARCHITECTURE_MIGRATION.md
```

## トラブルシューティング

### 問題1: Pre-commit hooksが通らない

**症状:**
```bash
$ git commit -m "Add feature"
ruff....................................................................Failed
```

**解決方法:**
```bash
# 1. エラー内容を確認
git commit -m "Add feature"  # エラーメッセージを読む

# 2. 自動修正を試す
uv run ruff check --fix .
uv run ruff format .

# 3. 再度コミット
git add .
git commit -m "Add feature"
```

### 問題2: 型エラーが解決できない

**症状:**
```
Argument of type "dict[str, Any]" cannot be assigned to parameter "data" of type "MyModel"
```

**解決方法:**
```python
# ❌ 型が合わない
from typing import Dict, Any

def process(data: MyModel):
    ...

process({"key": "value"})  # エラー

# ✅ 型を変換
def process(data: MyModel):
    ...

raw_data: Dict[str, Any] = {"key": "value"}
model = MyModel(**raw_data)
process(model)  # OK
```

### 問題3: CI/CDが遅い

**原因:**
- 不要なテスト実行
- キャッシュ未使用
- 並列化していない

**解決方法:**
```yaml
# .github/workflows/test.yml

# キャッシュ追加
- uses: actions/cache@v3
  with:
    path: ~/.cache/uv
    key: ${{ runner.os }}-uv-${{ hashFiles('**/uv.lock') }}

# 並列実行
strategy:
  matrix:
    python-version: [3.11]
    test-group: [unit, integration, e2e]

# テストグループごとに並列実行
- name: Run tests
  run: pytest tests/${{ matrix.test-group }}/
```

## ベストプラクティス

### コミットメッセージ

```bash
# ✅ 良い例
git commit -m "[PBI-001] 議員団管理機能を実装"
git commit -m "Fix: 話者マッチングのバグ修正"
git commit -m "Refactor: リポジトリパターンに統一"

# ❌ 悪い例
git commit -m "update"
git commit -m "fix bug"
git commit -m "WIP"
```

### PR説明

```markdown
## 概要
議員団管理機能を実装

## 変更内容
- Entity: ParliamentaryGroup
- Repository: IParliamentaryGroupRepository
- UseCase: ManageParliamentaryGroupUseCase
- UI: 議員団管理画面

## テスト
- [ ] ユニットテスト追加
- [ ] 統合テスト追加
- [ ] 手動テスト完了

## チェックリスト
- [ ] Pre-commit hooks通過
- [ ] CI/CD通過
- [ ] ドキュメント更新

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### コードレビュー

#### レビュー観点
1. **アーキテクチャ**: Clean Architectureに従っているか
2. **テスト**: 適切なテストがあるか
3. **型安全性**: 型ヒントが正しいか
4. **ドキュメント**: コメントやdocstringが適切か
5. **パフォーマンス**: 最適化の余地はないか

#### レビューコメント例
```markdown
# 良いフィードバック
✅ 型ヒントの追加をお願いします：
\`\`\`python
# 修正案
def process(data: Dict[str, Any]) -> ProcessResult:
    ...
\`\`\`

# 悪いフィードバック
❌ 型が足りない
```

## 参考資料

### 内部ドキュメント
- [DEVELOPMENT_GUIDE.md](../../docs/DEVELOPMENT_GUIDE.md): 開発ガイド
- [CONTRIBUTING.md](../../CONTRIBUTING.md): コントリビューションガイド

### 外部リソース
- [Pre-commit Documentation](https://pre-commit.com/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Pyright Documentation](https://microsoft.github.io/pyright/)
