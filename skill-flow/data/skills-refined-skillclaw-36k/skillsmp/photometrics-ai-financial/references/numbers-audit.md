# Numbers Audit

**Purpose:** Single source of truth for every number Photometrics AI uses. Each entry shows the claim, derivation logic, and source material so you never have to re-research how you got to a figure.

**Status Key:**
- ✅ VERIFIED — Backed by cited source with clear derivation
- 🔶 DERIVED — Calculated from verified inputs using documented logic
- ⚠️ ESTIMATE — Interpolated, rounded, or approximated from partial data
- 🔴 PLACEHOLDER — Needs source; do not cite as fact

---

## Market Size & Penetration

### Global Streetlights: 300-320 Million (as of 2022)

**Claim:** There are approximately 300-320 million streetlights worldwide  
**Logic:** Direct from source  
**Sources:**
- Arthur D. Little smart street lighting report (used 320M figure)
- Northeast Group (used ~300M figure)

**Status:** ✅ VERIFIED

---

### Connected Streetlights Penetration: ~15% (January 2026)

**Claim:** Approximately 15% of streetlights globally are connected to networked lighting controls  
**Logic:**
- Total global streetlights: 320 million (Arthur D. Little)
- Connected end of 2022: 23 million → 23M / 320M = **7.2% penetration**
- Projected 2027: 63.8 million → 63.8M / 320M = **~20% penetration**
- Linear interpolation to January 2026: ~15%

**Interpolation math:**
```
2022 end: 7.2%
2027 end: 20%
Growth over 5 years: 12.8 percentage points
Growth per year: 2.56 pp
Years from end 2022 to Jan 2026: ~3.1 years
Estimated Jan 2026: 7.2% + (2.56 × 3.1) = 15.1%
```

**Sources:**
- Arthur D. Little: 320M total streetlights
- [NEED SOURCE]: 23M connected end of 2022
- [NEED SOURCE]: 63.8M projected 2027

**Status:** ⚠️ ESTIMATE — Interpolated from 2022 actual to 2027 projection. The original "15%" claim was likely a rounded estimate; actual 2022 data shows 7.2%.

**Note:** GTM file currently shows different numbers (41.2M connected in 2025, 119.6M in 2030). Need to reconcile these two datasets.

---

### NLC Market Growth CAGR: 30%

**Claim:** Connected street light market growing at 30% CAGR (2024-2031)  
**Logic:** Direct from source  
**Sources:**
- DataM Intelligence, "Connected Street Light Market Set to Transform Urban Infrastructure" (January 2026)
- Report covers forecast period 2024-2031
- Published on openPR, January 8, 2026

**Status:** ✅ VERIFIED

**Note:** This supersedes the older 22.7% CAGR figure previously used. The GTM file data points (2019: 10.0M, 2025: 41.2M, 2030: 119.6M) may be from an older report and should be updated or removed to avoid confusion.

---

### ~~NLC Market Growth CAGR: 22.7%~~ (DEPRECATED)

**Status:** ❌ SUPERSEDED by 30% CAGR from DataM Intelligence (Jan 2026)

**Previous data points (source unknown, may be outdated):**
- 2019: 10.0M (3.2%)
- 2025: 41.2M (12%)
- 2030: 119.6M (32%)

**Action:** Remove from GTM file or update with current source.

---

### 374M Streetlights Worldwide by 2029

**Claim:** 374 million streetlights worldwide by 2029  
**Logic:** From source projection  
**Sources:**
- [NEED SOURCE]

**Status:** 🔴 PLACEHOLDER — No source cited

---

### US Streetlights: 26.5M (conservative) / 60M (national impact)

**Claim:** US has 26.5 million to 60 million streetlights  
**Logic:**
- 26.5M: DOE conservative estimate (used for per-light calculations)
- 60M: Higher estimate (used for national energy impact)

**Sources:**
- DOE: 26.5M figure
- [NEED SOURCE]: 60M figure

**Status:** ✅ VERIFIED (26.5M) / 🔴 PLACEHOLDER (60M needs source)

---

### California Streetlights: 3,380,000

**Claim:** California has approximately 3.38 million streetlights  
**Logic:** Population-based allocation using CA total population and national streetlight density

| Region | Population | % of CA Pop | Estimated Streetlights | 25% Energy Savings (MWh/year) | Homes Equivalent |
|--------|------------|-------------|------------------------|-------------------------------|------------------|
| PG&E | 13,302,816 | 25.48% | 861,224 | 53,827 | 5,023 |
| SCE | 13,676,473 | 26.19% | 885,222 | 55,326 | 5,164 |
| SDG&E | 3,603,348 | 6.90% | 233,220 | 14,576 | 1,361 |
| **Total IOUs** | **30,582,637** | **58.57%** | **1,979,666** | **123,729** | **11,548** |
| **California** | **52,214,021** | **100%** | **3,380,000** | **211,250** | **19,715** |

**Derivation method:**
- California population: 52,214,021
- Streetlight-to-population ratio derived from [NEED: source for base ratio]
- IOU territories allocated by population percentage

