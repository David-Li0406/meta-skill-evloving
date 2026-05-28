# Digital Twin - Validations

## Sensor Read Without Timeout

### **Id**
no-sensor-timeout
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - await\s+sensor\.read\(\)(?!.*timeout)
  - sensor\.get_value\(\)(?!.*timeout)
### **Message**
Sensor reads should have timeouts to handle communication failures.
### **Fix Action**
Add timeout: await asyncio.wait_for(sensor.read(), timeout=1.0)
### **Applies To**
  - **/*.py

## Sensor Data Used Without Quality Check

### **Id**
no-data-quality-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - twin\.update\(.*reading\.value(?!.*quality)
  - state\s*=.*sensor_value(?!.*valid|quality|fresh)
### **Message**
Sensor data should be validated for quality/freshness before use.
### **Fix Action**
Check data quality: if reading.quality > 0.5 and reading.is_fresh()
### **Applies To**
  - **/*.py

## Twin History Without Size Limit

### **Id**
unbounded-history
### **Severity**
info
### **Type**
regex
### **Pattern**
  - history\.append\(.*\)(?!.*maxlen|limit|[-]\d+:)
  - state_history\.append(?!.*deque)
### **Message**
History buffers should have size limits to prevent memory growth.
### **Fix Action**
Use deque(maxlen=N) or trim: history = history[-1000:]
### **Applies To**
  - **/*.py

## Twin Update Without Residual Check

### **Id**
no-residual-monitoring
### **Severity**
info
### **Type**
regex
### **Pattern**
  - twin\.update\(.*\)(?!.*residual|diverge|error)
### **Message**
Monitor residuals (predicted vs actual) to detect model divergence.
### **Fix Action**
Check residuals: if abs(predicted - actual) > threshold: recalibrate()
### **Applies To**
  - **/*.py

## Synchronous Sensor Polling in Loop

### **Id**
synchronous-sensor-loop
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - for.*sensor.*in.*:\s*\n.*sensor\.read\(\)(?!.*async|gather|parallel)
  - while.*True.*sensor\.poll\(\)(?!.*async)
### **Message**
Sequential sensor polling is slow. Use async/parallel reads.
### **Fix Action**
Use asyncio.gather() for parallel sensor reads
### **Applies To**
  - **/*.py

## Message Timestamp Not Validated

### **Id**
no-timestamp-validation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - message\.timestamp(?!.*now|age|stale|fresh|valid)
  - data\[['"]timestamp['"]\](?!.*check|valid)
### **Message**
Validate message timestamps to detect stale or future-dated data.
### **Fix Action**
Check: if abs(now - timestamp) > max_age: reject_or_flag()
### **Applies To**
  - **/*.py

## Hardcoded Model Calibration Parameters

### **Id**
hardcoded-calibration
### **Severity**
info
### **Type**
regex
### **Pattern**
  - friction\s*=\s*0\.\d+\s*(?!#.*config|env)
  - efficiency\s*=\s*0\.\d+\s*(?!#.*calibrat)
### **Message**
Calibration parameters should be configurable, not hardcoded.
### **Fix Action**
Load from config: friction = config.get('friction', default=0.1)
### **Applies To**
  - **/*.py

## Twin Update Without Latency Measurement

### **Id**
no-latency-tracking
### **Severity**
info
### **Type**
regex
### **Pattern**
  - def\s+update.*state.*:(?!.*latency|timing|perf)
### **Message**
Track end-to-end latency to ensure real-time requirements are met.
### **Fix Action**
Measure: latency = time.time() - message_timestamp; log if > threshold
### **Applies To**
  - **/*.py

## Global Mutable Twin State

### **Id**
global-twin-state
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^twin_state\s*=\s*\{|^current_state\s*=\s*\[
  - global\s+twin|global\s+state
### **Message**
Global mutable state causes race conditions in concurrent systems.
### **Fix Action**
Use instance attributes or thread-safe state management
### **Applies To**
  - **/*.py

## Sensor Communication Without Error Handling

### **Id**
no-error-handling-sensor
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - sensor\.read\(\)(?!.*try|except|error)
  - await\s+mqtt.*publish(?!.*try|except)
### **Message**
Sensor communication can fail. Handle errors gracefully.
### **Fix Action**
Wrap in try/except, use fallback or enter safe mode on failure
### **Applies To**
  - **/*.py