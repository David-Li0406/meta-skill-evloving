---
name: pull-request-workflow
description: Use this skill when you need to create a pull request (PR) following a structured workflow, ensuring all necessary checks and documentation are completed.
---

# Pull Request Workflow

## 目的
- main直pushを避け、PR作成までを確実に行う

## 手順

1. **ブランチ戦略の確認**  
   `README.md`を読み込んで、プロジェクトのブランチ戦略を理解します。  
   ```bash
   Read README.md
   git branch -a
   ```

2. **既存PRの未マージ有無を確認する**  
   既存のPRが未マージでないか確認します。

3. **mainを最新化する**  
   ```bash
   git pull origin main
   ```

4. **作業ブランチを作成する**  
   ```bash
   git checkout -b <feature-branch>
   ```

5. **変更を小さくコミットする**  
   変更を小さく分けてコミットします。  
   ```bash
   git add .
   git commit -m "Your commit message"
   ```

6. **テストとLintの実行**  
   プロジェクト固有のテストとLintを実行し、結果を記録します。  
   ```bash
   # 例: Node.jsプロジェクトの場合
   npm test
   npm run lint
   ```

7. **PR情報の準備**  
   PRタイトルと本文を以下のテンプレートに従って作成します。  
   ```markdown
   ## 概要
   [変更の目的と背景を記述]

   ## 変更点
   - [具体的な変更内容1]
   - [具体的な変更内容2]

   ## テスト計画
   - [x] [実施済みのテスト]
   - [ ] [実施予定のテスト]
   ```

8. **PRを作成する**  
   ユーザーの許可を得てからPRを作成します。  
   ```bash
   gh pr create --base <base-branch> --title "<PRタイトル>" --body "$(cat <<'EOF'
   ## 概要
   ...

   ## 変更点
   ...

   ## テスト計画
   ...
   EOF
   )"
   ```

9. **PR URLの確認**  
   PR作成後、URLをユーザーに提示します。

## PR本文の必須項目
- 変更点要約
- 動作確認手順
- 実行コマンド結果
- 影響範囲とロールバック観点
- 注意点（環境変数/モック）

## チェックリスト
PR作成前の確認事項:
- [ ] コードレビューの準備完了
- [ ] テスト正常実行
- [ ] 適切なコミットメッセージ
- [ ] IssueがPRにLinked
- [ ] セルフレビュー実施

## よくある間違い
- **間違い**: testが失敗しているのにPRを作成  
  **正解**: test・linterが全て成功してからPR作成

- **間違い**: ユーザーの許可なしにPRを作成  
  **正解**: 必ずPR情報を提示してユーザーの許可を得る

## 使用例
### 例: 新機能追加の場合
1. ブランチ確認
   ```bash
   git branch -a
   ```

2. Test・Linter実行
   ```bash
   npm test
   npm run lint
   ```

3. PR情報をユーザーに提示し、許可を得る。

4. 許可後にPR作成
   ```bash
   gh pr create --base staging --title "新機能追加" --body "$(cat <<'EOF'
   ## 概要
   ...

   ## 変更点
   ...

   ## テスト計画
   ...
   EOF
   )"
   ```

## PRのマージ（ユーザーから指示があった場合）
```bash
gh pr merge <PR番号> --merge --delete-branch
```

**注意**: プロジェクトでは**Merge commit**を使用します（Squash mergeは使用しない）。