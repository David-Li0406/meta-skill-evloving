---
name: fullstory-test-automation-mobile
version: v3
description: >
  MOBILE PLATFORM FILE — Part of fullstory-test-automation skill.
  Mobile test automation patterns for Fullstory-decorated codebases.
  Covers React Native (Detox), Android (Espresso), iOS (XCUITest),
  Flutter (integration_test), Appium, and Maestro.
  Read SKILL.md first for discovery and analysis.
platforms: [ios, android, flutter, react-native]
parent_skill: fullstory-test-automation
related_skills:
  - fullstory-stable-selectors
  - fullstory-element-properties
  - mobile-instrumentation-orchestrator
  - fullstory-privacy-controls
---

# Fullstory Test Automation - Mobile

**Prerequisites:** Read `SKILL.md` first for discovery, analysis, and decoration maturity assessment.

This skill covers mobile test automation frameworks:
- **Detox** — React Native
- **Espresso** — Android Native
- **XCUITest** — iOS Native
- **Flutter integration_test** — Flutter
- **Appium** — Cross-platform
- **Maestro** — Modern cross-platform

---

## MOBILE ACCESSIBILITY ID MAPPING

When following Fullstory mobile decoration patterns, map attributes to native accessibility identifiers:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  FULLSTORY DECORATION → MOBILE ACCESSIBILITY IDs                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  React Native                                                                │
│  ├── data-element → testID="element-name"                                   │
│  ├── data-component → testID="ComponentName"                                │
│  └── data-fs-element → accessibilityLabel="Element Name"                    │
│                                                                             │
│  Android (Native)                                                            │
│  ├── data-element → android:contentDescription="element-name"               │
│  ├── data-element → resource-id (via view tag)                              │
│  └── data-fs-element → contentDescription="Element Name"                    │
│                                                                             │
│  iOS (Native)                                                                │
│  ├── data-element → accessibilityIdentifier="element-name"                  │
│  └── data-fs-element → accessibilityLabel="Element Name"                    │
│                                                                             │
│  Flutter                                                                     │
│  ├── data-element → Key('element-name')                                     │
│  └── data-fs-element → Semantics(label: "Element Name")                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## REACT NATIVE (DETOX)

### Source Code Decoration

```tsx
// React Native component with Fullstory + testID decoration
import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';

interface ProductCardProps {
  product: {
    id: string;
    name: string;
    price: number;
  };
  onAddToCart: () => void;
}

export function ProductCard({ product, onAddToCart }: ProductCardProps) {
  return (
    <View
      // Fullstory decoration
      data-component="ProductCard"
      data-fs-element="Product Card"
      data-product-id={product.id}
      // Test automation ID
      testID="product-card"
      accessibilityLabel={`Product: ${product.name}`}
    >
      <Text
        data-element="product-name"
        testID="product-name"
      >
        {product.name}
      </Text>
      
      <Text
        data-element="product-price"
        testID="product-price"
        data-price={product.price}
      >
        ${product.price}
      </Text>
      
      <TouchableOpacity
        data-element="add-to-cart"
        data-action="add-to-cart"
        testID="add-to-cart-button"
        accessibilityLabel="Add to cart"
        accessibilityRole="button"
        onPress={onAddToCart}
      >
        <Text>Add to Cart</Text>
      </TouchableOpacity>
    </View>
  );
}
```

### Detox Test

