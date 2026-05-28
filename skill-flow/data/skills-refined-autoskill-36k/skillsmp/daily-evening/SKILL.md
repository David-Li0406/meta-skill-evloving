---
name: daily-evening
description: デイリーノート夜用アシスタント（更新）
allowed-tools: Bash(cd *), Bash(date *), Bash(TZ=*), Bash(uv *), Bash(find *), Write, Read, Glob, Edit, LS
disable-model-invocation: true
---

# デイリーノート夜用アシスタント（更新）

## 日付の扱い

- date引数（$1）がYYYY-MM-DD形式で指定された場合、その日付を使用
- 引数が指定されない場合、今日の日付（JST）を使用

## 環境変数

```txt
PROJECT_A = "Aプロジェクト"
PROJECT_B = "Bプロジェクト"
PROJECT_C = "Cプロジェクト"
GOAL_1 = "技術力の向上"
GOAL_2 = "プロジェクト管理能力の強化"
GOAL_3 = "コミュニケーション能力の向上"
```

## タスク概要

0. まずinstructions.mdを読み込み、手順を正確に把握する（この手順をスキップしてはならない）
1. 引数から対象日付を決定、または今日の日付を使用
2. 対象日付のGoogle Calendarイベントを取得
3. 対象日付のデイリーノートを検索して読み込む
4. 成果と振り返りについて質問をユーザーに行う
5. 回答と自動生成された明日のタスクで既存のデイリーノートファイルを更新
