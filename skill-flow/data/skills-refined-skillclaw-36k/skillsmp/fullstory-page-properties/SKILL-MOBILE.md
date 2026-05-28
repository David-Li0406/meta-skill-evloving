---
name: fullstory-page-properties-mobile
version: v3
platforms:
  - ios
  - android
  - flutter
  - react-native
sdks:
  - fullstory-swift
  - fullstory-android
  - fullstory-flutter
  - fullstory-react-native
description: Mobile implementation guide for Fullstory's Page Properties API. Includes API reference and code examples for iOS (Swift/SwiftUI), Android (Kotlin/Jetpack Compose), Flutter (Dart), and React Native.
parent_skill: fullstory-page-properties
related_skills:
  - fullstory-page-properties
  - fullstory-user-properties
  - fullstory-analytics-events
---

# Fullstory Page Properties — Mobile Implementation

> **Core Concepts**: See [SKILL.md](./SKILL.md) for pageName limits, property scoping, and best practices.
>
> **Web Implementation**: See [SKILL-WEB.md](./SKILL-WEB.md) for JavaScript/TypeScript.

---

## Quick Reference

| Platform | SDK | Method |
|----------|-----|--------|
| iOS | `FullStory` | `FS.setPage(pageName:properties:)` |
| Android | `FullStory` | `FS.setPage(pageName, properties)` |
| Flutter | `fullstory_flutter` | `FS.setPage(pageName: '', properties: {})` |
| React Native | `@fullstory/react-native` | `FullStory.setPage(pageName, properties)` |

---

## iOS (Swift/SwiftUI)

### API Reference

```swift
import FullStory

// Set page properties
FS.setPage(pageName: String, properties: [String: Any]?)
```

### ✅ GOOD Implementation Examples

#### Screen Appearance Tracking

```swift
// GOOD: Set page properties on screen appearance
class ProductDetailViewController: UIViewController {
    var product: Product!
    
    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        
        FS.setPage(pageName: "Product Detail", properties: [
            "productId": product.id,
            "productName": product.name,
            "category": product.category,
            "price": product.price,
            "inStock": product.inStock,
            "brand": product.brand
        ])
    }
}
```

#### Search Results Screen

```swift
// GOOD: Comprehensive search context
func setSearchPageProperties(results: SearchResults) {
    FS.setPage(pageName: "Search Results", properties: [
        // Search context
        "searchTerm": results.query,
        "searchType": results.type,
        
        // Results info
        "resultsCount": results.total,
        "hasResults": results.total > 0,
        
        // Filters
        "activeFilters": results.filters.keys.map { $0 },
        "filterCount": results.filters.count,
        
        // Sorting
        "sortBy": results.sortBy,
        "sortOrder": results.sortOrder,
        
        // Pagination
        "currentPage": results.page,
        "totalPages": results.totalPages
    ])
}
```

#### Checkout Flow

```swift
// GOOD: Checkout with step tracking
class CheckoutPageProperties {
    
    func setCartReviewStep(cart: Cart) {
        FS.setPage(pageName: "Checkout", properties: [
            "checkoutStep": 1,
            "checkoutStepName": "Cart Review",
            "cartId": cart.id,
            "cartValue": cart.subtotal,
            "cartItemCount": cart.items.count,
            "hasCoupon": cart.coupon != nil,
            "estimatedTotal": cart.total
        ])
    }
    
    func setShippingStep(cart: Cart, options: [ShippingOption]) {
        FS.setPage(pageName: "Checkout", properties: [
            "checkoutStep": 2,
            "checkoutStepName": "Shipping",
            "cartValue": cart.subtotal,
            "shippingOptionsCount": options.count
        ])
    }
    
    func setPaymentStep(cart: Cart, shipping: ShippingOption) {
        FS.setPage(pageName: "Checkout", properties: [
            "checkoutStep": 3,
            "checkoutStepName": "Payment",
            "cartValue": cart.subtotal,
            "shippingMethod": shipping.name,
            "shippingCost": shipping.price
        ])
    }
    
    func setConfirmationStep(order: Order) {
        FS.setPage(pageName: "Order Confirmation", properties: [
            "orderId": order.id,
            "orderTotal": order.total,
            "paymentMethod": order.paymentMethod,
            "shippingMethod": order.shippingMethod
        ])
    }
}
```

#### SwiftUI Integration

