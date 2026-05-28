# Composition Patterns Example

A complete working example demonstrating how to build complex UIs through widget composition in Flutter. This example shows how small, focused widgets combine to create sophisticated layouts without inheritance or code duplication.

## Overview

This example builds a product details screen for an e-commerce app, demonstrating composition patterns including:
- Breaking down complex UIs into smaller widgets
- Composing widgets for flexibility and reusability
- Separating concerns between presentational and container widgets
- Building responsive layouts through composition

## Complete Example

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Composition Patterns',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepOrange),
        useMaterial3: true,
      ),
      home: const ProductDetailsScreen(),
    );
  }
}

// ============================================================================
// Data Model
// ============================================================================

class Product {
  final String id;
  final String name;
  final String description;
  final double price;
  final double rating;
  final int reviewCount;
  final List<String> images;
  final List<String> sizes;
  final List<Color> colors;
  final bool inStock;

  const Product({
    required this.id,
    required this.name,
    required this.description,
    required this.price,
    required this.rating,
    required this.reviewCount,
    required this.images,
    required this.sizes,
    required this.colors,
    required this.inStock,
  });
}

// Sample data
final sampleProduct = Product(
  id: '1',
  name: 'Premium Wireless Headphones',
  description:
      'Experience superior sound quality with active noise cancellation, '
      '30-hour battery life, and premium comfort. Perfect for music lovers '
      'and professionals who demand the best audio experience.',
  price: 299.99,
  rating: 4.5,
  reviewCount: 1247,
  images: [
    'https://picsum.photos/600/600?random=1',
    'https://picsum.photos/600/600?random=2',
    'https://picsum.photos/600/600?random=3',
  ],
  sizes: ['S', 'M', 'L'],
  colors: [Colors.black, Colors.white, Colors.blue, Colors.red],
  inStock: true,
);

// ============================================================================
// Atomic Component 1: PriceTag
// Small, focused widget for displaying prices
// ============================================================================

class PriceTag extends StatelessWidget {
  final double price;
  final TextStyle? style;
  final String currency;

  const PriceTag({
    super.key,
    required this.price,
    this.style,
    this.currency = '\$',
  });

  @override
  Widget build(BuildContext context) {
    final textTheme = Theme.of(context).textTheme;
    final effectiveStyle = style ?? textTheme.headlineSmall?.copyWith(
      fontWeight: FontWeight.bold,
      color: Theme.of(context).colorScheme.primary,
    );

    return Text(
      '$currency${price.toStringAsFixed(2)}',
      style: effectiveStyle,
    );
  }
}

// ============================================================================
// Atomic Component 2: RatingDisplay
// Displays star rating with review count
// ============================================================================

class RatingDisplay extends StatelessWidget {
  final double rating;
  final int reviewCount;
  final double starSize;

  const RatingDisplay({
    super.key,
    required this.rating,
    required this.reviewCount,
    this.starSize = 20,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        ...List.generate(5, (index) {
          if (index < rating.floor()) {
            return Icon(Icons.star, size: starSize, color: Colors.amber);
          } else if (index < rating) {
            return Icon(Icons.star_half, size: starSize, color: Colors.amber);
          } else {
            return Icon(Icons.star_border, size: starSize, color: Colors.amber);
          }
        }),
        const SizedBox(width: 8),
        Text(
          '$rating ($reviewCount reviews)',
          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: Colors.grey.shade700,
              ),
        ),
      ],
    );
  }
}

// ============================================================================
// Atomic Component 3: ColorSelector
// Displays selectable color options
// ============================================================================

class ColorSelector extends StatefulWidget {
  final List<Color> colors;
  final Color? selectedColor;
  final ValueChanged<Color> onColorSelected;

  const ColorSelector({
    super.key,
    required this.colors,
    this.selectedColor,
    required this.onColorSelected,
  });

  @override
  State<ColorSelector> createState() => _ColorSelectorState();
}

class _ColorSelectorState extends State<ColorSelector> {
  late Color _selectedColor;

