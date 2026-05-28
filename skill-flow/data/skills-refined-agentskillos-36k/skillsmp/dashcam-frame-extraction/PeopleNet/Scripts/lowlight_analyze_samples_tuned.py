#!/usr/bin/env python3
import os
import sys
import cv2
import json
import numpy as np
from typing import List
import onnxruntime as ort

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
sys.path.append(os.path.join(PROJECT_ROOT, "Scripts"))
from peoplenet_onnx_inference import detect_people_in_frame, INPUT_WIDTH, INPUT_HEIGHT

def ensure_dir(p: str): 
	if not os.path.isdir(p): os.makedirs(p, exist_ok=True)

def brightness(frame: np.ndarray) -> float:
	return float(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).mean())

def apply_gamma(frame: np.ndarray, gamma: float) -> np.ndarray:
	if gamma <= 0: 
		return frame
	inv = 1.0 / gamma
	table = np.array([(i / 255.0) ** inv * 255 for i in range(256)]).astype("uint8")
	return cv2.LUT(frame, table)

def draw_dets(img: np.ndarray, dets: List[dict]) -> np.ndarray:
	out = img.copy()
	h, w = out.shape[:2]
	sx, sy = w / float(INPUT_WIDTH), h / float(INPUT_HEIGHT)
	for d in dets:
		l, t, r, b = d["bbox"]
		x1, y1, x2, y2 = int(l*sx), int(t*sy), int(r*sx), int(b*sy)
		cv2.rectangle(out, (x1,y1), (x2,y2), (0,255,0), 2)
		cv2.putText(out, f"{d['class']} {d['confidence']:.2f}", (x1, max(0, y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
	return out

def main():
	if len(sys.argv) < 5:
		print("Usage: python3 lowlight_analyze_samples_tuned.py <sample_list.txt> <model.onnx> <out_dir> <conf> [gamma_if_dark] [dark_thresh]")
		sys.exit(1)
	sample_list, model_path, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]
	conf = float(sys.argv[4])
	gamma_if_dark = float(sys.argv[5]) if len(sys.argv) > 5 else 1.8
	dark_thresh = float(sys.argv[6]) if len(sys.argv) > 6 else 30.0
	ensure_dir(out_dir)

	session = ort.InferenceSession(model_path)
	with open(sample_list, "r") as f:
		videos = [ln.strip() for ln in f if ln.strip()]

	report = []
	for vp in videos:
		base = os.path.basename(vp)
		stem = os.path.splitext(base)[0]
		vo = os.path.join(out_dir, stem)
		ensure_dir(vo)
		cap = cv2.VideoCapture(vp)
		if not cap.isOpened():
			print(f"WARN open fail: {vp}"); continue
		for ts in (5.0, 30.0):
			fps = cap.get(cv2.CAP_PROP_FPS) or 0
			frame_idx = int(ts * fps) if fps>0 else 0
			cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
			ret, frame = cap.read()
			if not ret: 
				continue
			br = brightness(frame)
			img_for_infer = frame
			applied_gamma = 1.0
			if br < dark_thresh:
				img_for_infer = apply_gamma(frame, gamma_if_dark)
				applied_gamma = gamma_if_dark
			dets = detect_people_in_frame(session, img_for_infer, conf_threshold=conf, nms_threshold=0.5)
			annot = draw_dets(img_for_infer, dets)
			cv2.imwrite(os.path.join(vo, f"t{int(ts):02d}s_f{frame_idx}_tuned.jpg"), annot)
			report.append({"video": vp, "ts": ts, "frame_idx": frame_idx, "brightness": br, "gamma": applied_gamma, "detections": len(dets)})
		cap.release()
	with open(os.path.join(out_dir, "summary_tuned.json"), "w") as f:
		json.dump(report, f, indent=2)
	print("Wrote:", os.path.join(out_dir, "summary_tuned.json"))

if __name__ == "__main__": 
	main()


