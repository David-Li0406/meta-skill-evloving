# Material 3 Expressive Loading Indicators

LoadingIndicator と ContainedLoadingIndicator の実装ガイド。

## Overview

Material 3 Expressive では、従来の `CircularProgressIndicator` に代わる新しいローディングコンポーネントを提供しています。
これらは流動的なシェイプモーフィングアニメーションを特徴とし、より魅力的なユーザー体験を実現します。

## コンポーネント比較

| コンポーネント | 特徴 | 用途 |
|--------------|------|------|
| `LoadingIndicator` | シェイプがモーフィングするローディング | 一般的なローディング表示 |
| `ContainedLoadingIndicator` | コンテナ内でモーフィング | カード内、ボタン内のローディング |
| `CircularProgressIndicator` | 従来の円形インジケーター | 後方互換性が必要な場合 |

## 基本的な使用法

### LoadingIndicator

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun BasicLoadingIndicator() {
    LoadingIndicator()
}
```

### ContainedLoadingIndicator

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun BasicContainedLoadingIndicator() {
    ContainedLoadingIndicator()
}
```

## カスタマイズ

### 色のカスタマイズ

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ColoredLoadingIndicator() {
    // 基本
    LoadingIndicator(
        color = MaterialTheme.colorScheme.tertiary
    )

    // コンテナ付き
    ContainedLoadingIndicator(
        indicatorColor = MaterialTheme.colorScheme.primary,
        containerColor = MaterialTheme.colorScheme.primaryContainer
    )
}
```

### サイズのカスタマイズ

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun SizedLoadingIndicators() {
    // 小さいサイズ
    LoadingIndicator(
        modifier = Modifier.size(24.dp)
    )

    // 標準サイズ
    LoadingIndicator(
        modifier = Modifier.size(48.dp)
    )

    // 大きいサイズ
    LoadingIndicator(
        modifier = Modifier.size(64.dp)
    )
}
```

## 使用パターン

### 画面全体のローディング

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun FullScreenLoading(isLoading: Boolean) {
    if (isLoading) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(MaterialTheme.colorScheme.background),
            contentAlignment = Alignment.Center
        ) {
            LoadingIndicator(
                modifier = Modifier.size(64.dp)
            )
        }
    }
}
```

### ボタン内のローディング

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun LoadingButton(
    onClick: () -> Unit,
    isLoading: Boolean,
    text: String
) {
    Button(
        onClick = onClick,
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
        Text(text)
    }
}
```

### カード内のローディング

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun LoadingCard(isLoading: Boolean) {
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
                // Content
                Text("Content loaded")
            }
        }
    }
}
```

### Pull to Refresh との統合

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class, ExperimentalMaterial3Api::class)
@Composable
fun PullToRefreshExample() {
    var isRefreshing by remember { mutableStateOf(false) }
    val state = rememberPullToRefreshState()

    Box(
        modifier = Modifier.nestedScroll(state.nestedScrollConnection)
    ) {
        LazyColumn(
            modifier = Modifier.fillMaxSize()
        ) {
            items(20) { index ->
                Text(
                    text = "Item $index",
                    modifier = Modifier.padding(16.dp)
                )
            }
        }

        PullToRefreshContainer(
            state = state,
            modifier = Modifier.align(Alignment.TopCenter),
            indicator = {
                // LoadingIndicator を使用
                LoadingIndicator(
                    modifier = Modifier.size(32.dp)
                )
            }
        )
    }
}
```

## 状態管理パターン

### UiState との統合

```kotlin
sealed interface UiState<out T> {
    data object Loading : UiState<Nothing>
    data class Success<T>(val data: T) : UiState<T>
    data class Error(val message: String) : UiState<Nothing>
}

@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun <T> StateAwareContent(
    state: UiState<T>,
    content: @Composable (T) -> Unit
) {
    when (state) {
        is UiState.Loading -> {
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                LoadingIndicator()
            }
        }
        is UiState.Success -> content(state.data)
        is UiState.Error -> {
            Text(
                text = state.message,
                color = MaterialTheme.colorScheme.error
            )
        }
    }
}
```

## アクセシビリティ

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun AccessibleLoadingIndicator() {
    LoadingIndicator(
        modifier = Modifier.semantics {
            contentDescription = "Loading content, please wait"
            // または日本語
            // contentDescription = "コンテンツを読み込み中です。お待ちください"
        }
    )
}
```

## アニメーションの挙動

LoadingIndicator は以下のようなアニメーションを行います：

1. **Shape Morphing**: 複数のシェイプ間でスムーズに変形
2. **Continuous Animation**: 表示されている間、継続的にアニメーション
3. **Spring Physics**: MotionScheme に基づくスプリングアニメーション

## ベストプラクティス

### 1. 適切なサイズを選択

| コンテキスト | 推奨サイズ |
|-------------|-----------|
| インラインテキスト横 | 16-20dp |
| ボタン内 | 20-24dp |
| カード/コンテナ内 | 32-48dp |
| 画面中央 | 48-64dp |

### 2. 一貫した使用

アプリ全体で同じローディングコンポーネントを使用：

```kotlin
// Good: 共通のローディングコンポーネント
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun AppLoadingIndicator(
    modifier: Modifier = Modifier,
    size: LoadingIndicatorSize = LoadingIndicatorSize.Medium
) {
    val indicatorSize = when (size) {
        LoadingIndicatorSize.Small -> 24.dp
        LoadingIndicatorSize.Medium -> 48.dp
        LoadingIndicatorSize.Large -> 64.dp
    }

    LoadingIndicator(
        modifier = modifier.size(indicatorSize),
        color = MaterialTheme.colorScheme.primary
    )
}

enum class LoadingIndicatorSize { Small, Medium, Large }
```

### 3. ローディング時間の考慮

- 5秒以下の短い待機: `LoadingIndicator` 推奨
- 長時間の処理: プログレスバーまたはパーセント表示を検討

## 関連リソース

- [Motion System](motion-system.md) - アニメーション設定
- [Theming](theming.md) - カラーカスタマイズ
- [examples/loading-indicator-example.kt](../examples/loading-indicator-example.kt) - 実装例
