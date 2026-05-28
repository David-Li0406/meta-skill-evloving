# Orbital Mechanics - Sharp Edges

## Two-Body Propagation Fails for LEO

### **Id**
two-body-assumption-failure
### **Severity**
critical
### **Summary**
Ignoring J2 causes km-level errors in hours
### **Symptoms**
  - Predicted position differs from actual by kilometers
  - Satellite not where expected during pass
  - Collision avoidance calculations wrong
### **Why**
  Earth's oblateness (J2) causes RAAN to drift ~7 deg/day for typical LEO.
  Two-body assumes spherical Earth. After one day, your predicted orbital
  plane can be wrong by degrees - that's hundreds of km in position.
  
### **Gotcha**
  "The satellite should be over Europe"
  "It's over Africa"
  "We propagated for 24 hours with Keplerian elements"
  "But Earth isn't a sphere"
  
  # J2 causes ~7 deg/day RAAN drift at ISS altitude
  
### **Solution**
  1. Always include J2 for LEO:
     - Use at minimum J2 secular rates
     - Better: full J2 in numerical propagation
     - Best: J2-J6 + drag + solar pressure
  
  2. Know your error growth:
     - Two-body: km/day error for LEO
     - J2 only: 100m/day error
     - Full model: cm-level possible
  
  3. Use appropriate tools:
     - SGP4/SDP4 for TLE propagation
     - GMAT/STK for precision work
  

## Plane Change at Wrong Location Wastes Delta-V

### **Id**
wrong-plane-change-location
### **Severity**
high
### **Summary**
Plane changes at periapsis cost 2x more than at apoapsis
### **Symptoms**
  - Excessive fuel consumption
  - Shorter mission life than planned
  - Maneuver sequence seems inefficient
### **Why**
  Delta-v for plane change is proportional to velocity: dv = 2*v*sin(di/2).
  Velocity is highest at periapsis, lowest at apoapsis. Same inclination
  change costs much more at periapsis.
  
### **Gotcha**
  "We need to change inclination by 10 degrees"
  "Let's do it at periapsis, we're there anyway"
  "That cost 500 m/s!"
  "At apoapsis it would have been 200 m/s"
  
  # v_periapsis / v_apoapsis can be 2x or more
  
### **Solution**
  1. Plan plane changes at apoapsis:
     - Velocity is lowest
     - Delta-v is minimized
     - Worth waiting half an orbit
  
  2. Combined maneuvers:
     - If raising orbit AND changing plane
     - Do both at same point
     - Vector sum is less than separate burns
  
  3. Analysis:
     - Calculate both options
     - Factor in mission constraints
     - Sometimes timing matters more than fuel
  

## Kepler Equation Solver Diverges

### **Id**
kepler-equation-divergence
### **Severity**
high
### **Summary**
Newton-Raphson fails for high eccentricity with poor initial guess
### **Symptoms**
  - Solver throws convergence error
  - NaN in orbital calculations
  - Highly elliptical orbits fail to propagate
### **Why**
  The Kepler equation M = E - e*sin(E) is solved iteratively. For high
  eccentricity, the function has steep regions. A poor initial guess
  can cause Newton-Raphson to diverge or oscillate.
  
### **Gotcha**
  "Propagation works for circular orbits"
  "But crashes for Molniya orbit (e=0.74)"
  "Newton-Raphson diverged"
  "Initial guess E=M doesn't work for high e"
  
  # Need E=pi as initial guess when e > 0.8
  
### **Solution**
  1. Adaptive initial guess:
     - e < 0.8: E_0 = M
     - e >= 0.8: E_0 = pi
     - Or use series expansion for first guess
  
  2. Robust solver:
     - Limit maximum iterations
     - Use bisection as fallback
     - Consider Laguerre's method
  
  3. Test edge cases:
     - e = 0 (circular)
     - e = 0.9 (highly elliptical)
     - e approaching 1 (near-parabolic)
  

## Patched Conic SOI Transition Errors

### **Id**
patched-conic-boundary-errors
### **Severity**
high
### **Summary**
Discontinuities at sphere of influence boundaries
### **Symptoms**
  - Trajectory jumps at planetary arrival
  - Energy not conserved across transition
  - Capture calculations wrong
### **Why**
  Patched conic is an approximation - we switch gravity sources at the
  sphere of influence (SOI). In reality, both bodies pull simultaneously.
  The transition introduces discontinuities in trajectory.
  
### **Gotcha**
  "Our Mars capture delta-v was calculated as 900 m/s"
  "Actual capture required 1100 m/s"
  "The patched conic transition added error"
  "We should have used higher fidelity at the boundary"
  
  # SOI is just a convention, not a physical boundary
  
### **Solution**
  1. Understand the approximation:
     - SOI is where gravitational influences are roughly equal
     - Not a sharp boundary
     - Error is inherent to method
  
  2. Add margins:
     - 10-20% delta-v margin for captures
     - More for low-altitude captures
     - Less for high flybys
  
  3. Higher fidelity when needed:
     - Full N-body for critical phases
     - Restricted three-body for libration points
     - Monte Carlo for uncertainty
  

## Mixing Up Anomaly Types

### **Id**
wrong-anomaly-type
### **Severity**
medium
### **Summary**
Using true anomaly where mean anomaly expected or vice versa
### **Symptoms**
  - Position calculations completely wrong
  - Time-of-flight calculations incorrect
  - Rendezvous timing errors
### **Why**
  Three anomaly types exist: Mean (M), Eccentric (E), True (nu).
  They're related but NOT interchangeable. Mean anomaly increases
  linearly with time. True anomaly is actual angle from periapsis.
  For eccentric orbits, they differ significantly.
  
### **Gotcha**
  "Spacecraft position is 45 degrees from periapsis"
  "That's the true anomaly"
  "But we used it as mean anomaly for propagation"
  "Now timing is off by hours"
  
  # At e=0.5, true anomaly 90 deg = mean anomaly 63 deg
  
### **Solution**
  1. Be explicit about anomaly type:
     - nu = true anomaly (geometric angle)
     - E = eccentric anomaly (auxiliary)
     - M = mean anomaly (linear in time)
  
  2. Convert correctly:
     - M -> E: Solve Kepler equation
     - E -> nu: tan(nu/2) = sqrt((1+e)/(1-e))*tan(E/2)
     - Know which your tools expect
  
  3. Verify with sanity checks:
     - M=E=nu=0 at periapsis
     - M=E=nu=pi at apoapsis
     - For circular orbits, all equal
  