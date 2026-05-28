# Material 3 Expressive Floating Toolbar

HorizontalFloatingToolbar, VerticalFloatingToolbar, FlexibleBottomAppBar の実装ガイド。

## Overview

Floating Toolbar は画面上に浮かぶツールバーで、
コンテキストに応じたアクションを提供します。

| コンポーネント | 説明 | 用途 |
|--------------|------|------|
| `HorizontalFloatingToolbar` | 水平方向のフローティングツールバー | 画面下部のアクションバー |
| `VerticalFloatingToolbar` | 垂直方向のフローティングツールバー | サイドアクション |
| `FlexibleBottomAppBar` | 柔軟なボトムアプリバー | 適応型レイアウト |

## HorizontalFloatingToolbar

### 基本的な使用法

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun BasicHorizontalToolbar() {
    var expanded by remember { mutableStateOf(true) }

    HorizontalFloatingToolbar(
        expanded = expanded,
        floatingActionButton = {
            FloatingActionButton(
                onClick = { /* primary action */ }
            ) {
                Icon(Icons.Default.Add, contentDescription = "Add")
            }
        }
    ) {
        IconButton(onClick = { }) {
            Icon(Icons.Default.Edit, contentDescription = "Edit")
        }
        IconButton(onClick = { }) {
            Icon(Icons.Default.Share, contentDescription = "Share")
        }
        IconButton(onClick = { }) {
            Icon(Icons.Default.Delete, contentDescription = "Delete")
        }
    }
}
```

### Vibrant スタイル

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun VibrantHorizontalToolbar() {
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

### Scaffold 統合

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ScaffoldWithFloatingToolbar() {
    var toolbarExpanded by remember { mutableStateOf(true) }

    Scaffold(
        floatingActionButton = {
            HorizontalFloatingToolbar(
                expanded = toolbarExpanded,
                floatingActionButton = {
                    FloatingToolbarDefaults.VibrantFloatingActionButton(
                        onClick = { }
                    ) {
                        Icon(Icons.Default.Add, contentDescription = "Add")
                    }
                }
            ) {
                IconButton(onClick = { }) {
                    Icon(Icons.Default.Edit, contentDescription = "Edit")
                }
                IconButton(onClick = { }) {
                    Icon(Icons.Default.Delete, contentDescription = "Delete")
                }
            }
        },
        floatingActionButtonPosition = FabPosition.Center
    ) { paddingValues ->
        // Content
    }
}
```

## VerticalFloatingToolbar

### 基本的な使用法

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun BasicVerticalToolbar() {
    var expanded by remember { mutableStateOf(true) }

    VerticalFloatingToolbar(
        expanded = expanded,
        floatingActionButton = {
            FloatingActionButton(
                onClick = { /* primary action */ }
            ) {
                Icon(Icons.Default.Add, contentDescription = "Add")
            }
        }
    ) {
        IconButton(onClick = { }) {
            Icon(Icons.Default.Edit, contentDescription = "Edit")
        }
        IconButton(onClick = { }) {
            Icon(Icons.Default.Share, contentDescription = "Share")
        }
        IconButton(onClick = { }) {
            Icon(Icons.Default.Delete, contentDescription = "Delete")
        }
    }
}
```

### サイド配置

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun SideVerticalToolbar() {
    var expanded by remember { mutableStateOf(true) }

    Box(modifier = Modifier.fillMaxSize()) {
        // Main content

        // 右側にツールバー配置
        VerticalFloatingToolbar(
            expanded = expanded,
            modifier = Modifier
                .align(Alignment.CenterEnd)
                .padding(16.dp),
            floatingActionButton = {
                FloatingActionButton(onClick = { }) {
                    Icon(Icons.Default.Add, contentDescription = "Add")
                }
            }
        ) {
            IconButton(onClick = { }) {
                Icon(Icons.Default.ZoomIn, contentDescription = "Zoom in")
            }
            IconButton(onClick = { }) {
                Icon(Icons.Default.ZoomOut, contentDescription = "Zoom out")
            }
            IconButton(onClick = { }) {
                Icon(Icons.Default.MyLocation, contentDescription = "My location")
            }
        }
    }
}
```

