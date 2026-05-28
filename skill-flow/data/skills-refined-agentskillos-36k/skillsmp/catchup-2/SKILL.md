---
name: catchup
description: Use when user requests learning review or knowledge consolidation. Triggers: (1) "daily review" or "daily" keywords, (2) "weekly review" or "weekly" keywords, (3) "understanding test" or "test" keywords, (4) "current location" or "where" keywords, (5) end-of-session retrospectives.
---

# Catchup - 学習支援

## 実行方法

各モードの操作はsubagentを起動して実行すること。
コード調査が必要な場合はGemini MCPに委託する。

## モード

### Daily
~/dev/logs/claude-catchup/dev/YYYY-MM-DD.yaml を読み込み:
- 今日触ったサービス/モジュール
- 獲得した知識（LANGUAGE/DOMAIN/ARCHITECTURE）
- 曖昧な領域（危険度1-3）
- 明日読むべきコード（3-5件）
- 理解チェック（3問）

### Weekly
直近7日分のYAMLから:
- よく触ったモジュール TOP5
- 理解不足領域 TOP3
- 今週の成長ポイント
- 来週のキャッチアップ計画

### Test
直近の編集コードから5問のクイズ:
- Q1〜Q5（コード/ドメインに紐づく）
- 模範回答
- 読み直すべきファイル（3件）

### Where
現在ファイルの位置づけ:
- ファイルの役割
- 主な呼び出し元（3件）
- 関連モジュール
- 次に読むべきファイル（3件）

## 共通出力フォーマット

すべてのモードで含める:
- Task Meaning: 変更がシステムで持つ意味
- Assumption Check: 前提概念（3-5個）
- Completion Criteria: 完了条件
- Self-Check Questions: 確認質問（1-3問）
