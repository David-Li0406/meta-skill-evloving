---
name: daily-report
description: 作業記録を自動化し、問題解決パターンを蓄積。/quit時に自動生成。
---

# Daily Report Skill

## 目的

作業記録を自動化し、メモリ機能を補完する。問題解決パターンを蓄積し、ナレッジベースを構築する。

## 使用タイミング

- `/quit` 実行時に自動生成
- セッション中の情報を集約
- 次回セッション開始時に前回の日報を参照

## 日報フォーマット

### 基本構造

```markdown
# 日報: YYYY-MM-DD

生成時刻: HH:MM:SS
セッション時間: [推定]

---

## 📋 実施タスク

### タスク1: [タスク名]

**ブランチ**: `feature/xxx` または `main` (記録)
**使用スキル**: 
- skill-name-1
- skill-name-2

**成果物**:
- `path/to/file1.py` (作成)
- `path/to/file2.ts` (修正)
- `tests/test_xxx.py` (テスト追加)

**変更サマリ**:
[1-2文で何をしたか]

**所要時間**: [推定]

---

### タスク2: [タスク名]

[同様の形式]

---

## 🐛 遭遇した問題

### 問題1: [問題名]

**現象**:
[何が起きたか]

**原因**:
[分析結果]

**解決策**:
[採用した方法]

**参照スキル**: 
- systematic-debugging
- [該当スキル]

**所要時間**: [推定]

**関連ファイル**:
- `claude_tmp/failure_log/YYYYMMDD_HHMMSS.md`

---

### 問題2: [問題名]

[同様の形式]

---

## 💡 学んだこと

### 技術的な学び

- [学び1]: [詳細]
- [学び2]: [詳細]

### プロセス改善

- [改善点1]: [詳細]
- [改善点2]: [詳細]

### スキル活用

- [有効だったスキル]: [どう役立ったか]
- [不足していたスキル]: [あれば良かったもの]

---

## 📝 明日以降のTODO

### 優先度: 高

- [ ] [タスク1]
- [ ] [タスク2]

### 優先度: 中

- [ ] [タスク3]
- [ ] [タスク4]

### 優先度: 低

- [ ] [タスク5]

---

## 🔗 関連ファイル

### ブレインストーミング
- `claude_tmp/brainstorming/xxx.md`

### 失敗ログ
- `claude_tmp/failure_log/yyy.md`

### レビューレポート
- `claude_tmp/review_reports/zzz.md`

---

## 📊 統計情報

- 実施タスク数: X件
- 遭遇した問題: Y件
- 使用スキル: [top 5]
- 変更ファイル数: Z件

---

## 🎯 次回セッションへの引き継ぎ

### 継続中のタスク

[進行中のタスクの状態]

### 懸念事項

[気になっていること、確認が必要なこと]

### 提案

[次回試したいこと、改善案]
```

## 自動生成の仕組み

### /quit 実行時の処理フロー

```text
1. セッション中の情報を収集
   - 実行したコマンド
   - 変更したファイル
   - 参照したスキル
   - 発生したエラー
   - ユーザーとの対話内容

2. 情報を分類
   - タスク: 実装・修正・調査
   - 問題: バグ・エラー・行き詰まり
   - 学び: 新しい知見・改善点

3. フォーマットに整形
   - 上記のテンプレートに当てはめる
   - 時系列順に整理
   - 関連ファイルをリンク

4. ファイルに保存
   - パス: claude_tmp/daily_reports/YYYY-MM-DD.md
   - 同日に複数セッションがある場合は追記

5. 確認メッセージ
   - "日報を生成しました: claude_tmp/daily_reports/YYYY-MM-DD.md"
```

### 情報収集の対象

```text
✅ 収集するもの:
- Git操作 (branch, status, diff)
- ファイル操作 (create, edit, delete)
- スキル参照 (view コマンド)
- エラー発生 (実行失敗、バグ検出)
- ユーザーの質問と回答
- ブレインストーミング内容
- レビュー結果

❌ 収集しないもの:
- 機密情報 (パスワード、APIキー)
- 個人情報
- センシティブなデータ
```

## 日報の活用方法

### 次回セッション開始時

```bash
# 前回の日報を確認
view claude_tmp/daily_reports/$(date -d yesterday +%Y-%m-%d).md

# または最新の日報
view claude_tmp/daily_reports/$(ls -t claude_tmp/daily_reports/ | head -1)
```

### 問題解決パターンの検索