```typescript
// e2e/checkout.test.ts
import { device, element, by, expect } from 'detox';

describe('Checkout Flow', () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  beforeEach(async () => {
    await device.reloadReactNative();
  });

  it('should add product to cart', async () => {
    // Navigate to product using testID (aligned with data-element)
    await element(by.id('product-card')).tap();
    
    // Verify product details
    await expect(element(by.id('product-name'))).toBeVisible();
    await expect(element(by.id('product-price'))).toHaveText('$99.99');
    
    // Add to cart using data-action aligned selector
    await element(by.id('add-to-cart-button')).tap();
    
    // Verify cart updated
    await expect(element(by.id('cart-badge'))).toHaveText('1');
  });

  it('should complete checkout', async () => {
    // Navigate to checkout
    await element(by.id('cart-button')).tap();
    await element(by.id('checkout-button')).tap();
    
    // Fill shipping info
    await element(by.id('shipping-first-name')).typeText('John');
    await element(by.id('shipping-last-name')).typeText('Test');
    await element(by.id('shipping-address')).typeText('123 Test St');
    await element(by.id('shipping-city')).typeText('Testville');
    await element(by.id('shipping-zip')).typeText('12345');
    
    // Scroll to payment section
    await element(by.id('checkout-form')).scroll(300, 'down');
    
    // Fill payment (test data)
    await element(by.id('card-number')).typeText('4111111111111111');
    await element(by.id('card-expiry')).typeText('12/25');
    await element(by.id('card-cvv')).typeText('123');
    
    // Submit order
    await element(by.id('submit-order-button')).tap();
    
    // Verify confirmation
    await expect(element(by.id('confirmation-screen'))).toBeVisible();
  });
});
```

### Detox Selector Helpers

```typescript
// e2e/helpers/selectors.ts

import { by } from 'detox';

/**
 * Fullstory-aligned selectors for Detox
 * Maps data-element naming to testID
 */
export const Selectors = {
  // By element name (testID)
  element: (name: string) => by.id(name),
  
  // By accessibility label (data-fs-element)
  label: (text: string) => by.label(text),
  
  // By text content
  text: (text: string) => by.text(text),
  
  // Common patterns
  button: (name: string) => by.id(`${name}-button`),
  input: (name: string) => by.id(name),
};

// Usage
await element(Selectors.element('add-to-cart')).tap();
await element(Selectors.button('submit-order')).tap();
```

---

## ANDROID NATIVE (ESPRESSO)

### Source Code Decoration

```xml
<!-- Android XML layout with Fullstory + contentDescription decoration -->
<LinearLayout
    android:id="@+id/product_card"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:contentDescription="Product Card"
    android:tag="data-component:ProductCard">

    <TextView
        android:id="@+id/product_name"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:contentDescription="product-name"
        android:tag="data-element:product-name" />

    <TextView
        android:id="@+id/product_price"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:contentDescription="product-price"
        android:tag="data-element:product-price" />

    <Button
        android:id="@+id/add_to_cart_button"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Add to Cart"
        android:contentDescription="add-to-cart"
        android:tag="data-element:add-to-cart;data-action:add-to-cart" />

</LinearLayout>
```

### Kotlin Decoration Helper

```kotlin
// Kotlin view decoration extension
fun View.setFullstoryDecoration(
    component: String? = null,
    element: String? = null,
    action: String? = null,
    fsElement: String? = null
) {
    val tags = mutableListOf<String>()
    component?.let { tags.add("data-component:$it") }
    element?.let { tags.add("data-element:$it") }
    action?.let { tags.add("data-action:$it") }
    
    tag = tags.joinToString(";")
    
    // Set contentDescription for Espresso accessibility
    contentDescription = element ?: fsElement ?: component
    
    // Apply Fullstory attributes
    element?.let { FS.setAttribute(this, "data-element", it) }
    component?.let { FS.setAttribute(this, "data-component", it) }
    action?.let { FS.setAttribute(this, "data-action", it) }
    fsElement?.let { FS.setAttribute(this, "data-fs-element", it) }
}

// Usage
binding.addToCartButton.setFullstoryDecoration(
    element = "add-to-cart",
    action = "add-to-cart",
    fsElement = "Add to Cart Button"
)
```

### Espresso Test

