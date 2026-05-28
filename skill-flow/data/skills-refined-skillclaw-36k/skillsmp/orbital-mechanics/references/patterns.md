# Orbital Mechanics

## Patterns


---
  #### **Name**
orbit_determination
  #### **Steps**
    - Collect position/velocity observations
    - Initial orbit determination (IOD) from multiple observations
    - Differential correction to refine orbit
    - Convert to standard orbital elements
    - Validate with propagation vs observations

---
  #### **Name**
maneuver_sequence
  #### **Steps**
    - Define initial and target orbits
    - Select transfer type (Hohmann, bi-elliptic, etc.)
    - Calculate delta-v requirements
    - Add margins for navigation uncertainty
    - Determine burn times and directions
    - Verify final orbit achieved

---
  #### **Name**
orbit_maintenance
  #### **Steps**
    - Define orbit tolerance box
    - Propagate with perturbations
    - Predict when leaving tolerance
    - Plan station-keeping maneuvers
    - Budget delta-v for mission lifetime

## Anti-Patterns


---
  #### **Name**
ignoring_j2_for_leo
  #### **Problem**
Predictions diverge within hours
  #### **Solution**
Include J2 perturbation at minimum for LEO

---
  #### **Name**
two_body_long_propagation
  #### **Problem**
Misses secular drifts over time
  #### **Solution**
Use perturbation model for multi-day propagation

---
  #### **Name**
hohmann_always_optimal
  #### **Problem**
Not true for large orbit ratio transfers
  #### **Solution**
Consider bi-elliptic when r2/r1 > 11.94

---
  #### **Name**
ignoring_sphere_of_influence
  #### **Problem**
Using wrong gravity source
  #### **Solution**
Properly model patched conic transitions

---
  #### **Name**
plane_change_at_periapsis
  #### **Problem**
Maximum delta-v waste
  #### **Solution**
Perform plane changes at apoapsis where velocity is lowest