# AI Music & Audio Generation

## Patterns


---
  #### **Name**
Music Generation with MusicGen/Replicate
  #### **Description**
Generate music from text descriptions using Meta's MusicGen
  #### **When**
User needs AI-generated background music or soundtracks
  #### **Implementation**
    import Replicate from "replicate";
    
    const replicate = new Replicate({
      auth: process.env.REPLICATE_API_TOKEN,
    });
    
    interface MusicOptions {
      prompt: string;
      duration?: number;           // seconds (max 30)
      modelVersion?: "stereo-large" | "melody-large" | "large";
      inputAudio?: string;         // for melody conditioning
      temperature?: number;        // 0-1, higher = more random
      topK?: number;              // token sampling
      topP?: number;              // nucleus sampling
      cfgCoefficient?: number;    // classifier-free guidance
      seed?: number;              // for reproducibility
    }
    
    async function generateMusic(options: MusicOptions): Promise<string> {
      const {
        prompt,
        duration = 8,
        modelVersion = "stereo-large",
        inputAudio,
        temperature = 1.0,
        topK = 250,
        topP = 0,
        cfgCoefficient = 3,
        seed,
      } = options;
    
      // Validate duration (MusicGen max is 30 seconds)
      const safeDuration = Math.min(duration, 30);
    
      const input: Record<string, unknown> = {
        prompt,
        duration: safeDuration,
        model_version: modelVersion,
        output_format: "mp3",
        temperature,
        top_k: topK,
        top_p: topP,
        classifier_free_guidance: cfgCoefficient,
      };
    
      if (inputAudio) {
        input.input_audio = inputAudio;
        input.continuation = false; // Use as melody reference
      }
    
      if (seed !== undefined) {
        input.seed = seed;
      }
    
      const output = await replicate.run(
        "meta/musicgen:671ac645ce5e552cc63a54a2bbff63fcf798043055f2b43c18a9f16e11e82434",
        { input }
      );
    
      return output as string;
    }
    
    // Usage
    const audioUrl = await generateMusic({
      prompt: "upbeat electronic dance music with synths and drums, 120 BPM",
      duration: 15,
      modelVersion: "stereo-large",
    });
    

---
  #### **Name**
Text-to-Speech with ElevenLabs
  #### **Description**
High-quality voice synthesis for narration and dialogue
  #### **When**
User needs natural-sounding speech from text
  #### **Implementation**
    import { ElevenLabsClient } from "elevenlabs";
    import { Readable } from "stream";
    
    const elevenlabs = new ElevenLabsClient({
      apiKey: process.env.ELEVENLABS_API_KEY,
    });
    
    interface TTSOptions {
      text: string;
      voiceId: string;           // Use premade or cloned voice
      modelId?: string;          // eleven_multilingual_v2, eleven_turbo_v2
      stability?: number;        // 0-1, lower = more expressive
      similarityBoost?: number;  // 0-1, higher = closer to original
      style?: number;            // 0-1, style exaggeration
      useSpeakerBoost?: boolean; // enhance voice clarity
    }
    
    async function textToSpeech(options: TTSOptions): Promise<Buffer> {
      const {
        text,
        voiceId,
        modelId = "eleven_multilingual_v2",
        stability = 0.5,
        similarityBoost = 0.75,
        style = 0,
        useSpeakerBoost = true,
      } = options;
    
      const audioStream = await elevenlabs.textToSpeech.convert(voiceId, {
        text,
        model_id: modelId,
        voice_settings: {
          stability,
          similarity_boost: similarityBoost,
          style,
          use_speaker_boost: useSpeakerBoost,
        },
      });
    
      // Convert stream to buffer
      const chunks: Buffer[] = [];
      for await (const chunk of audioStream) {
        chunks.push(Buffer.from(chunk));
      }
    
      return Buffer.concat(chunks);
    }
    
    // Streaming version for real-time playback
    async function streamTextToSpeech(
      options: TTSOptions,
      onChunk: (chunk: Buffer) => void
    ): Promise<void> {
      const audioStream = await elevenlabs.textToSpeech.convertAsStream(
        options.voiceId,
        {
          text: options.text,
          model_id: options.modelId || "eleven_turbo_v2",
          voice_settings: {
            stability: options.stability || 0.5,
            similarity_boost: options.similarityBoost || 0.75,
          },
        }
      );
    
      for await (const chunk of audioStream) {
        onChunk(Buffer.from(chunk));
      }
    }
    
    // Get available voices
    async function getVoices() {
      const response = await elevenlabs.voices.getAll();
      return response.voices.map((voice) => ({
        id: voice.voice_id,
        name: voice.name,
        category: voice.category,
        description: voice.description,
        previewUrl: voice.preview_url,
      }));
    }
    

