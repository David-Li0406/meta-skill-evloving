# トラブルシューティング (macOS)

macOSでのMapKit関連の問題解決ガイド。

## 位置情報が取得できない

### 1. エンタイトルメント確認

必須エンタイトルメント:
```xml
<key>com.apple.security.app-sandbox</key>
<true/>
<key>com.apple.security.personal-information.location</key>
<true/>
<key>com.apple.security.network.client</key>
<true/>
```

**重要:** `network.client`がないと位置情報取得に失敗する場合があります。

### 2. Info.plist確認

```xml
<key>NSLocationUsageDescription</key>
<string>現在地を地図上に表示するために位置情報を使用します。</string>
```

### 3. システム環境設定確認

1. システム環境設定 > プライバシーとセキュリティ > 位置情報サービス
2. 位置情報サービスが有効になっているか確認
3. アプリが許可リストにあるか確認

### 4. 権限リセット

```bash
# ターミナルで実行
tccutil reset LocationServices com.your.bundle.id
```

## 地図が表示されない

### 1. ネットワーク接続

- インターネット接続を確認
- ファイアウォール設定を確認
- プロキシ設定を確認

### 2. エンタイトルメント

```xml
<key>com.apple.security.network.client</key>
<true/>
```

### 3. デバッグ

```swift
// 地図の読み込み状態を確認
Map(position: $position) {
    // content
}
.onAppear {
    print("Map appeared")
}
```

## CLError コード一覧

| コード | 名前 | 説明 | 対処法 |
|-------|------|------|--------|
| 0 | `.locationUnknown` | 位置を特定できない | リトライ |
| 1 | `.denied` | 権限が拒否された | 設定へ誘導 |
| 2 | `.network` | ネットワークエラー | 接続確認、リトライ |
| 3 | `.headingFailure` | 方位取得失敗 | ハードウェア確認 |
| 4 | `.regionMonitoringDenied` | リージョン監視拒否 | - |
| 5 | `.regionMonitoringFailure` | リージョン監視失敗 | - |
| 6 | `.regionMonitoringSetupDelayed` | セットアップ遅延 | 待機 |
| 7 | `.regionMonitoringResponseDelayed` | 応答遅延 | 待機 |
| 8 | `.geocodeFoundNoResult` | ジオコード結果なし | クエリ確認 |
| 9 | `.geocodeFoundPartialResult` | 部分的な結果 | 結果確認 |
| 10 | `.geocodeCanceled` | ジオコードキャンセル | - |
| 11 | `.deferredFailed` | 遅延位置取得失敗 | - |
| 12 | `.deferredNotUpdatingLocation` | 位置更新していない | startUpdating確認 |
| 13 | `.deferredAccuracyTooLow` | 精度が低すぎる | 精度設定確認 |
| 14 | `.deferredDistanceFiltered` | フィルターで除外 | distanceFilter確認 |
| 15 | `.deferredCanceled` | 遅延取得キャンセル | - |
| 16 | `.rangingUnavailable` | レンジング利用不可 | - |
| 17 | `.rangingFailure` | レンジング失敗 | - |
| 18 | `.promptDeclined` | プロンプト拒否 | - |
| 19 | `.historicalLocationError` | 履歴位置エラー | - |

## MKError コード一覧

| コード | 名前 | 説明 | 対処法 |
|-------|------|------|--------|
| 1 | `.unknown` | 不明なエラー | リトライ |
| 2 | `.serverFailure` | サーバーエラー | リトライ |
| 3 | `.loadingThrottled` | レート制限 | 待機してリトライ |
| 4 | `.placemarkNotFound` | 場所が見つからない | クエリ確認 |
| 5 | `.directionsNotFound` | 経路が見つからない | 別の交通手段を試す |
| 6 | `.decodingFailed` | デコード失敗 | データ確認 |

## Sandbox関連エラー

### エンタイトルメント不足

**症状:** アプリがクラッシュ、または機能しない

**確認方法:**
```bash
# アプリのエンタイトルメントを確認
codesign -d --entitlements - /path/to/YourApp.app
```

**解決:**
1. Xcodeで正しいエンタイトルメントを設定
2. ビルド設定で`CODE_SIGN_ENTITLEMENTS`を確認

### コード署名エラー

**症状:** 「開発元を確認できない」エラー

**解決:**
1. 有効な開発者証明書で署名
2. 公証（Notarization）を実行

```bash
# 公証
xcrun notarytool submit YourApp.dmg --keychain-profile "YourProfile" --wait
```

## Look Around問題

### フルスクリーンボタンが表示されない

**原因:** macOS 15時点での既知の問題

**回避策:**
- 埋め込みプレビューのみ使用
- シートやポップオーバーで大きく表示

### シーンが読み込めない

**原因:**
1. カバレッジ外の場所
2. ネットワークエラー

**対処:**
```swift
func loadScene(for coordinate: CLLocationCoordinate2D) async {
    let request = MKLookAroundSceneRequest(coordinate: coordinate)

    do {
        lookAroundScene = try await request.scene
    } catch {
        // フォールバック表示
        showFallbackView = true
    }
}
```

## パフォーマンス問題

### 地図の動作が遅い

1. **マーカー数を減らす**
   - クラスタリングを使用
   - 表示範囲のマーカーのみ表示

2. **オーバーレイを最適化**
   - 複雑なポリゴンを簡略化
   - 不要なオーバーレイを削除

3. **更新頻度を下げる**
   - `onMapCameraChange(frequency: .onEnd)`を使用

### メモリ使用量が高い

1. **不要なリソースを解放**
   - 非表示時にシーンを解放
   - 画像キャッシュをクリア

2. **Instrumentsでプロファイリング**
   ```
   Xcode > Product > Profile > Leaks
   ```

## デバッグ方法

### コンソールログ

```swift
// 位置情報デバッグ
func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
    #if DEBUG
    if let location = locations.last {
        print("📍 Location: \(location.coordinate.latitude), \(location.coordinate.longitude)")
        print("   Accuracy: \(location.horizontalAccuracy)m")
    }
    #endif
}
```

### 権限状態のログ

```swift
func logAuthorizationStatus(_ status: CLAuthorizationStatus) {
    #if DEBUG
    let statusString: String
    switch status {
    case .notDetermined: statusString = "notDetermined"
    case .restricted: statusString = "restricted"
    case .denied: statusString = "denied"
    case .authorized: statusString = "authorized"
    case .authorizedAlways: statusString = "authorizedAlways"
    @unknown default: statusString = "unknown"
    }
    print("🔐 Authorization: \(statusString)")
    #endif
}
```

### シミュレータでのテスト

1. **位置情報シミュレーション**
   - Simulator > Features > Location
   - GPXファイルでカスタムルート

2. **権限のテスト**
   - システム環境設定で権限を変更
   - tccutilでリセット

## よくある問題と解決策

| 問題 | 原因 | 解決策 |
|------|------|--------|
| 地図が白い | ネットワーク/エンタイトルメント | network.client確認 |
| 現在地が表示されない | 権限/エンタイトルメント | 権限とInfo.plist確認 |
| マーカーが表示されない | 座標が範囲外 | 座標値を確認 |
| 経路が表示されない | ルートが見つからない | transportType確認 |
| アプリがクラッシュ | エンタイトルメント不足 | codesignで確認 |
| 審査でリジェクト | 説明文不足 | NSLocationUsageDescription確認 |
