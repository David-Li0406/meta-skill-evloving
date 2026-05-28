# POS UI Extension APIs

Complete reference for all available POS UI extension APIs.

## Accessing APIs

```tsx
import { useApi } from '@shopify/ui-extensions-react/point-of-sale';

function MyComponent() {
  // Type parameter specifies which target's APIs are available
  const api = useApi<'pos.home.modal.render'>();

  // Destructure the APIs you need
  const { cart, customer, session, navigation, toast, storage, scanner, print } = api;
}
```

## Contextual APIs

### Cart API

Add, remove, and modify cart items, apply discounts, and manage cart properties.

```tsx
const { cart } = useApi<'pos.home.modal.render'>();

// Get current cart
const currentCart = cart.getCart();
// Returns: { lineItems: [], customer: { id, email }, subtotal, total, discounts: [] }

// Subscribe to cart changes
cart.subscribeToCart((updatedCart) => {
  console.log('Cart updated:', updatedCart);
});

// Add line item
await cart.addLineItem({
  variantId: 'gid://shopify/ProductVariant/123',
  quantity: 1
});

// Update line item quantity
await cart.updateLineItem({
  lineItemId: 'line-item-id',
  quantity: 2
});

// Remove line item
await cart.removeLineItem('line-item-id');

// Apply cart discount (percentage)
await cart.applyCartDiscount({
  type: 'percentage',
  value: 10,
  title: '10% Off'
});

// Apply cart discount (fixed amount)
await cart.applyCartDiscount({
  type: 'fixedAmount',
  value: 5.00,
  title: '$5 Off'
});

// Apply line item discount
await cart.applyLineItemDiscount({
  lineItemId: 'line-item-id',
  type: 'percentage',
  value: 15,
  title: 'Item Discount'
});

// Remove discount
await cart.removeDiscount('discount-id');

// Set cart customer
await cart.setCustomer('gid://shopify/Customer/123');

// Remove cart customer
await cart.removeCustomer();

// Set cart properties (custom attributes)
await cart.setCartProperties([
  { key: 'gift_message', value: 'Happy Birthday!' }
]);

// Clear cart
await cart.clearCart();
```

### Customer API

Access customer data in customer-specific contexts.

```tsx
const { customer } = useApi<'pos.customer-details.block.render'>();

// Get current customer
const customerData = customer.getCustomer();
// Returns: { id, email, firstName, lastName, phone, tags, ... }

// Subscribe to customer changes
customer.subscribeToCustomer((updatedCustomer) => {
  console.log('Customer updated:', updatedCustomer);
});
```

### Product API

Access product data in product-specific contexts.

```tsx
const { product } = useApi<'pos.product-details.block.render'>();

// Get current product
const productData = product.getProduct();
// Returns: { id, title, variants: [], images: [], vendor, productType, ... }

// Get current variant (if on variant screen)
const variantData = product.getVariant();
```

### Order API

Access completed order data.

```tsx
const { order } = useApi<'pos.order-details.block.render'>();

// Get current order
const orderData = order.getOrder();
// Returns: { id, name, lineItems: [], customer, total, fulfillmentStatus, ... }
```

### Draft Order API

Access draft order data.

```tsx
const { draftOrder } = useApi<'pos.draft-order-details.block.render'>();

// Get current draft order
const draftOrderData = draftOrder.getDraftOrder();
```

## Platform APIs

### Session API

Manage session data and authentication.

```tsx
const { session } = useApi<'pos.home.modal.render'>();

// Get session token for backend authentication
const token = await session.getSessionToken();
// Use in Authorization header: `Bearer ${token}`

// Get current session info
const currentSession = session.currentSession;
// Returns: { shop, staff: { id, name }, location: { id, name } }

// Get shop domain
const shop = session.shop;

// Get current staff member
const staff = session.currentStaff;

// Get current location
const location = session.currentLocation;
```

### Navigation API

Navigate between screens.

```tsx
const { navigation } = useApi<'pos.home.modal.render'>();

// Dismiss modal/close extension
navigation.dismiss();

// Navigate to a named screen (within Navigator)
navigation.navigate('ScreenName');

// Navigate back
navigation.goBack();

// Navigate with parameters
navigation.navigate('Details', { productId: '123' });
```

### Toast API

Show temporary notifications.

```tsx
const { toast } = useApi<'pos.home.modal.render'>();

// Show success toast
toast.show('Item added successfully');

// Show with duration
toast.show('Processing...', { duration: 3000 });
```

### Storage API

