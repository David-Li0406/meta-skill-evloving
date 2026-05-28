# Spacecraft Systems - Validations

## Reaction Wheels Without Redundancy

### **Id**
no-wheel-redundancy
### **Severity**
error
### **Type**
regex
### **Pattern**
  - wheels\s*=\s*3(?!.*redundan)
  - n_wheels.*=.*3[^0-9]
  - ReactionWheel.*\[.*\].*len.*==.*3
### **Message**
Only 3 reaction wheels - no redundancy for 3-axis control
### **Fix Action**
Use 4 wheels minimum for 3-axis control with redundancy
### **Applies To**
  - **/*.py

## Missing Momentum Dumping Strategy

### **Id**
no-momentum-dumping
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - reaction_wheel(?!.*desaturat|dump|unload)
  - wheel_momentum(?!.*limit|max)
  - adcs_design(?!.*magnetorquer|thruster)
### **Message**
ADCS design may lack momentum dumping capability
### **Fix Action**
Plan magnetorquer or thruster desaturation
### **Applies To**
  - **/*.py

## Battery DOD Too High

### **Id**
high-dod-battery
### **Severity**
error
### **Type**
regex
### **Pattern**
  - dod.*=.*0\.[7-9]
  - depth_of_discharge.*>.*0\.5
  - battery.*80.*percent
### **Message**
Battery DOD > 50% significantly reduces cycle life
### **Fix Action**
Design for 30% DOD for long mission life
### **Applies To**
  - **/*.py

## Power Sizing Without EOL Degradation

### **Id**
no-eol-degradation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - solar.*power(?!.*degradation|eol)
  - array.*output(?!.*years)
  - panel_power.*=(?!.*\*.*0\.[89])
### **Message**
Solar array sizing may not account for EOL degradation
### **Fix Action**
Apply 2-3%/year degradation for mission lifetime
### **Applies To**
  - **/*.py

## Missing Safe Mode Definition

### **Id**
no-safe-mode
### **Severity**
error
### **Type**
regex
### **Pattern**
  - adcs.*mode(?!.*safe)
  - spacecraft.*state(?!.*safe)
  - fault.*response(?!.*safe)
### **Message**
Spacecraft design may lack autonomous safe mode
### **Fix Action**
Define safe mode for sun-pointing and minimum power
### **Applies To**
  - **/*.py
  - **/*.yaml

## Components Without Thermal Limits

### **Id**
no-thermal-limits
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ThermalNode\((?!.*temp_min)
  - component(?!.*temperature.*limit)
  - thermal.*model(?!.*min|max)
### **Message**
Thermal model may not define component temperature limits
### **Fix Action**
Define allowable temperature range for all components
### **Applies To**
  - **/*.py

## Link Budget Without Margin Check

### **Id**
no-link-margin
### **Severity**
error
### **Type**
regex
### **Pattern**
  - link_budget(?!.*margin)
  - eb_n0(?!.*required)
  - snr(?!.*threshold)
### **Message**
Link budget may not verify adequate margin
### **Fix Action**
Require 3+ dB margin over required Eb/N0
### **Applies To**
  - **/*.py

## Single Star Tracker Design

### **Id**
single-star-tracker
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - star_tracker.*=.*1
  - n_trackers.*=.*1
  - single.*star.*tracker
### **Message**
Single star tracker provides no redundancy
### **Fix Action**
Use 2+ star trackers with different boresights
### **Applies To**
  - **/*.py