  @override
  void initState() {
    super.initState();
    _selectedColor = widget.selectedColor ?? widget.colors.first;
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Color',
          style: Theme.of(context).textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.bold,
              ),
        ),
        const SizedBox(height: 12),
        Wrap(
          spacing: 12,
          children: widget.colors.map((color) {
            final isSelected = color == _selectedColor;
            return GestureDetector(
              onTap: () {
                setState(() {
                  _selectedColor = color;
                });
                widget.onColorSelected(color);
              },
              child: Container(
                width: 48,
                height: 48,
                decoration: BoxDecoration(
                  color: color,
                  shape: BoxShape.circle,
                  border: Border.all(
                    color: isSelected
                        ? Theme.of(context).colorScheme.primary
                        : Colors.grey.shade300,
                    width: isSelected ? 3 : 1,
                  ),
                ),
                child: isSelected
                    ? Icon(Icons.check, color: Colors.white)
                    : null,
              ),
            );
          }).toList(),
        ),
      ],
    );
  }
}

// ============================================================================
// Atomic Component 4: SizeSelector
// Displays selectable size options
// ============================================================================

class SizeSelector extends StatefulWidget {
  final List<String> sizes;
  final String? selectedSize;
  final ValueChanged<String> onSizeSelected;

  const SizeSelector({
    super.key,
    required this.sizes,
    this.selectedSize,
    required this.onSizeSelected,
  });

  @override
  State<SizeSelector> createState() => _SizeSelectorState();
}

class _SizeSelectorState extends State<SizeSelector> {
  late String _selectedSize;

  @override
  void initState() {
    super.initState();
    _selectedSize = widget.selectedSize ?? widget.sizes.first;
  }

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Size',
          style: Theme.of(context).textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.bold,
              ),
        ),
        const SizedBox(height: 12),
        Wrap(
          spacing: 12,
          children: widget.sizes.map((size) {
            final isSelected = size == _selectedSize;
            return GestureDetector(
              onTap: () {
                setState(() {
                  _selectedSize = size;
                });
                widget.onSizeSelected(size);
              },
              child: Container(
                width: 56,
                height: 40,
                decoration: BoxDecoration(
                  color: isSelected ? colorScheme.primary : Colors.transparent,
                  border: Border.all(
                    color: isSelected ? colorScheme.primary : Colors.grey.shade400,
                    width: 1,
                  ),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Center(
                  child: Text(
                    size,
                    style: TextStyle(
                      color: isSelected ? Colors.white : Colors.black,
                      fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                    ),
                  ),
                ),
              ),
            );
          }).toList(),
        ),
      ],
    );
  }
}

// ============================================================================
// Composite Component 1: ImageGallery
// Composes image display with thumbnails
// ============================================================================

class ImageGallery extends StatefulWidget {
  final List<String> images;

  const ImageGallery({
    super.key,
    required this.images,
  });

  @override
  State<ImageGallery> createState() => _ImageGalleryState();
}

class _ImageGalleryState extends State<ImageGallery> {
  int _currentIndex = 0;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Main image
        AspectRatio(
          aspectRatio: 1,
          child: Container(
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(12),
              color: Colors.grey.shade100,
            ),
            child: ClipRRect(
              borderRadius: BorderRadius.circular(12),
              child: Image.network(
                widget.images[_currentIndex],
                fit: BoxFit.cover,
              ),
            ),
          ),
        ),
        const SizedBox(height: 16),
        // Thumbnail strip
        SizedBox(
          height: 80,
          child: ListView.separated(
            scrollDirection: Axis.horizontal,
            itemCount: widget.images.length,
            separatorBuilder: (context, index) => const SizedBox(width: 12),
            itemBuilder: (context, index) {
              final isSelected = index == _currentIndex;
              return GestureDetector(
                onTap: () {
                  setState(() {
                    _currentIndex = index;
                  });
                },
                child: Container(
                  width: 80,
                  height: 80,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(
                      color: isSelected
                          ? Theme.of(context).colorScheme.primary
                          : Colors.grey.shade300,
                      width: isSelected ? 3 : 1,
                    ),
                  ),
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(8),
                    child: Image.network(
                      widget.images[index],
                      fit: BoxFit.cover,
                    ),
                  ),
                ),
              );
            },
          ),
        ),
      ],
    );
  }
}

