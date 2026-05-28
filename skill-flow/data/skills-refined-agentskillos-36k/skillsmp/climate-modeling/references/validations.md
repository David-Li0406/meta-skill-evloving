# Climate Modeling - Validations

## Single Climate Model for Projections

### **Id**
single-model-projection
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - load.*model.*=.*['"][A-Z].*['"].*ssp(?!.*ensemble|multi)
  - cmip6.*model\s*=\s*['"][A-Z](?!.*for.*in)
### **Message**
Use multi-model ensemble for projections, not single model.
### **Fix Action**
Load ensemble: models = ['CESM2', 'GFDL-ESM4', ...]; ensemble = load_ensemble(models)
### **Applies To**
  - **/*.py

## Raw Model Output for Impact Analysis

### **Id**
no-bias-correction
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - impact.*=.*model_data(?!.*bias|correct|adjust)
  - load_cmip.*\.sel\(.*\)(?!.*bias_correct)
### **Message**
Apply bias correction before using model data for impacts.
### **Fix Action**
Apply correction: corrected = quantile_mapping(model, obs)
### **Applies To**
  - **/*.py

## Scenario Presented as Prediction

### **Id**
scenario-as-prediction
### **Severity**
info
### **Type**
regex
### **Pattern**
  - will\s+be|will\s+reach.*ssp(?!.*if|scenario|under)
  - future.*=.*(?!.*scenario|ssp.*:)
### **Message**
SSP scenarios are 'what-if', not predictions. Use conditional language.
### **Fix Action**
Say 'Under SSP2-4.5...' not 'Temperature will be...'
### **Applies To**
  - **/*.py

## Combining Data Without Calendar Check

### **Id**
no-calendar-check
### **Severity**
info
### **Type**
regex
### **Pattern**
  - concat.*model.*dim\s*=\s*['"]model['"](?!.*calendar)
  - merge.*cmip(?!.*convert_calendar)
### **Message**
Check calendar compatibility before combining climate datasets.
### **Fix Action**
Check: ds.time.dt.calendar; convert if needed: ds.convert_calendar()
### **Applies To**
  - **/*.py

## Point Estimate Without Uncertainty Range

### **Id**
no-uncertainty-range
### **Severity**
info
### **Type**
regex
### **Pattern**
  - print.*mean.*(?!.*range|std|p10|p90|uncertainty)
  - result\s*=.*\.mean\(.*model.*\)(?!.*std|quantile)
### **Message**
Report uncertainty range, not just ensemble mean.
### **Fix Action**
Report range: f'{mean:.1f}°C (range: {p10:.1f} to {p90:.1f})'
### **Applies To**
  - **/*.py

## Hardcoded Baseline Period

### **Id**
hardcoded-baseline
### **Severity**
info
### **Type**
regex
### **Pattern**
  - baseline.*=.*['"](19|20)\d{2}.*(?!.*config|param)
  - sel.*time=slice\(['"]19\d{2}
### **Message**
Make baseline period configurable for different applications.
### **Fix Action**
Accept parameter: baseline_period = ('1981', '2010')
### **Applies To**
  - **/*.py

## Annual Mean for Extreme Event Analysis

### **Id**
annual-for-extremes
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - annual.*mean.*extreme|extreme.*annual.*mean
  - groupby.*year.*mean.*heat|heat.*resample.*Y.*mean
### **Message**
Use daily data for extreme event analysis, not annual means.
### **Fix Action**
Use daily: extremes = (daily_data > threshold).groupby('time.year').sum()
### **Applies To**
  - **/*.py

## Missing Model Agreement Assessment

### **Id**
no-model-agreement
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ensemble.*mean(?!.*agree|robust|sign)
### **Message**
Assess model agreement on direction of change.
### **Fix Action**
Check: agreement = (ensemble > 0).mean(dim='model')
### **Applies To**
  - **/*.py

## Bilinear Interpolation of Precipitation

### **Id**
interpolate-precipitation
### **Severity**
info
### **Type**
regex
### **Pattern**
  - interp.*precip.*bilinear|precip.*interp\(
### **Message**
Use conservative remapping for precipitation to preserve totals.
### **Fix Action**
Use conservative: regridder = xe.Regridder(ds, target, 'conservative')
### **Applies To**
  - **/*.py