**Sources:**
- Population data: [NEED: Census or CA DOF source/year]
- Streetlight estimate methodology: Internal analysis

**Status:** 🔶 DERIVED — Logic documented; base ratio source needed

**Usage notes:**
- Use 3.38M for California-specific proposals
- IOU breakdown useful for utility program applications (CalNEXT, etc.)
- 25% savings column assumes design optimization only (not early morning dimming)

---

## Energy & Savings

### 35% Total Energy Savings

**Claim:** Photometrics AI delivers 35% total system energy savings
**Logic:** Sum of two mechanisms:
1. **25% through precision design optimization** — Evening (dusk to 1 AM) and pre-dawn (5 AM to dawn), per-luminaire dimming = 75% power
2. **50% through early morning dimming** — 1AM-5AM (4 hrs/night), operating at 50% power during low-activity hours

**Dimming Schedule:**
| Period | Power Level | Energy Savings |
|--------|-------------|----------------|
| Dusk to 1 AM | 75% | 25% |
| 1 AM to 5 AM | 50% | 50% |
| 5 AM to Dawn | 75% | 25% |

**Combined effect calculation (using CZ10 twilight data):**
```
Evening hours (dusk to 1AM): ~5-6 hrs at 75% power
Early morning (1AM-5AM): 4 hrs at 50% power
Pre-dawn (5AM-dawn): ~1-2 hrs at 75% power

Weighted average power: ~65%
Energy savings: 100% - 65% = 35%
```

**Sources:**
- Internal engineering analysis
- CZ10 twilight data (tool-sun-phase, Riverside CA)
- AccStreetLightingAnalysis.xlsx

**Status:** 🔶 DERIVED — Logic documented, based on actual twilight analysis for Climate Zone 10

---

### Operating Hours: 4,100 hours/year (default)

**Claim:** Street lights operate approximately 4,100 hours annually (default for calculations)

**Logic:**
- Operating hours = dusk-to-dawn, varies by latitude
- PG&E LS-2 tariff explicitly states 4,100 hours in rate calculation formula
- Some utilities use 4,165 hours
- Astronomical average: 11.4 hrs/night × 365.25 days = ~4,164 hours

**Defensible Approach:**
- Use **4,100 hours as default** (conservative, citable to official PG&E tariff)
- Document that this varies by location/utility (range: 4,100-4,200)
- Customer calculator should use their actual tariff hours for precision

**Sources:**
1. PG&E Electric Schedule LS-2, Cal. P.U.C. Sheet No. 60744-E, Effective January 1, 2026
   - Page 1: "Monthly energy charges per lamp are calculated using the following formula: (Lamp wattage + ballast wattage) x **4,100 hours**/12 months/1000"
   - File: `sources/pge-ls2-streetlight-tariff-2026.pdf`
2. Astronomical calculation for typical US latitude: ~4,164 hours

**Status:** ✅ VERIFIED — Official California PUC-approved utility tariff

**Note for customer calculations:** Always use the customer's actual utility tariff hours when available. The 4,100 default is conservative and citable to an official regulatory document.

---

### Average LED Wattage: 50W

**Claim:** Average streetlight LED wattage is 50W  
**Logic:** Industry standard assumption for LED streetlights (replacing ~150-200W HPS)  
**Sources:**
- [NEED SOURCE]: Industry average data

**Status:** 🔴 PLACEHOLDER — Commonly used but needs citation

---

### Annual kWh per Streetlight: 208.19 kWh

**Claim:** Average streetlight consumes 208.19 kWh annually  
**Logic:**
```
50W × 11.4 hrs/day × 365.25 days / 1000 = 208.19 kWh
```

**Status:** 🔶 DERIVED — Correct math from stated assumptions (50W, 11.4 hrs)

---

### National Energy Impact: 4,372 GWh saved / 408,000 homes equivalent

**Claim:** Photometrics AI saves 4,372 GWh annually (equivalent to 408,000 homes)
**Logic:**
```
a. Annual consumption per streetlight: 208.19 kWh
b. Total US consumption (60M lights): 208.19 kWh × 60M = 12,491.4 GWh
c. Savings at 35%: 12,491.4 × 0.35 = 4,372 GWh
d. Equivalent homes: 4,372,000,000 kWh / 10,715 kWh/household = 408,000 homes
```

**Sources:**
- EIA: 10,715 kWh average household consumption
- 60M streetlights assumption (needs verification)

**Status:** 🔶 DERIVED — Math correct; depends on 60M lights and 35% savings assumptions

---

## Financial Model

### Municipal Value: $51.09/light/year

**Claim:** Total municipal value is $51.09 per streetlight per year
**Logic:** Sum of asset management ($30.44) + quality of life ($20.65)

**Breakdown:**
| Component | Value | Logic |
|-----------|-------|-------|
| Maintenance savings | $4.90 | 🔶 DERIVED — See dedicated section below |
| Luminaire life extension | $15.76 | 50% of lights reach EOL; 12→19 yr extension |
| Energy savings | $9.78 | 🔶 DERIVED — 35% of $27.94 baseline |
| DSM revenue | $2.02 | CA CBP + ELRP programs (verified rates) |
| Crime reduction | $10.81 | 1% of treatable crime cost (conservative; LAPD data supports $20.85) |
| Traffic incident reduction | $7.82 | 3% of darkness crash costs, inflation-adjusted |
| **Total** | **$51.09** | |

