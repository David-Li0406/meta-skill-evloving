---
name: weavr-api
description: Use when making Weavr API calls for corporates, consumers, cards, accounts, transfers, or KYC/KYB.
---

# Weavr Multi API

API Reference: [Weavr Multi API](https://weavr-multi-api.redoc.ly/)

## Quick Start

```typescript
// Create a Corporate - POST /multi/corporates
// Headers: api-key, programme-key, Content-Type: application/json
{
  "rootUser": { "name": "<name>", "surname": "<surname>", "email": "<email>",
    "mobile": { "countryCode": "<countryCode>", "number": "<number>" },
    "companyPosition": "<position>", "dateOfBirth": { "year": <year>, "month": <month>, "day": <day> }
  },
  "company": { "type": "<companyType>", "name": "<companyName>", "registrationNumber": "<registrationNumber>",
    "registrationCountry": "<registrationCountry>", "businessAddress": { "addressLine1": "<addressLine1>",
    "city": "<city>", "postCode": "<postCode>", "country": "<country>" }
  },
  "baseCurrency": "<currency>"
}
```

## Core Endpoints

- **Identity**: `/multi/corporates`, `/multi/consumers`, `/{id}/kyb/start`, `/{id}/kyc/start`
- **Auth**: `/multi/login_with_password`, `/multi/authentication/step-up`
- **Instruments**: `/multi/managed_accounts`, `/multi/managed_cards`
- **Transfers**: `/multi/transfers`, `/multi/sends`, `/multi/outgoing_wire_transfers`

## Authentication

Headers: `api-key` (server), `programme-key` (programme), `Authorization: Bearer` (user)

## Reference Files

See [references/endpoints.md](references/endpoints.md) for full endpoint details.