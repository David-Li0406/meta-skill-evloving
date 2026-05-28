# TheHUB - Development Roadmap

> Senast uppdaterad: 2026-01-23
>
> **Se:** `/admin/roadmap.php` for interaktiv vy

---

## PROJEKTOMRADEN

| Omrade | Status | Beskrivning | Progress |
|--------|--------|-------------|----------|
| Analytics Platform | KLAR | Statistik, KPI:er, trender, rapporter | 100% |
| Betalningssystem | 80% KLAR | Swish, Stripe, ordrar, checkout | 80% |
| Event Ratings | KLAR | Deltagarfeedback pa events | 100% |
| Win-Back System | KLAR | Aterengagera churnade deltagare | 100% |
| Klubb RF-Registrering | KLAR | SCF/NCF/DCU-synk och stavningskontroll | 100% |
| Bildbanken | PAGAENDE | AI-analyserade bilder kopplade till profiler | 10% |
| Ridercard Share | PAGAENDE | Statistikkort for Instagram-delning | 5% |

---

# PAGAENDE PROJEKT

## Bildbanken

**Mal:** AI-analyserade bilder kopplade till anvandarprofiler
**Status:** PAGAENDE (10%)
**Startad:** 2026-01

### Koncept

Bildbank dar bilder fran tavlingar automatiskt kopplas till ratt deltagare via:
- Manuell taggning av anvandare
- Automatisk identifiering via nummerplattar (AI/OCR)
- Ansiktsigenkanning (framtida mojlighet)

### Teknisk losning

- **Lagring:** Google Foto (tillfallig losning)
- **Framtida:** Egen lagring eller CDN (Cloudflare R2, AWS S3)
- **AI:** Google Vision API eller liknande for nummerplattsigenkanning

### Steg

- [ ] Definiera databasschema for bildmetadata
- [ ] Skapa admin-granssnitt for bilduppladdning
- [ ] Implementera manuell taggning av bilder
- [ ] Google Foto-integration (lasa bilder)
- [ ] AI/OCR for nummerplattsigenkanning
- [ ] Visa bilder pa anvandarprofiler
- [ ] Galleri-vy per event
- [ ] Sokfunktion for bilder

### Databastabeller (planerade)

```sql
image_library         -- Bildmetadata (url, event_id, photographer)
image_tags            -- Koppling bild <-> rider (rider_id, confidence)
image_bib_detections  -- AI-detekterade nummerplattar
```

---

## Ridercard Share

**Mal:** Generera snygga statistikkort som kan delas pa Instagram
**Status:** PAGAENDE (5%)
**Startad:** 2026-01

### Koncept

Automatiskt genererade "trading cards" med deltagarstatistik:
- Profilbild eller silhuett
- Namn, klubb, alder
- Statistik: starter, segrar, podiums, poang
- Serie-badges
- QR-kod till profil

### Teknisk losning

- **Rendering:** Server-side med PHP GD eller Imagick
- **Alternativ:** HTML-to-image via Puppeteer
- **Format:** 1080x1920 (Instagram Stories), 1080x1080 (Feed)

### Steg

- [ ] Designa kortmall (Figma/sketch)
- [ ] Implementera PHP-baserad bildgenerering
- [ ] Skapa API-endpoint for kortgenerering
- [ ] Lagg till "Dela"-knapp pa profil
- [ ] Stod for olika mallar/teman
- [ ] Sasongskort med hogtryckssiffror
- [ ] Event-specifika kort

### Exempel-data

```json
{
  "rider_name": "Erik Andersson",
  "club": "Lidingo SK",
  "age": 28,
  "stats": {
    "starts": 42,
    "wins": 3,
    "podiums": 12,
    "points": 1847
  },
  "series": ["GES", "GGS"],
  "profile_url": "thehub.gravityseries.se/rider/123"
}
```

---

# AVSLUTADE PROJEKT

## DEL 1: Analytics Platform

**Status:** KLAR (100%)

16 steg implementerade:
- [x] Governance & Identity Foundation
- [x] Databas & Analytics-tabeller
- [x] Analytics Engine
- [x] KPI Dashboard
- [x] Serieflodeanalys
- [x] Rapportgenerator (6 typer)
- [x] Publika Insikter (GDPR)
- [x] Automatisering & Cron
- [x] Admin-verktyg
- [x] Rookie-analys
- [x] Retention & Churn
- [x] Avancerade moduler (Cohort, At-Risk, Geography)
- [x] Production Readiness
- [x] First Season Journey
- [x] Longitudinal Journey
- [x] Event Participation

### Huvudfiler

- `admin/analytics-dashboard.php` - KPI-oversikt
- `admin/analytics-trends.php` - Historiska trender
- `admin/analytics-cohorts.php` - Kohortanalys
- `admin/analytics-atrisk.php` - Riskprediktion
- `admin/analytics-geography.php` - Regional statistik
- `analytics/includes/KPICalculator.php` - 100+ KPI-metoder

---

## DEL 2: Betalningssystem

**Status:** 80% KLAR

### Fungerar

- [x] Order CRUD och multi-rider ordrar
- [x] Manuell Swish (QR + deeplink)
- [x] Gateway-arkitektur (interface + PaymentManager)
- [x] Checkout-flode
- [x] Mina biljetter/anmalningar

### Aterstar