**Status:** 🔶 DERIVED — Each component has documented methodology in financial-model.md

---

### Energy Savings: $9.78/light/year

**Claim:** Reduced energy costs from running LEDs at ~65% average power

**Inputs:**
- Average LED wattage: 50W (🔴 PLACEHOLDER — needs industry source)
- Operating hours: 4,100 hrs/year (✅ VERIFIED — PG&E LS-2)
- Electric rate: $0.1363/kWh (✅ VERIFIED — EIA exact figure)
- Energy savings: 35% (🔶 DERIVED — 25% evening/pre-dawn + 50% early AM)

**Calculation:**
```
Baseline annual cost: (50W / 1000) × 4,100 hrs × $0.1363/kWh = $27.94/year
Savings at 35%: $27.94 × 0.35 = $9.78/light/year
```

**Logic:**
- 25% savings from precision design optimization (dusk-1AM, 5AM-dawn at 75% power)
- 50% savings during early morning hours (1AM-5AM at 50% power)
- Combined: 35% total energy savings → ~65% average power

**Why $0.1363/kWh (exact EIA figure)?**
- EIA October 2025, All Sectors: 13.63¢/kWh (consumption-weighted)
- Using exact figure for precision
- Consumption-weighted reflects actual cost per kWh sold nationally
- Customer calculations should use their actual utility rate

**Sources:**
1. U.S. Energy Information Administration, Electric Power Monthly, Table 5.6.A, October 2025
   File: `sources/eia-electric-power-monthly-oct2025.pdf`
2. PG&E Electric Schedule LS-2 — 4,100 operating hours
   File: `sources/pge-ls2-streetlight-tariff-2026.pdf`

**Status:** 🔶 DERIVED — 50W wattage assumption needs citation

**Scaling example:** 3,000 streetlights × $9.78 = ~$29,300 annual savings

---

### Utility Cost Avoidance: $10.18/light/year

**Claim:** Utility avoided cost value is $10.18 per light per year

**Logic:**
- Based on CPUC 2024 ACC Electric Model v1b (Avoided Cost Calculator)
- SCE Climate Zone 10, TRC test, 20-year levelization
- Hour-by-hour avoided costs applied to actual streetlight operating hours
- Twilight times from tool-sun-phase for Riverside, CA (CZ10)

**Key Finding:** Nighttime hours have **zero capacity value** — Generation Capacity, Transmission, and Distribution avoided costs are $0/MWh overnight. Nighttime value is dominated by GHG (~$70-80/MWh) and Energy (~$50-70/MWh).

**Dimming Schedule (35% total energy savings):**
| Period | Hours | Dimming | Savings |
|--------|-------|---------|---------|
| Dusk to 1 AM | ~5-6 hrs | 25% | 25% of energy |
| 1 AM to 5 AM | 4 hrs | 50% | 50% of energy |
| 5 AM to Dawn | ~1-2 hrs | 25% | 25% of energy |

**Calculation:**
```
Fleet: 20,000 lights × 50W = 1 MW
Annual hours by slot: Extracted from CZ10 twilight data (Riverside, CA)
ACC rates by hour: Extracted from 2024-ACC-Electric-Model-v1b.xlsb

Seasonal breakdown:
- May-Oct (Summer): Higher evening rates ($230-450/MWh at 5-7 PM)
- Nov-Apr (Winter): Lower overall rates (~$140-155/MWh overnight)

Total annual ACC benefit: $203,699
Per light: $203,699 / 20,000 = $10.18/light/year
```

**ACC Hourly Rates ($/MWh) - Nighttime:**
| Hour | May-Oct | Nov-Apr |
|------|---------|---------|
| 00:00 | 142.97 | 144.57 |
| 01:00 | 144.03 | 147.70 |
| 02:00 | 139.68 | 146.13 |
| 03:00 | 132.33 | 143.27 |
| 04:00 | 121.29 | 142.07 |
| 05:00 | 81.78 | 132.27 |
| 17:00 | 466.60 | 155.71 |
| 18:00 | 345.57 | 146.76 |
| 19:00 | 232.43 | 138.60 |

**Sources:**
1. CPUC 2024 ACC Electric Model v1b (2024-ACC-Electric-Model-v1b.xlsb)
   - "Detailed Output" sheet, hourly avoided costs by component
   - SDG&E CZ10 configuration (same nighttime values as SCE CZ10)
2. AccStreetLightingAnalysis.xlsx — Hour-by-hour calculation workbook
3. acc_hourly_rates.csv — Extracted hourly rates by season
4. cz10_riverside_2026.csv — Climate Zone 10 twilight times (tool-sun-phase)
5. cpuc-acc-documentation-2024.pdf — ACC methodology documentation