```bash
# 特定の問題を検索
grep -r "問題:" claude_tmp/daily_reports/

# 特定のスキルの使用例を検索
grep -r "systematic-debugging" claude_tmp/daily_reports/
```

### 進捗レポートの生成

```bash
# 週次レポート
cat claude_tmp/daily_reports/2025-01-{13..17}.md > weekly_report.md

# 月次レポート
cat claude_tmp/daily_reports/2025-01-*.md > monthly_report.md
```

## 日報の品質向上

### 良い日報の特徴

```text
✅ 具体的:
"バグを修正した" ではなく
"ログイン時のセッションID未初期化バグを修正"

✅ 定量的:
"速くした" ではなく
"応答時間を2秒から0.5秒に改善 (75%削減)"

✅ 再現可能:
"○○した" だけでなく
"○○スキルを参照し、△△の手順で実施"

✅ 学びを記録:
"できた" だけでなく
"□□の理由で××が有効だった"
```

### 避けるべき記述

```text
❌ 曖昧:
"いくつかのバグを修正した"

❌ 主観的:
"良い感じにできた"

❌ 結果のみ:
"実装した" (どう実装したかが不明)

❌ 学びなし:
タスク列挙のみで学びの記録がない
```

## 日報とメモリの関係

### 日報の役割

```text
メモリ (userMemories):
- 長期的な個人情報
- プロジェクト概要
- よく使うツール
- 好み・スタイル

日報 (daily_reports):
- 短期的な作業記録
- 具体的なタスク内容
- 遭遇した問題と解決策
- 学びと改善点
```

### 連携の仕組み

```text
セッション中:
1. メモリから長期情報を参照
2. 作業内容を記録
3. /quit 時に日報生成

次回セッション:
1. メモリから長期情報を参照
2. 前回の日報から作業継続
3. 新しい作業を記録
```

## 実装例

### hooks/on_quit.sh の実装 (参考)

```bash
#!/bin/bash

REPORT_DIR="claude_tmp/daily_reports"
REPORT_FILE="$REPORT_DIR/$(date +%Y-%m-%d).md"

mkdir -p "$REPORT_DIR"

# セッション情報を収集
SESSION_START=$(cat claude_tmp/.session_start 2>/dev/null || echo "不明")
SESSION_END=$(date +%H:%M:%S)

# Git情報
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "N/A")
CHANGED_FILES=$(git diff --name-only 2>/dev/null | wc -l)

# 日報生成
cat > "$REPORT_FILE" << EOF
# 日報: $(date +%Y-%m-%d)

生成時刻: $SESSION_END
セッション開始: $SESSION_START

---

## 📋 実施タスク

[自動収集された情報]

---

## 📊 統計情報

- 変更ファイル数: $CHANGED_FILES件
- 現在のブランチ: $CURRENT_BRANCH

EOF

echo "✅ 日報を生成しました: $REPORT_FILE"
```

## チェックリスト

### 日報生成時の確認

```text
□ 実施タスクが明確か?
□ 問題と解決策が記録されているか?
□ 学びが言語化されているか?
□ 次回TODOが明確か?
□ 関連ファイルがリンクされているか?
□ 統計情報が正確か?
```

### 日報活用時の確認

```text
□ 前回の日報を確認したか?
□ 継続タスクがあるか?
□ 前回の学びを活かせるか?
□ 似た問題が過去になかったか?
```

## よくある質問

### Q: 日報が長すぎる

```text
A: 重要な情報のみを記録する設定に変更可能
   - タスクサマリのみ
   - 問題のみ
   - 学びのみ
```

### Q: 日報を自動送信したい

```text
A: hooks でメール送信やSlack通知を追加可能
   on_quit.sh の最後に:
   - mail コマンド
   - Slack Webhook
   - GitHub Issues
```

### Q: 複数プロジェクトで日報を分けたい

```text
A: プロジェクトごとのディレクトリ構造
   claude_tmp/daily_reports/
   ├── project_a/
   │   └── YYYY-MM-DD.md
   └── project_b/
       └── YYYY-MM-DD.md
```

## 関連スキル

- `failure-logging` - 失敗記録の詳細
- `quality-automation` - 自動レビュー
- `consultation` - 相談記録

## まとめ

**日報は記憶の外部化**

1. セッション中の情報を自動収集
2. /quit 時に構造化して保存
3. 次回セッションで参照
4. 問題解決パターンを蓄積

**継続的な改善が可能になる**
