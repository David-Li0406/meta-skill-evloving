# Carbon Accounting - Validations

## Emissions Without Scope Classification

### **Id**
missing-scope-classification
### **Severity**
error
### **Type**
regex
### **Pattern**
  - emissions\s*=.*(?!scope_1|scope_2|scope_3|scope1|scope2|scope3)
  - co2e\s*=.*(?!.*scope)
### **Message**
All emissions must be classified by GHG Protocol scope (1, 2, or 3).
### **Fix Action**
Add scope: emissions_scope1['source'] = value or use structured inventory.
### **Applies To**
  - **/*.py

## Hardcoded Emission Factor Without Source

### **Id**
hardcoded-emission-factor
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ef\s*=\s*\d+\.\d+(?!.*source|epa|defra|ecoinvent)
  - emission_factor\s*=\s*\d+(?!.*#)
### **Message**
Document emission factor sources for audit trail.
### **Fix Action**
Add source: ef = 0.42  # EPA 2023, kg CO2/kWh, US average grid
### **Applies To**
  - **/*.py

## CH4 or N2O Without GWP Conversion

### **Id**
missing-gwp
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ch4.*=.*(?!.*gwp|co2e|\*\s*2[78])
  - n2o.*=.*(?!.*gwp|co2e|\*\s*2[67])
  - methane.*=.*(?!.*convert|co2e)
### **Message**
Convert CH4 and N2O to CO2e using GWP values.
### **Fix Action**
Apply GWP: co2e = co2 + ch4 * 27.9 + n2o * 273  # AR6 100-year
### **Applies To**
  - **/*.py

## Scope 2 Without Dual Reporting

### **Id**
scope2-single-method
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - scope_?2\s*=(?!.*location|market)
  - electricity_emissions\s*=(?!.*dual|both)
### **Message**
GHG Protocol requires dual Scope 2 reporting (location and market-based).
### **Fix Action**
Report both: scope2_location = mwh * grid_ef; scope2_market = mwh * contract_ef
### **Applies To**
  - **/*.py

## REC Applied Without Quality Check

### **Id**
rec-no-validation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - rec.*applied|recs.*cover(?!.*valid|vintage|region)
  - market_based\s*=\s*0(?!.*verified|certified)
### **Message**
Validate REC quality criteria before claiming zero market-based.
### **Fix Action**
Check: vintage matches year, region matches consumption, registry recognized.
### **Applies To**
  - **/*.py

## Scope 3 With Limited Categories

### **Id**
scope3-missing-categories
### **Severity**
info
### **Type**
regex
### **Pattern**
  - scope_?3\s*=.*travel.*(?!.*purchased|goods|capital)
  - scope3.*=.*\{.*\}(?!.*screen|categor)
### **Message**
Ensure all 15 Scope 3 categories are screened, not just easy ones.
### **Fix Action**
Screen all categories: purchased goods, capital goods, transport, waste, travel, commuting...
### **Applies To**
  - **/*.py

## Emissions Without Organizational Boundary

### **Id**
no-boundary-definition
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - inventory\s*=.*(?!.*boundary|operational|equity|financial)
  - total_emissions\s*=(?!.*consolidat)
### **Message**
Define organizational boundary approach before calculating inventory.
### **Fix Action**
Define: boundary = 'operational_control' or 'equity_share' or 'financial_control'
### **Applies To**
  - **/*.py

## Baseline Without Recalculation Policy

### **Id**
baseline-no-recalculation-policy
### **Severity**
info
### **Type**
regex
### **Pattern**
  - baseline\s*=.*(?!.*recalc|adjust|policy)
  - base_year.*=.*20\d{2}(?!.*trigger)
### **Message**
Document baseline recalculation policy and triggers.
### **Fix Action**
Define policy: recalc if >5% change from M&A, methodology change, or error correction.
### **Applies To**
  - **/*.py

## Intensity Metric Without Normalization

### **Id**
intensity-metric-undefined
### **Severity**
info
### **Type**
regex
### **Pattern**
  - intensity\s*=\s*emissions(?!.*revenue|production|employee|sqft)
  - per_unit.*=(?!.*normali)
### **Message**
Define intensity denominator clearly for comparability.
### **Fix Action**
Specify: intensity = emissions / revenue_million  # tCO2e per $M revenue
### **Applies To**
  - **/*.py

## SBTi Target Without Pathway Validation

### **Id**
sbti-target-not-validated
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - target.*=.*percent.*reduction(?!.*sbti|pathway|1\.5|2)
  - reduction_target\s*=\s*0\.\d+(?!.*science|align)
### **Message**
Validate that reduction targets align with SBTi-approved pathways.
### **Fix Action**
Validate: 1.5C requires 4.2% annual reduction; well-below 2C requires 2.5%.
### **Applies To**
  - **/*.py

## Emissions Reported Without Uncertainty

### **Id**
missing-uncertainty
### **Severity**
info
### **Type**
regex
### **Pattern**
  - print.*emissions.*(?!.*uncertainty|range|±)
  - report.*=.*total(?!.*uncertain|confidence)
### **Message**
Report uncertainty ranges, especially for Scope 3 estimates.
### **Fix Action**
Add uncertainty: total = 50000 ± 15% (Scope 3 estimates based on spend data).
### **Applies To**
  - **/*.py

## Spend-Based Scope 3 Without Inflation Adjustment

### **Id**
spend-based-no-deflator
### **Severity**
info
### **Type**
regex
### **Pattern**
  - spend.*\*.*ef(?!.*deflat|real|adjust)
  - procurement.*emission(?!.*inflat)
### **Message**
Adjust spend data for inflation when using economic emission factors.
### **Fix Action**
Deflate to base year: real_spend = nominal_spend / cpi_deflator
### **Applies To**
  - **/*.py