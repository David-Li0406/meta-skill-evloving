# Material 3 Expressive Troubleshooting

よくある問題と解決策のガイド。

## ビルドエラー

### Unresolved reference: MaterialExpressiveTheme

**原因**: Material 3 のバージョンが古い

**解決策**:
```kotlin
// build.gradle.kts
dependencies {
    implementation("androidx.compose.material3:material3:1.4.0-alpha15")
    // または
    implementation(platform("androidx.compose:compose-bom:2024.12.01"))
    implementation("androidx.compose.material3:material3")
}
```

### This declaration is experimental and its usage must be marked

**原因**: ExperimentalMaterial3ExpressiveApi のオプトインが必要

**解決策**:
```kotlin
// ファイルレベル
@file:OptIn(ExperimentalMaterial3ExpressiveApi::class)

// または関数レベル
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun MyComponent() { ... }

// または build.gradle.kts でプロジェクト全体に適用
kotlin {
    compilerOptions {
        freeCompilerArgs.add("-opt-in=androidx.compose.material3.ExperimentalMaterial3ExpressiveApi")
    }
}
```

### Unresolved reference: MotionScheme

**原因**: Compose バージョンが古い

**解決策**:
```kotlin
// compose-bom を 2024.12.01 以上に更新
implementation(platform("androidx.compose:compose-bom:2024.12.01"))
```

### Unresolved reference: LoadingIndicator

**原因**: Import が不足

**解決策**:
```kotlin
import androidx.compose.material3.LoadingIndicator
import androidx.compose.material3.ContainedLoadingIndicator
```

## ランタイムエラー

### Shape morphing not working

**原因 1**: MaterialExpressiveTheme で wrap されていない

**解決策**:
```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun MyApp() {
    MaterialExpressiveTheme {  // 必須
        MyContent()
    }
}
```

**原因 2**: MotionScheme が standard() になっている

**解決策**:
```kotlin
MaterialExpressiveTheme(
    motionScheme = MotionScheme.expressive()  // expressive を使用
) { ... }
```

### Animation feels different than expected

**原因**: 間違った spec タイプを使用

**解決策**:
```kotlin
val motionScheme = LocalMotionScheme.current

// サイズ/位置の変更には Spatial
val size by animateDpAsState(
    targetValue = targetSize,
    animationSpec = motionScheme.defaultSpatialSpec()  // Spatial を使用
)

// 色/透明度の変更には Effects
val color by animateColorAsState(
    targetValue = targetColor,
    animationSpec = motionScheme.defaultEffectsSpec()  // Effects を使用
)
```

### Carousel items not rendering

**原因**: rememberCarouselState の itemCount が 0

**解決策**:
```kotlin
HorizontalMultiBrowseCarousel(
    state = rememberCarouselState { items.count() },  // 正しいカウント
    ...
) { index ->
    // Content
}
```

### ButtonGroup shapes not connecting

**原因**: 正しい shape が指定されていない

**解決策**:
```kotlin
ButtonGroup(spacing = ButtonGroupDefaults.ConnectedSpacing) {
    ToggleButton(
        shape = ButtonGroupDefaults.connectedLeadingButtonShape  // 先頭
    ) { ... }
    ToggleButton(
        shape = ButtonGroupDefaults.connectedMiddleButtonShape   // 中間
    ) { ... }
    ToggleButton(
        shape = ButtonGroupDefaults.connectedTrailingButtonShape // 末尾
    ) { ... }
}
```

## パフォーマンス問題

### アニメーションがカクつく

**原因 1**: 過度な recomposition

**解決策**:
```kotlin
// remember を使用して不要な再計算を防ぐ
val motionScheme = LocalMotionScheme.current
val animationSpec = remember { motionScheme.defaultSpatialSpec<Dp>() }

val size by animateDpAsState(
    targetValue = targetSize,
    animationSpec = animationSpec
)
```

**原因 2**: デバッグビルド

**解決策**: リリースビルドでテスト

### カルーセルのスクロールが重い

**原因**: 複雑なコンテンツの再作成

**解決策**:
```kotlin
HorizontalMultiBrowseCarousel(
    state = carouselState,
    ...
) { index ->
    // key を使用して再利用を最適化
    key(items[index].id) {
        CarouselItem(item = items[index])
    }
}
```

### メモリ使用量が高い

**原因**: 画像のキャッシュ問題

**解決策**:
```kotlin
// Coil を使用した最適化
AsyncImage(
    model = ImageRequest.Builder(LocalContext.current)
        .data(imageUrl)
        .crossfade(true)
        .memoryCachePolicy(CachePolicy.ENABLED)
        .diskCachePolicy(CachePolicy.ENABLED)
        .build(),
    contentDescription = null
)
```

## Preview 問題

### Preview が表示されない

**原因**: ExperimentalApi のオプトインが Preview に適用されていない

**解決策**:
```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview
@Composable
private fun MyPreview() {
    MaterialExpressiveTheme {
        MyComponent()
    }
}
```

### Preview でアニメーションが動かない

**原因**: Preview は静的レンダリング

**解決策**: Interactive Preview または実機/エミュレータでテスト

## 互換性問題

### 古い Android バージョンでクラッシュ

**原因**: Dynamic Color は Android 12+ のみ

**解決策**:
```kotlin
val colorScheme = when {
    Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
        dynamicColorScheme(context)
    }
    else -> {
        // フォールバックカラースキーム
        lightColorScheme()
    }
}
```

### Compose Multiplatform で動作しない

**原因**: 一部の Expressive 機能は Android 専用

**解決策**:
```kotlin
// expect/actual パターンで分岐
@Composable
expect fun PlatformLoadingIndicator()

// Android
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
actual fun PlatformLoadingIndicator() {
    LoadingIndicator()
}

// Other platforms
@Composable
actual fun PlatformLoadingIndicator() {
    CircularProgressIndicator()
}
```

## エラーメッセージ一覧

| エラー | 原因 | 解決策 |
|--------|------|--------|
| `Unresolved reference: MaterialExpressiveTheme` | バージョン不足 | material3:1.4.0-alpha15+ |
| `This declaration is experimental` | OptIn 不足 | `@OptIn` を追加 |
| `Unresolved reference: MotionScheme` | BOM が古い | compose-bom:2024.12.01+ |
| `Type mismatch: Required SpringSpec` | 型不一致 | 正しい型パラメータを指定 |
| `NoSuchMethodError` | バージョン競合 | BOM で統一 |

## デバッグのヒント

### 1. アニメーションのデバッグ

```kotlin
// アニメーション値をログ出力
val size by animateDpAsState(
    targetValue = targetSize,
    animationSpec = motionScheme.defaultSpatialSpec(),
    label = "sizeAnimation"  // Compose Metrics でトラッキング
)

LaunchedEffect(size) {
    Log.d("Animation", "Current size: $size")
}
```

### 2. Recomposition のデバッグ

```kotlin
// Compose Compiler Reports を有効化
// build.gradle.kts
composeCompiler {
    reportsDestination = layout.buildDirectory.dir("compose_reports")
    metricsDestination = layout.buildDirectory.dir("compose_metrics")
}
```

### 3. Layout Inspector の使用

Android Studio の Layout Inspector で
Compose の recomposition を可視化できます。

## 関連リソース

- [Migration Guide](migration-guide.md) - 移行ガイド
- [Motion System](motion-system.md) - アニメーション詳細
- [Theming](theming.md) - テーマ設定
