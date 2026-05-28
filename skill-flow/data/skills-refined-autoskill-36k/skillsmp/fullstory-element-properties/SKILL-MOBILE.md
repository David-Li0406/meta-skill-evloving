---
name: fullstory-element-properties-mobile
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
description: Mobile implementation guide for Fullstory's Element Properties API. Includes API reference and code examples for iOS (Swift/SwiftUI), Android (Kotlin/Java), Flutter (Dart), and React Native.
parent_skill: fullstory-element-properties
related_skills:
  - fullstory-element-properties
  - fullstory-page-properties
  - fullstory-analytics-events
---

# Fullstory Element Properties — Mobile Implementation

> **Core Concepts**: See [SKILL.md](./SKILL.md) for property types, inheritance, and best practices.
>
> **Web Implementation**: See [SKILL-WEB.md](./SKILL-WEB.md) for JavaScript/HTML.

---

## Quick Reference

| Platform | SDK | Method |
|----------|-----|--------|
| iOS | `FullStory` | `FS.setAttribute(view:attributeName:attributeValue:)` |
| Android | `FullStory` | `FS.setAttribute(view, attributeName, attributeValue)` |
| Flutter | `fullstory_flutter` | `FS.setAttribute(view: view, name: '', value: '')` |
| React Native | `@fullstory/react-native` | `FullStory.setAttribute(ref, name, value)` |

---

## iOS (Swift/SwiftUI)

### API Reference

```swift
import FullStory

// Basic syntax
FS.setAttribute(view: UIView, attributeName: String, attributeValue: String)
```

**Note**: All attribute values must be strings. Convert numbers and booleans using `String()`.

### ✅ GOOD Implementation Examples

#### Product Card with Comprehensive Properties

```swift
// GOOD: Complete product card implementation
class ProductCardView: UIView {
    private var addToCartButton: UIButton!
    
    func configure(with product: Product) {
        // Set all attribute values first
        FS.setAttribute(self, attributeName: "data-product-id", attributeValue: product.id)
        FS.setAttribute(self, attributeName: "data-product-name", attributeValue: product.name)
        FS.setAttribute(self, attributeName: "data-category", attributeValue: product.category)
        FS.setAttribute(self, attributeName: "data-price", attributeValue: String(product.price))
        FS.setAttribute(self, attributeName: "data-stock-level", attributeValue: String(product.stockLevel))
        FS.setAttribute(self, attributeName: "data-rating", attributeValue: String(product.rating))
        FS.setAttribute(self, attributeName: "data-on-sale", attributeValue: String(product.isOnSale))
        FS.setAttribute(self, attributeName: "data-launch-date", attributeValue: product.launchDate.iso8601String)
        
        // Build properties schema as JSON string
        let schema: [String: Any] = [
            "data-product-id": ["type": "str", "name": "productId"],
            "data-product-name": ["type": "str", "name": "productName"],
            "data-category": ["type": "str", "name": "category"],
            "data-price": ["type": "real", "name": "price"],
            "data-stock-level": ["type": "int", "name": "stockLevel"],
            "data-rating": ["type": "real", "name": "rating"],
            "data-on-sale": ["type": "bool", "name": "isOnSale"],
            "data-launch-date": ["type": "date", "name": "launchDate"]
        ]
        
        // Convert to JSON string
        if let schemaData = try? JSONSerialization.data(withJSONObject: schema),
           let schemaString = String(data: schemaData, encoding: .utf8) {
            FS.setAttribute(self, attributeName: "data-fs-properties-schema", attributeValue: schemaString)
        }
        
        // Name the element
        FS.setAttribute(self, attributeName: "data-fs-element", attributeValue: "Product Card")
        
        // Configure child button (inherits parent properties)
        FS.setAttribute(addToCartButton, attributeName: "data-fs-element", attributeValue: "Add to Cart Button")
    }
}

// Helper extension for ISO8601 dates
extension Date {
    var iso8601String: String {
        let formatter = ISO8601DateFormatter()
        return formatter.string(from: self)
    }
}
```

