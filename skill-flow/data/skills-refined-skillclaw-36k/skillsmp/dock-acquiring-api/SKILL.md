---
name: dock-acquiring-api
description: Documentation and patterns for Dock Acquiring APIs (Onboarding, Transactions, Terminals).
---

# Dock Acquiring API Skill

This skill acts as a knowledge base and utility collection for integrating with Dock's Acquiring platform.

## 📚 Overview

The Dock Acquiring API allows you to manage the entire lifecycle of merchants, terminals, and transactions.
This skill is strictly for **Acquiring** endpoints.

## 🔒 Security & Authentication

### Token Types
1. **Integration Token**:
   - **Usage**: Onboarding, Terminals, and Initialization.
   - **Delivery**: Securely delivered via PGP (Pretty Good Privacy). You send your public key, Dock encrypts the token.
   - **Header**: `Authorization: Bearer <Integration_Token>`

2. **Transactional Token**:
   - **Usage**: All financial transactions (Sale, Void, Pre-auth, etc.).
   - **Generation**: Obtained via `/v1/initialization` endpoint.
   - **Validity**: **1 hour**. Must be refreshed periodically.
   - **Header**: `Authorization: Bearer <Transactional_Token>`

### Encryption
- **TLS**: All communication uses HTTPS with TLS.
- **PGP**: Used *only* for the initial delivery of the Integration Token. Request payloads do *not* need manual encryption unless specified (e.g., specific card data fields in legacy flows, though standard endpoints accept distinct PAN fields).

## 🛠️ Domains & Endpoints

### 1. Onboarding (Merchants)
Management of merchant accounts, commercial establishments (ECs), and affiliation data.

#### Create Merchant
- **URL**: `POST https://merchant.acquiring.hml.dock.tech/v1/onboarding`
- **Auth**: Integration Token
- **Key Params**: `documentId` (CPF/CNPJ), `mcc`, `address`, `responsiblePeople`, `merchantBankAccount`, `merchantConfiguration` (for CNP).
- **Flow**: Returns success (200) but KYC status starts as `WAITING_DOCUMENTS`.

#### Add Documents
- **URL**: `POST https://merchant.acquiring.hml.dock.tech/v1/merchants/{slugMerchant}/documents`
- **Content-Type**: `multipart/form-data`
- **Params**: `merchantDocumentList` containing `fileData`, `documentTypeSlug`, `file`.
- **Note**: Mandatory documents must be uploaded within **4 business days** or KYC is auto-rejected.

#### Sign Merchant Term (Acceptance)
- **URL**: `PUT https://merchant.acquiring.hml.dock.tech/v1/term_acceptance/{slugTerm}`
- **Body**: `userSigned` (CPF/Email of the signer).
- **Critical**: Merchant cannot transact until this step is completed.

### 2. Terminals (POS)
Management of physical and virtual capture devices.

#### Initialization (Get Transaction Token)
- **Physical POS**: `POST https://merchant.acquiring.hml.dock.tech/v1/initialization`
- **Virtual (CNP)**: `POST https://gw-caradhras.acquiring.hml.dock.tech/v1/initialization/virtual`
- **Input**: `documentId` or `apiKey`.
- **Output**: Returns the **Transactional Token**.

### 3. Transactions (Gateway)
Real-time transaction processing. **Requires Transaction Token.**

#### Create Sale
- **URL**: `POST https://gw-postilion-ecommerce.acquiring.hml.dock.tech/v2/sale`
- **Body**: `amount`, `currency` (BRL), `installments`, `cardNumber`, `cardSecurityCode`, `cardExpirationDate` (Format: `MMyyyy`), `orderId`.
- **Note**: For tokenized cards, use `slugToken` instead of card details.

#### Pre-Authorization Flow
1. **Create**: `POST .../v2/pre-authorization` (Reserves limit).
2. **Confirm**: `POST .../v2/capture` (Captures the amount).
   - Body: `transactionId`, `amount` (can be partial).
3. **Cancel**: `POST .../v2/void` (Reverses the hold).

#### Cancel Transaction (Void)
- **URL**: `POST https://gw-postilion-ecommerce.acquiring.hml.dock.tech/v2/void`
- **Types**:
  - `PRE_AUTHORIZATION`: Releases reserved limit.
  - `SALE` / `CREDIT`: Refunds the transaction.
- **Rule**: If > 1 day, it triggers a `D+N Void` (Refund with `PENDING` cycle).

#### Card Inquiry (ABU / Zero Auth)
- **URL**: `POST https://gw-postilion-ecommerce.acquiring.hml.dock.tech/v2/card-inquiry`
- **Usage**: Verify card validity and get updates (Account Updater) without charging.

#### Fee Simulator
- **URL**: `POST https://gw-postilion-ecommerce.acquiring.hml.dock.tech/v2/fee-simulator`
- **Usage**: Calculate net amount or required gross amount before transaction. Returns `saleSimulatorToken` to be used in the actual sale.

### 4. Payment Links
- **Create**: `POST https://serviceorder.acquiring.hml.dock.tech/v1/external_payment_links`
- **Update**: `PUT .../{slug}` (Cannot update if already paid).

## 📡 Webhooks
Configure webhooks to avoid polling.

1. **Merchant Onboarding** (`merchant_onboarding_status`): Updates on KYC analysis (`PENDING` -> `APPROVED`/`DECLINED`).
2. **Transactions** (`financial_cycle`): **Primary source of truth** for transaction status (`AUTHORIZATION`, `REFUND`, `VOID`).
3. **Payout**: Notifications about settlement provisioning.

## ⚠️ Error Handling
- **400 Bad Request**: Malformed data (e.g., `INVALID_AMOUNT`, `MIN_INSTALLMENTS`).
- **401 Unauthorized**: Invalid/Expired token. **Action**: Refresh Transactional Token via Initialization.
- **422 Unprocessable**: Business rule violation (e.g., `cardExpired`, `insufficientFunds`).
- **5xx**: Internal error. **Action**: Retry with exponential backoff.

## 📝 Best Practices
1. **Token Rotation**: Automate calling `/initialization` every 50-55 mins.
2. **Async Processing**: Use webhooks for final status, especially for KYC and Payouts.
3. **Validation**: Validate `cardExpirationDate` format (`MMyyyy`) and numeric fields before sending.
