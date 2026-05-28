---
name: cga-skills-update
description: git diff ..main と会話コンテキストから、Claude Code 拡張機能（Skills/CLAUDE.md/Hooks/Subagents）の更新を提案する。
allowed-tools: Bash Read Glob Grep Write Edit AskUserQuestion
---

## いつ使うか

- 新しい実装パターンを発見し、次回以降も使えそうなとき
- 既存スキルが実態と乖離していることに気づいたとき
- CLAUDE.md が肥大化している、または不足しているとき
- PR作成前のスキル整合性チェック

## いつ使わないか

- ドメイン知識・意思決定の記録 → `/cga-docs-update`
- コードの実装そのもの → `/cga-programming`

## 何をするか

1. `git diff main..HEAD` でコード変更を分析
2. 会話コンテキストから非自明な知見を抽出
3. 適切な拡張方法を判断（Skills / CLAUDE.md / Hooks / Subagents）
4. 品質テスト適用:「削除したら Claude が間違えるか？」
5. 更新提案をテーブル形式で提示
6. ユーザー確認後、更新を実行

## 基本ルール

- 自明なこと（コードを読めば分かること）はスキル化しない
- SKILL.md は 80行以内に保つ
- 提案前に既存スキルとの重複・矛盾を確認する

## 使用例

```text
/cga-skills-update
```

## 詳細

[guide.md](guide.md) を参照