#### Table View Cell with Reuse Handling

```swift
// GOOD: Properly handling cell reuse in UITableView
class ProductTableViewCell: UITableViewCell {
    private var currentAttributes: [String] = []
    
    override func prepareForReuse() {
        super.prepareForReuse()
        clearFullstoryAttributes()
    }
    
    func configure(with product: Product, at indexPath: IndexPath) {
        // Clear any existing attributes first
        clearFullstoryAttributes()
        
        // Set new attributes and track them
        setAndTrack("data-product-id", product.id)
        setAndTrack("data-product-name", product.name)
        setAndTrack("data-price", String(product.price))
        setAndTrack("data-in-stock", String(product.isInStock))
        setAndTrack("data-row", String(indexPath.row))
        setAndTrack("data-section", String(indexPath.section))
        
        // Build schema
        let schema: [String: Any] = [
            "data-product-id": ["type": "str", "name": "productId"],
            "data-product-name": ["type": "str", "name": "productName"],
            "data-price": ["type": "real", "name": "price"],
            "data-in-stock": ["type": "bool", "name": "inStock"],
            "data-row": ["type": "int", "name": "rowIndex"],
            "data-section": ["type": "int", "name": "sectionIndex"]
        ]
        
        if let schemaData = try? JSONSerialization.data(withJSONObject: schema),
           let schemaString = String(data: schemaData, encoding: .utf8) {
            setAndTrack("data-fs-properties-schema", schemaString)
        }
        
        setAndTrack("data-fs-element", "Product Cell")
    }
    
    private func setAndTrack(_ attribute: String, _ value: String) {
        FS.setAttribute(self, attributeName: attribute, attributeValue: value)
        currentAttributes.append(attribute)
    }
    
    private func clearFullstoryAttributes() {
        currentAttributes.forEach { attribute in
            FS.setAttribute(self, attributeName: attribute, attributeValue: "")
        }
        currentAttributes.removeAll()
    }
}
```

#### Form with Hierarchical Properties (Objective-C)

```objc
// GOOD: Form implementation with property inheritance
@implementation CheckoutFormViewController

- (void)setupFormTracking {
    UIView *formContainer = self.formContainerView;
    
    // Set form-level properties (inherited by all children)
    [FS setAttribute:formContainer 
        attributeName:@"data-form-type" 
        attributeValue:@"checkout"];
    [FS setAttribute:formContainer 
        attributeName:@"data-form-step" 
        attributeValue:@"payment"];
    [FS setAttribute:formContainer 
        attributeName:@"data-user-tier" 
        attributeValue:self.userTier];
    [FS setAttribute:formContainer 
        attributeName:@"data-cart-total" 
        attributeValue:[NSString stringWithFormat:@"%.2f", self.cartTotal]];
    
    // Build form schema
    NSDictionary *formSchema = @{
        @"data-form-type": @{@"type": @"str", @"name": @"formType"},
        @"data-form-step": @{@"type": @"str", @"name": @"checkoutStep"},
        @"data-user-tier": @{@"type": @"str", @"name": @"userTier"},
        @"data-cart-total": @{@"type": @"real", @"name": @"cartTotal"}
    };
    
    NSError *error;
    NSData *formSchemaData = [NSJSONSerialization dataWithJSONObject:formSchema 
                                                             options:0 
                                                               error:&error];
    if (formSchemaData && !error) {
        NSString *formSchemaString = [[NSString alloc] initWithData:formSchemaData 
                                                           encoding:NSUTF8StringEncoding];
        [FS setAttribute:formContainer 
            attributeName:@"data-fs-properties-schema" 
            attributeValue:formSchemaString];
    }
    
    [FS setAttribute:formContainer 
        attributeName:@"data-fs-element" 
        attributeValue:@"Checkout Form"];
    
    // Submit button inherits form properties
    [FS setAttribute:self.submitButton 
        attributeName:@"data-fs-element" 
        attributeValue:@"Submit Payment Button"];
}

@end
```

