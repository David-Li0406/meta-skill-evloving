---
name: reviewing-security
description: Use this skill when you need to conduct a security review based on the OWASP API Security Top 10 (2023) and relevant security best practices for a specific programming language.
---

# セキュリティレビュー

OWASP API Security Top 10 (2023) と {開発言語をここに書く} セキュリティベストプラクティスに基づくレビュースキル。

## OWASP チェック項目

| ID   | リスク      | チェック内容                               |
| ---- | ----------- | ------------------------------------------ |
| API1 | BOLA        | tenant_id 検証、file_id との組み合わせ検証 |
| API2 | Broken Auth | gRPC メタデータ認証                        |
| API3 | Property    | レスポンスの不要情報                       |
| API4 | Resource    | ファイルサイズ制限、ページネーション       |

## {開発言語をここに書く} セキュリティ

| 項目                 | 検索パターン |
| -------------------- | ------------ |
| 依存関係脆弱性       | `N/A`        |
| unsafe コード        | `N/A`        |
| ハードコード認証情報 | `N/A`        |

## バージョン管理チェック

dependabotやrenovateで自動検証できないバージョン指定をチェックします。Dockerfile内の直接指定、GitHub Actionsのバージョン、設定ファイルで指定されたツールバージョンなどが対象です。古いバージョンの使用はセキュリティリスクやパフォーマンス問題につながる可能性があります。

### チェック対象ファイルとパターン

| ファイルタイプ       | ファイル名/パターン                                          | チェック内容                                                                         |
| -------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| Dockerfile           | `Dockerfile`, `*.dockerfile`, `Dockerfile.*`                 | `FROM` イメージとタグ、`RUN apt-get install`、`RUN apk add` でのパッケージバージョン |
| GitHub Actions       | `.github/workflows/*.yml`, `.github/workflows/*.yaml`        | `uses:` でのアクションバージョン、`setup-*` アクションの `*-version` 指定            |
| ツールバージョン設定 | `.nvmrc`, `.python-version`, `.go-version`, `.tool-versions` | 開発環境のツールバージョン指定                                                       |
| その他の設定         | `Makefile`, `runtime.txt`                                    | ビルドスクリプトや実行環境のバージョン指定                                           |

### チェック手順

1. **ファイルの検出**

   - 上記パターンに該当するファイルを検索
   - 各ファイルからバージョン指定を抽出

2. **バージョン情報の取得**

   - 現在指定されているバージョンを特定
   - 可能な場合、最新の安定版を確認（Web検索やAPIを使用）
   - EOL（サポート終了）情報を確認

3. **更新可否の判定**

   - メジャーバージョン更新: 破壊的変更の可能性あり、更新を推奨
   - EOL: 早急な更新が必要
   - 既知のセキュリティ脆弱性: 即座の対応が必要
   - **注意**: マイナーバージョンやパッチバージョン程度の差では指摘しません

4. **優先度の設定**
   - 🔴 高: EOLバージョン、既知のセキュリティ脆弱性
   - 🟡 中: メジャーバージョン以上の差がある

### 出力フォーマット

```markdown
## バージョン管理ツールの更新可否

|