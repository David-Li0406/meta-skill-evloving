# Ground Station Ops - Validations

## TLE Age Not Validated

### **Id**
stale-tle-check
### **Severity**
error
### **Type**
regex
### **Pattern**
  - TLE(?!.*age|epoch|update)
  - propagate.*tle(?!.*valid)
  - predict.*pass(?!.*tle.*fresh)
### **Message**
TLE-based predictions may not check TLE age
### **Fix Action**
Validate TLE age before prediction (< 3 days for LEO)
### **Applies To**
  - **/*.py

## Command Without Echo Verification

### **Id**
no-command-echo
### **Severity**
error
### **Type**
regex
### **Pattern**
  - send_command(?!.*echo|verify)
  - uplink(?!.*confirm)
  - command\.execute(?!.*check)
### **Message**
Command uplink may lack echo verification
### **Fix Action**
Always verify command echo before execution acknowledgment
### **Applies To**
  - **/*.py

## Link Budget Without Margin Verification

### **Id**
no-link-margin-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - link_budget(?!.*margin)
  - signal_to_noise(?!.*threshold)
  - eb_n0(?!.*required)
### **Message**
Link analysis may not verify adequate margin
### **Fix Action**
Check Eb/N0 > required + 3 dB margin
### **Applies To**
  - **/*.py

## Scheduling Without Weather Check

### **Id**
no-weather-consideration
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - schedule.*pass(?!.*weather)
  - contact.*plan(?!.*rain|attenuation)
  - link.*loss(?!.*atmospheric)
### **Message**
Contact scheduling may not account for weather
### **Fix Action**
Include weather-based attenuation in link budget
### **Applies To**
  - **/*.py

## Telemetry Without Limit Checking

### **Id**
no-telemetry-limits
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - TelemetryPoint\((?!.*limit)
  - process.*telemetry(?!.*check|status)
  - calibrat(?!.*limit)
### **Message**
Telemetry processing may lack limit checking
### **Fix Action**
Define warning and critical limits for all telemetry
### **Applies To**
  - **/*.py

## Telemetry Without Archive

### **Id**
no-data-archive
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - process.*frame(?!.*store|archive|history)
  - telemetry.*latest(?!.*history)
  - TelemetryProcessor(?!.*history)
### **Message**
Telemetry processing may not archive historical data
### **Fix Action**
Archive all telemetry for trending and anomaly investigation
### **Applies To**
  - **/*.py

## Scheduler Without Conflict Resolution

### **Id**
no-conflict-resolution
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - schedule.*contact(?!.*conflict)
  - generate_schedule(?!.*overlap)
  - pass.*list(?!.*priority)
### **Message**
Contact scheduler may not handle conflicts
### **Fix Action**
Add priority-based conflict resolution
### **Applies To**
  - **/*.py

## Hardcoded Minimum Elevation

### **Id**
hardcoded-min-elevation
### **Severity**
info
### **Type**
regex
### **Pattern**
  - min_elevation\s*=\s*[0-9](?!.*config)
  - elevation.*>\s*5(?!.*parameter)
### **Message**
Minimum elevation may be hardcoded
### **Fix Action**
Make minimum elevation configurable per station
### **Applies To**
  - **/*.py