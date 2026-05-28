#!/usr/bin/env python3
import os
import sys
import cv2
import json
import math
import numpy as np
from typing import List, Tuple

import onnxruntime as ort

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
sys.path.append(os.path.join(PROJECT_ROOT, "Scripts"))
from peoplenet_onnx_inference import detect_people_in_frame, INPUT_WIDTH, INPUT_HEIGHT


def ensure_dir(path: str) -> None:
	if not os.path.isdir(path):
		os.makedirs(path, exist_ok=True)


def compute_brightness(frame_bgr: np.ndarray) -> float:
	gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
	return float(gray.mean())


def draw_detections(frame_bgr: np.ndarray, detections: List[dict]) -> np.ndarray:
	vis = frame_bgr.copy()
	for det in detections:
		left, top, right, bottom = det["bbox"]
		# Scale from model space (960x544) to frame size
		h, w = vis.shape[:2]
		scale_x = w / float(INPUT_WIDTH)
		scale_y = h / float(INPUT_HEIGHT)
		x1 = int(left * scale_x)
		y1 = int(top * scale_y)
		x2 = int(right * scale_x)
		y2 = int(bottom * scale_y)
		cv2.rectangle(vis, (x1, y1), (x2, y2), (0, 255, 0), 2)
		label = f"{det['class']} {det['confidence']:.2f}"
		cv2.putText(vis, label, (x1, max(0, y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
	return vis


def extract_frame_at_ts(cap: cv2.VideoCapture, second_mark: float) -> Tuple[bool, np.ndarray, int]:
	fps = cap.get(cv2.CAP_PROP_FPS) or 0
	if fps <= 0:
		return False, None, 0
	frame_idx = int(second_mark * fps)
	total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
	if frame_idx >= total:
		frame_idx = max(0, total - 1)
	cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
	ret, frame = cap.read()
	return ret, frame, frame_idx


def main():
	if len(sys.argv) < 4:
		print("Usage: python3 lowlight_analyze_samples.py <sample_list.txt> <model.onnx> <out_dir>")
		sys.exit(1)
	sample_list = sys.argv[1]
	model_path = sys.argv[2]
	out_dir = sys.argv[3]
	ensure_dir(out_dir)

	# Initialize ONNX session (CPU for small sample is OK; adjust providers if needed)
	session = ort.InferenceSession(model_path)

	with open(sample_list, "r") as f:
		videos = [line.strip() for line in f if line.strip()]

	results_index = []
	for idx, video_path in enumerate(videos, 1):
		base = os.path.basename(video_path)
		stem = os.path.splitext(base)[0]
		video_out = os.path.join(out_dir, stem)
		ensure_dir(video_out)

		cap = cv2.VideoCapture(video_path)
		if not cap.isOpened():
			print(f"WARN: could not open {video_path}")
			continue

		for ts in (5.0, 30.0):
			ret, frame, frame_idx = extract_frame_at_ts(cap, ts)
			if not ret:
				continue
			brightness = compute_brightness(frame)
			detections = detect_people_in_frame(session, frame, conf_threshold=0.6, nms_threshold=0.5)
			annot = draw_detections(frame, detections)

			frame_name = f"t{int(ts):02d}s_f{frame_idx}.jpg"
			annot_name = f"t{int(ts):02d}s_f{frame_idx}_annot.jpg"
			cv2.imwrite(os.path.join(video_out, frame_name), frame)
			cv2.imwrite(os.path.join(video_out, annot_name), annot)

			# Save a few person crops for manual review
			h, w = frame.shape[:2]
			for ci, det in enumerate(detections[:3]):
				l, t, r, b = det["bbox"]
				scale_x = w / float(INPUT_WIDTH)
				scale_y = h / float(INPUT_HEIGHT)
				x1 = max(0, int(l * scale_x))
				y1 = max(0, int(t * scale_y))
				x2 = min(w - 1, int(r * scale_x))
				y2 = min(h - 1, int(b * scale_y))
				if x2 > x1 and y2 > y1:
					crop = frame[y1:y2, x1:x2]
					cv2.imwrite(os.path.join(video_out, f"t{int(ts):02d}s_f{frame_idx}_crop{ci+1}.jpg"), crop)

			results_index.append({
				"video": video_path,
				"timestamp_s": ts,
				"frame_idx": frame_idx,
				"brightness_mean": brightness,
				"detections": len(detections),
				"out_dir": video_out
			})

		cap.release()

	with open(os.path.join(out_dir, "summary.json"), "w") as f:
		json.dump(results_index, f, indent=2)
	print(f"Wrote summary: {os.path.join(out_dir, 'summary.json')}")


if __name__ == "__main__":
	main()


