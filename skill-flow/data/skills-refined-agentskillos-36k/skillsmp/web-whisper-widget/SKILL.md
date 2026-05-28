---
name: web-whisper-widget
description: Add speech-to-text transcription widget to web pages using Whisper server. Creates WhisperWidget JS component that records audio, sends to whisper server, and returns transcribed text. Use when adding voice input to web applications.
---

# Web Whisper Widget Skill

Add browser-based speech-to-text transcription to any web page using a whisper.cpp server backend.

## Quick Integration

To add the widget to a page:

1. Create the JS and CSS files (code below)
2. Include them in the HTML
3. Initialize on a target element

```html
<link rel="stylesheet" href="whisper-widget.css">
<script src="whisper-widget.js"></script>

<div id="voice-input"></div>

<script>
const widget = new WhisperWidget('#voice-input', {
    serverUrl: '/whisper/inference',
    onTranscription: (text) => {
        // Do something with transcribed text
        document.getElementById('target').value += text + ' ';
    }
});
</script>
```

## API Reference

### Constructor

```javascript
new WhisperWidget(container, options)
```

- `container` - CSS selector string or DOM element
- `options` - Configuration object

### Options

```javascript
{
    serverUrl: '/whisper/inference',  // Whisper server endpoint
    showVisualizer: true,              // Show audio waveform
    showTimer: true,                   // Show recording duration
    showHistory: true,                 // Show transcription history
    historyLimit: 20,                  // Max history items
    onTranscription: (text) => {},     // Called with transcribed text
    onError: (message) => {},          // Called on error
    onRecordingStart: () => {},        // Called when recording starts
    onRecordingStop: () => {}          // Called when recording stops
}
```

### Methods

```javascript
widget.start()             // Start recording
widget.stop()              // Stop recording
widget.toggle()            // Toggle recording
widget.copy()              // Copy transcription to clipboard
widget.getTranscription()  // Get current transcription text
widget.getHistory()        // Get history array
widget.clearHistory()      // Clear history
widget.setServerUrl(url)   // Change server URL
widget.destroy()           // Clean up widget
```

### Events

Listen on the container element:

```javascript
container.addEventListener('whisper:transcription', (e) => {
    console.log(e.detail.text);
});
```

Events: `whisper:ready`, `whisper:recording`, `whisper:stopped`, `whisper:processing`, `whisper:transcription`, `whisper:error`

### CSS Variants

Add these classes to the container for different layouts:

- `ww-compact` - Smaller controls
- `ww-inline` - Horizontal layout
- `ww-minimal` - Just the record button
- `ww-light` - Light theme

### CSS Custom Properties

```css
.whisper-widget {
    --ww-bg-primary: #1a1a2e;
    --ww-bg-secondary: #16213e;
    --ww-text-primary: #eaeaea;
    --ww-text-secondary: #a0a0a0;
    --ww-accent: #e94560;
    --ww-success: #4ade80;
    --ww-recording: #ef4444;
    --ww-border-radius: 0.5rem;
}
```

## Full Source Code

### whisper-widget.js