### ❌ BAD Implementation Examples

```swift
// BAD: Type mismatches and formatting issues
func configureProductCard(with product: Product) {
    let cardView = self.productCardView
    
    // BAD: Including formatting/symbols in numeric values
    FS.setAttribute(cardView, 
        attributeName: "data-price", 
        attributeValue: "$\(product.price)") // BAD: includes $
    
    FS.setAttribute(cardView, 
        attributeName: "data-stock", 
        attributeValue: "\(product.stockLevel) items") // BAD: includes "items"
    
    FS.setAttribute(cardView, 
        attributeName: "data-available", 
        attributeValue: product.isInStock ? "Yes" : "No") // BAD: not boolean value
}
```

```swift
// BAD: Not handling cell reuse
class ProductCell: UITableViewCell {
    func configure(with product: Product) {
        // BAD: Just setting new attributes without clearing old ones
        FS.setAttribute(self, attributeName: "data-product-id", attributeValue: product.id)
        // When this cell is reused, old attributes remain!
    }
}
```

```swift
// BAD: Setting schema before values
func setupProductCard(product: Product) {
    let cardView = findViewById(R.id.product_card)
    
    // BAD: Setting schema first
    let schema = JSONObject().apply { ... }.toString()
    FS.setAttribute(cardView, "data-fs-properties-schema", schema)
    
    // Then setting values (TOO LATE)
    FS.setAttribute(cardView, "data-product-id", product.id)
}
```

---

## Android (Kotlin/Java)

### API Reference

```kotlin
import com.fullstory.FS

// Basic syntax
FS.setAttribute(view: View, attributeName: String, attributeValue: String)
```

**Note**: All attribute values must be strings. Use `String.valueOf()` or `.toString()` for numbers and booleans.

### ✅ GOOD Implementation Examples

#### Product Card with Comprehensive Properties (Kotlin)

```kotlin
// GOOD: Complete product card implementation
class ProductCardViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
    private val trackedAttributes = mutableListOf<String>()
    
    fun bind(product: Product) {
        val cardView = itemView.findViewById<View>(R.id.product_card)
        
        // Clear previous attributes (important for recycled views)
        clearAttributes()
        
        // Set individual attribute values
        setAndTrack(cardView, "data-product-id", product.id)
        setAndTrack(cardView, "data-product-name", product.name)
        setAndTrack(cardView, "data-category", product.category)
        setAndTrack(cardView, "data-price", product.price.toString())
        setAndTrack(cardView, "data-stock-level", product.stockLevel.toString())
        setAndTrack(cardView, "data-rating", product.rating.toString())
        setAndTrack(cardView, "data-on-sale", product.isOnSale.toString())
        setAndTrack(cardView, "data-launch-date", product.launchDate.toString())
        
        // Build and set schema
        val schema = JSONObject().apply {
            put("data-product-id", JSONObject().put("type", "str").put("name", "productId"))
            put("data-product-name", JSONObject().put("type", "str").put("name", "productName"))
            put("data-category", JSONObject().put("type", "str").put("name", "category"))
            put("data-price", JSONObject().put("type", "real").put("name", "price"))
            put("data-stock-level", JSONObject().put("type", "int").put("name", "stockLevel"))
            put("data-rating", JSONObject().put("type", "real").put("name", "rating"))
            put("data-on-sale", JSONObject().put("type", "bool").put("name", "isOnSale"))
            put("data-launch-date", JSONObject().put("type", "date").put("name", "launchDate"))
        }.toString()
        
        setAndTrack(cardView, "data-fs-properties-schema", schema)
        setAndTrack(cardView, "data-fs-element", "Product Card")
        
        // Configure child button (inherits parent properties)
        val addToCartBtn = itemView.findViewById<Button>(R.id.btn_add_to_cart)
        FS.setAttribute(addToCartBtn, "data-fs-element", "Add to Cart Button")
    }
    
    private fun setAndTrack(view: View, name: String, value: String) {
        FS.setAttribute(view, name, value)
        trackedAttributes.add(name)
    }
    
    private fun clearAttributes() {
        trackedAttributes.forEach { attr ->
            FS.setAttribute(itemView, attr, "")
        }
        trackedAttributes.clear()
    }
}
```

