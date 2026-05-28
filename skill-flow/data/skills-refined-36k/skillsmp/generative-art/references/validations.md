# Generative Art - Validations

## Seeded Random for Reproducibility

### **Id**
check-seeded-random
### **Description**
Use seeded random for reproducible generative art
### **Pattern**
random\(\)|Math\.random\(\)
### **File Glob**
**/*.{js,ts}
### **Match**
present
### **Context Pattern**
randomSeed|noiseSeed|seed|createRNG
### **Message**
Use seeded random for reproducible output
### **Severity**
warning
### **Autofix**


## Export/Save Functionality

### **Id**
check-save-function
### **Description**
Generative sketches should have export capability
### **Pattern**
createCanvas|canvas
### **File Glob**
**/*.{js,ts}
### **Match**
present
### **Context Pattern**
save|export|download|toDataURL
### **Message**
Add save/export functionality for high-resolution output
### **Severity**
info
### **Autofix**


## Intentional Color Palette

### **Id**
check-color-palette
### **Description**
Avoid default colors, use intentional palettes
### **Pattern**
fill\(255\)|stroke\(0\)|color\(255,\s*255,\s*255\)
### **File Glob**
**/*.{js,ts}
### **Match**
present
### **Message**
Avoid default colors - use intentional color palettes
### **Severity**
info
### **Autofix**


## Resolution Independence

### **Id**
check-resolution-independence
### **Description**
Use relative units for resolution-independent art
### **Pattern**
\d{3,}[^%]
### **File Glob**
**/*.{js,ts}
### **Match**
present
### **Context Pattern**
width|height|unit|ratio
### **Message**
Consider using relative units (% of width/height) for resolution independence
### **Severity**
info
### **Autofix**


## NFT Metadata Format

### **Id**
check-metadata-format
### **Description**
NFT metadata should follow standards
### **Pattern**
metadata|attributes|trait
### **File Glob**
**/*.{js,ts,json}
### **Match**
present
### **Context Pattern**
trait_type|value|name|description|image
### **Message**
Ensure metadata follows ERC-721/OpenSea standards
### **Severity**
warning
### **Autofix**


## Noise Seeding

### **Id**
check-noise-seed
### **Description**
Noise functions should be seeded for reproducibility
### **Pattern**
noise\(|perlin|simplex
### **File Glob**
**/*.{js,ts}
### **Match**
present
### **Context Pattern**
noiseSeed|seed
### **Message**
Seed noise functions for reproducible output
### **Severity**
warning
### **Autofix**


## Animation Frame Rate

### **Id**
check-frame-rate
### **Description**
Consider frame rate for animated pieces
### **Pattern**
draw\(\)|requestAnimationFrame|animate
### **File Glob**
**/*.{js,ts}
### **Match**
present
### **Context Pattern**
frameRate|fps|performance
### **Message**
Consider frame rate for animated generative art
### **Severity**
info
### **Autofix**


## Edge Case Handling

### **Id**
check-edge-cases
### **Description**
Handle edge cases in generative systems
### **Pattern**
weightedChoice|random.*select|pick
### **File Glob**
**/*.{js,ts}
### **Match**
present
### **Context Pattern**
fallback|default|constrain|clamp
### **Message**
Handle edge cases to prevent broken outputs
### **Severity**
warning
### **Autofix**


## Gradient Dithering

### **Id**
check-gradient-dithering
### **Description**
Add dithering to prevent gradient banding
### **Pattern**
gradient|lerp.*color|lerpColor
### **File Glob**
**/*.{js,ts}
### **Match**
present
### **Context Pattern**
noise|dither|random
### **Message**
Consider adding noise/dithering to prevent gradient banding
### **Severity**
info
### **Autofix**
