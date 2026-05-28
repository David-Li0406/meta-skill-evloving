# Openai-Api - Audio

**Pages:** 11

---

## Voice agents

**URL:** https://platform.openai.com/docs/guides/voice-agents

**Contents:**
- Voice agents
- Choose the right architecture
  - Speech-to-speech (realtime) architecture
  - Chained architecture
- Build a voice agent
  - Choose your transport method
  - Design your voice agent
  - Precisely prompt your agent
  - Handle agent handoff
  - Extend your agent with specialized models

Use the OpenAI API and Agents SDK to create powerful, context-aware voice agents for applications like customer support and language tutoring. This guide helps you design and build a voice agent.

OpenAI provides two primary architectures for building voice agents:

The multimodal speech-to-speech (S2S) architecture directly processes audio inputs and outputs, handling speech in real time in a single multimodal model, gpt-4o-realtime-preview. The model thinks and responds in speech. It doesn't rely on a transcript of the user's input—it hears emotion and intent, filters out noise, and responds directly in speech. Use this approach for highly interactive, low-latency, conversational use cases.

A chained architecture processes audio sequentially, converting audio to text, generating intelligent responses using large language models (LLMs), and synthesizing audio from text. We recommend this predictable architecture if you're new to building voice agents. Both the user input and model's response are in text, so you have a transcript and can control what happens in your application. It's also a reliable way to convert an existing LLM-based application into a voice agent.

You're chaining these models: gpt-4o-transcribe → gpt-4.1 → gpt-4o-mini-tts

The following guide below is for building agents using our recommended speech-to-speech architecture.

To learn more about the chained architecture, see the chained architecture guide.

Use OpenAI's APIs and SDKs to create powerful, context-aware voice agents.

Building a speech-to-speech voice agent requires:

If you are new to building voice agents, we recommend using the Realtime Agents in the TypeScript Agents SDK to get started with your voice agents.

If you want to get an idea of what interacting with a speech-to-speech voice agent looks like, check out our quickstart guide to get started or check out our example application below.

A collection of example speech-to-speech voice agents including handoffs and reasoning model validation.

As latency is critical in voice agent use cases, the Realtime API provides two low-latency transport methods:

The two transport methods for the Realtime API support largely the same capabilities, but which one is more suitable for you will depend on your use case.

WebRTC is generally the better choice if you are building client-side applications such as browser-based voice agents.

For anything where you are executing the agent server-side such as building an agent that can answer phone calls, WebSockets will be the better option.

If you are using the OpenAI Agents SDK for TypeScript, we will automatically use WebRTC if you are building in the browser and WebSockets otherwise.

Just like when designing a text-based agent, you'll want to start small and keep your agent focused on a single task.

Try to limit the number of tools your agent has access to and provide an escape hatch for the agent to deal with tasks that it is not equipped to handle.

This could be a tool that allows the agent to handoff the conversation to a human or a certain phrase that it can fall back to.

While providing tools to text-based agents is a great way to provide additional context to the agent, for voice agents you should consider giving critical information as part of the prompt as opposed to requiring the agent to call a tool first.

If you are just getting started, check out our Realtime Playground that provides prompt generation helpers, as well as a way to stub out your function tools including stubbed tool responses to try end to end flows.

With speech-to-speech agents, prompting is even more powerful than with text-based agents as the prompt allows you to not just control the content of the agent's response but also the way the agent speaks or help it understand audio content.

A good example of what a prompt might look like:

You do not have to be as detailed with your instructions. This is for illustrative purposes. For shorter examples, check out the prompts on OpenAI.fm.

For use cases with common conversation flows you can encode those inside the prompt using markup language like JSON

Instead of writing this out by hand, you can also check out this Voice Agent Metaprompter or copy the metaprompt and use it directly.

In order to keep your agent focused on a single task, you can provide the agent with the ability to transfer or handoff to another specialized agent. You can do this by providing the agent with a function tool to initiate the transfer. This tool should have information on when to use it for a handoff.

If you are using the OpenAI Agents SDK for TypeScript, you can define any agent as a potential handoff to another agent.

The SDK will automatically facilitate the handoff between the agents for you.

Alternatively if you are building your own voice agent, here is an example of such a tool definition:

Once the agent calls that tool you can then use the session.update event of the Realtime API to update the configuration of the session to use the instructions and tools available to the specialized agent.

While the speech-to-speech model is useful for conversational use cases, there might be use cases where you need a specific model to handle the task like having o3 validate a return request against a detailed return policy.

In that case you can expose your text-based agent using your preferred model as a function tool call that your agent can send specific requests to.

If you are using the OpenAI Agents SDK for TypeScript, you can give a RealtimeAgent a tool that will trigger the specialized agent on your server.

**Examples:**

Example 1 (unknown):
```unknown
npm install @openai/agents
```

Example 2 (bash):
```bash
npm install @openai/agents
```

Example 3 (unknown):
```unknown
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
# Personality and Tone
## Identity
// Who or what the AI represents (e.g., friendly teacher, formal advisor, helpful assistant). Be detailed and include specific details about their character or backstory.

## Task
// At a high level, what is the agent expected to do? (e.g. "you are an expert at accurately handling user returns")

## Demeanor
// Overall attitude or disposition (e.g., patient, upbeat, serious, empathetic)

## Tone
// Voice style (e.g., warm and conversational, polite and authoritative)

## Level of Enthusiasm
// Degree of energy in responses (e.g., highly enthusiastic vs. calm and measured)

## Level of Formality
// Casual vs. professional language (e.g., “Hey, great to see you!” vs. “Good afternoon, how may I assist you?”)

## Level of Emotion
// How emotionally expressive or neutral the AI should be (e.g., compassionate vs. matter-of-fact)

## Filler Words
// Helps make the agent more approachable, e.g. “um,” “uh,” "hm," etc.. Options are generally "none", "occasionally", "often", "very often"

## Pacing
// Rhythm and speed of delivery

## Other details
// Any other information that helps guide the personality or tone of the agent.

# Instructions
- If a user provides a name or phone number, or something else where you need to know the exact spelling, always repeat it back to the user to confirm you have the right understanding before proceeding. // Always include this
- If the caller corrects any detail, acknowledge the correction in a straightforward manner and confirm the new spelling or value.
```

Example 4 (text):
```text
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
# Personality and Tone
## Identity
// Who or what the AI represents (e.g., friendly teacher, formal advisor, helpful assistant). Be detailed and include specific details about their character or backstory.

## Task
// At a high level, what is the agent expected to do? (e.g. "you are an expert at accurately handling user returns")

## Demeanor
// Overall attitude or disposition (e.g., patient, upbeat, serious, empathetic)

## Tone
// Voice style (e.g., warm and conversational, polite and authoritative)

## Level of Enthusiasm
// Degree of energy in responses (e.g., highly enthusiastic vs. calm and measured)

## Level of Formality
// Casual vs. professional language (e.g., “Hey, great to see you!” vs. “Good afternoon, how may I assist you?”)

## Level of Emotion
// How emotionally expressive or neutral the AI should be (e.g., compassionate vs. matter-of-fact)

## Filler Words
// Helps make the agent more approachable, e.g. “um,” “uh,” "hm," etc.. Options are generally "none", "occasionally", "often", "very often"

## Pacing
// Rhythm and speed of delivery

## Other details
// Any other information that helps guide the personality or tone of the agent.

# Instructions
- If a user provides a name or phone number, or something else where you need to know the exact spelling, always repeat it back to the user to confirm you have the right understanding before proceeding. // Always include this
- If the caller corrects any detail, acknowledge the correction in a straightforward manner and confirm the new spelling or value.
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/realtime/create-call

**Contents:**
- Realtime
- Create call
    - Request body
    - Returns

Communicate with a multimodal model in real time over low latency interfaces like WebRTC, WebSocket, and SIP. Natively supports speech-to-speech as well as text, image, and audio inputs and outputs.

Learn more about the Realtime API.

Create a new Realtime API call over WebRTC and receive the SDP answer needed to complete the peer connection.

WebRTC Session Description Protocol (SDP) offer generated by the caller.

Optional session configuration to apply before the realtime session is created. Use the same parameters you would send in a create client secret request.

Returns 201 Created with the SDP answer in the response body. The Location response header includes the call ID for follow-up requests, e.g., establishing a monitoring WebSocket or hanging up the call.

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
4
curl -X POST https://api.openai.com/v1/realtime/calls \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F "sdp=<offer.sdp;type=application/sdp" \
  -F 'session={"type":"realtime","model":"gpt-realtime"};type=application/json'
```

Example 2 (bash):
```bash
1
2
3
4
curl -X POST https://api.openai.com/v1/realtime/calls \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F "sdp=<offer.sdp;type=application/sdp" \
  -F 'session={"type":"realtime","model":"gpt-realtime"};type=application/json'
```