// ============================================================================
// Composite Component 2: ProductInfo
// Composes product name, price, rating, and description
// ============================================================================

class ProductInfo extends StatelessWidget {
  final Product product;

  const ProductInfo({
    super.key,
    required this.product,
  });

  @override
  Widget build(BuildContext context) {
    final textTheme = Theme.of(context).textTheme;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Product name
        Text(
          product.name,
          style: textTheme.headlineMedium?.copyWith(
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 8),

        // Price and stock status
        Row(
          children: [
            PriceTag(price: product.price),
            const Spacer(),
            if (product.inStock)
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(
                  color: Colors.green.shade100,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  'In Stock',
                  style: TextStyle(
                    color: Colors.green.shade900,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              )
            else
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(
                  color: Colors.red.shade100,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  'Out of Stock',
                  style: TextStyle(
                    color: Colors.red.shade900,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
          ],
        ),
        const SizedBox(height: 12),

        // Rating
        RatingDisplay(
          rating: product.rating,
          reviewCount: product.reviewCount,
        ),
        const SizedBox(height: 16),

        // Description
        Text(
          'Description',
          style: textTheme.titleMedium?.copyWith(
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 8),
        Text(
          product.description,
          style: textTheme.bodyMedium?.copyWith(
            color: Colors.grey.shade700,
            height: 1.5,
          ),
        ),
      ],
    );
  }
}

// ============================================================================
// Composite Component 3: ProductOptions
// Composes color and size selectors
// ============================================================================

class ProductOptions extends StatelessWidget {
  final Product product;
  final ValueChanged<Color> onColorSelected;
  final ValueChanged<String> onSizeSelected;

  const ProductOptions({
    super.key,
    required this.product,
    required this.onColorSelected,
    required this.onSizeSelected,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        ColorSelector(
          colors: product.colors,
          onColorSelected: onColorSelected,
        ),
        const SizedBox(height: 24),
        SizeSelector(
          sizes: product.sizes,
          onSizeSelected: onSizeSelected,
        ),
      ],
    );
  }
}

// ============================================================================
// Container Component: ActionBar
// Composes action buttons for add to cart and buy now
// ============================================================================

class ActionBar extends StatelessWidget {
  final bool enabled;
  final VoidCallback onAddToCart;
  final VoidCallback onBuyNow;

  const ActionBar({
    super.key,
    required this.enabled,
    required this.onAddToCart,
    required this.onBuyNow,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, -5),
          ),
        ],
      ),
      child: SafeArea(
        child: Row(
          children: [
            Expanded(
              child: OutlinedButton.icon(
                onPressed: enabled ? onAddToCart : null,
                icon: const Icon(Icons.shopping_cart_outlined),
                label: const Text('Add to Cart'),
                style: OutlinedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                ),
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              flex: 2,
              child: FilledButton.icon(
                onPressed: enabled ? onBuyNow : null,
                icon: const Icon(Icons.shopping_bag),
                label: const Text('Buy Now'),
                style: FilledButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// ============================================================================
// Main Screen: Composes all components together
// ============================================================================

class ProductDetailsScreen extends StatefulWidget {
  const ProductDetailsScreen({super.key});

  @override
  State<ProductDetailsScreen> createState() => _ProductDetailsScreenState();
}

class _ProductDetailsScreenState extends State<ProductDetailsScreen> {
  Color? _selectedColor;
  String? _selectedSize;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Product Details'),
        actions: [
          IconButton(
            icon: const Icon(Icons.favorite_border),
            onPressed: () {},
          ),
          IconButton(
            icon: const Icon(Icons.share),
            onPressed: () {},
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Image gallery
                  ImageGallery(images: sampleProduct.images),
                  const SizedBox(height: 24),

                  // Product info
                  ProductInfo(product: sampleProduct),
                  const SizedBox(height: 24),

                  // Product options
                  ProductOptions(
                    product: sampleProduct,
                    onColorSelected: (color) {
                      setState(() {
                        _selectedColor = color;
                      });
                      print('Selected color: $color');
                    },
                    onSizeSelected: (size) {
                      setState(() {
                        _selectedSize = size;
                      });
                      print('Selected size: $size');
                    },
                  ),
                  const SizedBox(height: 100), // Space for action bar
                ],
              ),
            ),
          ),
        ],
      ),
      bottomNavigationBar: ActionBar(
        enabled: sampleProduct.inStock,
        onAddToCart: () {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(
                'Added to cart: ${sampleProduct.name}\n'
                'Color: $_selectedColor, Size: $_selectedSize',
              ),
              behavior: SnackBarBehavior.floating,
            ),
          );
        },
        onBuyNow: () {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Proceeding to checkout...'),
              behavior: SnackBarBehavior.floating,
            ),
          );
        },
      ),
    );
  }
}
```

## Composition Hierarchy

```
ProductDetailsScreen (Container)
├── AppBar
├── SingleChildScrollView
│   ├── ImageGallery (Composite)
│   │   ├── Main Image
│   │   └── Thumbnail ListView
│   ├── ProductInfo (Composite)
│   │   ├── Product Name (Text)
│   │   ├── PriceTag (Atomic)
│   │   ├── Stock Status
│   │   ├── RatingDisplay (Atomic)
│   │   └── Description (Text)
│   └── ProductOptions (Composite)
│       ├── ColorSelector (Atomic)
│       └── SizeSelector (Atomic)
└── ActionBar (Container)
    ├── Add to Cart Button
    └── Buy Now Button
