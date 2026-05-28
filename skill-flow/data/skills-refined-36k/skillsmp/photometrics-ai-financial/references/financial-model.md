# Financial Model & Methodology

## Summary: Value Per Streetlight Per Year

| Stakeholder | Total Value | Components |
|-------------|-------------|------------|
| **Municipal (SLOO)** | **$51.09** | Asset management + Quality of life |
| **Utility Cost Avoidance** | **$10.18** | ACC-based (energy, GHG; zero capacity at night) |
| **Combined System Value** | **$61.27** | Municipal + Utility |

All values are **Direct, Quantifiable, and Financial** — they show up in budgets, backed by studies and concrete methodologies.

---

## Definitions

**"Direct"** = Benefits go straight to Street Light Owners and Operators (SLOOs), not to other organizations or individuals

**"Quantifiable"** = Measurable using reliable data from nationwide studies (or representative states/cities when national data unavailable)

**"Financial"** = Shows up in a SLOO's budget

**"SLOO"** = Street Light Owners and Operators (cities, counties, state highway departments, IOUs, municipal utilities, cooperatives)

---

## Core Assumption: 35% Energy Savings

Photometrics AI delivers 35% total system energy savings through two mechanisms:

1. **25% through precision design optimization** — Applied during evening hours (dusk to 1 AM) and pre-dawn (5 AM to dawn). Per-luminaire dimming based on actual geometry, overlapping beam spreads, and Target Lighting Layers. Average operating level: 75% power.

2. **50% through early morning dimming** — Applied 1AM-5AM (4 hours/night). As vehicle miles traveled and pedestrian activity decline, applicable lighting standards decrease. Operating at 50% power during these hours in low-speed, low-crime residential areas.

**Dimming Schedule:**
| Period | Power Level | Energy Savings |
|--------|-------------|----------------|
| Dusk to 1 AM | 75% | 25% |
| 1 AM to 5 AM | 50% | 50% |
| 5 AM to Dawn | 75% | 25% |

Combined effect: ~65% average power (35% savings).

---

## Asset Management Benefits: $30.44/light/year

### Maintenance Savings: $4.90/light/year

**Baseline:** $35/year per LED streetlight
- Source: LEDsMaster, "How Much Do Street Lights Cost?"
- Midpoint of $20-$50 range for **LED-specific** maintenance
- File: `sources/ledsmaster-street-light-costs.pdf`

**Why $20-$50 (LEDsMaster) instead of $50-$120 (CPS Lighting)?**
- LEDsMaster provides **LED-specific** maintenance costs: $20-$50/year
- CPS Lighting shows **generic industry figures** across all technologies: $50-$120/year
- Our analysis is LED-specific — we only calculate savings for LED streetlights
- Using the LED-specific figure is more accurate; using the midpoint ($35) is conservative

**Logic:**
1. ~40% of LED maintenance costs are thermally-driven (driver failures, LED chip degradation, reactive repairs from premature component failure)
2. ~60% is non-thermal (scheduled inspections, cleaning, knockdowns/accidents, photocell issues)
3. Running at ~65% average power reduces thermal stress on components
4. Conservative linear assumption: 35% power reduction → 35% reduction in thermally-driven failures

**Calculation:**
```
Thermally-driven portion: $35 × 0.40 = $14.00
Reduction from dimming:  $14.00 × 0.35 = $4.90/light/year
```

**Sources:**
1. LEDsMaster, "How Much Do Street Lights Cost?" — LED-specific: $20-$50/year
   File: `sources/ledsmaster-street-light-costs.pdf`
2. CPS Lighting, "How Much Does a Street Light Cost?" (May 2024) — Generic: $50-$120/year
   File: `sources/cps-lighting-street-light-costs-2024.pdf`
3. OSRAM, "Reliability and Lifetime of LEDs" (Dec 2013) — Thermal/Arrhenius relationship
   File: `sources/osram-led-reliability-lifetime-2013.pdf`

