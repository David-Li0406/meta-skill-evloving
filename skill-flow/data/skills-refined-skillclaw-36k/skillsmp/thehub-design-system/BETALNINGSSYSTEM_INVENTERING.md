# TheHUB Betalningssystem - Inventeringsrapport

**Datum:** 2026-01-12
**Projektversion:** v1.0
**Utfört av:** Claude (Inventering, ingen kod skriven)

---

## 1. PLANERAT SYSTEM (fran ROADMAP-2025.md)

Enligt ROADMAP-2025.md finns foljande planerat under "BETALNINGS- & ANMALNINGSSYSTEM":

### Planerade integrations:
- [x] **Manuell Swish** - Visa Swish-nummer, admin markerar betalda (markerad som Klar)
- [ ] **Swish Handel** - QR-kod, automatisk callback (Planerad)
- [ ] **Multi-forening** - Varje klubb eget certifikat (Planerad)
- [ ] **Stripe Connect** - Platform-modell med Connected Accounts (Planerad)
- [ ] **Apple Pay / Google Pay** - Via Stripe (Planerad)
- [ ] **Klarna** - Planerad men ej implementerad

### Planerade features fran FAS 4 "E-HANDEL & BETALNINGAR":
- [ ] Varukorg i TheHUB
- [ ] Prismatris per klass/alder/licenstyp
- [ ] Early bird / Late fee
- [ ] Familjeanmalan
- [ ] Biljettforsaljning
- [ ] Marknadsplats (begagnad utrustning)

### Check-in & Startnummersystem:
- [ ] QR-kod pa biljett (email + "Min Sida")
- [ ] Scanner-app for incheckad
- [ ] Automatisk startnummer-tilldelning baserat pa ranking

---

## 2. VAD SOM FINNS I KODEN

### A. PHP-filer (betalningsrelaterade)

#### Admin-filer:

| Fil | Rader | Senast andrad | Vad den gor |
|-----|-------|---------------|-------------|
| `admin/payment-settings.php` | 510 | 2026-01-12 | Konfigurerar Swish-nummer for events/serier/promotorar |
| `admin/payment-recipients.php` | 468 | 2026-01-12 | Hantera centrala betalningsmottagare (nyare system) |
| `admin/orders.php` | 421 | 2026-01-12 | Lista ordrar, filtrera, manuellt bekrafta betalningar |
| `admin/event-payment.php` | 1270 | 2026-01-12 | Economy-tab for event - prissattning per klass, Swish-config |
| `admin/event-orders.php` | 383 | 2026-01-12 | Ordrar for ett specifikt event |
| `admin/event-registrations.php` | 316 | 2026-01-12 | Hantera anmalningar till event |
| `admin/event-tickets.php` | 337 | 2026-01-12 | Biljetthantering for event |
| `admin/event-ticketing.php` | 17 | 2026-01-12 | Redirect-fil (minimal) |
| `admin/ticketing.php` | 123 | 2026-01-12 | Biljettoversikt |
| `admin/swish-accounts.php` | - | 2026-01-12 | Hantera Swish-konton (refereras i kod) |
| `admin/promotor-payments.php` | 959 | 2026-01-12 | Promotor-specifika betalningar |
| `admin/promotor-registrations.php` | 698 | 2026-01-12 | Promotor-specifika anmalningar |
| `admin/registration-rules.php` | 254 | 2026-01-12 | Regler for anmalning |
| `admin/series-registrations.php` | 532 | 2026-01-12 | Serie-pass anmalningar |
| `admin/onsite-registration.php` | 117 | 2026-01-12 | On-site registrering (på plats) |

#### Includes-filer (Backend logic):

| Fil | Rader | Vad den gor |
|-----|-------|-------------|
| `includes/payment.php` | 1043 | **HUVUDFIL** - Order CRUD, Swish-lankar, QR-koder, rabattkoder |
| `includes/order-manager.php` | 668 | Multi-rider ordrar (en kopare, flera deltagare) |
| `includes/payment/PaymentManager.php` | 420 | Gateway-orkestrering, initiate/check/refund |
| `includes/payment/GatewayInterface.php` | 91 | Interface for alla gateways |
| `includes/payment/SwishClient.php` | 285 | Swish Commerce API-klient (certifikat) |
| `includes/payment/StripeClient.php` | 305 | Stripe API-klient |
| `includes/payment/gateways/SwishGateway.php` | 220 | Swish Handel gateway-implementation |
| `includes/payment/gateways/StripeGateway.php` | 221 | Stripe Connect gateway-implementation |
| `includes/payment/gateways/ManualGateway.php` | 212 | Manuell Swish (deep-link + QR for bekraftelse) |
| `includes/registration-rules.php` | 523 | Valideringsregler for anmalan |
| `includes/registration-validator.php` | 497 | Validerar anmalningar |
| `includes/series-registration.php` | 652 | Serie-pass registrering |