```swift
// GOOD: SwiftUI view with page properties
struct ProductDetailView: View {
    let product: Product
    
    var body: some View {
        ScrollView {
            ProductContent(product: product)
        }
        .onAppear {
            setPageProperties()
        }
    }
    
    private func setPageProperties() {
        FS.setPage(pageName: "Product Detail", properties: [
            "productId": product.id,
            "productName": product.name,
            "category": product.category,
            "price": product.price,
            "inStock": product.inStock
        ])
    }
}

// GOOD: Reusable view modifier
struct PagePropertiesModifier: ViewModifier {
    let pageName: String
    let properties: [String: Any]
    
    func body(content: Content) -> some View {
        content.onAppear {
            FS.setPage(pageName: pageName, properties: properties)
        }
    }
}

extension View {
    func pageProperties(_ pageName: String, properties: [String: Any] = [:]) -> some View {
        modifier(PagePropertiesModifier(pageName: pageName, properties: properties))
    }
}

// Usage
struct CategoryView: View {
    let category: Category
    
    var body: some View {
        ProductGrid(products: category.products)
            .pageProperties("Category", properties: [
                "categoryId": category.id,
                "categoryName": category.name,
                "productCount": category.products.count
            ])
    }
}
```

#### Dashboard with Dynamic State

```swift
// GOOD: Dashboard with view state
class DashboardViewController: UIViewController {
    var dashboardState: DashboardState!
    
    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        updatePageProperties()
    }
    
    func updatePageProperties() {
        FS.setPage(pageName: "Dashboard", properties: [
            "dashboardView": dashboardState.activeView,
            "dateRange": dashboardState.dateRange.label,
            "segmentFilter": dashboardState.segment,
            "widgetCount": dashboardState.widgets.count,
            "hasData": dashboardState.hasData
        ])
    }
    
    // Call when state changes
    func onStateChanged() {
        updatePageProperties()
    }
}
```

### ❌ BAD Implementation Examples

```swift
// BAD: Dynamic pageName
FS.setPage(pageName: product.name, properties: nil)
// Will exhaust 1,000 pageName limit!

// BAD: User data in page properties
FS.setPage(pageName: "Dashboard", properties: [
    "userId": user.id,      // Should be user property
    "userPlan": user.plan   // Should be user property
])

// BAD: Missing pageName context
FS.setPage(pageName: "Screen", properties: [
    "category": "Electronics"
])
// "Screen" is too generic
```

---

## Android (Kotlin/Jetpack Compose)

### API Reference

```kotlin
import com.fullstory.FS

// Set page properties
FS.setPage(pageName: String, properties: Map<String, Any>?)
```

### ✅ GOOD Implementation Examples

#### Activity/Fragment Tracking

```kotlin
// GOOD: Set page properties on screen resume
class ProductDetailActivity : AppCompatActivity() {
    private lateinit var product: Product
    
    override fun onResume() {
        super.onResume()
        
        FS.setPage("Product Detail", mapOf(
            "productId" to product.id,
            "productName" to product.name,
            "category" to product.category,
            "price" to product.price,
            "inStock" to product.inStock,
            "brand" to product.brand
        ))
    }
}
```

#### Search Results Screen

```kotlin
// GOOD: Comprehensive search context
fun setSearchPageProperties(results: SearchResults) {
    FS.setPage("Search Results", mapOf(
        // Search context
        "searchTerm" to results.query,
        "searchType" to results.type,
        
        // Results info
        "resultsCount" to results.total,
        "hasResults" to (results.total > 0),
        
        // Filters
        "activeFilters" to results.filters.keys.toList(),
        "filterCount" to results.filters.size,
        
        // Sorting
        "sortBy" to results.sortBy,
        "sortOrder" to results.sortOrder,
        
        // Pagination
        "currentPage" to results.page,
        "totalPages" to results.totalPages
    ))
}
```

#### Checkout Flow

