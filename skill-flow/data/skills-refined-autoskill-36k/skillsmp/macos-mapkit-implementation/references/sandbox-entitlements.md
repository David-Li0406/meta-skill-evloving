# App Sandbox & Entitlements

macOSアプリでMapKitを使用するためのApp Sandbox設定。

## App Sandboxとは

App Sandboxは、macOSアプリのセキュリティ機能で、アプリが使用できるリソースを制限します。

- Mac App Store配布には**必須**
- 開発者ID配布でも推奨
- 位置情報などの機密データにはエンタイトルメントが必要

## 必須エンタイトルメント

### 1. App Sandbox有効化

```xml
<key>com.apple.security.app-sandbox</key>
<true/>
```

### 2. 位置情報アクセス

```xml
<key>com.apple.security.personal-information.location</key>
<true/>
```

### 3. ネットワークアクセス（重要！）

```xml
<key>com.apple.security.network.client</key>
<true/>
```

**重要:** 位置情報サービスは内部的にネットワークを使用するため、このエンタイトルメントがないと位置情報取得に失敗する場合があります。

## エンタイトルメントファイル例

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.app-sandbox</key>
    <true/>
    <key>com.apple.security.personal-information.location</key>
    <true/>
    <key>com.apple.security.network.client</key>
    <true/>
</dict>
</plist>
```

## Xcodeでの設定方法

### Signing & Capabilities

1. プロジェクトナビゲータでプロジェクトを選択
2. ターゲットを選択
3. **Signing & Capabilities** タブを選択
4. **+ Capability** をクリック
5. **App Sandbox** を追加

### Sandbox設定

App Sandboxを追加後、以下を設定:

**Location:**
- ☑️ Location

**Network:**
- ☑️ Outgoing Connections (Client)

### 自動生成ファイル

設定すると、`.entitlements`ファイルが自動生成されます:
- `YourApp.entitlements`（通常ターゲット）
- `YourAppTests.entitlements`（テストターゲット）

## Hardened Runtime（非Sandbox）

Mac App Store外で配布する場合、Hardened Runtimeを使用:

```xml
<key>com.apple.security.cs.disable-library-validation</key>
<true/>
```

**注意:** Sandboxと異なり、位置情報に特別なエンタイトルメントは不要ですが、Info.plistの設定は必要です。

## エンタイトルメント一覧

### 位置情報関連

| エンタイトルメント | 説明 |
|------------------|------|
| `com.apple.security.personal-information.location` | 位置情報アクセス |

### ネットワーク関連

| エンタイトルメント | 説明 |
|------------------|------|
| `com.apple.security.network.client` | 送信接続（クライアント） |
| `com.apple.security.network.server` | 受信接続（サーバー） |

### その他（参考）

| エンタイトルメント | 説明 |
|------------------|------|
| `com.apple.security.files.user-selected.read-only` | ユーザー選択ファイル読み取り |
| `com.apple.security.files.user-selected.read-write` | ユーザー選択ファイル読み書き |
| `com.apple.security.personal-information.calendars` | カレンダーアクセス |
| `com.apple.security.personal-information.contacts` | 連絡先アクセス |
| `com.apple.security.personal-information.photos-library` | フォトライブラリアクセス |

## トラブルシューティング

### 位置情報が取得できない

1. **エンタイトルメント確認**
   - `personal-information.location` が設定されているか
   - `network.client` が設定されているか

2. **Info.plist確認**
   - `NSLocationUsageDescription` が設定されているか

3. **システム環境設定確認**
   - プライバシーとセキュリティ > 位置情報サービス
   - アプリが許可されているか

### ビルドは成功するが実行時にエラー

1. **コード署名の確認**
   - 開発証明書が有効か
   - エンタイトルメントファイルが正しく参照されているか

2. **ビルド設定の確認**
   - `CODE_SIGN_ENTITLEMENTS` の値が正しいか

### Mac App Store審査でリジェクト

1. **必要最小限の権限**
   - 使用しないエンタイトルメントを削除
   - 位置情報の使用理由を明確に

2. **プライバシーポリシー**
   - 位置情報の使用について記載

3. **説明文の確認**
   - Info.plistの説明文が適切か

## ベストプラクティス

1. **最小権限の原則**
   - 必要なエンタイトルメントのみ追加
   - 不要な権限は削除

2. **開発中からSandbox**
   - 開発初期からSandbox環境でテスト
   - 配布前に問題を発見

3. **権限リクエストの説明**
   - ユーザーにわかりやすい説明文
   - 使用目的とメリットを明記

4. **グレースフルデグレード**
   - 権限がない場合も基本機能は動作するように
   - エラーメッセージは適切に

## 参考リンク

- [App Sandbox Design Guide](https://developer.apple.com/library/archive/documentation/Security/Conceptual/AppSandboxDesignGuide/)
- [Entitlements - Apple Developer](https://developer.apple.com/documentation/bundleresources/entitlements)