**Conservatism Note:** The linear assumption is conservative. The Arrhenius equation suggests exponential benefits from temperature reduction — actual savings may be higher.

**Unquantified Benefit:** Photometrics AI's software-based scheduling eliminates "daytime burn" failures caused by photocell malfunctions. This benefit is real but not dollarized.

---

### Extension of Luminaire Life: $15.76/light/year

**Assumptions:**
- L70 life rating: 50,000 hours (field-realistic estimate)
- Total replacement cost: $1,100 (LED $100 + installation $1,000)
- Operating hours: 4,100 hours/year
- 35% energy savings (~65% average power)
- Survival rate: 50% (only half of lights reach natural EOL)

**Logic:** Lower operating power reduces thermal stress, extending lifespan. However, not all lights reach natural end-of-life — many are replaced early due to knockdowns, technology upgrades, or utility programs. We apply a 50% survival rate to account for this.

**Why 50,000 hours (not 100,000)?**
- 100,000 hours = 24+ years baseline — unrealistic; no one believes a streetlight stays up that long
- 50,000 hours = 12 years baseline, 19 years extended — believable and defensible
- Field conditions differ from lab specs; 50,000 is conservative

**Calculation:**
```
Baseline lifespan:    50,000 / 4,100 = 12.20 years
Annualized baseline:  $1,100 / 12.20 = $90.16/year

Extended lifespan:    50,000 / 0.65 = 76,923 hours
Extended years:       76,923 / 4,100 = 18.76 years
Annualized extended:  $1,100 / 18.76 = $58.64/year

Gross savings: $90.16 - $58.64 = $31.52/light/year
Adjusted for 50% survival rate: $31.52 × 0.50 = $15.76/light/year
```

**Clean separation from Maintenance:**
- **Maintenance ($4.90)** covers repairs during service life (driver replacements, reactive fixes)
- **Life Extension ($15.76)** covers delayed capital replacement for lights that reach natural EOL

**Conservatism Note:** The inverse-linear lifespan model is conservative. The Arrhenius equation suggests exponential benefits from temperature reduction — actual savings may be higher.

---

### Energy Savings: $9.78/light/year

**Assumptions:**
- Average LED wattage: 50W (industry standard — needs citation)
- Operating hours: 4,100 hours/year (PG&E LS-2 tariff)
- Electric rate: $0.1363/kWh (EIA exact figure, consumption-weighted)
- Energy savings: 35% (25% evening/pre-dawn + 50% early morning 1-5 AM)

**Calculation:**
```
Baseline annual energy cost: (50W / 1000) × 4,100 hrs × $0.1363 = $27.94/year
Savings at 35%: $27.94 × 0.35 = $9.78/light/year
```

**Why "All Sectors" (consumption-weighted) from EIA?**
- Streetlight ownership varies — municipalities, utilities, state DOTs
- No single EIA sector fits all streetlight billing arrangements
- Consumption-weighted reflects actual cost per kWh sold nationally
- States with lower rates consume more electricity (pulling average down)
- Lower-rate states have less incentive to optimize — not our primary market

**Why exact $0.1363/kWh?**
- EIA October 2025, All Sectors = 13.63¢/kWh (consumption-weighted)
- Using exact figure for precision
- Rates vary widely by state (7¢ in ND to 28¢+ in CA)
- Customer calculations should use their actual utility rate

**Sources:**
1. U.S. Energy Information Administration, Electric Power Monthly, Table 5.6.A, October 2025
   File: `sources/eia-electric-power-monthly-oct2025.pdf`
2. PG&E Electric Schedule LS-2 — 4,100 operating hours
   File: `sources/pge-ls2-streetlight-tariff-2026.pdf`

**Scaling example:** 3,000 streetlights = ~$33,500 annual savings

---

## Quality of Life Benefits: $20.65/light/year

### Demand Side Management: $2.02/light/year

Based on California's Capacity Bidding Program (CBP) and Emergency Load Reduction Program (ELRP).