---
  #### **Name**
Voice Cloning with ElevenLabs
  #### **Description**
Create custom voice clones from audio samples
  #### **When**
User wants to clone a voice for consistent narration
  #### **Implementation**
    import { ElevenLabsClient } from "elevenlabs";
    import * as fs from "fs";
    
    const elevenlabs = new ElevenLabsClient({
      apiKey: process.env.ELEVENLABS_API_KEY,
    });
    
    // Instant Voice Clone (from 1-3 minute sample)
    async function createInstantVoiceClone(
      name: string,
      samplePaths: string[],
      description?: string
    ) {
      // Read audio files
      const files = samplePaths.map((path) => fs.createReadStream(path));
    
      const voice = await elevenlabs.voices.add({
        name,
        description: description || `Instant clone of ${name}`,
        files,
        labels: {
          type: "instant_clone",
        },
      });
    
      return {
        voiceId: voice.voice_id,
        name: voice.name,
      };
    }
    
    // Professional Voice Clone (requires 1-3 hours of audio)
    // This initiates the process - actual training takes time
    async function initiateProfessionalClone(
      name: string,
      sampleUrls: string[], // Links to high-quality audio
      description: string
    ) {
      // PVC requires verification - user must agree to terms
      // and may need to complete identity verification
    
      const response = await fetch(
        "https://api.elevenlabs.io/v1/voices/add/professional",
        {
          method: "POST",
          headers: {
            "xi-api-key": process.env.ELEVENLABS_API_KEY!,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name,
            description,
            sample_urls: sampleUrls,
          }),
        }
      );
    
      if (!response.ok) {
        throw new Error(`PVC initiation failed: ${response.statusText}`);
      }
    
      return response.json();
    }
    
    // Best practices for voice samples:
    // - Use high-quality recording (XLR mic, treated room)
    // - Aim for -6dB to -3dB peak levels
    // - No background noise, reverb, or music
    // - For instant: 1-3 minutes
    // - For professional: 1-3 hours
    // - Include varied emotional range and speaking styles
    

---
  #### **Name**
Sound Effects Generation
  #### **Description**
Generate sound effects using AudioGen
  #### **When**
User needs custom sound effects for games or videos
  #### **Implementation**
    import Replicate from "replicate";
    
    const replicate = new Replicate({
      auth: process.env.REPLICATE_API_TOKEN,
    });
    
    interface SFXOptions {
      prompt: string;            // Description of sound
      duration?: number;         // seconds
      guidanceScale?: number;    // 1-20, higher = closer to prompt
      temperature?: number;      // randomness
    }
    
    async function generateSoundEffect(options: SFXOptions): Promise<string> {
      const {
        prompt,
        duration = 5,
        guidanceScale = 3,
        temperature = 1.0,
      } = options;
    
      // Using AudioGen via Replicate
      const output = await replicate.run(
        "meta/audiogen:f8a0bac6-4f97-4e62-ad89-5e5c89c5d5f2",
        {
          input: {
            prompt,
            duration: Math.min(duration, 10), // AudioGen max 10s
            guidance_scale: guidanceScale,
            temperature,
          },
        }
      );
    
      return output as string;
    }
    
    // Alternative: Using Bark for short sound effects with speech
    async function generateSpeechWithEffects(text: string): Promise<string> {
      // Bark supports sound effects in text
      // [laughs], [sighs], [clears throat], [music], etc.
      const output = await replicate.run(
        "suno-ai/bark:b76242b40d67c76ab6742e987628a2a9ac019e11d56ab96c4e91ce03b79b2787",
        {
          input: {
            prompt: text,
            text_temp: 0.7,
            waveform_temp: 0.7,
          },
        }
      );
    
      return output.audio_out as string;
    }
    
    // SFX prompting tips:
    // - Be specific: "footsteps on wooden floor" not "walking"
    // - Include environment: "rain on metal roof in warehouse"
    // - Describe qualities: "deep rumbling thunder, distant"
    // - Avoid music terms for non-music sounds
    

---
  #### **Name**
Audio Watermarking with AudioSeal
  #### **Description**
Embed imperceptible watermarks for content provenance
  #### **When**