```kotlin
// androidTest/java/com/example/app/CheckoutTest.kt

import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.action.ViewActions.*
import androidx.test.espresso.assertion.ViewAssertions.matches
import androidx.test.espresso.matcher.ViewMatchers.*
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class CheckoutTest {

    @Test
    fun testAddToCart() {
        // Navigate to product using contentDescription (aligned with data-element)
        onView(withContentDescription("product-card"))
            .perform(click())
        
        // Verify product details
        onView(withContentDescription("product-name"))
            .check(matches(isDisplayed()))
        
        onView(withContentDescription("product-price"))
            .check(matches(withText("$99.99")))
        
        // Add to cart
        onView(withContentDescription("add-to-cart"))
            .perform(click())
        
        // Verify cart badge
        onView(withContentDescription("cart-badge"))
            .check(matches(withText("1")))
    }

    @Test
    fun testCompleteCheckout() {
        // Navigate to checkout
        onView(withContentDescription("cart-button")).perform(click())
        onView(withContentDescription("checkout-button")).perform(click())
        
        // Fill shipping info
        onView(withContentDescription("shipping-first-name"))
            .perform(typeText("John"), closeSoftKeyboard())
        
        onView(withContentDescription("shipping-last-name"))
            .perform(typeText("Test"), closeSoftKeyboard())
        
        onView(withContentDescription("shipping-address"))
            .perform(typeText("123 Test St"), closeSoftKeyboard())
        
        onView(withContentDescription("shipping-city"))
            .perform(typeText("Testville"), closeSoftKeyboard())
        
        onView(withContentDescription("shipping-zip"))
            .perform(typeText("12345"), closeSoftKeyboard())
        
        // Fill payment
        onView(withContentDescription("card-number"))
            .perform(typeText("4111111111111111"), closeSoftKeyboard())
        
        onView(withContentDescription("card-expiry"))
            .perform(typeText("12/25"), closeSoftKeyboard())
        
        onView(withContentDescription("card-cvv"))
            .perform(typeText("123"), closeSoftKeyboard())
        
        // Submit order
        onView(withContentDescription("submit-order"))
            .perform(click())
        
        // Verify confirmation screen
        onView(withContentDescription("confirmation-screen"))
            .check(matches(isDisplayed()))
    }
}
```

### Espresso Test Data Tracking

```kotlin
// Helper for tracking test inputs in masked fields
class TestInputTracker {
    companion object {
        fun trackInput(fieldName: String, value: String, testName: String) {
            if (!BuildConfig.IS_TEST_AUTOMATION) return
            
            FullStory.track("Test Automation Input", mapOf(
                "field_name" to fieldName,
                "field_value" to value,
                "platform" to "android",
                "test_name" to testName
            ))
        }
    }
}

// Usage in test
onView(withContentDescription("card-number"))
    .perform(typeText("4111111111111111"))
TestInputTracker.trackInput("card-number", "4111111111111111", "testCompleteCheckout")
```

---

## iOS NATIVE (XCUITEST)

### Source Code Decoration

```swift
// Swift view decoration extension
extension UIView {
    func setFullstoryDecoration(
        component: String? = nil,
        element: String? = nil,
        action: String? = nil,
        fsElement: String? = nil
    ) {
        // Set accessibilityIdentifier for XCUITest
        accessibilityIdentifier = element ?? component
        
        // Set accessibilityLabel for VoiceOver and alternative lookup
        if let fsEl = fsElement {
            accessibilityLabel = fsEl
        }
        
        // Apply Fullstory attributes
        if let el = element {
            FS.setAttribute(self, attributeName: "data-element", attributeValue: el)
        }
        if let comp = component {
            FS.setAttribute(self, attributeName: "data-component", attributeValue: comp)
        }
        if let act = action {
            FS.setAttribute(self, attributeName: "data-action", attributeValue: act)
        }
        if let fsEl = fsElement {
            FS.setAttribute(self, attributeName: "data-fs-element", attributeValue: fsEl)
        }
    }
}

// Usage in ViewDidLoad
addToCartButton.setFullstoryDecoration(
    element: "add-to-cart",
    action: "add-to-cart",
    fsElement: "Add to Cart Button"
)
```

