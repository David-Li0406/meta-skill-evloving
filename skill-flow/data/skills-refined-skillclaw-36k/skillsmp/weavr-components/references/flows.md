# Weavr Integration Flows

## Corporate Onboarding Flow

```
1. Create Corporate (Server)
   POST /multi/corporates
   ↓
2. Set Password (Client - Secure UI)
   form.input("p", "password") → tokenize → POST /multi/passwords
   ↓
3. Start KYB (Server)
   POST /multi/corporates/{id}/kyb/start → returns reference
   ↓
4. Complete KYB (Client - Secure UI)
   OpcUxSecureClient.kyb().init({ reference })
   ↓
5. Poll KYB Status (Server)
   GET /multi/corporates/{id}/kyb → wait for APPROVED
```

### Implementation

```typescript
// Step 1: Create corporate (server)
const corporate = await createCorporate({
  rootUser: { name, surname, email, mobile, companyPosition, dateOfBirth },
  company: { type, name, registrationNumber, registrationCountry, businessAddress },
  baseCurrency: 'GBP'
});

// Step 2: Set password (client)
window.OpcUxSecureClient.init(uiKey);
const form = window.OpcUxSecureClient.form();
const passwordInput = form.input("p", "password", { placeholder: "Create password" });
const confirmInput = form.input("cp", "confirmPassword", { placeholder: "Confirm password" });

passwordInput.mount(document.getElementById("password"));
confirmInput.mount(document.getElementById("confirm-password"));

form.tokenize(async (tokens) => {
  await fetch('/api/set-password', {
    method: 'POST',
    body: JSON.stringify({
      corporateId: corporate.id,
      password: tokens.password
    })
  });
});

// Step 3: Start KYB (server)
const kybResponse = await startKyb(corporate.id);

// Step 4: Complete KYB (client)
window.OpcUxSecureClient.associate(
  `Bearer ${authToken}`,
  () => {
    window.OpcUxSecureClient.kyb().init(
      document.getElementById("kyb-container"),
      { accessToken: authToken, reference: kybResponse.reference },
      (messageType, payload) => {
        if (messageType === 'complete') {
          // KYB submitted - poll for approval
        }
      },
      { lang: "en" }
    );
  }
);
```

## Consumer Onboarding Flow

```
1. Create Consumer (Server)
   POST /multi/consumers
   ↓
2. Set Password (Client - Secure UI)
   form.input("p", "password") → tokenize → POST /multi/passwords
   ↓
3. Start KYC (Server)
   POST /multi/consumers/{id}/kyc/start → returns reference
   ↓
4. Complete KYC (Client - Secure UI)
   OpcUxSecureClient.consumer_kyc().init({ reference })
   ↓
5. Poll KYC Status (Server)
   GET /multi/consumers/{id}/kyc → wait for APPROVED
```

### Implementation

```typescript
// Step 1: Create consumer (server)
const consumer = await createConsumer({
  rootUser: { name, surname, email, mobile, dateOfBirth, address },
  baseCurrency: 'GBP'
});

// Step 2-3: Same pattern as corporate

// Step 4: Complete KYC (client)
window.OpcUxSecureClient.associate(
  `Bearer ${authToken}`,
  () => {
    window.OpcUxSecureClient.consumer_kyc().init({
      selector: document.getElementById("kyc-container"),
      reference: kycReference,
      lang: "en",
      onMessage: (message) => {
        if (message.type === "kycSubmitted") {
          // KYC submitted - poll for approval
        }
      },
      onError: (error) => console.error(error)
    });
  }
);
```

## Card Issuance Flow

```
1. Verify KYC/KYB Status (Server)
   GET /multi/corporates/{id}/kyb or /multi/consumers/{id}/kyc
   ↓
2. Create Managed Account (Server)
   POST /multi/managed_accounts
   ↓
3. Fund Account (Server)
   POST /multi/transfers (from funding source)
   ↓
4. Create Card (Server)
   POST /multi/managed_cards
   ↓
5. (Optional) Request Physical Card with PIN (Client)
   Step-up auth → form.input("cardPin") → POST /managed_cards/{id}/physical
```

### Implementation

