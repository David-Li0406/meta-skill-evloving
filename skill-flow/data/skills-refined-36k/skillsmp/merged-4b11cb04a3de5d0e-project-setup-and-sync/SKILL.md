---
name: project-setup-and-sync
description: Use this skill for initializing and synchronizing project documentation, ensuring consistency and organization across project files.
---

# プロジェクト初期化とドキュメント同期

## トリガー条件

以下のいずれかの場合に使用:
- プロジェクトルートにCLAUDE.mdが存在しない
- .claude/ディレクトリが存在しない
- PJ CLAUDE.mdの更新を依頼された場合
- ドキュメント構造の整理を依頼された場合
- ユーザーがプロジェクト初期化を要求した

## 実行手順

### 1. 現状把握

```bash
# PJ CLAUDE.mdの確認
cat CLAUDE.md 2>/dev/null || echo "CLAUDE.md not found"
wc -l CLAUDE.md 2>/dev/null

# ドキュメント構造の確認
ls -la .claude/ 2>/dev/null
ls -la docs/ 2>/dev/null

# user-level設定の確認
cat ~/.claude/CLAUDE.md
ls ~/.claude/context/
```

### 2. テンプレートの確認とCLAUDE.mdの作成

テンプレートが存在する場合、PJルートに以下の内容でCLAUDE.mdを作成:

```markdown
# <プロジェクト名>

## 変数
MEMORY_DIR=.local/
BASE_BRANCH=develop

## 品質チェック
```bash
npm run lint      # または適切なコマンド
npm run format
npm run typecheck
npm test
```

## 特記事項
- [PJ固有のルール]
```

### 3. 差分分析

以下を確認:

| 項目 | 確認内容 |
|------|---------|
| CLAUDE.md行数 | 60行以下か |
| 変数定義 | MEMORY_DIR, BASE_BRANCH があるか |
| 品質チェック | lint/format/typecheck/test コマンドがあるか |
| @参照 | 詳細をcontext/に委譲しているか |
| 分離原則 | 人間向け/エージェント向けが分離されているか |

### 4. 更新提案の作成

```markdown
## 更新提案

### CLAUDE.md
**現状:** XX行
**提案:** 以下に簡素化

```markdown
# <PJ名>

## 変数
MEMORY_DIR=.local/
BASE_BRANCH=develop

## 品質チェック
```bash
npm run lint
npm run format
npm run typecheck
npm test
```

## 特記事項
- [PJ固有ルール]
```

### 5. gitignore設定

`.local/`がgitに追跡されないよう設定:

```bash
# global gitignoreに.local/があるか確認
if git config --global core.excludesfile &>/dev/null; then
  GLOBAL_GITIGNORE=$(git config --global core.excludesfile)
  if grep -q "^\.local/$" "$GLOBAL_GITIGNORE" 2>/dev/null; then
    echo "global gitignoreで.local/は除外済み"
  else
    # gitリポジトリ内かどうか確認
    if git rev-parse --git-dir &>/dev/null; then
      # gitリポジトリ内の場合、.git/info/excludeに追加
      echo ".local/" >> "$(git rev-parse --git-dir)/info/exclude"
      echo ".git/info/excludeに.local/を追加"
    else
      # gitリポジトリ外（複数リポジトリの親ディレクトリ等）の場合はスキップ
      echo "gitリポジトリ外のため、gitignore設定をスキップ"
    fi
  fi
fi
```

### 6. ユーザー確認

AskUserQuestionで以下を確認:
1. 更新提案の承認
2. 削除対象の確認（誤削除防止）
3. メモリディレクトリの場所（モノレポの場合は調整が必要）
4. 品質チェックコマンド
5. ベースブランチ
6. PJ固有のルール

### 7. 設定の調整

ユーザーの回答に基づいてCLAUDE.mdを調整。

## モノレポの場合

モノレポでは、メモリディレクトリの場所を明確に指定:

```markdown
## 変数
MEMORY_DIR=<monorepo-root>/.local/
```

## 不要ファイルの判断基準

| 判断 | 条件 |
|------|------|
| **削除** | 古いagent定義、重複ドキュメント、空ファイル |
| **移動** | エージェント向け内容がdocs/にある場合 → .claude/context/ |
| **統合** | 類似内容の複数ファイル → 1ファイルに |
| **保持** | 人間向けドキュメント（README, docs/）、PJ固有設定 |

## チェックリスト

- [ ] CLAUDE.mdが60行以下
- [ ] 変数（MEMORY_DIR, BASE_BRANCH）が定義済み
- [ ] 品質チェックコマンドが記載済み
- [ ] ドキュメント分離原則に従っている
- [ ] 不要ファイルが削除済み
- [ ] @参照が正しく設定済み

### 8. 検証

```bash
# 行数確認
wc -l CLAUDE.md

# 構造確認
ls -la .claude/

# @参照の動作確認（手動）
```