**Status:** ✅ VERIFIED — Calculated from actual ACC model hourly outputs and location-specific twilight data

---

### Combined System Value: $61.27/light/year

**Claim:** Combined municipal + utility value is $61.27/light/year
**Logic:**
```
$51.09 (municipal) + $10.18 (utility ACC) = $61.27
```

**Status:** 🔶 DERIVED — Simple sum of verified components

---

### Maintenance Cost Baseline: $35/light/year

**Claim:** Baseline maintenance cost is $35 per streetlight per year
**Logic:** Midpoint of LED-specific maintenance range ($20-$50/year)

**Why $20-$50 (LEDsMaster) instead of $50-$120 (CPS Lighting)?**
- LEDsMaster provides **LED-specific** maintenance costs: $20-$50/year
- CPS Lighting shows **generic industry figures** across all technologies: $50-$120/year (same range for LED, HPS, Metal Halide, Solar)
- LEDsMaster explicitly notes LEDs require less maintenance than legacy HPS ($100-$200/year) due to fewer failures
- Our analysis is **LED-specific** — we're only calculating savings for LED streetlights, not legacy technology
- Using the LED-specific figure is more accurate and still conservative (midpoint $35, not $20)

**Sources:**
1. LEDsMaster, "How Much Do Street Lights Cost?" — LED-specific: $20-$50/year
   File: `sources/ledsmaster-street-light-costs.pdf`
2. CPS Lighting, "How Much Does a Street Light Cost?" (May 2024) — Generic: $50-$120/year
   File: `sources/cps-lighting-street-light-costs-2024.pdf`
   Note: Shows industry ranges can be higher, which makes our $35 estimate conservative

**Status:** ✅ VERIFIED

---

### Maintenance Savings: $4.90/light/year

**Claim:** Reduced maintenance costs from running LEDs at lower average power

**Baseline:** $35/year per LED streetlight
- Source: LEDsMaster, "How Much Do Street Lights Cost?"
- Midpoint of $20-$50 range for LED maintenance
- File: `sources/ledsmaster-street-light-costs.pdf`

**Logic:**
1. ~40% of LED maintenance costs are thermally-driven (driver failures, LED chip degradation, reactive repairs from premature component failure)
2. ~60% is non-thermal (scheduled inspections, cleaning, knockdowns/accidents, photocell issues)
3. Running at ~65% average power reduces thermal stress on components
4. We apply a conservative linear assumption: 35% power reduction → 35% reduction in thermally-driven failures

**Calculation:**
```
Thermally-driven portion: $35 × 0.40 = $14.00
Reduction from dimming:  $14.00 × 0.35 = $4.90/light/year
```

**Sources:**
1. LEDsMaster, "How Much Do Street Lights Cost?" — $35 baseline
   File: `sources/ledsmaster-street-light-costs.pdf`
2. OSRAM Opto Semiconductors, "Reliability and Lifetime of LEDs" Application Note, December 2013 — Thermal stress / Arrhenius relationship
   File: `sources/osram-led-reliability-lifetime-2013.pdf`

**Status:** 🔶 DERIVED

**Conservatism Note:** The linear assumption (35% power reduction = 35% thermal failure reduction) is conservative. The Arrhenius equation governing semiconductor reliability suggests exponential benefits from temperature reduction — actual savings may be higher.

**Unquantified Benefit:** Photometrics AI's software-based scheduling eliminates "daytime burn" failures caused by photocell malfunctions (lights stuck on during hot days, cooking the driver). This benefit is real but not dollarized in the $4.90 figure.

---

### Extension of Luminaire Life: $15.76/light/year

**Claim:** Delayed capital replacement saves $15.76 per streetlight per year

**Inputs:**
- L70 life rating: 50,000 hours (field-realistic estimate)
- Total replacement cost: $1,100 (LED $100 + installation $1,000)
- Operating hours: 4,100 hours/year
- Power reduction: 35% savings → ~65% average power
- Survival rate: 50% (only half of lights reach natural EOL)

**Logic:**
1. Running at ~65% average power reduces thermal stress on LED drivers and chips
2. Lower thermal stress extends lifespan (OSRAM Arrhenius relationship)
3. Conservative inverse-linear relationship: 65% power → 1/0.65 = 1.54× life extension
4. 50% survival rate accounts for lights replaced early due to knockdowns, technology upgrades, utility programs, etc.

**Calculation:**
```
Baseline lifespan:    50,000 ÷ 4,100 = 12.20 years
Annualized baseline:  $1,100 ÷ 12.20 = $90.16/year

Extended lifespan:    50,000 ÷ 0.65 = 76,923 hours
Extended years:       76,923 ÷ 4,100 = 18.76 years
Annualized extended:  $1,100 ÷ 18.76 = $58.64/year

Gross savings: $90.16 - $58.64 = $31.52/light/year
Adjusted for survival rate: $31.52 × 0.50 = $15.76/light/year
```

**Why 50,000 hours (not 100,000)?**
- 100,000 hours = 24+ years baseline — no one believes a streetlight stays up that long
- 50,000 hours = 12 years baseline, 19 years extended — realistic and defensible
- Field conditions differ from lab specs; 50,000 is conservative