#### RecyclerView Adapter with Proper Cleanup (Java)

```java
// GOOD: Handling dynamic list items with proper cleanup
public class ProductAdapter extends RecyclerView.Adapter<ProductAdapter.ViewHolder> {
    
    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        Product product = products.get(position);
        
        // Clear previous attributes (important for recycled views)
        holder.clearFullstoryAttributes();
        
        // Set new attributes
        holder.setProductProperties(product, position);
    }
    
    static class ViewHolder extends RecyclerView.ViewHolder {
        private List<String> appliedAttributes = new ArrayList<>();
        
        void setProductProperties(Product product, int position) {
            View itemView = this.itemView;
            
            // Track which attributes we're setting
            appliedAttributes.clear();
            
            // Set attributes
            setAttribute(itemView, "data-product-id", product.getId());
            setAttribute(itemView, "data-product-name", product.getName());
            setAttribute(itemView, "data-price", String.valueOf(product.getPrice()));
            setAttribute(itemView, "data-in-stock", String.valueOf(product.isInStock()));
            setAttribute(itemView, "data-position", String.valueOf(position));
            
            // Build and set schema
            try {
                String schema = new JSONObject()
                    .put("data-product-id", new JSONObject().put("type", "str").put("name", "productId"))
                    .put("data-product-name", new JSONObject().put("type", "str").put("name", "productName"))
                    .put("data-price", new JSONObject().put("type", "real").put("name", "price"))
                    .put("data-in-stock", new JSONObject().put("type", "bool").put("name", "inStock"))
                    .put("data-position", new JSONObject().put("type", "int").put("name", "listPosition"))
                    .toString();
                    
                setAttribute(itemView, "data-fs-properties-schema", schema);
                setAttribute(itemView, "data-fs-element", "Product List Item");
            } catch (JSONException e) {
                Log.e("ProductAdapter", "Error building properties schema", e);
            }
        }
        
        private void setAttribute(View view, String name, String value) {
            FS.setAttribute(view, name, value);
            appliedAttributes.add(name);
        }
        
        void clearFullstoryAttributes() {
            for (String attr : appliedAttributes) {
                FS.setAttribute(itemView, attr, "");
            }
            appliedAttributes.clear();
        }
    }
}
```

#### Form with Hierarchy (Kotlin)

```kotlin
// GOOD: Comprehensive form tracking with hierarchy
class CheckoutFormFragment : Fragment() {
    
    private fun setupFormTracking() {
        val formContainer = view?.findViewById<ViewGroup>(R.id.checkout_form)
        
        // Set form-level properties that all fields will inherit
        formContainer?.let { form ->
            FS.setAttribute(form, "data-form-type", "checkout")
            FS.setAttribute(form, "data-form-step", "payment")
            FS.setAttribute(form, "data-user-tier", "premium")
            FS.setAttribute(form, "data-total-amount", viewModel.cartTotal.toString())
            
            val formSchema = JSONObject().apply {
                put("data-form-type", JSONObject().put("type", "str").put("name", "formType"))
                put("data-form-step", JSONObject().put("type", "str").put("name", "checkoutStep"))
                put("data-user-tier", JSONObject().put("type", "str").put("name", "userTier"))
                put("data-total-amount", JSONObject().put("type", "real").put("name", "cartTotal"))
            }.toString()
            
            FS.setAttribute(form, "data-fs-properties-schema", formSchema)
            FS.setAttribute(form, "data-fs-element", "Checkout Form")
        }
        
        // Submit button inherits form properties
        val submitButton = view?.findViewById<Button>(R.id.submit_payment)
        submitButton?.let { button ->
            FS.setAttribute(button, "data-fs-element", "Submit Payment Button")
        }
    }
}
```

