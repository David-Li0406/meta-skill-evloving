/**
 * Material 3 Expressive - Carousel Examples
 *
 * HorizontalMultiBrowseCarousel, HorizontalCenteredHeroCarousel の使用例。
 */

package com.example.m3expressive.examples

import androidx.compose.foundation.background
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
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3ExpressiveApi
import androidx.compose.material3.HorizontalCenteredHeroCarousel
import androidx.compose.material3.HorizontalMultiBrowseCarousel
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialExpressiveTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.carousel.rememberCarouselState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

// =============================================================================
// Basic Multi-Browse Carousel
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun BasicMultiBrowseCarousel() {
    val items = listOf("Item 1", "Item 2", "Item 3", "Item 4", "Item 5")

    Column(
        modifier = Modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "Multi-Browse Carousel",
            style = MaterialTheme.typography.titleMedium
        )

        HorizontalMultiBrowseCarousel(
            state = rememberCarouselState { items.count() },
            modifier = Modifier
                .fillMaxWidth()
                .height(150.dp),
            preferredItemWidth = 120.dp,
            itemSpacing = 8.dp
        ) { index ->
            Card(
                modifier = Modifier.fillMaxSize()
            ) {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = items[index],
                        style = MaterialTheme.typography.titleMedium
                    )
                }
            }
        }
    }
}

// =============================================================================
// Hero Carousel
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun BasicHeroCarousel() {
    val items = listOf("Hero 1", "Hero 2", "Hero 3")

    Column(
        modifier = Modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "Hero Carousel",
            style = MaterialTheme.typography.titleMedium
        )

        HorizontalCenteredHeroCarousel(
            state = rememberCarouselState { items.count() },
            modifier = Modifier
                .fillMaxWidth()
                .height(200.dp),
            itemWidth = 280.dp,
            itemSpacing = 16.dp
        ) { index ->
            Card(
                modifier = Modifier.fillMaxSize(),
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer
                )
            ) {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = items[index],
                        style = MaterialTheme.typography.headlineMedium,
                        color = MaterialTheme.colorScheme.onPrimaryContainer
                    )
                }
            }
        }
    }
}

// =============================================================================
// Feature Cards Carousel
// =============================================================================

data class FeatureItem(
    val icon: ImageVector,
    val title: String,
    val description: String
)

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun FeatureCarousel() {
    val features = listOf(
        FeatureItem(Icons.Default.Star, "Premium", "Unlock all features"),
        FeatureItem(Icons.Default.Notifications, "Alerts", "Stay notified"),
        FeatureItem(Icons.Default.Favorite, "Favorites", "Save your picks"),
        FeatureItem(Icons.Default.Settings, "Settings", "Customize your experience")
    )

    Column(
        modifier = Modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "Feature Cards",
            style = MaterialTheme.typography.titleMedium
        )

        HorizontalCenteredHeroCarousel(
            state = rememberCarouselState { features.count() },
            modifier = Modifier
                .fillMaxWidth()
                .height(220.dp),
            itemWidth = 260.dp,
            itemSpacing = 16.dp
        ) { index ->
            val feature = features[index]

            Card(
                modifier = Modifier.fillMaxSize()
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(24.dp),
                    verticalArrangement = Arrangement.SpaceBetween
                ) {
                    Icon(
                        imageVector = feature.icon,
                        contentDescription = null,
                        modifier = Modifier.size(48.dp),
                        tint = MaterialTheme.colorScheme.primary
                    )

                    Column {
                        Text(
                            text = feature.title,
                            style = MaterialTheme.typography.titleLarge
                        )
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            text = feature.description,
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            }
        }
    }
}

// =============================================================================
// Carousel with Page Indicator
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun CarouselWithIndicator() {
    val items = listOf("A", "B", "C", "D", "E")
    val carouselState = rememberCarouselState { items.count() }

    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "Carousel with Indicator",
            style = MaterialTheme.typography.titleMedium
        )

        HorizontalMultiBrowseCarousel(
            state = carouselState,
            modifier = Modifier
                .fillMaxWidth()
                .height(150.dp),
            preferredItemWidth = 150.dp,
            itemSpacing = 8.dp
        ) { index ->
            Card(
                modifier = Modifier.fillMaxSize(),
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.secondaryContainer
                )
            ) {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = items[index],
                        style = MaterialTheme.typography.displaySmall,
                        color = MaterialTheme.colorScheme.onSecondaryContainer
                    )
                }
            }
        }

        // Page Indicator
        Row(
            horizontalArrangement = Arrangement.Center
        ) {
            items.forEachIndexed { index, _ ->
                val isSelected = carouselState.currentPage == index
                Box(
                    modifier = Modifier
                        .padding(4.dp)
                        .size(if (isSelected) 10.dp else 8.dp)
                        .clip(CircleShape)
                        .background(
                            color = if (isSelected)
                                MaterialTheme.colorScheme.primary
                            else
                                MaterialTheme.colorScheme.outline
                        )
                )
            }
        }
    }
}

