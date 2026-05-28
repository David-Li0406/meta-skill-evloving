# Ai Visual Effects - Validations

## Source resolution should be adequate for output

### **Id**
source-resolution-adequate
### **Severity**
high
### **Description**
Upscaling can't create missing information
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
upscale.*(480|360|240|144)p
  #### **Exclude**
test|sample|preview
### **Message**
Upscaling very low resolution source. Quality will be limited.
### **Autofix**


## Video processing should maintain temporal consistency

### **Id**
temporal-consistency-video
### **Severity**
high
### **Description**
Frame-by-frame processing causes flickering
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
for.*frame|forEach.*frame|process.*image
  #### **Exclude**
temporal|video|sequence|consistent|batch
### **Message**
Processing frames individually. Use video-aware processing for temporal consistency.
### **Autofix**


## Original files should be preserved

### **Id**
original-preserved
### **Severity**
high
### **Description**
Non-destructive workflow requires originals
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
overwrite|replace.*original|delete.*source
  #### **Exclude**
backup|copy|version|archive|preserve
### **Message**
Operation may overwrite originals. Preserve source files before processing.
### **Autofix**


## Upscaler model should match content type

### **Id**
upscaler-matches-content
### **Severity**
medium
### **Description**
Photo models on anime (or vice versa) produce poor results
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml}
  #### **Match**
(anime|illustration).*esrgan|(photo|realistic).*waifu
  #### **Exclude**
appropriate|match|detect|auto
### **Message**
Upscaler may not match content type. Select appropriate model.
### **Autofix**


## Composited elements should have color matching

### **Id**
color-matching-composite
### **Severity**
medium
### **Description**
Color mismatch destroys composite believability
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
composite|merge|overlay.*ai.*footage
  #### **Exclude**
color|grade|match|lut|correct
### **Message**
Compositing without color matching. Add color correction step.
### **Autofix**


## Composited elements should have edge treatment

### **Id**
edge-treatment-exists
### **Severity**
medium
### **Description**
Poor edges make composites obvious
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
composite|alpha.*blend|mask
  #### **Exclude**
edge|feather|blur|refine
### **Message**
Compositing without edge treatment. Add edge refinement.
### **Autofix**


## AI elements should match footage grain

### **Id**
grain-matching
### **Severity**
medium
### **Description**
Clean AI elements in grainy footage look fake
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
composite.*ai.*video|merge.*generated
  #### **Exclude**
grain|noise|texture|match
### **Message**
Compositing AI into footage without grain matching. Add grain/noise.
### **Autofix**


## Resolution should be consistent through pipeline

### **Id**
resolution-pipeline-planned
### **Severity**
medium
### **Description**
Unnecessary resolution changes lose quality
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
upscale.*resize|scale.*upscale
  #### **Exclude**
final|output|delivery
### **Message**
Multiple resolution changes in pipeline. Plan resolution workflow.
### **Autofix**


## ComfyUI workflows should be documented

### **Id**
workflow-documented
### **Severity**
low
### **Description**
Complex workflows need documentation for reuse
### **Pattern**
  #### **File Glob**
**/*.json
  #### **Match**
ComfyUI|workflow
  #### **Exclude**
readme|doc|comment|note
### **Message**
ComfyUI workflow may lack documentation. Add notes and README.
### **Autofix**


## Intermediate exports should use high quality codec

### **Id**
intermediate-quality
### **Severity**
low
### **Description**
Lossy compression mid-workflow degrades quality
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
export.*h264|encode.*mp4.*intermediate
  #### **Exclude**
prores|dnxhd|lossless|high.*quality
### **Message**
Intermediate export using lossy compression. Use ProRes/DNxHR.
### **Autofix**


## VFX projects should have version control

### **Id**
version-control
### **Severity**
low
### **Description**
Version control enables iteration and recovery
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
save.*project|export.*final
  #### **Exclude**
version|v\d|_v|backup
### **Message**
Saving without versioning. Add version numbers to files.
### **Autofix**


## Processing should include quality comparison

### **Id**
ab-comparison
### **Severity**
low
### **Description**
Easy to degrade quality without noticing
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
process|enhance|upscale
  #### **Exclude**
compare|original|before|quality.*check
### **Message**
Processing without comparison step. Verify improvement vs original.
### **Autofix**
