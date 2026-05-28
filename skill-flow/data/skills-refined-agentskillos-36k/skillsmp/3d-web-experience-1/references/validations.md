# 3D Web Experience - Validations

## No 3D Loading Indicator

### **Id**
no-loading-state
### **Severity**
high
### **Type**
conceptual
### **Check**
Should show loading state while 3D loads
### **Indicators**
  - No Suspense around Canvas
  - No loading progress
  - Blank screen during load
### **Message**
No loading indicator for 3D content.
### **Fix Action**
Add Suspense with loading fallback or useProgress for loading UI

## No WebGL Fallback

### **Id**
no-webgl-fallback
### **Severity**
medium
### **Type**
conceptual
### **Check**
Should have fallback for devices without WebGL
### **Indicators**
  - No WebGL detection
  - No static fallback image
  - Crashes on unsupported devices
### **Message**
No fallback for devices without WebGL support.
### **Fix Action**
Add WebGL detection and static image fallback

## Uncompressed 3D Models

### **Id**
uncompressed-models
### **Severity**
medium
### **Type**
pattern
### **Check**
3D models should be compressed
### **Pattern**
\.glb|\.gltf
### **Indicators**
  - GLB files over 5MB
  - No Draco compression
  - Large texture files
### **Message**
3D models may be unoptimized.
### **Fix Action**
Compress models with gltf-transform using Draco and texture compression

## OrbitControls Blocking Scroll

### **Id**
orbit-controls-scroll
### **Severity**
medium
### **Type**
pattern
### **Check**
OrbitControls should not block page scroll
### **Pattern**
OrbitControls
### **Indicators**
  - enableZoom not disabled
  - Scroll captured by 3D
  - Can't scroll page
### **Message**
OrbitControls may be capturing scroll events.
### **Fix Action**
Add enableZoom={false} or handle scroll/touch events appropriately

## High DPR on Mobile

### **Id**
high-dpr-mobile
### **Severity**
medium
### **Type**
pattern
### **Check**
Canvas DPR should be limited on mobile
### **Pattern**
dpr.*\[|dpr=
### **Indicators**
  - Full DPR on mobile
  - Performance issues on phones
  - Battery drain
### **Message**
Canvas DPR may be too high for mobile devices.
### **Fix Action**
Limit DPR to 1 on mobile devices for better performance