**Value Attribution:** DSM revenue can be categorized multiple ways:
- **Municipal benefit** — The municipality receives DR payments directly as revenue
- **Utility benefit** — The utility gains grid flexibility and avoided capacity costs
- **Quality of life benefit** — Residents benefit from more stable rates and reduced blackout risk

**Assumptions (Stockton example, scaled per light):**
- 20,000 streetlights
- Average wattage: 50W
- DR reduction capability: 75% (aggressive dimming to 25% during events)
- Event availability: 46.8% (4,100 operating hours ÷ 8,766 annual hours)
- CBP: 20 non-emergency events/year max, 3 hours each
- ELRP: 5 emergency events/year max, 3 hours each

**Payment Rates (verified):**
| Program | Rate | Status | Source |
|---------|------|--------|--------|
| CBP Capacity | $79/kW/year | ✅ VERIFIED | SCE Schedule CBP (Feb 2024) |
| CBP Energy | $0.10/kWh | ⚠️ ESTIMATE | Historical ~$0.08 |
| ELRP | $2.00/kWh | ✅ VERIFIED | CPUC ELRP program |

**Calculation:**
```
Committed capacity: 20,000 × 50W × 75% × 46.8% = 351 kW

CBP Capacity Payment: 351 kW × $79/kW/year = $27,729/year
CBP Energy Payment: 21,060 kWh × $0.10/kWh = $2,106/year
ELRP Payment: 5,265 kWh × $2.00/kWh = $10,530/year

Total: $27,729 + $2,106 + $10,530 = $40,365/year
Per light: $40,365 / 20,000 = $2.02/light/year
```

**Why 75% DR reduction (not 35%)?**
- Normal operation: 35% energy savings (~65% average power) — optimized for lighting quality
- DR events: 75% reduction (25% power) — aggressive dimming for short emergency periods
- Both measured against LED at full power baseline

**Sources:**
1. SCE Schedule CBP Tariff (Feb 2024) — CBP capacity rates by month
   File: `sources/sce-cbp-tariff-2024.pdf`
2. CPUC Emergency Load Reduction Program — ELRP $2/kWh rate
   File: `sources/cpuc-elrp-program-2024.pdf`
3. Internal analysis: "Street Lighting for Demand Response - Stockton CA"
   File: `sources/streetlighting-demand-response-stockton-ca.pdf`

**Geographic Note:** California-specific. Other states may have different DR programs or none at all.

---

### Crime Reduction: $10.81/light/year (conservative)

**Inputs:**
- State/local government spending on police, judicial, corrections (2017): $246.7B
- US streetlights: 26.5 million
- Crimes occurring at night: 45% (TheSleepJudge study, 840K incidents)
- Crimes influenced by street lighting: 20% (conservative assumption)
- Crime reduction from Photometrics AI: 1% (conservative)
- Inflation since 2017: 29%

**Original Calculation:**
```
Crime cost per streetlight: $246.7B / 26.5M = $9,309/light
Nighttime outdoor crimes: $9,309 × 0.45 × 0.20 = $837.90/light
1% reduction: $837.90 × 0.01 = $8.38/light
Inflation adjusted: $8.38 × 1.29 = $10.81/light/year
```

**Empirical Verification (LAPD Crime Data 2010-2019):**

We analyzed 2.13 million crime records to verify our assumptions:

| Metric | Original Assumption | LAPD Empirical |
|--------|---------------------|----------------|
| Crimes when streetlights ON | 45% | 39.2% |
| Of those, at lighting-influenced locations | 20% | 43.6% |
| **Treatable universe** | **9.0%** | **17.1%** |

**Methodology:**
- Calculated astronomical sun position for each crime (lat/long/date/time)
- Streetlights ON = nautical twilight or darker (sun 6°+ below horizon)
- Lighting-influenced = STREET, SIDEWALK, ALLEY, DRIVEWAY, etc. (premises where municipal lighting affects visibility)

**Updated Calculation (if using empirical 17.1%):**
```
$246.7B × 17.1% / 26.5M × 1% × 1.29 = $20.55/light/year
```

