---
name: fullstory-stable-selectors-mobile
version: v3
platforms: [ios, android, flutter, react-native]
sdks: [fullstory-swift, fullstory-android, fullstory-flutter, fullstory-react-native]
description: Mobile implementation guide for stable selectors across iOS (accessibilityIdentifier), Android (testTag, contentDescription), Flutter (Key, Semantics), and React Native (testID). Enables reliable element identification for Fullstory search, test automation, and CUA compatibility.
parent_skill: fullstory-stable-selectors
related_skills:
  - fullstory-element-properties
  - fullstory-privacy-controls
  - fullstory-test-automation
  - mobile-instrumentation-orchestrator
---

# Fullstory Stable Selectors — Mobile Implementation

> **📚 Core Concepts**: See [SKILL.md](./SKILL.md) for naming conventions, taxonomy, and platform-agnostic principles.
> **🌐 Web Implementation**: See [SKILL-WEB.md](./SKILL-WEB.md) for JavaScript/TypeScript with data-* attributes.

---

## Overview

This guide covers implementing stable selectors in **mobile applications** across all major platforms. Each platform has its own mechanism for adding stable identifiers, but the naming conventions and principles from SKILL.md apply universally.

---

## Quick Reference

| Platform | Primary Mechanism | Secondary | Example |
|----------|------------------|-----------|---------|
| **iOS (Swift)** | `accessibilityIdentifier` | — | `button.accessibilityIdentifier = "ProductCard.add-to-cart"` |
| **iOS (SwiftUI)** | `.accessibilityIdentifier()` | — | `.accessibilityIdentifier("ProductCard.add-to-cart")` |
| **Android (Kotlin)** | `contentDescription` | `android:tag` | `android:contentDescription="ProductCard.add-to-cart"` |
| **Android (Compose)** | `Modifier.testTag()` | `semantics {}` | `Modifier.testTag("ProductCard.add-to-cart")` |
| **React Native** | `testID` | `accessibilityLabel` | `testID="ProductCard.add-to-cart"` |
| **Flutter** | `Key` | `Semantics` | `Key('ProductCard.add-to-cart')` |

---

## Mobile-Specific Problem

### Dynamic View IDs

Unlike web where CSS classes are the problem, mobile has different sources of instability:

```
iOS View Hierarchy (Unstable):
UIButton (0x7f8b4c0123a0)         ← Memory address, changes every launch
  └── UIButtonLabel

Android View Tree (Unstable):
Button
  android:id="@+id/button1"        ← Often auto-generated or non-descriptive
  
React Native Bridge (Unstable):
RCTButton (nativeID: rn_42)       ← Bridge-generated, changes on re-render
```

**Sources of instability:**
- ❌ Memory addresses (change every launch)
- ❌ Auto-generated view IDs
- ❌ Framework-internal identifiers
- ❌ Position in view hierarchy (changes with layout)
- ❌ Index-based identification (changes with list order)

---

## The Solution: Platform-Specific Stable Identifiers

Add semantic identifiers using each platform's native mechanism:

```
iOS:        accessibilityIdentifier = "ProductCard.add-to-cart"
Android:    testTag("ProductCard.add-to-cart")
Flutter:    Key('ProductCard.add-to-cart')
RN:         testID="ProductCard.add-to-cart"
```

**Convention**: Use dot notation `Component.element` to combine component and element identifiers into a single string.

---

## iOS

### UIKit

```swift
// ProductCardView.swift
class ProductCardView: UIView {
    
    private let productImageView: UIImageView = {
        let imageView = UIImageView()
        imageView.accessibilityIdentifier = "ProductCard.product-image"
        return imageView
    }()
    
    private let productNameLabel: UILabel = {
        let label = UILabel()
        label.accessibilityIdentifier = "ProductCard.product-name"
        return label
    }()
    
    private let priceLabel: UILabel = {
        let label = UILabel()
        label.accessibilityIdentifier = "ProductCard.price"
        return label
    }()
    
    private let addToCartButton: UIButton = {
        let button = UIButton(type: .system)
        button.accessibilityIdentifier = "ProductCard.add-to-cart"
        button.accessibilityLabel = "Add to Cart"  // For screen readers
        return button
    }()
    
    override init(frame: CGRect) {
        super.init(frame: frame)
        accessibilityIdentifier = "ProductCard"
        setupViews()
    }
    
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
}
```

#### UIKit Helper Extension