User needs to mark AI-generated audio for detection
  #### **Implementation**
    // AudioSeal is typically run server-side with PyTorch
    // This shows the integration pattern
    
    import { spawn } from "child_process";
    
    interface WatermarkResult {
      watermarkedAudioPath: string;
      secret: string; // The embedded message
    }
    
    interface DetectionResult {
      isWatermarked: boolean;
      confidence: number;
      decodedMessage?: string;
    }
    
    // Python script for AudioSeal (run on server)
    const AUDIOSEAL_SCRIPT = `
    import torch
    import torchaudio
    from audioseal import AudioSeal
    import sys
    import json
    
    def watermark_audio(input_path, output_path, message=None):
        # Load model
        model = AudioSeal.load_generator("audioseal_wm_16bits")
    
        # Load audio
        audio, sr = torchaudio.load(input_path)
        if sr != 16000:
            resampler = torchaudio.transforms.Resample(sr, 16000)
            audio = resampler(audio)
    
        # Generate watermark
        if message:
            # Convert message to bits
            msg_bits = torch.tensor([int(b) for b in format(int(message, 16), '016b')])
            watermarked = model.embed(audio.unsqueeze(0), msg_bits.unsqueeze(0))
        else:
            watermarked = model.embed(audio.unsqueeze(0))
    
        # Save
        torchaudio.save(output_path, watermarked.squeeze(0), 16000)
        return {"success": True}
    
    def detect_watermark(audio_path):
        detector = AudioSeal.load_detector("audioseal_detector_16bits")
    
        audio, sr = torchaudio.load(audio_path)
        if sr != 16000:
            resampler = torchaudio.transforms.Resample(sr, 16000)
            audio = resampler(audio)
    
        result = detector.detect(audio.unsqueeze(0))
    
        return {
            "is_watermarked": result.score > 0.5,
            "confidence": float(result.score),
            "message": result.message if hasattr(result, 'message') else None
        }
    
    if __name__ == "__main__":
        action = sys.argv[1]
        if action == "watermark":
            result = watermark_audio(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
        elif action == "detect":
            result = detect_watermark(sys.argv[2])
        print(json.dumps(result))
    `;
    
          // Node.js wrapper
          async function watermarkAudio(
            inputPath: string,
            outputPath: string,
            message?: string
          ): Promise<WatermarkResult> {
            return new Promise((resolve, reject) => {
              const args = ["watermark", inputPath, outputPath];
              if (message) args.push(message);
    
              const process = spawn("python", ["-c", AUDIOSEAL_SCRIPT, ...args]);
    
              let output = "";
              process.stdout.on("data", (data) => (output += data));
              process.stderr.on("data", (data) => console.error(data.toString()));
    
              process.on("close", (code) => {
                if (code === 0) {
                  resolve({
                    watermarkedAudioPath: outputPath,
                    secret: message || "default",
                  });
                } else {
                  reject(new Error("Watermarking failed"));
                }
              });
            });
          }
    
          async function detectWatermark(audioPath: string): Promise<DetectionResult> {
            return new Promise((resolve, reject) => {
              const process = spawn("python", [
                "-c",
                AUDIOSEAL_SCRIPT,
                "detect",
                audioPath,
              ]);
    
              let output = "";
              process.stdout.on("data", (data) => (output += data));
    
              process.on("close", (code) => {
                if (code === 0) {
                  const result = JSON.parse(output);
                  resolve({
                    isWatermarked: result.is_watermarked,
                    confidence: result.confidence,
                    decodedMessage: result.message,
                  });
                } else {
                  reject(new Error("Detection failed"));
                }
              });
            });
          }
    

---
  #### **Name**
Streaming Audio Response
  #### **Description**
Stream generated audio for real-time playback
  #### **When**
User needs audio to start playing before generation completes
  #### **Implementation**
    import { NextRequest, NextResponse } from "next/server";
    import { ElevenLabsClient } from "elevenlabs";
    
    const elevenlabs = new ElevenLabsClient({
      apiKey: process.env.ELEVENLABS_API_KEY,
    });
    
    // Next.js streaming TTS endpoint
    export async function POST(request: NextRequest) {
      const { text, voiceId } = await request.json();
    
      // Get streaming audio
      const audioStream = await elevenlabs.textToSpeech.convertAsStream(
        voiceId,
        {
          text,
          model_id: "eleven_turbo_v2", // Faster for streaming
          voice_settings: {
            stability: 0.5,
            similarity_boost: 0.75,
          },
        }
      );
    
      // Create readable stream for response
      const stream = new ReadableStream({
        async start(controller) {
          for await (const chunk of audioStream) {
            controller.enqueue(chunk);
          }
          controller.close();
        },
      });
    
      return new NextResponse(stream, {
        headers: {
          "Content-Type": "audio/mpeg",
          "Transfer-Encoding": "chunked",
        },
      });
    }
    
    // Frontend: Play streaming audio
    async function playStreamingAudio(text: string, voiceId: string) {
      const response = await fetch("/api/tts/stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, voiceId }),
      });
    
      // Use Media Source Extensions for streaming playback
      const mediaSource = new MediaSource();
      const audio = new Audio();
      audio.src = URL.createObjectURL(mediaSource);
    
      mediaSource.addEventListener("sourceopen", async () => {
        const sourceBuffer = mediaSource.addSourceBuffer("audio/mpeg");
        const reader = response.body!.getReader();
    
        while (true) {
          const { done, value } = await reader.read();
          if (done) {
            mediaSource.endOfStream();
            break;
          }
    
          // Wait for buffer to be ready
          await new Promise((resolve) => {
            if (sourceBuffer.updating) {
              sourceBuffer.addEventListener("updateend", resolve, { once: true });
            } else {
              resolve(undefined);
            }
          });
    
          sourceBuffer.appendBuffer(value);
        }
      });
    
      await audio.play();
    }
    

