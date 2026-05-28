# Material 3 Expressive Motion System

Spring Physics に基づく新しいアニメーションシステムの詳細ガイド。

## Overview

M3 Expressive は従来の duration-based アニメーションから physics-based (Spring) アニメーションへ移行しました。
これにより、より自然で流動的、かつ中断可能なアニメーションが実現されます。

## Spring Physics 基礎

### 主要パラメータ

| パラメータ | 説明 | 値の範囲 |
|-----------|------|---------|
| **Stiffness** | バネの硬さ。高いほど速く収束 | `StiffnessVeryLow` → `StiffnessHigh` |
| **Damping Ratio** | 減衰率。オーバーシュート量を制御 | 0.0 → 1.0+ |

### Damping Ratio の影響

| 値 | 動作 | 定数 |
|----|------|------|
| < 1.0 | Under-damped（オーバーシュートあり、バウンス） | `DampingRatioHighBouncy`, `DampingRatioMediumBouncy`, `DampingRatioLowBouncy` |
| = 1.0 | Critically damped（オーバーシュートなし、最速収束） | `DampingRatioNoBouncy` |
| > 1.0 | Over-damped（オーバーシュートなし、ゆっくり収束） | - |

### Spring 定数一覧

```kotlin
// Stiffness
Spring.StiffnessHigh        // 10000f - 非常に硬い
Spring.StiffnessMediumHigh  // 5000f
Spring.StiffnessMedium      // 1500f - 標準
Spring.StiffnessMediumLow   // 400f
Spring.StiffnessLow         // 200f
Spring.StiffnessVeryLow     // 50f - 非常に柔らかい

// Damping Ratio
Spring.DampingRatioHighBouncy   // 0.2f - 強いバウンス
Spring.DampingRatioMediumBouncy // 0.5f - 中程度のバウンス
Spring.DampingRatioLowBouncy    // 0.75f - 軽いバウンス
Spring.DampingRatioNoBouncy     // 1.0f - バウンスなし
```

## MotionScheme

### 組み込みスキーム

```kotlin
// Expressive Scheme
// - 低い damping（バウンスあり）
// - ヒーローモーメント、主要インタラクション向け
val expressiveMotion = MotionScheme.expressive()

// Standard Scheme
// - 高い damping（バウンス最小）
// - ユーティリティアプリ、控えめなUI向け
val standardMotion = MotionScheme.standard()
```

### Scheme の適用

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ThemedApp() {
    MaterialExpressiveTheme(
        motionScheme = MotionScheme.expressive()
    ) {
        // すべてのコンポーネントがこの MotionScheme を使用
    }
}
```

## Spatial vs Effects Specs

### Spatial Specs（空間用）

**用途**: サイズ、位置、形状の変更

| Spec | 用途 | 例 |
|------|------|-----|
| `fastSpatialSpec` | 小さなコンポーネント | Switch, Checkbox, RadioButton |
| `defaultSpatialSpec` | 中間サイズ | Button, Card, TextField |
| `slowSpatialSpec` | 大きな要素、画面遷移 | Dialog, BottomSheet, Navigation |

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun SpatialAnimationExample() {
    val motionScheme = LocalMotionScheme.current
    var expanded by remember { mutableStateOf(false) }

    val size by animateDpAsState(
        targetValue = if (expanded) 200.dp else 100.dp,
        animationSpec = motionScheme.defaultSpatialSpec()
    )

    Box(
        modifier = Modifier
            .size(size)
            .background(MaterialTheme.colorScheme.primary)
            .clickable { expanded = !expanded }
    )
}
```

### Effects Specs（エフェクト用）

**用途**: 色、透明度、エフェクトの変更

| Spec | 用途 | 例 |
|------|------|-----|
| `fastEffectsSpec` | 即座のフィードバック | ホバー、フォーカス状態 |
| `defaultEffectsSpec` | 標準的な色変更 | 選択状態、有効/無効 |
| `slowEffectsSpec` | 緩やかな変化 | テーマ切り替え、背景色 |

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun EffectsAnimationExample() {
    val motionScheme = LocalMotionScheme.current
    var isSelected by remember { mutableStateOf(false) }

    val backgroundColor by animateColorAsState(
        targetValue = if (isSelected)
            MaterialTheme.colorScheme.primaryContainer
        else
            MaterialTheme.colorScheme.surface,
        animationSpec = motionScheme.defaultEffectsSpec()
    )

    Surface(
        color = backgroundColor,
        modifier = Modifier.clickable { isSelected = !isSelected }
    ) {
        Text("Select me")
    }
}
```

## カスタム Spring の作成

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
fun customSpring(): SpringSpec<Float> = spring(
    stiffness = Spring.StiffnessMedium,
    dampingRatio = Spring.DampingRatioMediumBouncy,
    visibilityThreshold = 0.1f
)

// 使用例
val offset by animateFloatAsState(
    targetValue = if (expanded) 100f else 0f,
    animationSpec = customSpring()
)
```

## カスタム MotionScheme

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
val CustomMotionScheme = MotionScheme(
    defaultSpatialSpec = spring(
        stiffness = Spring.StiffnessMedium,
        dampingRatio = 0.6f  // 少しバウンス
    ),
    fastSpatialSpec = spring(
        stiffness = Spring.StiffnessHigh,
        dampingRatio = Spring.DampingRatioNoBouncy
    ),
    slowSpatialSpec = spring(
        stiffness = Spring.StiffnessLow,
        dampingRatio = 0.7f
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

## 中断可能なアニメーション

Spring アニメーションの大きな利点は中断可能性です：

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun InterruptibleAnimation() {
    val motionScheme = LocalMotionScheme.current
    var targetPosition by remember { mutableStateOf(0f) }

    val position by animateFloatAsState(
        targetValue = targetPosition,
        animationSpec = motionScheme.defaultSpatialSpec()
    )

    Box(
        modifier = Modifier
            .offset { IntOffset(position.roundToInt(), 0) }
            .pointerInput(Unit) {
                detectDragGestures { change, dragAmount ->
                    change.consume()
                    // ドラッグ中でも新しいターゲットに即座に対応
                    targetPosition += dragAmount.x
                }
            }
    )
}
```

## アニメーション選択ガイドライン

### いつ Spatial を使うか

- サイズ変更（展開/折りたたみ）
- 位置移動（スライド、ドラッグ）
- 形状変更（モーフィング）
- 回転、スケール

### いつ Effects を使うか

- 背景色の変更
- 透明度（フェードイン/アウト）
- ボーダー色
- テキスト色

### Speed の選択

| コンポーネントサイズ | 推奨 Speed |
|-------------------|-----------|
| 小（< 48dp） | `fast` |
| 中（48dp - 200dp） | `default` |
| 大（> 200dp / 画面遷移） | `slow` |

## Reduce Motion 対応

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun AccessibleAnimation() {
    val reduceMotion = LocalReduceMotion.current

    val motionScheme = if (reduceMotion) {
        // モーション軽減時は instant または standard を使用
        MotionScheme.standard()
    } else {
        MotionScheme.expressive()
    }

    MaterialExpressiveTheme(motionScheme = motionScheme) {
        // Content
    }
}
```

## 関連リソース

- [Theming](theming.md) - MaterialExpressiveTheme 設定
- [Shape Library](shape-library.md) - シェイプモーフィング
- [examples/motion-scheme-examples.kt](../examples/motion-scheme-examples.kt) - 実装例
- [M3 Expressive Motion Blog](https://m3.material.io/blog/m3-expressive-motion-theming)