Example 3 (unknown):
```unknown
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
v=0
o=- 4227147428 1719357865 IN IP4 127.0.0.1
s=-
c=IN IP4 0.0.0.0
t=0 0
a=group:BUNDLE 0 1
a=msid-semantic:WMS *
a=fingerprint:sha-256 CA:92:52:51:B4:91:3B:34:DD:9C:0B:FB:76:19:7E:3B:F1:21:0F:32:2C:38:01:72:5D:3F:78:C7:5F:8B:C7:36
m=audio 9 UDP/TLS/RTP/SAVPF 111 0 8
a=mid:0
a=ice-ufrag:kZ2qkHXX/u11
a=ice-pwd:uoD16Di5OGx3VbqgA3ymjEQV2kwiOjw6
a=setup:active
a=rtcp-mux
a=rtpmap:111 opus/48000/2
a=candidate:993865896 1 udp 2130706431 4.155.146.196 3478 typ host ufrag kZ2qkHXX/u11
a=candidate:1432411780 1 tcp 1671430143 4.155.146.196 443 typ host tcptype passive ufrag kZ2qkHXX/u11
m=application 9 UDP/DTLS/SCTP webrtc-datachannel
a=mid:1
a=sctp-port:5000
```

Example 4 (json):
```json
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
v=0
o=- 4227147428 1719357865 IN IP4 127.0.0.1
s=-
c=IN IP4 0.0.0.0
t=0 0
a=group:BUNDLE 0 1
a=msid-semantic:WMS *
a=fingerprint:sha-256 CA:92:52:51:B4:91:3B:34:DD:9C:0B:FB:76:19:7E:3B:F1:21:0F:32:2C:38:01:72:5D:3F:78:C7:5F:8B:C7:36
m=audio 9 UDP/TLS/RTP/SAVPF 111 0 8
a=mid:0
a=ice-ufrag:kZ2qkHXX/u11
a=ice-pwd:uoD16Di5OGx3VbqgA3ymjEQV2kwiOjw6
a=setup:active
a=rtcp-mux
a=rtpmap:111 opus/48000/2
a=candidate:993865896 1 udp 2130706431 4.155.146.196 3478 typ host ufrag kZ2qkHXX/u11
a=candidate:1432411780 1 tcp 1671430143 4.155.146.196 443 typ host tcptype passive ufrag kZ2qkHXX/u11
m=application 9 UDP/DTLS/SCTP webrtc-datachannel
a=mid:1
a=sctp-port:5000
```

---

## Realtime transcription

**URL:** https://platform.openai.com/docs/guides/realtime-transcription

**Contents:**
- Realtime transcription
- Realtime transcription sessions
  - Session fields
- Handling transcriptions
- Voice activity detection
- Additional configurations
  - Noise reduction
  - Using logprobs

You can use the Realtime API for transcription-only use cases, either with input from a microphone or from a file. For example, you can use it to generate subtitles or transcripts in real-time. With the transcription-only mode, the model will not generate responses.

If you want the model to produce responses, you can use the Realtime API in speech-to-speech conversation mode.

To use the Realtime API for transcription, you need to create a transcription session, connecting via WebSockets or WebRTC.

Unlike the regular Realtime API sessions for conversations, the transcription sessions typically don't contain responses from the model.

The transcription session object uses the same base session shape, but it always has a type of "transcription":

You can find more information about the transcription session object in the API reference.

When using the Realtime API for transcription, you can listen for the conversation.item.input_audio_transcription.delta and conversation.item.input_audio_transcription.completed events.

For whisper-1 the delta event will contain full turn transcript, same as completed event. For gpt-4o-transcribe and gpt-4o-mini-transcribe the delta event will contain incremental transcripts as they are streamed out from the model.

Here is an example transcription delta event:

Here is an example transcription completion event:

Note that ordering between completion events from different speech turns is not guaranteed. You should use item_id to match these events to the input_audio_buffer.committed events and use input_audio_buffer.committed.previous_item_id to handle the ordering.

To send audio data to the transcription session, you can use the input_audio_buffer.append event.

The Realtime API supports automatic voice activity detection (VAD). Enabled by default, VAD will control when the input audio buffer is committed, therefore when transcription begins.

Read more about configuring VAD in our Voice Activity Detection guide.

You can also disable VAD by setting the audio.input.turn_detection property to null, and control when to commit the input audio on your end.

Use the audio.input.noise_reduction property to configure how to handle noise reduction in the audio stream.

You can use the include property to include logprobs in the transcription events, using item.input_audio_transcription.logprobs.

Those logprobs can be used to calculate the confidence score of the transcription.

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
{
  "object": "realtime.session",
  "type": "transcription",
  "id": "session_abc123",
  "audio": {
    "input": {
      "format": {
        "type": "audio/pcm",
        "rate": 24000
      },
      "noise_reduction": {
        "type": "near_field"
      },
      "transcription": {
        "model": "gpt-4o-transcribe",
        "prompt": "",
        "language": "en"
      },
      "turn_detection": {
        "type": "server_vad",
        "threshold": 0.5,
        "prefix_padding_ms": 300,
        "silence_duration_ms": 500
      }
    }
  },
  "include": [
    "item.input_audio_transcription.logprobs"
  ]
}
```

Example 2 (json):
```json
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
{
  "object": "realtime.session",
  "type": "transcription",
  "id": "session_abc123",
  "audio": {
    "input": {
      "format": {
        "type": "audio/pcm",
        "rate": 24000
      },
      "noise_reduction": {
        "type": "near_field"
      },
      "transcription": {
        "model": "gpt-4o-transcribe",
        "prompt": "",
        "language": "en"
      },
      "turn_detection": {
        "type": "server_vad",
        "threshold": 0.5,
        "prefix_padding_ms": 300,
        "silence_duration_ms": 500
      }
    }
  },
  "include": [
    "item.input_audio_transcription.logprobs"
  ]
}
```

Example 3 (unknown):
```unknown
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
```

Example 4 (unknown):
```unknown
1
2
3
4
5
6
7
{
  "event_id": "event_2122",
  "type": "conversation.item.input_audio_transcription.delta",
  "item_id": "item_003",
  "content_index": 0,
  "delta": "Hello,"
}
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/realtime_beta

**Contents:**
- Realtime BetaLegacy

Communicate with a multimodal model in real time over low latency interfaces like WebRTC, WebSocket, and SIP. Natively supports speech-to-speech as well as text, image, and audio inputs and outputs. Learn more about the Realtime API.

---

## 

**URL:** https://platform.openai.com/docs/api-reference/audio/createTranscription

**Contents:**
- Audio
- Create speech
    - Request body
    - Returns
- Create voice
    - Request body
    - Returns
- Create voice consent
    - Request body
    - Returns

Learn how to turn audio into text or text into audio.

Related guide: Speech to text

Generates audio from the input text.

The text to generate audio for. The maximum length is 4096 characters.

One of the available TTS models: tts-1, tts-1-hd or gpt-4o-mini-tts.

The voice to use when generating the audio. Supported voices are alloy, ash, ballad, coral, echo, fable, onyx, nova, sage, shimmer, and verse. Previews of the voices are available in the Text to speech guide.

Control the voice of your generated audio with additional instructions. Does not work with tts-1 or tts-1-hd.

The format to audio in. Supported formats are mp3, opus, aac, flac, wav, and pcm.

The speed of the generated audio. Select a value from 0.25 to 4.0. 1.0 is the default.

The format to stream the audio in. Supported formats are sse and audio. sse is not supported for tts-1 or tts-1-hd.

The audio file content or a stream of audio events.

Create a custom voice you can use for audio output (for example, in Text-to-Speech and the Realtime API). This requires an audio sample and a previously uploaded consent recording.

See the custom voices guide for requirements and best practices. Custom voices are limited to eligible customers.

The sample audio recording file. Maximum size is 10 MiB.

Supported MIME types: audio/mpeg, audio/wav, audio/x-wav, audio/ogg, audio/aac, audio/flac, audio/webm, audio/mp4.

The consent recording ID (for example, cons_1234).

The name of the new voice.

Upload a consent recording that authorizes creation of a custom voice.

See the custom voices guide for requirements and best practices. Custom voices are limited to eligible customers.

The BCP 47 language tag for the consent phrase (for example, en-US).

The label to use for this consent recording.

The consent audio recording file. Maximum size is 10 MiB.

Supported MIME types: audio/mpeg, audio/wav, audio/x-wav, audio/ogg, audio/aac, audio/flac, audio/webm, audio/mp4.

The created voice consent recording metadata.

List consent recordings available to your organization for creating custom voices.

See the custom voices guide. Custom voices are limited to eligible customers.

A cursor for use in pagination. after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include after=obj_foo in order to fetch the next page of the list.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

A paginated list of voice consent recordings.

Retrieve consent recording metadata used for creating custom voices.

See the custom voices guide. Custom voices are limited to eligible customers.

The ID of the consent recording to retrieve.

The voice consent recording metadata.

Update consent recording metadata used for creating custom voices. This endpoint updates metadata only and does not replace the underlying audio.

See the custom voices guide. Custom voices are limited to eligible customers.

The ID of the consent recording to update.

