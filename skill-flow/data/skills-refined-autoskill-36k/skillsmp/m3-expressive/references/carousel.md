# Material 3 Expressive Carousel

MultiBrowseCarousel, HorizontalCenteredHeroCarousel の実装ガイド。

## Overview

Carousel は水平方向にスクロールするコンテンツ表示コンポーネントです。
Material 3 Expressive では複数のカルーセルバリエーションが提供されています。

| コンポーネント | 説明 | 用途 |
|--------------|------|------|
| `HorizontalMultiBrowseCarousel` | 複数アイテム同時表示 | 商品一覧、画像ギャラリー |
| `HorizontalCenteredHeroCarousel` | 中央にヒーローアイテム | フィーチャー表示、ハイライト |
| `HorizontalUncontainedCarousel` | 画面端まで広がるカルーセル | フルワイド表示 |

## HorizontalMultiBrowseCarousel

### 基本的な使用法

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun BasicMultiBrowseCarousel() {
    val items = listOf("Item 1", "Item 2", "Item 3", "Item 4", "Item 5")

    HorizontalMultiBrowseCarousel(
        state = rememberCarouselState { items.count() },
        modifier = Modifier
            .fillMaxWidth()
            .height(200.dp),
        preferredItemWidth = 150.dp,
        itemSpacing = 8.dp
    ) { index ->
        Card(
            modifier = Modifier
                .fillMaxSize()
                .maskClip(MaterialTheme.shapes.medium)
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
```

### 画像カルーセル

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ImageCarousel(images: List<String>) {
    HorizontalMultiBrowseCarousel(
        state = rememberCarouselState { images.count() },
        modifier = Modifier
            .fillMaxWidth()
            .height(240.dp),
        preferredItemWidth = 280.dp,
        itemSpacing = 12.dp
    ) { index ->
        Card(
            modifier = Modifier
                .fillMaxSize()
                .maskClip(MaterialTheme.shapes.large)
        ) {
            AsyncImage(
                model = images[index],
                contentDescription = "Image ${index + 1}",
                modifier = Modifier.fillMaxSize(),
                contentScale = ContentScale.Crop
            )
        }
    }
}
```

## HorizontalCenteredHeroCarousel

### 基本的な使用法

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun BasicHeroCarousel() {
    val items = listOf("Hero 1", "Hero 2", "Hero 3")

    HorizontalCenteredHeroCarousel(
        state = rememberCarouselState { items.count() },
        modifier = Modifier
            .fillMaxWidth()
            .height(300.dp),
        itemWidth = 280.dp,
        itemSpacing = 16.dp
    ) { index ->
        Card(
            modifier = Modifier
                .fillMaxSize()
                .maskClip(MaterialTheme.shapes.large),
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
```

### フィーチャーカード

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun FeatureCarousel(features: List<Feature>) {
    HorizontalCenteredHeroCarousel(
        state = rememberCarouselState { features.count() },
        modifier = Modifier
            .fillMaxWidth()
            .height(320.dp),
        itemWidth = 300.dp,
        itemSpacing = 16.dp
    ) { index ->
        val feature = features[index]

        Card(
            modifier = Modifier
                .fillMaxSize()
                .maskClip(MaterialTheme.shapes.extraLarge)
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
                        style = MaterialTheme.typography.headlineSmall
                    )
                    Spacer(modifier = Modifier.height(8.dp))
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

data class Feature(
    val icon: ImageVector,
    val title: String,
    val description: String
)
```

## HorizontalUncontainedCarousel

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun UncontainedCarousel() {
    val items = (1..10).toList()

    HorizontalUncontainedCarousel(
        state = rememberCarouselState { items.count() },
        modifier = Modifier
            .fillMaxWidth()
            .height(180.dp),
        itemWidth = 120.dp,
        itemSpacing = 8.dp
    ) { index ->
        Card(
            modifier = Modifier
                .fillMaxSize()
                .maskClip(MaterialTheme.shapes.medium)
        ) {
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                Text("${items[index]}")
            }
        }
    }
}
```

## カルーセル状態管理

### 現在のアイテム取得

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun CarouselWithIndicator() {
    val items = listOf("A", "B", "C", "D", "E")
    val carouselState = rememberCarouselState { items.count() }

    Column {
        HorizontalMultiBrowseCarousel(
            state = carouselState,
            modifier = Modifier
                .fillMaxWidth()
                .height(200.dp),
            preferredItemWidth = 150.dp
        ) { index ->
            Card(modifier = Modifier.fillMaxSize()) {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Text(items[index])
                }
            }
        }

        // ページインジケーター
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.Center
        ) {
            items.forEachIndexed { index, _ ->
                val isSelected = carouselState.currentPage == index
                Box(
                    modifier = Modifier
                        .padding(4.dp)
                        .size(if (isSelected) 10.dp else 8.dp)
                        .background(
                            color = if (isSelected)
                                MaterialTheme.colorScheme.primary
                            else
                                MaterialTheme.colorScheme.outline,
                            shape = CircleShape
                        )
                )
            }
        }
    }
}
```

### プログラムでスクロール

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ControlledCarousel() {
    val items = (1..10).toList()
    val carouselState = rememberCarouselState { items.count() }
    val coroutineScope = rememberCoroutineScope()

    Column {
        HorizontalMultiBrowseCarousel(
            state = carouselState,
            modifier = Modifier
                .fillMaxWidth()
                .height(200.dp),
            preferredItemWidth = 150.dp
        ) { index ->
            Card(modifier = Modifier.fillMaxSize()) {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Text("Item ${items[index]}")
                }
            }
        }

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceEvenly
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
                Text("Previous")
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
```

## 自動スクロール

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun AutoScrollCarousel() {
    val items = (1..5).toList()
    val carouselState = rememberCarouselState { items.count() }

    // 自動スクロール
    LaunchedEffect(Unit) {
        while (true) {
            delay(3000L)
            val nextPage = (carouselState.currentPage + 1) % items.count()
            carouselState.animateScrollToItem(nextPage)
        }
    }

    HorizontalCenteredHeroCarousel(
        state = carouselState,
        modifier = Modifier
            .fillMaxWidth()
            .height(200.dp),
        itemWidth = 280.dp
    ) { index ->
        Card(
            modifier = Modifier
                .fillMaxSize()
                .maskClip(MaterialTheme.shapes.large)
        ) {
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                Text("Slide ${items[index]}")
            }
        }
    }
}
```

## クリック処理

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ClickableCarousel(
    items: List<Product>,
    onItemClick: (Product) -> Unit
) {
    HorizontalMultiBrowseCarousel(
        state = rememberCarouselState { items.count() },
        modifier = Modifier
            .fillMaxWidth()
            .height(220.dp),
        preferredItemWidth = 160.dp,
        itemSpacing = 12.dp
    ) { index ->
        val product = items[index]

        Card(
            onClick = { onItemClick(product) },
            modifier = Modifier
                .fillMaxSize()
                .maskClip(MaterialTheme.shapes.medium)
        ) {
            Column(
                modifier = Modifier.fillMaxSize()
            ) {
                AsyncImage(
                    model = product.imageUrl,
                    contentDescription = product.name,
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(1f),
                    contentScale = ContentScale.Crop
                )
                Text(
                    text = product.name,
                    modifier = Modifier.padding(12.dp),
                    style = MaterialTheme.typography.bodyMedium,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
        }
    }
}

data class Product(
    val id: String,
    val name: String,
    val imageUrl: String
)
```

## アクセシビリティ

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun AccessibleCarousel(items: List<String>) {
    HorizontalMultiBrowseCarousel(
        state = rememberCarouselState { items.count() },
        modifier = Modifier
            .fillMaxWidth()
            .height(200.dp)
            .semantics {
                contentDescription = "Image carousel, ${items.count()} items"
            },
        preferredItemWidth = 150.dp
    ) { index ->
        Card(
            modifier = Modifier
                .fillMaxSize()
                .semantics {
                    contentDescription = "Item ${index + 1} of ${items.count()}: ${items[index]}"
                }
        ) {
            Text(items[index])
        }
    }
}
```

## ベストプラクティス

### 1. 適切なカルーセルタイプの選択

| ユースケース | 推奨タイプ |
|-------------|-----------|
| 商品一覧 | `HorizontalMultiBrowseCarousel` |
| フィーチャーハイライト | `HorizontalCenteredHeroCarousel` |
| 画像ギャラリー | `HorizontalMultiBrowseCarousel` |
| バナー表示 | `HorizontalCenteredHeroCarousel` |

### 2. アイテム数

- 最低 3 個以上を推奨
- 多すぎる場合はページネーションを検討

### 3. パフォーマンス

```kotlin
// Good: maskClip を使用
Card(
    modifier = Modifier
        .fillMaxSize()
        .maskClip(MaterialTheme.shapes.medium)
) { }

// 画像の最適化
AsyncImage(
    model = ImageRequest.Builder(LocalContext.current)
        .data(imageUrl)
        .crossfade(true)
        .size(Size.ORIGINAL)
        .build(),
    contentDescription = null
)
```

## 関連リソース

- [Motion System](motion-system.md) - アニメーション
- [Shape Library](shape-library.md) - シェイプ
- [examples/carousel-example.kt](../examples/carousel-example.kt) - 実装例
