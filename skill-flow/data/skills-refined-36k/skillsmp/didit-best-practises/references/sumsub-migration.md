# Sumsub to Didit Migration Guide

## Overview

This guide covers migrating from Sumsub to Didit for identity verification. Didit offers a simpler API, built-in white-label support, and competitive pricing.

## Concept Mapping

| Sumsub Concept | Didit Equivalent | Notes |
|----------------|------------------|-------|
| Applicant | Session | Didit uses session-based verification |
| Level | Workflow | Configure in Console |
| Access Token | API Key | Single key per application |
| SDK Token | Session URL | Direct URL, no SDK required |
| Webhook Secret | - | Simpler webhook structure |

## Authentication Migration

### Sumsub (Before)
```typescript
// Sumsub requires complex signature generation
const signature = crypto
  .createHmac('sha256', SUMSUB_SECRET_KEY)
  .update(ts + method + path + body)
  .digest('hex');

const headers = {
  'X-App-Token': SUMSUB_APP_TOKEN,
  'X-App-Access-Sig': signature,
  'X-App-Access-Ts': ts
};
```

### Didit (After)
```typescript
// Didit uses simple API key
const headers = {
  'Content-Type': 'application/json',
  'x-api-key': DIDIT_API_KEY
};
```

## Session Creation Migration

### Sumsub (Before)
```typescript
// Create applicant
const applicant = await fetch('https://api.sumsub.com/resources/applicants', {
  method: 'POST',
  headers: sumsubHeaders,
  body: JSON.stringify({
    externalUserId: userId,
    levelName: 'basic-kyc-level'
  })
});

// Generate SDK token
const token = await fetch(
  `https://api.sumsub.com/resources/accessTokens?userId=${userId}&levelName=basic-kyc-level`,
  { method: 'POST', headers: sumsubHeaders }
);
```

### Didit (After)
```typescript
// Single API call creates session with URL
const session = await fetch('https://verification.didit.me/v3/session/', {
  method: 'POST',
  headers: diditHeaders,
  body: JSON.stringify({
    workflow_id: WORKFLOW_ID,
    vendor_data: userId,
    callback: 'https://yourapp.com/verification-complete'
  })
});

const { session_id, url } = await session.json();
// Redirect user to url - no SDK integration needed
```

## Frontend Migration

### Sumsub (Before)
```typescript
// Required SDK installation and initialization
import snsWebSdk from '@sumsub/websdk';

const sdk = snsWebSdk
  .init(accessToken, () => getNewAccessToken())
  .withConf({ lang: 'en' })
  .on('onError', handleError)
  .on('onMessage', handleMessage)
  .build();

sdk.launch('#sumsub-container');
```

### Didit (After)
```typescript
// No SDK required - simple redirect or iframe
window.location.href = sessionUrl;

// Or popup
window.open(sessionUrl, 'verification', 'width=500,height=700');

// Or iframe
<iframe src={sessionUrl} allow="camera; microphone" />
```

## Webhook Migration

### Sumsub Webhook (Before)
```typescript
interface SumsubWebhook {
  applicantId: string;
  inspectionId: string;
  correlationId: string;
  externalUserId: string;
  type: string;
  reviewStatus: string;
  reviewResult: {
    reviewAnswer: 'GREEN' | 'RED';
    rejectLabels?: string[];
    reviewRejectType?: string;
  };
  createdAt: string;
}

app.post('/webhooks/sumsub', (req, res) => {
  // Verify signature
  const signature = req.headers['x-payload-digest'];
  const expectedSig = crypto
    .createHmac('sha256', WEBHOOK_SECRET)
    .update(JSON.stringify(req.body))
    .digest('hex');
  
  if (signature !== expectedSig) {
    return res.status(401).send('Invalid signature');
  }
  
  const { externalUserId, reviewResult } = req.body;
  
  if (reviewResult.reviewAnswer === 'GREEN') {
    updateUserStatus(externalUserId, 'verified');
  } else {
    handleRejection(externalUserId, reviewResult.rejectLabels);
  }
});
```

### Didit Webhook (After)
```typescript
interface DiditWebhook {
  session_id: string;
  status: 'Approved' | 'Declined' | 'In Review' | 'Expired';
  vendor_data: string; // Your user ID
  // Verification-specific data
}

