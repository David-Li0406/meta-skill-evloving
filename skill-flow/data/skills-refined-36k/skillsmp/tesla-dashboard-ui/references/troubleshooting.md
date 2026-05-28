# Troubleshooting / トラブルシューティング

Tesla Dashboard UIでよくある問題と解決方法について解説します。

## Build Errors / ビルドエラー

### "Cannot find 'TeslaColors' in scope"

**原因:** ファイルがプロジェクトに追加されていない、またはターゲットに含まれていない。

**解決方法:**
1. `tesla-colors.swift` がプロジェクトに追加されていることを確認
2. File Inspector でターゲットにチェックが入っていることを確認
3. Clean Build Folder (Cmd + Shift + K) を実行

```swift
// 正しいインポート順序
// 1. tesla-colors.swift
// 2. tesla-typography.swift
// 3. tesla-animation.swift
// 4. tesla-theme-provider.swift
// 5. 他のコンポーネント
```

### "Type 'TeslaVehicle' does not conform to 'PersistentModel'"

**原因:** SwiftData の `@Model` マクロが正しく適用されていない。

**解決方法:**
```swift
import SwiftData

@Model
final class TeslaVehicle {
    // class でなければならない（struct は不可）
    // final が推奨
}
```

### "@Observable requires iOS 17.0 or newer"

**原因:** iOS 17未満のターゲットで `@Observable` を使用している。

**解決方法:**
1. Deployment Target を iOS 17.0 以上に設定
2. または `ObservableObject` にフォールバック

```swift
// iOS 17+
@Observable
final class TeslaTheme { }

// iOS 16以下
final class TeslaTheme: ObservableObject {
    @Published var colors: TeslaColorScheme = .dark
}
```

## Runtime Errors / ランタイムエラー

### "ModelContainer creation failed"

**原因:** SwiftData のスキーマが不正、またはマイグレーションが必要。

**解決方法:**
```swift
// 開発中はメモリ内のみに保存してテスト
let modelConfiguration = ModelConfiguration(
    schema: schema,
    isStoredInMemoryOnly: true  // 開発時はtrue
)

// または既存データを削除
// アプリを削除して再インストール
```

### "Location authorization status: denied"

**原因:** 位置情報の使用許可がない。

**解決方法:**
1. Info.plist に必要なキーを追加：

```xml
<key>NSLocationWhenInUseUsageDescription</key>
<string>ナビゲーションと現在地表示に位置情報を使用します</string>
```

2. シミュレータの場合: Features → Location → Custom Location

### "AVAudioSession activation failed"

**原因:** オーディオセッションの設定が不正。

**解決方法:**
```swift
do {
    try AVAudioSession.sharedInstance().setCategory(.playback, mode: .default)
    try AVAudioSession.sharedInstance().setActive(true)
} catch {
    print("Audio session error: \(error)")
}
```

バックグラウンド再生が必要な場合は Info.plist に追加：
```xml
<key>UIBackgroundModes</key>
<array>
    <string>audio</string>
</array>
```

## UI Issues / UI問題

### ガラスモーフィズムが表示されない

**原因:** `.ultraThinMaterial` が機能していない。

**解決方法:**
```swift
// 背景色を確認
.background(.ultraThinMaterial)
.background(TeslaColors.glassBackground)  // フォールバック

// 親ビューに背景があることを確認
ZStack {
    TeslaColors.background  // 背景が必要

    TeslaIconButton(...)
        .teslaGlassmorphism()
}
```

### アニメーションが動作しない

**原因:** `accessibilityReduceMotion` が有効、または `Animation` が適用されていない。

**解決方法:**
```swift
// Reduce Motionを確認
@Environment(\.accessibilityReduceMotion) private var reduceMotion

withAnimation(reduceMotion ? .none : TeslaAnimation.quick) {
    // ...
}

// 明示的にanimationを適用
.animation(TeslaAnimation.standard, value: isSelected)
```

### Dynamic Type でレイアウトが崩れる

**原因:** 固定サイズを使用している。

**解決方法:**
```swift
// ❌ 固定サイズ
.frame(width: 200)

// ✅ 最小/最大サイズ
.frame(minWidth: 100, maxWidth: 300)

// ✅ ScaledMetric
@ScaledMetric(relativeTo: .body) private var iconSize: CGFloat = 24
```

### タッチ領域が小さすぎる

**原因:** タップ可能領域が44x44pt未満。

