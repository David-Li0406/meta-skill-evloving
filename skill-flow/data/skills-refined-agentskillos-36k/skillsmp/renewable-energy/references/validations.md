# Renewable Energy - Validations

## Using STC Power Without Temperature Correction

### **Id**
stc-power-only
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - power\s*=.*rated_power\s*\*\s*irradiance(?!.*temp)
  - p_stc\s*\*\s*ghi(?!.*cell_temp|derate)
### **Message**
Apply temperature derating to PV power calculations.
### **Fix Action**
Add: power *= (1 + temp_coeff * (cell_temp - 25))
### **Applies To**
  - **/*.py

## Wind Resource From Single Year

### **Id**
single-year-wind
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - wind.*=.*load.*20\d{2}(?!.*20\d{2}|range|multi)
### **Message**
Use 10+ years of wind data for reliable resource assessment.
### **Fix Action**
Load multi-year: wind_data = load_data('2010-2023_wind.csv')
### **Applies To**
  - **/*.py

## Wind Farm Without Wake Losses

### **Id**
no-wake-model
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - farm_power\s*=\s*n_turbines\s*\*\s*turbine_power(?!.*wake)
  - total.*=.*sum.*turbine(?!.*wake|deficit)
### **Message**
Model wake losses for wind farms (10-20% typical).
### **Fix Action**
Apply wake model: farm_power *= (1 - wake_loss_factor)
### **Applies To**
  - **/*.py

## Battery Assumed 100% Efficient

### **Id**
battery-100-efficiency
### **Severity**
info
### **Type**
regex
### **Pattern**
  - energy_out\s*=\s*energy_in(?!.*eff)
  - storage.*charge.*discharge(?!.*loss|eff)
### **Message**
Battery round-trip efficiency is 85-95%, not 100%.
### **Fix Action**
Apply efficiency: energy_out = energy_in * efficiency_rt
### **Applies To**
  - **/*.py

## PV System Without Loss Factors

### **Id**
no-losses-pv
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ac_power\s*=\s*dc_power(?!.*loss|derate|eff)
  - production\s*=.*irradiance.*area(?!.*loss)
### **Message**
Apply PV system losses (soiling, wiring, inverter, etc.).
### **Fix Action**
Apply losses: ac_power = dc_power * (1 - total_losses)
### **Applies To**
  - **/*.py

## Wind Speed Not Extrapolated to Hub Height

### **Id**
hub-height-not-adjusted
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - wind_speed.*10m|10.*meter.*wind(?!.*extrap|hub|height)
### **Message**
Extrapolate wind speed from measurement height to hub height.
### **Fix Action**
Use log law: v_hub = v_meas * log(hub_height/z0) / log(meas_height/z0)
### **Applies To**
  - **/*.py

## Capacity Factor Assumed Not Calculated

### **Id**
capacity-factor-assumed
### **Severity**
info
### **Type**
regex
### **Pattern**
  - capacity_factor\s*=\s*0\.\d+(?!.*calculat|simulat)
### **Message**
Calculate capacity factor from site-specific resource data.
### **Fix Action**
Simulate: cf = sum(hourly_power) / (rated_power * 8760)
### **Applies To**
  - **/*.py

## Revenue Without Curtailment Consideration

### **Id**
no-curtailment
### **Severity**
info
### **Type**
regex
### **Pattern**
  - revenue\s*=.*production\s*\*\s*price(?!.*curtail)
### **Message**
Consider curtailment risk in high renewable grids.
### **Fix Action**
Adjust: revenue = production * (1 - curtailment_rate) * price
### **Applies To**
  - **/*.py

## Fixed Inverter Efficiency

### **Id**
fixed-inverter-efficiency
### **Severity**
info
### **Type**
regex
### **Pattern**
  - inverter_eff\s*=\s*0\.9\d(?!.*curve|loading)
### **Message**
Inverter efficiency varies with loading. Use efficiency curve.
### **Fix Action**
Model curve: eff = f(loading) where loading = power / rated_power
### **Applies To**
  - **/*.py