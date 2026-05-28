# Computer Vision Deep - Validations

## Vision Model Without Pretrained Weights

### **Id**
no-pretrained-backbone
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - pretrained\s*=\s*False
  - from_pretrained\s*=\s*False
  - weights\s*=\s*None
### **Message**
Training vision models from scratch is rarely optimal. Use pretrained weights.
### **Fix Action**
Use: pretrained=True or weights='imagenet'
### **Applies To**
  - **/*.py

## Image Training Without Augmentation

### **Id**
no-augmentation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - DataLoader\((?!.*transform|.*augment)
  - train_dataset(?!.*transform|.*augment)
### **Message**
Data augmentation significantly improves vision model generalization.
### **Fix Action**
Add augmentation transforms to training data
### **Applies To**
  - **/*train*.py

## Object Detection at Low Resolution

### **Id**
low-resolution-detection
### **Severity**
info
### **Type**
regex
### **Pattern**
  - imgsz\s*=\s*320
  - imgsz\s*=\s*416
  - input_size\s*=\s*[23]\d{2}
### **Message**
Low input resolution may miss small objects. Consider 640+ for better detection.
### **Fix Action**
Use: imgsz=640 or higher for small object detection
### **Applies To**
  - **/*.py

## Image Input Without Normalization

### **Id**
missing-normalize
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ToTensor\(\)(?!.*Normalize)
  - transforms\.Compose\(\[(?!.*Normalize)
### **Message**
Most vision models expect normalized input (ImageNet mean/std).
### **Fix Action**
Add: transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
### **Applies To**
  - **/*.py

## SAM Prediction Without set_image

### **Id**
sam-no-set-image
### **Severity**
error
### **Type**
regex
### **Pattern**
  - predictor\.predict\((?!.*set_image)
  - SamPredictor.*predict(?!.*set_image)
### **Message**
Call predictor.set_image() before predict() for SAM.
### **Fix Action**
Add: predictor.set_image(image) before predictions
### **Applies To**
  - **/*.py

## Bounding Box Format Not Specified

### **Id**
no-bbox-format
### **Severity**
info
### **Type**
regex
### **Pattern**
  - BboxParams\((?!.*format)
  - bbox_params\s*=(?!.*format)
### **Message**
Specify bbox format (yolo, pascal_voc, coco) for consistent augmentation.
### **Fix Action**
Add: format='yolo' or 'pascal_voc' or 'coco'
### **Applies To**
  - **/*.py

## Object Tracking Without Persistence

### **Id**
video-no-persist
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \.track\((?!.*persist)
### **Message**
Enable persist=True for consistent track IDs across frames.
### **Fix Action**
Add: persist=True in track() call
### **Applies To**
  - **/*.py