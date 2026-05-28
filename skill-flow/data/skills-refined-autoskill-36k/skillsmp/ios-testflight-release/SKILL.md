---
name: ios-testflight-release
description: iOS TestFlight リリース自動化。「TestFlightにリリース」「iOSリリース」「TestFlightアップロード」と言われたときに使用。
---

# iOS TestFlight リリース自動化

このスキルは Flutter iOS アプリを TestFlight にリリースするプロセスを自動化します。
他のFlutterプロジェクトにも `.claude/` フォルダをコピーするだけで使えます。

## 実行コマンド

プロジェクトルートから以下のスクリプトを実行してください:

```bash
.claude/scripts/upload-testflight.sh
```

## 前提条件

### 1. 環境変数の設定

以下の環境変数が必要です:

```bash
export APPLE_ID="your@email.com"
export APP_SPECIFIC_PASSWORD="xxxx-xxxx-xxxx-xxxx"
export TEAM_ID="XXXXXXXXXX"  # 複数チームに所属している場合
```

### 2. App用パスワードの生成方法

1. https://appleid.apple.com にアクセス
2. サインインとセキュリティ → App用パスワード
3. 「+」ボタンで新しいパスワードを生成
4. 生成されたパスワードを `APP_SPECIFIC_PASSWORD` に設定

### 3. チームIDの確認方法

```bash
# Xcode でプロジェクトを開き、Signing & Capabilities で確認
# または App Store Connect のユーザーとアクセスで確認
```

## 処理フロー

1. **環境変数チェック** - 必要な認証情報が設定されているか確認
2. **クリーンビルド** - `flutter clean` と `flutter pub get`
3. **IPAビルド** - `flutter build ipa --release`
4. **TestFlightアップロード** - `xcrun altool --upload-app`

## バージョン管理

バージョン番号は `pubspec.yaml` から自動取得されます:

```yaml
version: 1.0.0+1  # バージョン+ビルド番号
```

ビルド番号を上げる場合は、pubspec.yaml を更新してからスクリプトを実行してください。

## トラブルシューティング

### IPAファイルが見つからない

```bash
# ビルドディレクトリを確認
ls -la build/ios/ipa/
```

### 認証エラー

- Apple IDとパスワードが正しいか確認
- App用パスワードが有効か確認
- 2ファクタ認証が有効か確認

### コード署名エラー

```bash
# Xcode でプロジェクトを開き、Signing を確認
open ios/Runner.xcworkspace
```

## 使用例

ユーザーが以下のように言ったとき、このスキルを使用:

- 「TestFlightにリリースして」
- 「iOSアプリをTestFlightにアップロード」
- 「iOS リリースビルドを作成してアップロード」
- 「TestFlight にデプロイ」
