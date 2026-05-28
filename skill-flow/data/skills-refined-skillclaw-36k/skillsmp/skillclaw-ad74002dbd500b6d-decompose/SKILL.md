---
name: decompose
description: Use this skill for implementing a component-based architecture with lifecycle management and navigation in Kotlin Multiplatform (KMP).
---

# Decompose for Kotlin Multiplatform

This skill provides guidance on setting up and using the Decompose library for KMP, focusing on component architecture, lifecycle management, and navigation.

## Setup

### libs.versions.toml

```toml
[versions]
decompose = "3.5.0"
essenty = "2.5.0"

[libraries]
decompose = { module = "com.arkivanov.decompose:decompose", version.ref = "decompose" }
decompose-compose = { module = "com.arkivanov.decompose:extensions-compose", version.ref = "decompose" }
essenty-lifecycle = { module = "com.arkivanov.essenty:lifecycle", version.ref = "essenty" }
```

### build.gradle.kts

```kotlin
commonMain.dependencies {
    implementation(libs.decompose)
    implementation(libs.decompose.compose)
    implementation(libs.essenty.lifecycle)
    implementation(libs.kotlinx.serialization.json)
}
```

## Core Concepts

### Component

A component serves as a business logic container with a lifecycle, designed to be UI-agnostic.

```kotlin
// Interface (public API)
interface HomeComponent {
    val state: Value<HomeState>
    fun onItemClick(item: HomeItem)
    fun onRefresh()
}

// Implementation
class DefaultHomeComponent(
    componentContext: ComponentContext,
    private val repository: HomeRepository,
    private val onNavigateToDetails: (itemId: String) -> Unit
) : HomeComponent, ComponentContext by componentContext {

    private val _state = MutableValue<HomeState>(HomeState.Loading)
    override val state: Value<HomeState> = _state

    private val scope = componentScope()

    init {
        loadData()
    }

    private fun loadData() {
        scope.launch {
            _state.value = HomeState.Loading
            repository.getItems()
                .onSuccess { items ->
                    _state.value = HomeState.Success(items)
                }
                .onError { message, _ ->
                    _state.value = HomeState.Error(message)
                }
        }
    }

    override fun onItemClick(item: HomeItem) {
        onNavigateToDetails(item.id)
    }

    override fun onRefresh() {
        loadData()
    }
}

sealed class HomeState {
    data object Loading : HomeState()
    data class Success(val items: List<HomeItem>) : HomeState()
    data class Error(val message: String) : HomeState()
}
```

### ComponentContext

The `ComponentContext` provides lifecycle management, state preservation, and child component management.

```kotlin
class MyComponent(
    componentContext: ComponentContext
) : ComponentContext by componentContext {
    // Implementation details...
}
```