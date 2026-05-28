---
name: monthly-review
description: デイリーノートからKPT形式の月次振り返りを生成（引数なしで実行月、引数ありで指定月）
allowed-tools: Bash(cd *), Bash(date *), Bash(TZ=*), Bash(find *), Write, Read, Glob, LS
disable-model-invocation: true
---

# KPT形式の月次振り返り生成

## 日付の扱い

- 引数なし: 実行日の月のまとめ
- 引数1つ（YYYY-MM形式）: 指定月のまとめ

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

1. 対象期間の決定
2. デイリーノートの検索と読み込み
3. 情報の抽出と分析（KPT観点）
4. レビューファイルの作成

詳細な手順は instructions.md を参照。テンプレートは template.md を参照。
