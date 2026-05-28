---
name: daily-morning
description: デイリーノート朝用アシスタント（作成）
allowed-tools: Bash(cd *), Bash(date *), Bash(TZ=*), Bash(uv *), Bash(find *), Write, Read, Glob, LS
disable-model-invocation: true
---

# デイリーノート朝用アシスタント（作成）

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

1. 引数から対象日付を決定、または今日の日付を使用
2. Google Calendarのイベントを取得しMTG・イベントセクションに追加
3. 最新のデイリーノートから前日のtodoを取得
4. 対象日付のデイリーノートファイルを作成

詳細な手順は instructions.md を参照。テンプレートは template.md を参照。
