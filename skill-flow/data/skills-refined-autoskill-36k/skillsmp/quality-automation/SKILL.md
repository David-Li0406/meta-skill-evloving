---
name: quality-automation
description: タスク完了時の自動レビューを実装。手動チェックを削減し、一貫性のある品質を維持。
---

# Quality Automation Skill

## 目的

タスク完了時の自動レビューを実装し、品質を担保する。手動チェックを削減し、一貫性のある品質を維持する。

## 使用タイミング

- タスク完了時 (自動実行)
- ファイル保存時 (オプション)
- 手動レビュー要求時 (`self-review` コマンド)

## 自動レビューの仕組み

### トリガー

```text
1. タスク完了の検知
   - 実装が終わった
   - テストが通った
   - ユーザーが確認を求めた

2. hooks による起動
   - hooks/post_task.sh
   - 自動で実行される
```

### 実行フロー

```text
1. 変更ファイルを分析
   ↓
2. 該当スキルを自動判定
   ↓
3. 各スキルでレビュー実行
   ↓
4. 結果を集約
   ↓
5. レポート生成・保存
   ↓
6. ユーザーに通知
```

## レビュー項目

### 基本レビュー (全タスク共通)

```text
code-review:
  - コード品質
  - 可読性
  - 保守性
  - DRY原則
  - SOLID原則

security-checklist:
  - セキュリティ基本チェック
  - OWASP Top 10
  - 入力検証
  - 認証・認可
```

### ファイル種別による追加レビュー

```text
Python (.py):
  - test-driven-development (テストの存在)
  - code-generation (命名規則)
  - hallucination-prevention (事実確認)

TypeScript (.ts, .tsx):
  - typescript-strict (型チェック)
  - ui-ux-design (UI関連)
  - websocket-realtime (WebSocket使用時)

API実装 (api, endpoint, route含むファイル):
  - api-design (RESTful原則)
  - error-handling (エラー処理)
  - input-validation (入力検証)

DB変更 (migration, schema含むファイル):
  - database-design (正規化、インデックス)
  - migration-upgrade (マイグレーション)

認証関連 (auth, login, session含むファイル):
  - authentication-authorization (認証・認可)
  - security-review (セキュリティ詳細)

Docker (Dockerfile, docker-compose.yml):
  - docker (ベストプラクティス)
  - security-checklist (コンテナセキュリティ)

CI/CD (.github/workflows, .gitlab-ci.yml):
  - ci-cd (パイプライン設計)
  - dependency-management (依存関係)

テスト (test_, *_test.*):
  - test-driven-development (テストの品質)
  - code-review (テストの網羅性)
```

## レビューレポートのフォーマット

### 基本構造

```markdown
# 品質レビューレポート

生成日時: YYYY-MM-DD HH:MM:SS
対象ブランチ: feature/xxx
変更ファイル数: X件

---

## 📊 総合評価

- ✅ 合格: Y件
- ⚠️  警告: Z件
- ❌ 要修正: W件

---

## 📋 レビュー詳細

### ファイル: path/to/file1.py

**適用スキル**: code-review, test-driven-development

#### ✅ 合格項目

- コード品質: 良好
- 命名規則: 適切
- テストカバレッジ: 85%

#### ⚠️ 警告項目

- 関数の複雑度: `function_name` が若干高い (CC: 8)
  推奨: リファクタリングを検討

#### ❌ 要修正項目

- テストの不足: エッジケースのテストがない
  修正方法: test_edge_cases() を追加

---

### ファイル: path/to/file2.ts

[同様の形式]

---

## 🎯 改善提案

### 優先度: 高

1. [file1.py] テストの追加
   - 理由: エッジケースが未カバー
   - 参照スキル: test-driven-development

### 優先度: 中

2. [file1.py] 関数のリファクタリング
   - 理由: 複雑度が高い
   - 参照スキル: refactoring

### 優先度: 低

3. [file2.ts] 型注釈の追加
   - 理由: 一部でany型を使用
   - 参照スキル: typescript-strict

---

## 📚 参照したスキル

- code-review: 全ファイル
- test-driven-development: file1.py
- typescript-strict: file2.ts
- security-checklist: 全ファイル

---

## ✅ 次のアクション

1. 要修正項目の対応 (❌)
2. 警告項目の確認 (⚠️)
3. 改善提案の検討
```

