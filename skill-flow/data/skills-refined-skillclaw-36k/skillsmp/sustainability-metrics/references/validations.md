# Sustainability Metrics - Validations

## ESG Claim Without Supporting Data

### **Id**
unsubstantiated-claim
### **Severity**
error
### **Type**
regex
### **Pattern**
  - sustainable|eco-friendly|green(?!.*metric|data|evidence)
  - committed to|pledge(?!.*target|timeline)
### **Message**
ESG claims must be backed by measurable data.
### **Fix Action**
Add: specific metric, timeframe, baseline, and verification status.
### **Applies To**
  - **/*.py
  - **/*.md

## Materiality Without Impact Dimension

### **Id**
single-materiality-only
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - materiality.*financial(?!.*impact|society)
  - material.*=.*financial_score(?!.*impact)
### **Message**
CSRD requires double materiality (financial AND impact).
### **Fix Action**
Add: impact_score = assess_impact_on_society(topic)
### **Applies To**
  - **/*.py

## Metric Without Methodology Documentation

### **Id**
metric-no-methodology
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - esg_metric.*=.*(?!.*methodology|source|boundary)
  - report.*value(?!.*method)
### **Message**
Document metric methodology for comparability and audit.
### **Fix Action**
Add: methodology='GRI 305-1', boundary='operational control'
### **Applies To**
  - **/*.py

## Target Without Baseline Year

### **Id**
target-no-baseline
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - target.*=.*percent.*reduction(?!.*baseline|base_year)
  - reduce.*by.*20(?!.*from|vs|versus)
### **Message**
Targets must specify baseline year for meaningful comparison.
### **Fix Action**
Add: target='30% reduction vs 2020 baseline'
### **Applies To**
  - **/*.py

## GHG Reporting Without Scope 3

### **Id**
no-scope3-coverage
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - scope_?1.*scope_?2(?!.*scope_?3)
  - emissions.*=.*direct.*indirect(?!.*value.chain)
### **Message**
Scope 3 typically 70-90% of footprint. Include for completeness.
### **Fix Action**
Add: scope3_emissions = calculate_value_chain_emissions()
### **Applies To**
  - **/*.py

## TCFD Without All Pillars

### **Id**
tcfd-incomplete
### **Severity**
info
### **Type**
regex
### **Pattern**
  - tcfd.*governance(?!.*strategy|risk|metric)
  - climate_risk(?!.*scenario|financial)
### **Message**
TCFD requires all four pillars: governance, strategy, risk management, metrics.
### **Fix Action**
Include: tcfd_disclosure = {governance, strategy, risk_mgmt, metrics_targets}
### **Applies To**
  - **/*.py

## SDG Alignment Without Quantification

### **Id**
sdg-no-evidence
### **Severity**
info
### **Type**
regex
### **Pattern**
  - sdg.*contribut(?!.*measure|quantif|impact)
  - align.*sdg(?!.*metric|indicator)
### **Message**
SDG claims should be quantified with specific indicators.
### **Fix Action**
Add: sdg13_contribution = {metric: 'tCO2e avoided', value: 50000}
### **Applies To**
  - **/*.py

## Net Zero Relying on Offsets

### **Id**
offset-heavy-net-zero
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - net.zero.*offset(?!.*residual|<10%)
  - carbon.neutral.*credit(?!.*reduc)
### **Message**
SBTi requires 90%+ actual reduction before offsets.
### **Fix Action**
Add: reduction_plan = {...}; offsets_for_residual_only()
### **Applies To**
  - **/*.py

## Metric Without Verification Status

### **Id**
no-verification-flag
### **Severity**
info
### **Type**
regex
### **Pattern**
  - metric.*=.*value(?!.*verified|assured|audited)
  - report.*emissions(?!.*assurance)
### **Message**
Flag verification status for key metrics.
### **Fix Action**
Add: verified=True, assurance_provider='Auditor Name', standard='ISAE 3410'
### **Applies To**
  - **/*.py

## Optimizing for ESG Ratings Over Impact

### **Id**
rating-gaming
### **Severity**
info
### **Type**
regex
### **Pattern**
  - msci.*score|sustainalytics.*rating(?!.*actual.*impact)
  - improve.*rating(?!.*performance)
### **Message**
Focus on actual ESG performance, not rating optimization.
### **Fix Action**
Track: actual_impact alongside rating_score
### **Applies To**
  - **/*.py

## Selective Metric Reporting

### **Id**
cherry-pick-metrics
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - if.*positive.*report(?!.*negative)
  - exclude.*negative|hide.*poor
### **Message**
Report all material metrics regardless of performance.
### **Fix Action**
Report: all_material_metrics including challenges
### **Applies To**
  - **/*.py

## Metrics Without Historical Trend

### **Id**
no-trend-analysis
### **Severity**
info
### **Type**
regex
### **Pattern**
  - current_year.*only(?!.*trend|history)
  - report.*=.*\{.*2023(?!.*2022|trend)
### **Message**
Include historical trend for context (3-5 years).
### **Fix Action**
Add: trend = [value_2019, value_2020, value_2021, value_2022, value_2023]
### **Applies To**
  - **/*.py