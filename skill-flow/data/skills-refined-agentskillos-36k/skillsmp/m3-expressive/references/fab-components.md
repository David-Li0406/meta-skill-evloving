# Material 3 Expressive FAB Components

FloatingActionButtonMenu, VibrantFloatingActionButton, ToggleFloatingActionButton の実装ガイド。

## Overview

Material 3 Expressive では、従来の FAB を拡張した新しいコンポーネントが追加されました：

| コンポーネント | 説明 | 用途 |
|--------------|------|------|
| `FloatingActionButtonMenu` | 展開式FABメニュー | 2-6個の関連アクション |
| `ToggleFloatingActionButton` | トグル可能なFAB | メニュー開閉トリガー |
| `VibrantFloatingActionButton` | ビブラントスタイルFAB | 強調されたアクション |

## FloatingActionButtonMenu

### 基本的な使用法

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun BasicFABMenu() {
    var expanded by remember { mutableStateOf(false) }

    FloatingActionButtonMenu(
        expanded = expanded,
        button = {
            ToggleFloatingActionButton(
                checked = expanded,
                onCheckedChange = { expanded = it }
            ) {
                Icon(
                    imageVector = if (expanded) Icons.Default.Close else Icons.Default.Add,
                    contentDescription = if (expanded) "Close menu" else "Open menu"
                )
            }
        }
    ) {
        FloatingActionButtonMenuItem(
            onClick = { /* action */ },
            icon = { Icon(Icons.Default.Edit, contentDescription = null) },
            text = { Text("Edit") }
        )
        FloatingActionButtonMenuItem(
            onClick = { /* action */ },
            icon = { Icon(Icons.Default.Share, contentDescription = null) },
            text = { Text("Share") }
        )
        FloatingActionButtonMenuItem(
            onClick = { /* action */ },
            icon = { Icon(Icons.Default.Delete, contentDescription = null) },
            text = { Text("Delete") }
        )
    }
}
```

### Scaffold との統合

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ScaffoldWithFABMenu() {
    var fabExpanded by remember { mutableStateOf(false) }

    Scaffold(
        floatingActionButton = {
            FloatingActionButtonMenu(
                expanded = fabExpanded,
                button = {
                    ToggleFloatingActionButton(
                        checked = fabExpanded,
                        onCheckedChange = { fabExpanded = it }
                    ) {
                        Icon(
                            imageVector = if (fabExpanded) Icons.Default.Close else Icons.Default.Add,
                            contentDescription = null
                        )
                    }
                }
            ) {
                FloatingActionButtonMenuItem(
                    onClick = {
                        fabExpanded = false
                        // Navigate to create
                    },
                    icon = { Icon(Icons.Default.Create, null) },
                    text = { Text("New") }
                )
                FloatingActionButtonMenuItem(
                    onClick = {
                        fabExpanded = false
                        // Navigate to import
                    },
                    icon = { Icon(Icons.Default.Upload, null) },
                    text = { Text("Import") }
                )
            }
        }
    ) { paddingValues ->
        // Main content
    }
}
```

### メニューアイテムのカスタマイズ

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun CustomFABMenuItems() {
    var expanded by remember { mutableStateOf(false) }

    FloatingActionButtonMenu(
        expanded = expanded,
        button = {
            ToggleFloatingActionButton(
                checked = expanded,
                onCheckedChange = { expanded = it }
            ) {
                Icon(
                    imageVector = if (expanded) Icons.Default.Close else Icons.Default.Add,
                    contentDescription = null
                )
            }
        }
    ) {
        // アイコンのみ（テキストなし）
        FloatingActionButtonMenuItem(
            onClick = { },
            icon = { Icon(Icons.Default.Photo, contentDescription = "Photo") },
            text = { } // 空のテキスト
        )

        // カスタムカラー
        FloatingActionButtonMenuItem(
            onClick = { },
            icon = {
                Icon(
                    Icons.Default.Delete,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.error
                )
            },
            text = {
                Text(
                    "Delete",
                    color = MaterialTheme.colorScheme.error
                )
            }
        )
    }
}
```

## VibrantFloatingActionButton

### 基本的な使用法

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun BasicVibrantFAB() {
    FloatingToolbarDefaults.VibrantFloatingActionButton(
        onClick = { /* action */ }
    ) {
        Icon(
            imageVector = Icons.Default.Add,
            contentDescription = "Add"
        )
    }
}
```

### Floating Toolbar との統合

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ToolbarWithVibrantFAB() {
    var expanded by remember { mutableStateOf(true) }

    HorizontalFloatingToolbar(
        expanded = expanded,
        floatingActionButton = {
            FloatingToolbarDefaults.VibrantFloatingActionButton(
                onClick = { /* primary action */ }
            ) {
                Icon(Icons.Default.Add, contentDescription = "Add")
            }
        },
        colors = FloatingToolbarDefaults.vibrantFloatingToolbarColors()
    ) {
        IconButton(onClick = { }) {
            Icon(Icons.Default.Edit, contentDescription = "Edit")
        }
        IconButton(onClick = { }) {
            Icon(Icons.Default.Share, contentDescription = "Share")
        }
    }
}
```

## ToggleFloatingActionButton

### 基本的な使用法

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun BasicToggleFAB() {
    var isChecked by remember { mutableStateOf(false) }

    ToggleFloatingActionButton(
        checked = isChecked,
        onCheckedChange = { isChecked = it }
    ) {
        Icon(
            imageVector = if (isChecked) Icons.Filled.Bookmark else Icons.Outlined.BookmarkBorder,
            contentDescription = if (isChecked) "Remove bookmark" else "Add bookmark"
        )
    }
}
```