**Why we keep $10.81:**
1. Los Angeles is urban; may not represent national crime mix
2. Conservative figure is easier to defend in proposals
3. Can cite $20.55 as "validated upside" when appropriate
4. Maintains credibility with skeptical reviewers

**Sources:**
1. Bureau of Justice Statistics, "Justice Expenditure and Employment in the United States, 2017" (NCJ 256093, July 2021)
   - **Table 1:** State ($93.1B) + Local ($153.6B) = $246.7B
   - File: `sources/bjs-justice-expenditures-employment-2017.pdf`
2. Los Angeles Police Department, "Crime Data from 2010 to 2019"
   - Source: LA Open Data Portal (data.lacity.org)
   - Records: 2.13M crime incidents, CC0 license
   - File: `sources/lapd-crime-data-2010-2019-open-data-portal.pdf`
3. TheSleepJudge, "Crime and the Clock" — 45% nighttime crimes
   - File: `sources/Crimes that Happen While You Sleep - The Sleep Judge.pdf`

**Methodology Note:** This calculation treats all crimes equally (total spending ÷ crime count). In reality, violent crimes cost far more than property crimes. If violent crimes skew nighttime, our figure is conservative; if they skew daytime, it may be aggressive. Street-level crimes in the ROW (robbery, assault, vehicle theft) tend to be more serious than daytime retail theft, suggesting our figure is likely conservative. See numbers-audit.md for full discussion.

---

### Reduction in Traffic Incidents: $7.82/light/year

**Why municipalities bear crash costs:**
> "State and local government pay almost all costs of police, fire, emergency medical, vocational rehabilitation, victim assistance, and coroner services; incident management; and roadside furniture damage."
— NHTSA, "The Economic and Societal Impact of Motor Vehicle Crashes, 2019" (p. 327)

**Inputs:**
| Input | Value | Source |
|-------|-------|--------|
| Total crash costs 2019 | $339.809B | NHTSA Table 15-5 |
| State/local share | $10.948B (3.22%) | NHTSA Table 15-5 |
| US streetlights | 26.5M | DOE |
| Darkness crashes | 50% | FHWA (equal day/night fatals) |
| Improvement | 3% | Conservative estimate |
| Inflation 2019→2025 | 26.1% | BLS CPI CUUR0000SA0 |

**Calculation:**
```
State/local crash costs per streetlight:
  $10.948B ÷ 26.5M = $413.13/light

Darkness-related portion (50%):
  $413.13 × 0.50 = $206.57

Improvement from better lighting (3%):
  $206.57 × 0.03 = $6.20 (2019 dollars)

Inflation adjustment (26.1%):
  $6.20 × 1.261 = $7.82/light/year (2025 dollars)
```

**Why 50% darkness crashes?**
FHWA states: "The number of fatal crashes occurring in daylight is about the same as those that occur in darkness." The nighttime fatality rate is 3× higher despite only 25% of VMT occurring at night — darkness crashes are disproportionately severe.

**Why 3% improvement?**
FHWA documents that lighting can reduce crashes by 28-42%. However, these figures are for **installing lighting where there was none**. Photometrics AI optimizes **existing** lighting through faster outage detection, maintained output, and consistent operation. The 3% assumption says: "Of the 28% benefit that proper lighting provides, we capture ~10% through better management."

**FHWA Proven Safety Countermeasures — lighting can reduce crashes:**
- 42% for nighttime injury pedestrian crashes at intersections
- 33-38% for nighttime crashes at rural/urban intersections
- 28% for nighttime injury crashes on rural/urban highways

**Sources:**
1. NHTSA, "The Economic and Societal Impact of Motor Vehicle Crashes, 2019" (DOT HS 813 403)
   - Table 15-5: State/Locality $10,948M (3.22% of $339.809B)
   - File: `sources/nhtsa-crash-costs-2019.pdf`
