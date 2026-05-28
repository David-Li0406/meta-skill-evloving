# gencast Voice Options

gencast supports 6 different voices from OpenAI's TTS API. You can assign different voices to HOST1 and HOST2 to create conversational variety.

## Available Voices

### alloy
- **Character:** Neutral, balanced
- **Tone:** Professional, clear
- **Best for:** Educational content, technical explanations

### echo
- **Character:** Warm, friendly (DEFAULT for HOST2)
- **Tone:** Approachable, conversational
- **Best for:** Casual discussions, beginner content

### fable
- **Character:** Expressive, dynamic
- **Tone:** Storytelling, engaging
- **Best for:** Narrative content, interviews

### onyx
- **Character:** Deep, authoritative
- **Tone:** Formal, commanding
- **Best for:** Academic content, debates

### nova
- **Character:** Bright, energetic (DEFAULT for HOST1)
- **Tone:** Enthusiastic, clear
- **Best for:** Educational content, general audiences

### shimmer
- **Character:** Soft, gentle
- **Tone:** Calm, soothing
- **Best for:** Reflective content, accessible explanations

## Default Configuration

```bash
HOST1: nova
HOST2: echo
```

This pairing creates:
- Bright, energetic lead voice (nova)
- Warm, friendly supporting voice (echo)
- Good contrast for conversational flow

## Usage

### Specify Voices

```bash
gencast doc.md --minimal --host1-voice nova --host2-voice echo
```

### Common Pairings

**Educational (Balanced Authority + Warmth):**
```bash
--host1-voice alloy --host2-voice echo
```

**Technical (Professional Clarity):**
```bash
--host1-voice nova --host2-voice alloy
```

**Storytelling (Dynamic + Expressive):**
```bash
--host1-voice fable --host2-voice shimmer
```

**Academic (Authority + Depth):**
```bash
--host1-voice onyx --host2-voice alloy
```

**Casual (Friendly + Approachable):**
```bash
--host1-voice echo --host2-voice shimmer
```

## Voice Selection Tips

1. **Contrast is key** - Choose voices with different characteristics for better dialogue distinction
2. **Match content tone** - Formal content → onyx/alloy, Casual content → echo/shimmer
3. **Consider audience** - Beginners → echo/shimmer, Technical → alloy/nova
4. **Test pairings** - Different voice combinations create different conversational dynamics

## Examples

### Example 1: Technical Tutorial
```bash
gencast api_docs.md --minimal --host1-voice nova --host2-voice alloy --audience technical
```
Bright lead (nova) asks questions, professional support (alloy) explains.

### Example 2: Beginner Course
```bash
gencast intro.md --minimal --host1-voice echo --host2-voice shimmer --audience beginner
```
Warm, gentle pairing for approachable learning.

### Example 3: Research Discussion
```bash
gencast paper.md --minimal --host1-voice onyx --host2-voice alloy --style debate
```
Authoritative voices for serious academic discussion.

### Example 4: Storytelling
```bash
gencast story.md --minimal --host1-voice fable --host2-voice shimmer --style casual
```
Expressive narrator with gentle supporting voice.
