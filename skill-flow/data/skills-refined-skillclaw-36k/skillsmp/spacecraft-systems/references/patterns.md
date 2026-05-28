# Spacecraft Systems

## Patterns


---
  #### **Name**
power_budget_analysis
  #### **Steps**
    - List all power loads by mode
    - Calculate duty cycles
    - Determine peak and average power
    - Size solar array for worst case
    - Size battery for eclipse
    - Verify 20%+ margin

---
  #### **Name**
link_budget_analysis
  #### **Steps**
    - Define data rate requirement
    - Calculate EIRP
    - Compute path loss for max range
    - Add atmospheric and rain losses
    - Calculate received power
    - Verify 3+ dB margin

---
  #### **Name**
thermal_analysis
  #### **Steps**
    - Create thermal node model
    - Define hot and cold cases
    - Apply heat loads and environment
    - Run transient analysis
    - Verify all components in limits
    - Size heaters for cold case

## Anti-Patterns


---
  #### **Name**
single_string_adcs
  #### **Problem**
Any sensor failure loses attitude control
  #### **Solution**
Redundant sensors and fallback modes

---
  #### **Name**
battery_too_small
  #### **Problem**
Deep discharge shortens battery life
  #### **Solution**
Size for 30% DOD maximum

---
  #### **Name**
cold_side_facing_sun
  #### **Problem**
Thermal control impossible
  #### **Solution**
Define attitude constraints for thermal

---
  #### **Name**
undersized_comm_link
  #### **Problem**
Cannot download mission data
  #### **Solution**
Design for worst-case geometry

---
  #### **Name**
no_safe_mode
  #### **Problem**
Anomaly becomes mission loss
  #### **Solution**
Autonomous safe mode design