### XCUITest

```swift
// CheckoutUITests/CheckoutTests.swift

import XCTest

class CheckoutTests: XCTestCase {
    
    let app = XCUIApplication()
    
    override func setUpWithError() throws {
        continueAfterFailure = false
        app.launch()
    }
    
    func testAddToCart() throws {
        // Navigate to product using accessibilityIdentifier (aligned with data-element)
        app.otherElements["product-card"].tap()
        
        // Verify product details
        XCTAssertTrue(app.staticTexts["product-name"].exists)
        XCTAssertEqual(app.staticTexts["product-price"].label, "$99.99")
        
        // Add to cart
        app.buttons["add-to-cart"].tap()
        
        // Verify cart badge
        XCTAssertEqual(app.staticTexts["cart-badge"].label, "1")
    }
    
    func testCompleteCheckout() throws {
        // Navigate to checkout
        app.buttons["cart-button"].tap()
        app.buttons["checkout-button"].tap()
        
        // Fill shipping info
        let shippingFirstName = app.textFields["shipping-first-name"]
        shippingFirstName.tap()
        shippingFirstName.typeText("John")
        
        let shippingLastName = app.textFields["shipping-last-name"]
        shippingLastName.tap()
        shippingLastName.typeText("Test")
        
        let shippingAddress = app.textFields["shipping-address"]
        shippingAddress.tap()
        shippingAddress.typeText("123 Test St")
        
        let shippingCity = app.textFields["shipping-city"]
        shippingCity.tap()
        shippingCity.typeText("Testville")
        
        let shippingZip = app.textFields["shipping-zip"]
        shippingZip.tap()
        shippingZip.typeText("12345")
        
        // Fill payment
        let cardNumber = app.textFields["card-number"]
        cardNumber.tap()
        cardNumber.typeText("4111111111111111")
        
        let cardExpiry = app.textFields["card-expiry"]
        cardExpiry.tap()
        cardExpiry.typeText("12/25")
        
        let cardCvv = app.secureTextFields["card-cvv"]
        cardCvv.tap()
        cardCvv.typeText("123")
        
        // Submit order
        app.buttons["submit-order"].tap()
        
        // Verify confirmation screen
        XCTAssertTrue(app.otherElements["confirmation-screen"].waitForExistence(timeout: 5))
    }
}
```

### XCUITest Data Tracking

```swift
// iOS XCUITest helper
class TestInputTracker {
    static func track(field: String, value: String, testName: String) {
        #if DEBUG
        guard ProcessInfo.processInfo.environment["IS_TEST_AUTOMATION"] == "true" else { return }
        
        FS.track("Test Automation Input", properties: [
            "field_name": field,
            "field_value": value,
            "platform": "ios",
            "test_name": testName
        ])
        #endif
    }
}

// Usage in test
let cardNumber = app.textFields["card-number"]
cardNumber.typeText("4111111111111111")
TestInputTracker.track(field: "card-number", value: "4111111111111111", testName: name)
```

---

## FLUTTER

### Source Code Decoration

