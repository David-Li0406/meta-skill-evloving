# Weavr Simulator API - Full Endpoint Reference

Base URL: `https://sandbox.weavr.io` (Sandbox only)

All endpoints require `api-key` header with API Secret Key.
Optional `call-ref` header (max 255 chars) for request correlation.

---

## Accounts

### Simulate Incoming Wire Transfer (by Account ID)

```
POST /accounts/{account_id}/deposit
```

```json
{
  "depositAmount": { "currency": "GBP", "amount": 10000 },
  "senderName": "Sender Name",
  "reference": "Payment reference",
  "receiverName": "Receiver Name",
  "txId": "unique-transaction-id",
  "senderIban": "GB29NWBK60161331926819",
  "paymentNetwork": "SEPA"
}
```

**Payment Networks:** `SEPA`, `FASTER_PAYMENTS`, `SWIFT`, `BACS`, `CHAPS`, `RIX`

Response: `{ "code": "COMPLETED" }`

### Simulate Incoming Wire Transfer (by IBAN)

```
POST /accounts/deposit
```

```json
{
  "depositAmount": { "currency": "GBP", "amount": 10000 },
  "destinationIbanDetails": {
    "iban": "GB29NWBK60161331926819",
    "bankIdentifierCode": "NWBKGB2L"
  },
  "senderIbanDetails": {
    "name": "Sender Name",
    "iban": "DE89370400440532013000"
  },
  "paymentReference": "Payment reference",
  "paymentNetwork": "SEPA"
}
```

Alternative destination options:
- `destinationFasterPaymentsDetails`: `{ sortCode, accountNumber }`

---

## Cards

### Simulate Card Purchase (by Card ID)

```
POST /cards/{card_id}/purchase
```

```json
{
  "merchantName": "Test Merchant",
  "merchantId": "MID123456",
  "merchantCategoryCode": "5411",
  "transactionAmount": { "currency": "GBP", "amount": 2500 },
  "transactionCountry": "GBR",
  "atmWithdrawal": false,
  "cardHolderPresent": true,
  "cardPresent": true,
  "additionalMerchantData": {
    "street": "123 High Street",
    "city": "London",
    "state": "London",
    "postalCode": "EC1A 1BB",
    "country": "GBR"
  },
  "transactionTimestamp": 1702234567890
}
```

Response: `{ "code": "APPROVED", "threeDSecureChallengeId": "..." }`

### Simulate Card Purchase (by Card Number)

```
POST /cards/purchase
```

```json
{
  "cardNumber": "4000000000001234",
  "cvv": "123",
  "expiryDate": "1225",
  "merchantName": "Test Merchant",
  "transactionAmount": { "currency": "GBP", "amount": 2500 }
}
```

### Simulate Merchant Refund (by Card ID)

```
POST /cards/{card_id}/merchant_refund
```

Same request body as purchase endpoint.

### Simulate Merchant Refund (by Card Number)

```
POST /cards/merchant_refund
```

Same request body as purchase-by-number endpoint.

### Simulate Card Expiry

```
POST /cards/{card_id}/expire
```

Response: `204 No Content`

### Simulate Card About to Expire

```
POST /cards/{card_id}/about_to_expire
```

Response: `204 No Content`

### Simulate Card Renewal

```
POST /cards/{card_id}/renew
```

Response: `204 No Content`

---

## Identity Verification

### Verify Consumer (Auto-pass KYC)

```
POST /consumers/{consumer_id}/verify
```

No request body required.

Response: `204 No Content`

Sets: `emailVerified`, `mobileVerified`, `isPep=false`, `isSanctioned=false`

### Verify Corporate (Auto-pass KYB)

```
POST /corporates/{corporate_id}/verify
```

No request body required.

Response: `204 No Content`

Sets: `rootEmailVerified`, `rootMobileVerified`, `directorsVerified`, `UBOsVerified`, `basicCompanyChecksVerified`, `fullCompanyChecksVerified`

---

## Wire Transfers

### Accept Outgoing Wire Transfer

```
POST /wiretransfers/outgoing/{outgoing_wire_transfer_id}/accept
```

Response: `{ "code": "COMPLETED" }`

### Reject Outgoing Wire Transfer

```
POST /wiretransfers/outgoing/{outgoing_wire_transfer_id}/reject
```

Response: `{ "code": "COMPLETED" }`

---

## 2FA / Factor Challenges

### Simulate Successful Challenge

```
POST /factors/{credentials_id}/challenges/{challenge_id}/verify_success
```

Response: `{ "code": "COMPLETED" }`

### Simulate Invalid Challenge

```
POST /factors/{credentials_id}/challenges/{challenge_id}/verify_invalid
```

Response: `{ "code": "COMPLETED" }`

### Simulate Expired Challenge

```
POST /factors/{credentials_id}/challenges/{challenge_id}/verify_expired
```

Response: `{ "code": "COMPLETED" }`

---

## Linked Accounts

### Set Linked Account Status

```
POST /linked_accounts/{account_id}/set
```

```json
{
  "state": "VERIFIED"
}
```

States: `VERIFIED`, `REJECTED`

Response: `204 No Content`

### Verify Linked Account Steps

```
POST /linked_accounts/{account_id}/verify
```

```json
{
  "steps": ["INTERNAL_CHECKS", "TRANSFER_INSTRUCTION", "USER_DECLARATION_SCA_CHALLENGE"]
}
```

Response: `204 No Content`

---

## Common Response Codes

| Code | Meaning |
|------|---------|
| `COMPLETED` | Operation successful |
| `APPROVED` | Transaction approved (cards) |
| `204 No Content` | Success (no response body) |

## Error Response Format

```json
{
  "message": "Error description",
  "validation": {
    "invalid": true,
    "fields": [{ "name": "fieldName", "errors": ["error message"] }]
  }
}
```
