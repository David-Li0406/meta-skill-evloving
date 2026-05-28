---
name: fullstory-analytics-events-mobile
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
description: Mobile implementation guide for Fullstory's Analytics Events API. Includes API reference and code examples for iOS (Swift/SwiftUI), Android (Kotlin/Jetpack Compose), Flutter (Dart), and React Native.
parent_skill: fullstory-analytics-events
related_skills:
  - fullstory-analytics-events
  - fullstory-identify-users
  - fullstory-user-properties
---

# Fullstory Analytics Events — Mobile Implementation

> **Core Concepts**: See [SKILL.md](./SKILL.md) for event naming, property types, and best practices.
>
> **Web Implementation**: See [SKILL-WEB.md](./SKILL-WEB.md) for JavaScript/TypeScript.

---

## Quick Reference

| Platform | SDK | Method |
|----------|-----|--------|
| iOS | `FullStory` | `FS.event(name:properties:)` |
| Android | `FullStory` | `FS.event(name, properties)` |
| Flutter | `fullstory_flutter` | `FS.event(name: '', properties: {})` |
| React Native | `@fullstory/react-native` | `FullStory.event(name, properties)` |

---

## iOS (Swift/SwiftUI)

### API Reference

```swift
import FullStory

// Basic syntax
FS.event(name: String, properties: [String: Any])
```

### ✅ GOOD Implementation Examples

#### E-commerce — Product Added

```swift
// GOOD: Comprehensive product add event
func trackProductAdded(product: Product, quantity: Int, source: String) {
    FS.event(name: "Product Added", properties: [
        // Product identification
        "product_id": product.id,
        "sku": product.sku,
        "name": product.name,
        "brand": product.brand,
        
        // Categorization
        "category": product.category,
        "subcategory": product.subcategory ?? "",
        
        // Pricing
        "price": product.price,  // Double
        "currency": "USD",
        
        // Cart context
        "quantity": quantity,  // Int
        "cart_id": CartManager.shared.cartId,
        
        // Attribution
        "position": product.listPosition,
        "list_name": source,
        
        // Product attributes
        "variant": product.selectedVariant ?? "",
        "size": product.selectedSize ?? "",
        "color": product.selectedColor ?? ""
    ])
}
```

#### SaaS — Feature Usage

```swift
// GOOD: Track feature usage with context
func trackFeatureUsed(featureName: String, context: [String: Any] = [:]) {
    var properties: [String: Any] = [
        "feature_name": featureName,
        "feature_category": getFeatureCategory(featureName),
        "is_first_use": !hasUsedFeature(featureName),
        "times_used_total": getTotalUsageCount(featureName),
        "entry_point": currentScreen
    ]
    
    // Merge additional context
    for (key, value) in context {
        properties[key] = value
    }
    
    FS.event(name: "Feature Used", properties: properties)
}

// Usage
trackFeatureUsed(featureName: "advanced_export", context: [
    "export_format": "csv",
    "row_count": 1500
])
```

#### Subscription Events

```swift
// GOOD: Track subscription lifecycle
class SubscriptionTracker {
    
    func trackTrialStarted(trial: Trial) {
        FS.event(name: "Trial Started", properties: [
            "trial_plan": trial.plan,
            "trial_duration_days": trial.durationDays,
            "source": trial.acquisitionSource,
            "started_at": ISO8601DateFormatter().string(from: Date())
        ])
    }
    
    func trackSubscriptionStarted(subscription: Subscription) {
        FS.event(name: "Subscription Started", properties: [
            "plan_name": subscription.plan,
            "plan_tier": subscription.tier,
            "billing_cycle": subscription.billingCycle,
            "price": subscription.price,
            "currency": subscription.currency,
            "mrr": subscription.mrr,
            "trial_converted": subscription.wasTrialing,
            "payment_method": subscription.paymentMethod
        ])
    }
    
    func trackPlanChanged(from oldPlan: Plan, to newPlan: Plan) {
        let changeType = newPlan.price > oldPlan.price ? "upgrade" : "downgrade"
        
        FS.event(name: "Plan Changed", properties: [
            "from_plan": oldPlan.name,
            "to_plan": newPlan.name,
            "from_price": oldPlan.price,
            "to_price": newPlan.price,
            "price_change": newPlan.price - oldPlan.price,
            "change_type": changeType
        ])
    }
}
```

