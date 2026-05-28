# Material 3 Expressive ButtonGroup

ButtonGroup コンポーネントの実装ガイド。

## Overview

ButtonGroup は複数のボタンを論理的にグループ化し、
接続されたまたは分離されたスタイルで表示するコンポーネントです。
セグメントコントロールやツールバーアクションに最適です。

## 基本的な使用法

### Standard ButtonGroup

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun StandardButtonGroupExample() {
    var selectedIndex by remember { mutableIntStateOf(0) }

    ButtonGroup {
        ToggleButton(
            checked = selectedIndex == 0,
            onCheckedChange = { if (it) selectedIndex = 0 }
        ) {
            Text("Option 1")
        }
        ToggleButton(
            checked = selectedIndex == 1,
            onCheckedChange = { if (it) selectedIndex = 1 }
        ) {
            Text("Option 2")
        }
        ToggleButton(
            checked = selectedIndex == 2,
            onCheckedChange = { if (it) selectedIndex = 2 }
        ) {
            Text("Option 3")
        }
    }
}
```

### Connected ButtonGroup

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ConnectedButtonGroupExample() {
    var selectedIndex by remember { mutableIntStateOf(0) }

    ButtonGroup(
        // Connected スタイル: ボタン間の間隔なし
        spacing = ButtonGroupDefaults.ConnectedSpacing
    ) {
        ToggleButton(
            checked = selectedIndex == 0,
            onCheckedChange = { if (it) selectedIndex = 0 },
            shape = ButtonGroupDefaults.connectedLeadingButtonShape
        ) {
            Icon(Icons.Default.FormatAlignLeft, contentDescription = "Left align")
        }
        ToggleButton(
            checked = selectedIndex == 1,
            onCheckedChange = { if (it) selectedIndex = 1 },
            shape = ButtonGroupDefaults.connectedMiddleButtonShape
        ) {
            Icon(Icons.Default.FormatAlignCenter, contentDescription = "Center align")
        }
        ToggleButton(
            checked = selectedIndex == 2,
            onCheckedChange = { if (it) selectedIndex = 2 },
            shape = ButtonGroupDefaults.connectedTrailingButtonShape
        ) {
            Icon(Icons.Default.FormatAlignRight, contentDescription = "Right align")
        }
    }
}
```

## アイコン付き ButtonGroup

### アイコンのみ

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun IconOnlyButtonGroup() {
    var selectedIndex by remember { mutableIntStateOf(0) }
    val icons = listOf(
        Icons.Default.FormatBold,
        Icons.Default.FormatItalic,
        Icons.Default.FormatUnderlined
    )

    ButtonGroup {
        icons.forEachIndexed { index, icon ->
            ToggleButton(
                checked = selectedIndex == index,
                onCheckedChange = { if (it) selectedIndex = index }
            ) {
                Icon(icon, contentDescription = null)
            }
        }
    }
}
```

### アイコン + テキスト

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun IconTextButtonGroup() {
    var selectedIndex by remember { mutableIntStateOf(0) }
    val options = listOf(
        Icons.Default.List to "List",
        Icons.Default.GridView to "Grid",
        Icons.Default.ViewModule to "Module"
    )

    ButtonGroup {
        options.forEachIndexed { index, (icon, label) ->
            ToggleButton(
                checked = selectedIndex == index,
                onCheckedChange = { if (it) selectedIndex = index }
            ) {
                Icon(icon, contentDescription = null)
                Spacer(modifier = Modifier.width(8.dp))
                Text(label)
            }
        }
    }
}
```

## 複数選択 ButtonGroup

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun MultiSelectButtonGroup() {
    var selectedOptions by remember { mutableStateOf(setOf<Int>()) }
    val options = listOf("Bold", "Italic", "Underline")

    ButtonGroup {
        options.forEachIndexed { index, label ->
            ToggleButton(
                checked = selectedOptions.contains(index),
                onCheckedChange = { checked ->
                    selectedOptions = if (checked) {
                        selectedOptions + index
                    } else {
                        selectedOptions - index
                    }
                }
            ) {
                Text(label)
            }
        }
    }
}
```

## カスタマイズ

### 色のカスタマイズ

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ColoredButtonGroup() {
    var selectedIndex by remember { mutableIntStateOf(0) }

    ButtonGroup {
        ToggleButton(
            checked = selectedIndex == 0,
            onCheckedChange = { if (it) selectedIndex = 0 },
            colors = ToggleButtonDefaults.toggleButtonColors(
                checkedContainerColor = MaterialTheme.colorScheme.primaryContainer,
                checkedContentColor = MaterialTheme.colorScheme.onPrimaryContainer,
                containerColor = MaterialTheme.colorScheme.surface,
                contentColor = MaterialTheme.colorScheme.onSurface
            )
        ) {
            Text("Primary")
        }
        ToggleButton(
            checked = selectedIndex == 1,
            onCheckedChange = { if (it) selectedIndex = 1 },
            colors = ToggleButtonDefaults.toggleButtonColors(
                checkedContainerColor = MaterialTheme.colorScheme.secondaryContainer,
                checkedContentColor = MaterialTheme.colorScheme.onSecondaryContainer
            )
        ) {
            Text("Secondary")
        }
    }
}
```