## FlexibleBottomAppBar

### 基本的な使用法

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun BasicFlexibleBottomAppBar() {
    Scaffold(
        bottomBar = {
            FlexibleBottomAppBar(
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                IconButton(onClick = { }) {
                    Icon(Icons.Default.Home, contentDescription = "Home")
                }
                IconButton(onClick = { }) {
                    Icon(Icons.Default.Search, contentDescription = "Search")
                }
                IconButton(onClick = { }) {
                    Icon(Icons.Default.Favorite, contentDescription = "Favorites")
                }
                IconButton(onClick = { }) {
                    Icon(Icons.Default.Person, contentDescription = "Profile")
                }
            }
        }
    ) { paddingValues ->
        // Content
    }
}
```

### FAB 付き

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun FlexibleBottomAppBarWithFAB() {
    Scaffold(
        bottomBar = {
            FlexibleBottomAppBar(
                floatingActionButton = {
                    FloatingActionButton(
                        onClick = { },
                        elevation = FloatingActionButtonDefaults.bottomAppBarFabElevation()
                    ) {
                        Icon(Icons.Default.Add, contentDescription = "Add")
                    }
                }
            ) {
                IconButton(onClick = { }) {
                    Icon(Icons.Default.Menu, contentDescription = "Menu")
                }
                Spacer(modifier = Modifier.weight(1f))
                IconButton(onClick = { }) {
                    Icon(Icons.Default.Search, contentDescription = "Search")
                }
                IconButton(onClick = { }) {
                    Icon(Icons.Default.MoreVert, contentDescription = "More")
                }
            }
        }
    ) { paddingValues ->
        // Content
    }
}
```

## スクロール連動

### ツールバーの展開/折りたたみ

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ScrollAwareToolbar() {
    val listState = rememberLazyListState()
    var toolbarExpanded by remember { mutableStateOf(true) }

    // スクロール方向を監視
    LaunchedEffect(listState) {
        snapshotFlow { listState.firstVisibleItemScrollOffset }
            .collect { offset ->
                // 下スクロールで折りたたみ、上スクロールで展開
                toolbarExpanded = offset == 0
            }
    }

    Scaffold(
        floatingActionButton = {
            HorizontalFloatingToolbar(
                expanded = toolbarExpanded,
                floatingActionButton = {
                    FloatingActionButton(onClick = { }) {
                        Icon(Icons.Default.Add, contentDescription = "Add")
                    }
                }
            ) {
                IconButton(onClick = { }) {
                    Icon(Icons.Default.Edit, contentDescription = "Edit")
                }
            }
        }
    ) { paddingValues ->
        LazyColumn(
            state = listState,
            contentPadding = paddingValues
        ) {
            items(50) { index ->
                Text(
                    text = "Item $index",
                    modifier = Modifier.padding(16.dp)
                )
            }
        }
    }
}
```

### NestedScroll との統合

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun NestedScrollToolbar() {
    val scrollBehavior = BottomAppBarDefaults.exitAlwaysScrollBehavior()

    Scaffold(
        modifier = Modifier.nestedScroll(scrollBehavior.nestedScrollConnection),
        bottomBar = {
            FlexibleBottomAppBar(
                scrollBehavior = scrollBehavior
            ) {
                IconButton(onClick = { }) {
                    Icon(Icons.Default.Home, contentDescription = "Home")
                }
                IconButton(onClick = { }) {
                    Icon(Icons.Default.Search, contentDescription = "Search")
                }
            }
        }
    ) { paddingValues ->
        LazyColumn(contentPadding = paddingValues) {
            items(100) { index ->
                Text(
                    text = "Item $index",
                    modifier = Modifier.padding(16.dp)
                )
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
fun CustomColorToolbar() {
    HorizontalFloatingToolbar(
        expanded = true,
        colors = FloatingToolbarDefaults.floatingToolbarColors(
            containerColor = MaterialTheme.colorScheme.primaryContainer,
            contentColor = MaterialTheme.colorScheme.onPrimaryContainer
        ),
        floatingActionButton = {
            FloatingActionButton(
                onClick = { },
                containerColor = MaterialTheme.colorScheme.primary
            ) {
                Icon(Icons.Default.Add, contentDescription = "Add")
            }
        }
    ) {
        IconButton(onClick = { }) {
            Icon(Icons.Default.Edit, contentDescription = "Edit")
        }
    }
}
```

