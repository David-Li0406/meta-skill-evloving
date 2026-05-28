# Multimodal Mastery: Video, Audio, and Beyond (2026)

Gemini 3 is natively multimodal. This guide covers how to handle non-text data types efficiently.

## 1. Video Understanding

Gemini processes video by sampling frames (1 FPS by default).

-   **Native Upload**: Use the File API to upload `.mp4` or `.mov` files.
-   **Temporal Reasoning**: Ask questions about *when* something happened (e.g., "At what point does the user click the button?").
-   **Optimization**: For long videos (>1 hour), use the **Infinite Context Window** feature of Gemini 3 Pro.

## 2. Audio Processing

Gemini treats audio as a first-class citizen, not just a transcription task.

-   **Nuance Detection**: The model can detect sarcasm, emotion, and background noise.
-   **Direct Query**: Ask questions about the audio directly (e.g., "Summarize the key points and describe the speaker's tone.").

## 3. Large PDF and Document Sets

For high-fidelity document analysis:

-   **Visual Layout**: Gemini understands tables, charts, and diagrams within PDFs.
-   **OCR Replacement**: No need for separate OCR tools; Gemini reads handwritten text and complex fonts natively.

## 4. Multi-Image Logic

Comparing multiple images is a core strength.

```typescript
const parts = [
  { text: "Find the differences between these two screenshots." },
  { inlineData: { mimeType: "image/png", data: base64Image1 } },
  { inlineData: { mimeType: "image/png", data: base64Image2 } }
];
```

## 5. System Instructions for Multimodal

When working with video or images, be ultra-specific in your system instructions:

-   *Bad*: "Analyze this video."
-   *Good*: "You are a professional video editor. Transcribe all text on screen and provide a scene-by-scene breakdown of visual changes."

---
*Updated: January 22, 2026 - 17:15*
