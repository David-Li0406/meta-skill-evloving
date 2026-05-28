---
name: data-layer
description: Architecture du data layer
domain: tracking
---

# Data Layer - Architecture des Données

Tu es expert en **data layer** pour structurer les données de tracking.

## Ta Responsabilité

> Concevoir et documenter une architecture data layer robuste et maintenable.

## Qu'est-ce que le Data Layer

```javascript
// Le data layer est un tableau JavaScript
window.dataLayer = window.dataLayer || [];

// On y "push" des objets de données
dataLayer.push({
  'event': 'page_view',
  'page_type': 'product',
  'user_id': '12345'
});
```

## Architecture Recommandée

### Structure de Base

```javascript
dataLayer.push({
  // Identification de l'event
  'event': 'event_name',

  // Contexte page
  'page': {
    'type': 'product',
    'category': 'Chaussures',
    'name': 'Nike Air Max 90'
  },

  // Utilisateur
  'user': {
    'id': 'user_123',
    'logged_in': true,
    'type': 'customer'
  },

  // E-commerce (si applicable)
  'ecommerce': {
    // Objets GA4 standard
  }
});
```

### Events E-commerce GA4

```javascript
// View Item
dataLayer.push({ ecommerce: null });  // Clear previous
dataLayer.push({
  'event': 'view_item',
  'ecommerce': {
    'currency': 'EUR',
    'value': 89.99,
    'items': [{
      'item_id': 'SKU123',
      'item_name': 'Nike Air Max 90',
      'item_brand': 'Nike',
      'item_category': 'Chaussures',
      'item_category2': 'Running',
      'price': 89.99,
      'quantity': 1
    }]
  }
});

// Add to Cart
dataLayer.push({ ecommerce: null });
dataLayer.push({
  'event': 'add_to_cart',
  'ecommerce': {
    'currency': 'EUR',
    'value': 89.99,
    'items': [{
      'item_id': 'SKU123',
      'item_name': 'Nike Air Max 90',
      'price': 89.99,
      'quantity': 1
    }]
  }
});

// Purchase
dataLayer.push({ ecommerce: null });
dataLayer.push({
  'event': 'purchase',
  'ecommerce': {
    'transaction_id': 'T12345',
    'value': 179.98,
    'tax': 30.00,
    'shipping': 5.99,
    'currency': 'EUR',
    'items': [{
      'item_id': 'SKU123',
      'item_name': 'Nike Air Max 90',
      'price': 89.99,
      'quantity': 2
    }]
  }
});
```

## Data Layer par Page Type

### Page Produit

```javascript
dataLayer.push({
  'event': 'view_item',
  'page_type': 'product',
  'ecommerce': {
    'currency': 'EUR',
    'value': 89.99,
    'items': [{ /* product data */ }]
  }
});
```

### Page Catégorie

```javascript
dataLayer.push({
  'event': 'view_item_list',
  'page_type': 'category',
  'ecommerce': {
    'item_list_id': 'category_running',
    'item_list_name': 'Running Shoes',
    'items': [{ /* product array */ }]
  }
});
```

### Page Checkout

```javascript
dataLayer.push({
  'event': 'begin_checkout',
  'page_type': 'checkout',
  'ecommerce': {
    'currency': 'EUR',
    'value': 179.98,
    'items': [{ /* cart items */ }]
  }
});
```

### Page Confirmation

```javascript
dataLayer.push({
  'event': 'purchase',
  'page_type': 'confirmation',
  'ecommerce': {
    'transaction_id': 'T12345',
    /* ... */
  }
});
```

## Custom Events

### Formulaire Lead

```javascript
dataLayer.push({
  'event': 'generate_lead',
  'form_id': 'contact_form',
  'form_name': 'Demande de devis',
  'lead_value': 100  // Valeur estimée
});
```

### Interactions UI

```javascript
dataLayer.push({
  'event': 'cta_click',
  'cta_text': 'Voir les offres',
  'cta_location': 'hero_banner',
  'cta_url': '/offres'
});
```

## Documentation Data Layer

### Template de Documentation

| Event | Trigger | Paramètres | Exemple |
|-------|---------|------------|---------|
| `view_item` | Page produit | item_id, item_name, price, currency | Voir spec |
| `add_to_cart` | Clic ATC | items[], value, currency | Voir spec |
| `purchase` | Page confirmation | transaction_id, value, items[] | Voir spec |

## Debugging Data Layer

### Dans la Console

```javascript
// Voir le data layer
console.log(dataLayer);

// Observer les push
dataLayer.push = function(e) {
  console.log('DataLayer push:', e);
  Array.prototype.push.call(dataLayer, e);
};
```

### GTM Preview Mode

1. Activer Preview dans GTM
2. Onglet "Data Layer"
3. Voir chaque push et ses valeurs

## Checklist Data Layer

- [ ] Structure documentée
- [ ] Events GA4 standards respectés
- [ ] Clear ecommerce avant chaque push
- [ ] Items array correctement formaté
- [ ] Custom events définis
- [ ] Variables GTM créées
- [ ] Tests effectués par page type
