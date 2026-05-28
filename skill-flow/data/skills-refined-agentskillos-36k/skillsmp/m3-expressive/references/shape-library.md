# Material 3 Expressive Shape Library

35種類の新しいシェイプとモーフィングトランジションのガイド。

## Overview

Material 3 Expressive は丸角長方形を超えた35種類の多様なシェイプを提供します。
これらのシェイプはコンポーネント間でスムーズにモーフィング（変形）でき、
状態変化を視覚的に伝えることができます。

## MaterialShapes 一覧

### 基本シェイプ

| シェイプ | 説明 | 用途 |
|---------|------|------|
| `Circle` | 完全な円 | アバター、FAB |
| `Square` | 正方形（角なし） | タイル、グリッドアイテム |
| `RoundedSquare` | 角丸正方形 | カード、ボタン |

### 多角形シェイプ

| シェイプ | 説明 | 用途 |
|---------|------|------|
| `Hexagon` | 六角形 | バッジ、ステータスアイコン |
| `Pentagon` | 五角形 | 特殊なアクション |
| `Octagon` | 八角形 | ストップサイン風UI |
| `Diamond` | ひし形 | ハイライト、選択状態 |

### Cookie シェイプ（不規則な多角形）

| シェイプ | 説明 |
|---------|------|
| `Cookie4Sided` | 4辺の不規則シェイプ |
| `Cookie6Sided` | 6辺の不規則シェイプ |
| `Cookie7Sided` | 7辺の不規則シェイプ |
| `Cookie9Sided` | 9辺の不規則シェイプ |
| `Cookie12Sided` | 12辺の不規則シェイプ |

### Clover シェイプ（葉形）

| シェイプ | 説明 |
|---------|------|
| `Clover4Leaf` | 4枚葉のクローバー |
| `Clover8Leaf` | 8枚葉のクローバー |

### Pill シェイプ

| シェイプ | 説明 | 用途 |
|---------|------|------|
| `Pill` | カプセル形 | チップ、タグ |
| `SemiCircle` | 半円 | プログレス、メーター |

### 星形シェイプ

| シェイプ | 説明 |
|---------|------|
| `Star4Point` | 4点の星 |
| `Star6Point` | 6点の星 |
| `Star8Point` | 8点の星 |
| `Star12Point` | 12点の星 |

## 基本的な使用法

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ShapeExamples() {
    // IconButton with custom shape
    IconButton(
        onClick = { },
        shape = MaterialShapes.Cookie9Sided
    ) {
        Icon(Icons.Default.Favorite, contentDescription = null)
    }

    // Surface with shape
    Surface(
        shape = MaterialShapes.Hexagon,
        color = MaterialTheme.colorScheme.primaryContainer
    ) {
        Text("Hexagon")
    }

    // Card with shape
    Card(
        shape = MaterialShapes.RoundedSquare
    ) {
        // Content
    }
}
```

## Shape Morphing

### 押下時のモーフィング

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun MorphingIconButton() {
    IconButton(
        onClick = { },
        // IconButton は自動的に押下時にシェイプをモーフィング
    ) {
        Icon(Icons.Default.Add, contentDescription = "Add")
    }
}
```

### チェック状態でのモーフィング

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun MorphingToggleButton() {
    var isChecked by remember { mutableStateOf(false) }

    IconToggleButton(
        checked = isChecked,
        onCheckedChange = { isChecked = it }
        // チェック時に自動的にシェイプが変化
    ) {
        Icon(
            imageVector = if (isChecked) Icons.Filled.Favorite else Icons.Outlined.FavoriteBorder,
            contentDescription = null
        )
    }
}
```

### カスタムモーフィングアニメーション

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun CustomShapeMorphing() {
    var isExpanded by remember { mutableStateOf(false) }
    val motionScheme = LocalMotionScheme.current

    // シェイプをアニメーション
    val shape by animateValueAsState(
        targetValue = if (isExpanded) MaterialShapes.Circle else MaterialShapes.Square,
        typeConverter = ShapeTypeConverter(),
        animationSpec = motionScheme.defaultSpatialSpec()
    )

    Surface(
        shape = shape,
        modifier = Modifier
            .size(100.dp)
            .clickable { isExpanded = !isExpanded }
    ) {
        // Content
    }
}
```

