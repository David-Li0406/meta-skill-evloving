# Vr Ar Development - Validations

## Camera Movement Safety

### **Id**
check-camera-movement
### **Description**
Avoid automatic camera movement that causes motion sickness
### **Pattern**
camera\.(position|rotation).*=|camera\.lookAt
### **File Glob**
**/*.{js,ts,jsx,tsx}
### **Match**
present
### **Context Pattern**
controller|input|button|user
### **Message**
Ensure camera movement is user-initiated to prevent motion sickness
### **Severity**
error
### **Autofix**


## Frame Time Budget

### **Id**
check-frame-budget
### **Description**
XR requires 90fps (11ms) or better
### **Pattern**
setAnimationLoop|render\(
### **File Glob**
**/*.{js,ts,jsx,tsx}
### **Match**
present
### **Context Pattern**
performance|frameTime|budget
### **Message**
Monitor frame time to ensure 11ms budget for VR
### **Severity**
warning
### **Autofix**


## XR Renderer Enabled

### **Id**
check-xr-enabled
### **Description**
WebXR requires renderer.xr.enabled = true
### **Pattern**
WebGLRenderer
### **File Glob**
**/*.{js,ts,jsx,tsx}
### **Match**
present
### **Context Pattern**
xr\.enabled|VRButton|ARButton
### **Message**
Enable WebXR on renderer for VR/AR support
### **Severity**
warning
### **Autofix**


## Reference Space Configuration

### **Id**
check-reference-space
### **Description**
Set appropriate XR reference space
### **Pattern**
xr\.enabled
### **File Glob**
**/*.{js,ts,jsx,tsx}
### **Match**
present
### **Context Pattern**
setReferenceSpaceType|local-floor|bounded-floor
### **Message**
Configure XR reference space type
### **Severity**
info
### **Autofix**


## Tracking Loss Handling

### **Id**
check-tracking-loss
### **Description**
Handle tracking loss gracefully
### **Pattern**
getViewerPose|getPose
### **File Glob**
**/*.{js,ts,jsx,tsx}
### **Match**
present
### **Context Pattern**
null|undefined|!pose|tracking
### **Message**
Handle null pose when tracking is lost
### **Severity**
warning
### **Autofix**


## Controller Event Handling

### **Id**
check-controller-events
### **Description**
Handle XR controller input events
### **Pattern**
xr\.getController
### **File Glob**
**/*.{js,ts,jsx,tsx}
### **Match**
present
### **Context Pattern**
selectstart|selectend|squeeze
### **Message**
Add event listeners for XR controller input
### **Severity**
info
### **Autofix**


## UI Distance from Camera

### **Id**
check-ui-distance
### **Description**
UI should be at comfortable viewing distance
### **Pattern**
position.*-?[0-9]+\.?[0-9]*.*z|z.*=.*-?[0-9]
### **File Glob**
**/*.{js,ts,jsx,tsx}
### **Match**
present
### **Context Pattern**
ui|panel|text|button
### **Message**
Place UI at 0.5-2m distance for comfortable viewing
### **Severity**
info
### **Autofix**


## VR Text Size

### **Id**
check-text-size
### **Description**
Text must be large enough to read in VR
### **Pattern**
fontSize|textSize|font-size
### **File Glob**
**/*.{js,ts,jsx,tsx}
### **Match**
present
### **Context Pattern**
0\.0[2-9]|0\.1
### **Message**
Use minimum 0.02m (2cm) font size for VR readability
### **Severity**
info
### **Autofix**


## Safe Locomotion Method

### **Id**
check-locomotion
### **Description**
Use teleportation or snap turns for comfort
### **Pattern**
locomotion|movement|teleport|snap
### **File Glob**
**/*.{js,ts,jsx,tsx}
### **Match**
present
### **Context Pattern**
teleport|snap|blink|instant
### **Message**
Use teleportation or snap turns for motion sickness prevention
### **Severity**
warning
### **Autofix**


## XR Session Event Handling

### **Id**
check-session-events
### **Description**
Handle XR session start and end events
### **Pattern**
xr\.enabled
### **File Glob**
**/*.{js,ts,jsx,tsx}
### **Match**
present
### **Context Pattern**
sessionstart|sessionend|addEventListener
### **Message**
Handle XR session lifecycle events
### **Severity**
info
### **Autofix**
