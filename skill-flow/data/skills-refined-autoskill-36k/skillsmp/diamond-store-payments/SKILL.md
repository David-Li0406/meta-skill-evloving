---
name: Diamond Store & Payments
description: In-app purchases, diamond bundles, and payment processing
---

# Diamond Store & Payments Skill

## Overview
Implement the diamond store with Stripe payment processing for in-app purchases.

## Diamond Bundles
```javascript
const DIAMOND_BUNDLES = [
  { id: 'starter', name: 'Starter Pack', diamonds: 100, price: 0.99, bonus: 0 },
  { id: 'basic', name: 'Basic Pack', diamonds: 500, price: 4.99, bonus: 25 },
  { id: 'popular', name: 'Popular Pack', diamonds: 1200, price: 9.99, bonus: 100, featured: true },
  { id: 'value', name: 'Value Pack', diamonds: 2500, price: 19.99, bonus: 300 },
  { id: 'premium', name: 'Premium Pack', diamonds: 6500, price: 49.99, bonus: 1000 },
  { id: 'ultimate', name: 'Ultimate Pack', diamonds: 14000, price: 99.99, bonus: 3000 }
];
```

## Stripe Integration

### Create Checkout Session
```javascript
// pages/api/payments/create-checkout.js
import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

export default async function handler(req, res) {
  const { bundleId, userId } = req.body;
  const bundle = DIAMOND_BUNDLES.find(b => b.id === bundleId);
  
  const session = await stripe.checkout.sessions.create({
    payment_method_types: ['card'],
    line_items: [{
      price_data: {
        currency: 'usd',
        product_data: {
          name: bundle.name,
          description: `${bundle.diamonds + bundle.bonus} Diamonds`
        },
        unit_amount: Math.round(bundle.price * 100)
      },
      quantity: 1
    }],
    mode: 'payment',
    success_url: `${process.env.NEXT_PUBLIC_URL}/hub/diamond-store?success=true&session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.NEXT_PUBLIC_URL}/hub/diamond-store?canceled=true`,
    metadata: {
      userId,
      bundleId,
      diamonds: bundle.diamonds + bundle.bonus
    }
  });
  
  res.json({ sessionId: session.id });
}
```

### Webhook Handler
```javascript
// pages/api/payments/webhook.js
export default async function handler(req, res) {
  const event = stripe.webhooks.constructEvent(
    req.body,
    req.headers['stripe-signature'],
    process.env.STRIPE_WEBHOOK_SECRET
  );
  
  if (event.type === 'checkout.session.completed') {
    const session = event.data.object;
    const { userId, diamonds } = session.metadata;
    
    // Award diamonds
    await supabase.rpc('award_diamonds', {
      p_user_id: userId,
      p_amount: parseInt(diamonds),
      p_source: `purchase:${session.id}`
    });
    
    // Record transaction
    await supabase.from('purchase_history').insert({
      user_id: userId,
      stripe_session_id: session.id,
      amount_paid: session.amount_total / 100,
      diamonds_awarded: parseInt(diamonds)
    });
  }
  
  res.json({ received: true });
}
```

## Database
```sql
CREATE TABLE purchase_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  stripe_session_id TEXT UNIQUE,
  amount_paid DECIMAL(10, 2),
  diamonds_awarded INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) UNIQUE,
  stripe_subscription_id TEXT,
  plan TEXT, -- 'monthly', 'annual'
  status TEXT, -- 'active', 'canceled', 'past_due'
  current_period_end TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## VIP Subscription
```javascript
async function createVIPSubscription(userId, planId) {
  const prices = {
    monthly: 'price_monthly_id',
    annual: 'price_annual_id'
  };
  
  const session = await stripe.checkout.sessions.create({
    payment_method_types: ['card'],
    line_items: [{ price: prices[planId], quantity: 1 }],
    mode: 'subscription',
    success_url: `${process.env.NEXT_PUBLIC_URL}/hub/settings?vip=success`,
    cancel_url: `${process.env.NEXT_PUBLIC_URL}/hub/diamond-store`,
    metadata: { userId, plan: planId }
  });
  
  return session;
}
```

## Components
- `DiamondStore.jsx` - Main store page
- `BundleCard.jsx` - Purchase option display
- `CheckoutButton.jsx` - Stripe checkout trigger
- `PurchaseHistory.jsx` - Transaction history
- `VIPBanner.jsx` - Subscription upsell
