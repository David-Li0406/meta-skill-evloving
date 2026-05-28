---
name: file-refactor
description: ファイルやフォルダの名称変更・削除を行い、リポジトリ内の参照箇所を自動的に検索して更新するスキルです。ファイル/フォルダのリネームや削除を依頼された場合に使用してください。
---

# ファイル/フォルダリファクタリングスキル

このスキルは、ファイルやフォルダの名称変更や削除を安全に実行し、リポジトリ内のすべての参照箇所を検索して更新します。

## 利用可能なツール

このスキルでは以下のCopilotエージェントツールを使用します:

- **grep**: ファイル内容の検索（パターンマッチング）
- **glob**: ファイル名パターンの検索
- **edit**: ファイル内容の編集
- **bash**: Gitコマンド等の実行

**注**: これらはCopilotエージェント専用のツールで、標準コマンドラインツールとは構文が異なります。

## 使用すべきタイミング

以下の場合にこのスキルを使用してください:

- ファイルやフォルダの名称変更を依頼された場合
- ファイルやフォルダの削除を依頼された場合
- リファクタリング作業でパス構造を変更する場合

## 実行手順

### ファイル/フォルダの名称変更時

1. **変更前の準備**
   - 現在のファイル/フォルダパスを確認
   - 新しいパスを決定
   - `git status` でクリーンな状態を確認

2. **参照箇所の検索**
   
   以下のエージェントツールを使用してリポジトリ内の参照箇所を徹底的に検索します:
   
   ```
   # grepエージェントツールを使用してファイル内容を検索
   grep --pattern="旧ファイル名またはパス" --output_mode="content" -n
   ```
   
   **注**: これはCopilotエージェントの`grep`ツールの構文です。標準のコマンドラインgrepとは異なります。
   
   検索対象:
   - インポート文（TypeScript/JavaScript: `import`, `require`）
   - 相対パス参照（`./`, `../`）
   - ドキュメントのリンク（Markdown: `[text](path)`, `[text](./path)`）
   - 設定ファイルのパス（package.json, tsconfig.json, jest.config.jsなど）
   - HTML/JSXのパス参照（`src=`, `href=`）
   - コメント内のパス参照

3. **参照箇所の更新**
   
   検索で見つかったすべてのファイルで、以下を実行:
   - `edit` ツールを使用して旧パスを新パスに置換
   - 複数箇所ある場合は、各箇所ごとに個別に `edit` を呼び出す
   - 相対パスの場合は、ファイル位置に応じて正しい相対パスに調整

4. **名称変更の実行**
   
   ```bash
   git mv 旧パス 新パス
   ```

5. **検証**
   
   ```bash
   # 変更内容を確認
   git status
   git diff
   
   # ビルドとテストで検証
   npm run build
   npm test
   ```

### ファイル/フォルダの削除時

**重要**: 削除前に必ず参照箇所を検索し、すべての参照を処理してから削除を実行してください。

1. **削除前の必須検索**
   
   削除対象のファイル/フォルダ名またはパスで検索:
   
   ```
   # grepエージェントツールでファイル内容を検索
   grep --pattern="削除対象のファイル名またはパス" --output_mode="content" -n
   
   # globエージェントツールでファイル名パターンを検索（関連ファイルの確認）
   glob --pattern="**/削除対象のファイル名*"
   ```
   
   **注**: これらはCopilotエージェントのツール構文です。標準のコマンドラインツールとは異なります。

2. **参照箇所の処理**
   
   見つかった各参照箇所について:
   - **必要な参照**: 代替のファイル/実装に置き換え
   - **不要な参照**: 参照を削除
   - **インポート文**: 未使用インポートを削除
   - **ドキュメント**: リンクを削除または更新
   - **設定ファイル**: エントリを削除または更新

3. **削除の実行**
   
   すべての参照を処理した後:
   
   ```bash
   git rm -r 削除対象のパス
   ```

4. **検証**
   
   ```bash
   # 削除対象への参照が残っていないか再確認（grepエージェントツール）
   grep --pattern="削除したファイル名" --output_mode="content"
   # 結果が空であることを確認（-nフラグは不要、存在確認のみ）
   
   # ビルドとテストで検証
   npm run build
   npm test
   ```

## ベストプラクティス

### 検索パターンの工夫

- **ファイル名のみ**: ベースネームで検索（例: `MyComponent.tsx`）
- **パス付き**: ディレクトリ構造を含めて検索（例: `components/MyComponent`）
- **拡張子なし**: インポート時に拡張子を省略している場合に対応（例: `./MyComponent`）
- **エスケープ**: 特殊文字を含むパスは適切にエスケープ

### 段階的な実行

1. まず検索で影響範囲を完全に把握
2. 参照箇所をすべて更新
3. 最後に名称変更または削除を実行
4. 検証で問題がないことを確認

### エラー回避

- `git mv` を使用することで Git が履歴を追跡可能
- 一度に複数のファイルを変更する場合は、依存関係の順序に注意
- ビルドやテストが失敗した場合は、エラーメッセージから漏れた参照を特定

## 検索すべきファイルタイプ

以下のファイルタイプで参照を検索してください:

- **ソースコード**: `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.java`, `.go` など
- **設定ファイル**: `package.json`, `tsconfig.json`, `jest.config.js`, `webpack.config.js` など
- **ドキュメント**: `.md`, `.mdx`, `.txt`
- **スタイル**: `.css`, `.scss`, `.sass`
- **テンプレート**: `.html`, `.xml`, `.yaml`, `.yml`

## 注意事項

- **必ず削除前に検索**: 削除は取り消しが困難なため、参照検索は必須
- **バックアップの確認**: 重要なファイルの削除前は `git status` で確認
- **テストの実行**: 変更後は必ずビルドとテストを実行
- **段階的なコミット**: 大規模な変更は複数のコミットに分割することを検討

## 例

### ファイル名変更の例

```bash
# 1. 参照検索
grep --pattern="OldComponent" --output_mode="content" -n

# 2. 参照箇所を更新（各ファイルでeditツールを使用）
# import { OldComponent } from './OldComponent'
# ↓
# import { NewComponent } from './NewComponent'

# 3. ファイル名変更
git mv src/components/OldComponent.tsx src/components/NewComponent.tsx

# 4. 検証
npm run build && npm test
```

### ディレクトリ名変更の例

```bash
# 1. 参照検索
grep --pattern="old-directory" --output_mode="content" -n

# 2. 参照箇所を更新
# import something from '../old-directory/file'
# ↓
# import something from '../new-directory/file'

# 3. ディレクトリ名変更
git mv src/old-directory src/new-directory

# 4. 検証
npm run build && npm test
```

### ファイル削除の例

```bash
# 1. 削除前の必須検索
grep --pattern="deprecated-util" --output_mode="content" -n

# 2. 見つかった参照をすべて処理
# - import文を削除
# - 関数呼び出しを代替実装に置き換え
# - ドキュメントのリンクを削除

# 3. すべての参照を処理したことを確認
grep --pattern="deprecated-util" --output_mode="content"
# 結果が空であることを確認

# 4. ファイル削除
git rm src/utils/deprecated-util.ts

# 5. 検証
npm run build && npm test
```

## 参考資料

- **Gitファイル操作**: `git mv`, `git rm` (bashツールで実行)
- **Copilotエージェントツール**:
  - `grep` - ファイル内容検索
  - `glob` - ファイル名パターン検索
  - `edit` - ファイル編集
  - `bash` - コマンド実行
- [Copilotインストラクション](../../copilot-instructions.md)
