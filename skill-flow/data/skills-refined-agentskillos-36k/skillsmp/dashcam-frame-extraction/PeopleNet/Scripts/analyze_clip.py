#!/usr/bin/env python3
import cv2
import numpy as np
import onnxruntime as ort
import sys

# Paths
video_path = sys.argv[1] if len(sys.argv) > 1 else '/workspace/Outputs/Park_F_Batch1/20251029051127_076702A_people_21-29s.mp4'
model_path = '/workspace/model/resnet34_peoplenet_int8.onnx'

# Load model
session = ort.InferenceSession(model_path, providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])

# Open video
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print('ERROR: Cannot open video')
    sys.exit(1)

fps = cap.get(cv2.CAP_PROP_FPS) or 30
frame_num = 0
detections = []

print(f"Analyzing: {video_path.split('/')[-1]}")
print(f"FPS: {fps:.2f}")
print(f"Confidence threshold: 0.8")
print("\n" + "="*80)
print(f"{'Frame':<8} {'Time (s)':<10} {'Confidence':<12} {'Status'}")
print("="*80)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_num += 1

    timestamp = frame_num / fps

    # Preprocess
    img = cv2.resize(frame, (960, 544))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    img = np.transpose(img, (2, 0, 1))[np.newaxis, ...]

    # Run inference
    outputs = session.run(None, {'input_1:0': img})
    max_conf = outputs[0][0, 0, :, :].max()

    # Print every 15 frames (~0.5s intervals)
    if frame_num % 15 == 0 or max_conf >= 0.8:
        status = "✓ PERSON DETECTED" if max_conf >= 0.8 else ""
        print(f"{frame_num:<8} {timestamp:<10.2f} {max_conf:<12.3f} {status}")

        if max_conf >= 0.8:
            detections.append((timestamp, max_conf))

cap.release()

print("="*80)
print(f"\nSummary:")
print(f"Total frames analyzed: {frame_num}")
print(f"Video duration: {frame_num/fps:.2f} seconds")
print(f"Detections (conf >= 0.8): {len(detections)}")

if detections:
    print(f"\nDetection timestamps:")
    for ts, conf in detections:
        print(f"  {ts:.2f}s - Confidence: {conf:.3f}")
    print(f"\nConfidence range: {min(d[1] for d in detections):.3f} to {max(d[1] for d in detections):.3f}")
else:
    print("\nNo detections above 0.8 threshold found in this clip.")