**Why 50% survival rate?**
- Not all lights reach natural end-of-life
- Many replaced early due to: knockdowns/accidents, technology upgrades, utility replacement programs, vandalism
- 50% is a conservative estimate of lights that actually reach natural EOL

**Clean separation from Maintenance:**
| Category | What it covers |
|----------|----------------|
| **Maintenance ($4.90)** | Repairs during service life — driver replacements, reactive fixes, thermal-driven component failures |
| **Life Extension ($15.76)** | Delayed capital replacement — for the 50% of lights that reach natural EOL |

No double-counting between these categories.

**Sources:**
1. OSRAM, "Reliability and Lifetime of LEDs" Application Note, Dec 2013 — Thermal/Arrhenius relationship
   File: `sources/osram-led-reliability-lifetime-2013.pdf`
2. PG&E unmetered tariff — 4,100 operating hours/year

**Conservatism Note:** Inverse-linear model is conservative; Arrhenius suggests exponential benefits from temperature reduction — actual savings may be higher.

**Status:** 🔶 DERIVED

---

### Luminaire + Installation Cost: $1,100

**Claim:** Total replacement cost is $1,100 (LED $100 + installation $1,000)  
**Logic:** Industry standard assumption  
**Sources:**
- [NEED SOURCE]

**Status:** 🔴 PLACEHOLDER — Needs citation

---

### L70 Life Rating: 50,000 hours (default)

**Claim:** LED L70 life rating is 50,000 hours for financial calculations
**Logic:**
- Lab specs often cite 100,000 hours, but this implies 24+ year service life — unrealistic
- 50,000 hours = 12.2 years baseline service life — believable and defensible
- Field conditions differ from lab conditions; 50,000 is conservative

**Why not 100,000 hours?**
- 100,000 ÷ 4,100 hrs/yr = 24.4 years — no one believes a streetlight stays up 24 years
- Using 50,000 hours produces realistic 12-year baseline, 20-year extended timeframes

**Sources:**
- OSRAM: LED thermal stress / lifespan relationship
- Industry spec sheets typically show 50,000-100,000 hour range

**Status:** 🔶 DERIVED — Conservative field-realistic estimate

---

### Electric Rate: $0.13/kWh (national average)

**Claim:** National average electric rate is $0.13/kWh

**Source Data:**
- U.S. Energy Information Administration, Electric Power Monthly, Table 5.6.A
- "Average Price of Electricity to Ultimate Customers by End-Use Sector"
- **All Sectors, October 2025: 13.63¢/kWh**
- File: `sources/eia-electric-power-monthly-oct2025.pdf`
- URL: https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a

**Why "All Sectors" (not Commercial, Industrial, etc.)?**
- Streetlight ownership varies — municipalities, utilities, state DOTs
- No single EIA sector category fits all streetlight billing arrangements
- "All Sectors" is the standard national average cited in most analyses
- Most defensible as a blended rate across all customer types

**EIA Sector Options (October 2025):**
| Sector | Rate |
|--------|------|
| Residential | 17.98¢/kWh |
| Commercial | 13.41¢/kWh |
| Industrial | 8.65¢/kWh |
| Transportation | 13.57¢/kWh |
| **All Sectors** | **13.63¢/kWh** |

**Why use exact $0.1363?**
- Precision over conservatism — using exact EIA figure
- Consumption-weighted average reflects actual cost per kWh sold nationally
- States with lower rates consume more electricity (pulling average down)
- Lower-rate states have less incentive to optimize — not our primary market
- Customer calculations should still use their actual utility rate

**Status:** ✅ VERIFIED — EIA Electric Power Monthly, All Sectors, October 2025 (consumption-weighted)

---

## Safety & Crime

### Crime Reduction Value: $10.81/light/year (conservative)

**Claim:** Crime reduction value is $10.81 per streetlight per year (conservative estimate)

**Original Calculation:**
```
State/local crime spending 2017: $246.7B
US streetlights: 26.5M
Per streetlight: $246.7B / 26.5M = $9,309/light
Nighttime (45%) × outdoor (20%): $9,309 × 0.45 × 0.20 = $837.90
1% reduction: $837.90 × 0.01 = $8.38
Inflation (29% since 2017): $8.38 × 1.29 = $10.81
```

---

### Verified: LAPD Crime Data Analysis (2010-2019)

**Analysis conducted:** 2,133,137 crime records from LAPD spanning 2010-2019

**Methodology:**
1. Used astronomical sun position calculations (nautical twilight threshold: sun 6° below horizon)
2. Determined when streetlights would be ON for each crime based on lat/long/date/time
3. Classified premises by whether municipal street lighting affects visibility (STREET=YES, PARKING LOT=NO, etc.)

**Empirical Results:**
| Metric | Count | Percentage |
|--------|-------|------------|
| Total crimes analyzed | 2,133,137 | 100% |
| **Streetlights ON** (nautical twilight or darker) | 835,580 | **39.2%** |
| **Lighting-influenced locations** | 773,243 | **36.2%** |
| **BOTH (treatable universe)** | 364,568 | **17.1%** |

