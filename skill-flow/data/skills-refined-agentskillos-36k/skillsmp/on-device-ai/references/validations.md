# On Device Ai - Validations

## No WebGPU Fallback

### **Id**
no-webgpu-check
### **Severity**
error
### **Description**
Must check WebGPU support and provide fallback
### **Pattern**
  device.*webgpu(?!.*fallback|wasm|check|navigator\.gpu)
  
### **Message**
Check WebGPU support and fallback to WASM for unsupported browsers.
### **Autofix**


## No GPU Capability Check

### **Id**
no-gpu-capability-check
### **Severity**
warning
### **Description**
Check device capabilities before loading models
### **Pattern**
  pipeline|CreateMLCEngine(?!.*capability|device.*check|memory)
  
### **Message**
Check device capabilities before loading large models.
### **Autofix**


## Large Model on Mobile

### **Id**
large-model-mobile
### **Severity**
error
### **Description**
Don't load 7B+ models on mobile devices
### **Pattern**
  7B|8B|13B(?!.*isMobile|mobile.*check|device.*detect)
  
### **Message**
Models over 3B parameters are too large for mobile. Add device detection.
### **Autofix**


## No Memory Check

### **Id**
no-memory-check
### **Severity**
warning
### **Description**
Check available memory before loading models
### **Pattern**
  CreateMLCEngine|pipeline(?!.*memory|checkMemory|available)
  
### **Message**
Check available memory before loading models to prevent crashes.
### **Autofix**


## Multiple Models Loaded

### **Id**
multiple-models-loaded
### **Severity**
warning
### **Description**
Loading multiple models may exhaust memory
### **Pattern**
  pipeline.*await.*pipeline(?!.*unload|dispose)
  
### **Message**
Loading multiple models may exhaust memory. Consider unloading between uses.
### **Autofix**


## No Loading Progress UI

### **Id**
no-loading-progress
### **Severity**
warning
### **Description**
Show progress during model download
### **Pattern**
  CreateMLCEngine|pipeline(?!.*progress|initProgressCallback|progress_callback)
  
### **Message**
Show loading progress to users during model download.
### **Autofix**


## Blocking Main Thread

### **Id**
blocking-main-thread
### **Severity**
warning
### **Description**
Heavy inference should use Web Workers
### **Pattern**
  await.*generate(?!.*Worker|worker)
  
### **Message**
Consider using Web Workers for inference to prevent UI blocking.
### **Autofix**


## No Loading State

### **Id**
no-loading-state
### **Severity**
info
### **Description**
Track and display loading state
### **Pattern**
  pipeline.*useState(?!.*loading|isLoading|progress)
  
### **Message**
Track loading state to show appropriate UI during model initialization.
### **Autofix**


## No Model Loading Error Handling

### **Id**
no-model-error-handling
### **Severity**
error
### **Description**
Handle model loading failures gracefully
### **Pattern**
  await.*pipeline|CreateMLCEngine(?!.*catch|try|error)
  
### **Message**
Handle model loading errors with try/catch and fallback UI.
### **Autofix**


## No Inference Error Handling

### **Id**
no-inference-error-handling
### **Severity**
warning
### **Description**
Handle inference failures
### **Pattern**
  await.*generate|model\((?!.*catch|try|error)
  
### **Message**
Handle inference errors gracefully.
### **Autofix**


## Wrong Quantization for Task

### **Id**
wrong-quantization
### **Severity**
warning
### **Description**
Use appropriate quantization for task type
### **Pattern**
  q4.*code|math|precise|embedding
  
### **Message**
Q4 quantization may be too aggressive for code/math tasks. Use Q8 or FP16.
### **Autofix**


## No Model Caching Strategy

### **Id**
no-model-caching
### **Severity**
info
### **Description**
Implement caching for faster subsequent loads
### **Pattern**
  pipeline|CreateMLCEngine(?!.*cache|useBrowserCache)
  
### **Message**
Enable browser caching for faster model loads on subsequent visits.
### **Autofix**


## Parallel Inference Calls

### **Id**
parallel-inference
### **Severity**
error
### **Description**
Avoid concurrent model inference
### **Pattern**
  Promise\.all.*generate|Promise\.all.*model\(
  
### **Message**
Avoid parallel inference - queue requests instead to prevent memory issues.
### **Autofix**