// =============================================================================
// Controlled Carousel
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ControlledCarousel() {
    val items = (1..10).toList()
    val carouselState = rememberCarouselState { items.count() }
    val coroutineScope = rememberCoroutineScope()

    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "Controlled Carousel",
            style = MaterialTheme.typography.titleMedium
        )

        HorizontalMultiBrowseCarousel(
            state = carouselState,
            modifier = Modifier
                .fillMaxWidth()
                .height(150.dp),
            preferredItemWidth = 120.dp,
            itemSpacing = 8.dp
        ) { index ->
            Card(modifier = Modifier.fillMaxSize()) {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = "Item ${items[index]}",
                        style = MaterialTheme.typography.titleMedium
                    )
                }
            }
        }

        Row(
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Button(
                onClick = {
                    coroutineScope.launch {
                        carouselState.animateScrollToItem(0)
                    }
                }
            ) {
                Text("First")
            }

            Button(
                onClick = {
                    coroutineScope.launch {
                        val prev = (carouselState.currentPage - 1).coerceAtLeast(0)
                        carouselState.animateScrollToItem(prev)
                    }
                }
            ) {
                Text("Prev")
            }

            Button(
                onClick = {
                    coroutineScope.launch {
                        val next = (carouselState.currentPage + 1).coerceAtMost(items.lastIndex)
                        carouselState.animateScrollToItem(next)
                    }
                }
            ) {
                Text("Next")
            }

            Button(
                onClick = {
                    coroutineScope.launch {
                        carouselState.animateScrollToItem(items.lastIndex)
                    }
                }
            ) {
                Text("Last")
            }
        }
    }
}

// =============================================================================
// Auto-Scroll Carousel
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun AutoScrollCarousel() {
    val items = listOf("Slide 1", "Slide 2", "Slide 3", "Slide 4", "Slide 5")
    val carouselState = rememberCarouselState { items.count() }

    // Auto-scroll effect
    LaunchedEffect(Unit) {
        while (true) {
            delay(3000L)
            val nextPage = (carouselState.currentPage + 1) % items.count()
            carouselState.animateScrollToItem(nextPage)
        }
    }

    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "Auto-Scroll Carousel",
            style = MaterialTheme.typography.titleMedium
        )

        Text(
            text = "Changes every 3 seconds",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )

        HorizontalCenteredHeroCarousel(
            state = carouselState,
            modifier = Modifier
                .fillMaxWidth()
                .height(180.dp),
            itemWidth = 280.dp,
            itemSpacing = 16.dp
        ) { index ->
            Card(
                modifier = Modifier.fillMaxSize(),
                colors = CardDefaults.cardColors(
                    containerColor = MaterialTheme.colorScheme.tertiaryContainer
                )
            ) {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = items[index],
                        style = MaterialTheme.typography.headlineSmall,
                        color = MaterialTheme.colorScheme.onTertiaryContainer
                    )
                }
            }
        }

        // Page Indicator
        Row(
            horizontalArrangement = Arrangement.Center
        ) {
            items.forEachIndexed { index, _ ->
                val isSelected = carouselState.currentPage == index
                Box(
                    modifier = Modifier
                        .padding(4.dp)
                        .size(if (isSelected) 10.dp else 8.dp)
                        .clip(CircleShape)
                        .background(
                            color = if (isSelected)
                                MaterialTheme.colorScheme.tertiary
                            else
                                MaterialTheme.colorScheme.outline
                        )
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
private fun BasicMultiBrowseCarouselPreview() {
    MaterialExpressiveTheme {
        BasicMultiBrowseCarousel()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun BasicHeroCarouselPreview() {
    MaterialExpressiveTheme {
        BasicHeroCarousel()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun FeatureCarouselPreview() {
    MaterialExpressiveTheme {
        FeatureCarousel()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun CarouselWithIndicatorPreview() {
    MaterialExpressiveTheme {
        CarouselWithIndicator()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun ControlledCarouselPreview() {
    MaterialExpressiveTheme {
        ControlledCarousel()
    }
}
