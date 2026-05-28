# 詳細手順

+すべてのコマンドはプロジェクトルート（obsidianディレクトリ）から実行すること。

## ステップ0: 対象日付の決定

```bash
TARGET_DATE="$1"
if [ -z "$TARGET_DATE" ]; then
  TARGET_DATE=$(TZ=Asia/Tokyo date +%Y-%m-%d)
fi
echo "Creating daily note for: $TARGET_DATE"
```

## ステップ1: カレンダーイベントの取得

```bash
cd .claude/skills/scripts/today_calendar && uv run today-calendar.py --date "$TARGET_DATE"
```

カレンダー出力を解析し、各イベントをMTG・イベントセクション用のチェックボックス形式に変換する。

## ステップ2: 前日のタスク取得

最新のデイリーノートファイルを取得するため、必ず以下のBashコマンドを使用すること。

```bash
find 01_Daily -name "*.md" -type f | sort -r | head -1
```

注意: Globツールではなく必ずfindコマンドを使用すること。findは`sort -r | head -1`で確実に最新の1件のみ返すため、結果のtruncateや解釈ミスを防げる。

取得したファイルをReadツールで読み込み、「明日やる」セクションの内容を抽出する。

- タスクステータス: [ ] 未着手, [/] 進行中, [R] レビュー中, [x] 完了, [-] 中止
- 抽出したタスクをユーザーに確認せずに直接使用

## ステップ3: デイリーノート作成

`01_Daily/YYYY/MM/[TARGET_DATE].md`を作成する。

テンプレートは template.md を参照。

すべてのステップを実行し、ただちにファイルを作成すること。
