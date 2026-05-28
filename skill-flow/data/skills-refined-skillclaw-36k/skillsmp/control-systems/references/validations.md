# Control Systems - Validations

## Derivative Computed on Error

### **Id**
derivative-on-error
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - error\s*-\s*prev_error|prev_error\s*-\s*error
  - self\.error\s*-\s*self\.prev_error
  - d_term.*error.*prev
### **Message**
Computing derivative on error causes derivative kick on setpoint change.
### **Fix Action**
Use derivative on measurement: -(measurement - prev_measurement) / dt
### **Applies To**
  - **/*.py

## PID Without Anti-Windup

### **Id**
no-anti-windup
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - integral\s*\+=.*error.*dt(?![\s\S]{0,200}(clip|clamp|windup|limit|saturate))
### **Message**
Integral accumulation without anti-windup causes overshoot when saturated.
### **Fix Action**
Add clamping or back-calculation anti-windup
### **Applies To**
  - **/*.py

## PID Without Output Limits

### **Id**
no-output-limits
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - class.*PID.*:(?![\s\S]{0,500}(output_max|u_max|limit|clip|clamp))
### **Message**
PID controller should have output limits matching actuator constraints.
### **Fix Action**
Add output_limits parameter and clamp control output
### **Applies To**
  - **/*.py

## Unfiltered Derivative Term

### **Id**
raw-derivative
### **Severity**
info
### **Type**
regex
### **Pattern**
  - /\s*dt(?![\s\S]{0,50}(filter|alpha|tau|lpf))
  - d_term\s*=.*-.*prev.*(?!filter)
### **Message**
Unfiltered derivative amplifies high-frequency noise.
### **Fix Action**
Add low-pass filter: d_filt = alpha * d_raw + (1-alpha) * d_prev
### **Applies To**
  - **/*.py

## Simple Euler Integration for Integral Term

### **Id**
euler-integration
### **Severity**
info
### **Type**
regex
### **Pattern**
  - integral\s*\+=\s*error\s*\*\s*dt
### **Message**
Simple Euler integration can accumulate error. Consider trapezoidal integration.
### **Fix Action**
Use: integral += 0.5 * (error + prev_error) * dt for better accuracy
### **Applies To**
  - **/*.py

## Control Loop with sleep() Call

### **Id**
slow-control-loop
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - time\.sleep\(0\.[1-9]|time\.sleep\([1-9]
  - rospy\.sleep\(0\.[1-9]
### **Message**
Control loop may be too slow. Use hardware timer for consistent timing.
### **Fix Action**
Use hardware timer interrupt or ROS2 timer for precise control loop
### **Applies To**
  - **/*.py

## MPC Without Input Constraints

### **Id**
mpc-no-constraints
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - class.*MPC.*:(?![\s\S]{0,800}(u_min|u_max|bounds|constraint))
### **Message**
MPC without constraints loses main advantage. Add actuator limits.
### **Fix Action**
Add u_min/u_max constraints matching physical actuator limits
### **Applies To**
  - **/*.py

## Hardcoded PID Gains Without Comments

### **Id**
hardcoded-gains
### **Severity**
info
### **Type**
regex
### **Pattern**
  - kp\s*=\s*\d+\.?\d*\s*(?!#)
  - ki\s*=\s*\d+\.?\d*\s*(?!#)
  - PIDGains\(kp=\d+.*\)\s*$
### **Message**
Document tuning rationale for PID gains, or load from config.
### **Fix Action**
Add comment explaining tuning method, or use parameter server
### **Applies To**
  - **/*.py

## Step Setpoint Without Trajectory Generation

### **Id**
no-trajectory-filter
### **Severity**
info
### **Type**
regex
### **Pattern**
  - setpoint\s*=\s*target(?![\s\S]{0,100}(filter|ramp|trajectory|profile))
### **Message**
Sudden setpoint changes stress mechanical systems.
### **Fix Action**
Use trajectory generator (minimum-jerk, trapezoidal) for smooth motion
### **Applies To**
  - **/*.py

## Float Equality in Control Logic

### **Id**
floating-point-comparison
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - if.*error\s*==\s*0
  - if.*position\s*==\s*setpoint
### **Message**
Floating-point equality rarely holds. Use tolerance-based comparison.
### **Fix Action**
Use: if abs(error) < tolerance or np.isclose()
### **Applies To**
  - **/*.py

## LQR/MPC Without Explicit Jacobian

### **Id**
jacobian-missing
### **Severity**
info
### **Type**
regex
### **Pattern**
  - lqr|LQR|design_lqr(?![\s\S]{0,300}jacobian)
### **Message**
Ensure linearization Jacobian is computed correctly for nonlinear systems.
### **Fix Action**
Verify Jacobian analytically or use automatic differentiation
### **Applies To**
  - **/*.py