### ❌ BAD Implementation Examples

```java
// BAD: Type mismatches and string contamination
public void bindProductCard(Product product) {
    View cardView = findViewById(R.id.product_card);
    
    // Setting formatted values instead of clean data
    FS.setAttribute(cardView, "data-price", "$" + product.getPrice()); // BAD: includes $
    FS.setAttribute(cardView, "data-stock", product.getStockLevel() + " items"); // BAD: includes "items"
    FS.setAttribute(cardView, "data-available", product.isInStock() ? "Yes" : "No"); // BAD
}
```

```kotlin
// BAD: Not handling view recycling properly
class ProductAdapter : RecyclerView.Adapter<ProductAdapter.ViewHolder>() {
    
    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val product = products[position]
        
        // BAD: Setting attributes without clearing old ones from recycled view
        FS.setAttribute(holder.itemView, "data-product-id", product.id)
        // If this view was recycled, old attributes remain!
    }
}
```

```java
// BAD: Not converting primitive types to String
public void setupView(View view, int quantity, double price, boolean available) {
    // These will cause compilation errors
    FS.setAttribute(view, "data-quantity", quantity); // ERROR: expects String
    FS.setAttribute(view, "data-price", price); // ERROR: expects String
}
```

---

## Flutter (Dart)

### API Reference

```dart
import 'package:fullstory_flutter/fs.dart';

// Basic syntax
FS.setAttribute(view: view, name: String, value: String);
```

**Note**: Flutter's element properties API requires a view reference. Use `GlobalKey` to get the view.

### ✅ GOOD Implementation Examples

#### Product Card with Comprehensive Properties

```dart
// GOOD: Complete product card implementation
class ProductCard extends StatefulWidget {
  final Product product;
  
  const ProductCard({required this.product, Key? key}) : super(key: key);
  
  @override
  State<ProductCard> createState() => _ProductCardState();
}

class _ProductCardState extends State<ProductCard> {
  final GlobalKey _cardKey = GlobalKey();
  
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _setElementProperties();
    });
  }
  
  @override
  void didUpdateWidget(ProductCard oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.product.id != widget.product.id) {
      _setElementProperties();
    }
  }
  
  void _setElementProperties() {
    final view = _cardKey.currentContext?.findRenderObject();
    if (view == null) return;
    
    final product = widget.product;
    
    // Set attribute values first
    FS.setAttribute(view: view, name: 'data-product-id', value: product.id);
    FS.setAttribute(view: view, name: 'data-product-name', value: product.name);
    FS.setAttribute(view: view, name: 'data-category', value: product.category);
    FS.setAttribute(view: view, name: 'data-price', value: product.price.toString());
    FS.setAttribute(view: view, name: 'data-stock-level', value: product.stockLevel.toString());
    FS.setAttribute(view: view, name: 'data-on-sale', value: product.isOnSale.toString());
    
    // Build and set schema
    final schema = {
      'data-product-id': {'type': 'str', 'name': 'productId'},
      'data-product-name': {'type': 'str', 'name': 'productName'},
      'data-category': {'type': 'str', 'name': 'category'},
      'data-price': {'type': 'real', 'name': 'price'},
      'data-stock-level': {'type': 'int', 'name': 'stockLevel'},
      'data-on-sale': {'type': 'bool', 'name': 'isOnSale'},
    };
    
    FS.setAttribute(view: view, name: 'data-fs-properties-schema', value: jsonEncode(schema));
    FS.setAttribute(view: view, name: 'data-fs-element', value: 'Product Card');
  }
  
  @override
  Widget build(BuildContext context) {
    return Container(
      key: _cardKey,
      child: Column(
        children: [
          Text(widget.product.name),
          Text('\$${widget.product.price}'),
          ElevatedButton(
            onPressed: () => _addToCart(),
            child: const Text('Add to Cart'),
          ),
        ],
      ),
    );
  }
  
  void _addToCart() {
    CartManager.instance.add(widget.product);
  }
}
```

