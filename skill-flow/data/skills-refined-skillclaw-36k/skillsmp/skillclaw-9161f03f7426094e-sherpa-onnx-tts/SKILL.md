---
name: sherpa-onnx-tts
description: Use this skill when you need to perform local text-to-speech using the sherpa-onnx offline CLI without relying on cloud services.
---

# Skill body

## Install

1. Download the runtime for your OS (extracts into `~/.rampage/tools/sherpa-onnx-tts/runtime`):
   - **macOS**: 
     ```bash
     curl -L -o sherpa-onnx-macos.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-osx-universal2-shared.tar.bz2
     tar -xjf sherpa-onnx-macos.tar.bz2 -C ~/.rampage/tools/sherpa-onnx-tts/runtime --strip-components=1
     ```
   - **Linux**: 
     ```bash
     curl -L -o sherpa-onnx-linux.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-linux-x64-shared.tar.bz2
     tar -xjf sherpa-onnx-linux.tar.bz2 -C ~/.rampage/tools/sherpa-onnx-tts/runtime --strip-components=1
     ```
   - **Windows**: 
     ```powershell
     Invoke-WebRequest -Uri https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-win-x64-shared.tar.bz2 -OutFile sherpa-onnx-windows.tar.bz2
     tar -xjf sherpa-onnx-windows.tar.bz2 -C ~/.rampage/tools/sherpa-onnx-tts/runtime --strip-components=1
     ```

2. Download a voice model (extracts into `~/.rampage/tools/sherpa-onnx-tts/models`):
   ```bash
   curl -L -o model-lessac.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-en_US-lessac-high.tar.bz2
   tar -xjf model-lessac.tar.bz2 -C ~/.rampage/tools/sherpa-onnx-tts/models
   ```

3. Update your configuration file (`~/.rampage/rampage.json`):
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

4. Optionally, add the wrapper to your PATH:
   ```bash
   export PATH="{baseDir}/bin:$PATH"
   ```

## Usage

Run the TTS command:
```bash
{baseDir}/bin/sherpa-onnx-tts -o ./tts.wav "Hello from local TTS."
```

### Notes
- You can choose a different model from the sherpa-onnx `tts-models` release if you want another voice.