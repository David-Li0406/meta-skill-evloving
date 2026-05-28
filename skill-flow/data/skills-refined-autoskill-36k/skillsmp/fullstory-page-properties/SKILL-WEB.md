---
name: fullstory-page-properties-web
version: v3
platform: web
sdk: fullstory-browser
description: JavaScript/TypeScript implementation guide for Fullstory's Page Properties API. Includes API reference, code examples, and common patterns for web applications including SPAs.
parent_skill: fullstory-page-properties
related_skills:
  - fullstory-page-properties
  - fullstory-element-properties
  - fullstory-user-properties
---

# Fullstory Page Properties — Web Implementation

> **Core Concepts**: See [SKILL.md](./SKILL.md) for pageName limits, property scoping, and best practices.
>
> **Other Platforms**: See [SKILL-MOBILE.md](./SKILL-MOBILE.md) for iOS, Android, Flutter, React Native.

---

## API Reference

### Basic Syntax

```javascript
FS('setProperties', {
  type: 'page',
  properties: object     // Required: Key/value pairs
});
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `type` | string | **Yes** | Must be `'page'` for page properties |
| `properties` | object | **Yes** | Key/value pairs of page data |

---

## ✅ GOOD Implementation Examples

### Example 1: Search Results Page

```javascript
// GOOD: Comprehensive search results context
function setSearchPageProperties(searchResults) {
  FS('setProperties', {
    type: 'page',
    properties: {
      // Page naming for Journeys
      pageName: 'Search Results',
      
      // Search context
      searchTerm: searchResults.query,
      searchType: searchResults.type,  // 'keyword', 'category', 'tag'
      
      // Results info
      resultsCount: searchResults.total,
      resultsShown: searchResults.items.length,
      hasResults: searchResults.total > 0,
      
      // Filters applied
      activeFilters: Object.keys(searchResults.filters),
      filterCount: Object.keys(searchResults.filters).length,
      priceRangeMin: searchResults.filters.price?.min,
      priceRangeMax: searchResults.filters.price?.max,
      categoryFilter: searchResults.filters.category,
      
      // Sorting
      sortBy: searchResults.sortBy,
      sortOrder: searchResults.sortOrder,
      
      // Pagination
      currentPage: searchResults.page,
      totalPages: searchResults.totalPages
    }
  });
}

// Call when search results load
const results = await performSearch(query, filters);
setSearchPageProperties(results);
```

**Why this is good:**
- ✅ Named page for Journey mapping
- ✅ Captures full search context
- ✅ Records filter state for analysis
- ✅ Enables "search with 0 results" segment

### Example 2: Product Detail Page

```javascript
// GOOD: Product page with full context
function setProductPageProperties(product) {
  FS('setProperties', {
    type: 'page',
    properties: {
      pageName: 'Product Detail',
      
      // Product identification
      productId: product.id,
      productSku: product.sku,
      productName: product.name,
      
      // Categorization
      category: product.category,
      subcategory: product.subcategory,
      brand: product.brand,
      
      // Pricing
      price: product.price,
      originalPrice: product.originalPrice,
      onSale: product.price < product.originalPrice,
      discountPercent: product.discountPercent,
      currency: product.currency,
      
      // Inventory
      inStock: product.inStock,
      stockLevel: product.stockQuantity,
      
      // Ratings
      averageRating: product.rating.average,
      reviewCount: product.rating.count,
      
      // Variants
      availableColors: product.variants.colors,
      availableSizes: product.variants.sizes
    }
  });
}

// Call when product page loads
setProductPageProperties(productData);
```

**Why this is good:**
- ✅ Full product context for session search
- ✅ Pricing data for conversion analysis
- ✅ Inventory context for experience analysis
- ✅ Can segment by "viewed out-of-stock items"

### Example 3: Checkout Flow with Step Tracking

```javascript
// GOOD: Checkout with step and cart context
class CheckoutPageProperties {
  
