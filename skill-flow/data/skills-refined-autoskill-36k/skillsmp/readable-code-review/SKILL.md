---
name: readable-code-review
description: ユーザーがコードレビューを依頼したとき、またはコードの可読性・保守性・命名規則・コメントの改善提案を求めたときに使用します。指定されたファイルに対してテンプレートに基づく一貫したコードレビューを自動生成します。初期スクリーニングや複数ファイルの迅速な品質確認に最適です。
---

# リーダブルコードレビュー

## 概要

コードの可読性、保守性、理解しやすさに焦点を当てたコードレビューを実施します。変数名、関数名、コード構造、コメント、複雑度などを評価し、改善提案を行います。テンプレートベースの標準化されたレビュー形式で結果を作成します。

## パラメータ

| パラメータ | 型     | 必須 | 説明                                                               |
| ---------- | ------ | ---- | ------------------------------------------------------------------ |
| filepath   | string | はい | レビュー対象のファイルパス（複数ファイルやディレクトリも指定可能） |

## 手順

1. **レビュータスクの作成**
   - 事前クリーンアップ：過去に生成済みのタスクファイルを削除（存在する場合）
     - `rm -f .claude/skills/readable-code-review/tmp/readable-review-*.md`
   - 連番を決定：`.claude/skills/readable-code-review/tmp/` 内の既存の `readable-review-{数字}.md` ファイルの最大数字 + 1（存在しない場合は1）
   - `python3 .claude/skills/readable-code-review/scripts/generate_review.py {filepath} .claude/skills/readable-code-review/tmp/readable-review-{連番}.md`でレビュータスクを作成

2. **レビューの実施**
   - 生成されたレビュータスクファイルを開き、チェックリストに従ってレビューを実施
   - 各レビュー項目について `<reviewed>false</reviewed>` を `<reviewed>true</reviewed>` に変更
   - レビュー結果を `.claude/skills/readable-code-review/assets/result.md` のテンプレートに基づいて生成

## 使用例

### 基本的な使用例（ファイルを指定してレビュー）

```bash
rm -f .claude/skills/readable-code-review/tmp/readable-review-*.md
python3 .claude/skills/readable-code-review/scripts/generate_review.py src/main.py .claude/skills/readable-code-review/tmp/readable-review-1.md
```

### 複数ファイルの一括レビュー

```bash
#!/bin/bash
mkdir -p .claude/skills/readable-code-review/tmp
rm -f .claude/skills/readable-code-review/tmp/readable-review-*.md

counter=1
while IFS= read -r -d '' file; do
    echo "Processing: $file"
    if python3 .claude/skills/readable-code-review/scripts/generate_review.py "$file" ".claude/skills/readable-code-review/tmp/readable-review-${counter}.md"; then
        ((counter++))
    else
        echo "Error: Failed to process $file" >&2
    fi
done < <(find src -name "*.py" -type f -print0)

echo "Completed: Generated ${((counter-1))} review files"
```