2. FHWA Proven Safety Countermeasures: Lighting (FHWA-SA-21-050)
   - File: `sources/fhwa-lighting-safety-countermeasure.pdf`
3. BLS CPI (CUUR0000SA0): Dec 2019 = 256.974, Dec 2025 = 324.054 → 26.1% inflation

---

## Utility Cost Avoidance: $10.18/light/year

Calculated using the **CPUC 2024 Avoided Cost Calculator (ACC)** Electric Model v1b, configured for Climate Zone 10 (Riverside, CA area) under the Total Resource Cost test with a 20-year levelization period.

### ACC Methodology

The ACC produces hourly avoided costs that incorporate **all utility cost components**:
- Generation energy
- Generation capacity
- Transmission capacity
- Distribution capacity
- GHG compliance (cap-and-trade + GHG adder with rebalancing)
- Ancillary services
- System losses

### Key Finding: Nighttime Capacity Values Are Zero

**Critical insight:** Overnight hours (10 PM to 6 AM) have **zero capacity value** — Generation Capacity, Transmission, and Distribution avoided costs are $0/MWh. This significantly reduces the avoided cost value for streetlighting compared to daytime load reduction.

Nighttime avoided costs are dominated by:
- **GHG components:** ~$70-80/MWh (Cap-and-Trade + GHG Adder + Rebalancing)
- **Energy:** ~$50-70/MWh

Evening hours (5-8 PM) retain capacity value and have much higher rates ($230-450/MWh in summer).

### Calculation at 35% Savings

**Dimming Schedule:**
| Period | Dimming Level | Energy Savings |
|--------|---------------|----------------|
| Dusk to 1 AM | 25% (75% power) | 25% |
| 1 AM to 5 AM | 50% (50% power) | 50% |
| 5 AM to Dawn | 25% (75% power) | 25% |

**Hour-by-Hour Calculation:**

Using actual twilight times for Riverside, CA (CZ10) and ACC hourly rates by season:

```
Fleet: 20,000 lights × 50W = 1 MW
Operating hours: Extracted from nautical twilight data (tool-sun-phase)
ACC rates: Extracted from 2024-ACC-Electric-Model-v1b.xlsb "Detailed Output" sheet

Seasonal periods:
- Summer (May-Oct): Higher evening rates, moderate overnight
- Winter (Nov-Apr): Lower overall rates

Calculation: Σ (hours × MW × dimming% × ACC rate) for each hour slot and season

Total annual ACC benefit: $203,699
Per light: $203,699 / 20,000 = $10.18/light/year
```

**Sample ACC Rates ($/MWh):**
| Hour | May-Oct | Nov-Apr |
|------|---------|---------|
| Midnight | 142.97 | 144.57 |
| 1 AM | 144.03 | 147.70 |
| 5 AM | 81.78 | 132.27 |
| 5 PM | 466.60 | 155.71 |
| 6 PM | 345.57 | 146.76 |

**Sources:**
1. CPUC 2024 ACC Electric Model v1b (2024-ACC-Electric-Model-v1b.xlsb)
2. AccStreetLightingAnalysis.xlsx — Detailed hour-by-hour calculation
3. cz10_riverside_2026.csv — Twilight times for Climate Zone 10

**Note:** This is California-specific. Other jurisdictions may have different avoided cost values or no equivalent methodology.

---

## National Energy Impact

**Base assumptions:**
- Average streetlight wattage: 50W
- Operating hours per day: 11.4 hours
- Days per year: 365.25
- US streetlights: 60,000,000
- Average US household annual consumption: 10,715 kWh
- Energy savings: 35%

**Calculation:**
```
a. Annual consumption per streetlight: 50W × 11.4 hrs × 365.25 days / 1000 = 208.19 kWh
b. Total US consumption: 208.19 kWh × 60,000,000 = 12,491.4 GWh
c. Savings at 35%: 12,491.4 GWh × 0.35 = 4,372 GWh
d. Equivalent homes: 4,372,000,000 kWh / 10,715 kWh/household = 408,000 homes
```