### アニメーション付きアイコン切り替え

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun AnimatedToggleFAB() {
    var isChecked by remember { mutableStateOf(false) }

    ToggleFloatingActionButton(
        checked = isChecked,
        onCheckedChange = { isChecked = it }
    ) {
        // AnimatedContent でアイコンをアニメーション
        AnimatedContent(
            targetState = isChecked,
            transitionSpec = {
                fadeIn(animationSpec = tween(200)) togetherWith
                fadeOut(animationSpec = tween(200))
            },
            label = "FAB icon"
        ) { checked ->
            Icon(
                imageVector = if (checked) Icons.Default.Close else Icons.Default.Add,
                contentDescription = null
            )
        }
    }
}
```

## FAB サイズバリエーション

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun FABSizeVariations() {
    Row(
        horizontalArrangement = Arrangement.spacedBy(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Small FAB
        SmallFloatingActionButton(
            onClick = { }
        ) {
            Icon(Icons.Default.Add, contentDescription = "Add")
        }

        // Standard FAB
        FloatingActionButton(
            onClick = { }
        ) {
            Icon(Icons.Default.Add, contentDescription = "Add")
        }

        // Large FAB
        LargeFloatingActionButton(
            onClick = { }
        ) {
            Icon(
                Icons.Default.Add,
                contentDescription = "Add",
                modifier = Modifier.size(36.dp)
            )
        }

        // Extended FAB
        ExtendedFloatingActionButton(
            onClick = { },
            icon = { Icon(Icons.Default.Add, contentDescription = null) },
            text = { Text("Create") }
        )
    }
}
```

## 配置パターン

### 右下配置（標準）

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun StandardFABPlacement() {
    Scaffold(
        floatingActionButton = {
            FloatingActionButton(onClick = { }) {
                Icon(Icons.Default.Add, contentDescription = "Add")
            }
        },
        floatingActionButtonPosition = FabPosition.End
    ) { paddingValues ->
        // Content
    }
}
```

### 中央配置

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun CenterFABPlacement() {
    Scaffold(
        floatingActionButton = {
            FloatingActionButton(onClick = { }) {
                Icon(Icons.Default.Add, contentDescription = "Add")
            }
        },
        floatingActionButtonPosition = FabPosition.Center
    ) { paddingValues ->
        // Content
    }
}
```

## 状態管理パターン

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun FABWithState(
    viewModel: MyViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    var fabExpanded by remember { mutableStateOf(false) }

    FloatingActionButtonMenu(
        expanded = fabExpanded,
        button = {
            ToggleFloatingActionButton(
                checked = fabExpanded,
                onCheckedChange = { fabExpanded = it },
                // 処理中は無効化
                enabled = !uiState.isProcessing
            ) {
                if (uiState.isProcessing) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(24.dp),
                        strokeWidth = 2.dp
                    )
                } else {
                    Icon(
                        imageVector = if (fabExpanded) Icons.Default.Close else Icons.Default.Add,
                        contentDescription = null
                    )
                }
            }
        }
    ) {
        // Menu items
    }
}
```

## アクセシビリティ

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun AccessibleFABMenu() {
    var expanded by remember { mutableStateOf(false) }

    FloatingActionButtonMenu(
        expanded = expanded,
        modifier = Modifier.semantics {
            contentDescription = "Action menu"
            stateDescription = if (expanded) "Expanded" else "Collapsed"
        },
        button = {
            ToggleFloatingActionButton(
                checked = expanded,
                onCheckedChange = { expanded = it },
                modifier = Modifier.semantics {
                    role = Role.Button
                    contentDescription = if (expanded) "Close action menu" else "Open action menu"
                }
            ) {
                Icon(
                    imageVector = if (expanded) Icons.Default.Close else Icons.Default.Add,
                    contentDescription = null // 親で設定済み
                )
            }
        }
    ) {
        FloatingActionButtonMenuItem(
            onClick = { },
            icon = { Icon(Icons.Default.Edit, contentDescription = null) },
            text = { Text("Edit item") }
        )
    }
}
```

## ベストプラクティス

### 1. メニューアイテム数

- **推奨**: 2-6個のアクション
- 1個の場合: 通常の FAB を使用
- 6個以上: BottomSheet や NavigationDrawer を検討

### 2. アイコン + テキストの使用

```kotlin
// Good: アイコンとテキストの両方
FloatingActionButtonMenuItem(
    onClick = { },
    icon = { Icon(Icons.Default.Share, null) },
    text = { Text("Share") }
)

// シンプルなアクションはアイコンのみでもOK
FloatingActionButtonMenuItem(
    onClick = { },
    icon = { Icon(Icons.Default.ContentCopy, "Copy") },
    text = { }
)
```

### 3. 適切なフィードバック

```kotlin
// メニュー選択後にメニューを閉じる
FloatingActionButtonMenuItem(
    onClick = {
        expanded = false  // メニューを閉じる
        performAction()   // アクション実行
    },
    icon = { Icon(Icons.Default.Edit, null) },
    text = { Text("Edit") }
)
```

## 関連リソース

- [Floating Toolbar](floating-toolbar.md) - ツールバーとの組み合わせ
- [Motion System](motion-system.md) - アニメーション
- [examples/fab-menu-example.kt](../examples/fab-menu-example.kt) - 実装例
