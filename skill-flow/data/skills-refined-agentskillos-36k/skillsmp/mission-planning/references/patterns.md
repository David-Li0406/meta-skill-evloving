# Mission Planning

## Patterns


---
  #### **Name**
mission_concept_development
  #### **Steps**
    - Define science/mission objectives
    - Derive requirements (orbit, pointing, data rate)
    - Select mission architecture
    - Trade study on orbit types
    - Preliminary mass and power budget
    - Identify launch vehicle options

---
  #### **Name**
trajectory_design
  #### **Steps**
    - Generate launch window candidates
    - Create porkchop plots for options
    - Select baseline trajectory
    - Design backup trajectories
    - Calculate delta-v budget with margins
    - Verify launch vehicle capability

---
  #### **Name**
operations_planning
  #### **Steps**
    - Define mission phases and transitions
    - Identify critical operations
    - Plan contingency procedures
    - Schedule ground contacts
    - Allocate data volume per pass
    - Document flight rules

## Anti-Patterns


---
  #### **Name**
single_launch_window
  #### **Problem**
Mission fails if window missed
  #### **Solution**
Always identify backup windows

---
  #### **Name**
optimistic_mass_budget
  #### **Problem**
No margin for growth
  #### **Solution**
20%+ contingency in early phases

---
  #### **Name**
ignoring_station_keeping
  #### **Problem**
Orbit degrades over time
  #### **Solution**
Budget delta-v for orbit maintenance

---
  #### **Name**
single_string_critical_path
  #### **Problem**
Any failure ends mission
  #### **Solution**
Redundancy for critical functions

---
  #### **Name**
no_disposal_plan
  #### **Problem**
Space debris liability
  #### **Solution**
Plan end-of-life from start (25-year rule)