# Discrete Event Simulation - Validations

## Floating Point Time Accumulation

### **Id**
float-time-accumulation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - time\s*\+=\s*\d+\.\d+|current_time\s*\+=\s*delta
  - self\.now\s*\+=.*\d+\.\d+
### **Message**
Accumulating float time causes precision errors. Use integer time or track absolute.
### **Fix Action**
Use integer time units: time = int(seconds * TIME_SCALE)
### **Applies To**
  - **/*.py

## Statistics Without Warm-up Truncation

### **Id**
no-warmup-handling
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - mean\(.*observations\)|average\(.*stats\)(?!.*warmup|truncat)
### **Message**
Truncate warm-up period before computing steady-state statistics.
### **Fix Action**
Detect warm-up: truncation = mser_detect(data); data = data[truncation:]
### **Applies To**
  - **/*.py

## Single Simulation Run Without Replications

### **Id**
single-seed-run
### **Severity**
info
### **Type**
regex
### **Pattern**
  - result\s*=\s*run_simulation\(\)(?!.*for|while|replicate)
### **Message**
Run multiple replications to quantify output variability.
### **Fix Action**
Run replications: results = [run(seed=i) for i in range(30)]
### **Applies To**
  - **/*.py

## Unbounded List Used as Queue

### **Id**
unbounded-list-queue
### **Severity**
info
### **Type**
regex
### **Pattern**
  - queue\s*=\s*\[\]|waiting\s*=\s*\[\](?!.*maxlen|capacity)
### **Message**
Real queues have finite capacity. Model blocking/abandonment.
### **Fix Action**
Use simpy.Store(capacity=N) or check length before append
### **Applies To**
  - **/*.py

## Events Without Priority/Tiebreaker

### **Id**
no-event-priority
### **Severity**
info
### **Type**
regex
### **Pattern**
  - heappush\(.*,\s*\(time,\s*event\)\)|Event\(time=.*\)(?!.*priority|sequence)
### **Message**
Define event priority for consistent same-time ordering.
### **Fix Action**
Add priority: (time, priority, sequence, event) for deterministic tiebreaking
### **Applies To**
  - **/*.py

## Nested Resource Requests (Deadlock Risk)

### **Id**
nested-resource-request
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - with.*\.request\(\).*:\s*\n.*with.*\.request\(\)
### **Message**
Nested resource requests can cause deadlock. Acquire in consistent order.
### **Fix Action**
Acquire resources in fixed global order, or use timeout with retry
### **Applies To**
  - **/*.py

## Results Reported Without Confidence Intervals

### **Id**
no-confidence-interval
### **Severity**
info
### **Type**
regex
### **Pattern**
  - print.*mean.*result(?!.*ci|confidence|stderr|\+-)
### **Message**
Report confidence intervals with simulation results.
### **Fix Action**
Add CI: ci = (mean - 1.96*se, mean + 1.96*se)
### **Applies To**
  - **/*.py

## Compared Systems Using Independent Random Streams

### **Id**
independent-random-streams
### **Severity**
info
### **Type**
regex
### **Pattern**
  - system_a.*seed.*=.*\n.*system_b.*seed.*=.*(?!.*same|crn)
### **Message**
Use Common Random Numbers (CRN) for system comparison.
### **Fix Action**
Use same seed sequence for compared systems to reduce variance
### **Applies To**
  - **/*.py

## Global Mutable Simulation State

### **Id**
global-simulation-state
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^current_time\s*=|^event_queue\s*=\s*\[
  - global\s+sim_time|global\s+queue
### **Message**
Global simulation state prevents multiple independent runs.
### **Fix Action**
Encapsulate in SimulationEngine class with instance variables
### **Applies To**
  - **/*.py

## Hard-coded Simulation Run Length

### **Id**
hard-coded-run-length
### **Severity**
info
### **Type**
regex
### **Pattern**
  - run\(until=\d+\)|run\(max_time=\d+\)(?!.*config|param)
### **Message**
Run length should be configurable for sensitivity analysis.
### **Fix Action**
Accept parameter: def run_simulation(duration: float = 1000)
### **Applies To**
  - **/*.py