#### SwiftUI Integration

```swift
// GOOD: SwiftUI view with event tracking
struct ProductDetailView: View {
    let product: Product
    @State private var quantity = 1
    
    var body: some View {
        VStack {
            // Product info...
            
            Button("Add to Cart") {
                addToCart()
            }
        }
        .onAppear {
            trackProductViewed()
        }
    }
    
    private func trackProductViewed() {
        FS.event(name: "Product Viewed", properties: [
            "product_id": product.id,
            "name": product.name,
            "category": product.category,
            "price": product.price
        ])
    }
    
    private func addToCart() {
        CartManager.shared.add(product, quantity: quantity)
        
        FS.event(name: "Product Added", properties: [
            "product_id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": quantity
        ])
    }
}
```

### ❌ BAD Implementation Examples

```swift
// BAD: Generic event name
FS.event(name: "tap", properties: ["button": "cart"])

// BAD: Missing critical properties
FS.event(name: "Order Completed", properties: ["success": true])

// BAD: Wrong types (strings instead of numbers)
FS.event(name: "Product Added", properties: [
    "price": "$49.99",  // Should be 49.99
    "quantity": "3"     // Should be 3
])
```

---

## Android (Kotlin/Jetpack Compose)

### API Reference

```kotlin
import com.fullstory.FS

// Basic syntax
FS.event(name: String, properties: Map<String, Any>)
```

### ✅ GOOD Implementation Examples

#### E-commerce — Product Added

```kotlin
// GOOD: Comprehensive product add event
fun trackProductAdded(product: Product, quantity: Int, source: String) {
    FS.event("Product Added", mapOf(
        // Product identification
        "product_id" to product.id,
        "sku" to product.sku,
        "name" to product.name,
        "brand" to product.brand,
        
        // Categorization
        "category" to product.category,
        "subcategory" to (product.subcategory ?: ""),
        
        // Pricing
        "price" to product.price,  // Double
        "currency" to "USD",
        
        // Cart context
        "quantity" to quantity,  // Int
        "cart_id" to CartManager.cartId,
        
        // Attribution
        "position" to product.listPosition,
        "list_name" to source,
        
        // Product attributes
        "variant" to (product.selectedVariant ?: ""),
        "size" to (product.selectedSize ?: ""),
        "color" to (product.selectedColor ?: "")
    ))
}
```

#### SaaS — Feature Usage

```kotlin
// GOOD: Track feature usage with context
fun trackFeatureUsed(featureName: String, context: Map<String, Any> = emptyMap()) {
    val properties = mutableMapOf<String, Any>(
        "feature_name" to featureName,
        "feature_category" to getFeatureCategory(featureName),
        "is_first_use" to !hasUsedFeature(featureName),
        "times_used_total" to getTotalUsageCount(featureName),
        "entry_point" to currentScreen
    )
    
    // Merge additional context
    properties.putAll(context)
    
    FS.event("Feature Used", properties)
}

// Usage
trackFeatureUsed("advanced_export", mapOf(
    "export_format" to "csv",
    "row_count" to 1500
))
```

#### Subscription Events

```kotlin
// GOOD: Track subscription lifecycle
class SubscriptionTracker {
    
    fun trackTrialStarted(trial: Trial) {
        FS.event("Trial Started", mapOf(
            "trial_plan" to trial.plan,
            "trial_duration_days" to trial.durationDays,
            "source" to trial.acquisitionSource,
            "started_at" to Instant.now().toString()
        ))
    }
    
    fun trackSubscriptionStarted(subscription: Subscription) {
        FS.event("Subscription Started", mapOf(
            "plan_name" to subscription.plan,
            "plan_tier" to subscription.tier,
            "billing_cycle" to subscription.billingCycle,
            "price" to subscription.price,
            "currency" to subscription.currency,
            "mrr" to subscription.mrr,
            "trial_converted" to subscription.wasTrialing,
            "payment_method" to subscription.paymentMethod
        ))
    }
    
    fun trackPlanChanged(oldPlan: Plan, newPlan: Plan) {
        val changeType = if (newPlan.price > oldPlan.price) "upgrade" else "downgrade"
        
        FS.event("Plan Changed", mapOf(
            "from_plan" to oldPlan.name,
            "to_plan" to newPlan.name,
            "from_price" to oldPlan.price,
            "to_price" to newPlan.price,
            "price_change" to (newPlan.price - oldPlan.price),
            "change_type" to changeType
        ))
    }
}
```