#### ListView with Reuse Handling

```dart
// GOOD: ListView with proper element property management
class ProductListView extends StatelessWidget {
  final List<Product> products;
  
  const ProductListView({required this.products, Key? key}) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: products.length,
      itemBuilder: (context, index) {
        return ProductListItem(
          product: products[index],
          position: index,
        );
      },
    );
  }
}

class ProductListItem extends StatefulWidget {
  final Product product;
  final int position;
  
  const ProductListItem({
    required this.product,
    required this.position,
    Key? key,
  }) : super(key: key);
  
  @override
  State<ProductListItem> createState() => _ProductListItemState();
}

class _ProductListItemState extends State<ProductListItem> {
  final GlobalKey _itemKey = GlobalKey();
  final List<String> _trackedAttributes = [];
  
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _setElementProperties();
    });
  }
  
  @override
  void didUpdateWidget(ProductListItem oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.product.id != widget.product.id) {
      _clearAttributes();
      _setElementProperties();
    }
  }
  
  void _setAndTrack(dynamic view, String name, String value) {
    FS.setAttribute(view: view, name: name, value: value);
    _trackedAttributes.add(name);
  }
  
  void _clearAttributes() {
    final view = _itemKey.currentContext?.findRenderObject();
    if (view == null) return;
    
    for (final attr in _trackedAttributes) {
      FS.setAttribute(view: view, name: attr, value: '');
    }
    _trackedAttributes.clear();
  }
  
  void _setElementProperties() {
    final view = _itemKey.currentContext?.findRenderObject();
    if (view == null) return;
    
    final product = widget.product;
    
    _setAndTrack(view, 'data-product-id', product.id);
    _setAndTrack(view, 'data-product-name', product.name);
    _setAndTrack(view, 'data-price', product.price.toString());
    _setAndTrack(view, 'data-position', widget.position.toString());
    
    final schema = {
      'data-product-id': {'type': 'str', 'name': 'productId'},
      'data-product-name': {'type': 'str', 'name': 'productName'},
      'data-price': {'type': 'real', 'name': 'price'},
      'data-position': {'type': 'int', 'name': 'listPosition'},
    };
    
    _setAndTrack(view, 'data-fs-properties-schema', jsonEncode(schema));
    _setAndTrack(view, 'data-fs-element', 'Product List Item');
  }
  
  @override
  Widget build(BuildContext context) {
    return ListTile(
      key: _itemKey,
      title: Text(widget.product.name),
      subtitle: Text('\$${widget.product.price}'),
    );
  }
}
```

### ❌ BAD Implementation Examples

```dart
// BAD: Type mismatches
void setProductProperties(dynamic view, Product product) {
  FS.setAttribute(view: view, name: 'data-price', value: '\$${product.price}'); // BAD: includes $
  FS.setAttribute(view: view, name: 'data-stock', value: '${product.stock} items'); // BAD: includes text
}
```

```dart
// BAD: Not handling widget updates
class ProductCard extends StatefulWidget {
  @override
  void initState() {
    super.initState();
    _setElementProperties(); // Only called once - won't update when product changes!
  }
}
```

---

## React Native

### API Reference

```javascript
import FullStory from '@fullstory/react-native';

// Basic syntax
FullStory.setAttribute(ref, attributeName, attributeValue);
```

**Note**: Use `ref` to get access to the native view.

### ✅ GOOD Implementation Examples

#### Product Card with Comprehensive Properties