```kotlin
// GOOD: Checkout with step tracking
class CheckoutPageProperties {
    
    fun setCartReviewStep(cart: Cart) {
        FS.setPage("Checkout", mapOf(
            "checkoutStep" to 1,
            "checkoutStepName" to "Cart Review",
            "cartId" to cart.id,
            "cartValue" to cart.subtotal,
            "cartItemCount" to cart.items.size,
            "hasCoupon" to (cart.coupon != null),
            "estimatedTotal" to cart.total
        ))
    }
    
    fun setShippingStep(cart: Cart, options: List<ShippingOption>) {
        FS.setPage("Checkout", mapOf(
            "checkoutStep" to 2,
            "checkoutStepName" to "Shipping",
            "cartValue" to cart.subtotal,
            "shippingOptionsCount" to options.size
        ))
    }
    
    fun setPaymentStep(cart: Cart, shipping: ShippingOption) {
        FS.setPage("Checkout", mapOf(
            "checkoutStep" to 3,
            "checkoutStepName" to "Payment",
            "cartValue" to cart.subtotal,
            "shippingMethod" to shipping.name,
            "shippingCost" to shipping.price
        ))
    }
    
    fun setConfirmationStep(order: Order) {
        FS.setPage("Order Confirmation", mapOf(
            "orderId" to order.id,
            "orderTotal" to order.total,
            "paymentMethod" to order.paymentMethod,
            "shippingMethod" to order.shippingMethod
        ))
    }
}
```

#### Jetpack Compose Integration

```kotlin
// GOOD: Compose screen with page properties
@Composable
fun ProductDetailScreen(product: Product) {
    LaunchedEffect(product.id) {
        FS.setPage("Product Detail", mapOf(
            "productId" to product.id,
            "productName" to product.name,
            "category" to product.category,
            "price" to product.price,
            "inStock" to product.inStock
        ))
    }
    
    // Screen content
    ProductContent(product = product)
}

// GOOD: Reusable composable wrapper
@Composable
fun PagePropertiesEffect(
    pageName: String,
    properties: Map<String, Any> = emptyMap(),
    key: Any = Unit
) {
    LaunchedEffect(key) {
        FS.setPage(pageName, properties)
    }
}

// Usage
@Composable
fun CategoryScreen(category: Category) {
    PagePropertiesEffect(
        pageName = "Category",
        properties = mapOf(
            "categoryId" to category.id,
            "categoryName" to category.name,
            "productCount" to category.products.size
        ),
        key = category.id
    )
    
    ProductGrid(products = category.products)
}
```

#### Navigation Component Integration

```kotlin
// GOOD: Navigation destination tracking
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val navController = findNavController(R.id.nav_host)
        navController.addOnDestinationChangedListener { _, destination, arguments ->
            setPagePropertiesForDestination(destination, arguments)
        }
    }
    
    private fun setPagePropertiesForDestination(
        destination: NavDestination,
        arguments: Bundle?
    ) {
        val pageName = when (destination.id) {
            R.id.productDetail -> "Product Detail"
            R.id.categoryList -> "Category"
            R.id.checkout -> "Checkout"
            R.id.search -> "Search Results"
            else -> destination.label?.toString() ?: "Unknown"
        }
        
        val properties = mutableMapOf<String, Any>("path" to destination.route.orEmpty())
        
        // Extract route arguments
        arguments?.let { args ->
            args.getString("productId")?.let { properties["productId"] = it }
            args.getString("categoryId")?.let { properties["categoryId"] = it }
        }
        
        FS.setPage(pageName, properties)
    }
}
```

### ❌ BAD Implementation Examples

```kotlin
// BAD: Dynamic pageName
FS.setPage(product.name, null)
// Will exhaust 1,000 pageName limit!

// BAD: User data in page properties
FS.setPage("Dashboard", mapOf(
    "userId" to user.id,      // Should be user property
    "userPlan" to user.plan   // Should be user property
))

// BAD: Missing pageName context
FS.setPage("Screen", mapOf(
    "category" to "Electronics"
))
// "Screen" is too generic
```

---

## Flutter (Dart)

### API Reference

```dart
import 'package:fullstory_flutter/fs.dart';

// Set page properties
FS.setPage(pageName: String, properties: Map<String, dynamic>?);
```

### ✅ GOOD Implementation Examples

#### Screen Appearance Tracking

```dart
// GOOD: Set page properties on screen init
class ProductDetailScreen extends StatefulWidget {
  final Product product;
  
  const ProductDetailScreen({required this.product});
  
  @override
  State<ProductDetailScreen> createState() => _ProductDetailScreenState();
}

class _ProductDetailScreenState extends State<ProductDetailScreen> {
  @override
  void initState() {
    super.initState();
    _setPageProperties();
  }
  
  void _setPageProperties() {
    FS.setPage(pageName: 'Product Detail', properties: {
      'productId': widget.product.id,
      'productName': widget.product.name,
      'category': widget.product.category,
      'price': widget.product.price,
      'inStock': widget.product.inStock,
      'brand': widget.product.brand,
    });
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: ProductContent(product: widget.product),
    );
  }
}
```

