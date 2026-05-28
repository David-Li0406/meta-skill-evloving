#!/usr/bin/env python3
"""
Shared PeopleNet ONNX Inference Script with DetectNet_v2 Bbox Decoding

This script provides reusable functions for running PeopleNet inference using ONNX Runtime
and correctly decoding DetectNet_v2 bounding box format.

Key Features:
- Direct ONNX inference (bypasses DeepStream metadata issues)
- Correct DetectNet_v2 bbox decoding (grid cell units to pixels)
- Standardized confidence (0.6) and NMS (0.5) thresholds
- Frame-by-frame processing with proper bbox scaling

Usage:
    from peoplenet_onnx_inference import detect_people_in_video
    
    detections = detect_people_in_video(
        video_path="path/to/video.mp4",
        model_path="path/to/model.onnx",
        conf_threshold=0.6,
        nms_threshold=0.5
    )
"""

import cv2
import numpy as np
import onnxruntime as ort
from typing import List, Dict, Tuple, Optional
import json

# Model configuration constants
INPUT_WIDTH = 960
INPUT_HEIGHT = 544
GRID_WIDTH = 60
GRID_HEIGHT = 34
STRIDE_X = INPUT_WIDTH / GRID_WIDTH  # 16 pixels
STRIDE_Y = INPUT_HEIGHT / GRID_HEIGHT  # 16 pixels

# Standard thresholds (matching Part 2 Extract)
DEFAULT_CONF_THRESHOLD = 0.6
DEFAULT_NMS_THRESHOLD = 0.5


def nms(boxes: np.ndarray, scores: np.ndarray, iou_threshold: float = 0.5) -> List[int]:
    """
    Non-maximum suppression to remove duplicate detections.
    
    Args:
        boxes: Array of shape (N, 4) with [left, top, right, bottom] coordinates
        scores: Array of shape (N,) with confidence scores
        iou_threshold: IoU threshold for NMS (default: 0.5)
    
    Returns:
        List of indices to keep after NMS
    """
    if len(boxes) == 0:
        return []

    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    areas = (x2 - x1) * (y2 - y1)
    order = scores.argsort()[::-1]

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)

        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0.0, xx2 - xx1)
        h = np.maximum(0.0, yy2 - yy1)
        inter = w * h

        iou = inter / (areas[i] + areas[order[1:]] - inter)
        inds = np.where(iou <= iou_threshold)[0]
        order = order[inds + 1]

    return keep


def decode_detectnet_v2_bbox(
    center_x_offset: float,
    center_y_offset: float,
    width: float,
    height: float,
    cx_grid: int,
    cy_grid: int
) -> Tuple[float, float, float, float]:
    """
    Decode DetectNet_v2 bbox format from grid cell units to pixel coordinates.
    
    DetectNet_v2 bbox format: (center_x_offset, center_y_offset, width, height)
    - All values are in **grid cell units** (not pixels, not normalized 0-1)
    - Must be decoded relative to grid cell position
    
    Args:
        center_x_offset: Bbox center X offset in grid cell units
        center_y_offset: Bbox center Y offset in grid cell units
        width: Bbox width in grid cell units
        height: Bbox height in grid cell units
        cx_grid: Grid cell X index (0-59)
        cy_grid: Grid cell Y index (0-33)
    
    Returns:
        Tuple of (left, top, right, bottom) in pixel coordinates (model space: 960x544)
    """
    # Grid cell position in pixels
    grid_left = cx_grid * STRIDE_X
    grid_top = cy_grid * STRIDE_Y

    # Decode center coordinates (bbox values are in grid cell units)
    center_x_px = grid_left + center_x_offset * STRIDE_X
    center_y_px = grid_top + center_y_offset * STRIDE_Y

    # Decode size (width/height are also in grid cell units)
    width_px = width * STRIDE_X
    height_px = height * STRIDE_Y

    # Convert to corner coordinates
    left = center_x_px - width_px / 2
    top = center_y_px - height_px / 2
    right = center_x_px + width_px / 2
    bottom = center_y_px + height_px / 2

    # Clip to image bounds
    left = np.clip(left, 0, INPUT_WIDTH)
    top = np.clip(top, 0, INPUT_HEIGHT)
    right = np.clip(right, 0, INPUT_WIDTH)
    bottom = np.clip(bottom, 0, INPUT_HEIGHT)

    return left, top, right, bottom


