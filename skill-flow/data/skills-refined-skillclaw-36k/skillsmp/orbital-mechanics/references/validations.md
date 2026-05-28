# Orbital Mechanics - Validations

## Missing J2 Perturbation for LEO

### **Id**
no-j2-for-leo
### **Severity**
error
### **Type**
regex
### **Pattern**
  - propagate.*altitude.*<.*2000(?!.*j2)
  - LEO.*propagat(?!.*perturbation)
  - two_body.*low.*earth
### **Message**
LEO propagation may be missing J2 perturbation - predictions will diverge quickly
### **Fix Action**
Add J2 perturbation for any orbit below 2000 km altitude
### **Applies To**
  - **/*.py

## Hardcoded Gravitational Parameter

### **Id**
hardcoded-mu
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - mu\s*=\s*398600(?!.*comment)
  - GM\s*=\s*3\.986
  - \*\s*398600\.4
### **Message**
Gravitational parameter appears hardcoded - use named constant
### **Fix Action**
Define MU_EARTH or similar as named constant with units documented
### **Applies To**
  - **/*.py

## Kepler Solver Without Convergence Check

### **Id**
kepler-no-convergence-check
### **Severity**
error
### **Type**
regex
### **Pattern**
  - while.*kepler(?!.*max_iter)
  - for.*newton(?!.*converge)
  - eccentric_anomaly.*=(?!.*try)
### **Message**
Kepler equation solver may lack convergence checking
### **Fix Action**
Add maximum iteration limit and convergence tolerance check
### **Applies To**
  - **/*.py

## Plane Change at Periapsis

### **Id**
plane-change-at-periapsis
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - plane_change.*periapsis
  - inclination.*change.*at.*periapsis
  - delta_v.*incl(?!.*apoapsis)
### **Message**
Plane change at periapsis is inefficient - consider apoapsis
### **Fix Action**
Evaluate performing plane changes at apoapsis to minimize delta-v
### **Applies To**
  - **/*.py

## Unbounded Orbit Propagation

### **Id**
unbounded-propagation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - propagate\((?!.*max_time)
  - integrate.*orbit(?!.*limit)
  - while.*True.*propagat
### **Message**
Orbit propagation may run unbounded
### **Fix Action**
Set maximum propagation time or step limit
### **Applies To**
  - **/*.py

## Potential Division by Zero in Orbital Calculations

### **Id**
division-by-zero-orbit
### **Severity**
error
### **Type**
regex
### **Pattern**
  - /\s*\(.*\+.*\)(?!.*!=\s*0)
  - 1\s*/\s*e(?!.*if.*e)
  - sqrt\(1\s*-\s*e\*\*2\)(?!.*e\s*<\s*1)
### **Message**
Orbital calculation may divide by zero for edge cases (circular orbit, parabolic)
### **Fix Action**
Add checks for e=0 (circular), e=1 (parabolic), sum denominators
### **Applies To**
  - **/*.py

## Possible Unit Mismatch in Orbital Calculations

### **Id**
wrong-units-orbit
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - deg.*rad(?!.*convert)
  - km.*m(?!.*1000)
  - radians.*degrees(?!.*np\.)
### **Message**
Potential unit mismatch in orbital calculations
### **Fix Action**
Verify consistent units (km, rad) and explicit conversions
### **Applies To**
  - **/*.py