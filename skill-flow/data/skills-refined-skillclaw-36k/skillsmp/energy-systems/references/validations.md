# Energy Systems - Validations

## DC Power Flow for Voltage Analysis

### **Id**
dc-power-flow-voltage
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - rundcpp.*voltage|voltage.*rundcpp
  - dc_power_flow.*volt(?!age_angle)
### **Message**
DC power flow ignores voltage magnitudes. Use AC for voltage studies.
### **Fix Action**
Use: pp.runpp(net) instead of pp.rundcpp(net)
### **Applies To**
  - **/*.py

## Battery Storage Without Efficiency

### **Id**
storage-no-efficiency
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - energy_out\s*=\s*energy_in(?!.*eff)
  - soc.*charge.*discharge(?!.*loss|eff)
### **Message**
Battery round-trip efficiency is 85-95%, not 100%.
### **Fix Action**
Apply: energy_out = energy_in * sqrt(round_trip_eff) for each direction
### **Applies To**
  - **/*.py

## Battery Optimization Without Degradation

### **Id**
storage-no-degradation
### **Severity**
info
### **Type**
regex
### **Pattern**
  - arbitrage|dispatch.*optim(?!.*degrad|cycle|life)
  - maximize.*revenue.*storage(?!.*wear)
### **Message**
Include degradation cost in storage optimization.
### **Fix Action**
Add degradation cost = cycles * (replacement_cost / cycle_life)
### **Applies To**
  - **/*.py

## Dispatch Without Ramp Constraints

### **Id**
no-ramp-constraints
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - dispatch\[t\].*=(?!.*ramp)
  - power\[t\].*=.*demand(?!.*ramp|limit)
### **Message**
Include generator ramp rate constraints in dispatch.
### **Fix Action**
Add: abs(p[t] - p[t-1]) <= ramp_rate * timestep
### **Applies To**
  - **/*.py

## Unit Commitment Without Min Up/Down Time

### **Id**
no-min-up-down
### **Severity**
info
### **Type**
regex
### **Pattern**
  - unit_commitment(?!.*min_up|min_down)
  - on_off.*var(?!.*up_time|down_time)
### **Message**
Include minimum up/down time constraints for thermal units.
### **Fix Action**
Add: sum(u[t-min_up:t]) >= min_up * (u[t] - u[t-1])
### **Applies To**
  - **/*.py

## Only N-1 Contingency Analysis

### **Id**
single-contingency
### **Severity**
info
### **Type**
regex
### **Pattern**
  - contingency.*for.*element(?!.*n_1_1|n-1-1|second)
  - n_minus_1(?!.*n_minus_2|cascade)
### **Message**
Consider N-1-1 for critical infrastructure.
### **Fix Action**
After N-1, check second contingency before system is restored.
### **Applies To**
  - **/*.py

## Static Load in Dynamic Simulation

### **Id**
constant-load
### **Severity**
info
### **Type**
regex
### **Pattern**
  - dynamic.*sim.*p_mw\s*=\s*\d+(?!.*zip|composite)
  - transient.*load.*const
### **Message**
Use voltage-dependent load models for dynamic studies.
### **Fix Action**
Apply ZIP model: P = P0 * (z*V² + i*V + p)
### **Applies To**
  - **/*.py

## Power Flow Without Balance Verification

### **Id**
no-power-balance-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - runpp|runpf(?!.*balance|verify|check)
### **Message**
Verify power balance after power flow simulation.
### **Fix Action**
Check: abs(sum(gen) - sum(load) - losses) < tolerance
### **Applies To**
  - **/*.py

## Mixing Per-Unit and Physical Units

### **Id**
per-unit-mismatch
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - pu.*\*.*mw|mw.*\*.*pu(?!.*base)
  - v_pu.*\+.*kv|kv.*\+.*v_pu
### **Message**
Don't mix per-unit and physical units without base conversion.
### **Fix Action**
Convert: MW = pu * S_base; kV = pu * V_base
### **Applies To**
  - **/*.py

## Dispatch Ignoring Transmission Losses

### **Id**
ignore-losses
### **Severity**
info
### **Type**
regex
### **Pattern**
  - demand.*=.*sum.*gen(?!.*loss)
  - balance.*gen.*load(?!.*loss)
### **Message**
Include transmission losses (2-6% of generation).
### **Fix Action**
Add: sum(gen) = sum(load) + losses
### **Applies To**
  - **/*.py

## Generator Without Reactive Power Limits

### **Id**
no-reactive-limits
### **Severity**
info
### **Type**
regex
### **Pattern**
  - create_gen.*p_mw(?!.*q_max|q_min)
  - gen.*reactive(?!.*limit|cap)
### **Message**
Define generator reactive power limits for voltage analysis.
### **Fix Action**
Add: max_q_mvar and min_q_mvar to generator definition
### **Applies To**
  - **/*.py

## Large Disturbance Without Frequency Response

### **Id**
frequency-ignored
### **Severity**
info
### **Type**
regex
### **Pattern**
  - trip.*gen.*(?!.*frequency|inertia|governor)
  - contingency.*generator(?!.*freq)
### **Message**
Model frequency response for generator trip studies.
### **Fix Action**
Include inertia constant H, governor droop, load damping.
### **Applies To**
  - **/*.py