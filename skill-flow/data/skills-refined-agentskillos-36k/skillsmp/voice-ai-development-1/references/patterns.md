# Voice AI Development

## Patterns


---
  #### **Name**
OpenAI Realtime API
  #### **Description**
Native voice-to-voice with GPT-4o
  #### **When To Use**
When you want integrated voice AI without separate STT/TTS
  #### **Implementation**
    import asyncio
    import websockets
    import json
    import base64
    
    OPENAI_API_KEY = "sk-..."
    
    async def voice_session():
        url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "OpenAI-Beta": "realtime=v1"
        }
    
        async with websockets.connect(url, extra_headers=headers) as ws:
            # Configure session
            await ws.send(json.dumps({
                "type": "session.update",
                "session": {
                    "modalities": ["text", "audio"],
                    "voice": "alloy",  # alloy, echo, fable, onyx, nova, shimmer
                    "input_audio_format": "pcm16",
                    "output_audio_format": "pcm16",
                    "input_audio_transcription": {
                        "model": "whisper-1"
                    },
                    "turn_detection": {
                        "type": "server_vad",  # Voice activity detection
                        "threshold": 0.5,
                        "prefix_padding_ms": 300,
                        "silence_duration_ms": 500
                    },
                    "tools": [
                        {
                            "type": "function",
                            "name": "get_weather",
                            "description": "Get weather for a location",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "location": {"type": "string"}
                                }
                            }
                        }
                    ]
                }
            }))
    
            # Send audio (PCM16, 24kHz, mono)
            async def send_audio(audio_bytes):
                await ws.send(json.dumps({
                    "type": "input_audio_buffer.append",
                    "audio": base64.b64encode(audio_bytes).decode()
                }))
    
            # Receive events
            async for message in ws:
                event = json.loads(message)
    
                if event["type"] == "response.audio.delta":
                    # Play audio chunk
                    audio = base64.b64decode(event["delta"])
                    play_audio(audio)
    
                elif event["type"] == "response.audio_transcript.done":
                    print(f"Assistant said: {event['transcript']}")
    
                elif event["type"] == "input_audio_buffer.speech_started":
                    print("User started speaking")
    
                elif event["type"] == "response.function_call_arguments.done":
                    # Handle tool call
                    name = event["name"]
                    args = json.loads(event["arguments"])
                    result = call_function(name, args)
                    await ws.send(json.dumps({
                        "type": "conversation.item.create",
                        "item": {
                            "type": "function_call_output",
                            "call_id": event["call_id"],
                            "output": json.dumps(result)
                        }
                    }))
    

---
  #### **Name**
Vapi Voice Agent
  #### **Description**
Build voice agents with Vapi platform
  #### **When To Use**
Phone-based agents, quick deployment
  #### **Implementation**
    # Vapi provides hosted voice agents with webhooks
    
    from flask import Flask, request, jsonify
    import vapi
    
    app = Flask(__name__)
    client = vapi.Vapi(api_key="...")
    
    # Create an assistant
    assistant = client.assistants.create(
        name="Support Agent",
        model={
            "provider": "openai",
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful support agent..."
                }
            ]
        },
        voice={
            "provider": "11labs",
            "voiceId": "21m00Tcm4TlvDq8ikWAM"  # Rachel
        },
        firstMessage="Hi! How can I help you today?",
        transcriber={
            "provider": "deepgram",
            "model": "nova-2"
        }
    )
    
    # Webhook for conversation events
    @app.route("/vapi/webhook", methods=["POST"])
    def vapi_webhook():
        event = request.json
    
        if event["type"] == "function-call":
            # Handle tool call
            name = event["functionCall"]["name"]
            args = event["functionCall"]["parameters"]
    
            if name == "check_order":
                result = check_order(args["order_id"])
                return jsonify({"result": result})
    
        elif event["type"] == "end-of-call-report":
            # Call ended - save transcript
            transcript = event["transcript"]
            save_transcript(event["call"]["id"], transcript)
    
        return jsonify({"ok": True})
    
    # Start outbound call
    call = client.calls.create(
        assistant_id=assistant.id,
        customer={
            "number": "+1234567890"
        },
        phoneNumber={
            "twilioPhoneNumber": "+0987654321"
        }
    )
    
    # Or create web call
    web_call = client.calls.create(
        assistant_id=assistant.id,
        type="web"
    )
    # Returns URL for WebRTC connection
    

---
  #### **Name**
Deepgram STT + ElevenLabs TTS
  #### **Description**
