# Material 3 Expressive Menus

新しい Expressive Menu システムの実装ガイド。

## Overview

Material 3 Expressive では、メニューシステムが刷新され、
トグル可能なアイテム、選択可能なアイテム、グループ化などの新機能が追加されました。

## 基本的な DropdownMenu

```kotlin
@Composable
fun BasicDropdownMenu() {
    var expanded by remember { mutableStateOf(false) }

    Box {
        IconButton(onClick = { expanded = true }) {
            Icon(Icons.Default.MoreVert, contentDescription = "Menu")
        }

        DropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false }
        ) {
            DropdownMenuItem(
                text = { Text("Edit") },
                onClick = {
                    expanded = false
                    // Handle edit
                },
                leadingIcon = { Icon(Icons.Default.Edit, null) }
            )
            DropdownMenuItem(
                text = { Text("Share") },
                onClick = {
                    expanded = false
                    // Handle share
                },
                leadingIcon = { Icon(Icons.Default.Share, null) }
            )
            HorizontalDivider()
            DropdownMenuItem(
                text = { Text("Delete") },
                onClick = {
                    expanded = false
                    // Handle delete
                },
                leadingIcon = {
                    Icon(
                        Icons.Default.Delete,
                        null,
                        tint = MaterialTheme.colorScheme.error
                    )
                }
            )
        }
    }
}
```

## Expressive Menu Items

### Toggleable Menu Item

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ToggleableMenuExample() {
    var expanded by remember { mutableStateOf(false) }
    var notificationsEnabled by remember { mutableStateOf(true) }
    var darkModeEnabled by remember { mutableStateOf(false) }

    Box {
        IconButton(onClick = { expanded = true }) {
            Icon(Icons.Default.Settings, contentDescription = "Settings")
        }

        DropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false }
        ) {
            // Toggleable item with switch
            DropdownMenuItem(
                text = { Text("Notifications") },
                onClick = { notificationsEnabled = !notificationsEnabled },
                leadingIcon = { Icon(Icons.Default.Notifications, null) },
                trailingIcon = {
                    Switch(
                        checked = notificationsEnabled,
                        onCheckedChange = { notificationsEnabled = it }
                    )
                }
            )

            DropdownMenuItem(
                text = { Text("Dark Mode") },
                onClick = { darkModeEnabled = !darkModeEnabled },
                leadingIcon = { Icon(Icons.Default.DarkMode, null) },
                trailingIcon = {
                    Switch(
                        checked = darkModeEnabled,
                        onCheckedChange = { darkModeEnabled = it }
                    )
                }
            )
        }
    }
}
```

### Selectable Menu Item

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun SelectableMenuExample() {
    var expanded by remember { mutableStateOf(false) }
    var selectedOption by remember { mutableStateOf("Option 1") }
    val options = listOf("Option 1", "Option 2", "Option 3")

    Box {
        TextButton(onClick = { expanded = true }) {
            Text(selectedOption)
            Icon(Icons.Default.ArrowDropDown, null)
        }

        DropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false }
        ) {
            options.forEach { option ->
                DropdownMenuItem(
                    text = { Text(option) },
                    onClick = {
                        selectedOption = option
                        expanded = false
                    },
                    leadingIcon = {
                        if (selectedOption == option) {
                            Icon(Icons.Default.Check, null)
                        }
                    }
                )
            }
        }
    }
}
```

### Multi-Select Menu

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun MultiSelectMenuExample() {
    var expanded by remember { mutableStateOf(false) }
    var selectedOptions by remember { mutableStateOf(setOf<String>()) }
    val options = listOf("Bold", "Italic", "Underline", "Strikethrough")

    Box {
        IconButton(onClick = { expanded = true }) {
            Icon(Icons.Default.FormatSize, contentDescription = "Format")
        }

        DropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false }
        ) {
            options.forEach { option ->
                val isSelected = selectedOptions.contains(option)

                DropdownMenuItem(
                    text = { Text(option) },
                    onClick = {
                        selectedOptions = if (isSelected) {
                            selectedOptions - option
                        } else {
                            selectedOptions + option
                        }
                    },
                    leadingIcon = {
                        Checkbox(
                            checked = isSelected,
                            onCheckedChange = { checked ->
                                selectedOptions = if (checked) {
                                    selectedOptions + option
                                } else {
                                    selectedOptions - option
                                }
                            }
                        )
                    }
                )
            }
        }
    }
}
```

## Menu Groups

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun GroupedMenuExample() {
    var expanded by remember { mutableStateOf(false) }

    Box {
        IconButton(onClick = { expanded = true }) {
            Icon(Icons.Default.MoreVert, contentDescription = "Menu")
        }

        DropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false }
        ) {
            // Edit group
            Text(
                text = "Edit",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.primary,
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
            )
            DropdownMenuItem(
                text = { Text("Cut") },
                onClick = { expanded = false },
                leadingIcon = { Icon(Icons.Default.ContentCut, null) }
            )
            DropdownMenuItem(
                text = { Text("Copy") },
                onClick = { expanded = false },
                leadingIcon = { Icon(Icons.Default.ContentCopy, null) }
            )
            DropdownMenuItem(
                text = { Text("Paste") },
                onClick = { expanded = false },
                leadingIcon = { Icon(Icons.Default.ContentPaste, null) }
            )

            HorizontalDivider()

            // View group
            Text(
                text = "View",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.primary,
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
            )
            DropdownMenuItem(
                text = { Text("Zoom In") },
                onClick = { expanded = false },
                leadingIcon = { Icon(Icons.Default.ZoomIn, null) }
            )
            DropdownMenuItem(
                text = { Text("Zoom Out") },
                onClick = { expanded = false },
                leadingIcon = { Icon(Icons.Default.ZoomOut, null) }
            )
        }
    }
}
```