  setCartReviewStep(cart) {
    FS('setProperties', {
      type: 'page',
      properties: {
        pageName: 'Checkout',
        checkoutStep: 1,
        checkoutStepName: 'Cart Review',
        
        cartId: cart.id,
        cartValue: cart.subtotal,
        cartItemCount: cart.items.length,
        
        hasCoupon: !!cart.coupon,
        couponCode: cart.coupon,
        discountAmount: cart.discount,
        
        estimatedShipping: cart.shipping.estimate,
        estimatedTax: cart.tax.estimate,
        estimatedTotal: cart.total
      }
    });
  }
  
  setShippingStep(cart, shippingOptions) {
    FS('setProperties', {
      type: 'page',
      properties: {
        pageName: 'Checkout',
        checkoutStep: 2,
        checkoutStepName: 'Shipping',
        
        cartValue: cart.subtotal,
        cartItemCount: cart.items.length,
        
        shippingOptionsCount: shippingOptions.length,
        cheapestShipping: shippingOptions[0]?.price,
        fastestShipping: shippingOptions.find(o => o.fastest)?.name
      }
    });
  }
  
  setPaymentStep(cart, selectedShipping) {
    FS('setProperties', {
      type: 'page',
      properties: {
        pageName: 'Checkout',
        checkoutStep: 3,
        checkoutStepName: 'Payment',
        
        cartValue: cart.subtotal,
        shippingMethod: selectedShipping.name,
        shippingCost: selectedShipping.price,
        
        totalBeforePayment: cart.total,
        paymentMethodsAvailable: getAvailablePaymentMethods()
      }
    });
  }
  
  setConfirmationStep(order) {
    FS('setProperties', {
      type: 'page',
      properties: {
        pageName: 'Order Confirmation',
        checkoutStep: 4,
        checkoutStepName: 'Confirmation',
        
        orderId: order.id,
        orderTotal: order.total,
        paymentMethod: order.paymentMethod,
        shippingMethod: order.shippingMethod,
        estimatedDelivery: order.estimatedDelivery
      }
    });
  }
}
```

**Why this is good:**
- ✅ Same pageName groups checkout steps
- ✅ Step numbers enable drop-off analysis
- ✅ Cart value context throughout
- ✅ Each step has relevant context

### Example 4: SPA Navigation Handler

```javascript
// GOOD: Handle SPA route changes with page properties
class SPAPagePropertyManager {
  constructor() {
    this.routeHandlers = new Map();
    this.setupRouteListener();
  }
  
  setupRouteListener() {
    // For React Router, Vue Router, etc.
    window.addEventListener('popstate', () => this.handleRouteChange());
    
    // Intercept pushState/replaceState
    const originalPushState = history.pushState;
    history.pushState = (...args) => {
      originalPushState.apply(history, args);
      this.handleRouteChange();
    };
  }
  
  registerRoute(pathPattern, handler) {
    this.routeHandlers.set(pathPattern, handler);
  }
  
  handleRouteChange() {
    const path = window.location.pathname;
    
    // Find matching route handler
    for (const [pattern, handler] of this.routeHandlers) {
      const match = path.match(pattern);
      if (match) {
        const properties = handler(match, path);
        if (properties) {
          FS('setProperties', {
            type: 'page',
            properties
          });
        }
        return;
      }
    }
    
    // Default page properties
    FS('setProperties', {
      type: 'page',
      properties: {
        pageName: this.inferPageName(path),
        path: path
      }
    });
  }
  
  inferPageName(path) {
    const segments = path.split('/').filter(Boolean);
    return segments.length > 0 
      ? segments.map(s => s.charAt(0).toUpperCase() + s.slice(1)).join(' ')
      : 'Home';
  }
}

// Setup
const pageManager = new SPAPagePropertyManager();

pageManager.registerRoute(/^\/products\/([^/]+)$/, (match) => ({
  pageName: 'Product Detail',
  productSlug: match[1]
}));

pageManager.registerRoute(/^\/search$/, () => ({
  pageName: 'Search Results'
  // Additional properties set by search handler
}));