## Shared Element Transitions との統合

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class, ExperimentalSharedTransitionApi::class)
@Composable
fun SharedElementWithMorphing(
    sharedTransitionScope: SharedTransitionScope,
    animatedVisibilityScope: AnimatedVisibilityScope
) {
    with(sharedTransitionScope) {
        Surface(
            modifier = Modifier
                .sharedElement(
                    state = rememberSharedContentState(key = "item"),
                    animatedVisibilityScope = animatedVisibilityScope
                ),
            shape = MaterialShapes.Cookie9Sided
        ) {
            // Content
        }
    }
}
```

## 対応コンポーネント

以下のコンポーネントはシェイプモーフィングをサポートしています：

| コンポーネント | 押下時モーフィング | チェック時モーフィング |
|--------------|------------------|---------------------|
| `IconButton` | ✅ | - |
| `IconToggleButton` | ✅ | ✅ |
| `TextButton` | ✅ | - |
| `TextToggleButton` | ✅ | ✅ |
| `FilledIconButton` | ✅ | - |
| `FilledIconToggleButton` | ✅ | ✅ |
| `OutlinedIconButton` | ✅ | - |
| `OutlinedIconToggleButton` | ✅ | ✅ |
| `SplitButton` | ✅ | - |
| `ButtonGroup` | ✅ | ✅ |

## シェイプの選択ガイドライン

### コンテキスト別推奨シェイプ

| コンテキスト | 推奨シェイプ |
|-------------|-------------|
| ユーザーアバター | `Circle` |
| プライマリアクション | `RoundedSquare`, `Pill` |
| 装飾的要素 | `Cookie*`, `Star*` |
| ステータス表示 | `Hexagon`, `Diamond` |
| セカンダリアクション | `Square`, `Pentagon` |

### 状態による使い分け

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun StateBasedShape(isActive: Boolean) {
    val shape = if (isActive) {
        MaterialShapes.Circle  // アクティブ: 柔らかい印象
    } else {
        MaterialShapes.Square  // 非アクティブ: シャープな印象
    }

    Surface(shape = shape) {
        // Content
    }
}
```

## ベストプラクティス

### 1. 一貫性を保つ

同じ種類のコンポーネントには同じシェイプを使用：

```kotlin
// Good: 一貫したシェイプ
val actionButtonShape = MaterialShapes.RoundedSquare

Button(shape = actionButtonShape) { Text("Save") }
Button(shape = actionButtonShape) { Text("Cancel") }

// Bad: 不一致なシェイプ
Button(shape = MaterialShapes.Circle) { Text("Save") }
Button(shape = MaterialShapes.Hexagon) { Text("Cancel") }
```

### 2. 意味のあるモーフィング

状態変化と関連するシェイプ変化を使用：

```kotlin
// 選択状態: 丸みを増す
// 未選択: Circle, 選択: Cookie9Sided
IconToggleButton(checked = selected, onCheckedChange = { selected = it }) {
    // 自動的にシェイプがモーフィング
}
```

### 3. アクセシビリティ

シェイプだけでなく、色やアイコンでも状態を伝える：

```kotlin
IconToggleButton(
    checked = isChecked,
    onCheckedChange = { isChecked = it }
) {
    Icon(
        imageVector = if (isChecked) Icons.Filled.Check else Icons.Outlined.Add,
        contentDescription = if (isChecked) "Selected" else "Not selected"
    )
}
```

## 関連リソース

- [Motion System](motion-system.md) - アニメーション設定
- [Theming](theming.md) - Shapes カスタマイズ
- [examples/shape-morphing-button.kt](../examples/shape-morphing-button.kt) - 実装例
