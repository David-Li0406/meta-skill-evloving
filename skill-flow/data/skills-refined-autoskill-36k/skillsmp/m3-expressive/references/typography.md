# Material 3 Expressive Typography

Variable fonts とダイナミックタイポグラフィの実装ガイド。

## Overview

Material 3 Expressive は Variable fonts を活用し、より豊かで動的なタイポグラフィ表現を実現します。
weight（太さ）や width（幅）などのパラメータを連続的に調整できます。

## Type Scale

### M3 Expressive Type Scale

| Role | Size | Weight | Line Height | 用途 |
|------|------|--------|-------------|------|
| Display Large | 57sp | 400 | 64sp | ヒーローテキスト |
| Display Medium | 45sp | 400 | 52sp | 大見出し |
| Display Small | 36sp | 400 | 44sp | セクションタイトル |
| Headline Large | 32sp | 400 | 40sp | ページタイトル |
| Headline Medium | 28sp | 400 | 36sp | カードタイトル |
| Headline Small | 24sp | 400 | 32sp | サブセクション |
| Title Large | 22sp | 400 | 28sp | リストヘッダー |
| Title Medium | 16sp | 500 | 24sp | コンポーネントタイトル |
| Title Small | 14sp | 500 | 20sp | タブ、ボタン |
| Body Large | 16sp | 400 | 24sp | 本文（大） |
| Body Medium | 14sp | 400 | 20sp | 本文（標準） |
| Body Small | 12sp | 400 | 16sp | 本文（小） |
| Label Large | 14sp | 500 | 20sp | ボタンテキスト |
| Label Medium | 12sp | 500 | 16sp | ナビゲーション |
| Label Small | 11sp | 500 | 16sp | キャプション |

## 基本的な使用法

```kotlin
@Composable
fun TypographyExamples() {
    Column {
        Text(
            text = "Display Large",
            style = MaterialTheme.typography.displayLarge
        )
        Text(
            text = "Headline Medium",
            style = MaterialTheme.typography.headlineMedium
        )
        Text(
            text = "Body text",
            style = MaterialTheme.typography.bodyMedium
        )
        Text(
            text = "Label",
            style = MaterialTheme.typography.labelMedium
        )
    }
}
```

## カスタムタイポグラフィ

### Typography の定義

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
    displaySmall = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 36.sp,
        lineHeight = 44.sp,
        letterSpacing = 0.sp
    ),
    headlineLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 32.sp,
        lineHeight = 40.sp,
        letterSpacing = 0.sp
    ),
    headlineMedium = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 28.sp,
        lineHeight = 36.sp,
        letterSpacing = 0.sp
    ),
    headlineSmall = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 24.sp,
        lineHeight = 32.sp,
        letterSpacing = 0.sp
    ),
    titleLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 22.sp,
        lineHeight = 28.sp,
        letterSpacing = 0.sp
    ),
    titleMedium = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Medium,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.15.sp
    ),
    titleSmall = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Medium,
        fontSize = 14.sp,
        lineHeight = 20.sp,
        letterSpacing = 0.1.sp
    ),
    bodyLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.5.sp
    ),
    bodyMedium = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 14.sp,
        lineHeight = 20.sp,
        letterSpacing = 0.25.sp
    ),
    bodySmall = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 12.sp,
        lineHeight = 16.sp,
        letterSpacing = 0.4.sp
    ),
    labelLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Medium,
        fontSize = 14.sp,
        lineHeight = 20.sp,
        letterSpacing = 0.1.sp
    ),
    labelMedium = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Medium,
        fontSize = 12.sp,
        lineHeight = 16.sp,
        letterSpacing = 0.5.sp
    ),
    labelSmall = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Medium,
        fontSize = 11.sp,
        lineHeight = 16.sp,
        letterSpacing = 0.5.sp
    )
)
```

### テーマへの適用

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun MyApp() {
    MaterialExpressiveTheme(
        typography = ExpressiveTypography
    ) {
        // App content
    }
}
```

