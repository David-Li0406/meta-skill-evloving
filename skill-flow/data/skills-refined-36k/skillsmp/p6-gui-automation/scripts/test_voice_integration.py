#!/usr/bin/env python3
"""
Test Voice Integration.

Utility to verify Whisper and microphone setup for voice-driven P6 automation.
Tests: pyaudio, microphone access, Whisper model loading, and transcription.

Usage:
    python test_voice_integration.py
    python test_voice_integration.py --model small  # Use larger model
    python test_voice_integration.py --duration 5   # Record for 5 seconds
"""

import sys
import time
import argparse
import tempfile
import os

def main():
    parser = argparse.ArgumentParser(description="Test Voice Integration")
    parser.add_argument("--model", "-m", default="base", help="Whisper model (tiny, base, small, medium)")
    parser.add_argument("--duration", "-d", type=int, default=3, help="Recording duration in seconds")
    args = parser.parse_args()
    
    print("=" * 60)
    print("P6 Voice Integration Test")
    print("=" * 60)
    print()
    
    results = {
        "pyaudio": False,
        "microphone": False,
        "whisper": False,
        "transcription": False
    }
    
    # Test 1: PyAudio
    print("[1/4] Testing PyAudio installation...")
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        device_count = p.get_device_count()
        print(f"      OK - PyAudio installed, {device_count} audio devices found")
        results["pyaudio"] = True
        
        # List input devices
        print()
        print("      Input devices:")
        for i in range(device_count):
            info = p.get_device_info_by_index(i)
            if info["maxInputChannels"] > 0:
                print(f"        [{i}] {info['name']}")
        
        p.terminate()
        
    except ImportError:
        print("      FAIL - PyAudio not installed")
        print("      Run: pip install pyaudio")
        print("      (On Windows, you may need: pip install pipwin && pipwin install pyaudio)")
        return 1
    except Exception as e:
        print(f"      FAIL - PyAudio error: {e}")
        return 1
    
    # Test 2: Microphone access
    print()
    print("[2/4] Testing microphone access...")
    try:
        import pyaudio
        import wave
        
        p = pyaudio.PyAudio()
        
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        
        print(f"      Recording {args.duration} seconds of audio...")
        print("      (Speak now to test microphone)")
        print()
        
        frames = []
        for i in range(0, int(RATE / CHUNK * args.duration)):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
            
            # Progress indicator
            progress = int((i / (RATE / CHUNK * args.duration)) * 20)
            sys.stdout.write(f"\r      [{('=' * progress).ljust(20)}] {i * CHUNK / RATE:.1f}s")
            sys.stdout.flush()
        
        print()
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        # Check if we got audio
        audio_data = b''.join(frames)
        
        # Simple check for silence
        import struct
        samples = struct.unpack(f'{len(audio_data)//2}h', audio_data)
        max_amplitude = max(abs(s) for s in samples)
        avg_amplitude = sum(abs(s) for s in samples) / len(samples)
        
        print(f"      OK - Audio captured ({len(audio_data)} bytes)")
        print(f"      Max amplitude: {max_amplitude}")
        print(f"      Avg amplitude: {avg_amplitude:.0f}")
        
        if max_amplitude < 100:
            print("      WARNING - Audio appears to be silence. Check microphone.")
        else:
            print("      Audio levels look good!")
            results["microphone"] = True
        
        # Save for transcription test
        temp_wav = tempfile.mktemp(suffix=".wav")
        with wave.open(temp_wav, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT) if hasattr(pyaudio, 'PyAudio') else 2)
            wf.setframerate(RATE)
            wf.writeframes(audio_data)
        
    except Exception as e:
        print(f"      FAIL - Microphone error: {e}")
        temp_wav = None
    
    # Test 3: Whisper installation
    print()
    print("[3/4] Testing Whisper installation...")
    try:
        import whisper
        print(f"      OK - Whisper installed")
        print(f"      Loading '{args.model}' model (this may take a moment)...")
        
        start_time = time.time()
        model = whisper.load_model(args.model)
        load_time = time.time() - start_time
        
        print(f"      OK - Model loaded in {load_time:.1f} seconds")
        results["whisper"] = True
        
    except ImportError:
        print("      FAIL - Whisper not installed")
        print("      Run: pip install openai-whisper")
        model = None
    except Exception as e:
        print(f"      FAIL - Whisper error: {e}")
        model = None
    
    # Test 4: Transcription
    print()
    print("[4/4] Testing transcription...")
    
    if model and temp_wav and os.path.exists(temp_wav):
        try:
            print("      Transcribing recorded audio...")
            
            start_time = time.time()
            result = model.transcribe(temp_wav)
            transcribe_time = time.time() - start_time
            
            text = result["text"].strip()
            
            print(f"      OK - Transcription completed in {transcribe_time:.1f} seconds")
            print()
            print(f"      Transcribed text: \"{text}\"")
            print()
            
            if text:
                print("      Transcription successful!")
                results["transcription"] = True
            else:
                print("      WARNING - Empty transcription (silence or unclear audio)")
            
            # Cleanup
            os.unlink(temp_wav)
            
        except Exception as e:
            print(f"      FAIL - Transcription error: {e}")
    else:
        print("      SKIP - Cannot test transcription (previous steps failed)")
    
    # Summary
    print()
    print("=" * 60)
    print("RESULTS:")
    print("=" * 60)
    
    all_passed = all(results.values())
    
    for test, passed in results.items():
        status = "PASS" if passed else "FAIL"
        icon = "[OK]" if passed else "[X]"
        print(f"  {icon} {test.capitalize()}: {status}")
    
    print()
    
    if all_passed:
        print("All tests passed! Voice integration is ready.")
        print()
        print("You can now run:")
        print('  python "P6 GUI Automation/main.py"')
    else:
        print("Some tests failed. Please fix the issues above.")
        if not results["whisper"]:
            print()
            print("To install Whisper:")
            print("  pip install openai-whisper")
            print()
            print("Also ensure ffmpeg is installed:")
            print("  Windows: winget install ffmpeg")
            print("  macOS: brew install ffmpeg")
            print("  Linux: sudo apt install ffmpeg")
    
    print()
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