#### Pages-filer (Frontend):

| Fil | Rader | Vad den gor |
|-----|-------|-------------|
| `pages/checkout.php` | 524 | **CHECKOUT-SIDA** - Visar Swish-knapp/QR, rabattkod-input |
| `pages/profile/tickets.php` | 502 | "Mina biljetter" - visa kopare's biljetter |
| `pages/profile/registrations.php` | 141 | "Mina anmalningar" |
| `pages/profile/receipts.php` | 94 | Kvitton |
| `my-tickets.php` | - | Rotfil for biljetter (redirect?) |

#### API-filer:

| Fil | Rader | Vad den gor |
|-----|-------|-------------|
| `api/orders.php` | 235 | Order API (skapa, hamta) |
| `api/registration.php` | 305 | Event-anmalan API |
| `api/series-registration.php` | 442 | Serie-anmalan API |
| `api/validate-registration.php` | 140 | Validera anmalan |
| `api/apply-discount.php` | 86 | Tillamp rabattkod pa order |
| `api/validate-discount.php` | 61 | Validera rabattkod |
| `api/webhooks/swish-callback.php` | 242 | **WEBHOOK** - Tar emot Swish Handel callbacks |
| `api/webhooks/stripe-webhook.php` | 268 | **WEBHOOK** - Tar emot Stripe webhooks |

---

### B. Databastabeller

Baserat pa migrationsfiler finns foljande tabeller:

| Tabell | Skapad av | Kolumner (urval) | Status |
|--------|-----------|------------------|--------|
| `orders` | 048_payment_system.sql | id, order_number, rider_id, customer_email, customer_name, event_id, subtotal, discount, total_amount, payment_method, payment_status, swish_number, swish_message, paid_at | **FINNS** |
| `order_items` | 048_payment_system.sql | id, order_id, item_type, registration_id, description, unit_price, quantity, total_price | **FINNS** |
| `payment_configs` | 048_payment_system.sql | id, event_id, series_id, club_id, promotor_user_id, swish_enabled, swish_number, swish_name | **LEGACY** |
| `payment_recipients` | 054_payment_recipients_central.sql | id, name, swish_number, swish_name, gateway_type, gateway_config, gateway_enabled, stripe_account_id, stripe_account_status | **FINNS** (nyare) |
| `payment_transactions` | 099_multi_gateway_system.sql | id, order_id, gateway_code, transaction_type, request_data, response_data, status | **FINNS** |
| `gateway_certificates` | 099_multi_gateway_system.sql | id, payment_recipient_id, cert_type, cert_data, cert_password | **FINNS** |
| `webhook_logs` | 099_multi_gateway_system.sql | id, gateway_code, webhook_type, payload, headers, processed, order_id | **FINNS** |
| `event_registrations` | create_registrations_table.sql | id, event_id, rider_id, first_name, last_name, email, category, status, payment_status, order_id | **FINNS** |
| `series_registrations` | 110_series_registrations_system.php | id, series_id, rider_id, class_id, status, payment_status, order_id | **FINNS** |
| `pricing_templates` | 101_pricing_templates_system.sql | id, name, early_bird_percent, early_bird_days_before, late_fee_percent | **FINNS** |
| `pricing_template_rules` | 101_pricing_templates_system.sql | id, template_id, class_id, base_price | **FINNS** |
| `event_pricing_rules` | 101_pricing_templates_system.sql | id, event_id, class_id, base_price, early_bird_discount_percent | **FINNS** |
| `discount_codes` | Okand migration | id, code, discount_type, discount_value, max_uses, valid_from, valid_until | **OKANT** |
| `discount_code_usage` | Okand migration | id, discount_code_id, order_id, rider_id, discount_amount | **OKANT** |

---

### C. Identifierade integrations

#### Swish:

**Manuell Swish (ManualGateway):**
- Konfigfiler: `includes/payment/gateways/ManualGateway.php`
- Funktion: Genererar Swish deep-link (`https://app.swish.nu/1/p/sw/`) och QR-kod
- Admin bekraftar manuellt att betalning kommit
- **Status: FUNGERANDE** - Detta ar det som anvands idag

