# Available Voices

The Eleven Labs v3 model supports the following voices:

| Voice | Description | Best For |
|-------|-------------|----------|
| **George** | Professional male, clear and authoritative | Business, corporate presentations |
| **Aria** | Professional female, warm and engaging | Training, educational content |
| **Rachel** | Conversational female, friendly tone | Casual content, explainers |
| **Sam** | Young male, energetic and dynamic | Marketing, tech demos |
| **Charlie** | Neutral, authoritative presence | Documentaries, formal content |
| **Emily** | Soft female, calming tone | Wellness, meditation, gentle topics |

## Default Voice

The default voice is **George**, which works well for most professional presentations.

## Usage

Specify the voice in your presentation config:

```python
config = PresentationConfig(
    slides=[...],
    voice="Aria",  # Use Aria voice
    ...
)
```

Or in JSON config:

```json
{
    "voice": "Aria",
    "slides": [...]
}
```

## Tips

- **Corporate/Business**: George or Charlie
- **Training/Education**: Aria or Emily
- **Marketing/Sales**: Sam or Rachel
- **Technical/Demo**: George or Sam
- **Wellness/Soft topics**: Emily
