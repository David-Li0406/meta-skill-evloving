# Weavr API Quick Reference

Full docs: https://weavr-multi-api.redoc.ly/

## Authentication Headers

```
api-key: {{api_key}}              # Server-side API key
programme-key: {{programme_key}}  # Programme identifier
Authorization: Bearer {{token}}   # User auth token (after login)
Content-Type: application/json
```

## Environments

| Environment | Base URL |
|-------------|----------|
| Sandbox | `https://sandbox.weavr.io` |
| Production | `https://api.weavr.io` |

## Identity Endpoints

### Corporates
```
POST   /multi/corporates                    Create corporate
GET    /multi/corporates/{id}               Get corporate
PATCH  /multi/corporates/{id}               Update corporate
POST   /multi/corporates/{id}/kyb/start     Start KYB
GET    /multi/corporates/{id}/kyb           Get KYB status
```

### Consumers
```
POST   /multi/consumers                     Create consumer
GET    /multi/consumers/{id}                Get consumer
PATCH  /multi/consumers/{id}                Update consumer
POST   /multi/consumers/{id}/kyc/start      Start KYC
GET    /multi/consumers/{id}/kyc            Get KYC status
```

### Authorized Users
```
POST   /multi/users                         Create authorized user
GET    /multi/users                         List users
GET    /multi/users/{id}                    Get user
PATCH  /multi/users/{id}                    Update user
POST   /multi/users/{id}/activate           Activate user
POST   /multi/users/{id}/deactivate         Deactivate user
```

## Authentication Endpoints

```
POST   /multi/passwords/login_with_password   Login
POST   /multi/passwords                       Create password
PATCH  /multi/passwords                       Update password
POST   /multi/passwords/lost_password/start   Start reset
POST   /multi/passwords/lost_password/validate Complete reset
POST   /multi/authentication/step-up          Request step-up
POST   /multi/authentication/step-up/verify   Verify step-up
```

## Financial Instruments

### Managed Accounts
```
POST   /multi/managed_accounts              Create account
GET    /multi/managed_accounts              List accounts
GET    /multi/managed_accounts/{id}         Get account
GET    /multi/managed_accounts/{id}/statement Get statement
GET    /multi/managed_accounts/{id}/iban    Get IBAN
```

### Managed Cards
```
POST   /multi/managed_cards                         Create card
GET    /multi/managed_cards                         List cards
GET    /multi/managed_cards/{id}                    Get card
PATCH  /multi/managed_cards/{id}                    Update card
POST   /multi/managed_cards/{id}/physical           Request physical
POST   /multi/managed_cards/{id}/physical/activate  Activate physical
```

## Transfers

```
POST   /multi/transfers                     Internal transfer
POST   /multi/sends                         External send
POST   /multi/outgoing_wire_transfers       Wire transfer
GET    /multi/transfers/{id}                Get transfer
GET    /multi/sends/{id}                    Get send
GET    /multi/outgoing_wire_transfers/{id}  Get wire transfer
```

## Beneficiaries

```
POST   /multi/beneficiaries                 Create beneficiary
GET    /multi/beneficiaries                 List beneficiaries
GET    /multi/beneficiaries/{id}            Get beneficiary
DELETE /multi/beneficiaries/{id}            Delete beneficiary
```

## Common Request Bodies

### Create Corporate
```json
{
  "rootUser": {
    "name": "string",
    "surname": "string",
    "email": "string",
    "mobile": { "countryCode": "+44", "number": "7700900123" },
    "companyPosition": "DIRECTOR",
    "dateOfBirth": { "year": 1985, "month": 6, "day": 15 }
  },
  "company": {
    "type": "LLC",
    "name": "Acme Ltd",
    "registrationNumber": "12345678",
    "registrationCountry": "GB",
    "businessAddress": {
      "addressLine1": "123 High St",
      "city": "London",
      "postCode": "EC1A 1BB",
      "country": "GB"
    }
  },
  "baseCurrency": "GBP"
}
```

### Create Consumer
```json
{
  "rootUser": {
    "name": "string",
    "surname": "string",
    "email": "string",
    "mobile": { "countryCode": "+44", "number": "7700900123" },
    "dateOfBirth": { "year": 1990, "month": 3, "day": 20 },
    "address": {
      "addressLine1": "123 High St",
      "city": "London",
      "postCode": "EC1A 1BB",
      "country": "GB"
    }
  },
  "baseCurrency": "GBP"
}
```

### Create Managed Account
```json
{
  "profileId": "string",
  "friendlyName": "Main Account",
  "currency": "GBP"
}
```

### Create Managed Card
```json
{
  "profileId": "string",
  "friendlyName": "My Card",
  "currency": "GBP",
  "cardholderMobileNumber": { "countryCode": "+44", "number": "7700900123" },
  "billingAddress": {
    "addressLine1": "123 High St",
    "city": "London",
    "postCode": "EC1A 1BB",
    "country": "GB"
  }
}
```

### Create Transfer
```json
{
  "profileId": "string",
  "source": { "type": "managed_accounts", "id": "source_id" },
  "destination": { "type": "managed_accounts", "id": "dest_id" },
  "destinationAmount": { "currency": "GBP", "amount": 1000 }
}
```

## Enums

### Company Types
- `LLC`, `SOLE_TRADER`, `PUBLIC_LIMITED_COMPANY`, `PRIVATE_LIMITED_COMPANY`, `PARTNERSHIP`

### Company Positions
- `DIRECTOR`, `SHAREHOLDER`, `AUTHORISED_REPRESENTATIVE`, `ULTIMATE_BENEFICIAL_OWNER`

### KYC/KYB States
- `NOT_STARTED`, `PENDING_REVIEW`, `APPROVED`, `REJECTED`

### Card States
- `ACTIVE`, `INACTIVE`, `BLOCKED`, `DESTROYED`

### Transaction States
- `PENDING`, `COMPLETED`, `REJECTED`, `FAILED`

## Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - validation error |
| 401 | Unauthorized - invalid/missing auth |
| 403 | Forbidden - insufficient permissions |
| 404 | Not Found |
| 409 | Conflict - duplicate resource |
| 429 | Rate Limited |
