/**
 * Material 3 Expressive - FAB Menu Examples
 *
 * FloatingActionButtonMenu, ToggleFloatingActionButton, VibrantFloatingActionButton の使用例。
 */

package com.example.m3expressive.examples

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Create
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Photo
import androidx.compose.material.icons.filled.Share
import androidx.compose.material.icons.filled.Upload
import androidx.compose.material.icons.outlined.BookmarkBorder
import androidx.compose.material3.ExperimentalMaterial3ExpressiveApi
import androidx.compose.material3.ExtendedFloatingActionButton
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.FloatingActionButtonMenu
import androidx.compose.material3.FloatingActionButtonMenuItem
import androidx.compose.material3.FloatingToolbarDefaults
import androidx.compose.material3.HorizontalFloatingToolbar
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LargeFloatingActionButton
import androidx.compose.material3.MaterialExpressiveTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SmallFloatingActionButton
import androidx.compose.material3.Text
import androidx.compose.material3.ToggleFloatingActionButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp

// =============================================================================
// Basic FAB Menu
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun BasicFABMenu() {
    var expanded by remember { mutableStateOf(false) }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        contentAlignment = Alignment.BottomEnd
    ) {
        FloatingActionButtonMenu(
            expanded = expanded,
            button = {
                ToggleFloatingActionButton(
                    checked = expanded,
                    onCheckedChange = { expanded = it }
                ) {
                    AnimatedContent(
                        targetState = expanded,
                        transitionSpec = {
                            fadeIn(animationSpec = tween(200)) togetherWith
                                    fadeOut(animationSpec = tween(200))
                        },
                        label = "FAB icon"
                    ) { isExpanded ->
                        Icon(
                            imageVector = if (isExpanded) Icons.Default.Close else Icons.Default.Add,
                            contentDescription = if (isExpanded) "Close menu" else "Open menu"
                        )
                    }
                }
            }
        ) {
            FloatingActionButtonMenuItem(
                onClick = {
                    expanded = false
                    // Handle edit action
                },
                icon = { Icon(Icons.Default.Edit, contentDescription = null) },
                text = { Text("Edit") }
            )
            FloatingActionButtonMenuItem(
                onClick = {
                    expanded = false
                    // Handle share action
                },
                icon = { Icon(Icons.Default.Share, contentDescription = null) },
                text = { Text("Share") }
            )
            FloatingActionButtonMenuItem(
                onClick = {
                    expanded = false
                    // Handle delete action
                },
                icon = { Icon(Icons.Default.Delete, contentDescription = null) },
                text = { Text("Delete") }
            )
        }
    }
}

// =============================================================================
// FAB Menu in Scaffold
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun FABMenuInScaffold() {
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
                FloatingActionButtonMenuItem(
                    onClick = {
                        fabExpanded = false
                        // Navigate to photo
                    },
                    icon = { Icon(Icons.Default.Photo, null) },
                    text = { Text("Photo") }
                )
            }
        }
    ) { paddingValues ->
        LazyColumn(
            modifier = Modifier.padding(paddingValues),
            contentPadding = androidx.compose.foundation.layout.PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(20) { index ->
                Text(
                    text = "Item ${index + 1}",
                    modifier = Modifier.padding(16.dp)
                )
            }
        }
    }
}

// =============================================================================
// Toggle FAB (Bookmark Example)
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ToggleFABExample() {
    var isBookmarked by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            text = "Toggle FAB",
            style = MaterialTheme.typography.titleMedium
        )

        ToggleFloatingActionButton(
            checked = isBookmarked,
            onCheckedChange = { isBookmarked = it }
        ) {
            Icon(
                imageVector = if (isBookmarked) Icons.Filled.Bookmark else Icons.Outlined.BookmarkBorder,
                contentDescription = if (isBookmarked) "Remove bookmark" else "Add bookmark"
            )
        }

        Text(
            text = if (isBookmarked) "Bookmarked" else "Not bookmarked",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

// =============================================================================
// FAB Size Variants
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun FABSizeVariants() {
    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(24.dp)
    ) {
        Text(
            text = "FAB Size Variants",
            style = MaterialTheme.typography.titleMedium
        )

        Row(
            horizontalArrangement = Arrangement.spacedBy(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Small FAB
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                SmallFloatingActionButton(
                    onClick = { }
                ) {
                    Icon(Icons.Default.Add, contentDescription = "Add")
                }
                Text("Small", style = MaterialTheme.typography.labelSmall)
            }

            // Standard FAB
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                FloatingActionButton(
                    onClick = { }
                ) {
                    Icon(Icons.Default.Add, contentDescription = "Add")
                }
                Text("Standard", style = MaterialTheme.typography.labelSmall)
            }

            // Large FAB
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                LargeFloatingActionButton(
                    onClick = { }
                ) {
                    Icon(
                        Icons.Default.Add,
                        contentDescription = "Add",
                        modifier = Modifier.size(36.dp)
                    )
                }
                Text("Large", style = MaterialTheme.typography.labelSmall)
            }
        }

        // Extended FAB
        ExtendedFloatingActionButton(
            onClick = { },
            icon = { Icon(Icons.Default.Add, contentDescription = null) },
            text = { Text("Create") }
        )
        Text("Extended", style = MaterialTheme.typography.labelSmall)
    }
}

// =============================================================================
// Vibrant FAB with Toolbar
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun VibrantFABWithToolbar() {
    var expanded by remember { mutableStateOf(true) }

    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            text = "Vibrant FAB with Toolbar",
            style = MaterialTheme.typography.titleMedium
        )

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
            IconButton(onClick = { }) {
                Icon(Icons.Default.Delete, contentDescription = "Delete")
            }
        }
    }
}

// =============================================================================
// Custom Colored FAB Menu
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun CustomColoredFABMenu() {
    var expanded by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            text = "Custom Colored FAB Menu",
            style = MaterialTheme.typography.titleMedium
        )

        Box(
            modifier = Modifier.size(200.dp),
            contentAlignment = Alignment.BottomEnd
        ) {
            FloatingActionButtonMenu(
                expanded = expanded,
                button = {
                    ToggleFloatingActionButton(
                        checked = expanded,
                        onCheckedChange = { expanded = it },
                        containerColor = MaterialTheme.colorScheme.tertiaryContainer,
                        contentColor = MaterialTheme.colorScheme.onTertiaryContainer
                    ) {
                        Icon(
                            imageVector = if (expanded) Icons.Default.Close else Icons.Default.Add,
                            contentDescription = null
                        )
                    }
                }
            ) {
                FloatingActionButtonMenuItem(
                    onClick = { expanded = false },
                    icon = {
                        Icon(
                            Icons.Default.Edit,
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.tertiary
                        )
                    },
                    text = { Text("Edit") }
                )
                FloatingActionButtonMenuItem(
                    onClick = { expanded = false },
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
    }
}

// =============================================================================
// Previews
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun BasicFABMenuPreview() {
    MaterialExpressiveTheme {
        BasicFABMenu()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun FABMenuInScaffoldPreview() {
    MaterialExpressiveTheme {
        FABMenuInScaffold()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun ToggleFABPreview() {
    MaterialExpressiveTheme {
        ToggleFABExample()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun FABSizeVariantsPreview() {
    MaterialExpressiveTheme {
        FABSizeVariants()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun VibrantFABWithToolbarPreview() {
    MaterialExpressiveTheme {
        VibrantFABWithToolbar()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun CustomColoredFABMenuPreview() {
    MaterialExpressiveTheme {
        CustomColoredFABMenu()
    }
}
