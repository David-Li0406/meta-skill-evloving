/**
 * Material 3 Expressive - Expressive List Examples
 *
 * Expressive List Items と関連コンポーネントの使用例。
 */

package com.example.m3expressive.examples

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowForward
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.Star
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material.icons.outlined.FavoriteBorder
import androidx.compose.material3.Checkbox
import androidx.compose.material3.ExperimentalMaterial3ExpressiveApi
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.ListItem
import androidx.compose.material3.ListItemDefaults
import androidx.compose.material3.MaterialExpressiveTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.RadioButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp

// =============================================================================
// Basic List Items
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun BasicListItems() {
    Column(
        modifier = Modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "Basic List Items",
            style = MaterialTheme.typography.titleMedium
        )

        Surface(tonalElevation = 1.dp) {
            Column {
                // One-line
                ListItem(
                    headlineContent = { Text("One-line item") }
                )
                HorizontalDivider()

                // Two-line
                ListItem(
                    headlineContent = { Text("Two-line item") },
                    supportingContent = { Text("Supporting text") }
                )
                HorizontalDivider()

                // Three-line
                ListItem(
                    headlineContent = { Text("Three-line item") },
                    supportingContent = { Text("Supporting text that spans multiple lines to demonstrate the three-line variant") },
                    overlineContent = { Text("Overline") }
                )
            }
        }
    }
}

// =============================================================================
// List Items with Leading Icons
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ListItemsWithLeadingIcons() {
    Column(
        modifier = Modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "With Leading Icons",
            style = MaterialTheme.typography.titleMedium
        )

        Surface(tonalElevation = 1.dp) {
            Column {
                ListItem(
                    headlineContent = { Text("Profile") },
                    supportingContent = { Text("View and edit your profile") },
                    leadingContent = {
                        Icon(Icons.Default.Person, contentDescription = null)
                    }
                )
                HorizontalDivider()

                ListItem(
                    headlineContent = { Text("Notifications") },
                    supportingContent = { Text("Manage notification settings") },
                    leadingContent = {
                        Icon(Icons.Default.Notifications, contentDescription = null)
                    }
                )
                HorizontalDivider()

                ListItem(
                    headlineContent = { Text("Settings") },
                    supportingContent = { Text("App preferences") },
                    leadingContent = {
                        Icon(Icons.Default.Settings, contentDescription = null)
                    }
                )
            }
        }
    }
}

// =============================================================================
// List Items with Trailing Content
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ListItemsWithTrailingContent() {
    var notificationsEnabled by remember { mutableStateOf(true) }
    var darkModeEnabled by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "With Trailing Content",
            style = MaterialTheme.typography.titleMedium
        )

        Surface(tonalElevation = 1.dp) {
            Column {
                // With Switch
                ListItem(
                    headlineContent = { Text("Notifications") },
                    supportingContent = { Text("Receive push notifications") },
                    leadingContent = {
                        Icon(Icons.Default.Notifications, contentDescription = null)
                    },
                    trailingContent = {
                        Switch(
                            checked = notificationsEnabled,
                            onCheckedChange = { notificationsEnabled = it }
                        )
                    }
                )
                HorizontalDivider()

                // With Switch
                ListItem(
                    headlineContent = { Text("Dark Mode") },
                    supportingContent = { Text("Use dark theme") },
                    leadingContent = {
                        Icon(Icons.Default.Settings, contentDescription = null)
                    },
                    trailingContent = {
                        Switch(
                            checked = darkModeEnabled,
                            onCheckedChange = { darkModeEnabled = it }
                        )
                    }
                )
                HorizontalDivider()

                // With Chevron
                ListItem(
                    headlineContent = { Text("About") },
                    supportingContent = { Text("App version and info") },
                    leadingContent = {
                        Icon(Icons.Default.Info, contentDescription = null)
                    },
                    trailingContent = {
                        Icon(Icons.Default.ChevronRight, contentDescription = null)
                    },
                    modifier = Modifier.clickable { }
                )
            }
        }
    }
}

// =============================================================================
// Selectable List Items
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun SelectableListItems() {
    val items = remember {
        mutableStateListOf(
            "Item 1" to false,
            "Item 2" to true,
            "Item 3" to false,
            "Item 4" to true
        )
    }

    Column(
        modifier = Modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "Selectable List Items",
            style = MaterialTheme.typography.titleMedium
        )

        Surface(tonalElevation = 1.dp) {
            Column {
                items.forEachIndexed { index, (text, checked) ->
                    ListItem(
                        headlineContent = { Text(text) },
                        leadingContent = {
                            Checkbox(
                                checked = checked,
                                onCheckedChange = { newChecked ->
                                    items[index] = text to newChecked
                                }
                            )
                        },
                        modifier = Modifier.clickable {
                            items[index] = text to !checked
                        },
                        colors = if (checked) {
                            ListItemDefaults.colors(
                                containerColor = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.3f)
                            )
                        } else {
                            ListItemDefaults.colors()
                        }
                    )
                    if (index < items.lastIndex) {
                        HorizontalDivider()
                    }
                }
            }
        }
    }
}

