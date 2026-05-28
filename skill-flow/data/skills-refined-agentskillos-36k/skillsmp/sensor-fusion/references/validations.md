# Sensor Fusion - Validations

## Identity Matrix for Noise Covariance

### **Id**
identity-noise-matrix
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \bQ\s*=\s*np\.eye\s*\(
  - \bR\s*=\s*np\.eye\s*\(
  - self\.Q\s*=\s*np\.eye
  - self\.R\s*=\s*np\.eye
### **Message**
Using identity matrix for Q or R suggests untuned noise parameters. Calibrate from sensor data.
### **Fix Action**
Use Allan variance for IMU, measure sensor variance empirically
### **Applies To**
  - **/*.py

## Non-Joseph Form Covariance Update

### **Id**
non-joseph-update
### **Severity**
info
### **Type**
regex
### **Pattern**
  - P\s*=\s*\([^)]*-\s*K\s*@\s*H\s*\)\s*@\s*P
  - self\.P\s*=\s*\(.*I.*-.*K.*H.*\)\s*@\s*self\.P(?!.*@)
### **Message**
Use Joseph form for covariance update to maintain positive-definiteness.
### **Fix Action**
Use: P = (I - K @ H) @ P @ (I - K @ H).T + K @ R @ K.T
### **Applies To**
  - **/*.py

## Kalman Update Without Outlier Rejection

### **Id**
no-outlier-rejection
### **Severity**
info
### **Type**
regex
### **Pattern**
  - def\s+update.*:\s*[^}]*K\s*@\s*y(?![\s\S]{0,200}mahalanobis|gate|chi2)
### **Message**
Consider adding Mahalanobis gating to reject outlier measurements.
### **Fix Action**
Add chi-squared test on innovation before update
### **Applies To**
  - **/*.py

## Manual Jacobian Without Verification

### **Id**
manual-jacobian
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - def\s+.*jacobian.*:\s*[^}]*\bF\s*=\s*np\.
  - def\s+.*jacobian.*:\s*[^}]*\bH\s*=\s*np\.
### **Message**
Manual Jacobians are error-prone. Consider automatic differentiation or numerical verification.
### **Fix Action**
Use JAX/PyTorch autodiff, or verify against numerical Jacobian
### **Applies To**
  - **/*.py

## Using Arrival Time Instead of Sensor Time

### **Id**
arrival-time-fusion
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - time\.time\(\).*update
  - rospy\.Time\.now\(\).*(?!header\.stamp)
  - self\.get_clock\(\)\.now\(\).*(?!msg\.header)
### **Message**
Using current time instead of sensor timestamp causes fusion lag.
### **Fix Action**
Use msg.header.stamp or sensor's hardware timestamp
### **Applies To**
  - **/*.py

## No Minimum Covariance Enforcement

### **Id**
no-covariance-bounds
### **Severity**
info
### **Type**
regex
### **Pattern**
  - class.*Kalman.*:(?![\s\S]{0,500}min_cov|eigval|positive_definite)
### **Message**
Consider adding minimum covariance bounds to prevent filter collapse.
### **Fix Action**
Add eigenvalue check and enforce minimum variance
### **Applies To**
  - **/*.py

## Quaternion Not Normalized After Update

### **Id**
unit-quaternion-violation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - q\s*\+=.*(?![\s\S]{0,50}normalize|/.*norm)
  - self\.q\s*=.*\+.*(?![\s\S]{0,50}/)
### **Message**
Quaternions must be normalized after updates to maintain unit constraint.
### **Fix Action**
Add: q = q / np.linalg.norm(q) after quaternion operations
### **Applies To**
  - **/*.py

## Angle State Without Wrapping

### **Id**
angle-wrap-missing
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (theta|yaw|heading|psi).*\+=(?![\s\S]{0,100}wrap|atan2|mod)
### **Message**
Angle states should be wrapped to [-pi, pi] to avoid discontinuities.
### **Fix Action**
Use np.arctan2(np.sin(angle), np.cos(angle)) to wrap angles
### **Applies To**
  - **/*.py

## No Filter Consistency Monitoring

### **Id**
no-filter-health-check
### **Severity**
info
### **Type**
regex
### **Pattern**
  - class.*Kalman.*:(?![\s\S]{0,800}NEES|NIS|innovation|chi2|health)
### **Message**
Add NEES/NIS monitoring to detect filter inconsistency.
### **Fix Action**
Compute normalized innovation and compare to chi-squared bounds
### **Applies To**
  - **/*.py

## Extremely Large Initial Covariance

### **Id**
large-initial-covariance
### **Severity**
info
### **Type**
regex
### **Pattern**
  - P\s*=\s*np\.eye.*\*\s*(1e[3-9]|1e\d{2,}|10{4,})
### **Message**
Very large initial covariance may cause numerical issues. Use realistic uncertainty.
### **Fix Action**
Set P0 based on actual initial state uncertainty
### **Applies To**
  - **/*.py

## Multiple Sensors in Single Update

### **Id**
synchronous-fusion
### **Severity**
info
### **Type**
regex
### **Pattern**
  - update.*imu.*gps|update.*gps.*imu
  - kf\.update.*\[.*imu.*gps.*\]
### **Message**
Fusing multiple sensors simultaneously may lose timing information.
### **Fix Action**
Consider sequential updates with proper timestamps
### **Applies To**
  - **/*.py