---
name: voyager-to-navigation3
description: Use this skill when you need to convert Voyager Screens to Composable functions and NavKeys for Navigation 3.
---

# Skill body

## Task Background
The project currently uses Voyager (cafe.adriel.voyager:voyager-navigator) as the navigation framework, and you want to replace it with Navigation 3 (androidx.navigation3:navigation3-runtime).

## Task Content
You need to refactor all classes that inherit from `cafe.adriel.voyager.core.screen.Screen` or `com.zhangke.fread.common.page.BaseScreen` into Composable functions and corresponding NavKeys.

### Example Transformation
Given a Screen like this:
```kotlin
class ProfileScreen : BaseScreen() {
    @Composable
    override fun Content() {
        super.Content()
        val viewModel = getViewModel<ProfileHomeViewModel>()
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(MaterialTheme.colors.background),
        ) {
            Text(text = "Profile Screen")
        }
    }
}
```
Transform it to:
```kotlin
object ProfileScreenKey: NavKey

@Composable
fun ProfileScreen(viewModel: ProfileHomeViewModel) {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colors.background),
    ) {
        Text(text = "Profile Screen")
    }
}
```
If the Screen has parameters, the key should also include parameters:
```kotlin
data class DetailScreenKey(val itemId: String) : NavKey

@Composable
fun DetailScreen(viewModel: DetailViewModel) {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colors.background),
    ) {
        Text(text = "Detail Screen for item: $itemId")
    }
}
```

### Registration
Register the new NavKey in the current module's NavEntryProvider:
```kotlin
class ProfileNavEntryProvider : NavEntryProvider {
    override fun EntryProviderScope<NavKey>.build() {
        entry<ProfileScreenKey> {
            ProfileScreen(koinViewModel())
        }
        entry<CreatePlanScreenNavKey> { key ->
            CreatePlanScreen(koinViewModel { parametersOf(key.lexicon) })
        }
    }

    override fun PolymorphicModuleBuilder<NavKey>.polymorph() {
        subclass(ProfileScreenKey::class)
        subclass(CreatePlanScreenNavKey::class)
    }
}
```

## Workflow
1. Identify all Screens in the given module that:
   - Inherit from `cafe.adriel.voyager.core.screen.Screen` or `com.zhangke.fread.common.page.BaseScreen`
   - Do not contain any nested Navigators
2. List these Screens and output them to the console.
3. Refactor each identified Screen:
   - Create a NavKey for each Screen.
   - Convert the Screen to a Composable function.
4. Update navigation calls to use `LocalNavBackStack.currentOrThrow` instead of `LocalNavigator.currentOrThrow` and navigate using the NavKey.

### Notes
- Do not modify abstract classes or any other code outside the specified Screens and Navigation 3 related code.
- Ignore any nested Navigator pages or other cases that do not meet the criteria.