**Swish Handel (SwishGateway):**
- Konfigfiler: `includes/payment/gateways/SwishGateway.php`, `includes/payment/SwishClient.php`
- Certifikathantering: `gateway_certificates` tabell
- API-URL: `https://mss.cpc.getswish.net/swish-cpcapi/api/v2` (test) / `https://cpc.getswish.net/swish-cpcapi/api/v2` (prod)
- Webhook: `api/webhooks/swish-callback.php`
- **Status: IMPLEMENTERAT MEN EJ AKTIVERAT** - Saknar certifikat

#### Stripe:

- Konfigfiler: `includes/payment/gateways/StripeGateway.php`, `includes/payment/StripeClient.php`
- Environment: `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`
- Stodjer: Payment Intents, Connected Accounts, Refunds
- Webhook: `api/webhooks/stripe-webhook.php`
- **Status: IMPLEMENTERAT MEN EJ AKTIVERAT** - Saknar API-nycklar

#### Klarna:
- **Status: EJ IMPLEMENTERAD** - Namns i roadmap men ingen kod finns

---

## 3. IDENTIFIERADE PROBLEM

### A. Duplicerad kod:

1. **Tva order-system**:
   - `includes/payment.php` (createOrder, generateOrderNumber)
   - `includes/order-manager.php` (createMultiRiderOrder, generateOrderReference)
   - Dessa anvander olika format: `ORD-YYYY-NNNNNN` vs `A5F2J0112`

2. **Tva payment config-system**:
   - Legacy: `payment_configs` tabell (event/series/promotor-specifik)
   - Nyare: `payment_recipients` tabell (centrala mottagare)
   - `includes/payment.php` kollar bada med fallback-logik

3. **QR-kod generering** finns pa tva stallen:
   - `includes/payment.php` - `generateSwishQR()`
   - `includes/payment/gateways/ManualGateway.php` - `generateSwishQR()`

### B. Konflikter:

1. **Order-tabellen** skapas pa tva stallen med olika kolumner:
   - `database/migrations/_archive/048_payment_system.sql` (fullstandig)
   - `admin/event-payment.php` (enklare, skapas vid behov)

2. **Payment recipient logik**:
   - `getPaymentConfig()` i `includes/payment.php` har 7 fallback-steg
   - Prioritet: event_recipient > series_recipient > event_config > series_config > promotor_config > promotor_direct > WooCommerce
   - Detta kan vara forvirrande for administratorer

### C. Ofullstandigt:

1. **Email-bekraftelser** - Namns i checkout.php men ingen faktisk email-kod hittas
2. **QR-kod for check-in** - Finns i roadmap men ej implementerad
3. **Familjeanmalan** - order-manager.php har multi-rider-stod men ingen UI for det
4. **Early bird/Late fee** - Tabeller finns men prissattningslogik saknas i createOrder()
5. **WooCommerce-fallback** - Refereras i kod men ingen WooCommerce-integration finns

### D. Potentiellt trasigt:

1. **Swish Handel callback** (`api/webhooks/swish-callback.php`):
   - Anvander `$GLOBALS['pdo']` istallet for `hub_db()`
   - Kan krascha om fel databas-wrapper anvands

2. **Stripe webhook** (`api/webhooks/stripe-webhook.php`):
   - Samma problem med `$GLOBALS['pdo']`

3. **Rabattkods-tabeller** - Refereras i kod men ingen migration hittas:
   - `discount_codes`
   - `discount_code_usage`
   - Kan orsaka fel om tabellerna inte existerar

---

## 4. VAD SOM SAKNAS

Jamfort med roadmap, vad saknas helt:

- [x] Manuell Swish (fungerar)
- [ ] **Swish Handel aktivering** (certifikat saknas)
- [ ] **Stripe aktivering** (API-nycklar saknas)
- [ ] **Email-bekraftelser vid betalning**
- [ ] **QR-kod-biljetter for check-in**
- [ ] **Check-in app/sida**
- [ ] **Automatisk startnummer-tilldelning**
- [ ] **Varukorg (shopping cart)** - En order = en registrering idag
- [ ] **Early bird pris-berakning** (tabeller finns, logik saknas)
- [ ] **Late fee pris-berakning** (tabeller finns, logik saknas)
- [ ] **Klarna-integration**
- [ ] **Marknadsplats**

---