**Standard phrasing:** "Photometrics AI saves an average of 35% energy on the 60 million streetlights in the US, equivalent to 4,372 GWh annually or the energy consumption of approximately 408,000 homes."

---

## Customer Calculator Approach

For any customer, replace these generic assumptions with actual values:

| Input | Generic Value | Customer Value |
|-------|---------------|----------------|
| Number of streetlights | — | _____ |
| Average wattage | 50W | _____ |
| Electric rate ($/kWh) | $0.13 | _____ |
| Annual maintenance cost/light | $35 | _____ |
| Luminaire + install cost | $1,100 | _____ |
| L70 rating (hours) | 50,000 | _____ |
| Operating hours/year | 4,100 | _____ |
| Survival rate to EOL | 50% | _____ |

---

## ROI Summary

| Metric | Value |
|--------|-------|
| Value delivered | $51.09/light/year (municipal) |
| Pricing | $3-12/light/year |
| ROI | **<12 months** |
| 50,000-light city annual savings | **$2.55M+** |

Compare to LED retrofits: years to payback, capital-intensive, hardware required.

---

## Direct Unquantifiable Financial Benefits

These are real but harder to assign dollar values:

**Strategic Funding Opportunities**
- SS4A (Safe Streets For All)
- SMART grants
- DOE EECBG and GRIP programs
- DOJ Byrne JAG and COPS grants
- Photometrics AI strengthens grant applications with data-driven evidence

**Liability Reduction**
- Demonstrate purposeful, optimized lighting management
- Respond quickly to ROW changes (new crosswalks, bike lanes)
- Stronger legal position than "grouped standards" or "hasn't been reviewed"

**Resource Optimization**
- Automate routine tasks
- Free lighting professionals for complex/creative work

**Community & Economic Vibrancy**
- NYC nightlife: $35B annually, 300,000 jobs
- 1% increase = $350M economic activity = $31M tax revenue
- $124/streetlight/year in additional tax receipts (NYC example)

**Policy Alignment**
- Vision Zero
- Climate Action Plans
- DarkSky Recognized Codes and Statutes
- Local outdoor lighting ordinances

**Real Estate Value**
- 1-3% property value increase from perceived safety improvements
- 100,000 properties × $300,000 avg × 1% = $300M value increase

---

## Source Documentation

For detailed methodology, exact citations, or defense of calculations, see `references/sources/`:

| File | Content | Key Search Terms |
|------|---------|------------------|
| `ledsmaster-street-light-costs.pdf` | LED-specific maintenance costs ($20-$50/yr) | "$20-$50", "maintenance", "LED" |
| `cps-lighting-street-light-costs-2024.pdf` | Generic street light costs (secondary source) | "$50-$120", "maintenance", "TCO" |
| `pge-ls2-streetlight-tariff-2026.pdf` | PG&E LS-2 tariff — 4,100 hours/year source | "4,100 hours", "monthly energy charges", "formula" |
| `osram-led-reliability-lifetime-2013.pdf` | OSRAM "Reliability and Lifetime of LEDs" — thermal/Arrhenius | "junction temperature", "Arrhenius", "failure rate", "10°C" |
| `nhtsa-crash-costs-2019.pdf` | NHTSA crash costs — Table 15-5: $10.948B state/local | "state and local", "Table 15-5", "$339.8 billion", "3.22%" |
| `fhwa-lighting-safety-countermeasure.pdf` | FHWA Proven Safety Countermeasures - Lighting | "42%", "33-38%", "28%", "pedestrian", "intersection" |
| `cpuc-acc-documentation-2024.pdf` | California Avoided Cost Calculator methodology | "hourly avoided cost", "generation capacity", "T&D", "PCAF" |
| `eia-electric-power-monthly-oct2025.pdf` | EIA national electric rates by state | "U.S. Total", "13.63", "Commercial", "All Sectors" |
| `sce-cbp-tariff-2024.pdf` | SCE Capacity Bidding Program rates — $79/kW/year | "capacity credit", "$27.19", "August", "May-October" |
| `cpuc-elrp-program-2024.pdf` | CPUC Emergency Load Reduction Program — $2/kWh | "$2/kWh", "non-residential", "grid emergency" |
| `streetlighting-demand-response-stockton-ca.pdf` | DR analysis methodology — Stockton example | "CBP", "ELRP", "46.8%", "75% reduction" |
| `bjs-justice-expenditures-employment-2017.pdf` | BJS state/local crime spending | "$246.7B", "Table 1", "police", "corrections" |
| `lapd-crime-data-2010-2019-open-data-portal.pdf` | LAPD crime data — empirical verification | "2.13M", "17.1%", "treatable", "streetlights ON" |

