# Material 3 Expressive Color System

Design tokens とカラーパレットの実装ガイド。

## Overview

Material 3 Expressive は拡張されたカラーシステムを提供し、
より深いトーナルパレットとダイナミックカラーをサポートします。

## Color Roles

### Primary Colors

| Role | 用途 |
|------|------|
| `primary` | 主要アクション、強調要素 |
| `onPrimary` | primary 背景上のコンテンツ |
| `primaryContainer` | 主要要素のコンテナ背景 |
| `onPrimaryContainer` | primaryContainer 上のコンテンツ |

### Secondary Colors

| Role | 用途 |
|------|------|
| `secondary` | 二次的アクション |
| `onSecondary` | secondary 背景上のコンテンツ |
| `secondaryContainer` | 二次要素のコンテナ背景 |
| `onSecondaryContainer` | secondaryContainer 上のコンテンツ |

### Tertiary Colors

| Role | 用途 |
|------|------|
| `tertiary` | 三次的要素、アクセント |
| `onTertiary` | tertiary 背景上のコンテンツ |
| `tertiaryContainer` | 三次要素のコンテナ背景 |
| `onTertiaryContainer` | tertiaryContainer 上のコンテンツ |

### Error Colors

| Role | 用途 |
|------|------|
| `error` | エラー状態 |
| `onError` | error 背景上のコンテンツ |
| `errorContainer` | エラー要素のコンテナ |
| `onErrorContainer` | errorContainer 上のコンテンツ |

### Surface Colors

| Role | 用途 |
|------|------|
| `surface` | カード、シート、メニュー背景 |
| `onSurface` | surface 上のメインコンテンツ |
| `surfaceVariant` | 変形サーフェス（入力フィールドなど） |
| `onSurfaceVariant` | surfaceVariant 上のコンテンツ |
| `surfaceTint` | サーフェスのティント色 |

### Background & Outline

| Role | 用途 |
|------|------|
| `background` | 画面背景 |
| `onBackground` | background 上のコンテンツ |
| `outline` | 境界線、区切り線 |
| `outlineVariant` | 軽い区切り線 |

## 基本的な使用法

```kotlin
@Composable
fun ColorUsageExamples() {
    Column {
        // Primary
        Surface(
            color = MaterialTheme.colorScheme.primaryContainer
        ) {
            Text(
                text = "Primary Container",
                color = MaterialTheme.colorScheme.onPrimaryContainer
            )
        }

        // Secondary
        Surface(
            color = MaterialTheme.colorScheme.secondaryContainer
        ) {
            Text(
                text = "Secondary Container",
                color = MaterialTheme.colorScheme.onSecondaryContainer
            )
        }

        // Error
        Surface(
            color = MaterialTheme.colorScheme.errorContainer
        ) {
            Text(
                text = "Error Message",
                color = MaterialTheme.colorScheme.onErrorContainer
            )
        }
    }
}
```

## Dynamic Color

### Android 12+ Dynamic Color

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun DynamicColorTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context)
            else dynamicLightColorScheme(context)
        }
        darkTheme -> darkColorScheme()
        else -> lightColorScheme()
    }

    MaterialExpressiveTheme(
        colorScheme = colorScheme,
        content = content
    )
}
```

## カスタムカラースキーム

### Light Color Scheme

```kotlin
val CustomLightColorScheme = lightColorScheme(
    primary = Color(0xFF6200EE),
    onPrimary = Color.White,
    primaryContainer = Color(0xFFBB86FC),
    onPrimaryContainer = Color(0xFF3700B3),
    secondary = Color(0xFF03DAC5),
    onSecondary = Color.Black,
    secondaryContainer = Color(0xFFCEFAF8),
    onSecondaryContainer = Color(0xFF00504D),
    tertiary = Color(0xFF7C5800),
    onTertiary = Color.White,
    tertiaryContainer = Color(0xFFFFDEA6),
    onTertiaryContainer = Color(0xFF271900),
    error = Color(0xFFB00020),
    onError = Color.White,
    errorContainer = Color(0xFFFCDAD6),
    onErrorContainer = Color(0xFF410002),
    background = Color(0xFFFFFBFE),
    onBackground = Color(0xFF1C1B1F),
    surface = Color(0xFFFFFBFE),
    onSurface = Color(0xFF1C1B1F),
    surfaceVariant = Color(0xFFE7E0EC),
    onSurfaceVariant = Color(0xFF49454F),
    outline = Color(0xFF79747E),
    outlineVariant = Color(0xFFCAC4D0)
)
```

### Dark Color Scheme

```kotlin
val CustomDarkColorScheme = darkColorScheme(
    primary = Color(0xFFBB86FC),
    onPrimary = Color(0xFF3700B3),
    primaryContainer = Color(0xFF4F00B7),
    onPrimaryContainer = Color(0xFFEADDFF),
    secondary = Color(0xFF03DAC5),
    onSecondary = Color(0xFF00504D),
    secondaryContainer = Color(0xFF005653),
    onSecondaryContainer = Color(0xFF70F7ED),
    tertiary = Color(0xFFF4BF00),
    onTertiary = Color(0xFF3F2E00),
    tertiaryContainer = Color(0xFF5C4300),
    onTertiaryContainer = Color(0xFFFFDEA6),
    error = Color(0xFFCF6679),
    onError = Color(0xFF690005),
    errorContainer = Color(0xFF93000A),
    onErrorContainer = Color(0xFFFFDAD6),
    background = Color(0xFF1C1B1F),
    onBackground = Color(0xFFE6E1E5),
    surface = Color(0xFF1C1B1F),
    onSurface = Color(0xFFE6E1E5),
    surfaceVariant = Color(0xFF49454F),
    onSurfaceVariant = Color(0xFFCAC4D0),
    outline = Color(0xFF938F99),
    outlineVariant = Color(0xFF49454F)
)
```

## Color Tokens の活用

### 状態に応じた色の使用

```kotlin
@Composable
fun StateAwareColors(
    isSelected: Boolean,
    isEnabled: Boolean
) {
    val backgroundColor = when {
        !isEnabled -> MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.38f)
        isSelected -> MaterialTheme.colorScheme.primaryContainer
        else -> MaterialTheme.colorScheme.surface
    }

    val contentColor = when {
        !isEnabled -> MaterialTheme.colorScheme.onSurface.copy(alpha = 0.38f)
        isSelected -> MaterialTheme.colorScheme.onPrimaryContainer
        else -> MaterialTheme.colorScheme.onSurface
    }

    Surface(color = backgroundColor) {
        Text(text = "State-aware content", color = contentColor)
    }
}
```

### アニメーション付き色変更

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun AnimatedColorChange(isActive: Boolean) {
    val motionScheme = LocalMotionScheme.current

    val backgroundColor by animateColorAsState(
        targetValue = if (isActive)
            MaterialTheme.colorScheme.primaryContainer
        else
            MaterialTheme.colorScheme.surface,
        animationSpec = motionScheme.defaultEffectsSpec(),
        label = "backgroundColor"
    )

    Surface(color = backgroundColor) {
        // Content
    }
}
```

