---
name: sherpa-onnx-tts
description: Use this skill for local text-to-speech via sherpa-onnx (offline, no cloud).
---

# sherpa-onnx-tts

Local TTS using the sherpa-onnx offline CLI.

## Install

1) Download the runtime for your OS (extracts into `~/.rampage/tools/sherpa-onnx-tts/runtime` or `~/.clawdbot/tools/sherpa-onnx-tts/runtime`).
2) Download a voice model (extracts into `~/.rampage/tools/sherpa-onnx-tts/models` or `~/.clawdbot/tools/sherpa-onnx-tts/models`).

Update your configuration file (e.g., `~/.rampage/rampage.json` or `~/.clawdbot/clawdbot.json`):

```json5
{
  skills: {
    entries: {
      "sherpa-onnx-tts": {
        env: {
          SHERPA_ONNX_RUNTIME_DIR: "~/.rampage/tools/sherpa-onnx-tts/runtime",
          SHERPA_ONNX_MODEL_DIR: "~/.rampage/tools/sherpa-onnx-tts/models/vits-piper-en_US-lessac-high"
        }
      }
    }
  }
}
```

The wrapper lives in this skill folder. Run it directly, or add the wrapper to PATH:

```bash
export PATH="{baseDir}/bin:$PATH"
```

## Usage

```bash
{baseDir}/bin/sherpa-onnx-tts -o ./tts.wav "Hello from local TTS."
```

Notes:
- Pick a different model from the sherpa-onnx `tts-models` release if you want another voice.
- If the model directory has multiple `.onnx` files, set `SHERPA_ONNX_MODEL_FILE` or pass `--model-file`.
- You can also pass `--tokens-file` or `--data-dir` to override the defaults.
- Windows: run `node {baseDir}\\bin\\sherpa-onnx-tts -o tts.wav "Hello from local TTS."`