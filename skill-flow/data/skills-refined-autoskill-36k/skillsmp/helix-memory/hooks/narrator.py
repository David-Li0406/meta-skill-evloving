#!/usr/bin/env python3
"""Narrate memories as they're stored - David Attenborough style."""
import subprocess
from pathlib import Path
from typing import List, Dict

ATTENBOROUGH_PROMPT = """Narrate this memory in 1 short sentence. Be direct - state the key fact. No metaphors or fluff.

Memory: {memory}

Narration:"""


class Speaker:
	"""macOS TTS."""
	def __init__(self, voice: str = "Daniel", rate: int = 185):
		self.voice = voice
		self.rate = rate

	def speak(self, text: str) -> None:
		"""Blocking speak - we want to hear it before next exchange."""
		subprocess.run(
			["say", "-v", self.voice, "-r", str(self.rate), text],
			timeout=30
		)


def should_narrate(project: str = "") -> bool:
	"""Check if narration enabled for this project."""
	if not project:
		return False
	project_flag = Path.home() / f".narrator-{project.lower()}"
	return project_flag.exists()


def maybe_narrate(memories: List[Dict], project: str = "") -> None:
	"""
	Narrate stored memories if enabled.
	Reads memory content directly - no LLM processing.
	"""
	if not should_narrate(project):
		return

	if not memories:
		return

	speaker = Speaker()
	for mem in memories:
		content = mem.get("content", "")
		if not content:
			continue

		# Read content directly - faster, no fluff
		speaker.speak(content)


# CLI for testing
if __name__ == "__main__":
	import sys
	if len(sys.argv) > 1:
		test_memory = {"content": sys.argv[1]}
		project = sys.argv[2] if len(sys.argv) > 2 else "test"
		# Force enable for test
		test_flag = Path.home() / f".narrator-{project}"
		test_flag.touch()
		maybe_narrate([test_memory], project)
		test_flag.unlink()
	else:
		print("Usage: python narrator.py 'memory content' [project]")