```swift
// StableIdentifier.swift
extension UIView {
    /// Sets a stable identifier following Component.element convention
    func setStableIdentifier(component: String, element: String? = nil) {
        if let element = element {
            accessibilityIdentifier = "\(component).\(element)"
        } else {
            accessibilityIdentifier = component
        }
    }
}

// Usage
addToCartButton.setStableIdentifier(component: "ProductCard", element: "add-to-cart")
```

---

### SwiftUI

```swift
// ProductCard.swift
struct ProductCard: View {
    let product: Product
    let onAddToCart: () -> Void
    
    var body: some View {
        VStack {
            AsyncImage(url: product.imageURL)
                .accessibilityIdentifier("ProductCard.product-image")
            
            Text(product.name)
                .accessibilityIdentifier("ProductCard.product-name")
            
            Text(product.formattedPrice)
                .accessibilityIdentifier("ProductCard.price")
            
            Button("Add to Cart") {
                onAddToCart()
            }
            .accessibilityIdentifier("ProductCard.add-to-cart")
            .accessibilityLabel("Add \(product.name) to cart")
        }
        .accessibilityIdentifier("ProductCard")
    }
}
```

#### SwiftUI ViewModifier Helper

```swift
// StableIdentifier.swift
extension View {
    /// Adds stable identifier for Fullstory/testing/CUA
    func stableIdentifier(_ component: String, element: String? = nil) -> some View {
        let identifier = element != nil ? "\(component).\(element!)" : component
        return self.accessibilityIdentifier(identifier)
    }
}

// Usage
Button("Add to Cart") { }
    .stableIdentifier("ProductCard", element: "add-to-cart")
```

---

### iOS ✅ Good Examples

```swift
// ✅ GOOD: Descriptive, hierarchical identifiers
class CheckoutViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        view.accessibilityIdentifier = "CheckoutScreen"
        
        shippingSection.accessibilityIdentifier = "CheckoutScreen.shipping-section"
        addressField.accessibilityIdentifier = "CheckoutScreen.address-input"
        paymentSection.accessibilityIdentifier = "CheckoutScreen.payment-section"
        submitButton.accessibilityIdentifier = "CheckoutScreen.submit-button"
    }
}
```

### iOS ❌ Bad Examples

```swift
// ❌ BAD: Generic or position-based identifiers
button1.accessibilityIdentifier = "button"          // Too generic
button2.accessibilityIdentifier = "button2"         // Position-based
cell.accessibilityIdentifier = "cell_\(indexPath.row)"  // Index changes

// ✅ CORRECTED
addToCartButton.accessibilityIdentifier = "ProductCard.add-to-cart"
submitButton.accessibilityIdentifier = "CheckoutForm.submit-button"
cell.accessibilityIdentifier = "ProductList.product-item.\(product.id)"  // Business ID
```

---

## Android

### Views (XML + Kotlin/Java)

```xml
<!-- product_card.xml -->
<LinearLayout
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:tag="ProductCard">
    
    <ImageView
        android:id="@+id/productImage"
        android:contentDescription="ProductCard.product-image"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content" />
    
    <TextView
        android:id="@+id/productName"
        android:contentDescription="ProductCard.product-name"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content" />
    
    <TextView
        android:id="@+id/price"
        android:contentDescription="ProductCard.price"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content" />
    
    <Button
        android:id="@+id/addToCartButton"
        android:contentDescription="ProductCard.add-to-cart"
        android:text="Add to Cart"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content" />
        
</LinearLayout>
```

```kotlin
// ProductCardView.kt
class ProductCardView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null
) : LinearLayout(context, attrs) {

    init {
        tag = "ProductCard"
        
        // Or set programmatically
        addToCartButton.contentDescription = "ProductCard.add-to-cart"
    }
}
```

---

### Jetpack Compose

```kotlin
// ProductCard.kt
@Composable
fun ProductCard(
    product: Product,
    onAddToCart: () -> Unit
) {
    Column(
        modifier = Modifier.testTag("ProductCard")
    ) {
        AsyncImage(
            model = product.imageUrl,
            contentDescription = "Product image",
            modifier = Modifier.testTag("ProductCard.product-image")
        )
        
        Text(
            text = product.name,
            modifier = Modifier.testTag("ProductCard.product-name")
        )
        
        Text(
            text = product.formattedPrice,
            modifier = Modifier.testTag("ProductCard.price")
        )
        
        Button(
            onClick = onAddToCart,
            modifier = Modifier
                .testTag("ProductCard.add-to-cart")
                .semantics { 
                    contentDescription = "Add ${product.name} to cart"
                }
        ) {
            Text("Add to Cart")
        }
    }
}
```

#### Compose Helper Extensions