// =============================================================================
// Radio Button List
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun RadioButtonList() {
    var selectedOption by remember { mutableStateOf("Option 1") }
    val options = listOf("Option 1", "Option 2", "Option 3")

    Column(
        modifier = Modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "Radio Button List",
            style = MaterialTheme.typography.titleMedium
        )

        Surface(tonalElevation = 1.dp) {
            Column {
                options.forEachIndexed { index, option ->
                    ListItem(
                        headlineContent = { Text(option) },
                        leadingContent = {
                            RadioButton(
                                selected = selectedOption == option,
                                onClick = { selectedOption = option }
                            )
                        },
                        modifier = Modifier.clickable { selectedOption = option }
                    )
                    if (index < options.lastIndex) {
                        HorizontalDivider()
                    }
                }
            }
        }
    }
}

// =============================================================================
// Interactive List with Favorites
// =============================================================================

data class ListItemData(
    val id: Int,
    val title: String,
    val subtitle: String,
    val icon: ImageVector,
    var isFavorite: Boolean = false,
    var isBookmarked: Boolean = false
)

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun InteractiveList() {
    val items = remember {
        mutableStateListOf(
            ListItemData(1, "Article 1", "Technology", Icons.Default.Star),
            ListItemData(2, "Article 2", "Science", Icons.Default.Star),
            ListItemData(3, "Article 3", "Business", Icons.Default.Star),
            ListItemData(4, "Article 4", "Sports", Icons.Default.Star)
        )
    }

    Column(
        modifier = Modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "Interactive List",
            style = MaterialTheme.typography.titleMedium
        )

        Surface(tonalElevation = 1.dp) {
            LazyColumn {
                items(items) { item ->
                    ListItem(
                        headlineContent = { Text(item.title) },
                        supportingContent = { Text(item.subtitle) },
                        leadingContent = {
                            Icon(item.icon, contentDescription = null)
                        },
                        trailingContent = {
                            IconButton(
                                onClick = {
                                    val index = items.indexOfFirst { it.id == item.id }
                                    if (index >= 0) {
                                        items[index] = item.copy(isFavorite = !item.isFavorite)
                                    }
                                }
                            ) {
                                Icon(
                                    imageVector = if (item.isFavorite)
                                        Icons.Filled.Favorite
                                    else
                                        Icons.Outlined.FavoriteBorder,
                                    contentDescription = if (item.isFavorite) "Remove from favorites" else "Add to favorites",
                                    tint = if (item.isFavorite)
                                        MaterialTheme.colorScheme.error
                                    else
                                        MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                        }
                    )
                    HorizontalDivider()
                }
            }
        }
    }
}

// =============================================================================
// Colored List Items
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ColoredListItems() {
    Column(
        modifier = Modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "Colored List Items",
            style = MaterialTheme.typography.titleMedium
        )

        Column {
            // Primary container
            ListItem(
                headlineContent = { Text("Primary") },
                supportingContent = { Text("Primary container color") },
                leadingContent = {
                    Icon(Icons.Default.Check, contentDescription = null)
                },
                colors = ListItemDefaults.colors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer,
                    headlineColor = MaterialTheme.colorScheme.onPrimaryContainer,
                    supportingColor = MaterialTheme.colorScheme.onPrimaryContainer,
                    leadingIconColor = MaterialTheme.colorScheme.onPrimaryContainer
                )
            )

            // Secondary container
            ListItem(
                headlineContent = { Text("Secondary") },
                supportingContent = { Text("Secondary container color") },
                leadingContent = {
                    Icon(Icons.Default.Star, contentDescription = null)
                },
                colors = ListItemDefaults.colors(
                    containerColor = MaterialTheme.colorScheme.secondaryContainer,
                    headlineColor = MaterialTheme.colorScheme.onSecondaryContainer,
                    supportingColor = MaterialTheme.colorScheme.onSecondaryContainer,
                    leadingIconColor = MaterialTheme.colorScheme.onSecondaryContainer
                )
            )

            // Tertiary container
            ListItem(
                headlineContent = { Text("Tertiary") },
                supportingContent = { Text("Tertiary container color") },
                leadingContent = {
                    Icon(Icons.Default.Bookmark, contentDescription = null)
                },
                colors = ListItemDefaults.colors(
                    containerColor = MaterialTheme.colorScheme.tertiaryContainer,
                    headlineColor = MaterialTheme.colorScheme.onTertiaryContainer,
                    supportingColor = MaterialTheme.colorScheme.onTertiaryContainer,
                    leadingIconColor = MaterialTheme.colorScheme.onTertiaryContainer
                )
            )
        }
    }
}

// =============================================================================
// Previews
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun BasicListItemsPreview() {
    MaterialExpressiveTheme {
        BasicListItems()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun ListItemsWithLeadingIconsPreview() {
    MaterialExpressiveTheme {
        ListItemsWithLeadingIcons()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun ListItemsWithTrailingContentPreview() {
    MaterialExpressiveTheme {
        ListItemsWithTrailingContent()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun SelectableListItemsPreview() {
    MaterialExpressiveTheme {
        SelectableListItems()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun RadioButtonListPreview() {
    MaterialExpressiveTheme {
        RadioButtonList()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun InteractiveListPreview() {
    MaterialExpressiveTheme {
        InteractiveList()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun ColoredListItemsPreview() {
    MaterialExpressiveTheme {
        ColoredListItems()
    }
}