#### Search Results Screen

```dart
// GOOD: Comprehensive search context
void setSearchPageProperties(SearchResults results) {
  FS.setPage(pageName: 'Search Results', properties: {
    // Search context
    'searchTerm': results.query,
    'searchType': results.type,
    
    // Results info
    'resultsCount': results.total,
    'hasResults': results.total > 0,
    
    // Filters
    'activeFilters': results.filters.keys.toList(),
    'filterCount': results.filters.length,
    
    // Sorting
    'sortBy': results.sortBy,
    'sortOrder': results.sortOrder,
    
    // Pagination
    'currentPage': results.page,
    'totalPages': results.totalPages,
  });
}
```

#### Checkout Flow

```dart
// GOOD: Checkout with step tracking
class CheckoutPageProperties {
  
  void setCartReviewStep(Cart cart) {
    FS.setPage(pageName: 'Checkout', properties: {
      'checkoutStep': 1,
      'checkoutStepName': 'Cart Review',
      'cartId': cart.id,
      'cartValue': cart.subtotal,
      'cartItemCount': cart.items.length,
      'hasCoupon': cart.coupon != null,
      'estimatedTotal': cart.total,
    });
  }
  
  void setShippingStep(Cart cart, List<ShippingOption> options) {
    FS.setPage(pageName: 'Checkout', properties: {
      'checkoutStep': 2,
      'checkoutStepName': 'Shipping',
      'cartValue': cart.subtotal,
      'shippingOptionsCount': options.length,
    });
  }
  
  void setPaymentStep(Cart cart, ShippingOption shipping) {
    FS.setPage(pageName: 'Checkout', properties: {
      'checkoutStep': 3,
      'checkoutStepName': 'Payment',
      'cartValue': cart.subtotal,
      'shippingMethod': shipping.name,
      'shippingCost': shipping.price,
    });
  }
  
  void setConfirmationStep(Order order) {
    FS.setPage(pageName: 'Order Confirmation', properties: {
      'orderId': order.id,
      'orderTotal': order.total,
      'paymentMethod': order.paymentMethod,
      'shippingMethod': order.shippingMethod,
    });
  }
}
```

#### Navigator Observer Integration

```dart
// GOOD: Route observer for automatic page tracking
class FullstoryNavigatorObserver extends NavigatorObserver {
  final Map<String, PageConfig> _pageConfigs;
  
  FullstoryNavigatorObserver(this._pageConfigs);
  
  @override
  void didPush(Route route, Route? previousRoute) {
    _setPageProperties(route);
  }
  
  @override
  void didPop(Route route, Route? previousRoute) {
    if (previousRoute != null) {
      _setPageProperties(previousRoute);
    }
  }
  
  void _setPageProperties(Route route) {
    final routeName = route.settings.name;
    if (routeName == null) return;
    
    final config = _pageConfigs[routeName];
    if (config != null) {
      final properties = config.getProperties(route.settings.arguments);
      FS.setPage(pageName: config.pageName, properties: properties);
    }
  }
}

class PageConfig {
  final String pageName;
  final Map<String, dynamic> Function(Object?)? getProperties;
  
  PageConfig(this.pageName, {this.getProperties});
}

// Usage
final observer = FullstoryNavigatorObserver({
  '/product': PageConfig('Product Detail', getProperties: (args) {
    final product = args as Product;
    return {'productId': product.id, 'productName': product.name};
  }),
  '/category': PageConfig('Category'),
  '/checkout': PageConfig('Checkout'),
});

MaterialApp(
  navigatorObservers: [observer],
  // ...
);
```

#### Riverpod Integration

```dart
// GOOD: Using Riverpod for page properties
final pagePropertiesProvider = Provider((ref) => PagePropertiesService());

class PagePropertiesService {
  void setProductPage(Product product) {
    FS.setPage(pageName: 'Product Detail', properties: {
      'productId': product.id,
      'productName': product.name,
      'category': product.category,
      'price': product.price,
    });
  }
  
  void setSearchPage(SearchResults results) {
    FS.setPage(pageName: 'Search Results', properties: {
      'searchTerm': results.query,
      'resultsCount': results.total,
      'hasResults': results.total > 0,
    });
  }
  
  void updatePageProperty(String key, dynamic value) {
    // Note: On mobile, you typically call setPage again with all properties
    // Consider maintaining current page state if frequent updates needed
  }
}
```