pageManager.registerRoute(/^\/checkout\/(.+)$/, (match) => ({
  pageName: 'Checkout',
  checkoutStepSlug: match[1]
}));
```

**Why this is good:**
- ✅ Handles SPA navigation properly
- ✅ Consistent page naming
- ✅ Route-specific properties
- ✅ Fallback for unregistered routes

### Example 5: Dashboard with Dynamic Context

```javascript
// GOOD: Dashboard with view state properties
function setDashboardPageProperties(dashboardState) {
  FS('setProperties', {
    type: 'page',
    properties: {
      pageName: 'Dashboard',
      
      // View configuration
      dashboardView: dashboardState.activeView,
      dateRange: dashboardState.dateRange.label,
      dateRangeStart: dashboardState.dateRange.start,
      dateRangeEnd: dashboardState.dateRange.end,
      
      // Active filters
      segmentFilter: dashboardState.segment,
      channelFilter: dashboardState.channel,
      regionFilter: dashboardState.region,
      
      // Widget state
      visibleWidgets: dashboardState.widgets.map(w => w.id),
      widgetCount: dashboardState.widgets.length,
      
      // Data state
      dataLoaded: dashboardState.isLoaded,
      hasData: dashboardState.hasData,
      recordCount: dashboardState.recordCount
    }
  });
}

// Update properties when dashboard state changes
dashboardStore.subscribe((state) => {
  setDashboardPageProperties(state);
});
```

**Why this is good:**
- ✅ Captures dashboard configuration
- ✅ Tracks filter/segment context
- ✅ Updates on state changes
- ✅ Enables analysis of how users configure dashboards

### Example 6: Content/Article Page

```javascript
// GOOD: Article page with content metadata
function setArticlePageProperties(article) {
  FS('setProperties', {
    type: 'page',
    properties: {
      pageName: 'Article',
      
      // Content identification
      articleId: article.id,
      articleSlug: article.slug,
      articleTitle: article.title,
      
      // Categorization
      category: article.category,
      tags: article.tags,
      contentType: article.type,  // 'blog', 'tutorial', 'news'
      
      // Author info
      authorId: article.author.id,
      authorName: article.author.name,
      
      // Dates
      publishDate: article.publishedAt,
      lastUpdated: article.updatedAt,
      
      // Content metrics
      wordCount: article.wordCount,
      estimatedReadTime: article.readTime,
      hasVideo: article.hasVideo,
      imageCount: article.images.length,
      
      // Engagement indicators
      commentCount: article.comments.count,
      likeCount: article.likes,
      shareCount: article.shares
    }
  });
}