#### Jetpack Compose Integration

```kotlin
// GOOD: Compose screen with event tracking
@Composable
fun ProductDetailScreen(
    product: Product,
    viewModel: ProductViewModel = hiltViewModel()
) {
    var quantity by remember { mutableStateOf(1) }
    
    LaunchedEffect(product.id) {
        FS.event("Product Viewed", mapOf(
            "product_id" to product.id,
            "name" to product.name,
            "category" to product.category,
            "price" to product.price
        ))
    }
    
    Column {
        // Product info...
        
        Button(onClick = {
            viewModel.addToCart(product, quantity)
            
            FS.event("Product Added", mapOf(
                "product_id" to product.id,
                "name" to product.name,
                "price" to product.price,
                "quantity" to quantity
            ))
        }) {
            Text("Add to Cart")
        }
    }
}
```

### ❌ BAD Implementation Examples

```kotlin
// BAD: Generic event name
FS.event("click", mapOf("button" to "cart"))

// BAD: Missing critical properties
FS.event("Order Completed", mapOf("success" to true))

// BAD: Wrong types (strings instead of numbers)
FS.event("Product Added", mapOf(
    "price" to "$49.99",  // Should be 49.99
    "quantity" to "3"     // Should be 3
))
```

---

## Flutter (Dart)

### API Reference

```dart
import 'package:fullstory_flutter/fs.dart';

// Basic syntax
FS.event(name: String, properties: Map<String, dynamic>);
```

### ✅ GOOD Implementation Examples

#### E-commerce — Product Added

```dart
// GOOD: Comprehensive product add event
void trackProductAdded(Product product, int quantity, String source) {
  FS.event(name: 'Product Added', properties: {
    // Product identification
    'product_id': product.id,
    'sku': product.sku,
    'name': product.name,
    'brand': product.brand,
    
    // Categorization
    'category': product.category,
    'subcategory': product.subcategory ?? '',
    
    // Pricing
    'price': product.price,  // double
    'currency': 'USD',
    
    // Cart context
    'quantity': quantity,  // int
    'cart_id': CartManager.instance.cartId,
    
    // Attribution
    'position': product.listPosition,
    'list_name': source,
    
    // Product attributes
    'variant': product.selectedVariant ?? '',
    'size': product.selectedSize ?? '',
    'color': product.selectedColor ?? '',
  });
}
```

#### SaaS — Feature Usage

```dart
// GOOD: Track feature usage with context
void trackFeatureUsed(String featureName, {Map<String, dynamic>? context}) {
  final properties = <String, dynamic>{
    'feature_name': featureName,
    'feature_category': getFeatureCategory(featureName),
    'is_first_use': !hasUsedFeature(featureName),
    'times_used_total': getTotalUsageCount(featureName),
    'entry_point': currentRoute,
  };
  
  // Merge additional context
  if (context != null) {
    properties.addAll(context);
  }
  
  FS.event(name: 'Feature Used', properties: properties);
}

// Usage
trackFeatureUsed('advanced_export', context: {
  'export_format': 'csv',
  'row_count': 1500,
});
```

#### Subscription Events

```dart
// GOOD: Track subscription lifecycle
class SubscriptionTracker {
  
  void trackTrialStarted(Trial trial) {
    FS.event(name: 'Trial Started', properties: {
      'trial_plan': trial.plan,
      'trial_duration_days': trial.durationDays,
      'source': trial.acquisitionSource,
      'started_at': DateTime.now().toIso8601String(),
    });
  }
  
  void trackSubscriptionStarted(Subscription subscription) {
    FS.event(name: 'Subscription Started', properties: {
      'plan_name': subscription.plan,
      'plan_tier': subscription.tier,
      'billing_cycle': subscription.billingCycle,
      'price': subscription.price,
      'currency': subscription.currency,
      'mrr': subscription.mrr,
      'trial_converted': subscription.wasTrialing,
      'payment_method': subscription.paymentMethod,
    });
  }
  
  void trackPlanChanged(Plan oldPlan, Plan newPlan) {
    final changeType = newPlan.price > oldPlan.price ? 'upgrade' : 'downgrade';
    
    FS.event(name: 'Plan Changed', properties: {
      'from_plan': oldPlan.name,
      'to_plan': newPlan.name,
      'from_price': oldPlan.price,
      'to_price': newPlan.price,
      'price_change': newPlan.price - oldPlan.price,
      'change_type': changeType,
    });
  }
}
```

