/**
 * Material 3 Expressive - Floating Toolbar Examples
 *
 * HorizontalFloatingToolbar, VerticalFloatingToolbar, FlexibleBottomAppBar の使用例。
 */

package com.example.m3expressive.examples

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.ContentCopy
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material.icons.filled.MyLocation
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Share
import androidx.compose.material.icons.filled.ZoomIn
import androidx.compose.material.icons.filled.ZoomOut
import androidx.compose.material3.BottomAppBarDefaults
import androidx.compose.material3.ExperimentalMaterial3ExpressiveApi
import androidx.compose.material3.FabPosition
import androidx.compose.material3.FlexibleBottomAppBar
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.FloatingActionButtonDefaults
import androidx.compose.material3.FloatingToolbarDefaults
import androidx.compose.material3.HorizontalFloatingToolbar
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialExpressiveTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.VerticalFloatingToolbar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.runtime.snapshotFlow
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp

// =============================================================================
// Basic Horizontal Floating Toolbar
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun BasicHorizontalToolbar() {
    var expanded by remember { mutableStateOf(true) }

    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            text = "Horizontal Floating Toolbar",
            style = MaterialTheme.typography.titleMedium
        )

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
}

// =============================================================================
// Vibrant Horizontal Toolbar
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun VibrantHorizontalToolbar() {
    var expanded by remember { mutableStateOf(true) }

    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            text = "Vibrant Toolbar",
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
        }
    }
}

// =============================================================================
// Vertical Floating Toolbar
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun BasicVerticalToolbar() {
    var expanded by remember { mutableStateOf(true) }

    Column(
        modifier = Modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            text = "Vertical Floating Toolbar",
            style = MaterialTheme.typography.titleMedium
        )

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.End
        ) {
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
}

// =============================================================================
// Toolbar in Scaffold
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ToolbarInScaffold() {
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
        LazyColumn(
            modifier = Modifier.padding(paddingValues),
            contentPadding = androidx.compose.foundation.layout.PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(30) { index ->
                Text(
                    text = "Item ${index + 1}",
                    modifier = Modifier.padding(16.dp)
                )
            }
        }
    }
}

// =============================================================================
// Scroll-Aware Toolbar
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ScrollAwareToolbar() {
    val listState = rememberLazyListState()
    var toolbarExpanded by remember { mutableStateOf(true) }

    // スクロール方向を監視
    val isScrollingDown by remember {
        derivedStateOf {
            listState.firstVisibleItemScrollOffset > 0
        }
    }

    LaunchedEffect(listState) {
        snapshotFlow { listState.firstVisibleItemIndex to listState.firstVisibleItemScrollOffset }
            .collect { (index, offset) ->
                toolbarExpanded = index == 0 && offset < 100
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
                IconButton(onClick = { }) {
                    Icon(Icons.Default.Share, contentDescription = "Share")
                }
            }
        }
    ) { paddingValues ->
        LazyColumn(
            state = listState,
            modifier = Modifier.padding(paddingValues),
            contentPadding = androidx.compose.foundation.layout.PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(50) { index ->
                Text(
                    text = "Item ${index + 1}",
                    modifier = Modifier.padding(16.dp)
                )
            }
        }
    }
}

// =============================================================================
// Flexible Bottom App Bar
// =============================================================================

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
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues),
            contentAlignment = Alignment.Center
        ) {
            Text("Main Content")
        }
    }
}

// =============================================================================
// Flexible Bottom App Bar with FAB
// =============================================================================

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
        LazyColumn(
            modifier = Modifier.padding(paddingValues),
            contentPadding = androidx.compose.foundation.layout.PaddingValues(16.dp)
        ) {
            items(30) { index ->
                Text(
                    text = "Item ${index + 1}",
                    modifier = Modifier.padding(16.dp)
                )
            }
        }
    }
}

// =============================================================================
// Contextual Toolbar
// =============================================================================

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ContextualToolbarExample() {
    var selectedCount by remember { mutableIntStateOf(0) }

    Box(modifier = Modifier.fillMaxSize()) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = "Contextual Toolbar",
                style = MaterialTheme.typography.titleMedium
            )

            Text(
                text = "Selected: $selectedCount items",
                style = MaterialTheme.typography.bodySmall
            )

            Row(
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                androidx.compose.material3.Button(
                    onClick = { selectedCount++ }
                ) {
                    Text("Select")
                }
                androidx.compose.material3.Button(
                    onClick = { selectedCount = 0 }
                ) {
                    Text("Clear")
                }
            }
        }

        // Contextual toolbar
        AnimatedVisibility(
            visible = selectedCount > 0,
            modifier = Modifier.align(Alignment.BottomCenter),
            enter = slideInVertically(initialOffsetY = { it }),
            exit = slideOutVertically(targetOffsetY = { it })
        ) {
            HorizontalFloatingToolbar(
                expanded = true,
                modifier = Modifier.padding(16.dp),
                floatingActionButton = {
                    IconButton(onClick = { selectedCount = 0 }) {
                        Icon(Icons.Default.Close, contentDescription = "Dismiss")
                    }
                }
            ) {
                Text(
                    text = "$selectedCount selected",
                    modifier = Modifier.padding(horizontal = 16.dp)
                )
                Spacer(modifier = Modifier.weight(1f))
                IconButton(onClick = { }) {
                    Icon(Icons.Default.Share, contentDescription = "Share")
                }
                IconButton(onClick = { }) {
                    Icon(Icons.Default.ContentCopy, contentDescription = "Copy")
                }
                IconButton(onClick = { }) {
                    Icon(Icons.Default.Delete, contentDescription = "Delete")
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
private fun BasicHorizontalToolbarPreview() {
    MaterialExpressiveTheme {
        BasicHorizontalToolbar()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun VibrantHorizontalToolbarPreview() {
    MaterialExpressiveTheme {
        VibrantHorizontalToolbar()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun BasicVerticalToolbarPreview() {
    MaterialExpressiveTheme {
        BasicVerticalToolbar()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun BasicFlexibleBottomAppBarPreview() {
    MaterialExpressiveTheme {
        BasicFlexibleBottomAppBar()
    }
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Preview(showBackground = true)
@Composable
private fun ContextualToolbarPreview() {
    MaterialExpressiveTheme {
        ContextualToolbarExample()
    }
}
