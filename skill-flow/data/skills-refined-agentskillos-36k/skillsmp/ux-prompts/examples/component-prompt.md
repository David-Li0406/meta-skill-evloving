# Example: Component Prompt

A complete, self-contained prompt for a reusable UI component.

---

## Product Card Component

### Context
A product card displaying a single item in a product grid or list. Used on the homepage, category pages, and search results. Users click to view product details or add directly to cart.

Part of: E-commerce storefront
Appears in: ProductGrid, ProductList, FeaturedProducts

### Requirements

**Dimensions:**
- Width: Flexible, fills container (grid cell or list row)
- Minimum width: 200px
- Aspect ratio: 4:3 for image area
- Total card height: Auto based on content

**Layout:**
```
┌─────────────────────────────┐
│                             │
│         [Image]             │ ← Aspect ratio 4:3
│                             │
├─────────────────────────────┤
│ [Category tag]              │
│ Product Name                │
│ $XX.XX                      │
│                             │
│ [Add to Cart]     [♡]       │
└─────────────────────────────┘
```

**Visual Specs:**
- Card background: var(--surface-primary)
- Border: 1px solid var(--border-default)
- Border-radius: 12px
- Card shadow: 0 1px 3px rgba(0,0,0,0.1)
- Content padding: 16px

**Typography:**
- Category tag: 12px, uppercase, var(--text-tertiary), tracking 0.5px
- Product name: 16px, weight 500, var(--text-primary), max 2 lines with ellipsis
- Price: 18px, weight 600, var(--text-primary)
- Sale price: Original struck through + new price in var(--color-error)

**Image:**
- Object-fit: cover
- Placeholder: Skeleton with pulse until loaded
- Error: Gray background + product icon

### States

| State | Appearance | Behavior |
|-------|------------|----------|
| Default | As described above | Interactive |
| Hover | Card lifts 4px, shadow increases to 0 8px 24px rgba(0,0,0,0.12) | Cursor: pointer |
| Active | Card pressed down 2px | On click down |
| Loading | Skeleton for image + text blocks with pulse | Not interactive |
| Out of Stock | Gray overlay on image, "Sold Out" badge, Add to Cart disabled | Can still view details |
| Wishlisted | Heart icon filled | Toggle on click |

**State Details:**

Loading skeleton:
```
┌─────────────────────────────┐
│ [████████████████████████] │ ← Gray pulse
│ [████████████████████████] │
│ [████████████████████████] │
├─────────────────────────────┤
│ [████]                      │
│ [████████████]              │
│ [████]                      │
│                             │
│ [███████████]     [██]      │
└─────────────────────────────┘
```

### Interactions

**Click behaviors:**
- Card click (excluding buttons): Navigate to /products/[id]
- Add to Cart button: Add item to cart, show success state
- Heart icon: Toggle wishlist, animate heart

**Hover behaviors:**
- Card: Lift + shadow
- Add to Cart button: Darken background
- Heart icon: Scale 1.1

**Keyboard:**
- Tab: Focus card, then Add to Cart, then heart
- Enter on card: Navigate to product
- Enter on Add to Cart: Add to cart
- Enter on heart: Toggle wishlist

**Touch:**
- Touch target: Entire card for navigation
- Button touch targets: 44x44px minimum
- Long press: Quick preview modal (optional, can defer)

### Animation

**Hover transition:**
- Duration: 200ms
- Easing: ease-out
- Properties: transform, box-shadow

**Add to Cart success:**
- Button text → checkmark icon (150ms)
- Hold checkmark (400ms)
- Checkmark → original text (150ms)

**Wishlist toggle:**
- Heart scale: 1 → 1.3 → 1 (300ms, spring easing)
- Fill animation: 200ms

**Reduced motion:**
- All animations instant (0ms duration)
- Still show state changes

### Constraints

**This prompt includes:**
- Card visual structure
- All visual states
- Interactive behaviors
- Animations
- Loading skeleton

**This prompt does NOT include:**
- Cart logic/state management
- Wishlist API integration
- Product data fetching
- Parent grid/list layout
- Quick preview modal
- Price formatting logic

### Props Interface

```typescript
interface ProductCardProps {
  product: {
    id: string;
    name: string;
    price: number;
    salePrice?: number;
    category: string;
    imageUrl: string;
    inStock: boolean;
  };
  isWishlisted?: boolean;
  isLoading?: boolean;
  onAddToCart?: (id: string) => void;
  onToggleWishlist?: (id: string) => void;
  onNavigate?: (id: string) => void;
}
```

### Accessibility

- Card is a link (`<a>` or `role="link"`)
- Buttons have `aria-label` when icon-only
- Image has `alt` with product name
- Out of stock announced via `aria-label`
- Focus ring visible: 2px solid var(--color-primary), 2px offset

### Verification

- [ ] Types compile without errors
- [ ] Renders correctly with minimal props
- [ ] All 5 states visually verified:
  - [ ] Default
  - [ ] Hover
  - [ ] Loading
  - [ ] Out of Stock
  - [ ] Wishlisted
- [ ] Keyboard navigation works
- [ ] Screen reader announces correctly
- [ ] Light mode verified
- [ ] Dark mode verified
- [ ] Animation respects prefers-reduced-motion
- [ ] Touch targets are 44px minimum
