# Spacecraft Systems - Sharp Edges

## Reaction Wheel Saturation Causes Loss of Control

### **Id**
reaction-wheel-saturation
### **Severity**
critical
### **Summary**
Wheels absorb momentum until they can't spin faster
### **Symptoms**
  - Pointing accuracy degrades
  - Wheels at maximum speed
  - Spacecraft begins tumbling
### **Why**
  Reaction wheels absorb angular momentum from disturbances (gravity
  gradient, solar pressure, magnetic). They spin faster to compensate.
  Eventually they hit max speed and can't absorb more - you lose control.
  
### **Gotcha**
  "Spacecraft is drifting off target"
  "Wheels are at 6000 RPM"
  "Maximum is 6000 RPM"
  "We forgot to plan momentum dumping"
  
  # External torques: ~1e-6 Nm typical, adds up over orbits
  
### **Solution**
  1. Plan momentum management:
     - Calculate secular momentum buildup
     - Size wheel momentum capacity for dump interval
     - Allocate time for desaturation
  
  2. Dumping methods:
     - Magnetorquers (LEO, continuous)
     - Thrusters (any orbit, uses propellant)
     - Gravity gradient (specific orientations)
  
  3. Monitor and act:
     - Track wheel speeds in telemetry
     - Automatic desaturation triggers
     - Safe mode if approaching limits
  

## Deep Battery Discharge Kills Capacity

### **Id**
battery-deep-discharge
### **Severity**
critical
### **Summary**
Discharging below 70% SOC accelerates degradation
### **Symptoms**
  - Battery capacity decreasing over time
  - Eclipse duration margins shrinking
  - Mission life shortened
### **Why**
  Li-ion batteries degrade faster with deep discharge cycles.
  Rated for 50000 cycles at 30% DOD, but only 5000 cycles at 80% DOD.
  Each eclipse counts as a cycle. Deeper discharge = shorter life.
  
### **Gotcha**
  "Battery was sized for 1-hour eclipse at 80% DOD"
  "After 2 years, capacity is down 40%"
  "We can't survive full eclipses anymore"
  "Should have sized for 30% DOD"
  
  # 30% DOD = 50000 cycles, 80% DOD = 5000 cycles
  
### **Solution**
  1. Size conservatively:
     - Design for 30% DOD maximum
     - Include degradation in sizing
     - Account for cell imbalance
  
  2. Thermal management:
     - Battery operates best at 10-25C
     - Avoid thermal cycling
     - Dedicated thermal control
  
  3. Monitor health:
     - Track capacity vs prediction
     - Cell voltage monitoring
     - End-of-life planning
  

## Star Tracker Blinded by Sun/Moon/Earth

### **Id**
star-tracker-blinding
### **Severity**
high
### **Summary**
Bright objects in FOV prevent attitude determination
### **Symptoms**
  - Star tracker reports no solution
  - Attitude accuracy degrades
  - Occurs at certain orbit positions
### **Why**
  Star trackers image stars to determine attitude. Sun, Moon, or
  Earth limb in the FOV saturates the detector. The tracker can't
  see stars and loses its attitude solution.
  
### **Gotcha**
  "Star tracker 1 went blind"
  "Switch to tracker 2"
  "Both trackers are pointed the same direction"
  "Both are blinded by Earth"
  
  # Sun: always avoid, Moon: predictable, Earth: depends on orientation
  
### **Solution**
  1. Multiple trackers:
     - Different boresight directions
     - Can always see stars in some direction
     - Typically 2-3 trackers
  
  2. Exclusion zones:
     - Define Sun/Moon/Earth avoidance
     - ~30-40 deg exclusion typical
     - Mission planning for geometry
  
  3. Fallback sensors:
     - Sun sensors for coarse attitude
     - Gyro propagation during blind periods
     - Magnetometer for LEO
  

## Single Power Bus Failure Kills Spacecraft

### **Id**
single-point-power-failure
### **Severity**
high
### **Summary**
Power system has no redundancy path
### **Symptoms**
  - One component failure causes total loss
  - No way to isolate failed element
  - Cannot shed loads to survive
### **Why**
  Power is required by everything. A single power bus design means
  one failure (short, open, regulator) can take out the entire
  spacecraft. No power = no communication = mission lost.
  
### **Gotcha**
  "Solar array string shorted"
  "It pulled down the whole bus"
  "We couldn't isolate it"
  "Spacecraft went silent"
  
  # Power anomalies are leading cause of spacecraft failures
  
### **Solution**
  1. Redundant architecture:
     - Multiple solar array strings
     - Cross-strapped batteries
     - Redundant regulators
  
  2. Protection:
     - Current limiters
     - Fuses or circuit breakers
     - Autonomous load shedding
  
  3. Safe mode power:
     - Minimum configuration survives
     - Critical loads always powered
     - Can communicate for recovery
  

## Thermal Snap Causes Structural Damage

### **Id**
thermal-snap-structural
### **Severity**
high
### **Summary**
Rapid temperature change stresses structure beyond limits
### **Symptoms**
  - Cracking sounds in telemetry
  - Misalignment of components
  - Solar array deployment issues
### **Why**
  Eclipse entry/exit causes rapid temperature changes. Different
  materials expand/contract at different rates. Large temperature
  gradients create stress. This can crack structures or cause
  permanent deformation.
  
### **Gotcha**
  "Solar array won't deploy fully"
  "Mechanism binding"
  "It worked fine before eclipse"
  "Thermal gradient distorted the hinge"
  
  # Temperature change can be 100+ degrees in minutes
  
### **Solution**
  1. Design for thermal environment:
     - CTE matching for bonded joints
     - Flexible connections where needed
     - Thermal analysis of gradients
  
  2. Slow transitions:
     - Heater pre-conditioning
     - Attitude maneuvers to reduce gradient
     - Operational procedures
  
  3. Test:
     - Thermal vacuum testing
     - Multiple cycles
     - Include mechanisms in test
  