# Threading Guidelines for P6 Voice Agent

Critical threading patterns for building responsive voice-driven P6 automation with Whisper and tkinter.

## The Golden Rule

> **Whisper `transcribe()` is CPU-intensive and BLOCKING. It MUST run in a daemon thread to prevent UI freezing.**

## Architecture Overview

```
+------------------+     +------------------+     +------------------+
|   Main Thread    |     |  Whisper Thread  |     |   P6 Thread      |
|   (tkinter UI)   |     |   (daemon)       |     |   (automation)   |
+------------------+     +------------------+     +------------------+
        |                        |                        |
        |   start_recording()    |                        |
        |----------------------->|                        |
        |                        |                        |
        |   stop_recording()     |                        |
        |----------------------->|                        |
        |                        | transcribe()           |
        |                        | (blocking)             |
        |                        |                        |
        |   after(callback)      |                        |
        |<-----------------------|                        |
        |                        |                        |
        |   execute_command()    |                        |
        |----------------------------------------------->|
        |                        |                        |
        |   after(result)        |                        |
        |<-----------------------------------------------|
        |                        |                        |
```

## Thread Types

### Main Thread (UI)

- **Owner**: tkinter main loop (`root.mainloop()`)
- **Responsibilities**: 
  - UI rendering and updates
  - User input handling
  - Event callbacks
- **Constraints**: 
  - Must never block
  - All UI updates must happen here

### Worker Threads (Daemon)

- **Type**: `threading.Thread(daemon=True)`
- **Responsibilities**:
  - Whisper model loading
  - Audio transcription
  - Heavy computation
- **Constraints**:
  - Cannot update UI directly
  - Must use callbacks to main thread

### P6 Automation Thread (Optional)

- **Purpose**: Long-running P6 operations
- **When needed**: Multi-step automation sequences
- **Note**: Simple operations can run on main thread

## Critical Patterns

### Pattern 1: Background Whisper Transcription

```python
import threading

class AsyncWhisperTranscriber:
    def __init__(self, on_transcription, on_error):
        self.on_transcription = on_transcription
        self.on_error = on_error
        self.model = None
        self._audio_data = []
        self._is_recording = False
        self._root = None  # Set by UI
    
    def set_root(self, root):
        """Set tkinter root for thread-safe callbacks."""
        self._root = root
    
    def load_model_async(self, on_complete=None):
        """Load Whisper model in background thread."""
        def worker():
            try:
                import whisper
                self.model = whisper.load_model("base")
                if on_complete and self._root:
                    self._root.after(0, on_complete)
            except Exception as e:
                if self.on_error and self._root:
                    self._root.after(0, lambda: self.on_error(str(e)))
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
    
    def stop_and_transcribe_async(self):
        """Stop recording and transcribe in background."""
        audio_data = self._stop_recording()
        
        def worker():
            try:
                # This is the blocking call
                result = self.model.transcribe(audio_data)
                text = result["text"].strip()
                
                # Schedule callback on main thread
                if self._root:
                    self._root.after(0, lambda: self.on_transcription(text))
            except Exception as e:
                if self.on_error and self._root:
                    self._root.after(0, lambda: self.on_error(str(e)))
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
```

### Pattern 2: Thread-Safe UI Updates

```python
# WRONG - Will crash or cause undefined behavior
def on_transcription(text):
    label.config(text=text)  # Called from worker thread!
    button.config(state="normal")

# CORRECT - Schedule on main thread
def on_transcription(text):
    root.after(0, lambda: label.config(text=text))
    root.after(0, lambda: button.config(state="normal"))

# BETTER - Single callback with all updates
def on_transcription(text):
    def update_ui():
        label.config(text=text)
        button.config(state="normal")
        status_label.config(text="Ready")
    root.after(0, update_ui)
```

### Pattern 3: Callback Chain for Multi-Step Operations

```python
class VoiceAgent:
    def __init__(self, root, transcriber, p6_tools):
        self.root = root
        self.transcriber = transcriber
        self.p6_tools = p6_tools
    
    def on_record_release(self):
        """Called when user releases record button."""
        self.update_status("Processing...")
        self.transcriber.stop_and_transcribe_async()
        # Transcription result comes via callback
    
    def on_transcription(self, text):
        """Called (on main thread) when transcription completes."""
        self.update_transcript(text)
        self.update_status("Executing...")
        
        # Run P6 command in background if long-running
        self.execute_command_async(text)
    
    def execute_command_async(self, text):
        """Execute P6 command in background thread."""
        def worker():
            try:
                result = self.p6_tools.execute_from_text(text)
                self.root.after(0, lambda: self.on_command_complete(result))
            except Exception as e:
                self.root.after(0, lambda: self.on_command_error(str(e)))
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
    
    def on_command_complete(self, result):
        """Called (on main thread) when command completes."""
        self.update_status(f"Done: {result.message}")
```

### Pattern 4: Protected Shared State

