# Computer Vision Deep

## Patterns

### **Golden Rules**
  
---
    ##### **Rule**
YOLO for speed, SAM for accuracy
    ##### **Reason**
Different tools for different constraints
  
---
    ##### **Rule**
YOLO + SAM hybrid is powerful
    ##### **Reason**
Detection boxes → SAM masks
  
---
    ##### **Rule**
Anchor-free is the future
    ##### **Reason**
YOLO v8+ are anchor-free, simpler
  
---
    ##### **Rule**
Resolution matters enormously
    ##### **Reason**
2x resolution ≈ 4x compute, better small objects
  
---
    ##### **Rule**
Data augmentation is critical
    ##### **Reason**
Geometric + color augmentations improve robustness
  
---
    ##### **Rule**
Pre-trained backbones always
    ##### **Reason**
ImageNet/CLIP pretrained >>> random init
### **Task Landscape**
  #### **Image Classification**
    ##### **Description**
What is in the image?
    ##### **Output**
Single label or multi-label
    ##### **Models**
      - ResNet
      - ViT
      - EfficientNet
      - ConvNeXt
  #### **Object Detection**
    ##### **Description**
Where are objects?
    ##### **Output**
Bounding boxes + classes
    ##### **Models**
      - YOLO
      - DETR
      - Faster R-CNN
  #### **Semantic Segmentation**
    ##### **Description**
Pixel-wise classification
    ##### **Output**
All cars = same class
    ##### **Models**
      - DeepLab
      - SegFormer
      - UNet
  #### **Instance Segmentation**
    ##### **Description**
Separate each object instance
    ##### **Output**
Car 1, Car 2, Car 3 distinct
    ##### **Models**
      - Mask R-CNN
      - YOLO-Seg
      - SAM
  #### **Panoptic Segmentation**
    ##### **Description**
Semantic + Instance unified
    ##### **Models**
      - Panoptic FPN
      - MaskFormer
      - Mask2Former
### **Yolo Models**
  #### **Yolov8N**
    ##### **Params**
3.2M
    ##### **Map**
37.3
    ##### **Speed Ms**
1.2
    ##### **Use Case**
Edge, mobile
  #### **Yolov8S**
    ##### **Params**
11.2M
    ##### **Map**
44.9
    ##### **Speed Ms**
1.8
    ##### **Use Case**
Balanced
  #### **Yolov8M**
    ##### **Params**
25.9M
    ##### **Map**
50.2
    ##### **Speed Ms**
3.4
    ##### **Use Case**
Accuracy focus
  #### **Yolov8L**
    ##### **Params**
43.7M
    ##### **Map**
52.9
    ##### **Speed Ms**
5.0
    ##### **Use Case**
High accuracy
  #### **Yolov8X**
    ##### **Params**
68.2M
    ##### **Map**
53.9
    ##### **Speed Ms**
8.1
    ##### **Use Case**
Maximum accuracy
### **Foundation Models**
  #### **Sam**
    ##### **Description**
Segment Anything Model
    ##### **Capabilities**
      - Zero-shot segmentation
      - Point/box/text prompts
      - High-quality masks
  #### **Clip**
    ##### **Description**
Contrastive Language-Image Pre-training
    ##### **Capabilities**
      - Zero-shot classification
      - Image-text matching
      - Feature extraction
  #### **Dino**
    ##### **Description**
Self-supervised vision transformer
    ##### **Capabilities**
      - Self-supervised features
      - Part discovery
      - Correspondence

## Anti-Patterns


---
  #### **Pattern**
Training from scratch
  #### **Problem**
Slow, poor results
  #### **Solution**
Always use pretrained backbone

---
  #### **Pattern**
Low resolution for small objects
  #### **Problem**
Missing detections
  #### **Solution**
Increase input resolution

---
  #### **Pattern**
No augmentation
  #### **Problem**
Overfitting
  #### **Solution**
Strong augmentation pipeline

---
  #### **Pattern**
Wrong anchor sizes
  #### **Problem**
Poor box regression
  #### **Solution**
Anchor-free (YOLO v8+) or cluster anchors

---
  #### **Pattern**
Ignoring class imbalance
  #### **Problem**
Biased predictions
  #### **Solution**
Focal loss, oversampling

---
  #### **Pattern**
Not using SAM for annotation
  #### **Problem**
Slow manual annotation
  #### **Solution**
SAM-assisted labeling