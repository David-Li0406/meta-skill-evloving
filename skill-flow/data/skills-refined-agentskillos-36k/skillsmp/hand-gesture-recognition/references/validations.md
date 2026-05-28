# Hand Gesture Recognition - Validations

## Gesture Confidence Threshold

### **Id**
check-confidence-threshold
### **Description**
Gestures should have confidence thresholds to prevent false positives
### **Pattern**
detectGesture|classify.*gesture
### **File Glob**
**/*.{js,ts,jsx,tsx,py}
### **Match**
present
### **Context Pattern**
confidence|threshold|score
### **Message**
Add confidence threshold for gesture detection to prevent false positives
### **Severity**
warning
### **Autofix**


## Camera Permission Handling

### **Id**
check-camera-permissions
### **Description**
getUserMedia should have proper error handling
### **Pattern**
getUserMedia|navigator.mediaDevices
### **File Glob**
**/*.{js,ts,jsx,tsx}
### **Match**
present
### **Context Pattern**
catch|NotAllowedError|NotFoundError
### **Message**
Handle camera permission errors gracefully
### **Severity**
error
### **Autofix**


## Model Loading State

### **Id**
check-loading-state
### **Description**
Show loading state while ML model initializes
### **Pattern**
new Hands|handpose|hand.*model
### **File Glob**
**/*.{js,ts,jsx,tsx}
### **Match**
present
### **Context Pattern**
loading|progress|initialize
### **Message**
Show loading state during model initialization
### **Severity**
warning
### **Autofix**


## Fallback Input Method

### **Id**
check-fallback-input
### **Description**
Provide alternative input when gestures aren't available
### **Pattern**
gesture.*control|hand.*interface
### **File Glob**
**/*.{js,ts,jsx,tsx}
### **Match**
present
### **Context Pattern**
keyboard|mouse|fallback|alternative
### **Message**
Provide keyboard/mouse fallback for accessibility
### **Severity**
warning
### **Autofix**


## WebGL Feature Detection

### **Id**
check-feature-detection
### **Description**
Check for WebGL/WASM support before using hand tracking
### **Pattern**
mediapipe|handpose|tensorflow
### **File Glob**
**/*.{js,ts,jsx,tsx}
### **Match**
present
### **Context Pattern**
webgl|WebAssembly|getContext
### **Message**
Check WebGL/WASM support before initializing hand tracking
### **Severity**
warning
### **Autofix**


## Resource Cleanup

### **Id**
check-cleanup
### **Description**
Clean up camera and model resources on unmount
### **Pattern**
getUserMedia|new Hands
### **File Glob**
**/*.{js,ts,jsx,tsx}
### **Match**
present
### **Context Pattern**
stop|dispose|cleanup|close
### **Message**
Clean up camera stream and model when component unmounts
### **Severity**
warning
### **Autofix**


## Gesture Smoothing

### **Id**
check-gesture-smoothing
### **Description**
Raw gesture detection should be smoothed for stability
### **Pattern**
detectGesture|onResults
### **File Glob**
**/*.{js,ts,jsx,tsx}
### **Match**
present
### **Context Pattern**
smooth|history|buffer|debounce
### **Message**
Apply smoothing to prevent jittery gesture detection
### **Severity**
info
### **Autofix**


## Handedness Handling

### **Id**
check-handedness
### **Description**
Account for left vs right hand differences
### **Pattern**
thumb|finger.*extended
### **File Glob**
**/*.{js,ts,jsx,tsx}
### **Match**
present
### **Context Pattern**
handedness|left|right|hand
### **Message**
Account for left vs right hand when detecting gestures
### **Severity**
info
### **Autofix**


## Lighting Quality Feedback

### **Id**
check-lighting-feedback
### **Description**
Provide feedback about lighting conditions
### **Pattern**
hand.*track|gesture.*detect
### **File Glob**
**/*.{js,ts,jsx,tsx}
### **Match**
present
### **Context Pattern**
lighting|brightness|exposure
### **Message**
Consider providing lighting quality feedback to users
### **Severity**
info
### **Autofix**


## HTTPS for Camera Access

### **Id**
check-https-camera
### **Description**
Camera requires HTTPS in production
### **Pattern**
getUserMedia
### **File Glob**
**/*.{js,ts,jsx,tsx,html}
### **Match**
present
### **Context Pattern**
https|localhost|secure
### **Message**
Camera access requires HTTPS in production
### **Severity**
info
### **Autofix**