```kotlin
// StableIdentifiers.kt
fun Modifier.stableIdentifier(component: String, element: String? = null): Modifier {
    val tag = if (element != null) "$component.$element" else component
    return this.testTag(tag)
}

// Usage
Button(
    onClick = onAddToCart,
    modifier = Modifier.stableIdentifier("ProductCard", "add-to-cart")
) {
    Text("Add to Cart")
}
```

---

### Android ✅ Good Examples

```kotlin
// ✅ GOOD: Compose with descriptive identifiers
@Composable
fun CheckoutScreen() {
    Column(modifier = Modifier.testTag("CheckoutScreen")) {
        ShippingSection(
            modifier = Modifier.testTag("CheckoutScreen.shipping-section")
        )
        PaymentSection(
            modifier = Modifier.testTag("CheckoutScreen.payment-section")
        )
        Button(
            modifier = Modifier.testTag("CheckoutScreen.submit-button")
        ) {
            Text("Place Order")
        }
    }
}
```

### Android ❌ Bad Examples

```kotlin
// ❌ BAD: Generic or index-based
Modifier.testTag("button")                    // Too generic
Modifier.testTag("item_$index")               // Position-based
Modifier.testTag("view1")                     // Non-descriptive

// ✅ CORRECTED
Modifier.testTag("ProductCard.add-to-cart")
Modifier.testTag("ProductList.product-item.${product.id}")
Modifier.testTag("CheckoutForm.submit-button")
```

---

## React Native

### Basic Implementation

```tsx
// ProductCard.tsx
import React from 'react';
import { View, Text, Image, TouchableOpacity } from 'react-native';

interface ProductCardProps {
  product: Product;
  onAddToCart: () => void;
}

export const ProductCard: React.FC<ProductCardProps> = ({ 
  product, 
  onAddToCart 
}) => {
  return (
    <View testID="ProductCard">
      <Image 
        source={{ uri: product.imageUrl }}
        testID="ProductCard.product-image"
        accessibilityLabel={`Image of ${product.name}`}
      />
      
      <Text testID="ProductCard.product-name">
        {product.name}
      </Text>
      
      <Text testID="ProductCard.price">
        {product.formattedPrice}
      </Text>
      
      <TouchableOpacity 
        testID="ProductCard.add-to-cart"
        accessibilityLabel={`Add ${product.name} to cart`}
        accessibilityRole="button"
        onPress={onAddToCart}
      >
        <Text>Add to Cart</Text>
      </TouchableOpacity>
    </View>
  );
};
```

### React Native Helper Hook

```tsx
// useStableIdentifier.ts
export function useStableIdentifier(component: string) {
  return {
    root: { testID: component },
    element: (name: string) => ({ 
      testID: `${component}.${name}` 
    }),
  };
}

// Usage
export const ProductCard: React.FC<Props> = ({ product, onAddToCart }) => {
  const id = useStableIdentifier('ProductCard');
  
  return (
    <View {...id.root}>
      <Image {...id.element('product-image')} source={{ uri: product.imageUrl }} />
      <Text {...id.element('product-name')}>{product.name}</Text>
      <TouchableOpacity {...id.element('add-to-cart')} onPress={onAddToCart}>
        <Text>Add to Cart</Text>
      </TouchableOpacity>
    </View>
  );
};
```

---

### React Native ✅ Good Examples

```tsx
// ✅ GOOD: Clear hierarchy and purpose
const CheckoutScreen: React.FC = () => {
  return (
    <ScrollView testID="CheckoutScreen">
      <View testID="CheckoutScreen.shipping-section">
        <TextInput testID="CheckoutScreen.address-input" />
        <TextInput testID="CheckoutScreen.city-input" />
      </View>
      
      <View testID="CheckoutScreen.payment-section">
        <TextInput testID="CheckoutScreen.card-input" />
      </View>
      
      <TouchableOpacity 
        testID="CheckoutScreen.submit-button"
        accessibilityLabel="Place order"
      >
        <Text>Place Order</Text>
      </TouchableOpacity>
    </ScrollView>
  );
};
```

### React Native ❌ Bad Examples

```tsx
// ❌ BAD: Generic or position-based
<View testID="view" />                         // Too generic
<TouchableOpacity testID="button1" />          // Non-descriptive
<FlatList
  renderItem={({ item, index }) => (
    <View testID={`item-${index}`} />          // Position-based
  )}
/>

// ✅ CORRECTED
<View testID="ProductCard" />
<TouchableOpacity testID="ProductCard.add-to-cart" />
<FlatList
  renderItem={({ item }) => (
    <View testID={`ProductList.product-item.${item.id}`} />  // Business ID
  )}
/>
```

