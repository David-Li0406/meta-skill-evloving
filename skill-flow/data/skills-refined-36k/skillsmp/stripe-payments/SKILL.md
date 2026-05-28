---
name: Stripe Payments
description: Payment processing, subscriptions, and checkout integration
---

# Stripe Payments Skill

## Setup
```bash
npm install stripe @stripe/stripe-js @stripe/react-stripe-js
```

## Environment Variables
```env
STRIPE_SECRET_KEY=sk_test_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

## Server-Side (API Routes)

### Create Checkout Session
```javascript
// pages/api/checkout.js
import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

export default async function handler(req, res) {
  const session = await stripe.checkout.sessions.create({
    payment_method_types: ['card'],
    line_items: [{
      price_data: {
        currency: 'usd',
        product_data: {
          name: '1000 Diamonds',
          images: ['https://smarter.poker/diamonds.png']
        },
        unit_amount: 999, // $9.99 in cents
      },
      quantity: 1,
    }],
    mode: 'payment',
    success_url: `${process.env.NEXT_PUBLIC_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.NEXT_PUBLIC_URL}/store`,
    metadata: {
      userId: req.body.userId,
      diamonds: 1000
    }
  });
  
  res.json({ sessionId: session.id });
}
```

### Create Subscription
```javascript
const session = await stripe.checkout.sessions.create({
  mode: 'subscription',
  line_items: [{
    price: 'price_vip_monthly', // Price ID from Stripe dashboard
    quantity: 1,
  }],
  success_url: `${process.env.NEXT_PUBLIC_URL}/success`,
  cancel_url: `${process.env.NEXT_PUBLIC_URL}/pricing`,
});
```

### Webhook Handler
```javascript
// pages/api/webhooks/stripe.js
import { buffer } from 'micro';
import Stripe from 'stripe';

export const config = { api: { bodyParser: false } };

export default async function handler(req, res) {
  const buf = await buffer(req);
  const sig = req.headers['stripe-signature'];
  
  let event;
  try {
    event = stripe.webhooks.constructEvent(buf, sig, process.env.STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }
  
  switch (event.type) {
    case 'checkout.session.completed':
      await handleCheckoutComplete(event.data.object);
      break;
    case 'invoice.paid':
      await handleSubscriptionRenewal(event.data.object);
      break;
    case 'customer.subscription.deleted':
      await handleSubscriptionCancelled(event.data.object);
      break;
  }
  
  res.json({ received: true });
}
```

## Client-Side

### Checkout Button
```jsx
import { loadStripe } from '@stripe/stripe-js';

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY);

export function BuyDiamondsButton({ userId }) {
  const handleClick = async () => {
    const stripe = await stripePromise;
    const response = await fetch('/api/checkout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ userId })
    });
    const { sessionId } = await response.json();
    await stripe.redirectToCheckout({ sessionId });
  };
  
  return <button onClick={handleClick}>Buy 1000 Diamonds - $9.99</button>;
}
```

## Database Integration
```javascript
async function handleCheckoutComplete(session) {
  const { userId, diamonds } = session.metadata;
  
  await supabase
    .from('transactions')
    .insert({
      user_id: userId,
      stripe_session_id: session.id,
      amount: session.amount_total,
      diamonds: parseInt(diamonds),
      status: 'completed'
    });
  
  await supabase.rpc('add_diamonds', { 
    user_id: userId, 
    amount: parseInt(diamonds) 
  });
}
```

## Testing
```bash
# Test webhook locally
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# Trigger test events
stripe trigger checkout.session.completed
```
