---
name: new-screen
description: Scaffold a new Jetpack Compose screen following project patterns. Use when creating a new screen or view in the app.
allowed-tools: Read, Write, Edit, Glob
---

# New Screen Skill

Create a new Jetpack Compose screen following MateDroid's patterns.

## Project Structure

Screens are located in `app/src/main/java/com/matedroid/ui/screens/`:
```
screens/
├── dashboard/
│   └── DashboardScreen.kt
├── drives/
│   ├── DrivesScreen.kt
│   └── DriveDetailScreen.kt
├── charges/
│   ├── ChargesScreen.kt
│   └── ChargeDetailScreen.kt
├── settings/
│   └── SettingsScreen.kt
└── {feature}/
    └── {Feature}Screen.kt
```

## Process

1. Ask the user for:
   - Screen name (e.g., "Battery Health")
   - Brief description of what it displays
   - Whether it needs navigation parameters

2. Read an existing screen as reference (e.g., `DashboardScreen.kt`)

3. Create the new screen file following the pattern

## Screen Template

```kotlin
package com.matedroid.ui.screens.{feature}

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import com.matedroid.R

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun {Feature}Screen(
    onNavigateBack: () -> Unit,
    modifier: Modifier = Modifier
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(stringResource(R.string.{feature}_title)) },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = stringResource(R.string.back)
                        )
                    }
                }
            )
        }
    ) { paddingValues ->
        Column(
            modifier = modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp)
        ) {
            // Screen content here
        }
    }
}
```

## After Creating the Screen

1. Add string resources for the screen title using the translate skill
2. Add navigation route to the app's navigation graph
3. Remind the user to wire up the navigation

## Common Patterns

### Loading State
```kotlin
var isLoading by remember { mutableStateOf(true) }

if (isLoading) {
    CircularProgressIndicator()
} else {
    // Content
}
```

### API Data Fetching
```kotlin
LaunchedEffect(Unit) {
    // Fetch data from TeslamateApiService
}
```

### Pull to Refresh
```kotlin
val pullRefreshState = rememberPullToRefreshState()
PullToRefreshBox(state = pullRefreshState, isRefreshing = isRefreshing) {
    // Content
}
```

### Cards
```kotlin
Card(
    modifier = Modifier.fillMaxWidth(),
    colors = CardDefaults.cardColors(
        containerColor = MaterialTheme.colorScheme.surfaceVariant
    )
) {
    // Card content
}
```