## 5. REKOMMENDERAD VAG FRAMAT

Baserat pa inventeringen, foreslars:

### Alternativ A: Fortsatt pa befintlig kodbas (REKOMMENDERAS)

**Valj om:** Det mesta fungerar, behover bara aktiveras och poleras.

**Bedomning:** Systemet ar val strukturerat med:
- Gateway-abstraktion (interface + tre implementationer)
- Webhook-hantering
- Order + OrderItems-struktur
- Payment recipients-system
- Registreringsflode

**Arbete:** Ca 40-60 timmars fokuserat arbete

**Prioriterade atgarder:**
1. Rensa upp databas-wrappers (`$GLOBALS['pdo']` -> `hub_db()`)
2. Skapa/verifiera att alla tabeller existerar (discount_codes mm)
3. Aktivera Manuell Swish for alla events (redan fungerande)
4. Koppla email-notifieringar
5. Skapa enkel check-in-sida

---

## 6. KONKRET 3-VECKORS PLAN

For att salja biljetter inom 3 veckor:

### Vecka 1: Stabilisering

- [ ] Verifiera att alla databastabeller existerar
- [ ] Fixa `$GLOBALS['pdo']` -> `hub_db()` i webhooks
- [ ] Satt upp Manuell Swish for ett test-event
- [ ] Testa hela flodet: anmalan -> order -> checkout -> manuell bekraftelse
- [ ] Identifiera och fixa eventuella buggar

### Vecka 2: Email & UX

- [ ] Implementera email vid bekraftad betalning (PHPMailer eller liknande)
- [ ] Forbattra checkout-sidan (tydligare instruktioner)
- [ ] Skapa "Mina biljetter"-sida med QR-kod
- [ ] Skapa admin-sida for att se alla betalda anmalningar

### Vecka 3: Test & Lansering

- [ ] Fullstandig test med riktiga anvandare (pilot-event)
- [ ] Skapa dokumentation for administratorer
- [ ] Konfigurera production-Swish-nummer
- [ ] Lansera for ett eller tva events

---

## 7. KRITISKA FRAGOR TILL JALLE

Innan arbete kan borja behover foljande besvaras:

1. **Vilken betalmetod ska prioriteras?**
   - Manuell Swish (redan fungerar, admin bekraftar)
   - Swish Handel (krav: Swish Commerce-avtal + certifikat)
   - Stripe (krav: Stripe-konto + API-nycklar)

2. **Finns Swish Commerce-certifikat?**
   - Om ja: Swish Handel kan aktiveras
   - Om nej: Manuell Swish anvands tillfrlligt

3. **Finns Stripe-konto?**
   - Om ja: Kortbetalning kan aktiveras
   - Om nej: Manuell Swish ar enda alternativet

4. **Ska check-in/QR-kod finnas fran start?**
   - Kan prioriteras bort i forsta versionen
   - Enkel lista med namn racker initialt

5. **Vilka events ska lanseras forst?**
   - Forslag: Borja med ett event som test
   - Skala upp efter feedback

6. **Email-leverantor?**
   - Anvands WordPress-email idag?
   - SMTP-server tillganglig?
   - Eller tredje-part (SendGrid, Mailgun)?

7. **Vem ar "betalningsmottagare" for varje serie?**
   - GravitySeries centralt?
   - Arrangorsklubben?
   - Behover konfigureras per event/serie

8. **Behover flera priser per klass?**
   - Early bird
   - Ordinarie
   - Late fee
   - Licenserad vs olicienserad?

---

## 8. SAMMANFATTNING

### Vad som fungerar:
- Orderstruktur (orders + order_items)
- Manuell Swish (deep-link + QR + manuell bekraftelse)
- Gateway-arkitektur (for framtida Swish Handel / Stripe)
- Event-registrering
- Serie-pass registrering
- Admin-orderlista med bekraftelse

### Vad som behover fixas:
- Webhooks (databas-wrapper)
- Email-notifieringar (saknas helt)
- Pris-berakning (early bird / late fee)
- Check-in-sida

### Vad som saknas helt:
- Aktiverade betalnings-gateways (certifikat/nycklar)
- QR-biljetter for check-in
- Varukorg for flera items

### Bedomning:
Koden ar **val strukturerad** och redo for produktion efter mindre fixar. Rekommenderar att borja med Manuell Swish (redan fungerande) och lagga till automatiserade gateways senare.

---

**END OF RAPPORT**

*Skapad 2026-01-12 av Claude (Inventering)*
