#!/usr/bin/env python3
"""
GPU batch processor for PeopleNet using ONNX Runtime (CUDAExecutionProvider)
Processes a list of videos, detects presence of people at 1 FPS, and extracts
clips around detections via ffmpeg stream copy.
"""
import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import List, Tuple

import cv2
import numpy as np
import onnxruntime as ort


def list_execution_providers() -> List[str]:
	"""Return available execution providers (for logging)."""
	try:
		return ort.get_available_providers()
	except Exception:
		return []


class PeopleNetPresenceDetector:
	def __init__(
		self,
		model_path: str,
		confidence_threshold: float = 0.6,
	):
		self.model_path = model_path
		self.confidence_threshold = confidence_threshold

		available = list_execution_providers()
		preferred: List[str] = []
		# Prefer TensorRT if available in the container, then CUDA
		if "TensorrtExecutionProvider" in available:
			preferred.append("TensorrtExecutionProvider")
		if "CUDAExecutionProvider" in available:
			preferred.append("CUDAExecutionProvider")
		# Always add CPU as fallback inside the container (but we will log loudly)
		preferred.append("CPUExecutionProvider")

		try:
			self.session = ort.InferenceSession(self.model_path, providers=preferred)
		except Exception as provider_error:
			# Retry without TensorRT if that was the cause (missing TRT libs)
			if "TensorrtExecutionProvider" in preferred:
				safe_pref = [p for p in preferred if p != "TensorrtExecutionProvider"]
				self.session = ort.InferenceSession(self.model_path, providers=safe_pref)
			else:
				raise provider_error

		self.providers_in_use = self.session.get_providers()

	def detect_presence_in_frame(self, frame_bgr: np.ndarray) -> Tuple[bool, float]:
		"""Return (has_person, max_confidence) using PeopleNet coverage."""
		# Model expects 960x544 RGB normalized to [0,1], CHW
		img = cv2.resize(frame_bgr, (960, 544))
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
		img = np.transpose(img, (2, 0, 1))[np.newaxis, ...]

		# Infer (assumes input name 'input_1:0'; TRT/ORT ONNX in this model typically uses this)
		outputs = self.session.run(None, {"input_1:0": img})
		coverage = outputs[0]  # [1, 3, 34, 60]
		person_cov = coverage[0, 0, :, :]
		max_conf = float(np.max(person_cov))
		return max_conf >= self.confidence_threshold, max_conf


def merge_segments(timestamps: List[float], buffer_seconds: float) -> List[dict]:
	"""Merge +/- buffer_seconds windows around timestamps into non-overlapping segments."""
	if not timestamps:
		return []
	segments: List[dict] = []
	for ts in sorted(timestamps):
		start = max(0.0, ts - buffer_seconds)
		end = ts + buffer_seconds
		if segments and start <= segments[-1]["end"]:
			segments[-1]["end"] = max(segments[-1]["end"], end)
		else:
			segments.append({"start": start, "end": end})
	return segments


def extract_clips_ffmpeg(input_video: str, segments: List[dict], output_dir: str) -> int:
	"""Extract segments using ffmpeg stream-copy. Returns number of clips written."""
	os.makedirs(output_dir, exist_ok=True)
	base = os.path.splitext(os.path.basename(input_video))[0]
	written = 0
	for seg in segments:
		start_s = int(seg["start"])
		end_s = int(seg["end"])
		duration = max(0.1, seg["end"] - seg["start"])
		out_file = os.path.join(output_dir, f"{base}_people_{start_s}-{end_s}s.mp4")

		# Skip if already exists to avoid duplication
		if os.path.exists(out_file):
			written += 1
			continue

		cmd = [
			"ffmpeg",
			"-hide_banner",
			"-loglevel",
			"error",
			"-y",
			"-ss",
			str(seg["start"]),
			"-i",
			input_video,
			"-t",
			str(duration),
			"-c",
			"copy",
			out_file,
		]
		subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		if os.path.exists(out_file):
			written += 1
	return written


def process_video(
	video_path: str,
	output_dir: str,
	detector: PeopleNetPresenceDetector,
	sample_rate_fps: int,
) -> Tuple[int, int]:
	"""Return (num_detections, num_clips)."""
	cap = cv2.VideoCapture(video_path)
	if not cap.isOpened():
		return 0, 0
	fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
	frame_idx = 0
	timestamps: List[float] = []

	while True:
		ret, frame = cap.read()
		if not ret:
			break
		frame_idx += 1

		# Sample approximately 1 frame per second
		if int(fps) > 0 and (frame_idx % int(fps // sample_rate_fps if sample_rate_fps > 0 else fps) != 0):
			continue

		has_person, conf = detector.detect_presence_in_frame(frame)
		if has_person:
			ts = frame_idx / fps
			timestamps.append(ts)
	cap.release()

	segments = merge_segments(timestamps, buffer_seconds=4.0)
	clips = extract_clips_ffmpeg(video_path, segments, output_dir)
	return len(timestamps), clips


def process_list(
	video_list_file: str,
	output_dir: str,
	model_path: str,
	conf_threshold: float,
	sample_rate_fps: int,
	log_file: str,
):
	os.makedirs(output_dir, exist_ok=True)
	with open(video_list_file, "r") as f:
		videos = [line.strip() for line in f if line.strip()]

	with open(log_file, "w") as log:
		log.write(f"Using model: {model_path}\n")
		log.write(f"Confidence threshold: {conf_threshold}\n")
		log.write(f"Sample rate: {sample_rate_fps} FPS\n")

		detector = PeopleNetPresenceDetector(model_path=model_path, confidence_threshold=conf_threshold)
		log.write(f"Using execution providers: {detector.providers_in_use}\n\n")

		total = len(videos)
		processed = 0
		with_people = 0
		total_clips = 0

		for v in videos:
			processed += 1
			name = os.path.basename(v)
			log.write(f"[{processed}/{total}] Processing: {name}\n")
			log.flush()
			try:
				dets, clips = process_video(v, output_dir, detector, sample_rate_fps=sample_rate_fps)
				if dets > 0:
					with_people += 1
					total_clips += clips
					log.write(f"  Found {dets} detections, extracted {clips} clip(s)\n\n")
				else:
					log.write("  No people detected\n\n")
			except Exception as e:
				log.write(f"  ERROR: {e}\n\n")
				log.flush()
				continue

		log.write("=== Summary ===\n")
		log.write(f"Videos processed: {processed}\n")
		log.write(f"Videos with people: {with_people}\n")
		log.write(f"Total clips extracted: {total_clips}\n")


def main():
	parser = argparse.ArgumentParser(description="GPU batch processing for PeopleNet presence detection and clip extraction.")
	parser.add_argument("--video-list", type=str, required=True, help="Path to text file with one video path per line.")
	parser.add_argument("--output-dir", type=str, required=True, help="Directory to write extracted clips.")
	parser.add_argument("--model", type=str, required=True, help="Path to PeopleNet ONNX model.")
	parser.add_argument("--conf", type=float, default=0.6, help="Confidence threshold.")
	parser.add_argument("--sample-rate-fps", type=int, default=1, help="Sampling FPS (frames per second).")
	parser.add_argument("--log-file", type=str, default="", help="Processing log file path.")
	args = parser.parse_args()

	log_file = args.log_file or os.path.join(args.output_dir, "processing_log.txt")
	process_list(
		video_list_file=args.video_list,
		output_dir=args.output_dir,
		model_path=args.model,
		conf_threshold=args.conf,
		sample_rate_fps=args.sample_rate_fps,
		log_file=log_file,
	)


if __name__ == "__main__":
	main()