Best-in-class transcription and synthesis
  #### **When To Use**
High quality voice, custom pipeline
  #### **Implementation**
    import asyncio
    from deepgram import DeepgramClient, LiveTranscriptionEvents
    from elevenlabs import ElevenLabs
    
    # Deepgram real-time transcription
    deepgram = DeepgramClient(api_key="...")
    
    async def transcribe_stream(audio_stream):
        connection = deepgram.listen.live.v("1")
    
        async def on_transcript(result):
            transcript = result.channel.alternatives[0].transcript
            if transcript:
                print(f"Heard: {transcript}")
                if result.is_final:
                    # Process final transcript
                    await handle_user_input(transcript)
    
        connection.on(LiveTranscriptionEvents.Transcript, on_transcript)
    
        await connection.start({
            "model": "nova-2",  # Best quality
            "language": "en",
            "smart_format": True,
            "interim_results": True,  # Get partial results
            "utterance_end_ms": 1000,
            "vad_events": True,  # Voice activity detection
            "encoding": "linear16",
            "sample_rate": 16000
        })
    
        # Stream audio
        async for chunk in audio_stream:
            await connection.send(chunk)
    
        await connection.finish()
    
    # ElevenLabs streaming synthesis
    eleven = ElevenLabs(api_key="...")
    
    def text_to_speech_stream(text: str):
        """Stream TTS audio chunks."""
        audio_stream = eleven.text_to_speech.convert_as_stream(
            voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel
            model_id="eleven_turbo_v2_5",  # Fastest
            text=text,
            output_format="pcm_24000"  # Raw PCM for low latency
        )
    
        for chunk in audio_stream:
            yield chunk
    
    # Or with WebSocket for lowest latency
    async def tts_websocket(text_stream):
        async with eleven.text_to_speech.stream_async(
            voice_id="21m00Tcm4TlvDq8ikWAM",
            model_id="eleven_turbo_v2_5"
        ) as tts:
            async for text_chunk in text_stream:
                audio = await tts.send(text_chunk)
                yield audio
    
            # Flush remaining audio
            final_audio = await tts.flush()
            yield final_audio
    

---
  #### **Name**
LiveKit Real-time Infrastructure
  #### **Description**
WebRTC infrastructure for voice apps
  #### **When To Use**
Building custom real-time voice apps
  #### **Implementation**
    from livekit import api, rtc
    import asyncio
    
    # Server-side: Create room and tokens
    lk_api = api.LiveKitAPI(
        url="wss://your-livekit.livekit.cloud",
        api_key="...",
        api_secret="..."
    )
    
    async def create_room(room_name: str):
        room = await lk_api.room.create_room(
            api.CreateRoomRequest(name=room_name)
        )
        return room
    
    def create_token(room_name: str, participant_name: str):
        token = api.AccessToken(
            api_key="...",
            api_secret="..."
        )
        token.with_identity(participant_name)
        token.with_grants(api.VideoGrants(
            room_join=True,
            room=room_name
        ))
        return token.to_jwt()
    
    # Agent-side: Connect and process audio
    async def voice_agent(room_name: str):
        room = rtc.Room()
    
        @room.on("track_subscribed")
        def on_track(track, publication, participant):
            if track.kind == rtc.TrackKind.KIND_AUDIO:
                # Process incoming audio
                audio_stream = rtc.AudioStream(track)
                asyncio.create_task(process_audio(audio_stream))
    
        token = create_token(room_name, "agent")
        await room.connect("wss://your-livekit.livekit.cloud", token)
    
        # Publish agent's audio
        source = rtc.AudioSource(sample_rate=24000, num_channels=1)
        track = rtc.LocalAudioTrack.create_audio_track("agent-voice", source)
        await room.local_participant.publish_track(track)
    
        # Send audio from TTS
        async def speak(text: str):
            for audio_chunk in text_to_speech(text):
                await source.capture_frame(rtc.AudioFrame(
                    data=audio_chunk,
                    sample_rate=24000,
                    num_channels=1,
                    samples_per_channel=len(audio_chunk) // 2
                ))
    
        return room, speak
    
    # Process audio with STT
    async def process_audio(audio_stream):
        async for frame in audio_stream:
            # Send to Deepgram or other STT
            await transcriber.send(frame.data)
    

---
  #### **Name**
Full Voice Agent Pipeline
  #### **Description**
Complete voice agent with all components
  #### **When To Use**