```javascript
/**
 * WhisperWidget - Browser audio transcription component
 */
class WhisperWidget {
    static defaultOptions = {
        serverUrl: '/whisper/inference',
        showVisualizer: true,
        showTimer: true,
        showHistory: true,
        historyLimit: 20,
        onTranscription: null,
        onError: null,
        onRecordingStart: null,
        onRecordingStop: null
    };

    constructor(container, options = {}) {
        this.container = typeof container === 'string'
            ? document.querySelector(container)
            : container;
        if (!this.container) throw new Error('WhisperWidget: Container not found');
        this.options = { ...WhisperWidget.defaultOptions, ...options };
        this.state = {
            isRecording: false,
            isProcessing: false,
            mediaRecorder: null,
            audioChunks: [],
            audioContext: null,
            analyser: null,
            animationId: null,
            timerInterval: null,
            startTime: null,
            history: []
        };
        this.elements = {};
        this._init();
    }

    _init() {
        this._render();
        this._bindEvents();
        this._initCanvas();
        this._emit('ready');
    }

    _render() {
        this.container.classList.add('whisper-widget');
        this.container.innerHTML = `
            <div class="ww-visualizer-section">
                ${this.options.showVisualizer ? '<canvas class="ww-visualizer"></canvas>' : ''}
                <div class="ww-controls">
                    ${this.options.showTimer ? '<span class="ww-timer">0:00</span>' : ''}
                    <button class="ww-record-btn" title="Click to record (Space)">
                        <span class="ww-record-icon"></span>
                    </button>
                    <div class="ww-status">
                        <span class="ww-status-dot"></span>
                        <span class="ww-status-text">Ready</span>
                    </div>
                </div>
            </div>
            <div class="ww-output-section">
                <div class="ww-output-header">
                    <span class="ww-output-label">Transcription</span>
                    <button class="ww-copy-btn">Copy</button>
                </div>
                <div class="ww-output" data-empty="true">Click record to start...</div>
            </div>
            ${this.options.showHistory ? `
                <div class="ww-history-section" style="display: none;">
                    <div class="ww-history-header">
                        <span class="ww-history-label">History</span>
                        <button class="ww-clear-btn">Clear</button>
                    </div>
                    <div class="ww-history-list"></div>
                </div>
            ` : ''}
        `;
        this.elements = {
            canvas: this.container.querySelector('.ww-visualizer'),
            timer: this.container.querySelector('.ww-timer'),
            recordBtn: this.container.querySelector('.ww-record-btn'),
            statusDot: this.container.querySelector('.ww-status-dot'),
            statusText: this.container.querySelector('.ww-status-text'),
            output: this.container.querySelector('.ww-output'),
            copyBtn: this.container.querySelector('.ww-copy-btn'),
            historySection: this.container.querySelector('.ww-history-section'),
            historyList: this.container.querySelector('.ww-history-list'),
            clearBtn: this.container.querySelector('.ww-clear-btn')
        };
        if (this.elements.canvas) {
            this.canvasCtx = this.elements.canvas.getContext('2d');
        }
    }

    _bindEvents() {
        this.elements.recordBtn.addEventListener('click', () => this.toggle());
        this.elements.copyBtn.addEventListener('click', () => this.copy());
        if (this.elements.clearBtn) {
            this.elements.clearBtn.addEventListener('click', () => this.clearHistory());
        }
        this.container.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
                e.preventDefault();
                this.toggle();
            }
            if (e.code === 'Escape' && this.state.isRecording) {
                this.stop();
            }
        });
        if (!this.container.hasAttribute('tabindex')) {
            this.container.setAttribute('tabindex', '0');
        }
    }

    _initCanvas() {
        if (!this.elements.canvas) return;
        const resize = () => {
            const dpr = window.devicePixelRatio || 1;
            const rect = this.elements.canvas.getBoundingClientRect();
            this.elements.canvas.width = rect.width * dpr;
            this.elements.canvas.height = rect.height * dpr;
            this.canvasCtx.scale(dpr, dpr);
            this._drawIdle();
        };
        resize();
        window.addEventListener('resize', resize);
        this._resizeHandler = resize;
    }

    _drawIdle() {
        if (!this.elements.canvas) return;
        const width = this.elements.canvas.getBoundingClientRect().width;
        const height = this.elements.canvas.getBoundingClientRect().height;
        this.canvasCtx.fillStyle = 'var(--ww-bg-visualizer, #1a1a2e)';
        this.canvasCtx.fillRect(0, 0, width, height);
        this.canvasCtx.beginPath();
        this.canvasCtx.strokeStyle = 'var(--ww-accent, #e94560)';
        this.canvasCtx.lineWidth = 2;
        this.canvasCtx.moveTo(0, height / 2);
        this.canvasCtx.lineTo(width, height / 2);
        this.canvasCtx.stroke();
    }

    _drawVisualizer() {
        if (!this.state.analyser || !this.elements.canvas) return;
        const width = this.elements.canvas.getBoundingClientRect().width;
        const height = this.elements.canvas.getBoundingClientRect().height;
        const bufferLength = this.state.analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);
        const draw = () => {
            this.state.animationId = requestAnimationFrame(draw);
            this.state.analyser.getByteTimeDomainData(dataArray);
            this.canvasCtx.fillStyle = 'var(--ww-bg-visualizer, #1a1a2e)';
            this.canvasCtx.fillRect(0, 0, width, height);
            this.canvasCtx.lineWidth = 2;
            this.canvasCtx.strokeStyle = this.state.isRecording
                ? 'var(--ww-recording, #ef4444)'
                : 'var(--ww-accent, #e94560)';
            this.canvasCtx.beginPath();
            const sliceWidth = width / bufferLength;
            let x = 0;
            for (let i = 0; i < bufferLength; i++) {
                const v = dataArray[i] / 128.0;
                const y = (v * height) / 2;
                if (i === 0) this.canvasCtx.moveTo(x, y);
                else this.canvasCtx.lineTo(x, y);
                x += sliceWidth;
            }
            this.canvasCtx.lineTo(width, height / 2);
            this.canvasCtx.stroke();
        };
        draw();
    }

    _updateTimer() {
        if (!this.state.startTime || !this.elements.timer) return;
        const elapsed = Math.floor((Date.now() - this.state.startTime) / 1000);
        const minutes = Math.floor(elapsed / 60);
        const seconds = elapsed % 60;
        this.elements.timer.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }

    _setStatus(status, text) {
        this.elements.statusDot.className = 'ww-status-dot ww-status-' + status;
        this.elements.statusText.textContent = text;
    }

    _emit(eventName, detail = {}) {
        const event = new CustomEvent(`whisper:${eventName}`, { detail, bubbles: true });
        this.container.dispatchEvent(event);
    }

    async toggle() {
        if (this.state.isRecording) this.stop();
        else await this.start();
    }

    async start() {
        if (this.state.isRecording || this.state.isProcessing) return;
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                audio: { channelCount: 1, sampleRate: 16000, echoCancellation: true, noiseSuppression: true }
            });
            this.state.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.state.analyser = this.state.audioContext.createAnalyser();
            this.state.analyser.fftSize = 2048;
            const source = this.state.audioContext.createMediaStreamSource(stream);
            source.connect(this.state.analyser);
            let mimeType = 'audio/webm';
            if (MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) mimeType = 'audio/webm;codecs=opus';
            else if (MediaRecorder.isTypeSupported('audio/ogg;codecs=opus')) mimeType = 'audio/ogg;codecs=opus';
            else if (MediaRecorder.isTypeSupported('audio/mp4')) mimeType = 'audio/mp4';
            this.state.mimeType = mimeType;
            this.state.mediaRecorder = new MediaRecorder(stream, { mimeType });
            this.state.audioChunks = [];
            this.state.stream = stream;
            this.state.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) this.state.audioChunks.push(event.data);
            };
            this.state.mediaRecorder.onstop = () => this._onRecordingStopped();
            this.state.mediaRecorder.start(100);
            this.state.isRecording = true;
            this.elements.recordBtn.classList.add('ww-recording');
            this._setStatus('recording', 'Recording...');
            this.state.startTime = Date.now();
            this.state.timerInterval = setInterval(() => this._updateTimer(), 100);
            this._drawVisualizer();
            this._emit('recording');
            if (this.options.onRecordingStart) this.options.onRecordingStart();
        } catch (err) {
            console.error('WhisperWidget: Error accessing microphone:', err);
            this._showError('Could not access microphone. Please grant permission.');
        }
    }

    stop() {
        if (!this.state.isRecording) return;
        if (this.state.mediaRecorder && this.state.mediaRecorder.state !== 'inactive') {
            this.state.mediaRecorder.stop();
        }
        this.state.isRecording = false;
        this.elements.recordBtn.classList.remove('ww-recording');
        this._setStatus('processing', 'Processing...');
        clearInterval(this.state.timerInterval);
        this.state.timerInterval = null;
        if (this.state.animationId) {
            cancelAnimationFrame(this.state.animationId);
            this.state.animationId = null;
        }
        this._emit('stopped');
        if (this.options.onRecordingStop) this.options.onRecordingStop();
    }

    async _onRecordingStopped() {
        this.state.isProcessing = true;
        const audioBlob = new Blob(this.state.audioChunks, { type: this.state.mimeType });
        if (this.state.stream) this.state.stream.getTracks().forEach(track => track.stop());
        if (this.state.audioContext) {
            this.state.audioContext.close();
            this.state.audioContext = null;
        }
        await this._transcribe(audioBlob);
        this.state.isProcessing = false;
        if (this.elements.timer) this.elements.timer.textContent = '0:00';
        this.state.startTime = null;
        this._drawIdle();
    }

    async _transcribe(audioBlob) {
        this._emit('processing');
        try {
            const formData = new FormData();
            let extension = 'webm';
            if (audioBlob.type.includes('ogg')) extension = 'ogg';
            else if (audioBlob.type.includes('mp4')) extension = 'mp4';
            else if (audioBlob.type.includes('wav')) extension = 'wav';
            formData.append('file', audioBlob, `recording.${extension}`);
            const response = await fetch(this.options.serverUrl, { method: 'POST', body: formData });
            if (!response.ok) throw new Error(`Server returned ${response.status}: ${response.statusText}`);
            const result = await response.json();
            if (result.text) {
                const text = result.text.trim();
                this._displayOutput(text);
                this._addToHistory(text);
                this._setStatus('ready', 'Ready');
                this._emit('transcription', { text });
                if (this.options.onTranscription) this.options.onTranscription(text);
            } else {
                throw new Error('No transcription text in response');
            }
        } catch (err) {
            console.error('WhisperWidget: Transcription error:', err);
            this._showError(`Transcription failed: ${err.message}`);
        }
    }

    _displayOutput(text) {
        this.elements.output.textContent = text;
        this.elements.output.removeAttribute('data-empty');
    }

    _showError(message) {
        this._setStatus('error', 'Error');
        this._emit('error', { message });
        if (this.options.onError) this.options.onError(message);
    }

    _addToHistory(text) {
        if (!this.options.showHistory) return;
        const timestamp = new Date().toLocaleTimeString();
        this.state.history.unshift({ text, timestamp });
        if (this.state.history.length > this.options.historyLimit) this.state.history.pop();
        this._renderHistory();
    }

    _renderHistory() {
        if (!this.elements.historySection) return;
        if (this.state.history.length === 0) {
            this.elements.historySection.style.display = 'none';
            return;
        }
        this.elements.historySection.style.display = 'block';
        this.elements.historyList.innerHTML = this.state.history.map(item => `
            <div class="ww-history-item">
                <span class="ww-history-text">${this._escapeHtml(item.text)}</span>
                <span class="ww-history-time">${item.timestamp}</span>
            </div>
        `).join('');
    }

    _escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    copy() {
        const text = this.elements.output.textContent;
        if (text && !this.elements.output.hasAttribute('data-empty')) {
            navigator.clipboard.writeText(text).then(() => {
                const btn = this.elements.copyBtn;
                const original = btn.textContent;
                btn.textContent = 'Copied!';
                btn.classList.add('ww-copied');
                setTimeout(() => {
                    btn.textContent = original;
                    btn.classList.remove('ww-copied');
                }, 2000);
            });
        }
    }

    clearHistory() {
        this.state.history = [];
        this._renderHistory();
    }

    getTranscription() {
        if (this.elements.output.hasAttribute('data-empty')) return null;
        return this.elements.output.textContent;
    }

    getHistory() { return [...this.state.history]; }
    setServerUrl(url) { this.options.serverUrl = url; }

    destroy() {
        if (this.state.isRecording) this.stop();
        if (this._resizeHandler) window.removeEventListener('resize', this._resizeHandler);
        this.container.innerHTML = '';
        this.container.classList.remove('whisper-widget');
    }
}

if (typeof module !== 'undefined' && module.exports) module.exports = WhisperWidget;
```