### ❌ BAD Implementation Examples

```dart
// BAD: Dynamic pageName
FS.setPage(pageName: product.name, properties: null);
// Will exhaust 1,000 pageName limit!

// BAD: User data in page properties
FS.setPage(pageName: 'Dashboard', properties: {
  'userId': user.id,      // Should be user property
  'userPlan': user.plan,  // Should be user property
});

// BAD: Missing pageName context
FS.setPage(pageName: 'Screen', properties: {
  'category': 'Electronics',
});
// "Screen" is too generic
```

---

## React Native

### API Reference

```javascript
import FullStory from '@fullstory/react-native';

// Set page properties
FullStory.setPage(pageName: string, properties?: object);
```

### ✅ GOOD Implementation Examples

#### Screen Focus Tracking

```jsx
// GOOD: Set page properties on screen focus
import { useFocusEffect } from '@react-navigation/native';

function ProductDetailScreen({ route }) {
  const { product } = route.params;
  
  useFocusEffect(
    useCallback(() => {
      FullStory.setPage('Product Detail', {
        productId: product.id,
        productName: product.name,
        category: product.category,
        price: product.price,
        inStock: product.inStock,
        brand: product.brand,
      });
    }, [product])
  );
  
  return <ProductContent product={product} />;
}
```

#### Search Results Screen

```javascript
// GOOD: Comprehensive search context
function setSearchPageProperties(results) {
  FullStory.setPage('Search Results', {
    // Search context
    searchTerm: results.query,
    searchType: results.type,
    
    // Results info
    resultsCount: results.total,
    hasResults: results.total > 0,
    
    // Filters
    activeFilters: Object.keys(results.filters),
    filterCount: Object.keys(results.filters).length,
    
    // Sorting
    sortBy: results.sortBy,
    sortOrder: results.sortOrder,
    
    // Pagination
    currentPage: results.page,
    totalPages: results.totalPages,
  });
}
```

#### Checkout Flow

```javascript
// GOOD: Checkout with step tracking
class CheckoutPageProperties {
  setCartReviewStep(cart) {
    FullStory.setPage('Checkout', {
      checkoutStep: 1,
      checkoutStepName: 'Cart Review',
      cartId: cart.id,
      cartValue: cart.subtotal,
      cartItemCount: cart.items.length,
      hasCoupon: !!cart.coupon,
      estimatedTotal: cart.total,
    });
  }
  
  setShippingStep(cart, options) {
    FullStory.setPage('Checkout', {
      checkoutStep: 2,
      checkoutStepName: 'Shipping',
      cartValue: cart.subtotal,
      shippingOptionsCount: options.length,
    });
  }
  
  setPaymentStep(cart, shipping) {
    FullStory.setPage('Checkout', {
      checkoutStep: 3,
      checkoutStepName: 'Payment',
      cartValue: cart.subtotal,
      shippingMethod: shipping.name,
      shippingCost: shipping.price,
    });
  }
  
  setConfirmationStep(order) {
    FullStory.setPage('Order Confirmation', {
      orderId: order.id,
      orderTotal: order.total,
      paymentMethod: order.paymentMethod,
      shippingMethod: order.shippingMethod,
    });
  }
}
```

#### Custom Hook

```jsx
// GOOD: Reusable hook for page properties
import { useEffect } from 'react';
import { useFocusEffect } from '@react-navigation/native';
import FullStory from '@fullstory/react-native';

export function usePageProperties(pageName, properties = {}, deps = []) {
  useFocusEffect(
    useCallback(() => {
      FullStory.setPage(pageName, properties);
    }, [pageName, ...deps])
  );
}

// Usage
function CategoryScreen({ route }) {
  const { category } = route.params;
  
  usePageProperties('Category', {
    categoryId: category.id,
    categoryName: category.name,
    productCount: category.products.length,
  }, [category.id]);
  
  return <ProductGrid products={category.products} />;
}
```

#### React Navigation Integration

