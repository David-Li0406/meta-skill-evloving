---
title: Data Loading Patterns
author: @engineering
status: approved
date: 2026-01-13
instruction: "Master two essential data loading patterns: importing static JSON for fast prototypes, and fetching remote APIs for validation. Learn when to use each."
tags: ["data-loading", "patterns", "API-integration"]
related-jtbd: "Build components"
---

# Data Loading Patterns: Local vs Remote

Master the two most important data loading patterns in reactive-md: importing static JSON files and fetching from APIs. Both patterns matter—static data for fast prototypes, remote data for validating integrations.

## What This Shows You

This example demonstrates a product catalog selector with two different data sources:
1. **Local JSON** - Import static product data bundled with your spec
2. **Remote API** - Fetch user data live from an external API

Each pattern has trade-offs. Learn when to use each one and how they work in practice.

## The Trade-Off

| Pattern | When to Use | Pros | Cons |
|---------|------------|------|------|
| **JSON Import** | Static data, repeatable demos | Fast, offline, no CORS | Can't validate live API behavior |
| **Remote Fetch** | Live APIs, integration testing | Realistic, shows latency/errors | Requires internet, CORS issues |

## Files in This Example

- `README.md` - This guide
- `products.json` - Sample product data
- CSS and JSX examples showing both patterns

## How to Use This as a Template

Start with JSON imports for fast iteration (data lives in version control). When your API is ready, switch to fetch() to validate the real integration. Both patterns in this example use the same React state/component structure, so the transition is clean.

## Local JSON: Realistic Data, Version-Controlled

Import static data from `.json` files for prototypes with real structure. The data lives in your git repo, so changes are tracked and reviewable.

```css live
.product-list {
  max-width: 600px;
  margin: 0 auto;
  padding: 1rem;
}

.product-list h3 {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.product-grid {
  display: grid;
  gap: 0.75rem;
}

.product-card {
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: box-shadow 0.2s;
}

.product-card:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.product-name {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.product-price {
  font-size: 0.875rem;
  color: #6b7280;
}

.selection-box {
  margin-top: 1rem;
  padding: 1rem;
  background: #eff6ff;
  border-radius: 0.5rem;
}

.selection-box .label {
  font-weight: bold;
  margin-bottom: 0.25rem;
}

.selection-box .category {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.25rem;
}
```

```jsx live
import products from './products.json' with { type: 'json' };

export default function LocalDataDemo() {
  const [selected, setSelected] = React.useState(null);
  
  return (
    <div className="product-list">
      <h3>Products (Local JSON)</h3>
      <div className="product-grid">
        {products.map(product => (
          <div 
            key={product.id}
            className="product-card"
            onClick={() => setSelected(product)}
          >
            <div className="product-name">{product.name}</div>
            <div className="product-price">${product.price}</div>
          </div>
        ))}
      </div>
      
      {selected && (
        <div className="selection-box">
          <div className="label">Selected:</div>
          <div>{selected.name} - ${selected.price}</div>
          <div className="category">{selected.category}</div>
        </div>
      )}
    </div>
  );
}
```

**Why JSON imports work well here:**
- Separation of data from presentation code
- No external dependencies—data stays in your repo
- Easy to update without redeploying
- Perfect for design reviews with realistic numbers

---

## Remote API: Validate Real Integrations

Load live data from external APIs for dynamic prototypes. This lets you test error states, loading spinners, and actual API latency before shipping.

```css live
.user-list {
  max-width: 600px;
  margin: 0 auto;
  padding: 1rem;
}

.user-list h3 {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.loading-skeleton {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.skeleton-item {
  height: 3rem;
  background: #e5e7eb;
  border-radius: 0.5rem;
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.error-box {
  padding: 1rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 0.5rem;
  color: #991b1b;
}

.user-items {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.user-card {
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
}

.user-name {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.user-email {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.user-company {
  font-size: 0.75rem;
  color: #9ca3af;
}
```

```jsx live
export default function RemoteDataDemo() {
  const [users, setUsers] = React.useState([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState(null);
  
  React.useEffect(() => {
    fetch('https://jsonplaceholder.typicode.com/users?_limit=5')
      .then(res => res.json())
      .then(data => {
        setUsers(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);
  
  if (loading) {
    return (
      <div className="user-list">
        <div className="loading-skeleton">
          <div className="skeleton-item"></div>
          <div className="skeleton-item"></div>
          <div className="skeleton-item"></div>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="user-list">
        <div className="error-box">
          Error: {error}
        </div>
      </div>
    );
  }
  
  return (
    <div className="user-list">
      <h3>Users (Remote API)</h3>
      <div className="user-items">
        {users.map(user => (
          <div key={user.id} className="user-card">
            <div className="user-name">{user.name}</div>
            <div className="user-email">{user.email}</div>
            <div className="user-company">{user.company.name}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
```

**Why fetch() in your specs:**
- Validate API contracts early
- Show real loading and error states
- Prototype with live data before build time
- Catch latency issues in design phase

---

## Key Differences

| Pattern | When to Use | Pros | Cons |
|---------|------------|------|------|
| **JSON Import** | Static data, repeatable demos | Fast, offline, no CORS | Can't show real API behavior |
| **Remote Fetch** | Live data, API validation | Realistic, shows latency | Requires internet, CORS issues |

**Note:** The fetch example uses a public API (jsonplaceholder.typicode.com) that works without authentication. For your own APIs, adjust the URL and handle auth as needed.

---

## Files

- `products.json` - Sample product data for local import example

---
*Created with [Reactive MD](https://marketplace.visualstudio.com/items?itemName=million-views.reactive-md)*