## Variable Fonts

### Variable Font の読み込み

```kotlin
// res/font/inter_variable.ttf を使用
val InterVariableFont = FontFamily(
    Font(
        R.font.inter_variable,
        weight = FontWeight.Normal,
        variableFontSettings = FontVariation.Settings(
            FontVariation.weight(400)
        )
    ),
    Font(
        R.font.inter_variable,
        weight = FontWeight.Medium,
        variableFontSettings = FontVariation.Settings(
            FontVariation.weight(500)
        )
    ),
    Font(
        R.font.inter_variable,
        weight = FontWeight.Bold,
        variableFontSettings = FontVariation.Settings(
            FontVariation.weight(700)
        )
    )
)
```

### Variable Font でのカスタム Typography

```kotlin
val VariableFontTypography = Typography(
    displayLarge = TextStyle(
        fontFamily = InterVariableFont,
        fontWeight = FontWeight.Normal,
        fontSize = 57.sp,
        lineHeight = 64.sp
    ),
    // ... 他のスタイル
)
```

## Dynamic Typography

### アニメーション付きテキストサイズ

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun AnimatedTypography() {
    val motionScheme = LocalMotionScheme.current
    var isExpanded by remember { mutableStateOf(false) }

    val fontSize by animateFloatAsState(
        targetValue = if (isExpanded) 32f else 16f,
        animationSpec = motionScheme.defaultSpatialSpec(),
        label = "fontSize"
    )

    Text(
        text = "Animated Text",
        style = MaterialTheme.typography.bodyMedium.copy(
            fontSize = fontSize.sp
        ),
        modifier = Modifier.clickable { isExpanded = !isExpanded }
    )
}
```

### 状態に応じたスタイル変更

```kotlin
@Composable
fun StatefulTypography(isSelected: Boolean) {
    val style = if (isSelected) {
        MaterialTheme.typography.titleMedium.copy(
            fontWeight = FontWeight.Bold
        )
    } else {
        MaterialTheme.typography.bodyMedium
    }

    Text(
        text = "Stateful Text",
        style = style
    )
}
```

## アクセシビリティ

### Dynamic Type 対応

```kotlin
@Composable
fun AccessibleText() {
    // sp 単位を使用することでシステムのフォントスケールに自動対応
    Text(
        text = "This text scales with system settings",
        style = MaterialTheme.typography.bodyLarge
    )
}
```

### 最小タッチサイズの確保

```kotlin
@Composable
fun AccessibleButton() {
    Button(
        onClick = { },
        modifier = Modifier.defaultMinSize(minHeight = 48.dp)
    ) {
        Text(
            text = "Button",
            style = MaterialTheme.typography.labelLarge
        )
    }
}
```

## ベストプラクティス

### 1. 一貫したスタイル使用

```kotlin
// Good: テーマからスタイルを取得
Text(
    text = "Title",
    style = MaterialTheme.typography.titleLarge
)

// Bad: ハードコードされたスタイル
Text(
    text = "Title",
    fontSize = 22.sp,
    fontWeight = FontWeight.Normal
)
```

### 2. 適切なロールの選択

| コンテンツ | 推奨ロール |
|-----------|-----------|
| 画面タイトル | `headlineLarge` / `headlineMedium` |
| セクションタイトル | `titleLarge` / `titleMedium` |
| 本文 | `bodyLarge` / `bodyMedium` |
| ボタン | `labelLarge` |
| キャプション | `labelSmall` / `bodySmall` |

### 3. コントラストの確保

```kotlin
// 適切なコントラスト
Text(
    text = "Primary text",
    color = MaterialTheme.colorScheme.onSurface  // 高コントラスト
)

Text(
    text = "Secondary text",
    color = MaterialTheme.colorScheme.onSurfaceVariant  // やや低コントラスト
)
```

## 関連リソース

- [Color System](color-system.md) - カラートークン
- [Theming](theming.md) - テーマ設定
- [examples/basic-setup.kt](../examples/basic-setup.kt) - 基本設定例