```

## Key Patterns Demonstrated

### 1. Atomic Components

Small, single-purpose widgets that do one thing well:
- `PriceTag` - Display price
- `RatingDisplay` - Display rating with stars
- `ColorSelector` - Select color
- `SizeSelector` - Select size

### 2. Composite Components

Combine multiple atomic or composite components:
- `ImageGallery` - Main image + thumbnails
- `ProductInfo` - Combines PriceTag, RatingDisplay, and text
- `ProductOptions` - Combines ColorSelector and SizeSelector

### 3. Container Components

Manage state and coordinate child components:
- `ProductDetailsScreen` - Orchestrates entire screen
- `ActionBar` - Manages action buttons

### 4. Separation of Concerns

- **Presentation** - Atomic components focus on display
- **Composition** - Composite components combine presentational widgets
- **Logic** - Container components manage state and behavior

### 5. Props Down, Events Up

- Configuration flows down through constructor parameters
- User actions bubble up through callbacks

```dart
ColorSelector(
  colors: product.colors,  // Props down
  onColorSelected: (color) {  // Events up
    setState(() {
      _selectedColor = color;
    });
  },
)
```

## Benefits of This Approach

1. **Modularity** - Each component is self-contained
2. **Reusability** - Components can be used in different contexts
3. **Testability** - Small components are easy to test in isolation
4. **Maintainability** - Changes are localized to specific components
5. **Readability** - Clear hierarchy and purpose for each widget
6. **Flexibility** - Easy to rearrange or replace components
7. **Scalability** - Pattern scales to large applications

## Extension Ideas

Extend this example by:

1. **Add more atomic components** - Badges, tags, quantity selector
2. **Create variant compositions** - Different product card layouts
3. **Add animations** - Smooth transitions between images, color selection
4. **Implement responsive design** - Adapt layout for different screen sizes
5. **Add accessibility** - Semantic labels, screen reader support
6. **Integrate state management** - Use Provider, Riverpod, or Bloc
7. **Add error handling** - Handle image loading failures
8. **Implement caching** - Cache selected options

## Best Practices

1. **Keep widgets small** - Each widget should have a single responsibility
2. **Use composition** - Build complex UIs by combining simple widgets
3. **Pass data down** - Use constructor parameters for configuration
4. **Bubble events up** - Use callbacks for user interactions
5. **Extract early** - When a widget gets complex, extract parts into separate widgets
6. **Name descriptively** - Widget names should clearly indicate their purpose
7. **Make widgets configurable** - Use parameters for flexibility
8. **Avoid deep nesting** - Extract nested widgets into separate classes

## Further Reading

- [Custom Widgets Example](custom-widgets.md)
- [Widget Catalog](../references/widget-catalog.md)
- [Layout Patterns](../references/layout-patterns.md)
- [Widget Lifecycle](../references/widget-lifecycle.md)