Persist data locally on the device.

```tsx
const { storage } = useApi<'pos.home.modal.render'>();

// Store data
await storage.setItem('key', 'value');

// Store object (serialize to JSON)
await storage.setItem('settings', JSON.stringify({ theme: 'dark' }));

// Retrieve data
const value = await storage.getItem('key');

// Retrieve and parse object
const settings = JSON.parse(await storage.getItem('settings') || '{}');

// Remove data
await storage.removeItem('key');

// Clear all data
await storage.clear();
```

### Scanner API

Access barcode/QR code scanning.

```tsx
const { scanner } = useApi<'pos.home.modal.render'>();

// Scan barcode
const result = await scanner.scanBarcode();
if (result) {
  console.log('Scanned:', result.data);
  console.log('Format:', result.format); // 'QR_CODE', 'EAN_13', etc.
}
```

### Print API

Print documents and receipts.

```tsx
const { print } = useApi<'pos.home.modal.render'>();

// Print document
await print.printDocument({
  content: 'Receipt content here...',
  title: 'Receipt'
});

// Check if printer is available
const isPrinterAvailable = await print.isPrinterAvailable();
```

### Connectivity API

Monitor device connectivity.

```tsx
const { connectivity } = useApi<'pos.home.modal.render'>();

// Check if online
const isOnline = connectivity.isOnline;

// Subscribe to connectivity changes
connectivity.subscribe((status) => {
  console.log('Online:', status.isOnline);
});
```

### Device API

Get device information.

```tsx
const { device } = useApi<'pos.home.modal.render'>();

// Get device info
const deviceInfo = device.getDeviceInfo();
// Returns: { id, model, platform: 'ios' | 'android' }
```

### Action API

Launch modals and dialogs.

```tsx
const { action } = useApi<'pos.home.modal.render'>();

// Show confirmation dialog
const result = await action.showDialog({
  title: 'Confirm',
  message: 'Proceed with action?',
  primaryAction: { label: 'Yes' },
  secondaryAction: { label: 'No' }
});

if (result.primaryActionPressed) {
  // User confirmed
}
```

### Locale API

Access merchant localization settings.

```tsx
const { locale } = useApi<'pos.home.modal.render'>();

// Get current locale
const currentLocale = locale.locale; // 'en-US', 'fr-FR', etc.

// Get currency
const currency = locale.currency; // 'USD', 'EUR', etc.

// Get timezone
const timezone = locale.timezone;
```

### Product Search API

Search product catalog.

```tsx
const { productSearch } = useApi<'pos.home.modal.render'>();

// Search products
const results = await productSearch.search('sweater');
// Returns: { products: [{ id, title, variants, ... }] }

// Search with filters
const filtered = await productSearch.search('', {
  productType: 'Apparel',
  vendor: 'Nike'
});
```

## Direct GraphQL API Access

Available for extensions targeting `2025-07` or later (requires POS 10.6.0+).

```tsx
// Make direct GraphQL requests to Shopify Admin API
const response = await fetch('shopify:admin/api/graphql.json', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: `
      query GetCustomerOrders($customerId: ID!) {
        customer(id: $customerId) {
          orders(first: 10) {
            nodes {
              id
              name
              totalPrice
              createdAt
            }
          }
        }
      }
    `,
    variables: {
      customerId: 'gid://shopify/Customer/123'
    }
  })
});

const data = await response.json();
```

**Required configuration** in `shopify.app.toml`:
```toml
[access_scopes]
scopes = "read_products,write_products,read_customers,read_orders"
```

## Backend API Calls

For calls to your own backend, use session tokens for authentication.

```tsx
const { session } = useApi<'pos.home.modal.render'>();

async function callBackend(endpoint: string, data: any) {
  const token = await session.getSessionToken();

  const response = await fetch(`https://your-backend.com/api/${endpoint}`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });

  return response.json();
}
```

## API Availability by Target

| API | Home | Product | Customer | Cart | Order | Draft Order | Post-Purchase |
|-----|------|---------|----------|------|-------|-------------|---------------|
| cart | ✓ | ✓ | ✓ | ✓ | - | - | - |
| customer | ✓ | - | ✓ | - | ✓ | ✓ | ✓ |
| product | - | ✓ | - | - | - | - | - |
| order | - | - | - | - | ✓ | - | ✓ |
| draftOrder | - | - | - | - | - | ✓ | - |
| session | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| navigation | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| toast | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| storage | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| scanner | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| print | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| connectivity | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| locale | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| productSearch | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