### whisper-widget.css

```css
.whisper-widget {
    --ww-bg-primary: #1a1a2e;
    --ww-bg-secondary: #16213e;
    --ww-bg-visualizer: #1a1a2e;
    --ww-text-primary: #eaeaea;
    --ww-text-secondary: #a0a0a0;
    --ww-accent: #e94560;
    --ww-accent-hover: #ff6b6b;
    --ww-success: #4ade80;
    --ww-recording: #ef4444;
    --ww-border-radius: 0.5rem;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--ww-bg-primary);
    color: var(--ww-text-primary);
    border-radius: var(--ww-border-radius);
    padding: 1rem;
    box-sizing: border-box;
}
.whisper-widget *, .whisper-widget *::before, .whisper-widget *::after { box-sizing: border-box; }
.ww-visualizer-section { display: flex; flex-direction: column; align-items: center; gap: 1rem; margin-bottom: 1rem; }
.ww-visualizer { width: 100%; height: 80px; background: var(--ww-bg-visualizer); border-radius: var(--ww-border-radius); }
.ww-controls { display: flex; gap: 1rem; align-items: center; justify-content: center; }
.ww-timer { font-family: 'Monaco', 'Consolas', monospace; font-size: 1.25rem; color: var(--ww-text-primary); min-width: 60px; text-align: center; }
.ww-record-btn { width: 60px; height: 60px; border-radius: 50%; border: 3px solid var(--ww-accent); background: transparent; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.3s ease; padding: 0; }
.ww-record-btn:hover { background: rgba(233, 69, 96, 0.1); transform: scale(1.05); }
.ww-record-btn:focus { outline: none; box-shadow: 0 0 0 3px rgba(233, 69, 96, 0.3); }
.ww-record-icon { width: 28px; height: 28px; background: var(--ww-accent); border-radius: 50%; transition: all 0.3s ease; }
.ww-record-btn.ww-recording { border-color: var(--ww-recording); animation: ww-pulse 1.5s infinite; }
.ww-record-btn.ww-recording .ww-record-icon { background: var(--ww-recording); border-radius: 4px; width: 22px; height: 22px; }
@keyframes ww-pulse { 0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); } 50% { box-shadow: 0 0 0 15px rgba(239, 68, 68, 0); } }
.ww-status { display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; color: var(--ww-text-secondary); min-width: 100px; }
.ww-status-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--ww-text-secondary); flex-shrink: 0; }
.ww-status-dot.ww-status-ready { background: var(--ww-success); }
.ww-status-dot.ww-status-recording { background: var(--ww-recording); animation: ww-blink 0.8s infinite; }
.ww-status-dot.ww-status-processing { background: #fbbf24; animation: ww-blink 0.5s infinite; }
.ww-status-dot.ww-status-error { background: var(--ww-recording); }
@keyframes ww-blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
.ww-output-section { background: var(--ww-bg-secondary); border-radius: var(--ww-border-radius); padding: 0.75rem; }
.ww-output-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }
.ww-output-label { font-size: 0.75rem; font-weight: 600; color: var(--ww-text-secondary); text-transform: uppercase; letter-spacing: 0.05em; }
.ww-copy-btn { background: transparent; border: 1px solid var(--ww-text-secondary); color: var(--ww-text-secondary); padding: 0.25rem 0.5rem; border-radius: 0.25rem; cursor: pointer; font-size: 0.75rem; transition: all 0.2s ease; }
.ww-copy-btn:hover { border-color: var(--ww-accent); color: var(--ww-accent); }
.ww-copy-btn.ww-copied { border-color: var(--ww-success); color: var(--ww-success); }
.ww-output { min-height: 60px; font-size: 0.95rem; line-height: 1.5; white-space: pre-wrap; word-wrap: break-word; }
.ww-output[data-empty="true"] { color: var(--ww-text-secondary); font-style: italic; }
.ww-history-section { margin-top: 1rem; background: var(--ww-bg-secondary); border-radius: var(--ww-border-radius); padding: 0.75rem; }
.ww-history-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }
.ww-history-label { font-size: 0.75rem; font-weight: 600; color: var(--ww-text-secondary); text-transform: uppercase; letter-spacing: 0.05em; }
.ww-clear-btn { background: transparent; border: none; color: var(--ww-text-secondary); cursor: pointer; font-size: 0.75rem; padding: 0; transition: color 0.2s ease; }
.ww-clear-btn:hover { color: var(--ww-accent); }
.ww-history-list { display: flex; flex-direction: column; gap: 0.5rem; max-height: 200px; overflow-y: auto; }
.ww-history-item { background: var(--ww-bg-primary); padding: 0.5rem 0.75rem; border-radius: 0.25rem; font-size: 0.85rem; display: flex; justify-content: space-between; align-items: flex-start; gap: 0.5rem; }
.ww-history-text { flex: 1; word-break: break-word; }
.ww-history-time { color: var(--ww-text-secondary); font-size: 0.7rem; white-space: nowrap; }

/* Variants */
.whisper-widget.ww-compact .ww-visualizer { height: 50px; }
.whisper-widget.ww-compact .ww-record-btn { width: 50px; height: 50px; }
.whisper-widget.ww-compact .ww-record-icon { width: 22px; height: 22px; }
.whisper-widget.ww-compact .ww-timer { font-size: 1rem; }

.whisper-widget.ww-minimal .ww-visualizer-section { margin-bottom: 0; }
.whisper-widget.ww-minimal .ww-visualizer, .whisper-widget.ww-minimal .ww-timer, .whisper-widget.ww-minimal .ww-status, .whisper-widget.ww-minimal .ww-output-section, .whisper-widget.ww-minimal .ww-history-section { display: none !important; }

.whisper-widget.ww-light { --ww-bg-primary: #f5f5f5; --ww-bg-secondary: #e5e5e5; --ww-bg-visualizer: #e5e5e5; --ww-text-primary: #1a1a1a; --ww-text-secondary: #666666; }

.whisper-widget.ww-inline { display: flex; align-items: center; gap: 1rem; padding: 0.5rem; }
.whisper-widget.ww-inline .ww-visualizer-section { flex-direction: row; margin-bottom: 0; flex-shrink: 0; }
.whisper-widget.ww-inline .ww-visualizer { width: 120px; height: 40px; }
.whisper-widget.ww-inline .ww-record-btn { width: 40px; height: 40px; border-width: 2px; }
.whisper-widget.ww-inline .ww-record-icon { width: 18px; height: 18px; }
.whisper-widget.ww-inline .ww-record-btn.ww-recording .ww-record-icon { width: 14px; height: 14px; }
.whisper-widget.ww-inline .ww-timer { font-size: 0.875rem; min-width: 40px; }
.whisper-widget.ww-inline .ww-status { display: none; }
.whisper-widget.ww-inline .ww-output-section { flex: 1; min-width: 0; }
.whisper-widget.ww-inline .ww-output { min-height: auto; font-size: 0.875rem; }
.whisper-widget.ww-inline .ww-history-section { display: none; }
```