**When to read these files:**
- Grant reviewer challenges crash reduction methodology → Read FHWA doc
- Need exact citation for $339.8B crash cost → Read NHTSA doc
- Defending ACC calculation approach → Read CPUC doc
- Challenged on "$246.7B" crime spending → Read BJS doc, cite Table 1
- Asked "how do you know 17.1%?" → Reference LAPD analysis methodology

**Do not load these files** for routine proposals or general questions—the summary data in this file is sufficient.

---

## Quick Reference Citations

**Crash Reduction (FHWA-SA-21-050):**
- 42% reduction for nighttime injury pedestrian crashes at intersections
- 33-38% reduction for nighttime crashes at rural and urban intersections
- 28% reduction for nighttime injury crashes on rural and urban highways
- Source: Elvik, R. and Vaa, T., "Handbook of Road Safety Measures." Oxford, United Kingdom, Elsevier, (2004).

**Crash Costs (NHTSA 2019, inflation-adjusted):**
- Total economic cost: $339.809 billion (2019)
- State/local government share: 3.22% ($10.948B)
- Includes: police, fire, EMS, victim assistance, incident management
- Inflation 2019→2025: 26.1% (BLS CPI CUUR0000SA0)
- Source: "The Economic and Societal Impact of Motor Vehicle Crashes, 2019" Table 15-5

**Avoided Costs (CPUC 2024 ACC):**
- All-inclusive hourly rates bundle: energy, generation capacity, T&D capacity, GHG, ancillary services, losses
- Capacity allocated via Peak Capacity Allocation Factor (PCAF) method
- SCE Climate Zone 10, TRC test, 20-year levelization

---

## Additional Sources (Not in /sources/)

- DOE: 26.5M US streetlights (conservative; 60M used for national impact)
- EIA: National average electric rate $0.13/kWh
- Clean Energy Ministerium: Street lighting = 1-3% of electricity demand

## Sources in /sources/

- **LEDsMaster** — "How Much Do Street Lights Cost?" — LED-specific maintenance: $20-$50/year (midpoint $35)
- **CPS Lighting** — "How Much Does a Street Light Cost?" (May 2024) — Generic industry maintenance: $50-$120/year (secondary source, makes our estimate conservative)
- **PG&E LS-2 Tariff** — Electric Schedule LS-2, Cal. P.U.C. Sheet No. 60744-E, January 2026 — Authoritative source for 4,100 hours/year operating assumption
- **OSRAM** — "Reliability and Lifetime of LEDs" Application Note, December 2013 — Thermal stress / Arrhenius relationship for LED lifespan
- **SCE Schedule CBP** — Cal. PUC Sheet No. 87373-E, February 2024 — CBP capacity payment rates ($79/kW/year season total)
- **CPUC ELRP** — Emergency Load Reduction Program documentation — $2/kWh for non-residential participants
- **Stockton DR Analysis** — Internal analysis of streetlight demand response potential — 46.8% availability, 75% reduction methodology
- **BJS** — "Justice Expenditure and Employment in the United States, 2017" (NCJ 256093) — Table 1: $246.7B state/local spending
- **LAPD Crime Data** — LA Open Data Portal, 2.13M crime records (2010-2019) — Empirical verification: 17.1% treatable universe