---

## Flutter

### Basic Implementation

```dart
// product_card.dart
import 'package:flutter/material.dart';

class ProductCard extends StatelessWidget {
  final Product product;
  final VoidCallback onAddToCart;

  const ProductCard({
    Key? key,
    required this.product,
    required this.onAddToCart,
  }) : super(key: const Key('ProductCard'));

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Image.network(
          product.imageUrl,
          key: const Key('ProductCard.product-image'),
          semanticsLabel: 'Image of ${product.name}',
        ),
        
        Text(
          product.name,
          key: const Key('ProductCard.product-name'),
        ),
        
        Text(
          product.formattedPrice,
          key: const Key('ProductCard.price'),
        ),
        
        Semantics(
          label: 'Add ${product.name} to cart',
          button: true,
          child: ElevatedButton(
            key: const Key('ProductCard.add-to-cart'),
            onPressed: onAddToCart,
            child: const Text('Add to Cart'),
          ),
        ),
      ],
    );
  }
}
```

### Flutter Helper Extension

```dart
// stable_identifier.dart
extension StableIdentifier on String {
  /// Creates a Key from a stable identifier string
  Key toKey() => Key(this);
}

extension StableIdentifierWidget on Widget {
  /// Wraps widget with a stable identifier Key
  Widget withStableId(String component, [String? element]) {
    final id = element != null ? '$component.$element' : component;
    return KeyedSubtree(
      key: Key(id),
      child: this,
    );
  }
}

// Usage
ElevatedButton(
  onPressed: onAddToCart,
  child: const Text('Add to Cart'),
).withStableId('ProductCard', 'add-to-cart')
```

---

### Flutter ✅ Good Examples

```dart
// ✅ GOOD: Clear hierarchy with Keys
class CheckoutScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: const Key('CheckoutScreen'),
      body: Column(
        children: [
          _ShippingSection(
            key: const Key('CheckoutScreen.shipping-section'),
          ),
          _PaymentSection(
            key: const Key('CheckoutScreen.payment-section'),
          ),
          ElevatedButton(
            key: const Key('CheckoutScreen.submit-button'),
            onPressed: _placeOrder,
            child: const Text('Place Order'),
          ),
        ],
      ),
    );
  }
}
```

### Flutter ❌ Bad Examples

```dart
// ❌ BAD: Auto-generated or index-based keys
ListView.builder(
  itemBuilder: (context, index) => ProductTile(
    key: Key('$index'),           // Index-based, unstable
  ),
)

Container(key: UniqueKey())       // Changes every rebuild!

ElevatedButton(
  key: const Key('button'),       // Too generic
)

// ✅ CORRECTED
ListView.builder(
  itemBuilder: (context, index) => ProductTile(
    key: Key('ProductList.product-item.${products[index].id}'),  // Business ID
    product: products[index],
  ),
)

ElevatedButton(
  key: const Key('ProductCard.add-to-cart'),
)
```

---

## Common Patterns (All Platforms)

### List Items with Business IDs

**Don't use index-based identifiers.** Use business identifiers:

| Platform | Bad | Good |
|----------|-----|------|
| iOS | `cell_\(indexPath.row)` | `ProductList.item.\(product.id)` |
| Android | `item_$index` | `ProductList.item.${product.id}` |
| React Native | `item-${index}` | `ProductList.item.${product.id}` |
| Flutter | `Key('$index')` | `Key('ProductList.item.${product.id}')` |

### Screen/Component Hierarchy

```
Screen (root):         "CheckoutScreen"
  Section:             "CheckoutScreen.shipping-section"
    Input:             "CheckoutScreen.address-input"
    Input:             "CheckoutScreen.city-input"
  Section:             "CheckoutScreen.payment-section"
    Input:             "CheckoutScreen.card-input"
  Button:              "CheckoutScreen.submit-button"
```

### Privacy Integration

Combine stable identifiers with Fullstory privacy controls:

```swift
// iOS - Stable identifier + privacy masking
sensitiveField.accessibilityIdentifier = "ProfileScreen.ssn-input"
sensitiveField.fsClass = ["fs-exclude"]  // Privacy control
```

```kotlin
// Android Compose - Stable identifier + privacy
TextField(
    modifier = Modifier
        .testTag("ProfileScreen.ssn-input")
        .fsClass("fs-exclude")  // Privacy control
)
```

```tsx
// React Native - Stable identifier + privacy
<TextInput 
  testID="ProfileScreen.ssn-input"
  fsClass="fs-exclude"  // Privacy control
/>
```