## Elevation と Tonal Elevation

```kotlin
@Composable
fun ElevationExamples() {
    Column {
        // Tonal elevation (色の変化で高さを表現)
        Surface(
            tonalElevation = 0.dp,
            modifier = Modifier.padding(8.dp)
        ) {
            Text("0dp elevation")
        }

        Surface(
            tonalElevation = 1.dp,
            modifier = Modifier.padding(8.dp)
        ) {
            Text("1dp elevation")
        }

        Surface(
            tonalElevation = 3.dp,
            modifier = Modifier.padding(8.dp)
        ) {
            Text("3dp elevation")
        }

        Surface(
            tonalElevation = 6.dp,
            modifier = Modifier.padding(8.dp)
        ) {
            Text("6dp elevation")
        }
    }
}
```

## アクセシビリティ

### コントラスト比の確保

```kotlin
// WCAG 2.1 AA: 4.5:1 (通常テキスト), 3:1 (大きなテキスト)
// WCAG 2.1 AAA: 7:1 (通常テキスト), 4.5:1 (大きなテキスト)

@Composable
fun AccessibleColors() {
    // 高コントラスト: メインコンテンツ
    Text(
        text = "Primary content",
        color = MaterialTheme.colorScheme.onSurface  // 高コントラスト
    )

    // 中コントラスト: 二次的コンテンツ
    Text(
        text = "Secondary content",
        color = MaterialTheme.colorScheme.onSurfaceVariant
    )

    // エラー表示
    Text(
        text = "Error message",
        color = MaterialTheme.colorScheme.error
    )
}
```

## ベストプラクティス

### 1. セマンティックカラーの使用

```kotlin
// Good: セマンティックな色
Button(
    colors = ButtonDefaults.buttonColors(
        containerColor = MaterialTheme.colorScheme.primary
    )
) { Text("Primary Action") }

// Bad: ハードコードされた色
Button(
    colors = ButtonDefaults.buttonColors(
        containerColor = Color(0xFF6200EE)
    )
) { Text("Primary Action") }
```

### 2. 適切なペアリング

| 背景 | コンテンツ |
|------|-----------|
| `primary` | `onPrimary` |
| `primaryContainer` | `onPrimaryContainer` |
| `surface` | `onSurface` |
| `error` | `onError` |

### 3. 状態の表現

```kotlin
@Composable
fun StateColors(state: ComponentState) {
    val color = when (state) {
        ComponentState.Default -> MaterialTheme.colorScheme.surface
        ComponentState.Hovered -> MaterialTheme.colorScheme.surfaceVariant
        ComponentState.Focused -> MaterialTheme.colorScheme.primaryContainer
        ComponentState.Pressed -> MaterialTheme.colorScheme.primary
        ComponentState.Disabled -> MaterialTheme.colorScheme.surface.copy(alpha = 0.38f)
    }
}
```

## 関連リソース

- [Typography](typography.md) - タイポグラフィ
- [Theming](theming.md) - テーマ設定
- [Material Theme Builder](https://m3.material.io/theme-builder)