```dart
// Flutter widget with Key and Semantics decoration
import 'package:flutter/material.dart';

class ProductCard extends StatelessWidget {
  final Product product;
  final VoidCallback onAddToCart;
  
  const ProductCard({
    Key? key,
    required this.product,
    required this.onAddToCart,
  }) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: 'Product Card: ${product.name}',
      child: Container(
        key: const Key('product-card'),
        child: Column(
          children: [
            Text(
              product.name,
              key: const Key('product-name'),
              semanticsLabel: 'Product name: ${product.name}',
            ),
            Text(
              '\$${product.price}',
              key: const Key('product-price'),
              semanticsLabel: 'Price: \$${product.price}',
            ),
            ElevatedButton(
              key: const Key('add-to-cart'),
              onPressed: onAddToCart,
              child: Semantics(
                label: 'Add to cart',
                button: true,
                child: const Text('Add to Cart'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

### Flutter Integration Test

```dart
// integration_test/checkout_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:my_app/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Checkout Flow', () {
    testWidgets('should add product to cart', (tester) async {
      app.main();
      await tester.pumpAndSettle();
      
      // Navigate to product using Key (aligned with data-element)
      await tester.tap(find.byKey(const Key('product-card')));
      await tester.pumpAndSettle();
      
      // Verify product details
      expect(find.byKey(const Key('product-name')), findsOneWidget);
      expect(find.byKey(const Key('product-price')), findsWidgets);
      
      // Add to cart
      await tester.tap(find.byKey(const Key('add-to-cart')));
      await tester.pumpAndSettle();
      
      // Verify cart badge
      expect(find.byKey(const Key('cart-badge')), findsOneWidget);
    });

    testWidgets('should complete checkout', (tester) async {
      app.main();
      await tester.pumpAndSettle();
      
      // Navigate to checkout
      await tester.tap(find.byKey(const Key('cart-button')));
      await tester.pumpAndSettle();
      await tester.tap(find.byKey(const Key('checkout-button')));
      await tester.pumpAndSettle();
      
      // Fill shipping info
      await tester.enterText(
        find.byKey(const Key('shipping-first-name')),
        'John',
      );
      await tester.enterText(
        find.byKey(const Key('shipping-last-name')),
        'Test',
      );
      await tester.enterText(
        find.byKey(const Key('shipping-address')),
        '123 Test St',
      );
      await tester.enterText(
        find.byKey(const Key('shipping-city')),
        'Testville',
      );
      await tester.enterText(
        find.byKey(const Key('shipping-zip')),
        '12345',
      );
      
      // Scroll to payment section
      await tester.drag(
        find.byKey(const Key('checkout-form')),
        const Offset(0, -300),
      );
      await tester.pumpAndSettle();
      
      // Fill payment
      await tester.enterText(
        find.byKey(const Key('card-number')),
        '4111111111111111',
      );
      await tester.enterText(
        find.byKey(const Key('card-expiry')),
        '12/25',
      );
      await tester.enterText(
        find.byKey(const Key('card-cvv')),
        '123',
      );
      
      // Submit order
      await tester.tap(find.byKey(const Key('submit-order')));
      await tester.pumpAndSettle();
      
      // Verify confirmation screen
      expect(find.byKey(const Key('confirmation-screen')), findsOneWidget);
    });
  });
}
```

---

## APPIUM (CROSS-PLATFORM)

### Selector Helpers

```javascript
// appium/helpers/selectors.js

/**
 * Fullstory-aligned Appium selectors (cross-platform)
 */
class FullstorySelectors {
  constructor(driver, platform) {
    this.driver = driver;
    this.platform = platform; // 'ios' | 'android' | 'web'
  }
  
  // Get element by Fullstory element name
  async element(name) {
    switch (this.platform) {
      case 'ios':
        return this.driver.$(`~${name}`); // accessibilityIdentifier
      case 'android':
        return this.driver.$(`~${name}`); // contentDescription
      case 'web':
        return this.driver.$(`[data-element="${name}"]`);
    }
  }
  
  // Get element by testID (React Native)
  async testId(id) {
    switch (this.platform) {
      case 'ios':
        return this.driver.$(`~${id}`);
      case 'android':
        return this.driver.$(`~${id}`);
      case 'web':
        return this.driver.$(`[data-testid="${id}"]`);
    }
  }
  
  // Get element by accessibility label
  async label(text) {
    switch (this.platform) {
      case 'ios':
        return this.driver.$(`~${text}`);
      case 'android':
        return this.driver.$(`android=new UiSelector().description("${text}")`);
      case 'web':
        return this.driver.$(`[aria-label="${text}"]`);
    }
  }
}

