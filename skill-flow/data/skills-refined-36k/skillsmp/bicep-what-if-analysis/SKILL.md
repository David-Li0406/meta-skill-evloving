---
name: bicep-what-if-analysis
description: azd up/provision や Bicep 変更の影響分析（what-if実行とノイズ除去）。「デプロイ前の差分確認」「破壊的変更の有無」「変更影響の確認」を求める場合に使用。
---

# Bicep What-If 分析

インフラ変更前の影響範囲確認とノイズフィルタリングを支援する。
任意の azd プロジェクトで使用可能。

## Tools

| Tool | Use For |
|------|---------|
| `microsoft_docs_search` | ノイズ判断が難しい場合のドキュメント検索 |
| `microsoft_docs_fetch` | 詳細なプロパティ仕様の取得 |

## クイックスタート

```bash
# フィルタ済みwhat-if分析（推奨）
# azdプロジェクトのルートディレクトリで実行
./.github/skills/bicep-what-if-analysis/scripts/whatif-analyze.sh

# 生出力が必要な場合
./.github/skills/bicep-what-if-analysis/scripts/whatif-analyze.sh --raw

# カスタムテンプレートとパラメータを指定
./.github/skills/bicep-what-if-analysis/scripts/whatif-analyze.sh \
  --template infra/custom.bicep \
  --parameters "vmSize=Standard_D2s_v3" \
  --parameters "nodeCount=3"

# 破壊的変更のみ抽出
./.github/skills/bicep-what-if-analysis/scripts/whatif-analyze.sh | jq '.changes[] | select(.changeType == "Delete")'
```

## 前提条件

- `azd env`が初期化済み（`AZURE_LOCATION`等が設定済み）
- Azure CLIでログイン済み
- azdプロジェクトのルートディレクトリで実行（`azure.yaml`が存在する場所）

## ノイズ判定基準

詳細は [references/noise.md](references/noise.md) を参照。

### 重要：「破壊的ではない」と「ノイズ」は異なる

| 分類 | 説明 | 例 |
|------|------|-----|
| **ノイズ** | 実際のリソースに影響しない変更。無視して良い | `provisioningState`, `etag`, `redundancyMode`（読み取り専用） |
| **破壊的ではない変更** | リソース再作成は不要だが、実際に適用される変更 | `tags`, `sku.tier`（明示的に設定可能なプロパティ） |
| **破壊的変更** | リソースの再作成が必要な変更 | `location`, `networkPlugin` |

**判断の誤りを避けるために:**

1. **読み取り専用プロパティのみがノイズ** - ドキュメントに「readOnly」「output only」「populated by the server」と記載されているもの
2. **ユーザーが設定可能なプロパティはノイズではない** - `tags`、SKU設定、構成オプションなど
3. **複数プロパティをまとめて評価しない** - 同一リソースでも各プロパティを個別に判断する

## 分析フロー

```
1. what-if実行
   ↓
2. 変更タイプで分類
   - NoChange / NoEffect / Ignore → 無視
   - Create / Delete / Modify → 詳細確認
   ↓
3. Modifyの詳細確認
   - ノイズリストに該当 → 無視
   - 破壊的変更リストに該当 → 要注意
   - それ以外 → 意図した変更か確認
```

## 変更タイプの意味

| タイプ | 説明 | 対応 |
|--------|------|------|
| **Create** | 新規作成 | 設定内容を確認 |
| **Delete** | 削除 | 意図した削除か確認 |
| **Modify** | 変更あり | 破壊的変更か確認 |
| **NoChange** | 変更なし | 無視 |
| **NoEffect** | 影響なし（読み取り専用等） | 無視 |
| **Ignore** | 評価対象外 | 通常は無視 |

## トラブルシューティング

### "AZURE_LOCATION is not set" エラー

```bash
# azd環境を初期化
azd env refresh
```

### what-ifが大量の変更を報告する

- APIバージョン更新後は多くの「変更」が報告されることがある
- `--raw`オプションで生出力を確認し、実際の差分を確認する

### 特定リソースの詳細を確認したい

```bash
# リソースIDでフィルタ（例：AKSクラスター）
./.github/skills/bicep-what-if-analysis/scripts/whatif-analyze.sh | \
  jq '.changes[] | select(.resourceId | contains("managedClusters"))'

# リソースタイプでフィルタ（例：ストレージアカウント）
./.github/skills/bicep-what-if-analysis/scripts/whatif-analyze.sh | \
  jq '.changes[] | select(.resourceType | contains("storageAccounts"))'
```

### カスタムパラメータを使用したい

```bash
# azure.yaml から自動検出せず、明示的にテンプレートとパラメータを指定
./.github/skills/bicep-what-if-analysis/scripts/whatif-analyze.sh \
  --template infra/main.bicep \
  --parameters "environment=dev" \
  --parameters "sku=Standard"
```

## Dependencies

- **az**: Azure CLI（`az deployment sub what-if` の実行に必要）
- **azd**: Azure Developer CLI（環境変数の取得に必要）
- **jq**: JSON フィルタリングに必要
- **python3**: パラメータファイルのプレースホルダー展開に必要（`--parameters` オプションで直接指定する場合は不要）

## このスキルを使わない場合

以下の場合は静的分析で十分である：

- 「Bicepファイルの構文を確認して」（リンター実行）
- 「このモジュールは何を作成する？」（コードリーディング）
- 「パラメータのデフォルト値は？」（ファイル参照）