## hooks 実装

### hooks/post_task.sh (参考)

```bash
#!/bin/bash

# 変更ファイルを取得
CHANGED_FILES=$(git diff --name-only HEAD)

if [ -z "$CHANGED_FILES" ]; then
    echo "変更ファイルなし。レビューをスキップします。"
    exit 0
fi

# レポートディレクトリ
REPORT_DIR="claude_tmp/review_reports"
mkdir -p "$REPORT_DIR"

REPORT_FILE="$REPORT_DIR/$(date +%Y%m%d_%H%M%S).md"

echo "🔍 品質レビューを開始します..."
echo "対象ファイル数: $(echo "$CHANGED_FILES" | wc -l)"

# レポートヘッダー
cat > "$REPORT_FILE" << EOF
# 品質レビューレポート

生成日時: $(date +"%Y-%m-%d %H:%M:%S")
対象ブランチ: $(git branch --show-current)
変更ファイル数: $(echo "$CHANGED_FILES" | wc -l)件

---

## 📊 総合評価

EOF

# ファイルごとにレビュー
PASS_COUNT=0
WARN_COUNT=0
FAIL_COUNT=0

for file in $CHANGED_FILES; do
    echo "レビュー中: $file"
    
    # ファイル種別を判定
    case "$file" in
        *.py)
            SKILLS="code-review test-driven-development"
            ;;
        *.ts|*.tsx)
            SKILLS="code-review typescript-strict"
            ;;
        *migration*|*schema*)
            SKILLS="database-design migration-upgrade"
            ;;
        *auth*|*login*|*session*)
            SKILLS="authentication-authorization security-review"
            ;;
        Dockerfile|docker-compose.yml)
            SKILLS="docker security-checklist"
            ;;
        *)
            SKILLS="code-review"
            ;;
    esac
    
    # スキルを参照してレビュー実行
    # (実際のレビューロジックはここに実装)
    
    # 仮の判定 (実装時は実際のチェックに置き換え)
    RESULT="PASS"  # or "WARN" or "FAIL"
    
    case "$RESULT" in
        PASS) PASS_COUNT=$((PASS_COUNT + 1)) ;;
        WARN) WARN_COUNT=$((WARN_COUNT + 1)) ;;
        FAIL) FAIL_COUNT=$((FAIL_COUNT + 1)) ;;
    esac
done

# 総合評価を書き込み
cat >> "$REPORT_FILE" << EOF
- ✅ 合格: ${PASS_COUNT}件
- ⚠️  警告: ${WARN_COUNT}件
- ❌ 要修正: ${FAIL_COUNT}件

---

## 📋 レビュー詳細

[詳細は省略 - 実装時に追加]

EOF

echo "✅ レビュー完了: $REPORT_FILE"

# 要修正があれば警告
if [ $FAIL_COUNT -gt 0 ]; then
    echo "⚠️  要修正項目があります。レポートを確認してください。"
fi
```

## 自動判定のロジック

### ファイルパターンマッチング

```python
# 参考実装 (Python)

import re
from pathlib import Path

def determine_skills(filepath: str) -> list[str]:
    """ファイルパスから適用すべきスキルを判定"""
    
    skills = ["code-review"]  # 基本は常に適用
    
    # 拡張子ベース
    ext = Path(filepath).suffix
    if ext == ".py":
        skills.extend(["test-driven-development", "hallucination-prevention"])
    elif ext in [".ts", ".tsx"]:
        skills.extend(["typescript-strict"])
    
    # ファイル名パターンベース
    name = Path(filepath).name.lower()
    
    if "test" in name:
        skills.append("test-driven-development")
    
    if "migration" in name or "schema" in name:
        skills.extend(["database-design", "migration-upgrade"])
    
    if any(keyword in name for keyword in ["auth", "login", "session"]):
        skills.extend(["authentication-authorization", "security-review"])
    
    if "api" in name or "route" in name or "endpoint" in name:
        skills.extend(["api-design", "error-handling", "input-validation"])
    
    # ディレクトリベース
    parts = Path(filepath).parts
    if "tests" in parts or "test" in parts:
        skills.append("test-driven-development")
    
    if "api" in parts or "routes" in parts:
        skills.extend(["api-design"])
    
    # 重複を除去
    return list(set(skills))
```