```jsx
// GOOD: Complete product card implementation
import React, { useRef, useEffect } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import FullStory from '@fullstory/react-native';

function ProductCard({ product }) {
  const cardRef = useRef(null);
  const trackedAttributes = useRef([]);
  
  const setAndTrack = (name, value) => {
    if (cardRef.current) {
      FullStory.setAttribute(cardRef.current, name, String(value));
      trackedAttributes.current.push(name);
    }
  };
  
  const clearAttributes = () => {
    if (cardRef.current) {
      trackedAttributes.current.forEach(attr => {
        FullStory.setAttribute(cardRef.current, attr, '');
      });
      trackedAttributes.current = [];
    }
  };
  
  useEffect(() => {
    // Clear old attributes when product changes
    clearAttributes();
    
    // Set new attributes
    setAndTrack('data-product-id', product.id);
    setAndTrack('data-product-name', product.name);
    setAndTrack('data-category', product.category);
    setAndTrack('data-price', product.price);
    setAndTrack('data-stock-level', product.stockLevel);
    setAndTrack('data-on-sale', product.isOnSale);
    
    // Build and set schema
    const schema = {
      'data-product-id': { type: 'str', name: 'productId' },
      'data-product-name': { type: 'str', name: 'productName' },
      'data-category': { type: 'str', name: 'category' },
      'data-price': { type: 'real', name: 'price' },
      'data-stock-level': { type: 'int', name: 'stockLevel' },
      'data-on-sale': { type: 'bool', name: 'isOnSale' },
    };
    
    setAndTrack('data-fs-properties-schema', JSON.stringify(schema));
    setAndTrack('data-fs-element', 'Product Card');
    
    return () => clearAttributes();
  }, [product.id]);
  
  return (
    <View ref={cardRef} style={styles.card}>
      <Text>{product.name}</Text>
      <Text>${product.price}</Text>
      <TouchableOpacity onPress={() => addToCart(product)}>
        <Text>Add to Cart</Text>
      </TouchableOpacity>
    </View>
  );
}
```

#### FlatList with Proper Cleanup

```jsx
// GOOD: FlatList with element properties
import React, { useRef, useEffect, useCallback } from 'react';
import { FlatList, View, Text } from 'react-native';
import FullStory from '@fullstory/react-native';

function ProductList({ products }) {
  const renderItem = useCallback(({ item, index }) => (
    <ProductListItem product={item} position={index} />
  ), []);
  
  return (
    <FlatList
      data={products}
      renderItem={renderItem}
      keyExtractor={item => item.id}
    />
  );
}

function ProductListItem({ product, position }) {
  const itemRef = useRef(null);
  const trackedAttributes = useRef([]);
  
  const setAndTrack = (name, value) => {
    if (itemRef.current) {
      FullStory.setAttribute(itemRef.current, name, String(value));
      trackedAttributes.current.push(name);
    }
  };
  
  const clearAttributes = () => {
    if (itemRef.current) {
      trackedAttributes.current.forEach(attr => {
        FullStory.setAttribute(itemRef.current, attr, '');
      });
      trackedAttributes.current = [];
    }
  };
  
  useEffect(() => {
    clearAttributes();
    
    setAndTrack('data-product-id', product.id);
    setAndTrack('data-product-name', product.name);
    setAndTrack('data-price', product.price);
    setAndTrack('data-position', position);
    
    const schema = {
      'data-product-id': { type: 'str', name: 'productId' },
      'data-product-name': { type: 'str', name: 'productName' },
      'data-price': { type: 'real', name: 'price' },
      'data-position': { type: 'int', name: 'listPosition' },
    };
    
    setAndTrack('data-fs-properties-schema', JSON.stringify(schema));
    setAndTrack('data-fs-element', 'Product List Item');
    
    return () => clearAttributes();
  }, [product.id, position]);
  
  return (
    <View ref={itemRef} style={styles.item}>
      <Text>{product.name}</Text>
      <Text>${product.price}</Text>
    </View>
  );
}
```

#### Custom Hook for Element Properties