**Twilight Phase Distribution:**
| Phase | Count | Percentage |
|-------|-------|------------|
| Day | 1,214,096 | 56.9% |
| Civil Twilight | 82,553 | 3.9% |
| Nautical Twilight | 79,261 | 3.7% |
| Astronomical Twilight | 81,367 | 3.8% |
| Night | 674,952 | 31.7% |

**Key Finding:** Of nighttime crimes (when streetlights are ON), **43.6%** occurred at lighting-influenced locations.

**Top Lighting-Influenced Premises (streetlights ON):**
1. STREET: 231,209
2. SIDEWALK: 45,840
3. VEHICLE, PASSENGER/TRUCK: 39,342
4. DRIVEWAY: 23,467
5. ALLEY: 6,184

---

### Updated Calculation Using Verified Data

**Using empirical 17.1% (vs original 9%):**
```
State/local crime spending 2017: $246.7B
Treatable universe: 17.1% (streetlights ON + lighting-influenced)
Per streetlight: $246.7B × 0.171 / 26.5M = $1,592.60
1% reduction: $1,592.60 × 0.01 = $15.93
Inflation (29% since 2017): $15.93 × 1.29 = $20.55
```

**Comparison:**
| Assumption | Treatable % | Value/light/year |
|------------|-------------|------------------|
| Original (45% × 20%) | 9.0% | $10.81 |
| **Empirical (LAPD)** | **17.1%** | **$20.55** |

---

### Why Keep $10.81 as Primary Figure?

1. **Los Angeles bias:** LAPD data is urban; may not represent national mix
2. **Conservative credibility:** Lower figure is easier to defend in proposals
3. **Upside optionality:** Can disclose higher empirical value as "validated upside"
4. **Source alignment:** Maintains consistency with published BJS methodology

**Recommendation:** Continue using $10.81 as conservative baseline; cite LAPD analysis as supporting evidence that actual value may be 2× higher.

---

### Sources

**Verified:**
1. Bureau of Justice Statistics, "Justice Expenditure and Employment in the United States, 2017" (NCJ 256093, July 2021)
   - **Table 1:** State police + corrections + judicial ($93.1B) + Local police + corrections + judicial ($153.6B) = **$246.7B**
   - File: `sources/bjs-justice-expenditures-employment-2017.pdf`
   - URL: https://bjs.ojp.gov/sites/g/files/xyckuh236/files/media/document/jeeus17.pdf

2. TheSleepJudge: "Crime and the Clock: A Study of 840,000 Police Incidents from 10 U.S. Cities" (2017)
   - 45% of crimes occur at night (10 PM - 6 AM)
   - Based on 840,000 police incidents from 10 US cities
   - File: `sources/thesleepjudge-crime-clock-study-2017.pdf`

3. **Los Angeles Police Department, "Crime Data from 2010 to 2019"**
   - Source: LA Open Data Portal
   - URL: https://data.lacity.org/Public-Safety/Crime-Data-from-2010-to-2019/63jg-8b9z
   - Records: 2.13M crime incidents (2010-2019)
   - License: CC0 (Public Domain)
   - File: `sources/lapd-crime-data-2010-2019-open-data-portal.pdf`
   - Analysis results: 39.2% streetlights ON, 17.1% treatable universe
   - Methodology: Astronomical sun position (nautical twilight = sun 6° below horizon) + premises classification
   - Analysis tool: `tool-sun-phase` repository

**Status:** ✅ VERIFIED — Crime timing backed by official LAPD data (2.13M records) with reproducible methodology

---

### Methodology Limitation: Equal Crime Weighting

**Acknowledged simplification:** This calculation treats all crimes equally by dividing total justice spending by crime count. In reality, crime costs vary dramatically:

| Crime Type | Approximate Cost | Notes |
|------------|------------------|-------|
| Murder | $1M+ | Investigation, prosecution, lengthy incarceration |
| Aggravated assault | $50K-100K | Medical, legal, incarceration |
| Burglary | $5K-20K | Investigation, prosecution, shorter sentences |
| Theft | $1K-5K | Often not prosecuted |

**Implication:** If violent crimes (higher cost) occur disproportionately at night, our figure underestimates the value. If violent crimes occur disproportionately during the day, our figure overestimates.

**Why we don't weight by severity:**
1. BJS spending data is aggregate, not per-crime-type
2. LAPD data would need to be re-analyzed by crime severity
3. The 17.1% treatable universe already filters to outdoor/nighttime crimes
4. Conservative baseline is more defensible than complex weighting

**If challenged:** Acknowledge the simplification. Note that street-level crimes (robbery, assault, vehicle theft) that occur in public ROW tend to be more serious than daytime retail theft — suggesting our figure may actually be conservative.

---

### Traffic Incident Reduction Value: $7.82/light/year