app.post('/webhooks/didit', (req, res) => {
  const { vendor_data, status } = req.body;
  
  switch (status) {
    case 'Approved':
      updateUserStatus(vendor_data, 'verified');
      break;
    case 'Declined':
      handleDeclined(vendor_data);
      break;
    case 'In Review':
      flagForReview(vendor_data);
      break;
  }
  
  res.status(200).send('OK');
});
```

## Status Mapping

| Sumsub Status | Didit Status |
|---------------|--------------|
| `init` | Not Started |
| `pending` | In Progress |
| `GREEN` (approved) | Approved |
| `RED` (rejected) | Declined |
| `onHold` | In Review |
| - | Expired |
| - | Abandoned |

## Database Schema Migration

### Before (Sumsub)
```sql
CREATE TABLE user_verification (
  user_id VARCHAR PRIMARY KEY,
  sumsub_applicant_id VARCHAR,
  sumsub_inspection_id VARCHAR,
  review_status VARCHAR,
  review_answer VARCHAR,
  reject_labels JSONB,
  verified_at TIMESTAMP
);
```

### After (Didit)
```sql
CREATE TABLE user_verification (
  user_id VARCHAR PRIMARY KEY,
  didit_session_id VARCHAR,
  status VARCHAR, -- Approved, Declined, In Review, etc.
  verified_at TIMESTAMP,
  -- Keep old columns for historical data
  sumsub_applicant_id VARCHAR, -- Legacy
  migrated_at TIMESTAMP
);
```

## Migration Checklist

### Phase 1: Setup
- [ ] Create Didit account at business.didit.me
- [ ] Create Application in Console
- [ ] Configure Workflow matching Sumsub level
- [ ] Copy API Key to environment variables
- [ ] Set up webhook endpoint

### Phase 2: Backend
- [ ] Add Didit API client
- [ ] Create session creation endpoint
- [ ] Implement webhook handler
- [ ] Add session retrieval logic
- [ ] Update database schema

### Phase 3: Frontend
- [ ] Remove Sumsub SDK
- [ ] Implement redirect/iframe flow
- [ ] Handle callback URL
- [ ] Update status display logic

### Phase 4: Testing
- [ ] Test session creation
- [ ] Test verification flow end-to-end
- [ ] Test webhook handling
- [ ] Test all status scenarios
- [ ] Test mobile WebView integration

### Phase 5: Rollout
- [ ] Deploy to staging
- [ ] Run parallel with Sumsub (optional)
- [ ] Migrate new users to Didit
- [ ] Monitor error rates
- [ ] Full cutover
- [ ] Deprecate Sumsub integration

## Feature Comparison

| Feature | Sumsub | Didit |
|---------|--------|-------|
| ID Verification | ✅ | ✅ |
| Liveness | ✅ | ✅ |
| Face Match | ✅ | ✅ |
| AML Screening | ✅ | ✅ |
| NFC Verification | ✅ | ✅ |
| Proof of Address | ✅ | ✅ |
| Age Estimation | ✅ | ✅ |
| SDK Required | Yes | No |
| White Label | Paid add-on | Built-in |
| Custom Domain | Paid add-on | Built-in |
| Reusable KYC | ✅ | ✅ |

## Common Migration Issues

### Issue: SDK Token Expiration
**Sumsub**: Required token refresh logic
**Didit**: Session URLs don't expire during active use

### Issue: Complex Webhook Signatures
**Sumsub**: HMAC signature verification required
**Didit**: Simpler payload, validate via session retrieval if needed

### Issue: Multiple SDK Versions
**Sumsub**: Web SDK, iOS SDK, Android SDK
**Didit**: Single WebView approach works everywhere

### Issue: Applicant State Management
**Sumsub**: Track applicant lifecycle
**Didit**: Stateless sessions, retrieve status when needed
