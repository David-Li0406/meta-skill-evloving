# Demoscene Coding - Validations

## Time-Based Animation

### **Id**
check-time-based-animation
### **Description**
Animations should use time, not frame count
### **Pattern**
requestAnimationFrame|render|animate
### **File Glob**
**/*.{js,ts}
### **Match**
present
### **Context Pattern**
now|time|Date|performance
### **Message**
Use time-based animation (pass 'now' from requestAnimationFrame)
### **Severity**
warning
### **Autofix**


## GLSL Precision Qualifier

### **Id**
check-precision-qualifier
### **Description**
GLSL shaders should specify precision explicitly
### **Pattern**
precision\s+(lowp|mediump|highp)\s+float
### **File Glob**
**/*.{glsl,frag,vert,js,ts}
### **Match**
present
### **Context Pattern**
void\s+main|gl_FragColor|out\s+vec4
### **Message**
Add explicit precision qualifier to shader
### **Severity**
warning
### **Autofix**


## Audio Context User Interaction

### **Id**
check-audio-context-interaction
### **Description**
AudioContext should be created after user interaction
### **Pattern**
new\s+AudioContext|audioContext\.resume
### **File Glob**
**/*.{js,ts}
### **Match**
present
### **Context Pattern**
click|keydown|touchstart|onclick
### **Message**
Create AudioContext only after user interaction (click, key, touch)
### **Severity**
error
### **Autofix**


## Division By Zero Guard

### **Id**
check-division-by-zero
### **Description**
Division operations should guard against zero
### **Pattern**
1\.|length|distance|normalize
### **File Glob**
**/*.{glsl,frag,vert}
### **Match**
present
### **Context Pattern**
\+\s*0\.0+1|max\s*\(|clamp|step
### **Message**
Guard division by zero with epsilon or max()
### **Severity**
warning
### **Autofix**


## GLSL Variable Initialization

### **Id**
check-variable-initialization
### **Description**
Variables should be initialized to avoid undefined behavior
### **Pattern**
(float|vec[234]|mat[234])\s+\w+\s*;
### **File Glob**
**/*.{glsl,frag,vert}
### **Match**
absent
### **Message**
Initialize variables to avoid undefined behavior
### **Severity**
warning
### **Autofix**


## WebGL Context Fallback

### **Id**
check-webgl-context-fallback
### **Description**
Should have fallback if WebGL2 unavailable
### **Pattern**
getContext\(['"]webgl2['"]\)
### **File Glob**
**/*.{js,ts}
### **Match**
present
### **Context Pattern**
getContext\(['"]webgl['"]\)|catch|fallback
### **Message**
Add WebGL1 fallback for broader compatibility
### **Severity**
info
### **Autofix**


## Viewport Resize Handler

### **Id**
check-viewport-resize
### **Description**
Canvas should handle window resize
### **Pattern**
canvas\.width|renderer\.setSize|viewport
### **File Glob**
**/*.{js,ts}
### **Match**
present
### **Context Pattern**
resize|innerWidth|innerHeight
### **Message**
Handle window resize for different display sizes
### **Severity**
warning
### **Autofix**


## Audio Gain Safety

### **Id**
check-audio-clipping
### **Description**
Multiple audio sources should be properly mixed to prevent clipping
### **Pattern**
createOscillator|createGain|connect
### **File Glob**
**/*.{js,ts}
### **Match**
present
### **Context Pattern**
gain\.value|compressor|limiter|master
### **Message**
Use proper gain staging or compressor to prevent audio clipping
### **Severity**
info
### **Autofix**


## Shader Loop Bounds

### **Id**
check-loop-bounds
### **Description**
Loops should have reasonable upper bounds
### **Pattern**
for\s*\(\s*int\s+\w+\s*=\s*\d+\s*;[^;]+<\s*(\d+)
### **File Glob**
**/*.{glsl,frag,vert}
### **Match**
present
### **Message**
Ensure loop bounds are reasonable for all GPUs
### **Severity**
info
### **Autofix**


## Texture Coordinate Safety

### **Id**
check-texture-coord-safety
### **Description**
Texture coordinates should be clamped or wrapped
### **Pattern**
texture\s*\(
### **File Glob**
**/*.{glsl,frag,vert}
### **Match**
present
### **Context Pattern**
fract|clamp|mod
### **Message**
Ensure texture coordinates are properly wrapped or clamped
### **Severity**
info
### **Autofix**
