/**
 * Material 3 Expressive - Shape Morphing Examples
 *
 * MaterialShapes を使用したシェイプモーフィングのデモ。
 */

package com.example.m3expressive.examples

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.Share
import androidx.compose.material.icons.filled.Star
import androidx.compose.material.icons.outlined.Add
import androidx.compose.material.icons.outlined.FavoriteBorder
import androidx.compose.material.icons.outlined.Star
import androidx.compose.material3.ExperimentalMaterial3ExpressiveApi
import androidx.compose.material3.FilledIconButton
import androidx.compose.material3.FilledIconToggleButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.IconToggleButton
import androidx.compose.material3.MaterialExpressiveTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedIconButton
import androidx.compose.material3.OutlinedIconToggleButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
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
// Basic Icon Toggle Button with Morphing
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun BasicMorphingIconToggleButton() {
    var isChecked by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "Basic Icon Toggle Button",
            style = MaterialTheme.typography.titleMedium
        )

        Text(
            text = "Tap to see shape morphing",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )

        // IconToggleButton は自動的にシェイプモーフィングを行う
        IconToggleButton(
            checked = isChecked,
            onCheckedChange = { isChecked = it },
            modifier = Modifier.size(56.dp)
        ) {
            Icon(
                imageVector = if (isChecked) Icons.Filled.Favorite else Icons.Outlined.FavoriteBorder,
                contentDescription = if (isChecked) "Remove from favorites" else "Add to favorites",
                modifier = Modifier.size(24.dp)
            )
        }

        Text(
            text = if (isChecked) "Checked" else "Unchecked",
            style = MaterialTheme.typography.labelMedium
        )
    }
}

// =============================================================================
// Filled Icon Toggle Button Variants
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun FilledMorphingButtons() {
    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            text = "Filled Icon Toggle Buttons",
            style = MaterialTheme.typography.titleMedium
        )

        Row(
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Favorite Toggle
            var isFavorite by remember { mutableStateOf(false) }
            FilledIconToggleButton(
                checked = isFavorite,
                onCheckedChange = { isFavorite = it }
            ) {
                Icon(
                    imageVector = if (isFavorite) Icons.Filled.Favorite else Icons.Outlined.FavoriteBorder,
                    contentDescription = "Favorite"
                )
            }

            // Star Toggle
            var isStarred by remember { mutableStateOf(false) }
            FilledIconToggleButton(
                checked = isStarred,
                onCheckedChange = { isStarred = it }
            ) {
                Icon(
                    imageVector = if (isStarred) Icons.Filled.Star else Icons.Outlined.Star,
                    contentDescription = "Star"
                )
            }

            // Check Toggle
            var isSelected by remember { mutableStateOf(false) }
            FilledIconToggleButton(
                checked = isSelected,
                onCheckedChange = { isSelected = it }
            ) {
                Icon(
                    imageVector = if (isSelected) Icons.Filled.Check else Icons.Outlined.Add,
                    contentDescription = "Select"
                )
            }
        }
    }
}

// =============================================================================
// Outlined Icon Toggle Button Variants
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun OutlinedMorphingButtons() {
    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            text = "Outlined Icon Toggle Buttons",
            style = MaterialTheme.typography.titleMedium
        )

        Row(
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Favorite Toggle
            var isFavorite by remember { mutableStateOf(false) }
            OutlinedIconToggleButton(
                checked = isFavorite,
                onCheckedChange = { isFavorite = it }
            ) {
                Icon(
                    imageVector = if (isFavorite) Icons.Filled.Favorite else Icons.Outlined.FavoriteBorder,
                    contentDescription = "Favorite"
                )
            }

            // Star Toggle
            var isStarred by remember { mutableStateOf(true) }
            OutlinedIconToggleButton(
                checked = isStarred,
                onCheckedChange = { isStarred = it }
            ) {
                Icon(
                    imageVector = if (isStarred) Icons.Filled.Star else Icons.Outlined.Star,
                    contentDescription = "Star"
                )
            }
        }
    }
}

