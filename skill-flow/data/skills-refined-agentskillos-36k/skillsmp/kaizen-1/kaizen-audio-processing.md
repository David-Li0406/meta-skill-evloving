# Audio Processing

Whisper transcription and audio analysis.

## TranscriptionAgent

```python
from kaizen.agents import TranscriptionAgent, TranscriptionAgentConfig

config = TranscriptionAgentConfig()  # Uses Whisper
agent = TranscriptionAgent(config=config)

result = agent.transcribe(audio_path="/path/to/audio.mp3")
print(result['transcription'])
print(result['duration'])
print(result['language'])
```

## Performance
- Speed: ~0.5x real-time (1 min audio → ~30 sec processing)
- Cost: Free (local processing)
- Quality: Excellent
- Languages: 90+ supported

## References
- **Examples**: `apps/kailash-kaizen/examples/8-multi-modal/audio-transcription/`