#### Widget Integration

```dart
// GOOD: StatefulWidget with event tracking
class ProductDetailScreen extends StatefulWidget {
  final Product product;
  
  const ProductDetailScreen({required this.product});
  
  @override
  State<ProductDetailScreen> createState() => _ProductDetailScreenState();
}

class _ProductDetailScreenState extends State<ProductDetailScreen> {
  int quantity = 1;
  
  @override
  void initState() {
    super.initState();
    _trackProductViewed();
  }
  
  void _trackProductViewed() {
    FS.event(name: 'Product Viewed', properties: {
      'product_id': widget.product.id,
      'name': widget.product.name,
      'category': widget.product.category,
      'price': widget.product.price,
    });
  }
  
  void _addToCart() {
    CartManager.instance.add(widget.product, quantity);
    
    FS.event(name: 'Product Added', properties: {
      'product_id': widget.product.id,
      'name': widget.product.name,
      'price': widget.product.price,
      'quantity': quantity,
    });
  }
  
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Product info...
        ElevatedButton(
          onPressed: _addToCart,
          child: const Text('Add to Cart'),
        ),
      ],
    );
  }
}
```

### ❌ BAD Implementation Examples

```dart
// BAD: Generic event name
FS.event(name: 'tap', properties: {'button': 'cart'});

// BAD: Missing critical properties
FS.event(name: 'Order Completed', properties: {'success': true});

// BAD: Wrong types (strings instead of numbers)
FS.event(name: 'Product Added', properties: {
  'price': '\$49.99',  // Should be 49.99
  'quantity': '3',     // Should be 3
});
```

---

## React Native

### API Reference

```javascript
import FullStory from '@fullstory/react-native';

// Basic syntax
FullStory.event(name: string, properties: object);
```

### ✅ GOOD Implementation Examples

#### E-commerce — Product Added

```javascript
// GOOD: Comprehensive product add event
function trackProductAdded(product, quantity, source) {
  FullStory.event('Product Added', {
    // Product identification
    product_id: product.id,
    sku: product.sku,
    name: product.name,
    brand: product.brand,
    
    // Categorization
    category: product.category,
    subcategory: product.subcategory || '',
    
    // Pricing
    price: product.price,  // number
    currency: 'USD',
    
    // Cart context
    quantity: quantity,  // number
    cart_id: getCartId(),
    
    // Attribution
    position: product.listPosition,
    list_name: source,
    
    // Product attributes
    variant: product.selectedVariant || '',
    size: product.selectedSize || '',
    color: product.selectedColor || '',
  });
}
```

#### SaaS — Feature Usage

```javascript
// GOOD: Track feature usage with context
function trackFeatureUsed(featureName, context = {}) {
  FullStory.event('Feature Used', {
    feature_name: featureName,
    feature_category: getFeatureCategory(featureName),
    is_first_use: !hasUsedFeature(featureName),
    times_used_total: getTotalUsageCount(featureName),
    entry_point: currentScreen,
    ...context,
  });
}

// Usage
trackFeatureUsed('advanced_export', {
  export_format: 'csv',
  row_count: 1500,
});
```

#### Subscription Events

```javascript
// GOOD: Track subscription lifecycle
class SubscriptionTracker {
  
  trackTrialStarted(trial) {
    FullStory.event('Trial Started', {
      trial_plan: trial.plan,
      trial_duration_days: trial.durationDays,
      source: trial.acquisitionSource,
      started_at: new Date().toISOString(),
    });
  }
  
  trackSubscriptionStarted(subscription) {
    FullStory.event('Subscription Started', {
      plan_name: subscription.plan,
      plan_tier: subscription.tier,
      billing_cycle: subscription.billingCycle,
      price: subscription.price,
      currency: subscription.currency,
      mrr: subscription.mrr,
      trial_converted: subscription.wasTrialing,
      payment_method: subscription.paymentMethod,
    });
  }
  
  trackPlanChanged(oldPlan, newPlan) {
    const changeType = newPlan.price > oldPlan.price ? 'upgrade' : 'downgrade';
    
    FullStory.event('Plan Changed', {
      from_plan: oldPlan.name,
      to_plan: newPlan.name,
      from_price: oldPlan.price,
      to_price: newPlan.price,
      price_change: newPlan.price - oldPlan.price,
      change_type: changeType,
    });
  }
}
```