// =============================================================================
// Press Animation Demo (Standard Icon Buttons)
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun PressAnimationDemo() {
    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            text = "Press Animation (Hold to see)",
            style = MaterialTheme.typography.titleMedium
        )

        Text(
            text = "Standard buttons morph shape when pressed",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )

        Row(
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Standard IconButton
            IconButton(onClick = { }) {
                Icon(Icons.Default.Add, contentDescription = "Add")
            }

            // Filled IconButton
            FilledIconButton(onClick = { }) {
                Icon(Icons.Default.Edit, contentDescription = "Edit")
            }

            // Outlined IconButton
            OutlinedIconButton(onClick = { }) {
                Icon(Icons.Default.Share, contentDescription = "Share")
            }
        }
    }
}

// =============================================================================
// Multiple Selection Demo
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun MultipleSelectionDemo() {
    val items = listOf(
        "Edit" to Icons.Default.Edit,
        "Share" to Icons.Default.Share,
        "Delete" to Icons.Default.Delete,
        "Favorite" to Icons.Default.Favorite,
        "Star" to Icons.Default.Star
    )

    var selectedItems by remember { mutableStateOf(setOf<String>()) }

    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            text = "Multiple Selection",
            style = MaterialTheme.typography.titleMedium
        )

        Text(
            text = "Selected: ${selectedItems.size}",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )

        LazyRow(
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(items) { (label, icon) ->
                val isSelected = selectedItems.contains(label)

                FilledIconToggleButton(
                    checked = isSelected,
                    onCheckedChange = { checked ->
                        selectedItems = if (checked) {
                            selectedItems + label
                        } else {
                            selectedItems - label
                        }
                    }
                ) {
                    Icon(
                        imageVector = icon,
                        contentDescription = label
                    )
                }
            }
        }
    }
}

// =============================================================================
// Size Variants Demo
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun SizeVariantsDemo() {
    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            text = "Size Variants",
            style = MaterialTheme.typography.titleMedium
        )

        Row(
            horizontalArrangement = Arrangement.spacedBy(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Small
            var small by remember { mutableStateOf(false) }
            FilledIconToggleButton(
                checked = small,
                onCheckedChange = { small = it },
                modifier = Modifier.size(40.dp)
            ) {
                Icon(
                    imageVector = if (small) Icons.Filled.Favorite else Icons.Outlined.FavoriteBorder,
                    contentDescription = "Small",
                    modifier = Modifier.size(20.dp)
                )
            }

            // Medium (default)
            var medium by remember { mutableStateOf(false) }
            FilledIconToggleButton(
                checked = medium,
                onCheckedChange = { medium = it },
                modifier = Modifier.size(48.dp)
            ) {
                Icon(
                    imageVector = if (medium) Icons.Filled.Favorite else Icons.Outlined.FavoriteBorder,
                    contentDescription = "Medium",
                    modifier = Modifier.size(24.dp)
                )
            }

            // Large
            var large by remember { mutableStateOf(false) }
            FilledIconToggleButton(
                checked = large,
                onCheckedChange = { large = it },
                modifier = Modifier.size(56.dp)
            ) {
                Icon(
                    imageVector = if (large) Icons.Filled.Favorite else Icons.Outlined.FavoriteBorder,
                    contentDescription = "Large",
                    modifier = Modifier.size(28.dp)
                )
            }
        }

        Text(
            text = "40dp / 48dp / 56dp",
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

// =============================================================================
// Combined Demo Screen
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ShapeMorphingDemoScreen() {
    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(24.dp)
        ) {
            Text(
                text = "Shape Morphing Demo",
                style = MaterialTheme.typography.headlineMedium
            )

            BasicMorphingIconToggleButton()

            Spacer(modifier = Modifier.height(8.dp))

            FilledMorphingButtons()

            Spacer(modifier = Modifier.height(8.dp))

            OutlinedMorphingButtons()

            Spacer(modifier = Modifier.height(8.dp))

            PressAnimationDemo()
        }
    }
}

// =============================================================================
// Previews
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun BasicMorphingPreview() {
    MaterialExpressiveTheme {
        BasicMorphingIconToggleButton()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun FilledMorphingPreview() {
    MaterialExpressiveTheme {
        FilledMorphingButtons()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun OutlinedMorphingPreview() {
    MaterialExpressiveTheme {
        OutlinedMorphingButtons()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun MultipleSelectionPreview() {
    MaterialExpressiveTheme {
        MultipleSelectionDemo()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun SizeVariantsPreview() {
    MaterialExpressiveTheme {
        SizeVariantsDemo()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun ShapeMorphingScreenPreview() {
    MaterialExpressiveTheme {
        ShapeMorphingDemoScreen()
    }
}