**Claim:** Traffic incident reduction value is $7.82 per streetlight per year

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
FHWA states: "The number of fatal crashes occurring in daylight is about the same as those that occur in darkness." This supports the 50% assumption. Additionally, "the nighttime fatality rate is three times the daytime rate because only 25 percent of vehicle miles traveled (VMT) occur at night" — indicating darkness crashes are disproportionately severe.

**Why 3% improvement?**
FHWA documents that lighting can reduce crashes by 28-42% (see below). However, these figures are for **installing lighting where there was none**. Photometrics AI optimizes **existing** lighting through:
- Faster outage detection → lights restored sooner
- Maintained luminaire output → preventing degradation
- Consistent operation → ensuring lights are ON when expected

The 3% assumption says: "Of the 28% benefit that proper lighting provides, we capture ~10% through better management." This is deliberately conservative.

**Sources:**
1. NHTSA, "The Economic and Societal Impact of Motor Vehicle Crashes, 2019" (DOT HS 813 403)
   - Table 15-5: Source of Payment of Economic Costs by Cost Category
   - State/Locality: $10,948M (3.22% of $339.809B total)
   - File: `sources/nhtsa-crash-costs-2019.pdf`

2. FHWA Proven Safety Countermeasures: Lighting (FHWA-SA-21-050)
   - 28% reduction for nighttime injury crashes on highways
   - 33-38% reduction for nighttime crashes at intersections
   - 42% reduction for nighttime pedestrian crashes at intersections
   - Source: Elvik & Vaa, "Handbook of Road Safety Measures" (2004)
   - File: `sources/fhwa-lighting-safety-countermeasure.pdf`

3. BLS CPI All Urban Consumers (CUUR0000SA0)
   - December 2019: 256.974
   - December 2025: 324.054
   - Inflation: 26.1%
   - API: `api.bls.gov/publicAPI/v2/timeseries/data/CUUR0000SA0`

**Status:** 🔶 DERIVED — All inputs verified from authoritative sources

---

### FHWA Crash Reduction Percentages

**Claim:** Lighting improvements reduce crashes by specific percentages  
**Data:**
- 42% reduction for nighttime injury pedestrian crashes at intersections
- 33-38% reduction for nighttime crashes at rural and urban intersections
- 28% reduction for nighttime injury crashes on rural and urban highways

**Sources:**
- fhwa-lighting-safety-countermeasure.pdf (FHWA-SA-21-050)
- Original: Elvik, R. and Vaa, T., "Handbook of Road Safety Measures" (2004)

**Status:** ✅ VERIFIED

---

## Demand Response

### DSM Revenue: $2.02/light/year (California)

**Claim:** Demand-side management revenue is $2.02 per light per year

**Value Attribution:** DSM revenue can be categorized as:
- **Municipal benefit** — The municipality receives the DR payments directly
- **Utility benefit** — The utility gains grid flexibility and avoided capacity costs
- **Quality of life benefit** — Residents benefit from more stable rates and reduced blackout risk

**Logic (Stockton example, 20,000 lights):**

Two California DR programs that can be enrolled simultaneously:

1. **Capacity Bidding Program (CBP)** — Day-ahead planned events
   - Capacity payments for committed load reduction availability
   - Energy payments for actual kWh reduced during events

2. **Emergency Load Reduction Program (ELRP)** — Grid emergency events
   - Energy-only payments at premium rate
   - No penalties for non-performance

**Assumptions:**
| Parameter | Value | Notes |
|-----------|-------|-------|
| Lights | 20,000 | Example deployment |
| Average wattage | 50W | Standard LED assumption |
| DR reduction capability | 75% | Aggressive dimming to 25% power during events |
| Operating hours | 4,100/year | PG&E LS-2 tariff |
| Event availability | 46.8% | 4,100 ÷ 8,766 hours (% of time lights are on) |
| CBP events | 20/year × 3 hrs | Maximum per utility program |
| ELRP events | 5/year × 3 hrs | Maximum per utility program |

**Payment Rates:**
| Program | Rate | Status | Source |
|---------|------|--------|--------|
| CBP Capacity | $79/kW/year | ✅ VERIFIED | SCE Schedule CBP (Feb 2024) |
| CBP Energy | $0.10/kWh | ⚠️ ESTIMATE | Historical ~$0.08; using conservative $0.10 |
| ELRP | $2.00/kWh | ✅ VERIFIED | CPUC ELRP program documentation |

**Calculation:**
```
Committed capacity: 20,000 × 50W × 75% × 46.8% = 351 kW

CBP Capacity Payment:
  351 kW × $79/kW/year = $27,729/year

CBP Energy Payment:
  20,000 × 50W × 75% × 3 hrs × 20 events × 46.8% = 21,060 kWh
  21,060 kWh × $0.10/kWh = $2,106/year

CBP Total: $27,729 + $2,106 = $29,835/year

ELRP Payment:
  20,000 × 50W × 75% × 3 hrs × 5 events × 46.8% = 5,265 kWh
  5,265 kWh × $2.00/kWh = $10,530/year

Grand Total: $29,835 + $10,530 = $40,365/year
Per light: $40,365 / 20,000 = $2.02/light/year
```

