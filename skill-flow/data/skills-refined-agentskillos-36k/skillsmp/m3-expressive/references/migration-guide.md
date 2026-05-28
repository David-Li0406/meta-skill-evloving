# Material 3 to Material 3 Expressive Migration Guide

M3 から M3 Expressive への移行ガイド。

## Overview

Material 3 Expressive は Material 3 の拡張であり、
後方互換性を維持しながら新機能を追加しています。
段階的な移行が可能です。

## 移行チェックリスト

### Phase 1: 依存関係の更新

- [ ] `build.gradle.kts` を更新
- [ ] Compose BOM を最新版に更新
- [ ] material3 を alpha 版に更新（Expressive コンポーネント使用時）

```kotlin
// build.gradle.kts
dependencies {
    // BOM を使用（推奨）
    implementation(platform("androidx.compose:compose-bom:2024.12.01"))
    implementation("androidx.compose.material3:material3")

    // または直接指定（Expressive 機能が必要な場合）
    implementation("androidx.compose.material3:material3:1.4.0-alpha15")
}
```

### Phase 2: テーマの更新

- [ ] `MaterialTheme` → `MaterialExpressiveTheme` への移行
- [ ] `MotionScheme` の設定

```kotlin
// Before: Material 3
@Composable
fun MyApp() {
    MaterialTheme(
        colorScheme = colorScheme,
        typography = typography
    ) {
        // Content
    }
}

// After: Material 3 Expressive
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun MyApp() {
    MaterialExpressiveTheme(
        colorScheme = colorScheme,
        typography = typography,
        motionScheme = MotionScheme.expressive()
    ) {
        // Content
    }
}
```

### Phase 3: コンポーネントの更新

- [ ] `@OptIn` アノテーションの追加
- [ ] 新しいコンポーネントへの置き換え（任意）

## コンポーネントマッピング

| M3 Component | M3 Expressive Equivalent | 変更点 |
|--------------|-------------------------|--------|
| `FloatingActionButton` | `VibrantFloatingActionButton` | 視覚的に強調 |
| `CircularProgressIndicator` | `LoadingIndicator` | シェイプモーフィング |
| Custom button groups | `ButtonGroup` | 組み込みサポート |
| Custom toggle buttons | `IconToggleButton` | シェイプモーフィング |
| `BottomAppBar` | `FlexibleBottomAppBar` | より柔軟なレイアウト |
| Manual spring animations | `MotionScheme` | 統一された物理アニメーション |

## 段階的移行戦略

### Strategy 1: 全体移行

すべてのコンポーネントを一度に移行：

```kotlin
// app/build.gradle.kts
@file:OptIn(ExperimentalMaterial3ExpressiveApi::class)

// Theme.kt
MaterialExpressiveTheme { ... }
```

**利点**: 一貫した UX
**欠点**: 大きな変更、テスト範囲が広い

### Strategy 2: 画面単位移行

画面ごとに段階的に移行：

```kotlin
// 新しい画面のみ Expressive を使用
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun NewFeatureScreen() {
    MaterialExpressiveTheme {
        // New expressive content
    }
}

// 既存画面は従来通り
@Composable
fun ExistingScreen() {
    MaterialTheme {
        // Existing content
    }
}
```

**利点**: リスク低減、段階的テスト
**欠点**: 一時的な不整合

### Strategy 3: コンポーネント単位移行

特定のコンポーネントのみ移行：

```kotlin
// ローディングインジケーターのみ移行
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun LoadingState() {
    LoadingIndicator() // 新しいコンポーネント
}

// 他は従来通り
@Composable
fun ActionButton() {
    FloatingActionButton(...) // 従来のコンポーネント
}
```

**利点**: 最小限の変更
**欠点**: 部分的な UX 改善

## アニメーション移行

### Before: Duration-based

```kotlin
// 従来の duration-based アニメーション
val size by animateDpAsState(
    targetValue = if (expanded) 200.dp else 100.dp,
    animationSpec = tween(durationMillis = 300)
)
```

### After: Spring-based

```kotlin
// 新しい spring-based アニメーション
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun SpringAnimation() {
    val motionScheme = LocalMotionScheme.current

    val size by animateDpAsState(
        targetValue = if (expanded) 200.dp else 100.dp,
        animationSpec = motionScheme.defaultSpatialSpec()
    )
}
```

## Breaking Changes

### 1. ExperimentalMaterial3ExpressiveApi

すべての新しい Expressive コンポーネントには OptIn が必要：

```kotlin
// 必須
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
```

### 2. MotionScheme の導入

従来のアニメーションは引き続き動作しますが、
MotionScheme を使用することで一貫性が向上します。

### 3. 新しいコンポーネント API

一部のコンポーネントは新しい API を持っています：

```kotlin
// ButtonGroup の新しい API
ButtonGroup(
    spacing = ButtonGroupDefaults.ConnectedSpacing
) {
    ToggleButton(
        checked = ...,
        onCheckedChange = ...,
        shape = ButtonGroupDefaults.connectedLeadingButtonShape
    ) { ... }
}
```

## 互換性の維持

### 既存コードとの共存

```kotlin
@Composable
fun HybridScreen() {
    // 既存の Material 3 コンポーネントは引き続き動作
    Button(onClick = {}) {
        Text("Standard Button")
    }

    // 新しい Expressive コンポーネントを追加
    @OptIn(ExperimentalMaterial3ExpressiveApi::class)
    LoadingIndicator()
}
```

### テーマの共存

```kotlin
// MaterialExpressiveTheme は MaterialTheme を含む
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
MaterialExpressiveTheme {
    // MaterialTheme.* も使用可能
    val colors = MaterialTheme.colorScheme
    val typography = MaterialTheme.typography
}
```

## テスト戦略

### 1. Visual Regression Testing

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview
@Composable
fun ComponentPreview() {
    MaterialExpressiveTheme {
        MyComponent()
    }
}
```

### 2. Animation Testing

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Test
fun testMotionSchemeAnimation() {
    composeTestRule.setContent {
        MaterialExpressiveTheme {
            AnimatedComponent()
        }
    }

    // アニメーション完了を待機
    composeTestRule.waitForIdle()
}
```

## トラブルシューティング

移行中の問題については [troubleshooting.md](troubleshooting.md) を参照してください。

## 関連リソース

- [Theming](theming.md) - テーマ設定
- [Motion System](motion-system.md) - アニメーション
- [Troubleshooting](troubleshooting.md) - 問題解決
