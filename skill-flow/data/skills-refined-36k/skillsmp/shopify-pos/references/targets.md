# POS UI Extension Targets

Complete reference for all available POS UI extension targets.

## Target Naming Convention

```
pos.<location>.<type>.render
pos.<location>.action.menu-item.render  (for menu items)
pos.<location>.action.render            (for modals triggered by menu items)
```

## Home Screen (Smart Grid)

| Target | Type | Description |
|--------|------|-------------|
| `pos.home.tile.render` | Tile | Clickable tile on POS home smart grid |
| `pos.home.modal.render` | Modal | Full-screen modal when tile is tapped |

**Use cases**: App entry points, status displays, quick actions, workflow launchers

**Example configuration**:
```toml
[[extensions.targeting]]
module = "./src/Tile.tsx"
target = "pos.home.tile.render"

[[extensions.targeting]]
module = "./src/Modal.tsx"
target = "pos.home.modal.render"
```

## Product Details

| Target | Type | Description |
|--------|------|-------------|
| `pos.product-details.block.render` | Block | Inline content on product details screen |
| `pos.product-details.action.menu-item.render` | Menu Item | Button in product details menu |
| `pos.product-details.action.render` | Modal | Modal when menu item is tapped |

**Use cases**: Extended product info, inventory tools, supplier data, custom attributes

**Available API**: `product` - access current product/variant data

## Customer Details

| Target | Type | Description |
|--------|------|-------------|
| `pos.customer-details.block.render` | Block | Inline content on customer details screen |
| `pos.customer-details.action.menu-item.render` | Menu Item | Button in customer details menu |
| `pos.customer-details.action.render` | Modal | Modal when menu item is tapped |

**Use cases**: Loyalty programs, customer notes, purchase history, CRM integration

**Available API**: `customer` - access current customer data

## Cart Line Item Details

| Target | Type | Description |
|--------|------|-------------|
| `pos.cart.line-item-details.action.menu-item.render` | Menu Item | Button in cart item menu |
| `pos.cart.line-item-details.action.render` | Modal | Modal when menu item is tapped |

**Use cases**: Item customization, add-ons, special instructions, warranties

**Available API**: `cart` - access and modify cart contents

## Order Details (Completed Orders)

| Target | Type | Description |
|--------|------|-------------|
| `pos.order-details.block.render` | Block | Inline content on order details screen |
| `pos.order-details.action.menu-item.render` | Menu Item | Button in order details menu |
| `pos.order-details.action.render` | Modal | Modal when menu item is tapped |

**Use cases**: Order management, fulfillment tools, customer service, post-sale actions

**Available API**: `order` - access completed order data

## Draft Order Details

| Target | Type | Description |
|--------|------|-------------|
| `pos.draft-order-details.block.render` | Block | Inline content on draft order screen |
| `pos.draft-order-details.action.menu-item.render` | Menu Item | Button in draft order menu |
| `pos.draft-order-details.action.render` | Modal | Modal when menu item is tapped |

**Use cases**: Quote management, approval workflows, B2B orders

**Available API**: `draftOrder` - access draft order data

## Post-Purchase

| Target | Type | Description |
|--------|------|-------------|
| `pos.purchase.post.block.render` | Block | Inline content after sale completion |
| `pos.purchase.post.action.menu-item.render` | Menu Item | Button on post-purchase screen |
| `pos.purchase.post.action.render` | Modal | Modal when menu item is tapped |

**Use cases**: Surveys, loyalty sign-up, upsells, warranty registration, follow-up scheduling

**Available API**: `order` - access just-completed order data

## Post-Return (Beta)

| Target | Type | Description |
|--------|------|-------------|
| `pos.return.post.block.render` | Block | Inline content after return completion |
| `pos.return.post.action.menu-item.render` | Menu Item | Button on post-return screen |
| `pos.return.post.action.render` | Modal | Modal when menu item is tapped |

**Use cases**: Return surveys, exchange offers, feedback collection

**Requirements**: POS UI extensions 2025-07+, POS app 9.31.0+, invite-only preview

## Post-Exchange (Beta)

| Target | Type | Description |
|--------|------|-------------|
| `pos.exchange.post.block.render` | Block | Inline content after exchange completion |
| `pos.exchange.post.action.menu-item.render` | Menu Item | Button on post-exchange screen |
| `pos.exchange.post.action.render` | Modal | Modal when menu item is tapped |

**Use cases**: Exchange tracking, inventory updates, customer service

**Requirements**: POS UI extensions 2025-07+, POS app 9.31.0+, invite-only preview

## Receipt Customization (Beta)

| Target | Type | Description |
|--------|------|-------------|
| `pos.receipt-header.block.render` | Block | Custom content in receipt header |
| `pos.receipt-footer.block.render` | Block | Custom content in receipt footer |

**Use cases**: Custom branding, promotions, store info, QR codes, loyalty info

**Requirements**: POS UI extensions 2025-04+, POS app 9.31.0+, invite-only preview

**Available components**: `POSReceiptBlock`, `QRCode`, `Text`, `Image`

## Target Type Patterns

### Tile + Modal Pattern
Most common pattern for home screen extensions:
```tsx
// 1. Tile appears on smart grid
reactExtension('pos.home.tile.render', () => <MyTile />);

// 2. Modal opens when tile is tapped
reactExtension('pos.home.modal.render', () => <MyModal />);
```

### Menu Item + Modal Pattern
For context-specific actions on detail screens:
```tsx
// 1. Menu item appears in "More actions" menu
reactExtension('pos.customer-details.action.menu-item.render', () => <MyMenuItem />);

// 2. Modal opens when menu item is tapped
reactExtension('pos.customer-details.action.render', () => <MyModal />);
```

### Block Pattern
For inline content that's always visible:
```tsx
// Block renders inline on the screen
reactExtension('pos.product-details.block.render', () => <MyBlock />);
```

## API Availability by Target

| Target Location | cart | customer | product | order | draftOrder | session | storage |
|-----------------|------|----------|---------|-------|------------|---------|---------|
| Home | ✓ | ✓ | - | - | - | ✓ | ✓ |
| Product Details | ✓ | - | ✓ | - | - | ✓ | ✓ |
| Customer Details | ✓ | ✓ | - | - | - | ✓ | ✓ |
| Cart Line Item | ✓ | - | - | - | - | ✓ | ✓ |
| Order Details | - | ✓ | - | ✓ | - | ✓ | ✓ |
| Draft Order | - | ✓ | - | - | ✓ | ✓ | ✓ |
| Post-Purchase | - | ✓ | - | ✓ | - | ✓ | ✓ |
| Post-Return | - | ✓ | - | ✓ | - | ✓ | ✓ |
| Post-Exchange | - | ✓ | - | ✓ | - | ✓ | ✓ |