#### React Native Component Integration

```jsx
// GOOD: Functional component with event tracking
import React, { useEffect, useState } from 'react';
import { View, Button } from 'react-native';
import FullStory from '@fullstory/react-native';

function ProductDetailScreen({ product }) {
  const [quantity, setQuantity] = useState(1);
  
  useEffect(() => {
    // Track product view on mount
    FullStory.event('Product Viewed', {
      product_id: product.id,
      name: product.name,
      category: product.category,
      price: product.price,
    });
  }, [product.id]);
  
  const handleAddToCart = () => {
    CartManager.add(product, quantity);
    
    FullStory.event('Product Added', {
      product_id: product.id,
      name: product.name,
      price: product.price,
      quantity: quantity,
    });
  };
  
  return (
    <View>
      {/* Product info... */}
      <Button title="Add to Cart" onPress={handleAddToCart} />
    </View>
  );
}
```

#### Custom Hook

```javascript
// GOOD: Reusable event tracking hook
import { useCallback } from 'react';
import FullStory from '@fullstory/react-native';

export function useEventTracker() {
  const track = useCallback((name, properties) => {
    FullStory.event(name, properties);
  }, []);
  
  const trackWithTiming = useCallback((name, startTime, properties = {}) => {
    const duration = Date.now() - startTime;
    FullStory.event(name, {
      ...properties,
      duration_ms: duration,
    });
  }, []);
  
  return { track, trackWithTiming };
}

// Usage
function CheckoutScreen() {
  const { track, trackWithTiming } = useEventTracker();
  const [startTime] = useState(Date.now());
  
  const handleComplete = (order) => {
    trackWithTiming('Checkout Completed', startTime, {
      order_id: order.id,
      revenue: order.total,
    });
  };
  
  return <CheckoutForm onComplete={handleComplete} />;
}
```

### ❌ BAD Implementation Examples

```javascript
// BAD: Generic event name
FullStory.event('tap', { button: 'cart' });

// BAD: Missing critical properties
FullStory.event('Order Completed', { success: true });

// BAD: Wrong types (strings instead of numbers)
FullStory.event('Product Added', {
  price: '$49.99',  // Should be 49.99
  quantity: '3',    // Should be 3
});

// BAD: Tracking on every render
function BadComponent({ product }) {
  // This fires on EVERY render!
  FullStory.event('Product Viewed', { product_id: product.id });
  
  return <View>...</View>;
}
```

---

## Common Patterns (All Platforms)

### Event Tracking Service

Create a centralized service to standardize event tracking across your app:

| Platform | Pattern |
|----------|---------|
| iOS | Singleton class with static methods |
| Android | Object/companion object or Hilt-injected class |
| Flutter | Singleton or Provider/Riverpod |
| React Native | Custom hook or context provider |

### Timed Events

Track duration for events like video watching or form completion:

```
1. Store start time when action begins
2. Calculate duration when action completes
3. Include duration_ms in properties
4. Include completed: true/false for completion status
```

### Funnel Tracking

For multi-step flows (checkout, onboarding):

```
1. Track "{Funnel} Started" with entry context
2. Track "{Funnel} Step Completed" for each step with:
   - step_number
   - step_name
   - step_duration_ms
   - time_in_funnel_ms
3. Track "{Funnel} Completed" or "{Funnel} Abandoned"
```

---

## Reference Links

- **iOS**: https://developer.fullstory.com/mobile/ios/capture-events/analytics-events/
- **Android**: https://developer.fullstory.com/mobile/android/capture-events/analytics-events/
- **Flutter**: https://developer.fullstory.com/mobile/flutter/capture-events/analytics-events/
- **React Native**: https://developer.fullstory.com/mobile/react-native/capture-events/analytics-events/
