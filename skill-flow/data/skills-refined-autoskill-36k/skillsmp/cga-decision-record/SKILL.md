---
name: cga-decision-record
description: 対話形式で意思決定記録（DR）を作成。チャットで話すだけでDRファイルが生成される。
allowed-tools: Read Write AskUserQuestion
---

## いつ使うか

- 技術選定や設計判断を記録したいとき（ADR）
- ドメインルールやビジネス判断を残したいとき（DDR）

## 何をするか

1. AskUserQuestion で基本情報を質問（種類、決定事項、選択肢、不可逆性）
2. 理由とトレードオフを深掘り
3. `doc/decisions/{種類}-{YYYYMMDDHH}-{slug}.md` として保存

## 使用例

```
/cga-decision-record
```

対話が始まり、質問に答えていくとDRファイルが生成される。

## 詳細

[guide.md](guide.md) を参照