```typescript
// Step 2: Create account (server)
const account = await createManagedAccount({
  profileId: ACCOUNT_PROFILE_ID,
  friendlyName: 'Main Account',
  currency: 'GBP'
});

// Step 4: Create card (server)
const card = await createManagedCard({
  profileId: CARD_PROFILE_ID,
  friendlyName: 'Business Card',
  currency: 'GBP',
  cardholderMobileNumber: mobile,
  billingAddress: address
});

// Step 5: Physical card with PIN (client)
window.OpcUxSecureClient.associate(
  `Bearer ${steppedUpToken}`,
  () => {
    const form = window.OpcUxSecureClient.form();
    const pinInput = form.input("cardPin", "cardPin", { placeholder: "Set PIN" });
    pinInput.mount(document.getElementById("pin-input"));

    form.tokenize(async (tokens) => {
      await fetch(`/api/cards/${cardId}/physical`, {
        method: 'POST',
        body: JSON.stringify({ pin: tokens.cardPin })
      });
    });
  }
);
```

## Card Display Flow (View Card Details)

```
1. Login User (Server)
   POST /multi/passwords/login_with_password → auth token
   ↓
2. Request Step-up Auth (Server)
   POST /multi/authentication/step-up → challenge sent
   ↓
3. Verify Step-up (Server)
   POST /multi/authentication/step-up/verify → stepped-up token
   ↓
4. Get Card Details (Server)
   GET /multi/managed_cards/{id} → tokenized card data
   ↓
5. Display Card (Client - Secure UI)
   OpcUxSecureClient.associate() → span("cardNumber", token)
```

### Implementation

```typescript
// Step 2-3: Step-up auth (server)
await requestStepUp(userId);
const steppedUpToken = await verifyStepUp(userId, otpCode);

// Step 4: Get card details (server)
const card = await getCard(cardId, steppedUpToken);
// card contains: cardNumber: { value: "tokenized_value" }

// Step 5: Display card (client)
window.OpcUxSecureClient.associate(
  `Bearer ${steppedUpToken}`,
  () => {
    const cardNumberSpan = window.OpcUxSecureClient.span("cardNumber", card.cardNumber.value);
    cardNumberSpan.mount(document.getElementById("card-number"));

    const cvvSpan = window.OpcUxSecureClient.span("cvv", card.cvv.value);
    cvvSpan.mount(document.getElementById("cvv"));
  },
  (error) => console.error("Association failed:", error)
);
```

## Authentication Flow

```
1. Show Login Form (Client - Secure UI)
   form.input("p", "password") → tokenize
   ↓
2. Login Request (Server)
   POST /multi/passwords/login_with_password
   ↓
3. Store Auth Token (Client)
   Save token for subsequent requests
```

### Implementation

```javascript
// Client
window.OpcUxSecureClient.init(uiKey);
const form = window.OpcUxSecureClient.form();
const input = form.input("p", "password", { placeholder: "Password" });
input.mount(document.getElementById("password"));

input.on("submit", () => {
  form.tokenize(async (tokens) => {
    const response = await fetch('/api/login', {
      method: 'POST',
      body: JSON.stringify({ email, password: tokens.password })
    });
    const { token } = await response.json();
    localStorage.setItem('authToken', token);
  });
});
```

## Payment Transfer Flow

```
1. Verify Sufficient Balance (Server)
   GET /multi/managed_accounts/{id}
   ↓
2. Create Transfer (Server)
   POST /multi/transfers (internal)
   POST /multi/sends (to external card/account)
   POST /multi/outgoing_wire_transfers (bank transfer)
```

### Implementation

```typescript
// Internal transfer between accounts
const transfer = await createTransfer({
  profileId: TRANSFER_PROFILE_ID,
  source: { type: 'managed_accounts', id: sourceAccountId },
  destination: { type: 'managed_accounts', id: destAccountId },
  destinationAmount: { currency: 'GBP', amount: 10000 } // Amount in minor units (pence)
});

// Wire transfer to external bank
const wireTransfer = await createWireTransfer({
  profileId: OWT_PROFILE_ID,
  sourceInstrument: { type: 'managed_accounts', id: sourceAccountId },
  transferAmount: { currency: 'GBP', amount: 10000 },
  beneficiary: beneficiaryId
});
```

## Step-up Authentication Pattern

Use when performing sensitive operations (card display, PIN operations):

```typescript
// Server-side helper
async function getSteppedUpToken(userId: string, otpCode: string): Promise<string> {
  // 1. Request step-up challenge
  await fetch('/multi/authentication/step-up', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${authToken}` }
  });

  // 2. User receives OTP via SMS/email

  // 3. Verify OTP and get stepped-up token
  const response = await fetch('/multi/authentication/step-up/verify', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${authToken}` },
    body: JSON.stringify({ verificationCode: otpCode })
  });

  return response.token; // Stepped-up token valid for sensitive operations
}
```