---

## Troubleshooting

### Identifiers Not Visible in Fullstory

**iOS:**
- Ensure `accessibilityIdentifier` is set (not just `accessibilityLabel`)
- Check that view is in the visible hierarchy
- Verify identifier survives view lifecycle

**Android:**
- For Compose, use `testTag` modifier
- For Views, check `contentDescription` or `tag`
- Ensure ProGuard/R8 isn't stripping identifiers

**React Native:**
- Use `testID` prop (not just `accessibilityLabel`)
- Verify native view receives the prop
- Check for conditional rendering issues

**Flutter:**
- Use `Key` on the widget (not just Semantics)
- Ensure key persists across rebuilds
- Avoid `UniqueKey()` - it changes every rebuild

### Identifiers in Production

**Problem**: Identifiers stripped in release builds

**Solutions by platform:**

| Platform | Solution |
|----------|----------|
| iOS | `accessibilityIdentifier` is NOT stripped in release |
| Android | Keep `testTag` in release; don't use test-only configurations |
| React Native | `testID` is preserved; don't strip in babel config |
| Flutter | `Key` is preserved; don't use debug-only code |

### Too Many Results / Duplicates

**Problem**: Same identifier on multiple elements

**Solution**: Use hierarchical identifiers with unique qualifiers:

```
❌ Bad:  "add-to-cart" (appears in every ProductCard)
✅ Good: "ProductCard.add-to-cart" (scoped to component)
✅ Best: "ProductList.product-item.SKU123.add-to-cart" (fully qualified)
```

---

## KEY TAKEAWAYS FOR AGENT

When helping mobile developers implement stable selectors:

### Platform Detection

First, identify the platform:
1. **iOS (Swift)** → `accessibilityIdentifier`
2. **iOS SwiftUI** → `.accessibilityIdentifier()`
3. **Android (Kotlin)** → `contentDescription` or `tag`
4. **Android Compose** → `Modifier.testTag()`
5. **React Native** → `testID`
6. **Flutter** → `Key()`

### Universal Principles (All Platforms)

1. **Dot notation**: `Component.element` pattern
2. **Business IDs for lists**: `ProductList.item.SKU123` not `item-0`
3. **Purpose over appearance**: `add-to-cart` not `blue-button`
4. **Combine with accessibility**: Stable ID + accessibility label

### Platform-Specific Notes

| Platform | Key Point |
|----------|-----------|
| iOS | `accessibilityIdentifier` ≠ `accessibilityLabel` — use both |
| Android | Compose uses `testTag`; Views use `contentDescription` |
| React Native | `testID` for testing/Fullstory; `accessibilityLabel` for screen readers |
| Flutter | `Key` persists identity; avoid `UniqueKey()` |

### Questions to Ask Developers

1. "What platform/framework are you using?"
2. "Are your view identifiers stable across app launches?"
3. "How do you identify list items—by index or business ID?"
4. "Are you using any E2E testing frameworks?"

### Implementation Checklist (Mobile)

```markdown
□ Set component identifier on screen/view root
□ Set element identifiers on interactive elements
□ Use business IDs for list items (not indices)
□ Combine with accessibility labels for screen readers
□ Verify identifiers in debug tools (Xcode/Android Studio)
□ Test identifiers survive app lifecycle
□ Configure E2E tests to use stable identifiers
```

---

## REFERENCE LINKS

### Fullstory Mobile SDKs
- **iOS SDK**: https://developer.fullstory.com/mobile/ios/
- **Android SDK**: https://developer.fullstory.com/mobile/android/
- **React Native SDK**: https://developer.fullstory.com/mobile/react-native/
- **Flutter SDK**: https://developer.fullstory.com/mobile/flutter/

### Platform Documentation
- **iOS Accessibility**: https://developer.apple.com/accessibility/
- **Android Testing**: https://developer.android.com/training/testing
- **React Native Testing**: https://reactnative.dev/docs/testing-overview
- **Flutter Testing**: https://docs.flutter.dev/testing

### Testing Frameworks
- **Detox (React Native)**: https://wix.github.io/Detox/
- **Espresso (Android)**: https://developer.android.com/training/testing/espresso
- **XCUITest (iOS)**: https://developer.apple.com/documentation/xctest
- **Flutter integration_test**: https://docs.flutter.dev/testing/integration-tests
- **Maestro (Cross-platform)**: https://maestro.mobile.dev/

---

*This skill provides mobile-specific implementation guidance for stable selectors. See SKILL.md for core concepts and SKILL-WEB.md for web implementation.*