---
  #### **Name**
Lyria for High-Quality Music
  #### **Description**
Use Fal.ai's Lyria model for production music
  #### **When**
User needs higher quality AI music than MusicGen
  #### **Implementation**
    // Using Fal.ai's Lyria model for music generation
    // Lyria2 provides higher quality output
    
    interface LyriaOptions {
      prompt: string;
      duration?: number;
      negativePrompt?: string;
    }
    
    async function generateMusicWithLyria(options: LyriaOptions) {
      const response = await fetch("https://fal.run/fal-ai/lyria2", {
        method: "POST",
        headers: {
          Authorization: `Key ${process.env.FAL_KEY}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: options.prompt,
          duration_seconds: options.duration || 30,
          negative_prompt: options.negativePrompt,
        }),
      });
    
      if (!response.ok) {
        throw new Error(`Lyria generation failed: ${response.statusText}`);
      }
    
      const result = await response.json();
      return {
        audioUrl: result.audio.url,
        duration: result.audio.duration,
      };
    }
    
    // Music prompting best practices:
    // - Include genre: "synthwave", "lo-fi hip hop", "orchestral"
    // - Specify tempo: "120 BPM", "slow tempo", "upbeat"
    // - Describe mood: "melancholic", "energetic", "peaceful"
    // - Add instruments: "piano and strings", "electric guitar solo"
    // - Reference styles: "in the style of 80s synth pop"
    

## Anti-Patterns


---
  #### **Name**
Exposing audio API keys client-side
  #### **Why Bad**
Audio generation is expensive - leaked keys cause massive bills
  #### **Example Bad**
    // Frontend code with exposed key
    const elevenlabs = new ElevenLabsClient({
      apiKey: "sk-..." // Exposed in browser!
    });
    
  #### **Example Good**
    // Server-side only
    // app/api/tts/route.ts
    const elevenlabs = new ElevenLabsClient({
      apiKey: process.env.ELEVENLABS_API_KEY,
    });
    

---
  #### **Name**
No character/duration limits
  #### **Why Bad**
Single long text can cost $10+ in TTS charges
  #### **Example Bad**
    async function synthesize(text: string) {
      return elevenlabs.textToSpeech.convert(voiceId, { text });
    }
    
  #### **Example Good**
    async function synthesize(text: string) {
      if (text.length > 5000) {
        throw new Error("Text exceeds 5000 character limit");
      }
      // Also implement cost tracking
      await recordCost(userId, text.length * 0.00003); // ~$0.03/1000 chars
      return elevenlabs.textToSpeech.convert(voiceId, { text });
    }
    

---
  #### **Name**
Voice cloning without consent
  #### **Why Bad**
Creates deepfakes, legal liability, platform bans
  #### **Example Bad**
    // Clone any uploaded voice
    await createVoiceClone(userUploadedAudio);
    
  #### **Example Good**
    // Require explicit consent
    const consent = await db.voiceConsent.findUnique({
      where: { voiceOwnerEmail, voiceId },
    });
    
    if (!consent || !consent.verified) {
      throw new Error("Voice consent not verified");
    }
    
    await createVoiceClone(userUploadedAudio);
    

---
  #### **Name**
No content moderation on generated audio
  #### **Why Bad**
AI can generate harmful content (hate speech, misinformation)
  #### **Example Bad**
    // Generate without checking
    const audio = await textToSpeech(userInput);
    return audio;
    
  #### **Example Good**
    // Moderate text before synthesis
    const moderation = await openai.moderations.create({ input: userInput });
    if (moderation.results[0].flagged) {
      throw new Error("Content violates policy");
    }
    const audio = await textToSpeech(userInput);
    

---
  #### **Name**
Synchronous long audio generation
  #### **Why Bad**
Music generation takes 30-120+ seconds, blocks requests
  #### **Example Bad**
    // Blocks for 2+ minutes
    app.post("/api/music", async (req, res) => {
      const audio = await generateMusic(req.body.prompt);
      res.json({ audio });
    });
    
  #### **Example Good**
    // Queue-based async
    app.post("/api/music", async (req, res) => {
      const job = await musicQueue.add("generate", req.body);
      res.json({ jobId: job.id, status: "pending" });
    });
    