## ExposedDropdownMenu

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ExposedDropdownMenuExample() {
    var expanded by remember { mutableStateOf(false) }
    var selectedOption by remember { mutableStateOf("") }
    val options = listOf("Option 1", "Option 2", "Option 3", "Option 4")

    ExposedDropdownMenuBox(
        expanded = expanded,
        onExpandedChange = { expanded = it }
    ) {
        OutlinedTextField(
            value = selectedOption,
            onValueChange = {},
            readOnly = true,
            label = { Text("Select option") },
            trailingIcon = {
                ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded)
            },
            colors = ExposedDropdownMenuDefaults.outlinedTextFieldColors(),
            modifier = Modifier
                .menuAnchor()
                .fillMaxWidth()
        )

        ExposedDropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false }
        ) {
            options.forEach { option ->
                DropdownMenuItem(
                    text = { Text(option) },
                    onClick = {
                        selectedOption = option
                        expanded = false
                    },
                    contentPadding = ExposedDropdownMenuDefaults.ItemContentPadding
                )
            }
        }
    }
}
```

## Context Menu

```kotlin
@Composable
fun ContextMenuExample() {
    var showMenu by remember { mutableStateOf(false) }
    var menuOffset by remember { mutableStateOf(Offset.Zero) }

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(200.dp)
            .background(MaterialTheme.colorScheme.surfaceVariant)
            .pointerInput(Unit) {
                detectTapGestures(
                    onLongPress = { offset ->
                        menuOffset = offset
                        showMenu = true
                    }
                )
            }
    ) {
        Text(
            text = "Long press to show context menu",
            modifier = Modifier.align(Alignment.Center)
        )

        DropdownMenu(
            expanded = showMenu,
            onDismissRequest = { showMenu = false },
            offset = DpOffset(menuOffset.x.dp, menuOffset.y.dp)
        ) {
            DropdownMenuItem(
                text = { Text("Copy") },
                onClick = { showMenu = false },
                leadingIcon = { Icon(Icons.Default.ContentCopy, null) }
            )
            DropdownMenuItem(
                text = { Text("Paste") },
                onClick = { showMenu = false },
                leadingIcon = { Icon(Icons.Default.ContentPaste, null) }
            )
            DropdownMenuItem(
                text = { Text("Select All") },
                onClick = { showMenu = false },
                leadingIcon = { Icon(Icons.Default.SelectAll, null) }
            )
        }
    }
}
```

## カスタマイズ

### メニューアイテムの色

```kotlin
@Composable
fun ColoredMenuItems() {
    DropdownMenuItem(
        text = {
            Text(
                "Delete",
                color = MaterialTheme.colorScheme.error
            )
        },
        onClick = { },
        leadingIcon = {
            Icon(
                Icons.Default.Delete,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.error
            )
        }
    )
}
```

### 無効化されたアイテム

```kotlin
@Composable
fun DisabledMenuItem() {
    DropdownMenuItem(
        text = { Text("Disabled Item") },
        onClick = { },
        enabled = false,
        leadingIcon = { Icon(Icons.Default.Block, null) }
    )
}
```

## アクセシビリティ

```kotlin
@Composable
fun AccessibleMenu() {
    var expanded by remember { mutableStateOf(false) }

    Box {
        IconButton(
            onClick = { expanded = true },
            modifier = Modifier.semantics {
                contentDescription = "Open menu"
            }
        ) {
            Icon(Icons.Default.MoreVert, contentDescription = null)
        }

        DropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false }
        ) {
            DropdownMenuItem(
                text = { Text("Edit") },
                onClick = { expanded = false },
                modifier = Modifier.semantics {
                    contentDescription = "Edit item"
                }
            )
        }
    }
}
```

## ベストプラクティス

### 1. 適切なアイテム数

- 推奨: 3-10 個
- 多い場合はサブメニューやグループ化を検討

### 2. 一貫したアイコン使用

```kotlin
// Good: すべてのアイテムにアイコンがある
DropdownMenuItem(text = { Text("Edit") }, leadingIcon = { Icon(...) }, onClick = {})
DropdownMenuItem(text = { Text("Delete") }, leadingIcon = { Icon(...) }, onClick = {})

// Bad: 一部のみアイコン
DropdownMenuItem(text = { Text("Edit") }, leadingIcon = { Icon(...) }, onClick = {})
DropdownMenuItem(text = { Text("Delete") }, onClick = {})  // アイコンなし
```

### 3. 破壊的アクションの視覚化

```kotlin
// 削除などの破壊的アクションは赤色で強調
DropdownMenuItem(
    text = { Text("Delete", color = MaterialTheme.colorScheme.error) },
    leadingIcon = { Icon(Icons.Default.Delete, tint = MaterialTheme.colorScheme.error) }
)
```

## 関連リソース

- [FAB Components](fab-components.md) - FAB メニュー
- [Motion System](motion-system.md) - アニメーション