The updated label for this consent recording.

The updated voice consent recording metadata.

Delete a consent recording that was uploaded for creating custom voices.

See the custom voices guide. Custom voices are limited to eligible customers.

The ID of the consent recording to delete.

A deletion confirmation.

Transcribes audio into the input language.

The audio file object (not file name) to transcribe, in one of these formats: flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, or webm.

ID of the model to use. The options are gpt-4o-transcribe, gpt-4o-mini-transcribe, whisper-1 (which is powered by our open source Whisper V2 model), and gpt-4o-transcribe-diarize.

Controls how the audio is cut into chunks. When set to "auto", the server first normalizes loudness and then uses voice activity detection (VAD) to choose boundaries. server_vad object can be provided to tweak VAD detection parameters manually. If unset, the audio is transcribed as a single block. Required when using gpt-4o-transcribe-diarize for inputs longer than 30 seconds.

Additional information to include in the transcription response. logprobs will return the log probabilities of the tokens in the response to understand the model's confidence in the transcription. logprobs only works with response_format set to json and only with the models gpt-4o-transcribe and gpt-4o-mini-transcribe. This field is not supported when using gpt-4o-transcribe-diarize.

Optional list of speaker names that correspond to the audio samples provided in known_speaker_references[]. Each entry should be a short identifier (for example customer or agent). Up to 4 speakers are supported.

Optional list of audio samples (as data URLs) that contain known speaker references matching known_speaker_names[]. Each sample must be between 2 and 10 seconds, and can use any of the same input audio formats supported by file.

The language of the input audio. Supplying the input language in ISO-639-1 (e.g. en) format will improve accuracy and latency.

An optional text to guide the model's style or continue a previous audio segment. The prompt should match the audio language. This field is not supported when using gpt-4o-transcribe-diarize.

The format of the output, in one of these options: json, text, srt, verbose_json, vtt, or diarized_json. For gpt-4o-transcribe and gpt-4o-mini-transcribe, the only supported format is json. For gpt-4o-transcribe-diarize, the supported formats are json, text, and diarized_json, with diarized_json required to receive speaker annotations.

If set to true, the model response data will be streamed to the client as it is generated using server-sent events. See the Streaming section of the Speech-to-Text guide for more information.

Note: Streaming is not supported for the whisper-1 model and will be ignored.

The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use log probability to automatically increase the temperature until certain thresholds are hit.

The timestamp granularities to populate for this transcription. response_format must be set verbose_json to use timestamp granularities. Either or both of these options are supported: word, or segment. Note: There is no additional latency for segment timestamps, but generating word timestamps incurs additional latency. This option is not available for gpt-4o-transcribe-diarize.

The transcription object, a diarized transcription object, a verbose transcription object, or a stream of transcript events.

Translates audio into English.

The audio file object (not file name) translate, in one of these formats: flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, or webm.

string or "whisper-1"

ID of the model to use. Only whisper-1 (which is powered by our open source Whisper V2 model) is currently available.

An optional text to guide the model's style or continue a previous audio segment. The prompt should be in English.

The format of the output, in one of these options: json, text, srt, verbose_json, or vtt.

The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use log probability to automatically increase the temperature until certain thresholds are hit.

A custom voice that can be used for audio output.

The Unix timestamp (in seconds) for when the voice was created.

The voice identifier, which can be referenced in API endpoints.

The name of the voice.

The object type, which is always audio.voice.

A consent recording used to authorize creation of a custom voice.

The Unix timestamp (in seconds) for when the consent recording was created.

The consent recording identifier.

The BCP 47 language tag for the consent phrase (for example, en-US).

The label provided when the consent recording was uploaded.

The object type, which is always audio.voice_consent.

The consent recording identifier.

Represents a transcription response returned by model, based on the provided input.

The log probabilities of the tokens in the transcription. Only returned with the models gpt-4o-transcribe and gpt-4o-mini-transcribe if logprobs is added to the include array.

The transcribed text.

Token usage statistics for the request.

Represents a diarized transcription response returned by the model, including the combined transcript and speaker-segment annotations.

Duration of the input audio in seconds.

Segments of the transcript annotated with timestamps and speaker labels.

The type of task that was run. Always transcribe.

The concatenated transcript text for the entire audio input.

Token or duration usage statistics for the request.

Represents a verbose json transcription response returned by model, based on the provided input.

The duration of the input audio.

The language of the input audio.

Segments of the transcribed text and their corresponding details.

The transcribed text.

Usage statistics for models billed by audio input duration.

Extracted words and their corresponding timestamps.

Emitted for each chunk of audio data generated during speech synthesis.

A chunk of Base64-encoded audio data.

The type of the event. Always speech.audio.delta.

Emitted when the speech synthesis is complete and all audio has been streamed.

The type of the event. Always speech.audio.done.

Token usage statistics for the request.

Emitted when there is an additional text delta. This is also the first event emitted when the transcription starts. Only emitted when you create a transcription with the Stream parameter set to true.

The text delta that was additionally transcribed.

The log probabilities of the delta. Only included if you create a transcription with the include[] parameter set to logprobs.

Identifier of the diarized segment that this delta belongs to. Only present when using gpt-4o-transcribe-diarize.

The type of the event. Always transcript.text.delta.

Emitted when a diarized transcription returns a completed segment with speaker information. Only emitted when you create a transcription with stream set to true and response_format set to diarized_json.

End timestamp of the segment in seconds.

Unique identifier for the segment.

Speaker label for this segment.

Start timestamp of the segment in seconds.

Transcript text for this segment.

The type of the event. Always transcript.text.segment.

Emitted when the transcription is complete. Contains the complete transcription text. Only emitted when you create a transcription with the Stream parameter set to true.

The log probabilities of the individual tokens in the transcription. Only included if you create a transcription with the include[] parameter set to logprobs.

The text that was transcribed.

The type of the event. Always transcript.text.done.

Usage statistics for models billed by token usage.

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
4
5
6
7
8
9
curl https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini-tts",
    "input": "The quick brown fox jumped over the lazy dog.",
    "voice": "alloy"
  }' \
  --output speech.mp3
```

Example 2 (bash):
```bash
1
2
3
4
5
6
7
8
9
curl https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini-tts",
    "input": "The quick brown fox jumped over the lazy dog.",
    "voice": "alloy"
  }' \
  --output speech.mp3
```

Example 3 (unknown):
```unknown
1
2
3
4
5
6
7
8
9
```

Example 4 (python):
```python
1
2
3
4
5
6
7
8
9
10
from pathlib import Path
import openai

speech_file_path = Path(__file__).parent / "speech.mp3"
with openai.audio.speech.with_streaming_response.create(
  model="gpt-4o-mini-tts",
  voice="alloy",
  input="The quick brown fox jumped over the lazy dog."
) as response:
  response.stream_to_file(speech_file_path)
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/realtime

**Contents:**
- Realtime
- Create call
    - Request body
    - Returns

Communicate with a multimodal model in real time over low latency interfaces like WebRTC, WebSocket, and SIP. Natively supports speech-to-speech as well as text, image, and audio inputs and outputs.

Learn more about the Realtime API.

Create a new Realtime API call over WebRTC and receive the SDP answer needed to complete the peer connection.

WebRTC Session Description Protocol (SDP) offer generated by the caller.

Optional session configuration to apply before the realtime session is created. Use the same parameters you would send in a create client secret request.

Returns 201 Created with the SDP answer in the response body. The Location response header includes the call ID for follow-up requests, e.g., establishing a monitoring WebSocket or hanging up the call.

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
4
curl -X POST https://api.openai.com/v1/realtime/calls \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F "sdp=<offer.sdp;type=application/sdp" \
  -F 'session={"type":"realtime","model":"gpt-realtime"};type=application/json'
```

Example 2 (bash):
```bash
1
2
3
4
curl -X POST https://api.openai.com/v1/realtime/calls \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F "sdp=<offer.sdp;type=application/sdp" \
  -F 'session={"type":"realtime","model":"gpt-realtime"};type=application/json'
