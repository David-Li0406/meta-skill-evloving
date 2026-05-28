# Mission Planning - Validations

## Single Launch Window Defined

### **Id**
no-backup-launch-window
### **Severity**
error
### **Type**
regex
### **Pattern**
  - launch_window\s*=(?!.*backup)
  - single.*launch.*opportunity
  - window.*=.*\[.*\](?!.*,.*,)
### **Message**
Only one launch window defined - identify backup opportunities
### **Fix Action**
Calculate and document backup launch windows
### **Applies To**
  - **/*.py
  - **/*.yaml

## Mass Budget Without Margin

### **Id**
no-mass-margin
### **Severity**
error
### **Type**
regex
### **Pattern**
  - mass_budget(?!.*margin)
  - total_mass.*=.*(?!.*contingency)
  - dry_mass\s*\+\s*propellant(?!.*reserve)
### **Message**
Mass budget may lack contingency margin
### **Fix Action**
Add 20%+ mass margin for early phase, 10% for CDR
### **Applies To**
  - **/*.py

## Delta-V Budget Without Margin

### **Id**
no-delta-v-margin
### **Severity**
error
### **Type**
regex
### **Pattern**
  - delta_v.*total(?!.*margin)
  - propellant.*=.*calculate(?!.*reserve)
  - maneuver_budget(?!.*contingency)
### **Message**
Delta-v budget may lack margin for errors and contingencies
### **Fix Action**
Add 10-20% delta-v margin to budget
### **Applies To**
  - **/*.py

## Missing Disposal Planning

### **Id**
no-disposal-plan
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - mission.*timeline(?!.*disposal)
  - phases.*=.*\[(?!.*disposal|deorbit)
  - end_of_life(?!.*deorbit|graveyard)
### **Message**
Mission may lack end-of-life disposal planning
### **Fix Action**
Plan deorbit (LEO) or graveyard orbit (GEO) disposal
### **Applies To**
  - **/*.py
  - **/*.yaml

## Possibly Optimistic Isp Value

### **Id**
optimistic-isp
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - isp.*=.*[4-9][0-9][0-9](?!.*electric|ion|hall)
  - specific_impulse.*>.*400
### **Message**
High Isp value - verify propulsion type supports this
### **Fix Action**
Verify Isp matches propulsion type (chemical ~300s, electric ~3000s)
### **Applies To**
  - **/*.py

## Incomplete Mission Phase Definition

### **Id**
missing-phase-definition
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - phases.*=.*\[(?!.*launch)
  - timeline(?!.*commission|checkout)
  - mission.*plan(?!.*contingency)
### **Message**
Mission phases may be incomplete
### **Fix Action**
Define all phases: launch, commissioning, ops, disposal
### **Applies To**
  - **/*.py
  - **/*.yaml

## Critical System Without Redundancy Analysis

### **Id**
no-redundancy-check
### **Severity**
info
### **Type**
regex
### **Pattern**
  - critical.*system(?!.*redundan)
  - single.*point(?!.*failure)
  - FMECA(?!.*complete)
### **Message**
Critical systems should have redundancy analysis
### **Fix Action**
Perform FMECA and add redundancy for critical functions
### **Applies To**
  - **/*.py
  - **/*.md