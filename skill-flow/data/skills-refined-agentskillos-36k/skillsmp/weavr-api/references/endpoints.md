# Weavr Multi API Endpoints

Full API Reference: https://weavr-multi-api.redoc.ly/

## Identity Management

### Corporates

```
POST   /multi/corporates                           Create corporate
GET    /multi/corporates/{id}                      Get corporate
PATCH  /multi/corporates/{id}                      Update corporate
POST   /multi/corporates/{id}/kyb/start            Start KYB verification
GET    /multi/corporates/{id}/kyb                  Get KYB status
```

**Create Corporate Request:**

```json
{
  "tag": "optional-tag",
  "rootUser": {
    "name": "string",
    "surname": "string",
    "email": "string",
    "mobile": { "countryCode": "+44", "number": "7700900123" },
    "companyPosition": "DIRECTOR|SHAREHOLDER|AUTHORISED_REPRESENTATIVE|ULTIMATE_BENEFICIAL_OWNER",
    "dateOfBirth": { "year": 1985, "month": 6, "day": 15 },
    "tag": "optional"
  },
  "company": {
    "type": "LLC|SOLE_TRADER|PUBLIC_LIMITED_COMPANY|PRIVATE_LIMITED_COMPANY|PARTNERSHIP",
    "name": "string",
    "registrationNumber": "string",
    "registrationCountry": "GB",
    "businessAddress": {
      "addressLine1": "string",
      "addressLine2": "optional",
      "city": "string",
      "postCode": "string",
      "state": "optional",
      "country": "GB"
    }
  },
  "baseCurrency": "GBP|EUR|USD",
  "feeGroup": "optional",
  "ipAddress": "optional"
}
```

### Consumers

```
POST   /multi/consumers                            Create consumer
GET    /multi/consumers/{id}                       Get consumer
PATCH  /multi/consumers/{id}                       Update consumer
POST   /multi/consumers/{id}/kyc/start             Start KYC verification
GET    /multi/consumers/{id}/kyc                   Get KYC status
```

**Create Consumer Request:**

```json
{
  "tag": "optional-tag",
  "rootUser": {
    "name": "string",
    "surname": "string",
    "email": "string",
    "mobile": { "countryCode": "+44", "number": "7700900123" },
    "dateOfBirth": { "year": 1990, "month": 3, "day": 20 },
    "address": {
      "addressLine1": "string",
      "city": "string",
      "postCode": "string",
      "country": "GB"
    }
  },
  "baseCurrency": "GBP|EUR|USD",
  "feeGroup": "optional",
  "ipAddress": "optional"
}
```

## User Authentication

```
POST   /multi/login_with_password                  Login with password
POST   /multi/passwords                            Create password
PATCH  /multi/passwords                            Update password
POST   /multi/passwords/lost_password/start        Start password reset
POST   /multi/passwords/lost_password/validate     Complete password reset
```

**Login Request:**

```json
{
  "email": "user@example.com",
  "password": { "value": "string" }
}
```

## Strong Customer Authentication (SCA)

```
POST   /multi/authentication/step-up               Request step-up auth
POST   /multi/authentication/step-up/verify        Verify step-up (OTP)
GET    /multi/authentication/factors               List auth factors
POST   /multi/authentication/otp/enroll            Enroll OTP
```

## Financial Instruments

### Managed Accounts

```
POST   /multi/managed_accounts                     Create managed account
GET    /multi/managed_accounts                     List accounts
GET    /multi/managed_accounts/{id}                Get account
GET    /multi/managed_accounts/{id}/statement      Get statement
POST   /multi/managed_accounts/{id}/iban           Assign IBAN to account
GET    /multi/managed_accounts/{id}/iban           Get IBAN details
```

**IBAN Assignment:**
- POST assigns an IBAN (account must be ACTIVE)
- GET retrieves IBAN details after assignment
- Response includes `state` ("UNALLOCATED" or "ALLOCATED") and `bankAccountDetails`

**Create Account Request:**

```json
{
  "profileId": "string",
  "tag": "optional",
  "friendlyName": "Main Account",
  "currency": "GBP"
}
```

### Managed Cards

```
POST   /multi/managed_cards                        Create managed card
GET    /multi/managed_cards                        List cards
GET    /multi/managed_cards/{id}                   Get card
PATCH  /multi/managed_cards/{id}                   Update card
POST   /multi/managed_cards/{id}/physical/activate Activate physical card
```

**Create Card Request:**

```json
{
  "profileId": "string",
  "tag": "optional",
  "friendlyName": "My Card",
  "currency": "GBP",
  "cardholderMobileNumber": { "countryCode": "+44", "number": "7700900123" },
  "billingAddress": {
    "addressLine1": "string",
    "city": "string",
    "postCode": "string",
    "country": "GB"
  }
}
```

## Transfers & Payments

### Internal Transfers

```
POST   /multi/transfers                            Create transfer
GET    /multi/transfers                            List transfers
GET    /multi/transfers/{id}                       Get transfer
```

**Transfer Request:**

```json
{
  "profileId": "string",
  "tag": "optional",
  "source": { "type": "managed_accounts", "id": "source_account_id" },
  "destination": { "type": "managed_accounts", "id": "dest_account_id" },
  "destinationAmount": { "currency": "GBP", "amount": 1000 }
}
```

### External Sends

```
POST   /multi/sends                                Create send
GET    /multi/sends                                List sends
GET    /multi/sends/{id}                           Get send
```

### Wire Transfers

```
POST   /multi/outgoing_wire_transfers              Create wire transfer
GET    /multi/outgoing_wire_transfers              List wire transfers
GET    /multi/outgoing_wire_transfers/{id}         Get wire transfer
```

## Beneficiaries

```
POST   /multi/beneficiaries                        Create beneficiary
GET    /multi/beneficiaries                        List beneficiaries
GET    /multi/beneficiaries/{id}                   Get beneficiary
DELETE /multi/beneficiaries/{id}                   Delete beneficiary
```

## Authorized Users

```
POST   /multi/users                                Create authorized user
GET    /multi/users                                List users
GET    /multi/users/{id}                           Get user
PATCH  /multi/users/{id}                           Update user
POST   /multi/users/{id}/activate                  Activate user
POST   /multi/users/{id}/deactivate                Deactivate user
```

## Common Response Codes

| Code | Description                          |
| ---- | ------------------------------------ |
| 200  | Success                              |
| 201  | Created                              |
| 400  | Bad Request - validation error       |
| 401  | Unauthorized - invalid/missing auth  |
| 403  | Forbidden - insufficient permissions |
| 404  | Not Found                            |
| 409  | Conflict - duplicate resource        |
| 429  | Rate Limited                         |

## Enums Reference

### Company Types

- `LLC` - Limited Liability Company
- `SOLE_TRADER` - Sole Trader
- `PUBLIC_LIMITED_COMPANY` - Public Limited Company (PLC)
- `PRIVATE_LIMITED_COMPANY` - Private Limited Company
- `PARTNERSHIP` - Partnership

### Company Positions

- `DIRECTOR`
- `SHAREHOLDER`
- `AUTHORISED_REPRESENTATIVE`
- `ULTIMATE_BENEFICIAL_OWNER`

### KYC/KYB States

- `NOT_STARTED`
- `PENDING_REVIEW`
- `APPROVED`
- `REJECTED`

### Card States

- `ACTIVE`
- `INACTIVE`
- `BLOCKED`
- `DESTROYED`

### Transaction States

- `PENDING`
- `COMPLETED`
- `REJECTED`
- `FAILED`