### シェイプのカスタマイズ

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun CustomShapeToolbar() {
    HorizontalFloatingToolbar(
        expanded = true,
        shape = RoundedCornerShape(24.dp),
        floatingActionButton = {
            FloatingActionButton(
                onClick = { },
                shape = CircleShape
            ) {
                Icon(Icons.Default.Add, contentDescription = "Add")
            }
        }
    ) {
        IconButton(onClick = { }) {
            Icon(Icons.Default.Edit, contentDescription = "Edit")
        }
    }
}
```

## 使用パターン

### コンテキストツールバー

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ContextualToolbar(
    selectedCount: Int,
    onDelete: () -> Unit,
    onShare: () -> Unit,
    onCopy: () -> Unit,
    onDismiss: () -> Unit
) {
    AnimatedVisibility(
        visible = selectedCount > 0,
        enter = slideInVertically(initialOffsetY = { it }),
        exit = slideOutVertically(targetOffsetY = { it })
    ) {
        HorizontalFloatingToolbar(
            expanded = true,
            floatingActionButton = {
                IconButton(onClick = onDismiss) {
                    Icon(Icons.Default.Close, contentDescription = "Dismiss")
                }
            }
        ) {
            Text(
                text = "$selectedCount selected",
                modifier = Modifier.padding(horizontal = 16.dp)
            )
            Spacer(modifier = Modifier.weight(1f))
            IconButton(onClick = onShare) {
                Icon(Icons.Default.Share, contentDescription = "Share")
            }
            IconButton(onClick = onCopy) {
                Icon(Icons.Default.ContentCopy, contentDescription = "Copy")
            }
            IconButton(onClick = onDelete) {
                Icon(Icons.Default.Delete, contentDescription = "Delete")
            }
        }
    }
}
```

## アクセシビリティ

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun AccessibleToolbar() {
    HorizontalFloatingToolbar(
        expanded = true,
        modifier = Modifier.semantics {
            contentDescription = "Action toolbar"
        },
        floatingActionButton = {
            FloatingActionButton(
                onClick = { },
                modifier = Modifier.semantics {
                    contentDescription = "Create new item"
                }
            ) {
                Icon(Icons.Default.Add, contentDescription = null)
            }
        }
    ) {
        IconButton(
            onClick = { },
            modifier = Modifier.semantics {
                contentDescription = "Edit selected items"
            }
        ) {
            Icon(Icons.Default.Edit, contentDescription = null)
        }
    }
}
```

## ベストプラクティス

### 1. アクション数

- 水平ツールバー: 2-5個
- 垂直ツールバー: 2-4個
- 多い場合は オーバーフローメニュー を使用

### 2. 一貫した配置

- プライマリアクション（FAB）は右端または下端
- 関連アクションはグループ化

### 3. スクロール挙動

- コンテンツ閲覧時は折りたたみを検討
- 重要なアクションは常に表示

## 関連リソース

- [FAB Components](fab-components.md) - FAB の詳細
- [Motion System](motion-system.md) - アニメーション
- [examples/floating-toolbar-example.kt](../examples/floating-toolbar-example.kt) - 実装例
