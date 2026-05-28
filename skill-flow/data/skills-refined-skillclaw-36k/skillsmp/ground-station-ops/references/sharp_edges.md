# Ground Station Ops - Sharp Edges

## Stale TLE Causes Missed Passes

### **Id**
stale-tle-predictions
### **Severity**
critical
### **Summary**
Predictions diverge from reality as TLE ages
### **Symptoms**
  - Satellite not acquired at predicted AOS
  - Antenna searching but no signal
  - Pass shorter than predicted
### **Why**
  TLE (Two-Line Element) sets have built-in epoch time. Prediction
  accuracy degrades with age. For LEO, a TLE >3 days old can have
  km-level errors. The satellite isn't where you think it is.
  
### **Gotcha**
  "Antenna is tracking the predicted position"
  "But no signal at AOS"
  "When was the TLE updated?"
  "A week ago"
  
  # LEO TLE: update daily, GEO: weekly okay
  
### **Solution**
  1. Fresh TLEs:
     - LEO: Update daily minimum
     - MEO/GEO: Update weekly
     - Get from Space-Track.org
  
  2. Prediction monitoring:
     - Compare actual AOS to predicted
     - Track systematic errors
     - Flag when TLE is stale
  
  3. Acquisition margins:
     - Start tracking before predicted AOS
     - Use search pattern if needed
     - Allow for prediction uncertainty
  

## Commanding Without Verification

### **Id**
command-without-verification
### **Severity**
critical
### **Summary**
Wrong command sent without checking echo
### **Symptoms**
  - Spacecraft in unexpected state
  - Command log doesn't match intent
  - Operator error propagated to spacecraft
### **Why**
  Commands can be mistyped, selected incorrectly, or corrupted in
  transmission. Without verifying the command echo (what the
  spacecraft received), you don't know what was actually executed.
  
### **Gotcha**
  "I sent the attitude maneuver command"
  "But the spacecraft is spinning"
  "The parameter was wrong - 100 deg instead of 10 deg"
  "We didn't check the echo before execution"
  
  # Command errors are a leading cause of spacecraft anomalies
  
### **Solution**
  1. Mandatory verification:
     - Always check command echo
     - Compare to intended parameters
     - Block execution until verified
  
  2. Two-person rule:
     - Second operator confirms
     - Required for critical commands
     - Audit trail of both authorizations
  
  3. Constraint checking:
     - Automated prerequisite verification
     - Range/limit checking on parameters
     - State machine validation
  

## Rain Fade Causes Critical Contact Loss

### **Id**
rain-fade-loss
### **Severity**
high
### **Summary**
Atmospheric attenuation drops link during rain
### **Symptoms**
  - Link margin degrades during pass
  - Data errors increase
  - Contact lost before LOS
### **Why**
  Rain absorbs and scatters RF energy, especially at higher
  frequencies (Ka-band: 3-10 dB loss, X-band: 1-3 dB).
  A link designed with 3 dB margin can fail in moderate rain.
  
### **Gotcha**
  "We lost the link at 45 degrees elevation"
  "Should have been fine until 10 degrees"
  "It started raining during the pass"
  "Our Ka-band link couldn't handle it"
  
  # Ka-band very sensitive, S-band nearly immune
  
### **Solution**
  1. Design for weather:
     - Extra margin for rain (location-dependent)
     - Lower frequency backup (X instead of Ka)
     - Diversity sites
  
  2. Weather awareness:
     - Monitor forecasts
     - Real-time attenuation sensing
     - Adaptive data rates
  
  3. Operations:
     - Critical activities during clear weather
     - Backup scheduling
     - Rain rate statistics for site
  

## Data Overflow Due to Insufficient Contact

### **Id**
data-overflow-loss
### **Severity**
high
### **Summary**
On-board recorder fills faster than data can be downlinked
### **Symptoms**
  - Data recorder approaching full
  - Oldest data being overwritten
  - Science data lost
### **Why**
  Spacecraft generate data continuously but can only downlink during
  contacts. If generation rate exceeds average downlink capacity,
  the recorder fills up. Then you lose data.
  
### **Gotcha**
  "Payload generated 10 GB today"
  "We only had one 8-minute pass"
  "Downlinked 500 MB"
  "9.5 GB waiting, but recorder is only 5 GB"
  
  # Average generation must be < average downlink
  
### **Solution**
  1. Budget data volume:
     - Calculate daily generation
     - Calculate daily downlink capacity
     - Verify positive margin
  
  2. Prioritization:
     - Mark data by priority
     - Oldest-first or priority-first
     - Don't overwrite critical data
  
  3. Operations:
     - More ground stations
     - Higher data rate mode
     - Reduce payload duty cycle
  

## Command Sent to Wrong Spacecraft

### **Id**
wrong-spacecraft-command
### **Severity**
critical
### **Summary**
Multi-satellite constellation command routing error
### **Symptoms**
  - Commanded satellite doesn't respond
  - Different satellite executes command
  - Constellation coordination broken
### **Why**
  With multiple satellites, each has a unique address. If the
  ground system isn't correctly configured, or operator selects
  wrong target, commands go to unintended spacecraft.
  
### **Gotcha**
  "SAT-1 didn't execute the maneuver"
  "But SAT-2 is now in wrong orbit"
  "The command routing was set to SAT-2"
  "We commanded the wrong satellite"
  
  # Constellation operations require rigorous ID checking
  
### **Solution**
  1. Configuration management:
     - Unique spacecraft identifiers
     - Session-based target locking
     - Visual confirmation of target
  
  2. Verification:
     - Spacecraft echoes include ID
     - Cross-check before execution
     - Telemetry from correct satellite
  
  3. Automation:
     - Scheduler sets correct target
     - Procedure includes ID verification
     - Block cross-routing
  