- [ ] Fixa webhook databas-wrapper
- [ ] Email-bekraftelser (PHPMailer)
- [ ] Rabattkoder (discount_codes-tabeller)
- [ ] Swish Handel (certifikat)
- [ ] Stripe Connect (API-nycklar)

### Huvudfiler

- `includes/payment.php` - Order CRUD
- `gateways/ManualGateway.php` - Manuell Swish
- `pages/checkout.php` - Checkout UI

---

## DEL 3: Event Ratings

**Status:** KLAR (100%)

- [x] 10 standardfragor + overgripande betyg
- [x] Anonym feedback
- [x] Tidsfonstrer (30 dagar efter event)
- [x] Profil-integration
- [x] Admin-rapport med aggregerade betyg

### Huvudfiler

- `pages/profile/event-ratings.php` - Betygsformular
- `admin/analytics-event-ratings.php` - Rapport

---

## DEL 4: Win-Back System

**Status:** KLAR (100%)

- [x] Identifiera churnade deltagare
- [x] Kampanjhantering med varumarkesfilter
- [x] Enkatsystem (flerval, skala, fritext)
- [x] Automatisk rabattkod vid avslutat
- [x] Email-inbjudningar
- [x] Promotor access control
- [x] Win-Back Analytics

### Huvudfiler

- `admin/winback-campaigns.php` - Kampanjhantering
- `admin/winback-analytics.php` - Dataanalys
- `pages/profile/winback-survey.php` - Enkat

---

## DEL 5: Klubb RF-Registrering

**Status:** KLAR (100%)

- [x] 400+ SCF-klubbar
- [x] 385 NCF-klubbar (Norge)
- [x] 290 DCU-klubbar (Danmark)
- [x] Automatisk matchning
- [x] Stavningskontroll mot register
- [x] RF-badges pa profiler

### Huvudfiler

- `admin/club-rf-registration.php` - Synkverktyg
- `admin/club-rf-spelling.php` - Stavningskontroll

---

# TEKNISKA BESLUT

### Databas
- `results` + `events` ar source of truth
- `rider_merge_map` hanterar dubbletter
- Pre-beraknad statistik i `rider_yearly_stats`

### GDPR
- Publika insikter visar EJ segment < 10 deltagare
- Export-loggning med `analytics_exports`

### Betalning
- PaymentManager + GatewayInterface-arkitektur
- Manuell Swish forst, Swish Handel/Stripe senare

### Visualisering
- Chart.js for grafer
- SVGChartRenderer for PDF-export

---

# CHANGELOG

### 2026-01-23 (Klassanalys & Events)
- **Branch: claude/participant-analysis-tool-v8luL**

- **Forbattrad klassanalys**
  - Anvander display_name fran classes-tabellen
  - Sorterar klasser enligt sort_order (samma som classes.php)
  - Flyttat klasser-lank fran Konfiguration till Tavlingar

- **Events admin forbattringar**
  - Fixat venue_id i update-event-field.php
  - Fixat event_format validation i bulk-update-events.php
  - Lagt till point_scale_id och venue_id i bulk-update
  - Lagt till e.venue_id i SQL SELECT
  - Andrat platshistorik till att anvanda venues-tabellen

### 2026-01-22 (Roadmap Forbattring)
- **Branch: claude/participant-analysis-tool-v8luL**

- **Forbattrad roadmap-struktur**
  - Omorganiserad ROADMAP.md for battre lasbarhet
  - Lagt till progress-procent per projekt
  - Klickbara projektområden i roadmap.php

- **Nya projekt tillagda:**
  - Bildbanken - AI-analyserade bilder
  - Ridercard Share - Statistikkort for Instagram

### 2026-01-21 (Win-Back Survey System)
- **Branch: claude/participant-analysis-tool-v8luL**

- **Ny funktion: Win-Back Survey System**
  - Identifiering av churnade deltagare
  - Kampanjhantering med varumarkesfilter
  - Enkatsystem med fragor
  - Automatisk rabattkod
  - Email-inbjudningar
  - Svarsstatistik

- **Bugfixar:**
  - Fixat brand-tabell (series_brands istallet for brands)
  - Fixat databasanslutning (KPICalculator)
  - Mobilanpassning edge-to-edge

### 2026-01-19 (PHP 7 Kompatibilitet)
- **Branch: claude/add-event-ratings-dj5ED**

- **KRITISK FIX: PHP 7 Kompatibilitet**
  - Ersatte match() (PHP 8.0+) med array lookups
  - Ersatte arrow functions fn() med traditional functions

### 2026-01-18 (Event Ratings System)
- **Ny funktion: Event Ratings**
  - Deltagare kan betygsatta events
  - 10 standardfragor + overgripande betyg
  - Anonym feedback

### 2026-01-16 (Analytics v3.2)
- **Steg 16 KLAR: Event Participation Analysis**
- **Unified Migration Tool**
- **Nya KPICalculator-metoder**

### 2026-01-14 (Analytics Phase 2)
- **Steg 11 KLAR: Avancerade moduler**
  - Cohort Analysis
  - At-Risk Prediction
  - Geographic Analysis
  - Feeder Trends

### 2026-01-13
- **Analytics Platform startat**
- **Steg 0-7 KLAR pa en dag**

---

**ANALYTICS PLATFORM KOMPLETT!**
**BETALNINGSSYSTEM REDO FOR LANSERING**
