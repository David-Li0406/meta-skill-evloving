# Material 3 Expressive Theming

MaterialExpressiveTheme を使用した包括的なテーマカスタマイズガイド。

## Overview

Material 3 Expressive では `MaterialExpressiveTheme()` を使用してアプリ全体のテーマを設定します。
従来の `MaterialTheme()` を拡張し、MotionScheme を含む新しいカスタマイズオプションを提供します。

## 基本セットアップ

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun MyApp() {
    MaterialExpressiveTheme(
        colorScheme = lightColorScheme(),
        typography = Typography,
        shapes = Shapes,
        motionScheme = MotionScheme.expressive()
    ) {
        Surface(
            modifier = Modifier.fillMaxSize(),
            color = MaterialTheme.colorScheme.background
        ) {
            MainContent()
        }
    }
}
```

## テーマコンポーネント

### 1. Color Scheme

```kotlin
// Dynamic Color（Android 12+）
val dynamicColorScheme = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
    val context = LocalContext.current
    if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
} else {
    if (darkTheme) darkColorScheme() else lightColorScheme()
}

// カスタムカラースキーム
val customLightColorScheme = lightColorScheme(
    primary = Color(0xFF6200EE),
    onPrimary = Color.White,
    primaryContainer = Color(0xFFBB86FC),
    onPrimaryContainer = Color(0xFF3700B3),
    secondary = Color(0xFF03DAC5),
    // ... 他のカラー
)
```

### 2. Typography

```kotlin
val ExpressiveTypography = Typography(
    displayLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 57.sp,
        lineHeight = 64.sp,
        letterSpacing = (-0.25).sp
    ),
    displayMedium = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 45.sp,
        lineHeight = 52.sp,
        letterSpacing = 0.sp
    ),
    // ... 他のスタイル
)
```

### 3. Shapes

```kotlin
val ExpressiveShapes = Shapes(
    extraSmall = RoundedCornerShape(4.dp),
    small = RoundedCornerShape(8.dp),
    medium = RoundedCornerShape(12.dp),
    large = RoundedCornerShape(16.dp),
    extraLarge = RoundedCornerShape(28.dp)
)
```

### 4. Motion Scheme

```kotlin
// Expressive: バウンス感のあるアニメーション
val expressiveMotion = MotionScheme.expressive()

// Standard: 控えめなアニメーション
val standardMotion = MotionScheme.standard()

// カスタム MotionScheme
val customMotionScheme = MotionScheme(
    defaultSpatialSpec = spring(
        stiffness = Spring.StiffnessMedium,
        dampingRatio = Spring.DampingRatioMediumBouncy
    ),
    fastSpatialSpec = spring(
        stiffness = Spring.StiffnessHigh,
        dampingRatio = Spring.DampingRatioNoBouncy
    ),
    slowSpatialSpec = spring(
        stiffness = Spring.StiffnessLow,
        dampingRatio = Spring.DampingRatioLowBouncy
    ),
    defaultEffectsSpec = spring(
        stiffness = Spring.StiffnessMedium,
        dampingRatio = Spring.DampingRatioNoBouncy
    ),
    fastEffectsSpec = spring(
        stiffness = Spring.StiffnessHigh,
        dampingRatio = Spring.DampingRatioNoBouncy
    ),
    slowEffectsSpec = spring(
        stiffness = Spring.StiffnessLow,
        dampingRatio = Spring.DampingRatioNoBouncy
    )
)
```

## テーマへのアクセス

```kotlin
@Composable
fun ThemedComponent() {
    // カラーへのアクセス
    val backgroundColor = MaterialTheme.colorScheme.background
    val primaryColor = MaterialTheme.colorScheme.primary

    // タイポグラフィへのアクセス
    val titleStyle = MaterialTheme.typography.titleLarge
    val bodyStyle = MaterialTheme.typography.bodyMedium

    // シェイプへのアクセス
    val cardShape = MaterialTheme.shapes.medium

    // MotionScheme へのアクセス
    val motionScheme = LocalMotionScheme.current
    val spatialSpec = motionScheme.defaultSpatialSpec<Float>()
}
```

## ダーク/ライトテーマ対応

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun MyApp(darkTheme: Boolean = isSystemInDarkTheme()) {
    val colorScheme = when {
        Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }
        darkTheme -> darkColorScheme()
        else -> lightColorScheme()
    }

    MaterialExpressiveTheme(
        colorScheme = colorScheme,
        motionScheme = MotionScheme.expressive()
    ) {
        // App content
    }
}
```

## CompositionLocal によるカスタム値の提供

```kotlin
// カスタム CompositionLocal の定義
val LocalCustomSpacing = compositionLocalOf { Spacing() }

data class Spacing(
    val small: Dp = 4.dp,
    val medium: Dp = 8.dp,
    val large: Dp = 16.dp,
    val extraLarge: Dp = 32.dp
)

// テーマでの提供
@Composable
fun MyApp() {
    CompositionLocalProvider(
        LocalCustomSpacing provides Spacing()
    ) {
        MaterialExpressiveTheme {
            // App content
        }
    }
}

// 使用
@Composable
fun SpacedContent() {
    val spacing = LocalCustomSpacing.current
    Column(
        verticalArrangement = Arrangement.spacedBy(spacing.medium)
    ) {
        // Content
    }
}
```

## ベストプラクティス

### 1. テーマの一元管理

```kotlin
// theme/Theme.kt
object AppTheme {
    val colors: ColorScheme
        @Composable
        get() = MaterialTheme.colorScheme

    val typography: Typography
        @Composable
        get() = MaterialTheme.typography

    val shapes: Shapes
        @Composable
        get() = MaterialTheme.shapes

    val motion: MotionScheme
        @Composable
        get() = LocalMotionScheme.current
}
```

### 2. Preview でのテーマ使用

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(name = "Light Mode")
@Preview(name = "Dark Mode", uiMode = Configuration.UI_MODE_NIGHT_YES)
@Composable
private fun ComponentPreview() {
    MaterialExpressiveTheme {
        Surface {
            MyComponent()
        }
    }
}
```

### 3. テーマトークンの活用

```kotlin
// ハードコードを避ける
// Bad
Text(
    text = "Title",
    color = Color(0xFF000000),
    fontSize = 24.sp
)

// Good
Text(
    text = "Title",
    color = MaterialTheme.colorScheme.onSurface,
    style = MaterialTheme.typography.titleLarge
)
```

## 関連リソース

- [Motion System](motion-system.md) - MotionScheme 詳細
- [Color System](color-system.md) - カラートークン
- [Typography](typography.md) - タイポグラフィ設定
- [examples/basic-setup.kt](../examples/basic-setup.kt) - 基本セットアップ例
