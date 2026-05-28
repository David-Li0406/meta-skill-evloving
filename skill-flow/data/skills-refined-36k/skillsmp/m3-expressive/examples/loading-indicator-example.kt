/**
 * Material 3 Expressive - Loading Indicator Examples
 *
 * LoadingIndicator と ContainedLoadingIndicator の使用例。
 */

package com.example.m3expressive.examples

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.ContainedLoadingIndicator
import androidx.compose.material3.ExperimentalMaterial3ExpressiveApi
import androidx.compose.material3.LoadingIndicator
import androidx.compose.material3.MaterialExpressiveTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.delay

// =============================================================================
// Basic Loading Indicators
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun BasicLoadingIndicators() {
    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(24.dp)
    ) {
        Text(
            text = "Loading Indicators",
            style = MaterialTheme.typography.titleLarge
        )

        // 基本的な LoadingIndicator
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Text("LoadingIndicator", style = MaterialTheme.typography.labelMedium)
            Spacer(modifier = Modifier.height(8.dp))
            LoadingIndicator()
        }

        // ContainedLoadingIndicator
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Text("ContainedLoadingIndicator", style = MaterialTheme.typography.labelMedium)
            Spacer(modifier = Modifier.height(8.dp))
            ContainedLoadingIndicator()
        }
    }
}

// =============================================================================
// Size Variants
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun LoadingIndicatorSizes() {
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
            horizontalArrangement = Arrangement.spacedBy(24.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Small
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                LoadingIndicator(modifier = Modifier.size(24.dp))
                Text("24dp", style = MaterialTheme.typography.labelSmall)
            }

            // Medium
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                LoadingIndicator(modifier = Modifier.size(40.dp))
                Text("40dp", style = MaterialTheme.typography.labelSmall)
            }

            // Large
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                LoadingIndicator(modifier = Modifier.size(56.dp))
                Text("56dp", style = MaterialTheme.typography.labelSmall)
            }

            // Extra Large
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                LoadingIndicator(modifier = Modifier.size(72.dp))
                Text("72dp", style = MaterialTheme.typography.labelSmall)
            }
        }
    }
}

// =============================================================================
// Color Variants
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun LoadingIndicatorColors() {
    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            text = "Color Variants",
            style = MaterialTheme.typography.titleMedium
        )

        Row(
            horizontalArrangement = Arrangement.spacedBy(24.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Primary
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                LoadingIndicator(
                    modifier = Modifier.size(40.dp),
                    color = MaterialTheme.colorScheme.primary
                )
                Text("Primary", style = MaterialTheme.typography.labelSmall)
            }

            // Secondary
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                LoadingIndicator(
                    modifier = Modifier.size(40.dp),
                    color = MaterialTheme.colorScheme.secondary
                )
                Text("Secondary", style = MaterialTheme.typography.labelSmall)
            }

            // Tertiary
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                LoadingIndicator(
                    modifier = Modifier.size(40.dp),
                    color = MaterialTheme.colorScheme.tertiary
                )
                Text("Tertiary", style = MaterialTheme.typography.labelSmall)
            }

            // Error
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                LoadingIndicator(
                    modifier = Modifier.size(40.dp),
                    color = MaterialTheme.colorScheme.error
                )
                Text("Error", style = MaterialTheme.typography.labelSmall)
            }
        }
    }
}

// =============================================================================
// Contained Loading Indicator Variants
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ContainedLoadingIndicatorVariants() {
    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            text = "Contained Variants",
            style = MaterialTheme.typography.titleMedium
        )

        Row(
            horizontalArrangement = Arrangement.spacedBy(24.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Primary Container
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                ContainedLoadingIndicator(
                    indicatorColor = MaterialTheme.colorScheme.primary,
                    containerColor = MaterialTheme.colorScheme.primaryContainer
                )
                Text("Primary", style = MaterialTheme.typography.labelSmall)
            }

            // Secondary Container
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                ContainedLoadingIndicator(
                    indicatorColor = MaterialTheme.colorScheme.secondary,
                    containerColor = MaterialTheme.colorScheme.secondaryContainer
                )
                Text("Secondary", style = MaterialTheme.typography.labelSmall)
            }

            // Surface Variant
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                ContainedLoadingIndicator(
                    indicatorColor = MaterialTheme.colorScheme.onSurfaceVariant,
                    containerColor = MaterialTheme.colorScheme.surfaceVariant
                )
                Text("Surface", style = MaterialTheme.typography.labelSmall)
            }
        }
    }
}