Custom production voice agent
  #### **Implementation**
    import asyncio
    from dataclasses import dataclass
    from typing import AsyncIterator
    
    @dataclass
    class VoiceAgentConfig:
        stt_provider: str = "deepgram"
        tts_provider: str = "elevenlabs"
        llm_provider: str = "openai"
        vad_enabled: bool = True
        interrupt_enabled: bool = True
    
    class VoiceAgent:
        def __init__(self, config: VoiceAgentConfig):
            self.config = config
            self.is_speaking = False
            self.conversation_history = []
    
        async def process_audio_stream(
            self,
            audio_in: AsyncIterator[bytes],
            audio_out: asyncio.Queue
        ):
            """Main audio processing loop."""
    
            # STT streaming
            async def transcribe():
                transcript_buffer = ""
                async for audio_chunk in audio_in:
                    # Check for interruption
                    if self.is_speaking and self.config.interrupt_enabled:
                        if await self.detect_speech(audio_chunk):
                            await self.stop_speaking()
    
                    result = await self.stt.transcribe(audio_chunk)
                    if result.is_final:
                        yield result.transcript
    
            # Process transcripts
            async for user_text in transcribe():
                if not user_text.strip():
                    continue
    
                self.conversation_history.append({
                    "role": "user",
                    "content": user_text
                })
    
                # Generate response with streaming
                self.is_speaking = True
                async for audio_chunk in self.generate_response(user_text):
                    await audio_out.put(audio_chunk)
                self.is_speaking = False
    
        async def generate_response(self, text: str) -> AsyncIterator[bytes]:
            """Stream LLM response through TTS."""
    
            # Stream LLM tokens
            llm_stream = self.llm.stream_chat(self.conversation_history)
    
            # Buffer for TTS (need ~50 chars for good prosody)
            text_buffer = ""
            full_response = ""
    
            async for token in llm_stream:
                text_buffer += token
                full_response += token
    
                # Send to TTS when we have enough text
                if len(text_buffer) > 50 or token in ".!?":
                    async for audio in self.tts.synthesize_stream(text_buffer):
                        yield audio
                    text_buffer = ""
    
            # Flush remaining
            if text_buffer:
                async for audio in self.tts.synthesize_stream(text_buffer):
                    yield audio
    
            self.conversation_history.append({
                "role": "assistant",
                "content": full_response
            })
    
        async def detect_speech(self, audio: bytes) -> bool:
            """Voice activity detection."""
            # Use WebRTC VAD or Silero VAD
            return self.vad.is_speech(audio)
    
        async def stop_speaking(self):
            """Handle interruption."""
            self.is_speaking = False
            # Clear audio queue
            # Stop TTS generation
    
    # Latency optimization tips:
    # 1. Use streaming everywhere (STT, LLM, TTS)
    # 2. Start TTS before LLM finishes (~50 char buffer)
    # 3. Use PCM audio format (no encoding overhead)
    # 4. Keep WebSocket connections alive
    # 5. Use regional endpoints close to users
    

## Anti-Patterns


---
  #### **Name**
Non-streaming Pipeline
  #### **Description**
Wait for full response before TTS
  #### **Why Bad**
    Adds seconds of latency.
    User perceives as slow.
    Loses conversation flow.
    
  #### **What To Do Instead**
    Stream everything:
    - STT: interim results
    - LLM: token streaming
    - TTS: chunk streaming
    Start TTS before LLM finishes.
    

---
  #### **Name**
Ignoring Interruptions
  #### **Description**
Agent keeps talking when user speaks
  #### **Why Bad**
    Frustrating user experience.
    Feels like talking to a machine.
    Wastes time.
    
  #### **What To Do Instead**
    Implement barge-in detection.
    Use VAD to detect user speech.
    Stop TTS immediately.
    Clear audio queue.
    

---
  #### **Name**
Single Provider Lock-in
  #### **Description**
Using one provider for all components
  #### **Why Bad**
    May not be best quality.
    Single point of failure.
    Harder to optimize.
    
  #### **What To Do Instead**
    Mix best providers:
    - Deepgram for STT (speed + accuracy)
    - ElevenLabs for TTS (voice quality)
    - OpenAI/Anthropic for LLM
    

---
  #### **Name**
No VAD Configuration
  #### **Description**
Using default voice activity detection
  #### **Why Bad**
    Too sensitive = interrupts on noise.
    Too slow = delays response.
    Poor end-of-speech detection.
    
  #### **What To Do Instead**
    Tune VAD thresholds.
    Adjust silence duration.
    Test with real users.
    Consider Silero VAD.
    