**Why 75% DR reduction (not 35%)?**
- Normal operation: 35% energy savings (~65% average power) — optimized for lighting quality
- DR events: 75% reduction (25% power) — aggressive dimming for short emergency periods
- DR baseline compares against 100% power, not already-dimmed levels
- Both measurements use the same baseline (LED at full power)

**Why 46.8% event availability?**
- DR events can only generate revenue when lights are already on (baseline exists)
- If event occurs during daylight when lights are off, no reduction can be measured
- 4,100 operating hours ÷ 8,766 total hours = 46.8%

**Sources:**
1. SCE Schedule CBP Tariff, Cal. PUC Sheet No. 87373-E, Effective Feb 15, 2024
   - CBP Capacity rates by month: May $4.59, June $6.89, July $23.30, Aug $27.19, Sept $14.54, Oct $2.69
   - Season total: ~$79/kW/year
   - File: `sources/sce-cbp-tariff-2024.pdf`
   - URL: https://www.sce.com/sites/default/files/custom-files/ELECTRIC_SCHEDULES_CBP.pdf

2. CPUC Emergency Load Reduction Program (ELRP)
   - Non-residential rate: $2.00/kWh
   - Program duration: May-Oct, 4-9 PM, 1-5 hours per event, up to 60 hours/year
   - No penalties for non-performance
   - Program authorized through 2027
   - File: `sources/cpuc-elrp-program-2024.pdf`
   - URL: https://www.cpuc.ca.gov/industries-and-topics/electrical-energy/electric-costs/demand-response-dr/emergency-load-reduction-program

3. Internal analysis: "Street Lighting for Demand Response - Stockton CA"
   - File: `sources/streetlighting-demand-response-stockton-ca.pdf`

**Geographic Limitation:** This calculation is California-specific (PG&E/SCE/SDG&E territories). Other states may have different DR programs with different rates, or no programs at all.

**Status:** 🔶 DERIVED — California-specific; verified program rates, estimated event counts

---

### Peak Reduction: 14-28 kW per 1,000 luminaires

**Claim:** Peak reduction capability is 14-28 kW per 1,000 luminaires  
**Logic:**
```
1,000 lights × 50W × 75% DR capability = 37.5 kW max
Accounting for event availability (46.8%): 37.5 × 0.468 = 17.6 kW
Range accounts for different scenarios and assumptions
```

**Sources:**
- Internal engineering analysis

**Status:** 🔶 DERIVED — Needs validation from actual deployment data

---

## Technical Performance

### Processing Speed: 2,000 lights in 3-5 minutes

**Claim:** System processes 2,000 lights in 3-5 minutes  
**Logic:** Internal benchmarking  
**Sources:**
- Internal testing

**Status:** ⚠️ ESTIMATE — Based on current system; may vary with infrastructure

---

### Lighting Compliance: 91-97%

**Claim:** Photometrics AI achieves 91-97% lighting standard compliance  
**Logic:** From pilot results and modeling  
**Sources:**
- Internal analysis / pilot data
- [NEED]: Published pilot results

**Status:** ⚠️ ESTIMATE — Range from modeling; needs pilot validation

---

## Items Requiring Source Research

**Priority HIGH — Used in sales/proposals:**
1. 60M US streetlights (vs 26.5M DOE figure)
2. ~~$35/light/year baseline maintenance~~ ✅ RESOLVED — LEDsMaster source ($20-$50 range, $35 midpoint)
3. $1,100 luminaire + installation cost
4. Average 50W LED wattage
5. Market penetration source data (23M connected 2022, 63.8M projected 2027)

**Priority MEDIUM — Market sizing:**
6. 374M global streetlights by 2029
7. ~~22.7% CAGR reconciliation~~ ✅ RESOLVED — Use 30% CAGR from DataM Intelligence (Jan 2026)
8. GTM penetration numbers need update (old data points don't match current CAGR)

**Priority LOW — Supporting assumptions:**
9. ~~45% crimes at night assumption~~ ✅ RESOLVED — TheSleepJudge study (45%) + LAPD analysis (39.2%)
10. ~~20% crimes influenced by lighting assumption~~ ✅ RESOLVED — LAPD analysis shows 43.6% of nighttime crimes at lighting-influenced locations (combined 17.1% treatable universe)
11. ~~50% crashes in darkness assumption~~ ✅ RESOLVED — FHWA: "The number of fatal crashes occurring in daylight is about the same as those that occur in darkness"

---

## Data Reconciliation Needed

### GTM vs Other Sources: Connected Streetlights

| Year | GTM File | Other Sources |
|------|----------|---------------|
| 2019 | 10.0M (3.2%) | — |
| 2022 | — | 23M (7.2% of 320M) |
| 2025 | 41.2M (12%) | — |
| 2027 | — | 63.8M (~20%) |
| 2030 | 119.6M (32%) | — |

**Action:** Identify the source for each dataset and determine which to use as primary.

### US Streetlight Count

- DOE conservative: 26.5M
- National impact calc: 60M

**Action:** Determine source for 60M figure or switch national impact to 26.5M with adjusted claims.
