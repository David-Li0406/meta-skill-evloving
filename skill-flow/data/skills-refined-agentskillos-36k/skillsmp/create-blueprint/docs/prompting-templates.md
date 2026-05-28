# Prompting Templates by Use Case

This guide provides prompting patterns organized by use case. Each template lists which models it works best with.

## Table of Contents

- [Video Templates](#video-templates)
- [Image Templates](#image-templates)
- [Audio Templates](#audio-templates)

---

## Video Templates

### Cinematic Scene with Dialogue

**Applicable models:** Veo 3.1, Sora 2

**When to use:** When generating video clips that include natural dialogue or ambient sound.

**Template structure:**
```
[Scene description], [character action], [camera movement], [mood/lighting], [audio elements]
```

**Example:**
```
A woman in a red dress walks through a sunlit café, ordering coffee from the barista.
Medium shot, natural lighting, ambient café sounds with soft jazz in the background.
```

**Tips:**
- Mention audio elements explicitly when using `GenerateAudio: true`
- Include camera movement descriptions
- Specify lighting conditions

---

### Animation / Stylized Motion

**Applicable models:** Seedance (all versions)

**When to use:** For animated or stylized video content with expressive character movement.

**Template structure:**
```
[Animation style], [character description], [action], [environment], [motion quality]
```

**Example:**
```
Anime-style, a young warrior with flowing blue hair leaps across rooftops at sunset.
Dynamic camera following the motion, vibrant colors, smooth fluid animation.
```

**Tips:**
- Specify animation style explicitly (anime, 3D, cartoon)
- Describe motion quality (fluid, snappy, exaggerated)
- Use `CameraFixed: false` for dynamic camera

---

### Smooth Frame-to-Frame Transition

**Applicable models:** Hailuo (02, 2.3), Kling (o1)

**When to use:** When interpolating between a start and end image with smooth motion.

**Template structure:**
```
[Start state] transitioning to [end state], [motion type], [duration feel]
```

**Example:**
```
A flower bud slowly blooming into a full rose, time-lapse style,
gradual transformation with petals unfurling one by one.
```

**Tips:**
- Describe the transformation explicitly
- Mention timing (slow, rapid, gradual)
- Use `EndImage` input for target frame

---

### Consistent Character Across Shots

**Applicable models:** WAN 2.6 (reference-to-video), Veo 3.1 (reference-to-video)

**When to use:** When a character or product must look the same across multiple video clips.

**Template structure:**
```
[Subject from reference] doing [action] in [environment], [style consistency note]
```

**Example:**
```
The character from the reference video walks through a busy marketplace,
maintaining their distinct blue jacket and casual stride, cinematic lighting.
```

**Tips:**
- Reference the subject without over-describing (the model has the reference)
- Focus on the new action/environment
- Use `ReferenceImages` or `ReferenceVideos` input

---

### Talking Head from Audio

**Applicable models:** Creatify Aurora, VEED Fabric, InfiniTalk

**When to use:** Creating lip-synced video from pre-existing audio.

**Template structure:**
```
[Character demeanor], [head/body movement], [background], [expression]
```

**Example:**
```
Professional speaker, subtle head movements, neutral office background,
engaged and confident expression.
```

**Tips:**
- Focus on non-speech visual elements
- The audio drives the lip sync
- Keep backgrounds simple for better results

---

## Image Templates

### Product Photography

**Applicable models:** SeedDream 4.5, GPT Image 1.5, Qwen Image

**When to use:** Generating clean product images for marketing.

**Template structure:**
```
[Product description], [angle], [lighting], [background], [style]
```

**Example:**
```
Sleek smartphone on a marble surface, 45-degree angle, soft studio lighting,
clean white background, professional product photography style.
```

**Tips:**
- Use `Background: transparent` for GPT Image when isolation is needed
- Specify lighting (soft, dramatic, natural)
- Mention photographic style

---

### Character Portrait

**Applicable models:** SeedDream 4/4.5, Flux Pro Kontext

**When to use:** Creating consistent character images for video workflows.

**Template structure:**
```
[Character description], [pose], [expression], [clothing], [style], [lighting]
```

**Example:**
```
A middle-aged man with gray beard, facing camera, warm smile,
wearing a blue button-down shirt, photorealistic portrait, soft natural lighting.
```

**Tips:**
- Be specific about distinctive features
- Consistent descriptions help with character continuity
- Use `Seed` for reproducibility across variations

---

### Scene Composition

**Applicable models:** Qwen Image, WAN v2.6

**When to use:** Creating detailed scenes with multiple elements.

**Template structure:**
```
[Main subject], [secondary elements], [environment], [atmosphere], [style]
```

**Example:**
```
A cozy living room with a leather armchair by the fireplace,
bookshelves lining the walls, warm evening light streaming through windows,
hygge atmosphere, interior design photography.
```

**Tips:**
- Use `NegativePrompt` to exclude unwanted elements
- Layer details from foreground to background
- Specify atmosphere/mood

---

### Image Editing with Mask

**Applicable models:** GPT Image 1.5 (edit), Qwen Image Edit

**When to use:** Modifying specific regions of an existing image.

**Template structure:**
```
Replace [masked area] with [new content], maintaining [consistency requirements]
```

**Example:**
```
Replace the sky with a dramatic sunset,
maintaining the lighting direction and color temperature on the buildings.
```

**Tips:**
- Use white in mask for areas to edit
- Reference elements that should stay consistent
- Keep edits localized for best results

---

## Audio Templates

### Expressive Narration with Emotion

**Applicable models:** MiniMax Speech (all versions)

**When to use:** When the narration needs emotional depth and variation.

**Text preparation:**
- Write naturally with punctuation for pacing
- Use ellipses (...) for pauses
- Exclamation marks for emphasis

**Key settings:**
- `Emotion`: Match the content (happy, sad, angry, neutral, surprised, fearful, disgusted)
- `Pitch`: Adjust for character (higher for excitement, lower for gravitas)
- `Speed`: Slower for emphasis, faster for urgency

**Example text:**
```
And then... everything changed. The door swung open, revealing what we had feared most!
```

---

### Natural Conversational Voice

**Applicable models:** ElevenLabs v3, Chatterbox

**When to use:** For documentary-style or natural narration.

**Text preparation:**
- Write in a conversational tone
- Short to medium sentences
- Natural pauses with commas and periods

**Key settings:**
- `Speed`: 1.0 for natural pace, 0.9 for emphasis
- Use `ReferenceAudioUrl` (Chatterbox) for specific voice matching

**Example text:**
```
What makes this discovery so remarkable is not just what was found,
but how it changes our understanding of the past.
```

---

### Background Music with Mood

**Applicable models:** Stable Audio 2.5, MiniMax Music 1.5

**When to use:** Creating ambient or mood-setting background tracks.

**Prompt structure:**
```
[Genre], [mood], [instruments], [tempo], [purpose]
```

**Example:**
```
Ambient electronic, calm and contemplative, soft synthesizer pads and gentle piano,
slow tempo, background music for a documentary about nature.
```

**Tips:**
- Be specific about tempo (BPM if known)
- Mention purpose to set appropriate energy
- Use `Duration` for instrumental (Stable Audio)

---

### Song with Lyrics

**Applicable models:** MiniMax Music 1.5

**When to use:** Creating songs with vocals and structure.

**Lyrics format:**
```
[intro]
(Instrumental intro)

[verse]
First line of the verse
Second line with the story
Building up the narrative

[chorus]
The memorable hook goes here
Repeat the main message
Catchy and singable

[bridge]
A contrasting section
Different melody or mood

[outro]
Final thoughts
(Fade out)
```

**Prompt example:**
```
Indie pop, upbeat and hopeful, acoustic guitar and light drums,
female vocals, summery feel
```

---

## General Tips

### For All Video Models
- Start with the main subject and action
- Include camera information when relevant
- Specify lighting and mood
- Keep prompts focused (avoid conflicting instructions)

### For All Image Models
- Lead with the most important element
- Layer details from important to less important
- Use negative prompts to exclude common issues
- Specify style/medium (photo, illustration, 3D render)

### For All Audio Models
- Match text punctuation to desired pacing
- Consider the emotional arc of the content
- Test with short samples before long generations
- Use consistent voice settings across related clips