```javascript
// GOOD: Reusable hook for element properties
import { useRef, useEffect, useCallback } from 'react';
import FullStory from '@fullstory/react-native';

function useElementProperties(properties, elementName, deps = []) {
  const ref = useRef(null);
  const trackedAttributes = useRef([]);
  
  const setAndTrack = useCallback((name, value) => {
    if (ref.current) {
      FullStory.setAttribute(ref.current, name, String(value));
      trackedAttributes.current.push(name);
    }
  }, []);
  
  const clearAttributes = useCallback(() => {
    if (ref.current) {
      trackedAttributes.current.forEach(attr => {
        FullStory.setAttribute(ref.current, attr, '');
      });
      trackedAttributes.current = [];
    }
  }, []);
  
  useEffect(() => {
    clearAttributes();
    
    const schema = {};
    
    Object.entries(properties).forEach(([key, config]) => {
      const attrName = `data-${key}`;
      setAndTrack(attrName, config.value);
      schema[attrName] = { type: config.type, name: config.name || key };
    });
    
    setAndTrack('data-fs-properties-schema', JSON.stringify(schema));
    setAndTrack('data-fs-element', elementName);
    
    return () => clearAttributes();
  }, deps);
  
  return ref;
}

// Usage
function ProductCard({ product }) {
  const cardRef = useElementProperties({
    productId: { value: product.id, type: 'str' },
    productName: { value: product.name, type: 'str' },
    price: { value: product.price, type: 'real' },
    inStock: { value: product.inStock, type: 'bool' },
  }, 'Product Card', [product.id]);
  
  return (
    <View ref={cardRef}>
      <Text>{product.name}</Text>
    </View>
  );
}
```

### ❌ BAD Implementation Examples

```javascript
// BAD: Type mismatches
FullStory.setAttribute(ref, 'data-price', `$${product.price}`); // BAD: includes $
FullStory.setAttribute(ref, 'data-available', product.inStock ? 'Yes' : 'No'); // BAD: not boolean

// BAD: Not handling list item recycling
function ProductItem({ product }) {
  const ref = useRef(null);
  
  useEffect(() => {
    // BAD: Not clearing old attributes when product changes
    FullStory.setAttribute(ref.current, 'data-product-id', product.id);
  }, [product.id]);
}

// BAD: Setting attributes without ref check
useEffect(() => {
  // BAD: ref.current might be null!
  FullStory.setAttribute(ref.current, 'data-product-id', product.id);
}, []);
```

---

## Common Patterns (All Platforms)

### Element Property Manager

Create a centralized helper to standardize element property management:

| Platform | Pattern |
|----------|---------|
| iOS | Extension on UIView or helper class |
| Android | Extension function or utility class |
| Flutter | Mixin or helper class |
| React Native | Custom hook |

### Key Implementation Rules

1. **Always convert to strings**: Mobile SDKs expect string values
2. **Handle view recycling**: Clear old attributes before setting new ones
3. **Track applied attributes**: Maintain a list for cleanup
4. **Set values before schema**: Always set attribute values first, then the schema
5. **Use JSON builders**: Avoid manual JSON string construction

### Mobile-Specific Considerations

| Consideration | iOS | Android | Flutter | React Native |
|---------------|-----|---------|---------|--------------|
| Cell/View reuse | `prepareForReuse()` | `onBindViewHolder` | `didUpdateWidget` | `useEffect` cleanup |
| Type conversion | `String()` | `.toString()` | `.toString()` | `String()` |
| JSON building | `JSONSerialization` | `JSONObject` | `jsonEncode` | `JSON.stringify` |
| View reference | Direct UIView | Direct View | `GlobalKey` | `useRef` |

---

## Reference Links

- **iOS API**: https://developer.fullstory.com/mobile/ios/fullcapture/set-element-properties/
- **Android API**: https://developer.fullstory.com/mobile/android/fullcapture/set-element-properties/
- **Flutter API**: https://developer.fullstory.com/mobile/flutter/fullcapture/set-element-properties/
- **React Native API**: https://developer.fullstory.com/mobile/react-native/fullcapture/set-element-properties/
- **Help Center**: https://help.fullstory.com/hc/en-us/articles/24236341468311-Extracted-Element-Properties
