---
name: ai-tools-sync
description: ai-tools同期 - リポジトリと~/.claude/間の設定ファイル同期。to-local/from-local/diffモード。
---

# ai-tools設定ファイル同期

## 使用タイミング

- ai-toolsリポジトリの変更を~/.claude/に反映したい時
- ローカル設定をリポジトリにコミットしたい時

## モード

### to-local (リポジトリ → ローカル)

ai-tools/claude-code/ → ~/.claude/ に反映

**同期対象**:
- CLAUDE.md
- commands/
- guidelines/
- skills/
- agents/
- scripts/
- statusline.js

### from-local (ローカル → リポジトリ)

~/.claude/ → ai-tools/claude-code/ に反映
既存の sync.sh を実行

### diff (差分確認)

両方向の差分を表示（変更なしで確認のみ）

## 実行手順

1. モード確認（to-local / from-local / diff）
2. 引数がない場合はユーザーに確認
3. 対象ファイルの差分を表示
4. ユーザー確認後に同期実行
5. 結果を報告

## 注意事項

- **to-local**: templates/内は環境変数置換が必要
- **from-local**: センシティブ情報は自動マスク（sync.sh機能）
- 実行前に必ず差分を確認