// Call when article loads
setArticlePageProperties(articleData);
```

**Why this is good:**
- ✅ Rich content metadata
- ✅ Enables content performance analysis
- ✅ Author attribution for patterns
- ✅ Engagement context

---

## ❌ BAD Implementation Examples

### Example 1: Missing pageName

```javascript
// BAD: No pageName - can't use in Journeys
FS('setProperties', {
  type: 'page',
  properties: {
    category: 'Electronics',
    sortBy: 'price'
  }
});
```

**Why this is bad:**
- ❌ Page won't appear in Journeys
- ❌ Hard to identify page type in search
- ❌ Missing semantic naming

**CORRECTED:**
```javascript
// GOOD: Include pageName
FS('setProperties', {
  type: 'page',
  properties: {
    pageName: 'Category Page',
    category: 'Electronics',
    sortBy: 'price'
  }
});
```

### Example 2: Wrong Type Parameter

```javascript
// BAD: Using 'user' type for page data
FS('setProperties', {
  type: 'user',  // Wrong type!
  properties: {
    currentPage: 'Search Results',
    searchTerm: 'laptops'
  }
});
```

**Why this is bad:**
- ❌ Page context becomes user property
- ❌ Pollutes user profile with transient data
- ❌ Won't reset on navigation

**CORRECTED:**
```javascript
// GOOD: Use 'page' type
FS('setProperties', {
  type: 'page',
  properties: {
    pageName: 'Search Results',
    searchTerm: 'laptops'
  }
});
```

### Example 3: Dynamic pageName (Exceeds Limit)

```javascript
// BAD: Dynamic pageName creating too many unique values
function setProductPage(product) {
  FS('setProperties', {
    type: 'page',
    properties: {
      // BAD: Product name as pageName creates 1000s of unique values
      pageName: product.name,
      productId: product.id
    }
  });
}
```

**Why this is bad:**
- ❌ pageName limited to 1,000 unique values
- ❌ Will be ignored once limit reached
- ❌ Pollutes Journey definitions

**CORRECTED:**
```javascript
// GOOD: Generic pageName, specific properties
function setProductPage(product) {
  FS('setProperties', {
    type: 'page',
    properties: {
      pageName: 'Product Detail',  // Generic
      productName: product.name,   // Specific as property
      productId: product.id,
      category: product.category
    }
  });
}
```

### Example 4: Changing pageName on Same Page

```javascript
// BAD: Multiple different pageNames on same page
function updateFilters(filters) {
  FS('setProperties', {
    type: 'page',
    properties: {
      pageName: `Search - ${filters.category}`,  // BAD: Changes pageName
      filters: Object.keys(filters)
    }
  });
}
```

**Why this is bad:**
- ❌ Later pageName calls are IGNORED
- ❌ Only first pageName sticks
- ❌ Creates confusion and missing data

**CORRECTED:**
```javascript
// GOOD: Set pageName once, update other properties
function setSearchPage(initialData) {
  FS('setProperties', {
    type: 'page',
    properties: {
      pageName: 'Search Results',  // Set once
      searchTerm: initialData.query
    }
  });
}

function updateFilters(filters) {
  // Update properties without pageName
  FS('setProperties', {
    type: 'page',
    properties: {
      activeCategory: filters.category,
      filterCount: Object.keys(filters).length,
      filters: Object.keys(filters)
    }
  });
}
```

### Example 5: User Data in Page Properties

```javascript
// BAD: Putting user-specific data in page properties
FS('setProperties', {
  type: 'page',
  properties: {
    pageName: 'Dashboard',
    userId: user.id,           // BAD: User data
    userEmail: user.email,     // BAD: User data
    userPlan: user.plan        // BAD: User data
  }
});
```

**Why this is bad:**
- ❌ User data should be user properties
- ❌ Will reset on navigation
- ❌ Wrong scope for the data

**CORRECTED:**
```javascript
// GOOD: Separate user and page data
FS('setIdentity', {
  uid: user.id,
  properties: {
    email: user.email,
    plan: user.plan
  }
});

FS('setProperties', {
  type: 'page',
  properties: {
    pageName: 'Dashboard',
    dashboardView: 'analytics',
    dateRange: 'last30days'
  }
});
```

### Example 6: Not Handling SPA Navigation

```javascript
// BAD: Only setting properties on initial load
document.addEventListener('DOMContentLoaded', () => {
  FS('setProperties', {
    type: 'page',
    properties: {
      pageName: 'Home'
    }
  });
  // Properties never updated for SPA navigation!
});
```

**Why this is bad:**
- ❌ SPA navigations don't trigger DOMContentLoaded
- ❌ Page properties become stale
- ❌ Wrong context after navigation

**CORRECTED:**
```javascript
// GOOD: Handle SPA navigation
function setPageProperties(route) {
  FS('setProperties', {
    type: 'page',
    properties: {
      pageName: route.name,
      ...route.properties
    }
  });
}

// Call on initial load
setPageProperties(getCurrentRoute());

// Call on navigation
router.on('routeChange', (route) => {
  setPageProperties(route);
});
```

---

## Common Implementation Patterns

### Pattern 1: Page Property Manager

```javascript
// Centralized page property management
class PagePropertyManager {
  constructor() {
    this.currentPageName = null;
    this.baseProperties = {};
  }
  
