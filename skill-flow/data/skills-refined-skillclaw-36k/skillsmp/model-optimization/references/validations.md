# Model Optimization - Validations

## Static Quantization Without Calibration

### **Id**
no-calibration-data
### **Severity**
error
### **Type**
regex
### **Pattern**
  - quantization\.convert\((?!.*calibrat)
  - prepare\(.*\).*convert\((?!.*for.*in)
### **Message**
Static quantization requires calibration data for accurate activation ranges.
### **Fix Action**
Add calibration loop before convert()
### **Applies To**
  - **/*.py

## ONNX Export Without Dynamic Axes

### **Id**
onnx-no-dynamic-axes
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - torch\.onnx\.export\((?!.*dynamic_axes)
  - onnx\.export\((?!.*dynamic_axes)
### **Message**
ONNX export without dynamic_axes creates fixed-shape model.
### **Fix Action**
Add: dynamic_axes={'input': {0: 'batch'}, 'output': {0: 'batch'}}
### **Applies To**
  - **/*.py

## Quantization Without model.eval()

### **Id**
no-model-eval
### **Severity**
error
### **Type**
regex
### **Pattern**
  - quantize_dynamic\((?!.*\.eval\(\))
  - prepare\((?!.*\.eval\(\))
### **Message**
Model must be in eval mode before quantization.
### **Fix Action**
Add: model.eval() before quantization
### **Applies To**
  - **/*.py

## ONNX Export Without Opset Version

### **Id**
missing-opset-version
### **Severity**
info
### **Type**
regex
### **Pattern**
  - torch\.onnx\.export\((?!.*opset_version)
### **Message**
Specify opset_version for reproducible ONNX export.
### **Fix Action**
Add: opset_version=17 (or appropriate version)
### **Applies To**
  - **/*.py

## FP16 Training Without GradScaler

### **Id**
fp16-no-scaler
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - autocast.*float16(?!.*GradScaler)
  - torch\.float16.*backward\(\)(?!.*scaler)
### **Message**
FP16 training needs GradScaler to prevent gradient underflow.
### **Fix Action**
Use: scaler = GradScaler(); scaler.scale(loss).backward()
### **Applies To**
  - **/*train*.py

## Quantizing Untrained Model

### **Id**
quantize-before-train
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - quantize.*\n.*\.train\(
  - prepare_qat.*\n.*for.*epoch.*range\(\d{2,}\)
### **Message**
Model should be trained before quantization for best results.
### **Fix Action**
Train model first, then apply quantization
### **Applies To**
  - **/*.py

## ONNX Export Without Validation

### **Id**
no-onnx-check
### **Severity**
info
### **Type**
regex
### **Pattern**
  - torch\.onnx\.export\((?!.*onnx\.checker|onnx\.load)
### **Message**
Validate ONNX export with onnx.checker.check_model().
### **Fix Action**
Add: onnx.checker.check_model(onnx.load(path))
### **Applies To**
  - **/*.py