def detect_people_in_frame(
    session: ort.InferenceSession,
    frame: np.ndarray,
    conf_threshold: float = DEFAULT_CONF_THRESHOLD,
    nms_threshold: float = DEFAULT_NMS_THRESHOLD
) -> List[Dict]:
    """
    Detect people in a single frame using PeopleNet ONNX model.
    
    Args:
        session: ONNX Runtime inference session
        frame: Input frame (BGR format, any size)
        conf_threshold: Confidence threshold (default: 0.6)
        nms_threshold: NMS IoU threshold (default: 0.5)
    
    Returns:
        List of detection dictionaries with keys:
        - 'bbox': [left, top, right, bottom] in model space (960x544)
        - 'confidence': float confidence score
        - 'class': 'person' (always person class for this function)
    """
    # Preprocess frame
    img_resized = cv2.resize(frame, (INPUT_WIDTH, INPUT_HEIGHT))
    img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
    img_normalized = img_rgb.astype(np.float32) / 255.0
    img_chw = np.transpose(img_normalized, (2, 0, 1))
    img_batch = np.expand_dims(img_chw, axis=0)

    # Run inference
    outputs = session.run(None, {'input_1:0': img_batch})
    cov_output = outputs[0]  # Coverage/confidence output
    bbox_output = outputs[1]  # Bounding box output

    # Decode detections
    class_id = 0  # Person class
    cov_class = cov_output[0, class_id, :, :]
    indices = np.where(cov_class >= conf_threshold)

    if len(indices[0]) == 0:
        return []

    detections = []
    for i in range(len(indices[0])):
        cy_grid = indices[0][i]
        cx_grid = indices[1][i]
        conf = float(cov_class[cy_grid, cx_grid])

        # Extract bbox values from model output
        bbox_idx = class_id * 4
        center_x_offset = bbox_output[0, bbox_idx + 0, cy_grid, cx_grid]
        center_y_offset = bbox_output[0, bbox_idx + 1, cy_grid, cx_grid]
        width = bbox_output[0, bbox_idx + 2, cy_grid, cx_grid]
        height = bbox_output[0, bbox_idx + 3, cy_grid, cx_grid]

        # Decode bbox to pixel coordinates
        left, top, right, bottom = decode_detectnet_v2_bbox(
            center_x_offset, center_y_offset, width, height,
            cx_grid, cy_grid
        )

        if right > left and bottom > top:
            detections.append({
                'bbox': [float(left), float(top), float(right), float(bottom)],
                'confidence': conf,
                'class': 'person'
            })

    # Apply NMS
    if len(detections) > 0:
        boxes = np.array([d['bbox'] for d in detections])
        scores = np.array([d['confidence'] for d in detections])
        keep_indices = nms(boxes, scores, nms_threshold)
        detections = [detections[i] for i in keep_indices]

    return detections


def detect_people_in_video(
    video_path: str,
    model_path: str,
    conf_threshold: float = DEFAULT_CONF_THRESHOLD,
    nms_threshold: float = DEFAULT_NMS_THRESHOLD,
    frame_interval: int = 1,
    max_frames: Optional[int] = None
) -> List[Dict]:
    """
    Detect people in a video file, processing frames at specified interval.
    
    Args:
        video_path: Path to input video file
        model_path: Path to PeopleNet ONNX model file
        conf_threshold: Confidence threshold (default: 0.6)
        nms_threshold: NMS IoU threshold (default: 0.5)
        frame_interval: Process every Nth frame (default: 1, process all frames)
        max_frames: Maximum number of frames to process (None = all)
    
    Returns:
        List of detection dictionaries, one per frame, with format:
        {
            'frame_idx': int,
            'pts_ms': int,  # Presentation timestamp in milliseconds
            'detections': [
                {
                    'bbox': [left, top, right, bottom],  # Model space (960x544)
                    'confidence': float,
                    'class': 'person'
                }
            ]
        }
    """
    # Load model
    session = ort.InferenceSession(model_path)

    # Open video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    all_detections = []
    frame_num = 0
    processed_frames = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Process frame if it matches interval
        if frame_num % frame_interval == 0:
            detections = detect_people_in_frame(
                session, frame, conf_threshold, nms_threshold
            )

            # Calculate presentation timestamp
            pts_ms = int((frame_num / fps) * 1000) if fps > 0 else 0

            all_detections.append({
                'frame_idx': frame_num,
                'pts_ms': pts_ms,
                'detections': detections
            })

            processed_frames += 1
            if max_frames and processed_frames >= max_frames:
                break

        frame_num += 1

    cap.release()
    return all_detections


def scale_bbox_to_original(
    bbox: List[float],
    model_width: int,
    model_height: int,
    original_width: int,
    original_height: int
) -> List[int]:
    """
    Scale bbox coordinates from model space (960x544) to original video resolution.
    
    Args:
        bbox: [left, top, right, bottom] in model space
        model_width: Model input width (960)
        model_height: Model input height (544)
        original_width: Original video width
        original_height: Original video height
    
    Returns:
        [left, top, right, bottom] scaled to original resolution (integers)
    """
    left, top, right, bottom = bbox
    scale_x = original_width / model_width
    scale_y = original_height / model_height

    return [
        int(left * scale_x),
        int(top * scale_y),
        int(right * scale_x),
        int(bottom * scale_y)
    ]


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python3 peoplenet_onnx_inference.py <video_path> <model_path> [output_json]")
        sys.exit(1)

    video_path = sys.argv[1]
    model_path = sys.argv[2]
    output_json = sys.argv[3] if len(sys.argv) > 3 else None

    print(f"Processing video: {video_path}")
    detections = detect_people_in_video(video_path, model_path)

    # Format for Part 3 detection JSON format
    result = {
        "video_path": video_path,
        "detections": []
    }

    for frame_data in detections:
        for det in frame_data['detections']:
            result["detections"].append({
                "frame_idx": frame_data['frame_idx'],
                "pts_ms": frame_data['pts_ms'],
                "object_id": -1,  # No tracking
                "class": det['class'],
                "confidence": det['confidence'],
                "bbox": det['bbox']  # In model space (960x544)
            })

    if output_json:
        with open(output_json, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Saved detections to: {output_json}")
    else:
        print(json.dumps(result, indent=2))

    print(f"\nTotal frames processed: {len(detections)}")
    print(f"Total detections: {len(result['detections'])}")

