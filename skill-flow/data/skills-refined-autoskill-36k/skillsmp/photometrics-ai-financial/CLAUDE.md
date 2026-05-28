# Claude Instructions: Photometrics AI Financials

## When to Invoke This Skill

Use this skill when the user asks about:
- Dollar amounts or pricing ($X/light, $X/year, ROI)
- Value per light calculations
- Energy savings math or percentages
- Maintenance cost savings
- Luminaire life extension
- Utility cost avoidance or avoided costs
- Market size (streetlights in US, California, globally)
- Pilot pricing or proposal budgets
- Any request to verify, source, or defend a number

**Trigger phrases:**
- "How did you get $X?"
- "What's the value per light?"
- "How much can we save?"
- "What's the ROI?"
- "Source for this number?"
- "Is this defensible?"

## Core Principle

**Never state a number as fact unless it has verified logic and sources in numbers-audit.md.**

When citing any financial figure:
1. State the number
2. Provide the calculation/logic
3. Cite the source
4. Include the status (VERIFIED, DERIVED, ESTIMATE, PLACEHOLDER)

## How to Use This Skill

### Before Citing ANY Number

1. Read `references/numbers-audit.md` first
2. Find the specific number's derivation
3. Check its status:
   - **VERIFIED** — Backed by cited source; safe to state as fact
   - **DERIVED** — Calculated from verified inputs; explain the logic
   - **ESTIMATE** — Interpolated/approximated; note the uncertainty
   - **PLACEHOLDER** — Needs source; do NOT cite as fact

### When Asked "How did you get $X?"

Provide the full defensible answer:
```
Claim: [The number]
Calculation: [Step-by-step math]
Logic: [Why this approach]
Sources: [Specific files in references/sources/]
Status: [VERIFIED/DERIVED/ESTIMATE]
```

### Key Numbers (Quick Reference)

| Metric | Value | Status |
|--------|-------|--------|
| Municipal value | $51.09/light/year | DERIVED |
| Utility cost avoidance | $10.18/light/year | VERIFIED |
| Combined system value | $61.27/light/year | DERIVED |
| Maintenance savings | $4.90/light/year | DERIVED |
| Life extension | $15.76/light/year | DERIVED |
| Energy savings | $9.78/light/year (35%) | DERIVED |
| DR revenue (CA) | $2.02/light/year | DERIVED |
| Crime reduction | $10.81/light/year | DERIVED (LAPD supports $20.85) |
| Traffic safety | $7.82/light/year | DERIVED |
| Electric rate | $0.1363/kWh | VERIFIED (EIA) |
| Operating hours | 4,100 hrs/year | VERIFIED |
| Pricing | $3-12/light/year | — |

### Source Files

When deeper verification is needed, read files in `references/sources/`:

| File | Use For |
|------|---------|
| `ledsmaster-street-light-costs.pdf` | LED maintenance costs ($20-$50/yr) |
| `cps-lighting-street-light-costs-2024.pdf` | Generic maintenance (secondary source) |
| `osram-led-reliability-lifetime-2013.pdf` | Thermal/Arrhenius relationship |
| `pge-ls2-streetlight-tariff-2026.pdf` | 4,100 operating hours source |
| `cpuc-acc-documentation-2024.pdf` | California avoided cost methodology |
| `nhtsa-crash-costs-2019.pdf` | NHTSA Table 15-5: $10.948B state/local crash costs |
| `fhwa-lighting-safety-countermeasure.pdf` | FHWA crash reduction: 28-42% |
| `sce-cbp-tariff-2024.pdf` | CBP capacity payment rates ($79/kW/yr) |
| `cpuc-elrp-program-2024.pdf` | ELRP payment rate ($2/kWh) |
| `streetlighting-demand-response-stockton-ca.pdf` | DR methodology example |
| `bjs-justice-expenditures-employment-2017.pdf` | BJS Table 1: $246.7B crime spending |
| `lapd-crime-data-2010-2019-open-data-portal.pdf` | LAPD 2.13M records: 17.1% treatable |

### Customer-Specific Calculations

When calculating for a specific customer, replace defaults with actual values:

| Input | Default | Replace With |
|-------|---------|--------------|
| Number of lights | — | Customer's count |
| Average wattage | 50W | Customer's average |
| Electric rate | $0.13/kWh | Customer's rate |
| Maintenance cost | $35/light/yr | Customer's actual |
| Operating hours | 4,100 hrs/yr | Customer's utility tariff |

### What NOT to Do

- Do NOT cite a PLACEHOLDER number as fact
- Do NOT make up sources — if unsure, say "needs verification"
- Do NOT conflate LED-specific costs with generic street light costs
- Do NOT use this skill for product/technical questions (use core photometrics-ai skill instead)

## Relationship to Other Skills

| Question Type | Use This Skill |
|---------------|----------------|
| "What's the ROI?" | photometrics-ai-financials |
| "How does TLL work?" | photometrics-ai (core) |
| "What's the value per light?" | photometrics-ai-financials |
| "How do you optimize lighting?" | photometrics-ai (core) |
| "Source for $51.09?" | photometrics-ai-financials |