```

Example 3 (unknown):
```unknown
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
v=0
o=- 4227147428 1719357865 IN IP4 127.0.0.1
s=-
c=IN IP4 0.0.0.0
t=0 0
a=group:BUNDLE 0 1
a=msid-semantic:WMS *
a=fingerprint:sha-256 CA:92:52:51:B4:91:3B:34:DD:9C:0B:FB:76:19:7E:3B:F1:21:0F:32:2C:38:01:72:5D:3F:78:C7:5F:8B:C7:36
m=audio 9 UDP/TLS/RTP/SAVPF 111 0 8
a=mid:0
a=ice-ufrag:kZ2qkHXX/u11
a=ice-pwd:uoD16Di5OGx3VbqgA3ymjEQV2kwiOjw6
a=setup:active
a=rtcp-mux
a=rtpmap:111 opus/48000/2
a=candidate:993865896 1 udp 2130706431 4.155.146.196 3478 typ host ufrag kZ2qkHXX/u11
a=candidate:1432411780 1 tcp 1671430143 4.155.146.196 443 typ host tcptype passive ufrag kZ2qkHXX/u11
m=application 9 UDP/DTLS/SCTP webrtc-datachannel
a=mid:1
a=sctp-port:5000
```

Example 4 (json):
```json
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
v=0
o=- 4227147428 1719357865 IN IP4 127.0.0.1
s=-
c=IN IP4 0.0.0.0
t=0 0
a=group:BUNDLE 0 1
a=msid-semantic:WMS *
a=fingerprint:sha-256 CA:92:52:51:B4:91:3B:34:DD:9C:0B:FB:76:19:7E:3B:F1:21:0F:32:2C:38:01:72:5D:3F:78:C7:5F:8B:C7:36
m=audio 9 UDP/TLS/RTP/SAVPF 111 0 8
a=mid:0
a=ice-ufrag:kZ2qkHXX/u11
a=ice-pwd:uoD16Di5OGx3VbqgA3ymjEQV2kwiOjw6
a=setup:active
a=rtcp-mux
a=rtpmap:111 opus/48000/2
a=candidate:993865896 1 udp 2130706431 4.155.146.196 3478 typ host ufrag kZ2qkHXX/u11
a=candidate:1432411780 1 tcp 1671430143 4.155.146.196 443 typ host tcptype passive ufrag kZ2qkHXX/u11
m=application 9 UDP/DTLS/SCTP webrtc-datachannel
a=mid:1
a=sctp-port:5000
```

---

## Realtime API

**URL:** https://platform.openai.com/docs/guides/realtime

**Contents:**
- Realtime API
- Voice agents
- Connection methods
- API Usage
- Beta to GA migration
  - All Items
  - Function Call Output
  - Message

The OpenAI Realtime API enables low-latency communication with models that natively support speech-to-speech interactions as well as multimodal inputs (audio, images, and text) and outputs (audio and text). These APIs can also be used for realtime audio transcription.

One of the most common use cases for the Realtime API is building voice agents for speech-to-speech model interactions in the browser. Our recommended starting point for these types of applications is the Agents SDK for TypeScript, which uses a WebRTC connection to the Realtime model in the browser, and WebSocket when used on the server.

Follow the voice agent quickstart to build Realtime agents in the browser.

To use the Realtime API directly outside the context of voice agents, check out the other connection options below.

While building voice agents with the Agents SDK is the fastest path to one specific type of application, the Realtime API provides an entire suite of flexible tools for a variety of use cases.

There are three primary supported interfaces for the Realtime API:

Ideal for browser and client-side interactions with a Realtime model.

Ideal for middle tier server-side applications with consistent low-latency network connections.

Ideal for VoIP telephony connections.

Depending on how you'd like to connect to a Realtime model, check out one of the connection guides above to get started. You'll learn how to initialize a Realtime session, and how to interact with a Realtime model using client and server events.

Once connected to a realtime model using one of the methods above, learn how to interact with the model in these usage guides.

There are a few key differences between the interfaces in the Realtime beta API and the recently released GA API. Expand the topics below for more information about migrating from the beta interface to GA.

For REST API requests, WebSocket connections, and other interfaces with the Realtime API, beta users had to include the following header with each request:

This header should be removed for requests to the GA interface. To retain the behavior of the beta API, you should continue to include this header.

In the beta interface, there were multiple endpoints for generating ephemeral keys for either Realtime sessions or transcription sessions. In the GA interface, there is only one REST API endpoint used to generate keys - POST /v1/realtime/client_secrets.

To create a session and receive a client secret you can use to initialize a WebRTC or WebSocket connection on a client, you can request one like this using the appropriate session configuration:

These tokens can safely be used in client environments like browsers and mobile applications.

When initializing a WebRTC session in the browser, the URL for obtaining remote session information via SDP is now /v1/realtime/calls:

When creating or updating a Realtime session in the GA interface, you must now specify a session type, since now the same client event is used to create both speech-to-speech and transcription sessions. The options for the session type are:

Configuration for input modalities and other properties have moved as well, notably output audio configuration like model voice. Check the API reference for the latest event shapes.

Finally, some event names have changed to reflect their new position in the event data model:

For response.output_item, the API has always had both .added and .done events, but for conversation level items the API previously only had .created, which by convention is emitted at the start when the item added.

We have added a .added and .done event to allow better ergonomics for developers when receiving events that need some loading time (such as MCP tool listing or input audio transcriptions if these were to be modeled as items in the future).

Current event shape for conversation items added:

New events to replace the above:

Realtime API sets an object=realtime.item param on all items in the GA interface.

status : Realtime now accepts a no-op status field for the function call output item param. This aligns with the Responses API implementation.

Assistant Message Content

The type properties of output assistant messages now align with the Responses API:

**Examples:**

Example 1 (python):
```python
1
2
3
4
5
6
7
8
9
10
11
12
13
import { RealtimeAgent, RealtimeSession } from "@openai/agents/realtime";

const agent = new RealtimeAgent({
    name: "Assistant",
    instructions: "You are a helpful assistant.",
});

const session = new RealtimeSession(agent);

// Automatically connects your microphone and audio output
await session.connect({
    apiKey: "<client-api-key>",
});
```

Example 2 (js):
```js
1
2
3
4
5
6
7
8
9
10
11
12
13
import { RealtimeAgent, RealtimeSession } from "@openai/agents/realtime";

const agent = new RealtimeAgent({
    name: "Assistant",
    instructions: "You are a helpful assistant.",
});

const session = new RealtimeSession(agent);

// Automatically connects your microphone and audio output
await session.connect({
    apiKey: "<client-api-key>",
});
```

Example 3 (unknown):
```unknown
1
2
3
4
5
6
7
8
9
10
11
12
13
```

Example 4 (unknown):
```unknown
OpenAI-Beta: realtime=v1
```

---

## Text to speech

**URL:** https://platform.openai.com/docs/guides/text-to-speech

**Contents:**
- Text to speech
- Quickstart
  - Text-to-speech models
  - Voice options
  - Streaming realtime audio
- Supported output formats
- Supported languages
- Custom voices
    - Creating a voice
    - Using a voice during speech generation

The Audio API provides a speech endpoint based on our GPT-4o mini TTS (text-to-speech) model. It comes with 11 built-in voices and can be used to:

Here's an example of the alloy voice:

Our usage policies require you to provide a clear disclosure to end users that the TTS voice they are hearing is AI-generated and not a human voice.

The speech endpoint takes three key inputs:

Here's a simple request example:

By default, the endpoint outputs an MP3 of the spoken audio, but you can configure it to output any supported format.

For intelligent realtime applications, use the gpt-4o-mini-tts model, our newest and most reliable text-to-speech model. You can prompt the model to control aspects of speech, including:

Our other text-to-speech models are tts-1 and tts-1-hd. The tts-1 model provides lower latency, but at a lower quality than the tts-1-hd model.

The TTS endpoint provides 11 built‑in voices to control how speech is rendered from text. Hear and play with these voices in OpenAI.fm, our interactive demo for trying the latest text-to-speech model in the OpenAI API. Voices are currently optimized for English.

If you're using the Realtime API, note that the set of available voices is slightly different—see the realtime conversations guide for current realtime voices.

The Speech API provides support for realtime audio streaming using chunk transfer encoding. This means the audio can be played before the full file is generated and made accessible.

For the fastest response times, we recommend using wav or pcm as the response format.

The default response format is mp3, but other formats like opus and wav are available.

The TTS model generally follows the Whisper model in terms of language support. Whisper supports the following languages and performs well, despite voices being optimized for English:

Afrikaans, Arabic, Armenian, Azerbaijani, Belarusian, Bosnian, Bulgarian, Catalan, Chinese, Croatian, Czech, Danish, Dutch, English, Estonian, Finnish, French, Galician, German, Greek, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, Italian, Japanese, Kannada, Kazakh, Korean, Latvian, Lithuanian, Macedonian, Malay, Marathi, Maori, Nepali, Norwegian, Persian, Polish, Portuguese, Romanian, Russian, Serbian, Slovak, Slovenian, Spanish, Swahili, Swedish, Tagalog, Tamil, Thai, Turkish, Ukrainian, Urdu, Vietnamese, and Welsh.

You can generate spoken audio in these languages by providing input text in the language of your choice.

Custom voices enable you to create a unique voice for your agent or application. These voices can be used for audio output with the Text to Speech API, the Realtime API, or the Chat Completions API with audio output.

To create a custom voice, you’ll provide a short sample audio reference that the model will seek to replicate.

Custom voices are limited to eligible customers. Contact sales at sales@openai.com to learn more. Once enabled for your organization, you’ll have access to the Voices tab under Audio.

Currently, voices must be created through an API request. See the API reference for the full set of API operations.

Creating a voice requires two separate audio recordings:

Tips for creating a high-quality voice

The quality of your custom voice is highly dependent on the quality of the sample you provide. Optimizing the recording quality can make a big difference.

Requirements and limitations

Refer to the Text-to-Speech Supplemental Agreement for additional terms of use.

Creating a voice consent

The consent audio recording must only include one of the following phrases. Any divergence from the script will lead to a failure.

Then upload the recording via the API. A successful upload will return the consent recording ID that you’ll reference later. Note the consent can be used for multiple different voice creations if the same voice actor is making multiple attempts.

Next, you’ll create the actual voice by referencing the consent recording ID, and providing the voice sample.

If successful, the created voice will be listed under the Audio tab.

Speech generation will work as usual. Simply specify the ID of the voice in the voice parameter when creating speech, or when initiating a realtime session.

Text to speech example

**Examples:**

Example 1 (python):
```python
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
import fs from "fs";
import path from "path";
import OpenAI from "openai";

