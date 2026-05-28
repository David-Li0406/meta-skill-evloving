---
name: photometrics-ai-financial
description: Financial model, value calculations, and verified numbers for Photometrics AI. Use when Ari needs help with ROI calculations, proposal budgets, value per light figures, utility cost avoidance, pricing, energy savings math, or any quantitative claims. Triggers on dollar amounts, per-light values, energy savings, market size, pilot pricing, or requests to verify/source a number.
---

# Photometrics AI Financials

**Purpose:** Single source of truth for all financial calculations, quantitative claims, and their derivations.

**Core principle:** Never state a number as fact unless it has verified logic and sources documented here.

---

## Quick Reference: Key Numbers

| Metric | Value | Status |
|--------|-------|--------|
| Municipal value | $51.09/light/year | 🔶 DERIVED |
| Utility cost avoidance | $10.18/light/year | ✅ VERIFIED |
| Combined system value | $61.27/light/year | 🔶 DERIVED |
| Energy savings | 35% (25% eve/pre-dawn + 50% 1-5AM) | 🔶 DERIVED |
| DR revenue (CA) | $2.02/light/year | 🔶 DERIVED |
| Peak reduction | 14-28 kW per 1,000 lights | 🔶 DERIVED |
| Pricing | $3-12/light/year | — |
| ROI timeline | <12 months | 🔶 DERIVED |

**Status Key:**
- ✅ VERIFIED — Backed by cited source
- 🔶 DERIVED — Calculated from verified inputs
- ⚠️ ESTIMATE — Interpolated or approximated
- 🔴 PLACEHOLDER — Needs source; do not cite as fact

---

## Reference Files

### ⚠️ CRITICAL: Always Check Numbers Audit First

**Before citing ANY number, read [Numbers Audit](references/numbers-audit.md).**

Each number shows: the claim, derivation logic, source citations, and verification status.

---

- **[Numbers Audit](references/numbers-audit.md)** — Derivation logic and sources for ALL quantitative claims
- **[Financial Model](references/financial-model.md)** — Full methodology for $51.09 municipal + $10.18 utility calculations

---

## Source Documents

Source PDFs and images are in `references/sources/`:

| File | Content |
|------|---------|
| `ledsmaster-street-light-costs.pdf` | LED-specific maintenance costs ($20-$50/yr) |
| `cps-lighting-street-light-costs-2024.pdf` | General street light costs (secondary source) |
| `osram-led-reliability-lifetime-2013.pdf` | OSRAM "Reliability and Lifetime of LEDs" — thermal/Arrhenius |
| `pge-ls2-streetlight-tariff-2026.pdf` | PG&E LS-2 tariff — authoritative 4,100 hours/year source |
| `eia-electric-power-monthly-oct2025.pdf` | EIA national electric rates — $0.1363/kWh source |
| `cpuc-acc-documentation-2024.pdf` | California Avoided Cost Calculator methodology |
| `nhtsa-crash-costs-2019.pdf` | NHTSA crash costs — Table 15-5: $10.948B state/local (3.22%) |
| `fhwa-lighting-safety-countermeasure.pdf` | FHWA crash reduction: 28-42% from lighting |
| `datam-connected-streetlight-market-2026.pdf` | 30% CAGR market growth (Jan 2026) |
| `california-streetlights-by-iou.png` | CA streetlight counts by utility territory |
| `sce-cbp-tariff-2024.pdf` | SCE Capacity Bidding Program — $79/kW/year |
| `cpuc-elrp-program-2024.pdf` | CPUC Emergency Load Reduction Program — $2/kWh |
| `streetlighting-demand-response-stockton-ca.pdf` | DR methodology and calculation example |
| `bjs-justice-expenditures-employment-2017.pdf` | BJS $246.7B state/local crime spending (Table 1) |
| `lapd-crime-data-2010-2019-open-data-portal.pdf` | LAPD 2.13M crime records — empirical verification |

---

## Value Breakdown: Municipal ($51.09/light/year)

### Asset Management: $30.44

| Component | Value | Logic |
|-----------|-------|-------|
| Maintenance savings | $4.90 | 🔶 DERIVED — See numbers-audit.md |
| Luminaire life extension | $15.76 | 50% of lights reach EOL; 12→19 yr extension |
| Energy savings | $9.78 | 205 kWh × 35% × $0.1363/kWh |

