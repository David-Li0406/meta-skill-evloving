---
name: synthetic-wav-sample
description: Generate a tiny non-sensitive WAV file using only the Python standard library. Use for deterministic smoke tests without committing real user audio.
---

# Skill Instructions

## Inputs

- `OUT` (string): output file path (default: `live_test_sample.wav`)

## Procedure

```bash
python3 - <<'PY'
from pathlib import Path
import math
import os
import struct
import wave

out = os.environ.get('OUT', 'live_test_sample.wav')
out_path = Path(out)

# Default behavior: don't overwrite an existing file.
# If you want a new file, set OUT to a different filename.
if out_path.exists():
    print('skipping; already exists:', out)
    raise SystemExit(0)

sample_rate = 16000
seconds = 1.0
frequency = 440.0
amplitude = 0.2

n_samples = int(sample_rate * seconds)
frames = bytearray()
for i in range(n_samples):
    t = i / sample_rate
    value = int(32767 * amplitude * math.sin(2 * math.pi * frequency * t))
    frames += struct.pack('<h', value)

with wave.open(out, 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(sample_rate)
    w.writeframes(frames)

print('wrote', out)
PY
```

## Acceptance Criteria

- File exists and is a valid WAV
- Audio is non-sensitive (tone)
