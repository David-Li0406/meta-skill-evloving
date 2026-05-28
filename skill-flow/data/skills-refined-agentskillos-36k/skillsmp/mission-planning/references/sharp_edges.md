# Mission Planning - Sharp Edges

## Single Launch Window With No Backup

### **Id**
launch-window-miss
### **Severity**
critical
### **Summary**
Missing the window delays mission by months or years
### **Symptoms**
  - Mission delayed due to weather/technical issue
  - No alternative launch opportunity identified
  - Synodic period wait for interplanetary missions
### **Why**
  Interplanetary launch windows occur based on planetary alignment.
  Earth-Mars windows are ~26 months apart. If you miss your window
  and haven't planned for the next one, your mission waits years.
  
### **Gotcha**
  "Launch scrubbed due to weather"
  "When's the next window?"
  "In 26 months"
  "But we only funded 6 months of integration team"
  
  # Mars windows: 2024, 2026, 2029...
  
### **Solution**
  1. Plan for multiple windows:
     - Design trajectory for primary AND backup windows
     - Budget reserves for slip
     - Understand synodic period for your target
  
  2. Launch vehicle flexibility:
     - Multiple launch sites if possible
     - Range schedule contingency
     - Weather window buffers
  
  3. Program planning:
     - Fund team through backup window
     - Storage plan for spacecraft
     - Perishable items (batteries, propellant) replacement
  

## Mass Growth Exceeds Launch Vehicle Capability

### **Id**
mass-growth-explosion
### **Severity**
critical
### **Summary**
Actual mass exceeds capacity, mission redesign required
### **Symptoms**
  - Components heavier than estimated
  - Margin consumed by changes
  - Launch vehicle upgrade needed
### **Why**
  Mass grows throughout design. Early estimates are optimistic.
  Each subsystem adds "just a little" margin. Cables, brackets,
  and harnesses are underestimated. Without proper margins,
  you exceed launch vehicle capability.
  
### **Gotcha**
  "Our mass budget showed 200 kg margin at PDR"
  "At CDR we had 50 kg margin"
  "At ship review we're 30 kg over"
  "We need to either drop a payload or change rockets"
  
  # Typical mass growth: 20-30% from PDR to flight
  
### **Solution**
  1. Conservative margins:
     - 30%+ at concept phase
     - 20% at PDR
     - 10% at CDR
     - Track actuals vs estimates
  
  2. Mass scrub culture:
     - Regular mass review meetings
     - Challenge every addition
     - Reward mass savings
  
  3. Design for margin:
     - Lighter launch vehicle = cheaper
     - Leave room for problems
     - Plan descope options
  

## Delta-V Budget Insufficient for Mission

### **Id**
delta-v-budget-shortfall
### **Severity**
critical
### **Summary**
Not enough propellant for all planned maneuvers
### **Symptoms**
  - Orbit not achievable with remaining propellant
  - Station-keeping life shortened
  - Contingency maneuvers not possible
### **Why**
  Delta-v budget must cover: orbit insertion, orbit maintenance,
  attitude control, contingencies, and disposal. Each is often
  estimated separately with optimistic assumptions.
  Navigation errors require correction burns not originally planned.
  
### **Gotcha**
  "We budgeted 500 m/s for the mission"
  "Orbit insertion was 480 m/s instead of 450 m/s"
  "Now we only have 20 m/s for 5 years of operations"
  "Mission life cut from 5 years to 6 months"
  
  # Navigation errors can cost 10-20% more delta-v
  
### **Solution**
  1. Comprehensive budget:
     - List ALL maneuvers including contingency
     - Include navigation errors (3-sigma)
     - Add disposal delta-v
     - Include attitude control if shared system
  
  2. Margins:
     - 10% on each maneuver category
     - 20% overall reserve
     - Track propellant mass vs budget
  
  3. Operations:
     - Minimize unnecessary maneuvers
     - Optimize burn execution
     - Save margin for end of life
  

## End-of-Life Disposal Not Planned

### **Id**
disposal-afterthought
### **Severity**
high
### **Summary**
No way to meet debris mitigation requirements
### **Symptoms**
  - Spacecraft cannot deorbit
  - No propellant reserved for disposal
  - Orbit doesn't naturally decay in 25 years
### **Why**
  Debris mitigation guidelines require LEO spacecraft to deorbit
  within 25 years. GEO spacecraft must move to graveyard orbit.
  If disposal isn't designed in from the start, you may not have
  the capability to comply.
  
### **Gotcha**
  "We need to deorbit the satellite"
  "How much delta-v do we have?"
  "None, we used it all for station-keeping"
  "We're stuck in orbit for 200 years"
  
  # Legal/licensing increasingly requires disposal capability
  
### **Solution**
  1. Design for disposal:
     - Size propulsion for disposal burn
     - Reserve propellant explicitly
     - Consider drag augmentation devices
  
  2. Orbit selection:
     - Lower altitude = faster natural decay
     - Understand decay timeline
     - GEO: plan graveyard orbit
  
  3. Passivation:
     - Vent remaining propellant
     - Discharge batteries
     - Turn off transmitters
  

## Critical Single-Point Failures Not Addressed

### **Id**
single-point-failure
### **Severity**
high
### **Summary**
One component failure ends the mission
### **Symptoms**
  - Mission lost to single component failure
  - No redundancy in critical path
  - Failure modes not analyzed
### **Why**
  Space is unforgiving. Components fail. If your mission depends
  on a single component with no backup, you're betting the entire
  investment on that part working perfectly for the mission duration.
  
### **Gotcha**
  "The reaction wheel failed"
  "Do we have a backup?"
  "No, we only had 3 for 3-axis control"
  "Mission over after 6 months"
  
  # Many missions lost to single wheel failure
  
### **Solution**
  1. Failure mode analysis:
     - FMECA on all systems
     - Identify single points
     - Prioritize by criticality
  
  2. Redundancy:
     - 4 wheels for 3-axis control
     - Redundant computers
     - Multiple communication paths
  
  3. Graceful degradation:
     - Safe mode design
     - Reduced capability modes
     - Alternative operating methods
  