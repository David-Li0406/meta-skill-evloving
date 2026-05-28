/**
 * Material 3 Expressive - Complete Screen Example
 *
 * すべてのコンポーネントを統合した完全な画面例。
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
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.GridView
import androidx.compose.material.icons.filled.List
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.Share
import androidx.compose.material.icons.filled.Star
import androidx.compose.material.icons.outlined.FavoriteBorder
import androidx.compose.material3.ButtonGroup
import androidx.compose.material3.ButtonGroupDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CenterAlignedTopAppBar
import androidx.compose.material3.ContainedLoadingIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExperimentalMaterial3ExpressiveApi
import androidx.compose.material3.FloatingActionButtonMenu
import androidx.compose.material3.FloatingActionButtonMenuItem
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.HorizontalMultiBrowseCarousel
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.ListItem
import androidx.compose.material3.LoadingIndicator
import androidx.compose.material3.MaterialExpressiveTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.MotionScheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.ToggleButton
import androidx.compose.material3.ToggleFloatingActionButton
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.carousel.rememberCarouselState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.delay

// =============================================================================
// Data Models
// =============================================================================

data class FeaturedItem(
    val id: Int,
    val title: String,
    val subtitle: String,
    val icon: ImageVector
)

data class ContentItem(
    val id: Int,
    val title: String,
    val description: String,
    var isFavorite: Boolean = false
)

// =============================================================================
// Complete Screen
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class, ExperimentalMaterial3Api::class)
@Composable
fun CompleteExpressiveScreen() {
    // State
    var isLoading by remember { mutableStateOf(true) }
    var fabExpanded by remember { mutableStateOf(false) }
    var viewMode by remember { mutableIntStateOf(0) } // 0: List, 1: Grid

    val featuredItems = remember {
        listOf(
            FeaturedItem(1, "Featured 1", "Explore now", Icons.Default.Star),
            FeaturedItem(2, "Featured 2", "New arrival", Icons.Default.Notifications),
            FeaturedItem(3, "Featured 3", "Popular", Icons.Default.Favorite),
            FeaturedItem(4, "Featured 4", "Recommended", Icons.Default.Person)
        )
    }

    val contentItems = remember {
        mutableStateListOf(
            ContentItem(1, "Article 1", "Description for article 1"),
            ContentItem(2, "Article 2", "Description for article 2"),
            ContentItem(3, "Article 3", "Description for article 3"),
            ContentItem(4, "Article 4", "Description for article 4"),
            ContentItem(5, "Article 5", "Description for article 5"),
            ContentItem(6, "Article 6", "Description for article 6"),
            ContentItem(7, "Article 7", "Description for article 7"),
            ContentItem(8, "Article 8", "Description for article 8")
        )
    }

    // Simulate loading
    LaunchedEffect(Unit) {
        delay(2000)
        isLoading = false
    }

    val scrollBehavior = TopAppBarDefaults.pinnedScrollBehavior()

    Scaffold(
        modifier = Modifier.nestedScroll(scrollBehavior.nestedScrollConnection),
        topBar = {
            CenterAlignedTopAppBar(
                title = { Text("M3 Expressive") },
                actions = {
                    IconButton(onClick = { }) {
                        Icon(Icons.Default.Search, contentDescription = "Search")
                    }
                    IconButton(onClick = { }) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings")
                    }
                },
                scrollBehavior = scrollBehavior
            )
        },
        floatingActionButton = {
            FloatingActionButtonMenu(
                expanded = fabExpanded,
                button = {
                    ToggleFloatingActionButton(
                        checked = fabExpanded,
                        onCheckedChange = { fabExpanded = it }
                    ) {
                        AnimatedContent(
                            targetState = fabExpanded,
                            transitionSpec = {
                                fadeIn(tween(200)) togetherWith fadeOut(tween(200))
                            },
                            label = "FAB icon"
                        ) { expanded ->
                            Icon(
                                imageVector = if (expanded) Icons.Default.Close else Icons.Default.Add,
                                contentDescription = null
                            )
                        }
                    }
                }
            ) {
                FloatingActionButtonMenuItem(
                    onClick = { fabExpanded = false },
                    icon = { Icon(Icons.Default.Edit, null) },
                    text = { Text("New Post") }
                )
                FloatingActionButtonMenuItem(
                    onClick = { fabExpanded = false },
                    icon = { Icon(Icons.Default.Share, null) },
                    text = { Text("Share") }
                )
            }
        }
    ) { paddingValues ->
        if (isLoading) {
            LoadingScreen()
        } else {
            MainContent(
                paddingValues = paddingValues,
                featuredItems = featuredItems,
                contentItems = contentItems,
                viewMode = viewMode,
                onViewModeChange = { viewMode = it },
                onFavoriteToggle = { item ->
                    val index = contentItems.indexOfFirst { it.id == item.id }
                    if (index >= 0) {
                        contentItems[index] = item.copy(isFavorite = !item.isFavorite)
                    }
                }
            )
        }
    }
}

// =============================================================================
// Loading Screen
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
private fun LoadingScreen() {
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

// =============================================================================
// Main Content
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
private fun MainContent(
    paddingValues: PaddingValues,
    featuredItems: List<FeaturedItem>,
    contentItems: List<ContentItem>,
    viewMode: Int,
    onViewModeChange: (Int) -> Unit,
    onFavoriteToggle: (ContentItem) -> Unit
) {
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(paddingValues),
        contentPadding = PaddingValues(bottom = 88.dp)
    ) {
        // Featured Carousel
        item {
            FeaturedCarousel(items = featuredItems)
        }

        // View Mode Selector
        item {
            ViewModeSelector(
                selectedMode = viewMode,
                onModeChange = onViewModeChange
            )
        }

        // Content List
        item {
            Text(
                text = "Recent Articles",
                style = MaterialTheme.typography.titleLarge,
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
            )
        }

        items(contentItems, key = { it.id }) { item ->
            ContentListItem(
                item = item,
                onFavoriteToggle = { onFavoriteToggle(item) }
            )
            HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp))
        }
    }
}

// =============================================================================
// Featured Carousel
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
private fun FeaturedCarousel(items: List<FeaturedItem>) {
    Column(
        modifier = Modifier.padding(vertical = 16.dp)
    ) {
        Text(
            text = "Featured",
            style = MaterialTheme.typography.titleLarge,
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
        )

        HorizontalMultiBrowseCarousel(
            state = rememberCarouselState { items.count() },
            modifier = Modifier
                .fillMaxWidth()
                .height(160.dp),
            preferredItemWidth = 200.dp,
            itemSpacing = 12.dp,
            contentPadding = PaddingValues(horizontal = 16.dp)
        ) { index ->
            val item = items[index]
            FeaturedCard(item = item)
        }
    }
}

@Composable
private fun FeaturedCard(item: FeaturedItem) {
    Card(
        modifier = Modifier.fillMaxSize(),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.primaryContainer
        )
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            Icon(
                imageVector = item.icon,
                contentDescription = null,
                modifier = Modifier.size(32.dp),
                tint = MaterialTheme.colorScheme.onPrimaryContainer
            )

            Column {
                Text(
                    text = item.title,
                    style = MaterialTheme.typography.titleMedium,
                    color = MaterialTheme.colorScheme.onPrimaryContainer
                )
                Text(
                    text = item.subtitle,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onPrimaryContainer.copy(alpha = 0.7f)
                )
            }
        }
    }
}

// =============================================================================
// View Mode Selector
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
private fun ViewModeSelector(
    selectedMode: Int,
    onModeChange: (Int) -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = "View Mode",
            style = MaterialTheme.typography.titleSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )

        ButtonGroup(
            spacing = ButtonGroupDefaults.ConnectedSpacing
        ) {
            ToggleButton(
                checked = selectedMode == 0,
                onCheckedChange = { if (it) onModeChange(0) },
                shape = ButtonGroupDefaults.connectedLeadingButtonShape
            ) {
                Icon(Icons.Default.List, contentDescription = "List view")
                Spacer(modifier = Modifier.width(4.dp))
                Text("List")
            }
            ToggleButton(
                checked = selectedMode == 1,
                onCheckedChange = { if (it) onModeChange(1) },
                shape = ButtonGroupDefaults.connectedTrailingButtonShape
            ) {
                Icon(Icons.Default.GridView, contentDescription = "Grid view")
                Spacer(modifier = Modifier.width(4.dp))
                Text("Grid")
            }
        }
    }
}

// =============================================================================
// Content List Item
// =============================================================================

@Composable
private fun ContentListItem(
    item: ContentItem,
    onFavoriteToggle: () -> Unit
) {
    ListItem(
        headlineContent = {
            Text(
                text = item.title,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        },
        supportingContent = {
            Text(
                text = item.description,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis
            )
        },
        leadingContent = {
            Icon(
                imageVector = Icons.Default.Star,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.primary
            )
        },
        trailingContent = {
            IconButton(onClick = onFavoriteToggle) {
                Icon(
                    imageVector = if (item.isFavorite)
                        Icons.Filled.Favorite
                    else
                        Icons.Outlined.FavoriteBorder,
                    contentDescription = if (item.isFavorite)
                        "Remove from favorites"
                    else
                        "Add to favorites",
                    tint = if (item.isFavorite)
                        MaterialTheme.colorScheme.error
                    else
                        MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    )
}

// =============================================================================
// Preview
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun CompleteExpressiveScreenPreview() {
    MaterialExpressiveTheme(
        motionScheme = MotionScheme.expressive()
    ) {
        CompleteExpressiveScreen()
    }
}

// =============================================================================
// Usage Notes
// =============================================================================

/*
この完全な画面例には以下のコンポーネントが含まれています：

1. MaterialExpressiveTheme
   - motionScheme = MotionScheme.expressive()

2. LoadingIndicator
   - シェイプモーフィングによるローディング表示

3. HorizontalMultiBrowseCarousel
   - フィーチャードアイテムの表示

4. ButtonGroup
   - ビューモード切り替え（List/Grid）

5. FloatingActionButtonMenu
   - 展開式FABメニュー

6. ListItem
   - コンテンツリスト

7. IconToggleButton (Favorite)
   - シェイプモーフィング付きトグル

使用手順：
1. @OptIn(ExperimentalMaterial3ExpressiveApi::class) を追加
2. MaterialExpressiveTheme でラップ
3. 必要なコンポーネントをインポート
*/