## Common Integration Patterns

### Append to textarea

```javascript
const widget = new WhisperWidget('#voice-input', {
    serverUrl: '/whisper/inference',
    showHistory: false,
    onTranscription: (text) => {
        const textarea = document.getElementById('myTextarea');
        textarea.value += text + ' ';
        textarea.focus();
    }
});
```

### Replace input value

```javascript
const widget = new WhisperWidget('#voice-input', {
    serverUrl: '/whisper/inference',
    onTranscription: (text) => {
        document.getElementById('searchInput').value = text;
    }
});
```

### Trigger form submit

```javascript
const widget = new WhisperWidget('#voice-input', {
    serverUrl: '/whisper/inference',
    onTranscription: (text) => {
        document.getElementById('chatInput').value = text;
        document.getElementById('chatForm').submit();
    }
});
```

### Minimal button only

```html
<div id="mic-btn" class="ww-minimal"></div>
<script>
new WhisperWidget('#mic-btn', {
    serverUrl: '/whisper/inference',
    showVisualizer: false,
    showTimer: false,
    showHistory: false,
    onTranscription: (text) => handleVoiceInput(text)
});
</script>
```

## Server Requirements

The widget expects a whisper.cpp server running with the `/inference` endpoint.

**Start whisper-server:**
```bash
whisper-server -m /path/to/model.bin --port 8080
```

**Reverse proxy example (nginx):**
```nginx
location /whisper/ {
    proxy_pass http://localhost:8080/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    client_max_body_size 50M;
}
```

## Workflow

1. Copy `whisper-widget.js` and `whisper-widget.css` to project
2. Include both files in HTML
3. Create container element with desired variant class
4. Initialize with target element selector and options
5. Handle `onTranscription` callback to use the text
