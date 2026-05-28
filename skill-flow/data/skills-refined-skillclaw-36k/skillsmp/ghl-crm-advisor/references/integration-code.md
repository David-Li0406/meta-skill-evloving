# GHL Integration Code Patterns

## Authentication

```typescript
// Private Integration Token (recommended for ACT)
const headers = {
  'Authorization': `Bearer ${process.env.GHL_PRIVATE_TOKEN}`,
  'Content-Type': 'application/json',
  'Version': '2021-07-28'
};
```

## GHL API Client with Retry

```typescript
import pRetry from 'p-retry';

async function callGHLAPI(endpoint, options) {
  return await pRetry(
    async () => {
      const response = await fetch(
        `https://services.leadconnectorhq.com${endpoint}`,
        { ...options, headers }
      );

      if (response.status === 429) throw new Error('Rate limit');
      if (!response.ok) throw new Error(`API error: ${response.status}`);

      return response.json();
    },
    { retries: 3, factor: 2, minTimeout: 500 }
  );
}
```

## Contact Upsert Pattern

```typescript
async function handleContactSubmission(formData) {
  const contact = await ghlClient.contacts.upsert({
    email: formData.email,
    name: formData.name,
    phone: formData.phone,
    source: '[Project] Website',
    tags: ['project-name', `interest:${formData.interest}`],
    customFields: {
      interest_area: formData.interest,
      submission_date: new Date().toISOString(),
    },
  });

  // Add to pipeline
  await ghlClient.opportunities.create({
    contactId: contact.id,
    pipelineId: PIPELINE_ID,
    pipelineStageId: INITIAL_STAGE_ID,
    name: `${formData.name} - ${formData.interest}`,
    status: 'open',
  });

  return contact;
}
```

## Supabase → GHL Sync

```typescript
async function syncToGHL(supabaseUser) {
  const contact = await ghlClient.contacts.upsert({
    email: supabaseUser.email,
    name: supabaseUser.user_metadata.full_name,
    tags: ['empathy-ledger', `role:${supabaseUser.user_metadata.role}`],
    customFields: {
      supabase_user_id: supabaseUser.id,
      account_created: supabaseUser.created_at,
    },
  });

  // Store sync relationship
  await supabase.from('ghl_contact_sync').upsert({
    supabase_user_id: supabaseUser.id,
    ghl_contact_id: contact.id,
    last_synced: new Date().toISOString(),
  });
}
```

## Stripe Webhook Handler

```typescript
// app/api/webhooks/stripe/route.ts
export async function POST(request: Request) {
  const body = await request.text();
  const signature = headers().get('stripe-signature')!;

  const event = stripe.webhooks.constructEvent(
    body, signature, process.env.STRIPE_WEBHOOK_SECRET!
  );

  if (event.type === 'checkout.session.completed') {
    const session = event.data.object;
    const { contactId } = session.metadata!;

    await ghlClient.contacts.updateCustomFields(contactId, {
      payment_status: 'fully_paid',
      amount_paid: session.amount_total! / 100,
      stripe_charge_id: session.payment_intent,
    });

    await ghlClient.workflows.trigger(
      process.env.GHL_BOOKING_CONFIRMED_WORKFLOW_ID!,
      { contactId }
    );
  }

  return Response.json({ received: true });
}
```

## GHL Webhook Handler

```typescript
// app/api/webhooks/ghl/route.ts
import crypto from 'crypto';

export async function POST(req) {
  const signature = req.headers.get('x-ghl-signature');
  const body = await req.text();

  const expected = crypto
    .createHmac('sha256', process.env.GHL_WEBHOOK_SECRET)
    .update(body)
    .digest('hex');

  if (signature !== expected) {
    return Response.json({ error: 'Invalid signature' }, { status: 401 });
  }

  const event = JSON.parse(body);

  switch (event.type) {
    case 'ContactCreate':
      // Handle new contact
      break;
    case 'OpportunityStatusUpdate':
      // Handle deal won/lost
      break;
  }

  return Response.json({ success: true });
}
```

## Environment Variables

```bash
GHL_PRIVATE_TOKEN=your-private-token
GHL_LOCATION_ID=your-location-id
GHL_WEBHOOK_SECRET=your-webhook-secret
```