```jsx
// GOOD: Navigation state listener for automatic page tracking
import { NavigationContainer } from '@react-navigation/native';
import FullStory from '@fullstory/react-native';

const pageConfigs = {
  ProductDetail: (params) => ({
    pageName: 'Product Detail',
    properties: {
      productId: params?.productId,
      productName: params?.productName,
    },
  }),
  Category: (params) => ({
    pageName: 'Category',
    properties: {
      categoryId: params?.categoryId,
    },
  }),
  Search: () => ({
    pageName: 'Search Results',
    properties: {},
  }),
  Checkout: (params) => ({
    pageName: 'Checkout',
    properties: {
      step: params?.step,
    },
  }),
};

function App() {
  const onStateChange = (state) => {
    const currentRoute = getCurrentRoute(state);
    if (!currentRoute) return;
    
    const config = pageConfigs[currentRoute.name];
    if (config) {
      const { pageName, properties } = config(currentRoute.params);
      FullStory.setPage(pageName, properties);
    }
  };
  
  return (
    <NavigationContainer onStateChange={onStateChange}>
      <AppNavigator />
    </NavigationContainer>
  );
}

function getCurrentRoute(state) {
  if (!state) return null;
  const route = state.routes[state.index];
  if (route.state) return getCurrentRoute(route.state);
  return route;
}
```

#### Dashboard with Dynamic State

```jsx
// GOOD: Dashboard with state updates
function DashboardScreen() {
  const [dashboardState, setDashboardState] = useState(initialState);
  
  // Set page properties on focus
  useFocusEffect(
    useCallback(() => {
      updatePageProperties(dashboardState);
    }, [])
  );
  
  // Update page properties when state changes
  useEffect(() => {
    updatePageProperties(dashboardState);
  }, [dashboardState.activeView, dashboardState.dateRange]);
  
  const updatePageProperties = (state) => {
    FullStory.setPage('Dashboard', {
      dashboardView: state.activeView,
      dateRange: state.dateRange.label,
      segmentFilter: state.segment,
      widgetCount: state.widgets.length,
      hasData: state.hasData,
    });
  };
  
  return <DashboardContent state={dashboardState} />;
}
```

### ❌ BAD Implementation Examples

```javascript
// BAD: Dynamic pageName
FullStory.setPage(product.name, {});
// Will exhaust 1,000 pageName limit!

// BAD: User data in page properties
FullStory.setPage('Dashboard', {
  userId: user.id,      // Should be user property
  userPlan: user.plan,  // Should be user property
});

// BAD: Setting on every render
function BadComponent({ product }) {
  // This fires on EVERY render!
  FullStory.setPage('Product Detail', { productId: product.id });
  
  return <View>...</View>;
}

// BAD: Missing pageName context
FullStory.setPage('Screen', {
  category: 'Electronics',
});
// "Screen" is too generic
```

---

## Common Patterns (All Platforms)

### Page Property Manager

Create a centralized service to standardize page property management:

| Platform | Pattern |
|----------|---------|
| iOS | Singleton class or static methods |
| Android | Object/companion object or Hilt-injected class |
| Flutter | Singleton, Provider, or Navigator observer |
| React Native | Custom hook or navigation listener |

### Screen Lifecycle Hooks

Set page properties at the right moment:

| Platform | Lifecycle Hook |
|----------|----------------|
| iOS (Swift) | `viewDidAppear` |
| iOS SwiftUI | `.onAppear` |
| Android Activity | `onResume` |
| Android Compose | `LaunchedEffect` |
| Flutter | `initState` or Navigator observer |
| React Native | `useFocusEffect` |

### Page Categories

Recommended pageName values by app type:

| E-commerce | SaaS | Content |
|------------|------|---------|
| Home | Dashboard | Home |
| Category | Reports | Article |
| Product Detail | Settings | Category |
| Search Results | Team | Author |
| Cart | Billing | Search |
| Checkout | Integrations | Bookmarks |
| Order Confirmation | Profile | - |

### Property Categories by Page Type

| Page Type | Recommended Properties |
|-----------|----------------------|
| Product Detail | productId, productName, category, price, inStock |
| Search Results | searchTerm, resultsCount, activeFilters, sortBy |
| Checkout | checkoutStep, cartValue, itemCount, hasCoupon |
| Category | categoryId, categoryName, productCount |
| Dashboard | activeView, dateRange, selectedFilters |

---

## Reference Links

- **iOS**: https://developer.fullstory.com/mobile/ios/capture-data/set-page-properties/
- **Android**: https://developer.fullstory.com/mobile/android/capture-data/set-page-properties/
- **Flutter**: https://developer.fullstory.com/mobile/flutter/capture-data/set-page-properties/
- **React Native**: https://developer.fullstory.com/mobile/react-native/capture-data/set-page-properties/
