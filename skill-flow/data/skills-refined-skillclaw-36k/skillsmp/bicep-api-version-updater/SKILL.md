---
name: bicep-api-version-updater
description: BicepファイルのAzure リソースAPIバージョンを最新化。「APIバージョンを更新」「Bicepを最新化」「古いAPIバージョンをチェック」を求める場合に使用。
---

# Bicep API Version Updater

BicepファイルのAzureリソースAPIバージョンを最新の安定版に更新する。

## Tools

| Tool | 用途 |
|------|------|
| `az provider show` | 最新GA版の取得（プライマリ） |
| `microsoft_docs_fetch` | 最新GA版の取得（フォールバック：APIリファレンス参照） |
| `az bicep build` | 構文検証・Linterチェック |
| `microsoft_docs_search` | Breaking changes情報の検索 |
| `grep` / `view` | Bicepファイルの解析 |
| `edit` | APIバージョンの更新 |

### bicepschemaを使用しない理由

> **注意:** 以下は挙動観察に基づく注意点であり、公式ドキュメントに明記された仕様ではない。

Azure MCP Serverの`bicepschema`が返すAPIバージョンと、`az provider show`が返す最新GA版が異なるケースが観察されている（例: Microsoft.Network/virtualNetworksでbicepschemaは2024-07-01、az provider showは2025-05-01を返す）。この差異が「既に最新」の誤判断を招く可能性があるため、最新版の判定には`az provider show`を使用する。

### az provider showの制限

`az provider show` はリソースプロバイダーに登録されているリソースタイプのみを返す。一部の子リソース（例: `redisEnterprise/databases/accessPolicyAssignments`）は登録されていない場合があり、その場合はAPIリファレンスを参照する必要がある。

## 更新フロー

```
1. Bicepファイル解析 → Step 1
   ↓
2. プレビュー版チェック → Step 2
   - "-preview" を含む場合は更新スキップ
   ↓
3. 最新GA版の取得と比較 → Step 3
   - az provider show で最新GA版を取得
   - 現在のバージョンと比較
   ↓
4. Breaking Changes確認 → Step 4
   ↓
5. APIバージョン更新（仮適用） → Step 5
   ↓
6. Linter検証 → Step 6
   - 警告が出た場合は元のバージョンに戻す
```

## スキップ理由の分類

| 理由 | 報告時の状態 | 追加アクション |
|------|-------------|---------------|
| プレビュー版使用中 | ⏭️ スキップ（プレビュー版） | GA移行可否の分析（必須） |
| 既に最新GA版 | ⏭️ スキップ（既に最新） | なし |
| GA版が存在しない | ⏭️ スキップ（GA版なし） | なし |
| Linter警告発生 | ⚠️ スキップ（BCP081警告） | なし |

## 実行手順

### Step 1: リソースタイプとAPIバージョンの抽出

```bash
grep -E "^resource\s+" infra/**/*.bicep
```

### Step 2: プレビュー版のスキップ判定

APIバージョンに `-preview` が含まれる場合は**更新をスキップ**。

**ただし、以下の分析は必ず実施すること:**

1. 現在のBicepファイルで使用している属性を特定
2. `az provider show` で最新GA版を取得
3. コードの属性がGA版でサポートされているか確認（ドキュメント検索）
4. 結果を出力フォーマットの「プレビュー版分析セクション」に含める

### Step 3: 最新GA版の取得と比較

#### 3-1. 最新GA版の取得

```bash
az provider show -n Microsoft.Network \
  --query "resourceTypes[?resourceType=='virtualNetworks'].apiVersions" \
  -o tsv | tr '\t' '\n' | grep -iv preview | head -1
```

複数リソースタイプの一括取得:
```bash
for provider_resource in \
  "Microsoft.ManagedIdentity:userAssignedIdentities" \
  "Microsoft.Network:virtualNetworks" \
  "Microsoft.Authorization:roleAssignments"
do
  provider="${provider_resource%%:*}"
  resource="${provider_resource##*:}"
  echo "=== $provider/$resource ==="
  az provider show -n "$provider" \
    --query "resourceTypes[?resourceType=='$resource'].apiVersions" \
    -o tsv 2>/dev/null | tr '\t' '\n' | grep -iv preview | head -1
done
```