// =============================================================================
// Loading Button
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun LoadingButtonExample() {
    var isLoading by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            text = "Loading Button",
            style = MaterialTheme.typography.titleMedium
        )

        Button(
            onClick = {
                isLoading = true
            },
            enabled = !isLoading
        ) {
            if (isLoading) {
                ContainedLoadingIndicator(
                    modifier = Modifier.size(20.dp),
                    indicatorColor = MaterialTheme.colorScheme.onPrimary,
                    containerColor = Color.Transparent
                )
                Spacer(modifier = Modifier.width(8.dp))
            }
            Text(if (isLoading) "Loading..." else "Submit")
        }

        // シミュレートされたローディング完了
        LaunchedEffect(isLoading) {
            if (isLoading) {
                delay(2000)
                isLoading = false
            }
        }
    }
}

// =============================================================================
// Full Screen Loading
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun FullScreenLoadingExample() {
    var isLoading by remember { mutableStateOf(true) }

    Box(modifier = Modifier.fillMaxSize()) {
        // Main content (shown when not loading)
        if (!isLoading) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(16.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                Text(
                    text = "Content Loaded!",
                    style = MaterialTheme.typography.headlineMedium
                )
                Spacer(modifier = Modifier.height(16.dp))
                Button(onClick = { isLoading = true }) {
                    Text("Reload")
                }
            }
        }

        // Loading overlay
        if (isLoading) {
            Surface(
                modifier = Modifier.fillMaxSize(),
                color = MaterialTheme.colorScheme.background
            ) {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        LoadingIndicator(
                            modifier = Modifier.size(64.dp)
                        )
                        Text(
                            text = "Loading...",
                            style = MaterialTheme.typography.bodyLarge,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            }
        }

        // シミュレートされたローディング完了
        LaunchedEffect(isLoading) {
            if (isLoading) {
                delay(2000)
                isLoading = false
            }
        }
    }
}

// =============================================================================
// Card Loading State
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun CardLoadingExample() {
    var isLoading by remember { mutableStateOf(true) }

    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            text = "Card Loading State",
            style = MaterialTheme.typography.titleMedium
        )

        Card(
            modifier = Modifier
                .fillMaxWidth()
                .height(200.dp)
        ) {
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                if (isLoading) {
                    ContainedLoadingIndicator(
                        containerColor = MaterialTheme.colorScheme.surfaceVariant
                    )
                } else {
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center
                    ) {
                        Text(
                            text = "Card Content",
                            style = MaterialTheme.typography.titleLarge
                        )
                        Text(
                            text = "Data loaded successfully",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            }
        }

        Button(onClick = { isLoading = !isLoading }) {
            Text(if (isLoading) "Show Content" else "Show Loading")
        }
    }
}

// =============================================================================
// Accessible Loading Indicator
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun AccessibleLoadingIndicator() {
    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            text = "Accessible Loading",
            style = MaterialTheme.typography.titleMedium
        )

        LoadingIndicator(
            modifier = Modifier
                .size(48.dp)
                .semantics {
                    contentDescription = "Loading content, please wait"
                }
        )

        Text(
            text = "Screen readers will announce the loading state",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

// =============================================================================
// Previews
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun BasicLoadingIndicatorsPreview() {
    MaterialExpressiveTheme {
        BasicLoadingIndicators()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun LoadingIndicatorSizesPreview() {
    MaterialExpressiveTheme {
        LoadingIndicatorSizes()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun LoadingIndicatorColorsPreview() {
    MaterialExpressiveTheme {
        LoadingIndicatorColors()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun ContainedVariantsPreview() {
    MaterialExpressiveTheme {
        ContainedLoadingIndicatorVariants()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun LoadingButtonPreview() {
    MaterialExpressiveTheme {
        LoadingButtonExample()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun CardLoadingPreview() {
    MaterialExpressiveTheme {
        CardLoadingExample()
    }
}