const openai = new OpenAI();
const speechFile = path.resolve("./speech.mp3");

const mp3 = await openai.audio.speech.create({
  model: "gpt-4o-mini-tts",
  voice: "coral",
  input: "Today is a wonderful day to build something people love!",
  instructions: "Speak in a cheerful and positive tone.",
});

const buffer = Buffer.from(await mp3.arrayBuffer());
await fs.promises.writeFile(speechFile, buffer);
```

Example 2 (javascript):
```javascript
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
import fs from "fs";
import path from "path";
import OpenAI from "openai";

const openai = new OpenAI();
const speechFile = path.resolve("./speech.mp3");

const mp3 = await openai.audio.speech.create({
  model: "gpt-4o-mini-tts",
  voice: "coral",
  input: "Today is a wonderful day to build something people love!",
  instructions: "Speak in a cheerful and positive tone.",
});

const buffer = Buffer.from(await mp3.arrayBuffer());
await fs.promises.writeFile(speechFile, buffer);
```

Example 3 (unknown):
```unknown
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
```

Example 4 (python):
```python
1
2
3
4
5
6
7
8
9
10
11
12
13
from pathlib import Path
from openai import OpenAI

client = OpenAI()
speech_file_path = Path(__file__).parent / "speech.mp3"

with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="coral",
    input="Today is a wonderful day to build something people love!",
    instructions="Speak in a cheerful and positive tone.",
) as response:
    response.stream_to_file(speech_file_path)
```

---

## Realtime conversations

**URL:** https://platform.openai.com/docs/guides/realtime-conversations

**Contents:**
- Realtime conversations
- Realtime speech-to-speech sessions
- Session lifecycle events
- Text inputs and outputs
- Audio inputs and outputs
  - Voice options
  - Handling audio with WebRTC
  - Client and server events for audio in WebRTC
  - Handling audio with WebSockets
  - Streaming audio input to the server

Once you have connected to the Realtime API through either WebRTC or WebSocket, you can call a Realtime model (such as gpt-realtime) to have speech-to-speech conversations. Doing so will require you to send client events to initiate actions, and listen for server events to respond to actions taken by the Realtime API.

This guide will walk through the event flows required to use model capabilities like audio and text generation and function calling, and how to think about the state of a Realtime Session.

If you do not need to have a conversation with the model, meaning you don't expect any response, you can use the Realtime API in transcription mode.

A Realtime Session is a stateful interaction between the model and a connected client. The key components of the session are:

Input audio buffer and WebSockets

If you are using WebRTC, much of the media handling required to send and receive audio from the model is assisted by WebRTC APIs.

If you are using WebSockets for audio, you will need to manually interact with the input audio buffer by sending audio to the server, sent with JSON events with base64-encoded audio.

All these components together make up a Realtime Session. You will use client events to update the state of the session, and listen for server events to react to state changes within the session.

After initiating a session via either WebRTC or WebSockets, the server will send a session.created event indicating the session is ready. On the client, you can update the current session configuration with the session.update event. Most session properties can be updated at any time, except for the voice the model uses for audio output, after the model has responded with audio once during the session. The maximum duration of a Realtime session is 60 minutes.

The following example shows updating the session with a session.update client event. See the WebRTC or WebSocket guide for more on sending client events over these channels.

When the session has been updated, the server will emit a session.updated event with the new state of the session.

To generate text with a Realtime model, you can add text inputs to the current conversation, ask the model to generate a response, and listen for server-sent events indicating the progress of the model's response. In order to generate text, the session must be configured with the text modality (this is true by default).

Create a new text conversation item using the conversation.item.create client event. This is similar to sending a user message (prompt) in Chat Completions in the REST API.

After adding the user message to the conversation, send the response.create event to initiate a response from the model. If both audio and text are enabled for the current session, the model will respond with both audio and text content. If you'd like to generate text only, you can specify that when sending the response.create client event, as shown below.

When the response is completely finished, the server will emit the response.done event. This event will contain the full text generated by the model, as shown below.

While the model response is being generated, the server will emit a number of lifecycle events during the process. You can listen for these events, such as response.output_text.delta, to provide realtime feedback to users as the response is generated. A full listing of the events emitted by there server are found below under related server events. They are provided in the rough order of when they are emitted, along with relevant client-side events for text generation.

conversation.item.create

conversation.item.added

conversation.item.done

response.output_item.added

response.content_part.added

response.output_text.delta

response.output_text.done

response.content_part.done

response.output_item.done

One of the most powerful features of the Realtime API is voice-to-voice interaction with the model, without an intermediate text-to-speech or speech-to-text step. This enables lower latency for voice interfaces, and gives the model more data to work with around the tone and inflection of voice input.

Realtime sessions can be configured to use one of several built‑in voices when producing audio output. You can set the voice on session creation (or on a response.create) to control how the model sounds. Current voice options are alloy, ash, ballad, coral, echo, sage, shimmer, and verse. Once the model has emitted audio in a session, the voice cannot be modified for that session.

If you are connecting to the Realtime API using WebRTC, the Realtime API is acting as a peer connection to your client. Audio output from the model is delivered to your client as a remote media stream. Audio input to the model is collected using audio devices (getUserMedia), and media streams are added as tracks to to the peer connection.

The example code from the WebRTC connection guide shows a basic example of configuring both local and remote audio using browser APIs:

The snippet above enables simple interaction with the Realtime API, but there's much more that can be done. For more examples of different kinds of user interfaces, check out the WebRTC samples repository. Live demos of these samples can also be found here.

Using media captures and streams in the browser enables you to do things like mute and unmute microphones, select which device to collect input from, and more.

By default, WebRTC clients don't need to send any client events to the Realtime API before sending audio inputs. Once a local audio track is added to the peer connection, your users can just start talking!

However, WebRTC clients still receive a number of server-sent lifecycle events as audio is moving back and forth between client and server over the peer connection. Examples include:

Manipulating WebRTC APIs for media streams may give you all the control you need. However, it may occasionally be necessary to use lower-level interfaces for audio input and output. Refer to the WebSockets section below for more information and a listing of events required for granular audio input handling.

When sending and receiving audio over a WebSocket, you will have a bit more work to do in order to send media from the client, and receive media from the server. Below, you'll find a table describing the flow of events during a WebSocket session that are necessary to send and receive audio over the WebSocket.

The events below are given in lifecycle order, though some events (like the delta events) may happen concurrently.

conversation.item.create

(send whole audio message)

input_audio_buffer.append

(stream audio in chunks)

input_audio_buffer.commit

(used when VAD is disabled)

(used when VAD is disabled)

input_audio_buffer.speech_started

input_audio_buffer.speech_stopped

input_audio_buffer.committed

input_audio_buffer.clear

(used when VAD is disabled)

conversation.item.added

conversation.item.done

response.output_item.created

response.content_part.added

response.output_audio.delta

response.output_audio.done

response.output_audio_transcript.delta

response.output_audio_transcript.done

response.output_text.delta

response.output_text.done

response.content_part.done

response.output_item.done

To stream audio input to the server, you can use the input_audio_buffer.append client event. This event requires you to send chunks of Base64-encoded audio bytes to the Realtime API over the socket. Each chunk cannot exceed 15 MB in size.

The format of the input chunks can be configured either for the entire session, or per response.

It is also possible to create conversation messages that are full audio recordings. Use the conversation.item.create client event to create messages with input_audio content.

To play output audio back on a client device like a web browser, we recommend using WebRTC rather than WebSockets. WebRTC will be more robust sending media to client devices over uncertain network conditions.

But to work with audio output in server-to-server applications using a WebSocket, you will need to listen for response.output_audio.delta events containing the Base64-encoded chunks of audio data from the model. You will either need to buffer these chunks and write them out to a file, or maybe immediately stream them to another source like a phone call with Twilio.

Note that the response.output_audio.done and response.done events won't actually contain audio data in them - just audio content transcriptions. To get the actual bytes, you'll need to listen for the response.output_audio.delta events.

The format of the output chunks can be configured either for the entire session, or per response.

By default, Realtime sessions have voice activity detection (VAD) enabled, which means the API will determine when the user has started or stopped speaking and respond automatically.

Read more about how to configure VAD in our voice activity detection guide.

VAD can be disabled by setting turn_detection to null with the session.update client event. This can be useful for interfaces where you would like to take granular control over audio input, like push to talk interfaces.

When VAD is disabled, the client will have to manually emit some additional client events to trigger audio responses:

If you would like to keep VAD mode enabled, but would just like to retain the ability to manually decide when a response is generated, you can set turn_detection.interrupt_response and turn_detection.create_response to false with the session.update client event. This will retain all the behavior of VAD but not automatically create new Responses. Clients can trigger these manually with a response.create event.

This can be useful for moderation or input validation or RAG patterns, where you're comfortable trading a bit more latency in the interaction for control over inputs.

By default, all responses generated during a session are added to the session's conversation state (the "default conversation"). However, you may want to generate model responses outside the context of the session's default conversation, or have multiple responses generated concurrently. You might also want to have more granular control over which conversation items are considered while the model generates a response (e.g. only the last N number of turns).

Generating "out-of-band" responses which are not added to the default conversation state is possible by setting the response.conversation field to the string none when creating a response with the response.create client event.

When creating an out-of-band response, you will probably also want some way to identify which server-sent events pertain to this response. You can provide metadata for your model response that will help you identify which response is being generated for this client-sent event.

Now, when you listen for the response.done server event, you can identify the result of your out-of-band response.

You can also construct a custom context that the model will use to generate a response, outside the default/current conversation. This can be done using the input array on a response.create client event. You can use new inputs, or reference existing input items in the conversation by ID.

You can also insert responses into the default conversation, ignoring all other instructions and context. Do this by setting input to an empty array.

The Realtime models also support function calling, which enables you to execute custom code to extend the capabilities of the model. Here's how it works at a high level:

Let's see how this would work in practice by adding a callable function that will provide today's horoscope to users of the model. We'll show the shape of the client event objects that need to be sent, and what the server will emit in turn.

First, we must give the model a selection of functions it can call based on user input. Available functions can be configured either at the session level, or the individual response level.

Here's an example client event payload for a session.update that configures a horoscope generation function, that takes a single argument (the astrological sign for which the horoscope should be generated):

The description fields for the function and the parameters help the model choose whether or not to call the function, and what data to include in each parameter. If the model receives input that indicates the user wants their horoscope, it will call this function with a sign parameter.

Based on inputs to the model, the model may decide to call a function in order to generate the best response. Let's say our application adds the following conversation item with a conversation.item.create event and then creates a response:

Followed by a response.create client event to generate a response:

Instead of immediately returning a text or audio response, the model will instead generate a response that contains the arguments that should be passed to a function in the developer's application. You can listen for realtime updates to function call arguments using the response.function_call_arguments.delta server event, but response.done will also have the complete data we need to call our function.

In the JSON emitted by the server, we can detect that the model wants to call a custom function:

Given this information, we can execute code in our application to generate the horoscope, and then provide that information back to the model so it can generate a response.

Upon receiving a response from the model with arguments to a function call, your application can execute code that satisfies the function call. This could be anything you want, like talking to external APIs or accessing databases.

Once you are ready to give the model the results of your custom code, you can create a new conversation item containing the result via the conversation.item.create client event.

Once we have added the conversation item containing our function call results, we again emit the response.create event from the client. This will trigger a model response using the data from the function call.

The error event is emitted by the server whenever an error condition is encountered on the server during the session. Occasionally, these errors can be traced to a client event that was emitted by your application.

Unlike HTTP requests and responses, where a response is implicitly tied to a request from the client, we need to use an event_id property on client events to know when one of them has triggered an error condition on the server. This technique is shown in the code below, where the client attempts to emit an unsupported event type.

This unsuccessful event sent from the client will emit an error event like the following:

In many voice applications the user can interrupt the model while it's speaking. Realtime API handles interruptions when VAD is enabled, in that it detects user speech, cancels the ongoing response, and starts a new one. However in this scenario you will want the model to know where it was interrupted, so it can continue the conversation naturally (for example if the user says "what was that last thing?"). We call this truncating the model's last response, i.e. removing the unplayed portion of the model's last response from the conversation.

In WebRTC and SIP connections the server manages a buffer of output audio, and thus knows how much audio has been played at a given moment. The server will automatically truncate unplayed audio when there's a user interruption.

With a WebSocket connection the client manages audio playback, and thus must stop playback and handle truncation. Here's how this procedure works:

What about truncating the transcript as well? The realtime model doesn't have enough information to precisely align transcript and audio, and thus conversation.item.truncate will cut the audio at a given place and remove the text transcript for the unplayed portion. This solves the problem of removing unplayed audio but doesn't provide a truncated transcript.

Realtime API defaults to using voice activity detection (VAD), which means model responses will be triggered with audio input. You can also do a push-to-talk interaction by disabling VAD and using an application-level gate to control when audio input is sent to the model, for example holding the space-bar down to capture audio, then triggering a response when it's released. For some apps this works surprisingly well -- it gives the users control over interactions, avoids VAD failures, and it feels snappy because we're not waiting for a VAD timeout.

Implementing push-to-talk looks a bit different on WebSockets and WebRTC. In a Realtime API WebSocket connection all events are sent in the same channel and with the same ordering, while a WebRTC connection has separate channels for audio and control events.

To implement push-to-talk with a WebSocket connection, you'll want the client to stop audio playback, handle interruptions, and kick off a new response. Here's a more detailed procedure:

Implementing push-to-talk with WebRTC is similar but the input audio buffer must be explicitly cleared. Here's a procedure:

**Examples:**

Example 1 (javascript):
```javascript
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
const event = {
  type: "session.update",
  session: {
      type: "realtime",
      model: "gpt-realtime",
      // Lock the output to audio (set to ["text"] if you want text without audio)
      output_modalities: ["audio"],
      audio: {
        input: {
          format: {
            type: "audio/pcm",
            rate: 24000,
          },
          turn_detection: {
            type: "semantic_vad"
          }
        },
        output: {
          format: {
            type: "audio/pcm",
          },
          voice: "marin",
        }
      },
      // Use a server-stored prompt by ID. Optionally pin a version and pass variables.
      prompt: {
        id: "pmpt_123",          // your stored prompt ID
        version: "89",           // optional: pin a specific version
        variables: {
          city: "Paris"          // example variable used by your prompt
        }
      },
      // You can still set direct session fields; these override prompt fields if they overlap:
      instructions: "Speak clearly and briefly. Confirm understanding before taking actions."
  },
};