### コンテンツベースの判定

```python
def determine_skills_from_content(content: str) -> list[str]:
    """ファイル内容から適用すべきスキルを判定"""
    
    skills = []
    
    # キーワード検索
    if re.search(r'(jwt|oauth|password|token)', content, re.I):
        skills.append("authentication-authorization")
    
    if re.search(r'(async|await|promise)', content, re.I):
        skills.append("concurrency-async")
    
    if re.search(r'(websocket|socket\.io)', content, re.I):
        skills.append("websocket-realtime")
    
    if re.search(r'(redis|cache|memcache)', content, re.I):
        skills.append("caching")
    
    if re.search(r'(CREATE TABLE|ALTER TABLE|migration)', content, re.I):
        skills.append("database-design")
    
    return skills
```

## 手動レビューコマンド

### self-review コマンド

```bash
#!/bin/bash
# commands/self-review

# 使用方法:
# claude-code self-review              # 全ファイル
# claude-code self-review file.py      # 特定ファイル
# claude-code self-review --skills test-driven-development  # 特定スキル

if [ $# -eq 0 ]; then
    # 全ファイル
    FILES=$(git diff --name-only HEAD)
else
    FILES="$@"
fi

echo "🔍 手動レビューを開始します..."

for file in $FILES; do
    echo "レビュー中: $file"
    
    # quality-automation スキルを参照
    # レビュー実行
    
    echo "✅ レビュー完了: $file"
done
```

## レビュー結果の活用

### レビューレポートの検索

```bash
# 最新のレポート
view claude_tmp/review_reports/$(ls -t claude_tmp/review_reports/ | head -1)

# 要修正項目の検索
grep -r "❌ 要修正" claude_tmp/review_reports/

# 特定スキルのレポート
grep -r "test-driven-development" claude_tmp/review_reports/
```

### レビュー結果の統計

```bash
# 合格率の計算
cat claude_tmp/review_reports/*.md | \
  grep -E "(✅ 合格|⚠️  警告|❌ 要修正)" | \
  awk '{sum[$2]+=$3} END {for (i in sum) print i, sum[i]}'
```

## チェックリスト

### 自動レビュー設定時

```text
□ hooks/post_task.sh が実行権限を持つか?
□ レポートディレクトリが存在するか?
□ 必要なスキルがすべて配置されているか?
□ ファイル判定ロジックが正しいか?
```

### レビュー実行時

```text
□ すべての変更ファイルがレビューされたか?
□ 要修正項目があるか?
□ 警告項目を確認したか?
□ 改善提案を検討したか?
```

## よくある質問

### Q: レビューが遅い

```text
A: 並列実行に変更可能
   - GNU parallel
   - xargs -P
   - 非同期処理
```

### Q: 誤検知が多い

```text
A: ルールをカスタマイズ
   - .reviewrc 設定ファイル
   - プロジェクト固有のルール
   - 除外リスト
```

### Q: レビューをスキップしたい

```text
A: 環境変数で制御
   SKIP_REVIEW=1 [command]
```

## 関連スキル

- `code-review` - 基本レビュー
- `security-checklist` - セキュリティ
- `test-driven-development` - テスト
- すべてのスキル - 各専門分野

## まとめ

**自動化で品質を担保**

1. タスク完了時に自動実行
2. ファイル種別に応じたレビュー
3. 結果をレポート化
4. 継続的な改善

**手動チェックの負担を削減し、一貫性のある品質を維持**