// Usage in Appium test
const sel = new FullstorySelectors(driver, 'android');

describe('Checkout Flow', () => {
  it('should add product to cart', async () => {
    await (await sel.element('product-card')).click();
    await (await sel.element('add-to-cart')).click();
    await expect(await sel.element('cart-badge')).toHaveText('1');
  });
});
```

---

## MAESTRO

Maestro is particularly well-suited for Fullstory-decorated apps because it supports direct testID and accessibility label targeting.

### Flow File

```yaml
# maestro/flows/checkout.yaml

appId: com.example.myapp

---
# Add product to cart flow
- launchApp

# Navigate to product (using testID aligned with data-element)
- tapOn:
    id: "product-card"

# Verify product details
- assertVisible:
    id: "product-name"

- assertVisible:
    id: "product-price"
    text: "$99.99"

# Add to cart
- tapOn:
    id: "add-to-cart"

# Verify cart badge
- assertVisible:
    id: "cart-badge"
    text: "1"

---
# Complete checkout flow
- tapOn:
    id: "cart-button"

- tapOn:
    id: "checkout-button"

# Fill shipping info
- tapOn:
    id: "shipping-first-name"
- inputText: "John"

- tapOn:
    id: "shipping-last-name"  
- inputText: "Test"

- tapOn:
    id: "shipping-address"
- inputText: "123 Test St"

- tapOn:
    id: "shipping-city"
- inputText: "Testville"

- tapOn:
    id: "shipping-zip"
- inputText: "12345"

# Scroll to payment
- scroll:
    direction: DOWN

# Fill payment
- tapOn:
    id: "card-number"
- inputText: "4111111111111111"

- tapOn:
    id: "card-expiry"
- inputText: "12/25"

- tapOn:
    id: "card-cvv"
- inputText: "123"

# Submit order
- tapOn:
    id: "submit-order"

# Verify confirmation
- assertVisible:
    id: "confirmation-screen"
```

### Maestro with Accessibility Labels

```yaml
# Using accessibility labels for better readability
- tapOn:
    label: "Add to Cart"

- assertVisible:
    label: "Order Confirmation"
    
# Using testID for precise targeting
- tapOn:
    id: "submit-order-button"
```

---

## BEST PRACTICES (MOBILE)

### ✅ DO

- Use consistent `testID` / `accessibilityIdentifier` / `Key` naming
- Align mobile IDs with web `data-element` names for cross-platform consistency
- Set `accessibilityLabel` for human-readable test assertions
- Use platform-specific helpers to abstract selector differences

### ❌ DON'T

- Use platform-specific selectors when cross-platform is needed
- Rely on view hierarchy position
- Use text matchers for dynamic content
- Forget to set accessibility properties (breaks both tests and screen readers)

---

## REFERENCE LINKS

### This Skill's Files
- **Core (Discovery & Routing)**: `./SKILL.md`
- **Web Platform**: `./SKILL-WEB.md`

### Fullstory Skills
- **Stable Selectors**: ../fullstory-stable-selectors/SKILL.md
- **Mobile Instrumentation Orchestrator**: ../../meta/mobile-instrumentation-orchestrator/SKILL.md
- **Element Properties**: ../../core/fullstory-element-properties/SKILL.md
- **Privacy Controls**: ../../core/fullstory-privacy-controls/SKILL.md

### Framework Documentation
- **Detox**: https://wix.github.io/Detox/
- **Espresso**: https://developer.android.com/training/testing/espresso
- **XCUITest**: https://developer.apple.com/documentation/xctest
- **Flutter Testing**: https://docs.flutter.dev/testing
- **Appium**: https://appium.io/docs/en/
- **Maestro**: https://maestro.mobile.dev/

---

*This file covers mobile test automation. For web, see `./SKILL-WEB.md`. For discovery and analysis, see `./SKILL.md`.*