### Quality of Life: $20.65

| Component | Value | Logic |
|-----------|-------|-------|
| DSM revenue (CA) | $2.02 | CBP ($79/kW/yr) + ELRP ($2/kWh) — verified rates |
| Crime reduction | $10.81 | 1% of lighting-influenced crime cost (conservative; LAPD analysis supports $20.85) |
| Traffic incidents | $7.82 | 3% of darkness crash costs, inflation-adjusted (NHTSA 2019 + 26.1% CPI) |

**DSM Value Attribution:** Can be categorized as municipal benefit (city receives payments), utility benefit (grid flexibility), or quality of life benefit (rate stability, blackout reduction).

---

## Value Breakdown: Utility ($10.18/light/year)

Based on CPUC 2024 ACC Electric Model v1b, Climate Zone 10 (Riverside, CA).

**Key Finding:** Nighttime hours have zero capacity value (Gen Capacity, Transmission, Distribution = $0/MWh). Overnight avoided costs are GHG + Energy only (~$130-150/MWh).

**Dimming Schedule (35% savings):**
| Period | Power Level | Savings |
|--------|-------------|---------|
| Dusk to 1 AM | 75% | 25% |
| 1 AM to 5 AM | 50% | 50% |
| 5 AM to Dawn | 75% | 25% |

**Calculation:** Hour-by-hour ACC rates × hours × dimming factor, using CZ10 twilight data.
- Fleet: 20,000 lights × 50W = 1 MW
- Annual ACC benefit: $203,699
- Per light: **$10.18/light/year**

**Sources:** 2024-ACC-Electric-Model-v1b.xlsb, AccStreetLightingAnalysis.xlsx, cz10_riverside_2026.csv

**Note:** California-specific. Other jurisdictions require different methodology.

---

## Pricing & ROI

### SaaS Pricing: $3-12/light/year

Based on:
- Deployment size (volume discounts)
- Service level (self-service vs managed)
- Feature set (basic vs full dynamic scheduling)

### ROI Calculation

```
Value delivered: $51.09/light/year
Cost: $3-12/light/year
Net benefit: $39.09-48.09/light/year
ROI: <12 months
```

**Example:** 50,000-light city
- Annual value: 50,000 × $51.09 = $2.55M
- Annual cost: 50,000 × $6/light = $300K (mid-range)
- Net savings: $2.25M/year

### Pilot Structure

| Parameter | Value |
|-----------|-------|
| Scope | 1,500 networked luminaires |
| Duration | 10-12 weeks |
| Cost | ~$25,000 USD |

---

## Market Size

### Global Streetlights

| Metric | Value | Status |
|--------|-------|--------|
| Total global (2022) | 300-320M | ✅ VERIFIED |
| Connected (Jan 2026) | ~15% penetration | ⚠️ ESTIMATE |
| Market CAGR | 30% (2024-2031) | ✅ VERIFIED |

### US Streetlights

| Metric | Value | Status |
|--------|-------|--------|
| Conservative (DOE) | 26.5M | ✅ VERIFIED |
| Higher estimate | 60M | 🔴 PLACEHOLDER |

### California Streetlights

| Territory | Streetlights |
|-----------|-------------|
| PG&E | 861,224 |
| SCE | 885,222 |
| SDG&E | 233,220 |
| **Total IOUs** | **1,979,666** |
| **California Total** | **3,380,000** |

---

## National Energy Impact

**Claim:** 4,372 GWh saved annually (408,000 homes equivalent)

**Calculation:**
```
Annual kWh per light: 50W × 11.4 hrs × 365.25 = 208.19 kWh
US total (60M lights): 208.19 × 60M = 12,491 GWh
35% savings: 12,491 × 0.35 = 4,372 GWh
Homes equivalent: 4,372,000,000 ÷ 10,715 = 408,000 homes
```

**Status:** 🔶 DERIVED — Depends on 60M lights and 35% savings assumptions

---

## When to Use This Skill

**Use photometrics-financials for:**
- ROI calculations and proposal budgets
- Value per light questions
- Energy savings math
- Market size and penetration data
- Verifying any quantitative claim
- Utility cost avoidance calculations
- Pricing discussions

**Use photometrics-ai (core skill) for:**
- How the product works
- Technical architecture (TLL, optimization engine)
- Competitive positioning
- Go-to-market strategy
- Use cases and applications