// WebRTC data channel and WebSocket both have .send()
dataChannel.send(JSON.stringify(event));
```

Example 2 (javascript):
```javascript
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
const event = {
  type: "session.update",
  session: {
      type: "realtime",
      model: "gpt-realtime",
      // Lock the output to audio (set to ["text"] if you want text without audio)
      output_modalities: ["audio"],
      audio: {
        input: {
          format: {
            type: "audio/pcm",
            rate: 24000,
          },
          turn_detection: {
            type: "semantic_vad"
          }
        },
        output: {
          format: {
            type: "audio/pcm",
          },
          voice: "marin",
        }
      },
      // Use a server-stored prompt by ID. Optionally pin a version and pass variables.
      prompt: {
        id: "pmpt_123",          // your stored prompt ID
        version: "89",           // optional: pin a specific version
        variables: {
          city: "Paris"          // example variable used by your prompt
        }
      },
      // You can still set direct session fields; these override prompt fields if they overlap:
      instructions: "Speak clearly and briefly. Confirm understanding before taking actions."
  },
};

// WebRTC data channel and WebSocket both have .send()
dataChannel.send(JSON.stringify(event));
```

Example 3 (unknown):
```unknown
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
```

Example 4 (unknown):
```unknown
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
event = {
    "type": "session.update",
    session: {
      type: "realtime",
      model: "gpt-realtime",
      # Lock the output to audio (add "text" if you also want text)
      output_modalities: ["audio"],
      audio: {
        input: {
          format: {
            type: "audio/pcm",
            rate: 24000,
          },
          turn_detection: {
            type: "semantic_vad"
          }
        },
        output: {
          format: {
            type: "audio/pcmu",
          },
          voice: "marin",
        }
      },
      # Use a server-stored prompt by ID. Optionally pin a version and pass variables.
      prompt: {
        id: "pmpt_123",          // your stored prompt ID
        version: "89",           // optional: pin a specific version
        variables: {
          city: "Paris"          // example variable used by your prompt
        }
      },
      # You can still set direct session fields; these override prompt fields if they overlap:
      instructions: "Speak clearly and briefly. Confirm understanding before taking actions."
    }
}
ws.send(json.dumps(event))
```

---

## 

**URL:** https://platform.openai.com/docs/api-reference/audio

**Contents:**
- Audio
- Create speech
    - Request body
    - Returns
- Create voice
    - Request body
    - Returns
- Create voice consent
    - Request body
    - Returns

Learn how to turn audio into text or text into audio.

Related guide: Speech to text

Generates audio from the input text.

The text to generate audio for. The maximum length is 4096 characters.

One of the available TTS models: tts-1, tts-1-hd or gpt-4o-mini-tts.

The voice to use when generating the audio. Supported voices are alloy, ash, ballad, coral, echo, fable, onyx, nova, sage, shimmer, and verse. Previews of the voices are available in the Text to speech guide.

Control the voice of your generated audio with additional instructions. Does not work with tts-1 or tts-1-hd.

The format to audio in. Supported formats are mp3, opus, aac, flac, wav, and pcm.

The speed of the generated audio. Select a value from 0.25 to 4.0. 1.0 is the default.

The format to stream the audio in. Supported formats are sse and audio. sse is not supported for tts-1 or tts-1-hd.

The audio file content or a stream of audio events.

Create a custom voice you can use for audio output (for example, in Text-to-Speech and the Realtime API). This requires an audio sample and a previously uploaded consent recording.

See the custom voices guide for requirements and best practices. Custom voices are limited to eligible customers.

The sample audio recording file. Maximum size is 10 MiB.

Supported MIME types: audio/mpeg, audio/wav, audio/x-wav, audio/ogg, audio/aac, audio/flac, audio/webm, audio/mp4.

The consent recording ID (for example, cons_1234).

The name of the new voice.

Upload a consent recording that authorizes creation of a custom voice.

See the custom voices guide for requirements and best practices. Custom voices are limited to eligible customers.

The BCP 47 language tag for the consent phrase (for example, en-US).

The label to use for this consent recording.

The consent audio recording file. Maximum size is 10 MiB.

Supported MIME types: audio/mpeg, audio/wav, audio/x-wav, audio/ogg, audio/aac, audio/flac, audio/webm, audio/mp4.

The created voice consent recording metadata.

List consent recordings available to your organization for creating custom voices.

See the custom voices guide. Custom voices are limited to eligible customers.

A cursor for use in pagination. after is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include after=obj_foo in order to fetch the next page of the list.

A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20.

A paginated list of voice consent recordings.

Retrieve consent recording metadata used for creating custom voices.

See the custom voices guide. Custom voices are limited to eligible customers.

The ID of the consent recording to retrieve.

The voice consent recording metadata.

Update consent recording metadata used for creating custom voices. This endpoint updates metadata only and does not replace the underlying audio.

See the custom voices guide. Custom voices are limited to eligible customers.

The ID of the consent recording to update.

The updated label for this consent recording.

The updated voice consent recording metadata.

Delete a consent recording that was uploaded for creating custom voices.

See the custom voices guide. Custom voices are limited to eligible customers.

The ID of the consent recording to delete.

A deletion confirmation.

Transcribes audio into the input language.

The audio file object (not file name) to transcribe, in one of these formats: flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, or webm.

ID of the model to use. The options are gpt-4o-transcribe, gpt-4o-mini-transcribe, whisper-1 (which is powered by our open source Whisper V2 model), and gpt-4o-transcribe-diarize.

Controls how the audio is cut into chunks. When set to "auto", the server first normalizes loudness and then uses voice activity detection (VAD) to choose boundaries. server_vad object can be provided to tweak VAD detection parameters manually. If unset, the audio is transcribed as a single block. Required when using gpt-4o-transcribe-diarize for inputs longer than 30 seconds.

Additional information to include in the transcription response. logprobs will return the log probabilities of the tokens in the response to understand the model's confidence in the transcription. logprobs only works with response_format set to json and only with the models gpt-4o-transcribe and gpt-4o-mini-transcribe. This field is not supported when using gpt-4o-transcribe-diarize.

Optional list of speaker names that correspond to the audio samples provided in known_speaker_references[]. Each entry should be a short identifier (for example customer or agent). Up to 4 speakers are supported.

Optional list of audio samples (as data URLs) that contain known speaker references matching known_speaker_names[]. Each sample must be between 2 and 10 seconds, and can use any of the same input audio formats supported by file.

The language of the input audio. Supplying the input language in ISO-639-1 (e.g. en) format will improve accuracy and latency.

An optional text to guide the model's style or continue a previous audio segment. The prompt should match the audio language. This field is not supported when using gpt-4o-transcribe-diarize.

The format of the output, in one of these options: json, text, srt, verbose_json, vtt, or diarized_json. For gpt-4o-transcribe and gpt-4o-mini-transcribe, the only supported format is json. For gpt-4o-transcribe-diarize, the supported formats are json, text, and diarized_json, with diarized_json required to receive speaker annotations.

If set to true, the model response data will be streamed to the client as it is generated using server-sent events. See the Streaming section of the Speech-to-Text guide for more information.

Note: Streaming is not supported for the whisper-1 model and will be ignored.

The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use log probability to automatically increase the temperature until certain thresholds are hit.

The timestamp granularities to populate for this transcription. response_format must be set verbose_json to use timestamp granularities. Either or both of these options are supported: word, or segment. Note: There is no additional latency for segment timestamps, but generating word timestamps incurs additional latency. This option is not available for gpt-4o-transcribe-diarize.

The transcription object, a diarized transcription object, a verbose transcription object, or a stream of transcript events.

Translates audio into English.

The audio file object (not file name) translate, in one of these formats: flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, or webm.

string or "whisper-1"

ID of the model to use. Only whisper-1 (which is powered by our open source Whisper V2 model) is currently available.

An optional text to guide the model's style or continue a previous audio segment. The prompt should be in English.

The format of the output, in one of these options: json, text, srt, verbose_json, or vtt.

The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use log probability to automatically increase the temperature until certain thresholds are hit.

A custom voice that can be used for audio output.

The Unix timestamp (in seconds) for when the voice was created.

The voice identifier, which can be referenced in API endpoints.

The name of the voice.

The object type, which is always audio.voice.

A consent recording used to authorize creation of a custom voice.

The Unix timestamp (in seconds) for when the consent recording was created.

The consent recording identifier.

The BCP 47 language tag for the consent phrase (for example, en-US).

The label provided when the consent recording was uploaded.

The object type, which is always audio.voice_consent.

The consent recording identifier.

Represents a transcription response returned by model, based on the provided input.

The log probabilities of the tokens in the transcription. Only returned with the models gpt-4o-transcribe and gpt-4o-mini-transcribe if logprobs is added to the include array.

The transcribed text.

Token usage statistics for the request.

Represents a diarized transcription response returned by the model, including the combined transcript and speaker-segment annotations.

Duration of the input audio in seconds.

Segments of the transcript annotated with timestamps and speaker labels.

The type of task that was run. Always transcribe.

The concatenated transcript text for the entire audio input.

Token or duration usage statistics for the request.

Represents a verbose json transcription response returned by model, based on the provided input.

The duration of the input audio.

The language of the input audio.

Segments of the transcribed text and their corresponding details.

The transcribed text.

Usage statistics for models billed by audio input duration.

Extracted words and their corresponding timestamps.

Emitted for each chunk of audio data generated during speech synthesis.

A chunk of Base64-encoded audio data.

The type of the event. Always speech.audio.delta.

Emitted when the speech synthesis is complete and all audio has been streamed.

The type of the event. Always speech.audio.done.

Token usage statistics for the request.

Emitted when there is an additional text delta. This is also the first event emitted when the transcription starts. Only emitted when you create a transcription with the Stream parameter set to true.

The text delta that was additionally transcribed.

The log probabilities of the delta. Only included if you create a transcription with the include[] parameter set to logprobs.

Identifier of the diarized segment that this delta belongs to. Only present when using gpt-4o-transcribe-diarize.

The type of the event. Always transcript.text.delta.

Emitted when a diarized transcription returns a completed segment with speaker information. Only emitted when you create a transcription with stream set to true and response_format set to diarized_json.

End timestamp of the segment in seconds.

Unique identifier for the segment.

Speaker label for this segment.

Start timestamp of the segment in seconds.

Transcript text for this segment.

The type of the event. Always transcript.text.segment.

Emitted when the transcription is complete. Contains the complete transcription text. Only emitted when you create a transcription with the Stream parameter set to true.

The log probabilities of the individual tokens in the transcription. Only included if you create a transcription with the include[] parameter set to logprobs.

The text that was transcribed.

The type of the event. Always transcript.text.done.

Usage statistics for models billed by token usage.

**Examples:**

Example 1 (unknown):
```unknown
1
2
3
4
5
6
7
8
9
curl https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini-tts",
    "input": "The quick brown fox jumped over the lazy dog.",
    "voice": "alloy"
  }' \
  --output speech.mp3