### シェイプのカスタマイズ

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ShapedButtonGroup() {
    var selectedIndex by remember { mutableIntStateOf(0) }

    ButtonGroup {
        ToggleButton(
            checked = selectedIndex == 0,
            onCheckedChange = { if (it) selectedIndex = 0 },
            shape = RoundedCornerShape(
                topStart = 16.dp,
                bottomStart = 16.dp,
                topEnd = 4.dp,
                bottomEnd = 4.dp
            )
        ) {
            Text("First")
        }
        ToggleButton(
            checked = selectedIndex == 1,
            onCheckedChange = { if (it) selectedIndex = 1 },
            shape = RoundedCornerShape(4.dp)
        ) {
            Text("Middle")
        }
        ToggleButton(
            checked = selectedIndex == 2,
            onCheckedChange = { if (it) selectedIndex = 2 },
            shape = RoundedCornerShape(
                topStart = 4.dp,
                bottomStart = 4.dp,
                topEnd = 16.dp,
                bottomEnd = 16.dp
            )
        ) {
            Text("Last")
        }
    }
}
```

## 使用パターン

### ビュー切り替え

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ViewSwitcher() {
    var viewType by remember { mutableStateOf(ViewType.List) }

    ButtonGroup(
        modifier = Modifier.fillMaxWidth(),
        spacing = ButtonGroupDefaults.ConnectedSpacing
    ) {
        ViewType.entries.forEachIndexed { index, type ->
            val shape = when (index) {
                0 -> ButtonGroupDefaults.connectedLeadingButtonShape
                ViewType.entries.lastIndex -> ButtonGroupDefaults.connectedTrailingButtonShape
                else -> ButtonGroupDefaults.connectedMiddleButtonShape
            }

            ToggleButton(
                checked = viewType == type,
                onCheckedChange = { if (it) viewType = type },
                shape = shape,
                modifier = Modifier.weight(1f)
            ) {
                Icon(type.icon, contentDescription = type.label)
                Spacer(modifier = Modifier.width(4.dp))
                Text(type.label)
            }
        }
    }
}

enum class ViewType(val icon: ImageVector, val label: String) {
    List(Icons.Default.List, "List"),
    Grid(Icons.Default.GridView, "Grid"),
    Card(Icons.Default.ViewModule, "Cards")
}
```

### テキストフォーマットツールバー

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun TextFormatToolbar() {
    var isBold by remember { mutableStateOf(false) }
    var isItalic by remember { mutableStateOf(false) }
    var isUnderline by remember { mutableStateOf(false) }

    Row(
        horizontalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // フォーマット切り替え（複数選択可能）
        ButtonGroup(spacing = ButtonGroupDefaults.ConnectedSpacing) {
            ToggleButton(
                checked = isBold,
                onCheckedChange = { isBold = it },
                shape = ButtonGroupDefaults.connectedLeadingButtonShape
            ) {
                Icon(Icons.Default.FormatBold, contentDescription = "Bold")
            }
            ToggleButton(
                checked = isItalic,
                onCheckedChange = { isItalic = it },
                shape = ButtonGroupDefaults.connectedMiddleButtonShape
            ) {
                Icon(Icons.Default.FormatItalic, contentDescription = "Italic")
            }
            ToggleButton(
                checked = isUnderline,
                onCheckedChange = { isUnderline = it },
                shape = ButtonGroupDefaults.connectedTrailingButtonShape
            ) {
                Icon(Icons.Default.FormatUnderlined, contentDescription = "Underline")
            }
        }

        // アライメント（単一選択）
        var alignment by remember { mutableIntStateOf(0) }
        ButtonGroup(spacing = ButtonGroupDefaults.ConnectedSpacing) {
            ToggleButton(
                checked = alignment == 0,
                onCheckedChange = { if (it) alignment = 0 },
                shape = ButtonGroupDefaults.connectedLeadingButtonShape
            ) {
                Icon(Icons.Default.FormatAlignLeft, contentDescription = "Left")
            }
            ToggleButton(
                checked = alignment == 1,
                onCheckedChange = { if (it) alignment = 1 },
                shape = ButtonGroupDefaults.connectedMiddleButtonShape
            ) {
                Icon(Icons.Default.FormatAlignCenter, contentDescription = "Center")
            }
            ToggleButton(
                checked = alignment == 2,
                onCheckedChange = { if (it) alignment = 2 },
                shape = ButtonGroupDefaults.connectedTrailingButtonShape
            ) {
                Icon(Icons.Default.FormatAlignRight, contentDescription = "Right")
            }
        }
    }
}
```

## アクセシビリティ

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun AccessibleButtonGroup() {
    var selectedIndex by remember { mutableIntStateOf(0) }
    val options = listOf("Daily", "Weekly", "Monthly")

    ButtonGroup(
        modifier = Modifier.semantics {
            // グループ全体の説明
            contentDescription = "View frequency selection"
        }
    ) {
        options.forEachIndexed { index, label ->
            ToggleButton(
                checked = selectedIndex == index,
                onCheckedChange = { if (it) selectedIndex = index },
                modifier = Modifier.semantics {
                    // 各ボタンの状態を明示
                    stateDescription = if (selectedIndex == index) "Selected" else "Not selected"
                }
            ) {
                Text(label)
            }
        }
    }
}
```

## ベストプラクティス

### 1. 選択肢の数

- **推奨**: 2-5個の選択肢
- **最大**: 視認性を保つため5個以下を推奨
- 多い場合は DropdownMenu や BottomSheet を検討

### 2. ラベルの長さ

- 短く簡潔に（1-2語）
- 均等な長さが望ましい

### 3. 一貫性

```kotlin
// Good: 統一されたスタイル
ButtonGroup {
    ToggleButton(...) { Text("Option A") }
    ToggleButton(...) { Text("Option B") }
    ToggleButton(...) { Text("Option C") }
}

// Bad: 不統一なスタイル
ButtonGroup {
    ToggleButton(...) { Text("A") }
    ToggleButton(...) { Icon(...) }
    ToggleButton(...) { Text("Very Long Option") }
}
```

## 関連リソース

- [Shape Library](shape-library.md) - シェイプカスタマイズ
- [Motion System](motion-system.md) - アニメーション
- [examples/button-group-example.kt](../examples/button-group-example.kt) - 実装例