#### 3-2. 比較と判断

- 現在のバージョン == 最新GA版 → スキップ（既に最新）
- 現在のバージョン < 最新GA版 → Step 4へ

#### 3-3. フォールバック: APIリファレンス参照

`az provider show` で結果が空の場合（リソースタイプが登録されていない場合）、`microsoft_docs_fetch` でAPIリファレンスを参照:

```
URL形式:
https://learn.microsoft.com/en-us/azure/templates/{provider}/{resourceType}

例:
https://learn.microsoft.com/en-us/azure/templates/microsoft.cache/redisenterprise/databases/accesspolicyassignments
```

APIリファレンスページの上部に利用可能なAPIバージョン一覧が表示される。`-preview` を含まない最新バージョンを選択する。

### Step 4: Breaking Changes確認

`microsoft_docs_search` で破壊的変更を検索:

```
検索クエリ例:
- "Microsoft.ContainerService managedClusters API breaking changes"
```

参考リンク:
- AKS: https://aka.ms/aks/breakingchanges

### Step 5: APIバージョン更新（仮適用）

`edit` ツールで更新。この時点では「仮適用」。

### Step 6: Linter検証と更新確定

```bash
az bicep build --file infra/main.bicep 2>&1
```

#### 警告が出た場合の対応（必須）

1. **更新前のバージョンに戻す**
2. 「スキップされたリソース」として報告

**禁止:** 型定義がサポートする中間バージョンへの変更

#### 警告が出なかった場合

更新確定。

## 出力フォーマット（必須）

以下のセクションを**必ず**含めること:

1. **更新サマリーテーブル** - 全リソースの更新状況（BCP081警告も含む）
2. **プレビュー版分析セクション** - GA移行可否と理由（プレビュー版が存在する場合）

### テンプレート

```markdown
## APIバージョン更新サマリー

| ファイル | リソースタイプ | 更新前 | 更新後 | 状態 |
|----------|---------------|--------|--------|------|
| identity.bicep | Microsoft.ManagedIdentity/userAssignedIdentities | 2023-01-31 | 2024-11-30 | ✅ 更新 |
| aks.bicep | Microsoft.ContainerService/managedClusters | 2025-06-02-preview | - | ⏭️ スキップ（プレビュー版） |
| network.bicep | Microsoft.Network/virtualNetworks | 2024-07-01 | - | ⏭️ スキップ（既に最新） |
| network.bicep | Microsoft.Network/publicIPAddresses | 2024-07-01 | - | ⚠️ スキップ（BCP081警告） |

**BCP081警告について:** 最新GA版への更新を試みたが、Bicep型定義が未対応のため元のバージョンを維持した。Bicep CLI更新後に再実行で更新可能になる場合がある。

### スキップされたプレビュー版リソースの分析

| ファイル | リソースタイプ | 現在のバージョン | 最新GA版 | GA移行可否 |
|----------|---------------|-----------------|---------|-----------|
| aks.bicep | Microsoft.ContainerService/managedClusters | 2025-06-02-preview | 2025-10-01 | ❌ 不可 |

**GA版に存在しない属性:**
- `properties.networkProfile.advancedNetworking.security.advancedNetworkPolicies`

上記の属性はプレビュー専用のため、GA版への移行には機能の代替または削除が必要である。
すべての属性がGA版に存在する場合は「✅ 可能」と表示され、GA版への移行を検討できる。
```

## 前提条件

- Azure CLIでログイン済み（`az login`）
- Bicep CLIがインストール済み

## このスキルを使わない場合

- 「特定のプレビュー機能を使いたい」（意図的なプレビュー使用）
- 「APIバージョンを固定したい」（安定性優先）

## 関連スキル

- **bicep-what-if-analysis**: デプロイ前の影響分析とノイズ除去