```python
import threading

class RecordingState:
    def __init__(self):
        self._lock = threading.Lock()
        self._is_recording = False
        self._audio_frames = []
    
    def start_recording(self):
        with self._lock:
            self._is_recording = True
            self._audio_frames = []
    
    def add_frame(self, frame):
        with self._lock:
            if self._is_recording:
                self._audio_frames.append(frame)
    
    def stop_recording(self):
        with self._lock:
            self._is_recording = False
            frames = self._audio_frames[:]
            self._audio_frames = []
            return frames
    
    @property
    def is_recording(self):
        with self._lock:
            return self._is_recording
```

## PyAudio Callback Threading

PyAudio uses separate threads for audio callbacks:

```python
class WhisperTranscriber:
    def __init__(self):
        self._frames = []
        self._lock = threading.Lock()
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Called by PyAudio thread - NOT main thread!"""
        with self._lock:
            self._frames.append(in_data)
        return (None, pyaudio.paContinue)
    
    def start_recording(self):
        self._frames = []
        self._stream = self._audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            stream_callback=self._audio_callback  # Called in PyAudio thread
        )
        self._stream.start_stream()
    
    def get_audio_data(self):
        """Safe to call from any thread."""
        with self._lock:
            return b''.join(self._frames)
```

## Common Mistakes

### Mistake 1: Blocking Main Thread

```python
# WRONG - Freezes UI for 5-30 seconds
def on_button_click():
    result = whisper_model.transcribe(audio_data)  # Blocking!
    label.config(text=result["text"])

# CORRECT - Non-blocking
def on_button_click():
    def worker():
        result = whisper_model.transcribe(audio_data)
        root.after(0, lambda: label.config(text=result["text"]))
    threading.Thread(target=worker, daemon=True).start()
```

### Mistake 2: UI Updates from Worker Thread

```python
# WRONG - Race condition, may crash
def worker_thread():
    for i in range(100):
        progress_bar["value"] = i  # Direct UI access!

# CORRECT - Schedule updates
def worker_thread():
    for i in range(100):
        root.after(0, lambda v=i: update_progress(v))
        time.sleep(0.1)
```

### Mistake 3: Non-Daemon Threads

```python
# WRONG - Thread keeps running after window closes
thread = threading.Thread(target=long_task)
thread.start()

# CORRECT - Daemon thread stops with main program
thread = threading.Thread(target=long_task, daemon=True)
thread.start()
```

### Mistake 4: Missing Error Handling

```python
# WRONG - Errors silently ignored
def worker():
    result = risky_operation()
    root.after(0, lambda: on_success(result))

# CORRECT - Errors propagated to main thread
def worker():
    try:
        result = risky_operation()
        root.after(0, lambda: on_success(result))
    except Exception as e:
        root.after(0, lambda: on_error(str(e)))
```

## tkinter `after()` Method

The `after()` method is the key to thread-safe UI updates:

```python
# Schedule callback after delay (milliseconds)
root.after(1000, my_function)  # Call after 1 second

# Schedule callback immediately on main thread
root.after(0, my_function)  # Call ASAP on main thread

# With arguments
root.after(0, lambda: my_function(arg1, arg2))

# Cancel scheduled callback
callback_id = root.after(1000, my_function)
root.after_cancel(callback_id)
```

## Queue-Based Communication (Alternative)

For complex communication, use queues:

```python
import queue
import threading

class ThreadSafeUI:
    def __init__(self, root):
        self.root = root
        self.queue = queue.Queue()
        self._poll_queue()
    
    def _poll_queue(self):
        """Poll queue for updates (runs on main thread)."""
        try:
            while True:
                callback = self.queue.get_nowait()
                callback()
        except queue.Empty:
            pass
        # Schedule next poll
        self.root.after(100, self._poll_queue)
    
    def schedule_update(self, callback):
        """Thread-safe way to schedule UI update."""
        self.queue.put(callback)
    
    def update_status(self, text):
        """Called from any thread."""
        self.schedule_update(lambda: self.status_label.config(text=text))
```

## Testing Threading

```python
import threading
import time

def test_threading_safety():
    """Verify threading patterns work correctly."""
    root = tk.Tk()
    results = []
    
    def worker():
        time.sleep(0.1)  # Simulate work
        # This should work without error
        root.after(0, lambda: results.append("success"))
    
    # Start multiple workers
    threads = [threading.Thread(target=worker, daemon=True) for _ in range(10)]
    for t in threads:
        t.start()
    
    # Wait and check
    root.after(500, root.quit)
    root.mainloop()
    
    assert len(results) == 10, f"Expected 10, got {len(results)}"
    print("Threading test passed!")
```

## Performance Considerations

1. **Model Loading**: Load Whisper model once at startup
2. **Batch Updates**: Combine multiple UI updates into single `after()` call
3. **Throttle Updates**: Don't update UI too frequently (max 60fps)
4. **Memory**: Large audio buffers should be cleared after transcription
5. **Thread Pool**: For multiple concurrent operations, consider `concurrent.futures.ThreadPoolExecutor`