```

Example 2 (bash):
```bash
1
2
3
4
5
6
7
8
9
curl https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini-tts",
    "input": "The quick brown fox jumped over the lazy dog.",
    "voice": "alloy"
  }' \
  --output speech.mp3
```

Example 3 (unknown):
```unknown
1
2
3
4
5
6
7
8
9
```

Example 4 (python):
```python
1
2
3
4
5
6
7
8
9
10
from pathlib import Path
import openai

speech_file_path = Path(__file__).parent / "speech.mp3"
with openai.audio.speech.with_streaming_response.create(
  model="gpt-4o-mini-tts",
  voice="alloy",
  input="The quick brown fox jumped over the lazy dog."
) as response:
  response.stream_to_file(speech_file_path)
```

---

## Speech to text

**URL:** https://platform.openai.com/docs/guides/speech-to-text

**Contents:**
- Speech to text
- Quickstart
  - Transcriptions
  - Speaker diarization
  - Translations
- Supported languages
- Timestamps
- Longer inputs
- Prompting
- Streaming transcriptions

The Audio API provides two speech to text endpoints:

Historically, both endpoints have been backed by our open source Whisper model (whisper-1). The transcriptions endpoint now also supports higher quality model snapshots, with limited parameter support:

All endpoints can be used to:

File uploads are currently limited to 25 MB, and the following input file types are supported: mp3, mp4, mpeg, mpga, m4a, wav, and webm. Known speaker reference clips for diarization accept the same formats when provided as data URLs.

The transcriptions API takes as input the audio file you want to transcribe and the desired output file format for the transcription of the audio. All models support the same set of input formats. On output:

By default, the response type will be json with the raw text included.

The Audio API also allows you to set additional parameters in a request. For example, if you want to set the response_format as text, your request would look like the following:

The API Reference includes the full list of available parameters.

gpt-4o-transcribe and gpt-4o-mini-transcribe support json or text responses and allow prompts and logprobs. gpt-4o-transcribe-diarize adds speaker labels but requires chunking_strategy when your audio is longer than 30 seconds ("auto" is recommended) and does not support prompts, logprobs, or timestamp_granularities[].

gpt-4o-transcribe-diarize produces speaker-aware transcripts. Request the diarized_json response format to receive an array of segments with speaker, start, and end metadata. Set chunking_strategy (either "auto" or a Voice Activity Detection configuration) so that the service can split the audio into segments; this is required when the input is longer than 30 seconds.

You can optionally supply up to four short audio references with known_speaker_names[] and known_speaker_references[] to map segments onto known speakers. Provide reference clips between 2–10 seconds in any input format supported by the main audio upload; encode them as data URLs when using multipart form data.

When stream=true, diarized responses emit transcript.text.segment events whenever a segment completes. transcript.text.delta events include a segment_id field, but diarized deltas do not stream partial speaker assignments until each segment is finalized.

gpt-4o-transcribe-diarize is currently available via /v1/audio/transcriptions only and is not yet supported in the Realtime API.

The translations API takes as input the audio file in any of the supported languages and transcribes, if necessary, the audio into English. This differs from our /Transcriptions endpoint since the output is not in the original input language and is instead translated to English text. This endpoint supports only the whisper-1 model.

In this case, the inputted audio was german and the outputted text looks like:

We only support translation into English at this time.

We currently support the following languages through both the transcriptions and translations endpoint:

Afrikaans, Arabic, Armenian, Azerbaijani, Belarusian, Bosnian, Bulgarian, Catalan, Chinese, Croatian, Czech, Danish, Dutch, English, Estonian, Finnish, French, Galician, German, Greek, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, Italian, Japanese, Kannada, Kazakh, Korean, Latvian, Lithuanian, Macedonian, Malay, Marathi, Maori, Nepali, Norwegian, Persian, Polish, Portuguese, Romanian, Russian, Serbian, Slovak, Slovenian, Spanish, Swahili, Swedish, Tagalog, Tamil, Thai, Turkish, Ukrainian, Urdu, Vietnamese, and Welsh.

While the underlying model was trained on 98 languages, we only list the languages that exceeded <50% word error rate (WER) which is an industry standard benchmark for speech to text model accuracy. The model will return results for languages not listed above but the quality will be low.

We support some ISO 639-1 and 639-3 language codes for GPT-4o based models. For language codes we don’t have, try prompting for specific languages (i.e., “Output in English”).

By default, the Transcriptions API will output a transcript of the provided audio in text. The timestamp_granularities[] parameter enables a more structured and timestamped json output format, with timestamps at the segment, word level, or both. This enables word-level precision for transcripts and video edits, which allows for the removal of specific frames tied to individual words.

The timestamp_granularities[] parameter is only supported for whisper-1.

By default, the Transcriptions API only supports files that are less than 25 MB. If you have an audio file that is longer than that, you will need to break it up into chunks of 25 MB's or less or used a compressed audio format. To get the best performance, we suggest that you avoid breaking the audio up mid-sentence as this may cause some context to be lost.

One way to handle this is to use the PyDub open source Python package to split the audio:

OpenAI makes no guarantees about the usability or security of 3rd party software like PyDub.

You can use a prompt to improve the quality of the transcripts generated by the Transcriptions API.

For gpt-4o-transcribe and gpt-4o-mini-transcribe, you can use the prompt parameter to improve the quality of the transcription by giving the model additional context similarly to how you would prompt other GPT-4o models. Prompting is not currently available for gpt-4o-transcribe-diarize.

Here are some examples of how prompting can help in different scenarios:

For whisper-1, the model tries to match the style of the prompt, so it's more likely to use capitalization and punctuation if the prompt does too. However, the current prompting system is more limited than our other language models and provides limited control over the generated text.

You can find more examples on improving your whisper-1 transcriptions in the improving reliability section.

There are two ways you can stream your transcription depending on your use case and whether you are trying to transcribe an already completed audio recording or handle an ongoing stream of audio and use OpenAI for turn detection.

If you have an already completed audio recording, either because it's an audio file or you are using your own turn detection (like push-to-talk), you can use our Transcription API with stream=True to receive a stream of transcript events as soon as the model is done transcribing that part of the audio.

You will receive a stream of transcript.text.delta events as soon as the model is done transcribing that part of the audio, followed by a transcript.text.done event when the transcription is complete that includes the full transcript. When using response_format="diarized_json", the stream also emits transcript.text.segment events with speaker labels each time a segment is finalized.

Additionally, you can use the include[] parameter to include logprobs in the response to get the log probabilities of the tokens in the transcription. These can be helpful to determine how confident the model is in the transcription of that particular part of the transcript.

Streamed transcription is not supported in whisper-1.

In the Realtime API, you can stream the transcription of an ongoing audio recording. To start a streaming session with the Realtime API, create a WebSocket connection with the following URL:

Below is an example payload for setting up a transcription session:

To stream audio data to the API, append audio buffers:

When in VAD mode, the API will respond with input_audio_buffer.committed every time a chunk of speech has been detected. Use input_audio_buffer.committed.item_id and input_audio_buffer.committed.previous_item_id to enforce the ordering.

The API responds with transcription events indicating speech start, stop, and completed transcriptions.

The primary resource used by the streaming ASR API is the TranscriptionSession:

Authenticate directly through the WebSocket connection using your API key or an ephemeral token obtained from:

This endpoint returns an ephemeral token (client_secret) to securely authenticate WebSocket connections.

One of the most common challenges faced when using Whisper is the model often does not recognize uncommon words or acronyms. Here are some different techniques to improve the reliability of Whisper in these cases:

The first method involves using the optional prompt parameter to pass a dictionary of the correct spellings.

Because it wasn't trained with instruction-following techniques, Whisper operates more like a base GPT model. Keep in mind that Whisper only considers the first 224 tokens of the prompt.

While it increases reliability, this technique is limited to 224 tokens, so your list of SKUs needs to be relatively small for this to be a scalable solution.

The second method involves a post-processing step using GPT-4 or GPT-3.5-Turbo.

We start by providing instructions for GPT-4 through the system_prompt variable. Similar to what we did with the prompt parameter earlier, we can define our company and product names.

If you try this on your own audio file, you'll see that GPT-4 corrects many misspellings in the transcript. Due to its larger context window, this method might be more scalable than using Whisper's prompt parameter. It's also more reliable, as GPT-4 can be instructed and guided in ways that aren't possible with Whisper due to its lack of instruction following.

**Examples:**

Example 1 (python):
```python
1
2
3
4
5
6
7
8
9
10
11
import fs from "fs";
import OpenAI from "openai";

const openai = new OpenAI();

const transcription = await openai.audio.transcriptions.create({
  file: fs.createReadStream("/path/to/file/audio.mp3"),
  model: "gpt-4o-transcribe",
});

console.log(transcription.text);
```

Example 2 (javascript):
```javascript
1
2
3
4
5
6
7
8
9
10
11
import fs from "fs";
import OpenAI from "openai";

const openai = new OpenAI();

const transcription = await openai.audio.transcriptions.create({
  file: fs.createReadStream("/path/to/file/audio.mp3"),
  model: "gpt-4o-transcribe",
});

console.log(transcription.text);
```

Example 3 (unknown):
```unknown
1
2
3
4
5
6
7
8
9
10
11
```

Example 4 (python):
```python
1
2
3
4
5
6
7
8
9
10
11
from openai import OpenAI

client = OpenAI()
audio_file= open("/path/to/file/audio.mp3", "rb")

transcription = client.audio.transcriptions.create(
    model="gpt-4o-transcribe", 
    file=audio_file
)

print(transcription.text)
```

---
