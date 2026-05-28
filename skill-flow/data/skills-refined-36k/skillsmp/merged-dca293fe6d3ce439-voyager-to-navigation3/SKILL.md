---
name: voyager-to-navigation3
description: Use this skill when you need to convert Voyager Screens to Composable functions and NavKeys for navigation3.
---

## 任务背景
目前项目中使用了 Voyager(cafe.adriel.voyager:voyager-navigator) 作为导航框架，现在我希望将 Voyager 替换成 navigation3(androidx.navigation3:navigation3-runtime)。

## 任务内容
你需要将所有继承自 `cafe.adriel.voyager.core.screen.Screen` 或者 `com.zhangke.fread.common.page.BaseScreen` 的类改成 Composable 函数，并新增对应的 NavKey。

### 示例
对于一个 Screen 类：
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
你需要改成如下方式，并新增一个 NavKey：
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
如果页面有参数，NavKey 也应带参数：
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

### 注册 NavKey
将新增的 NavKey 注册到当前模块的 NavEntryProvider 中，例如：
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

### 工作流程
1. 找到给定模块中所有符合条件的 Screen：
   - 继承自 `cafe.adriel.voyager.core.screen.Screen` 或 `com.zhangke.fread.common.page.BaseScreen`
   - 不包含任何嵌套 Navigator
2. 列出并输出符合条件的 Screen 到控制台。
3. 逐个重构这些 Screen。
4. 为每个 Screen 创建 NavKey，并将其改为 Composable 函数。
5. 对于使用了 `navigationResult` 的地方保持不动。
6. 将 NavKey 和 Composable 函数注册到模块的 NavEntryProvider 中。
7. 找到相关引用并将跳转处改为 NavKey。
8. 结束当前 Screen 的重构，进入下一个 Screen。
9. 直到所有符合条件的 Screen 重构完成。

## 绝对禁止
以下内容为绝对禁止修改的规则：
1. 对于已经修改完成的类请不要再改。
2. 只修改 Screen 和 navigation3 相关的代码，其他代码不做改动。
3. 不修改任何 Tab 及其直接引用的页面。
4. 遇到不属于上述情况的页面请直接忽略。
5. 不要求改任何嵌套的 Navigator 页面，遇到嵌套情况直接跳过。
6. 不做任何超出要求的事情。