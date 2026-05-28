---
name: zoop-integration
description: Official guidelines and API reference for integrating with Zoop (Fintech as a Service).
---

# Zoop Integration Skill

This skill provides the **authoritative and exhaustive** reference for implementing Zoop features in `portal-outbank`.
It combines the full API mapping with critical security and implementation guidelines for this project.

## 1. Authentication & Base Config (Project Standards)
*   **Base URL:** `https://api.zoop.ws` (Production) / `https://api.zoop.ws` (Sandbox usually handled via keys)
*   **Auth Header (Frontend):** `Authorization: Basic base64(PUBLISHABLE_KEY)` (`zpk_...`)
*   **Auth Header (Backend):** `Authorization: Basic base64(MARKETPLACE_ID)` or `zmk_...` depending on operation depth.
*   **Marketplace ID:** Essential path parameter for all routes: `/v1/marketplaces/{marketplace_id}/...`

## 2. Implementation Guidelines (CRITICAL)

1.  **Server-Side Only:**
    *   SENSITIVE operations must *never* be called from the Frontend.
    *   **Must be Server Actions/API Routes:** Split Rules, Prepayment, Transfers, Banking, Auth Challenges.
    *   **Safe for Frontend:** Tokenization (Card/Bank Account).

2.  **Idempotency:**
    *   **Always** send the `idempotency-key` header in POST requests to prevent double charges.

3.  **Webhooks:**
    *   Endpoint: `/api/webhooks/zoop`
    *   Listen for: `transaction.succeeded`, `seller.activated`, `subscription.paid`.

4.  **2FA Flow:**
    *   Banking operations (transfers, payments) **MUST** confirm an SMS or TOTP challenge via the `/v1/api/company/...` endpoints before execution.

---

## 3. Exhaustive API Reference (Master Guide)

### 3.1. Cadastro e Credenciamento (Onboarding)
*   **POST** `/v1/marketplaces/{id}/sellers/individuals` (PF)
    *   Required: `first_name`, `last_name`, `taxpayer_id` (CPF), `birthdate`, `email`.
*   **POST** `/v1/marketplaces/{id}/sellers/businesses` (PJ)
    *   Required: `business_name`, `business_taxpayer_id` (CNPJ), `mcc`, `owner` (PF object).
*   **GET** `/v1/marketplaces/{id}/sellers` (List)
*   **GET** `/v1/marketplaces/{id}/sellers/{seller_id}` (Details)
*   **DELETE** `/v1/marketplaces/{id}/sellers/{seller_id}` (Archive)

### 3.2. Dados Bancários e Cartões (Wallet)
*   **POST** `/v1/marketplaces/{id}/bank_accounts/tokens` (Tokenize Account)
*   **POST** `/v1/marketplaces/{id}/bank_accounts` (Link Account)
*   **POST** `/v1/marketplaces/{id}/cards/tokens` (Tokenize Card - PCI Safe)
*   **POST** `/v1/marketplaces/{id}/cards` (Save Card to Customer)

### 3.3. Adquirência e Transações (Payments)
*   **POST** `/v1/marketplaces/{id}/transactions`
    *   **Credit:** `amount`, `currency`, `payment_type: "credit"`, `on_behalf_of`, `source` (token).
    *   **Pix:** `payment_type: "pix"`, `amount`, `on_behalf_of`.
    *   **Boleto:** `payment_type: "boleto"`, `amount`, `customer`.
*   **POST** `/v1/marketplaces/{id}/transactions/{transaction_id}/capture`
*   **POST** `/v1/marketplaces/{id}/transactions/{transaction_id}/void` (Full or Partial Refund)

### 3.4. Regras de Divisão (Split Rules)
*   **POST** `/v1/marketplaces/{id}/transactions/{transaction_id}/split_rules`
    *   Required: `recipient`, `liable` (bool), `percentage` OR `amount`.

### 3.5. Recorrência (Assinaturas)
*   **POST** `/v1/marketplaces/{id}/recurrence/plans`
    *   Required: `name`, `amount`, `interval` (day/month/year).
*   **POST** `/v1/marketplaces/{id}/recurrence/subscriptions`
    *   Required: `plan_id`, `customer_id`, `payment_method`.
*   **POST** `/v1/marketplaces/{id}/invoices` (Avulsa)

### 3.6. Banking & Transferências
*   **GET** `/v1/marketplaces/{id}/sellers/{seller_id}/balances`
*   **POST** `/v1/marketplaces/{id}/transfers` (TED/DOC External)
    *   Required: `amount`, `bank_account_id`.
*   **POST** `/v1/marketplaces/{id}/transfers/owner_to_receiver` (P2P Internal)
    *   Required: `amount`, `target_seller_id`.

### 3.7. Antecipação (Prepayment)
*   **POST** `/v1/marketplaces/{id}/prepayments` (Request Advance)
*   **GET** `/v1/marketplaces/{id}/sellers/{seller_id}/prepayments/simulation` (Simulate Cost)

### 3.8. Pix Keys (Dict)
*   **POST** `/v1/marketplaces/{id}/dict/keys` (Create)
*   **POST** `/v1/marketplaces/{id}/dict/keys/{key}/ownership` (Challenge)
*   **POST** `/v1/marketplaces/{id}/dict/keys/{key}/ownership/verify` (Activate)

### 3.9. Hardware (POS) & Tap to Pay
*   **POST** `/v1/marketplaces/{id}/terminals/pairing`
*   **Tap to Pay:** Transactions appear in standard list with `capture_method: "contactless_mobile"`.

---

## 4. Advanced Authentication & 2FA (Security)
*   **Login:** `POST /v1/api/company/login`
*   **SMS Challenge:** `POST /v1/api/company/sms/session`
*   **TOTP Challenge:** `POST /v1/api/company/totp/session`
*   **Validation:** All banking actions should verify the session token from these challenges.

## 5. References
*   [Zoop Docs Home](https://docs.zoop.co/)
