/**
 * Material 3 Expressive - ButtonGroup Examples
 *
 * ButtonGroup コンポーネントの使用例。
 */

package com.example.m3expressive.examples

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.FormatAlignCenter
import androidx.compose.material.icons.filled.FormatAlignLeft
import androidx.compose.material.icons.filled.FormatAlignRight
import androidx.compose.material.icons.filled.FormatBold
import androidx.compose.material.icons.filled.FormatItalic
import androidx.compose.material.icons.filled.FormatUnderlined
import androidx.compose.material.icons.filled.GridView
import androidx.compose.material.icons.filled.List
import androidx.compose.material.icons.filled.ViewModule
import androidx.compose.material3.ButtonGroup
import androidx.compose.material3.ButtonGroupDefaults
import androidx.compose.material3.ExperimentalMaterial3ExpressiveApi
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialExpressiveTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.ToggleButton
import androidx.compose.material3.ToggleButtonDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp

// =============================================================================
// Basic Text ButtonGroup
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun BasicTextButtonGroup() {
    var selectedIndex by remember { mutableIntStateOf(0) }
    val options = listOf("Day", "Week", "Month")

    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "Basic Text ButtonGroup",
            style = MaterialTheme.typography.titleMedium
        )

        ButtonGroup {
            options.forEachIndexed { index, label ->
                ToggleButton(
                    checked = selectedIndex == index,
                    onCheckedChange = { if (it) selectedIndex = index }
                ) {
                    Text(label)
                }
            }
        }

        Text(
            text = "Selected: ${options[selectedIndex]}",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

// =============================================================================
// Connected ButtonGroup
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ConnectedButtonGroup() {
    var selectedIndex by remember { mutableIntStateOf(1) }

    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "Connected ButtonGroup",
            style = MaterialTheme.typography.titleMedium
        )

        ButtonGroup(
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
}

// =============================================================================
// Icon Only ButtonGroup
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun IconOnlyButtonGroup() {
    var selectedIndex by remember { mutableIntStateOf(0) }
    val icons = listOf(
        Icons.Default.List to "List view",
        Icons.Default.GridView to "Grid view",
        Icons.Default.ViewModule to "Module view"
    )

    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "Icon Only ButtonGroup",
            style = MaterialTheme.typography.titleMedium
        )

        ButtonGroup {
            icons.forEachIndexed { index, (icon, description) ->
                ToggleButton(
                    checked = selectedIndex == index,
                    onCheckedChange = { if (it) selectedIndex = index }
                ) {
                    Icon(icon, contentDescription = description)
                }
            }
        }
    }
}

// =============================================================================
// Icon + Text ButtonGroup
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun IconTextButtonGroup() {
    var selectedIndex by remember { mutableIntStateOf(0) }
    val options = listOf(
        Icons.Default.List to "List",
        Icons.Default.GridView to "Grid"
    )

    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "Icon + Text ButtonGroup",
            style = MaterialTheme.typography.titleMedium
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
}

// =============================================================================
// Multi-Select ButtonGroup
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun MultiSelectButtonGroup() {
    var isBold by remember { mutableStateOf(false) }
    var isItalic by remember { mutableStateOf(false) }
    var isUnderline by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "Multi-Select ButtonGroup",
            style = MaterialTheme.typography.titleMedium
        )

        ButtonGroup(
            spacing = ButtonGroupDefaults.ConnectedSpacing
        ) {
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

        Text(
            text = buildString {
                if (isBold) append("Bold ")
                if (isItalic) append("Italic ")
                if (isUnderline) append("Underline ")
                if (isEmpty()) append("None selected")
            }.trim(),
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

// =============================================================================
// Colored ButtonGroup
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ColoredButtonGroup() {
    var selectedIndex by remember { mutableIntStateOf(0) }
    val options = listOf("Primary", "Secondary", "Tertiary")

    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "Colored ButtonGroup",
            style = MaterialTheme.typography.titleMedium
        )

        ButtonGroup {
            ToggleButton(
                checked = selectedIndex == 0,
                onCheckedChange = { if (it) selectedIndex = 0 },
                colors = ToggleButtonDefaults.toggleButtonColors(
                    checkedContainerColor = MaterialTheme.colorScheme.primaryContainer,
                    checkedContentColor = MaterialTheme.colorScheme.onPrimaryContainer
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
            ToggleButton(
                checked = selectedIndex == 2,
                onCheckedChange = { if (it) selectedIndex = 2 },
                colors = ToggleButtonDefaults.toggleButtonColors(
                    checkedContainerColor = MaterialTheme.colorScheme.tertiaryContainer,
                    checkedContentColor = MaterialTheme.colorScheme.onTertiaryContainer
                )
            ) {
                Text("Tertiary")
            }
        }
    }
}

// =============================================================================
// Full Width ButtonGroup
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun FullWidthButtonGroup() {
    var selectedIndex by remember { mutableIntStateOf(0) }
    val options = listOf("All", "Active", "Completed")

    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "Full Width ButtonGroup",
            style = MaterialTheme.typography.titleMedium
        )

        ButtonGroup(
            modifier = Modifier.fillMaxWidth(),
            spacing = ButtonGroupDefaults.ConnectedSpacing
        ) {
            options.forEachIndexed { index, label ->
                val shape = when (index) {
                    0 -> ButtonGroupDefaults.connectedLeadingButtonShape
                    options.lastIndex -> ButtonGroupDefaults.connectedTrailingButtonShape
                    else -> ButtonGroupDefaults.connectedMiddleButtonShape
                }

                ToggleButton(
                    checked = selectedIndex == index,
                    onCheckedChange = { if (it) selectedIndex = index },
                    shape = shape,
                    modifier = Modifier.weight(1f)
                ) {
                    Text(label)
                }
            }
        }
    }
}

// =============================================================================
// Text Format Toolbar
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun TextFormatToolbar() {
    var isBold by remember { mutableStateOf(false) }
    var isItalic by remember { mutableStateOf(false) }
    var isUnderline by remember { mutableStateOf(false) }
    var alignment by remember { mutableIntStateOf(0) }

    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            text = "Text Format Toolbar",
            style = MaterialTheme.typography.titleMedium
        )

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
}

// =============================================================================
// Previews
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun BasicTextButtonGroupPreview() {
    MaterialExpressiveTheme {
        BasicTextButtonGroup()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun ConnectedButtonGroupPreview() {
    MaterialExpressiveTheme {
        ConnectedButtonGroup()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun IconOnlyButtonGroupPreview() {
    MaterialExpressiveTheme {
        IconOnlyButtonGroup()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun MultiSelectButtonGroupPreview() {
    MaterialExpressiveTheme {
        MultiSelectButtonGroup()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun FullWidthButtonGroupPreview() {
    MaterialExpressiveTheme {
        FullWidthButtonGroup()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun TextFormatToolbarPreview() {
    MaterialExpressiveTheme {
        TextFormatToolbar()
    }
}