  // Initialize page with base properties
  initialize(pageName, baseProps = {}) {
    this.currentPageName = pageName;
    this.baseProperties = baseProps;
    
    FS('setProperties', {
      type: 'page',
      properties: {
        pageName,
        ...baseProps,
        pageLoadTime: new Date().toISOString()
      }
    });
  }
  
  // Add additional properties (merges with existing)
  addProperties(additionalProps) {
    FS('setProperties', {
      type: 'page',
      properties: additionalProps
    });
  }
  
  // Update specific property
  updateProperty(key, value) {
    FS('setProperties', {
      type: 'page',
      properties: {
        [key]: value
      }
    });
  }
}

// Usage
const pageProps = new PagePropertyManager();

// On page load
pageProps.initialize('Product Listing', {
  category: 'Electronics',
  totalProducts: 150
});

// When user applies filter
pageProps.addProperties({
  activeFilters: ['brand:Apple', 'price:500-1000'],
  filteredCount: 23
});
```

### Pattern 2: React Router Integration

```jsx
// React component for automatic page properties
import { useEffect } from 'react';
import { useLocation, useParams } from 'react-router-dom';

function PagePropertySetter({ pageName, children, getProperties }) {
  const location = useLocation();
  const params = useParams();
  
  useEffect(() => {
    const properties = getProperties ? getProperties(params, location) : {};
    
    FS('setProperties', {
      type: 'page',
      properties: {
        pageName,
        ...properties,
        path: location.pathname,
        queryParams: Object.fromEntries(new URLSearchParams(location.search))
      }
    });
  }, [pageName, location, params, getProperties]);
  
  return children;
}

// Usage
function App() {
  return (
    <Routes>
      <Route 
        path="/products/:category" 
        element={
          <PagePropertySetter 
            pageName="Product Listing"
            getProperties={(params) => ({
              category: params.category
            })}
          >
            <ProductListingPage />
          </PagePropertySetter>
        } 
      />
      <Route 
        path="/product/:id" 
        element={
          <PagePropertySetter 
            pageName="Product Detail"
            getProperties={(params) => ({
              productId: params.id
            })}
          >
            <ProductDetailPage />
          </PagePropertySetter>
        } 
      />
    </Routes>
  );
}
```

### Pattern 3: React Hook

```jsx
import { useEffect, useCallback } from 'react';
import { useLocation } from 'react-router-dom';

export function usePageProperties(pageName, initialProperties = {}) {
  const location = useLocation();
  
  // Set initial properties on mount/navigation
  useEffect(() => {
    FS('setProperties', {
      type: 'page',
      properties: {
        pageName,
        ...initialProperties,
        path: location.pathname
      }
    });
  }, [pageName, location.pathname]);
  
  // Return function to update properties
  const updateProperties = useCallback((properties) => {
    FS('setProperties', {
      type: 'page',
      properties
    });
  }, []);
  
  return { updateProperties };
}

// Usage
function SearchResultsPage() {
  const { updateProperties } = usePageProperties('Search Results', {
    searchType: 'keyword'
  });
  
  const handleSearch = async (query) => {
    const results = await search(query);
    updateProperties({
      searchTerm: query,
      resultsCount: results.total,
      hasResults: results.total > 0
    });
  };
  
  return <SearchUI onSearch={handleSearch} />;
}
```

### Pattern 4: Vue Router Integration

```javascript
// Vue plugin for page properties
export const PagePropertiesPlugin = {
  install(app, { router }) {
    router.afterEach((to) => {
      const pageName = to.meta.pageName || to.name;
      const properties = to.meta.pageProperties 
        ? to.meta.pageProperties(to.params) 
        : {};
      
      FS('setProperties', {
        type: 'page',
        properties: {
          pageName,
          ...properties,
          path: to.path
        }
      });
    });
    
    // Add method to update properties
    app.config.globalProperties.$setPageProperties = (properties) => {
      FS('setProperties', {
        type: 'page',
        properties
      });
    };
  }
};