**解決方法:**
```swift
Button { } label: {
    Image(systemName: "gear")
        .font(.system(size: 16))
}
.frame(minWidth: 44, minHeight: 44)  // 最小サイズを確保

// または contentShape
HStack { /* small content */ }
    .contentShape(Rectangle())
    .frame(minHeight: 44)
```

## Data Issues / データ問題

### SwiftData の変更が保存されない

**原因:** `modelContext` が正しく設定されていない。

**解決方法:**
```swift
// Viewで modelContext を使用
@Environment(\.modelContext) private var modelContext

func saveChanges() {
    // 自動保存されるが、明示的に保存する場合
    try? modelContext.save()
}
```

### プレビューでデータが表示されない

**原因:** プレビュー用のコンテナが設定されていない。

**解決方法:**
```swift
#Preview {
    TeslaVehicleScreen(vehicleData: .preview)
        .modelContainer(for: [TeslaVehicle.self], inMemory: true)
}

// または Preview データを使用
extension VehicleData {
    static var preview: VehicleData {
        VehicleData(
            name: "My Model S",
            batteryLevel: 80,
            // ...
        )
    }
}
```

## Performance Issues / パフォーマンス問題

### スクロールがカクつく

**原因:** 複雑なビューの再描画。

**解決方法:**
```swift
// LazyVStack を使用
ScrollView {
    LazyVStack {  // VStack ではなく LazyVStack
        ForEach(items) { item in
            ItemRow(item: item)
        }
    }
}

// drawingGroup() で GPU レンダリング
ComplexAnimatedView()
    .drawingGroup()
```

### メモリ使用量が高い

**原因:** 画像キャッシュ、または不要なオブジェクトの保持。

**解決方法:**
```swift
// AsyncImage を使用
AsyncImage(url: imageURL) { image in
    image.resizable()
} placeholder: {
    ProgressView()
}

// 大きな画像はサイズを制限
image.resizable()
    .aspectRatio(contentMode: .fill)
    .frame(width: 200, height: 200)
    .clipped()
```

## MapKit Issues / MapKit問題

### 地図が表示されない

**原因:** 位置情報の権限がない、またはネットワーク接続がない。

**解決方法:**
1. 位置情報の権限を確認
2. シミュレータで Location を設定
3. ネットワーク接続を確認

### ルートが表示されない

**原因:** ルート計算に失敗。

**解決方法:**
```swift
// エラーハンドリングを追加
func calculateRoute() async {
    let result = await navigationManager.startNavigation(to: destination)

    switch result {
    case .success(let route):
        print("ルート計算成功: \(route.distance)m")
    case .failure(let error):
        print("ルート計算失敗: \(error.localizedDescription)")
        // ユーザーにエラーを表示
    }
}
```

## Common Mistakes / よくある間違い

### 1. @State の初期化

```swift
// ❌ Bad: init で @State を設定
init(value: Int) {
    self.value = value  // 動作しない
}

// ✅ Good: _value で設定
init(value: Int) {
    _value = State(initialValue: value)
}
```

### 2. ObservableObject の更新

```swift
// ❌ Bad: バックグラウンドスレッドで更新
DispatchQueue.global().async {
    self.data = newData  // クラッシュの可能性
}

// ✅ Good: MainActor で更新
Task { @MainActor in
    self.data = newData
}
```

### 3. Environment の伝播

```swift
// ❌ Bad: sheet 内で Environment が利用できない
.sheet(isPresented: $showSheet) {
    ChildView()  // teslaTheme が利用できない
}

// ✅ Good: Environment を明示的に渡す
.sheet(isPresented: $showSheet) {
    ChildView()
        .environment(\.teslaTheme, theme)
}
```

## Debug Tips / デバッグヒント

### View の再描画を確認

```swift
var body: some View {
    let _ = print("Rendering: \(Self.self)")

    VStack { /* content */ }
}
```

### SwiftData クエリをログ

```swift
#if DEBUG
func logQuery<T>(_ descriptor: FetchDescriptor<T>, results: [T]) {
    print("Query: \(T.self), Results: \(results.count)")
}
#endif
```

### 位置情報をシミュレート

```
Simulator → Features → Location → Custom Location
```

## Related Documents / 関連ドキュメント

- [Error Handling](./error-handling.md)
- [Accessibility Guide](./accessibility-guide.md)
- [SwiftData Models](./swiftdata-models.md)
