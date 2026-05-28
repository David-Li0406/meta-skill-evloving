# Computer Vision Deep - Sharp Edges

## Missing Small Object Detections

### **Id**
resolution-small-objects
### **Severity**
critical
### **Summary**
Input resolution too low for small objects
### **Symptoms**
  - Small objects not detected
  - Works on large objects, fails on small
  - Recall drops dramatically for small objects
### **Why**
  Object detectors need minimum feature map size to detect.
  At 640x640, a 10x10 pixel object becomes 1x1 on final feature map.
  Below threshold, object becomes undetectable.
  
### **Gotcha**
  # Default resolution misses small objects
  model = YOLO('yolov8n.pt')
  results = model(image, imgsz=640)  # 10px objects invisible
  
  # Looking for defects, small products, distant objects
  
### **Solution**
  # Higher resolution for small objects
  results = model(image, imgsz=1280)  # 2x resolution
  
  # Or use tiled inference
  from sahi import AutoDetectionModel, get_sliced_prediction
  
  detection_model = AutoDetectionModel.from_pretrained(
      model_type="yolov8",
      model_path="yolov8n.pt",
  )
  
  result = get_sliced_prediction(
      image,
      detection_model,
      slice_height=640,
      slice_width=640,
      overlap_height_ratio=0.2,
      overlap_width_ratio=0.2,
  )
  

## Segmentation Masks Don't Match Augmented Images

### **Id**
augmentation-mask-mismatch
### **Severity**
critical
### **Summary**
Geometric augmentations not applied to masks
### **Symptoms**
  - Masks are offset from objects
  - Training loss doesn't decrease
  - Model predicts wrong regions
### **Why**
  Geometric augmentations (rotation, flip, crop) change pixel locations.
  If mask isn't transformed identically, supervision is wrong.
  Model learns to predict wrong regions.
  
### **Gotcha**
  # Augmenting only the image
  augmented_image = A.RandomRotate90()(image=image)['image']
  # mask is NOT rotated!
  
  model.train(image=augmented_image, mask=mask)  # Mask misaligned
  
### **Solution**
  import albumentations as A
  
  # Apply SAME transform to both
  transform = A.Compose([
      A.RandomRotate90(p=0.5),
      A.HorizontalFlip(p=0.5),
      A.RandomResizedCrop(512, 512, scale=(0.5, 1.0)),
  ])
  
  # Transform together
  transformed = transform(image=image, mask=mask)
  augmented_image = transformed['image']
  augmented_mask = transformed['mask']
  

## Duplicate or Missing Detections

### **Id**
nms-threshold-wrong
### **Severity**
high
### **Summary**
NMS threshold not tuned for use case
### **Symptoms**
  - Multiple boxes on same object
  - Overlapping objects miss detections
  - Confidence seems wrong
### **Why**
  NMS (Non-Maximum Suppression) removes duplicate boxes.
  Too high IoU threshold: duplicates remain.
  Too low: overlapping objects get suppressed.
  
### **Gotcha**
  # Default IoU threshold
  results = model(image, iou=0.7)  # Default
  
  # For crowded scenes, correct box suppressed
  # For sparse scenes, duplicates remain
  
### **Solution**
  # Tune for your use case
  results = model(
      image,
      conf=0.25,  # Confidence threshold
      iou=0.45,   # IoU for NMS (lower = more suppression)
  )
  
  # For crowded scenes (pedestrians, products)
  iou=0.5  # Higher threshold, keep overlapping boxes
  
  # For sparse scenes (vehicles, large objects)
  iou=0.3  # Lower threshold, aggressive duplicate removal
  
  # Alternative: Soft-NMS for crowded scenes
  # Reduces score instead of removing
  

## SAM Inference Very Slow

### **Id**
sam-encoding-slow
### **Severity**
medium
### **Summary**
Re-encoding image for every prompt
### **Symptoms**
  - Interactive segmentation is slow
  - Batch segmentation takes forever
  - GPU utilization spiky
### **Why**
  SAM has two stages: image encoding and mask decoding.
  Image encoding is expensive (~150ms on GPU).
  If you re-encode for each prompt, it's 150ms × N prompts.
  
### **Gotcha**
  for box in bounding_boxes:
      # Re-encodes image every iteration!
      masks = predictor.predict(image=image, box=box)
  
### **Solution**
  # Encode once, decode many
  predictor = SamPredictor(sam)
  predictor.set_image(image)  # Encode once (~150ms)
  
  for box in bounding_boxes:
      # Only decode (~10ms each)
      masks, scores, _ = predictor.predict(box=box)
  
  # For batch processing
  from segment_anything import SamPredictor
  
  predictor.set_image(image)
  all_masks = []
  
  for prompt in prompts:
      mask, _, _ = predictor.predict(**prompt)
      all_masks.append(mask)
  

## Tracking IDs Switch Between Objects

### **Id**
video-tracking-id-swap
### **Severity**
medium
### **Summary**
Similar objects swap identities
### **Symptoms**
  - Person A becomes Person B mid-video
  - Objects crossing paths swap IDs
  - Consistent tracking breaks on occlusion
### **Why**
  Tracking algorithms rely on appearance + motion.
  When objects look similar and cross paths,
  the tracker can confuse their identities.
  
### **Gotcha**
  # Basic tracking fails on similar objects
  results = model.track(video_path, tracker="bytetrack.yaml")
  
  # When two similar people cross paths,
  # IDs may swap
  
### **Solution**
  # Use more robust tracker
  results = model.track(
      video_path,
      tracker="botsort.yaml",  # Better re-ID
      persist=True,
  )
  
  # Or use appearance-based re-identification
  # Add ReID model for feature matching
  
  # Tune tracking parameters
  # botsort.yaml:
  # track_high_thresh: 0.5  # Higher for fewer false positives
  # track_low_thresh: 0.1
  # match_thresh: 0.8
  # new_track_thresh: 0.6
  

## Monocular Depth Has Wrong Scale

### **Id**
depth-scale-ambiguity
### **Severity**
medium
### **Summary**
Relative depth, not metric depth
### **Symptoms**
  - Depth values don't match real distances
  - Scale changes between frames
  - Can't use for measurement
### **Why**
  Single-image depth estimation is inherently ambiguous.
  A toy car close up looks like a real car far away.
  Most models output relative depth, not metric.
  
### **Gotcha**
  depth = depth_model(image)
  
  # depth is relative (0-1 range typically)
  # NOT actual meters
  
  distance = depth[y, x]  # This is NOT 5.2 meters!
  
### **Solution**
  # Option 1: Use metric depth models
  from transformers import pipeline
  
  pipe = pipeline("depth-estimation", model="LiheYoung/depth-anything-large-hf")
  # Still relative, but better calibrated
  
  # Option 2: Calibrate with known reference
  known_distance = 10.0  # meters
  known_depth_value = depth[ref_y, ref_x]
  scale = known_distance / known_depth_value
  
  metric_depth = depth * scale
  
  # Option 3: Use stereo or structured light
  # For actual metric depth, need multiple views
  