// Router setup
const routes = [
  {
    path: '/products/:category',
    component: ProductListing,
    meta: {
      pageName: 'Product Listing',
      pageProperties: (params) => ({
        category: params.category
      })
    }
  }
];
```

### Pattern 5: Angular Router Integration

```typescript
// Angular service for page properties
@Injectable({ providedIn: 'root' })
export class PagePropertiesService {
  constructor(private router: Router, private route: ActivatedRoute) {
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe(() => {
      this.setPropertiesFromRoute();
    });
  }
  
  private setPropertiesFromRoute(): void {
    const data = this.route.snapshot.firstChild?.data;
    if (data?.pageName) {
      this.setProperties({
        pageName: data.pageName,
        ...(data.pageProperties || {})
      });
    }
  }
  
  setProperties(properties: Record<string, any>): void {
    FS('setProperties', {
      type: 'page',
      properties
    });
  }
}

// Route config
const routes: Routes = [
  {
    path: 'products/:category',
    component: ProductListingComponent,
    data: {
      pageName: 'Product Listing'
    }
  }
];
```

### Pattern 6: Search Page Handler

```javascript
// Complete search page property management
class SearchPageProperties {
  constructor() {
    this.initialized = false;
  }
  
  initialize() {
    FS('setProperties', {
      type: 'page',
      properties: {
        pageName: 'Search Results'
      }
    });
    this.initialized = true;
  }
  
  setSearchContext(query, results) {
    if (!this.initialized) this.initialize();
    
    FS('setProperties', {
      type: 'page',
      properties: {
        searchTerm: query.term,
        searchCategory: query.category,
        resultsCount: results.total,
        hasResults: results.total > 0,
        responseTime: results.timing
      }
    });
  }
  
  setFilters(filters) {
    FS('setProperties', {
      type: 'page',
      properties: {
        activeFilters: filters.active,
        filterCount: filters.active.length,
        priceMin: filters.price?.min,
        priceMax: filters.price?.max,
        brandFilters: filters.brands,
        ratingFilter: filters.minRating
      }
    });
  }
  
  setSorting(sort) {
    FS('setProperties', {
      type: 'page',
      properties: {
        sortField: sort.field,
        sortDirection: sort.direction
      }
    });
  }
  
  setPagination(page, total) {
    FS('setProperties', {
      type: 'page',
      properties: {
        currentPage: page,
        totalPages: total
      }
    });
  }
}
```

---

## Integration with Other APIs

### Page Properties + User Properties

```javascript
// User properties: who they are
FS('setIdentity', {
  uid: user.id,
  properties: {
    plan: 'enterprise',
    role: 'admin'
  }
});

// Page properties: where they are and what they're doing
FS('setProperties', {
  type: 'page',
  properties: {
    pageName: 'Reports Dashboard',
    reportType: 'revenue',
    dateRange: 'last_quarter'
  }
});
```

### Page Properties + Events

```javascript
// Set page context
FS('setProperties', {
  type: 'page',
  properties: {
    pageName: 'Product Detail',
    productId: 'SKU-123',
    price: 99.99
  }
});

// Events inherit page context for search
FS('trackEvent', {
  name: 'Add to Cart',
  properties: {
    quantity: 2
  }
});
// This event is searchable via: "Add to Cart on Product Detail page"
```

### Page Properties + Element Properties

```javascript
// Page-level context
FS('setProperties', {
  type: 'page',
  properties: {
    pageName: 'Search Results',
    searchTerm: 'laptop',
    resultsCount: 50
  }
});

// Element-level context (on each product card via data attributes)
// data-fs-element-properties for product-specific data
// Elements inherit page properties automatically
```

---

## Reference Links

- **Set Page Properties**: https://developer.fullstory.com/browser/set-page-properties/
- **Custom Properties**: https://developer.fullstory.com/browser/custom-properties/
- **Help Center - Page Properties**: https://help.fullstory.com/hc/en-us/articles/360020623454
