# LiveKit docs

> LiveKit is a platform for building voice and realtime AI applications. LiveKit Cloud is the hosted commercial offering based on the open-source LiveKit project.

## Overview

LiveKit is an open-source framework and cloud platform for building voice, video, and physical AI agents. It consists of these primary components:

- **LiveKit server**: An open-source WebRTC Selective Forwarding Unit (SFU) that orchestrates realtime communication. Use [LiveKit Cloud](https://cloud.livekit.io) or self-host on your own infrastructure.
- **LiveKit Agents framework**: High-level tools for building AI agents in [Python](https://github.com/livekit/agents) or [Node.js](https://github.com/livekit/agents-js), including a [deployment environment](https://docs.livekit.io/agents/ops/deployment.md) for running agents on LiveKit Cloud, a hosted voice AI [inference service](https://docs.livekit.io/agents/models.md#inference), and an extensive [plugin system](https://docs.livekit.io/agents/models.md#plugins) for connecting to a wide range of AI providers.
- A global WebRTC-based realtime media server with [realtime SDKs](https://docs.livekit.io/intro/basics/connect.md) for- [Web](https://github.com/livekit/client-sdk-js)
- [Swift](https://github.com/livekit/client-sdk-swift)
- [Android](https://github.com/livekit/client-sdk-android)
- [Flutter](https://github.com/livekit/client-sdk-flutter)
- [React Native](https://github.com/livekit/client-sdk-react-native)
- [Unity](https://github.com/livekit/client-sdk-unity)
- [Python](https://github.com/livekit/client-sdk-python)
- [Node.js](https://github.com/livekit/client-sdk-node)
- [Rust](https://github.com/livekit/client-sdk-rust)
- [ESP32](https://github.com/livekit/client-sdk-esp32)
- and more
- **Integration services**: [Telephony](https://docs.livekit.io/telephony.md) for connecting to phone networks, [Egress](https://docs.livekit.io/intro/basics/egress.md) for recording and streaming, and [Ingress](https://docs.livekit.io/intro/basics/ingress.md) for external media streams.

For greater detail, see [Intro to LiveKit](https://docs.livekit.io/intro.md).

## Introduction

### Get Started

- [Intro to LiveKit](https://docs.livekit.io/intro.md): An overview of the LiveKit ecosystem.
- [Docs MCP server](https://docs.livekit.io/intro/mcp-server.md): Turn your AI coding assistant into a LiveKit expert.
- [DeepLearning course](https://www.deeplearning.ai/short-courses/building-ai-voice-agents-for-production/)

### Understanding LiveKit

- [Overview](https://docs.livekit.io/intro/basics.md): An overview of the core concepts and fundamentals to get started with LiveKit.

#### LiveKit CLI

- [Overview](https://docs.livekit.io/intro/basics/cli.md): Command-line tools for managing LiveKit Cloud projects, creating applications, and streamlining your development workflow.
- [Setup](https://docs.livekit.io/intro/basics/cli/start.md): Install the LiveKit CLI and test your setup using an example frontend application.
- [Project management](https://docs.livekit.io/intro/basics/cli/projects.md): Add, list, and manage projects in the LiveKit CLI.
- [App templates](https://docs.livekit.io/intro/basics/cli/templates.md): Create and initialize an app from a convenient set of templates.
- [Connecting to LiveKit](https://docs.livekit.io/intro/basics/connect.md): Learn how to connect to LiveKit using realtime SDKs.

#### Rooms, participants, & tracks

- [Overview](https://docs.livekit.io/intro/basics/rooms-participants-tracks.md): Understand the core building blocks of LiveKit applications.
- [Room management](https://docs.livekit.io/intro/basics/rooms-participants-tracks/rooms.md): Create, list, and delete Rooms from your backend server.
- [Participant management](https://docs.livekit.io/intro/basics/rooms-participants-tracks/participants.md): List, remove, and mute from your backend server.
- [Track management](https://docs.livekit.io/intro/basics/rooms-participants-tracks/tracks.md): Understand tracks and track publications in LiveKit applications.
- [Webhooks & events](https://docs.livekit.io/intro/basics/rooms-participants-tracks/webhooks-events.md): Configure webhooks and handle events to monitor and respond to changes in rooms, participants, and tracks.
- [Building AI agents](https://docs.livekit.io/intro/basics/agents.md): Build AI agents that interact with users through realtime media and data streams.

### Reference

- [Recipes](https://docs.livekit.io/reference/recipes.md)
- [Room service API](https://docs.livekit.io/reference/other/roomservice-api.md): Use LiveKit's built-in API to manage rooms, participants, and tracks in your backend.

## Build Agents

### Get Started

- [Introduction](https://docs.livekit.io/agents.md): Realtime framework for voice, video, and physical AI agents.
- [Voice AI quickstart](https://docs.livekit.io/agents/start/voice-ai-quickstart.md): Build and deploy a simple voice assistant in less than 10 minutes.
- [Agent builder](https://docs.livekit.io/agents/start/builder.md): Prototype simple voice agents directly in your browser.
- [Agents playground](https://docs.livekit.io/agents/start/playground.md): A virtual workbench to test your multimodal AI agent.
- [Prompting guide](https://docs.livekit.io/agents/start/prompting.md): How to write good instructions to guide your agent's behavior.
- [Testing & evaluation](https://docs.livekit.io/agents/start/testing.md): Write tests to control and evaluate agent behavior.

### Multimodality

- [Overview](https://docs.livekit.io/agents/multimodality.md): Build agents that communicate through multiple channels for richer, more natural interactions.
- [Speech & audio](https://docs.livekit.io/agents/multimodality/audio.md): Speech and audio capabilities for LiveKit agents.
- [Text & transcriptions](https://docs.livekit.io/agents/multimodality/text.md): Integrate realtime text features into your agent.
- [Vision](https://docs.livekit.io/agents/multimodality/vision.md): Enhance your agent with visual understanding from images and live video.

### Logic & Structure

- [Overview](https://docs.livekit.io/agents/logic-structure.md): An overview of logic and structure components for LiveKit Agents.
- [Agent sessions](https://docs.livekit.io/agents/logic-structure/sessions.md): How to use AgentSession to orchestrate your voice AI app.
- [Tasks & task groups](https://docs.livekit.io/agents/logic-structure/tasks.md): Use tasks to build complex workflows for your voice AI agents.
- [Workflows](https://docs.livekit.io/agents/logic-structure/workflows.md): How to model repeatable, accurate workflows through agents, handoffs, and tasks.
- [Tool definition & use](https://docs.livekit.io/agents/logic-structure/tools.md): Let your agents call external tools and more.
- [Pipeline nodes & hooks](https://docs.livekit.io/agents/logic-structure/nodes.md): Learn how to customize the behavior of your agent with nodes and hooks in the voice pipeline.

#### Turn detection & interruptions

- [Overview](https://docs.livekit.io/agents/logic-structure/turns.md): Guide to managing conversation turns in voice AI.
- [Turn detector](https://docs.livekit.io/agents/logic-structure/turns/turn-detector.md): Open-weights model for contextually-aware voice AI turn detection.
- [Silero VAD plugin](https://docs.livekit.io/agents/logic-structure/turns/vad.md): High-performance voice activity detection for LiveKit Agents.
- [Agents & handoffs](https://docs.livekit.io/agents/logic-structure/agents-handoffs.md): How to use agents and handoffs as part of a voice AI workflow.
- [External data & RAG](https://docs.livekit.io/agents/logic-structure/external-data.md): Best practices for adding context and taking external actions.

### Agent Server

- [Overview](https://docs.livekit.io/agents/server.md): An overview of agent server components for LiveKit Agents.
- [Server lifecycle](https://docs.livekit.io/agents/server/lifecycle.md): How agent servers register, receive requests, and manage jobs.
- [Agent dispatch](https://docs.livekit.io/agents/server/agent-dispatch.md): Specifying how and when your agents are assigned to rooms.
- [Job lifecycle](https://docs.livekit.io/agents/server/job.md): Learn more about the entrypoint function and how to end and clean up LiveKit sessions.
- [Server options](https://docs.livekit.io/agents/server/options.md): Learn about the options available for creating an agent server.

### Models

- [Overview](https://docs.livekit.io/agents/models.md): Choose the right AI models for your voice agent.

#### LLM

- [Overview](https://docs.livekit.io/agents/models/llm.md): Conversational intelligence for your voice agents.

##### Inference

- [DeepSeek](https://docs.livekit.io/agents/models/llm/inference/deepseek.md): Reference for DeepSeek models served via LiveKit Inference.
- [Gemini](https://docs.livekit.io/agents/models/llm/inference/gemini.md): Reference for the Google Gemini models served via LiveKit Inference.
- [Kimi](https://docs.livekit.io/agents/models/llm/inference/kimi.md): Reference for Kimi models served via LiveKit Inference.
- [OpenAI](https://docs.livekit.io/agents/models/llm/inference/openai.md): Reference for OpenAI models served via LiveKit Inference.
- [Qwen](https://docs.livekit.io/agents/models/llm/inference/qwen.md): Reference for Qwen models served via LiveKit Inference.

##### Plugins

- [Anthropic](https://docs.livekit.io/agents/models/llm/plugins/anthropic.md): How to use the Anthropic Claude LLM plugin for LiveKit Agents.
- [AWS](https://docs.livekit.io/agents/models/llm/plugins/aws.md): How to use the Amazon Bedrock LLM plugin for LiveKit Agents.
- [Azure OpenAI](https://docs.livekit.io/agents/models/llm/plugins/azure-openai.md): How to use the Azure OpenAI LLM plugin for LiveKit Agents.
- [Baseten](https://docs.livekit.io/agents/models/llm/plugins/baseten.md): How to use the Baseten LLM plugin for LiveKit Agents.
- [Cerebras](https://docs.livekit.io/agents/models/llm/plugins/cerebras.md): How to use the Cerebras inference with LiveKit Agents.
- [DeepSeek](https://docs.livekit.io/agents/models/llm/plugins/deepseek.md): How to use DeepSeek models with LiveKit Agents.
- [Fireworks](https://docs.livekit.io/agents/models/llm/plugins/fireworks.md): How to use Fireworks AI with LiveKit Agents.
- [Gemini](https://docs.livekit.io/agents/models/llm/plugins/gemini.md): A guide to using Google Gemini with LiveKit Agents.
- [Groq](https://docs.livekit.io/agents/models/llm/plugins/groq.md): How to use the Groq LLM plugin for LiveKit Agents.
- [LangChain](https://docs.livekit.io/agents/models/llm/plugins/langchain.md): How to use LangGraph workflows with LiveKit Agents.
- [Letta](https://docs.livekit.io/agents/models/llm/plugins/letta.md): How to use a Letta agent for your LLM with LiveKit Agents.
- [Mistral AI](https://docs.livekit.io/agents/models/llm/plugins/mistralai.md): How to integrate Mistral AI's La Plateforme inference service with LiveKit Agents.
- [Ollama](https://docs.livekit.io/agents/models/llm/plugins/ollama.md): How to run models locally using Ollama with LiveKit Agents.
- [OpenAI](https://docs.livekit.io/agents/models/llm/plugins/openai.md): How to use the OpenAI LLM plugin for LiveKit Agents.
- [OpenRouter](https://docs.livekit.io/agents/models/llm/plugins/openrouter.md): How to use OpenRouter with LiveKit Agents to access 500+ AI models.
- [Perplexity](https://docs.livekit.io/agents/models/llm/plugins/perplexity.md): How to use Perplexity LLM with LiveKit Agents.
- [Telnyx](https://docs.livekit.io/agents/models/llm/plugins/telnyx.md): How to use Telnyx inference with LiveKit Agents.
- [Together](https://docs.livekit.io/agents/models/llm/plugins/together.md): How to use Together AI Llama models with LiveKit Agents.
- [XAI](https://docs.livekit.io/agents/models/llm/plugins/xai.md): How to use xAI LLM with LiveKit Agents.

#### STT

- [Overview](https://docs.livekit.io/agents/models/stt.md): Models and plugins for realtime transcription in your voice agents.

##### Inference

- [AssemblyAI](https://docs.livekit.io/agents/models/stt/inference/assemblyai.md): Reference for AssemblyAI STT in LiveKit Inference.
- [Cartesia](https://docs.livekit.io/agents/models/stt/inference/cartesia.md): Reference for Cartesia STT in LiveKit Inference.
- [Deepgram](https://docs.livekit.io/agents/models/stt/inference/deepgram.md): Reference for Deepgram STT in LiveKit Inference.

##### Plugins

- [AssemblyAI](https://docs.livekit.io/agents/models/stt/plugins/assemblyai.md): How to use the AssemblyAI STT plugin for LiveKit Agents.
- [AWS](https://docs.livekit.io/agents/models/stt/plugins/aws.md): How to use the Amazon Transcribe STT plugin for LiveKit Agents.
- [Azure](https://docs.livekit.io/agents/models/stt/plugins/azure.md): How to use the Azure Speech STT plugin for LiveKit Agents.
- [Azure OpenAI](https://docs.livekit.io/agents/models/stt/plugins/azure-openai.md): How to use the Azure OpenAI STT plugin for LiveKit Agents.
- [Baseten](https://docs.livekit.io/agents/models/stt/plugins/baseten.md): How to use the Baseten STT plugin for LiveKit Agents.
- [Cartesia](https://docs.livekit.io/agents/models/stt/plugins/cartesia.md): How to use the Cartesia STT plugin for LiveKit Agents.
- [Clova](https://docs.livekit.io/agents/models/stt/plugins/clova.md): How to use the Clova STT plugin for LiveKit Agents.
- [Deepgram](https://docs.livekit.io/agents/models/stt/plugins/deepgram.md): How to use the Deepgram STT plugin for LiveKit Agents.
- [FAL](https://docs.livekit.io/agents/models/stt/plugins/fal.md): How to use the fal STT plugin for LiveKit Agents.
- [Gladia](https://docs.livekit.io/agents/models/stt/plugins/gladia.md): How to use the Gladia STT plugin for LiveKit Agents.
- [Google](https://docs.livekit.io/agents/models/stt/plugins/google.md): How to use the Google Cloud STT plugin for LiveKit Agents.
- [Groq](https://docs.livekit.io/agents/models/stt/plugins/groq.md): How to use the Groq STT plugin for LiveKit Agents.
- [Mistral AI](https://docs.livekit.io/agents/models/stt/plugins/mistralai.md): How to use the Mistral STT plugin for LiveKit Agents.
- [OpenAI](https://docs.livekit.io/agents/models/stt/plugins/openai.md): How to use the OpenAI STT plugin for LiveKit Agents.
- [Sarvam](https://docs.livekit.io/agents/models/stt/plugins/sarvam.md): How to use the Sarvam STT plugin for LiveKit Agents.
- [Soniox](https://docs.livekit.io/agents/models/stt/plugins/soniox.md): How to use the Soniox STT plugin for LiveKit Agents.
- [Speechmatics](https://docs.livekit.io/agents/models/stt/plugins/speechmatics.md): How to use the Speechmatics STT plugin for LiveKit Agents.
- [Spitch](https://docs.livekit.io/agents/models/stt/plugins/spitch.md): How to use the Spitch STT plugin for LiveKit Agents.

#### TTS

- [Overview](https://docs.livekit.io/agents/models/tts.md): Voices and plugins to add realtime speech to your voice agents.

##### Inference

- [Cartesia](https://docs.livekit.io/agents/models/tts/inference/cartesia.md): Reference for Cartesia TTS in LiveKit Inference.
- [ElevenLabs](https://docs.livekit.io/agents/models/tts/inference/elevenlabs.md): Reference for ElevenLabs TTS in LiveKit Inference.
- [Inworld](https://docs.livekit.io/agents/models/tts/inference/inworld.md): Reference for Inworld TTS in LiveKit Inference.
- [Rime](https://docs.livekit.io/agents/models/tts/inference/rime.md): Reference for Rime TTS in LiveKit Inference.

##### Plugins

- [AWS](https://docs.livekit.io/agents/models/tts/plugins/aws.md): How to use the Amazon Polly TTS plugin for LiveKit Agents.
- [Azure](https://docs.livekit.io/agents/models/tts/plugins/azure.md): How to use the Azure Speech TTS plugin for LiveKit Agents.
- [Azure OpenAI](https://docs.livekit.io/agents/models/tts/plugins/azure-openai.md): How to use the Azure OpenAI TTS plugin for LiveKit Agents.
- [Baseten](https://docs.livekit.io/agents/models/tts/plugins/baseten.md): How to use the Baseten TTS plugin for LiveKit Agents.
- [Cartesia](https://docs.livekit.io/agents/models/tts/plugins/cartesia.md): How to use the Cartesia TTS plugin for LiveKit Agents.
- [Deepgram](https://docs.livekit.io/agents/models/tts/plugins/deepgram.md): How to use the Deepgram TTS plugin for LiveKit Agents.
- [ElevenLabs](https://docs.livekit.io/agents/models/tts/plugins/elevenlabs.md): How to use the ElevenLabs TTS plugin for LiveKit Agents.
- [Gemini](https://docs.livekit.io/agents/models/tts/plugins/gemini.md): How to use the Gemini TTS plugin for LiveKit Agents.
- [Google](https://docs.livekit.io/agents/models/tts/plugins/google.md): How to use the Google Cloud TTS plugin for LiveKit Agents.
- [Groq](https://docs.livekit.io/agents/models/tts/plugins/groq.md): How to use the Groq TTS plugin for LiveKit Agents.
- [Hume](https://docs.livekit.io/agents/models/tts/plugins/hume.md): How to use the Hume TTS plugin for LiveKit Agents.
- [Inworld](https://docs.livekit.io/agents/models/tts/plugins/inworld.md): How to use the Inworld TTS plugin for LiveKit Agents.
- [LMNT](https://docs.livekit.io/agents/models/tts/plugins/lmnt.md): How to use the LMNT TTS plugin for LiveKit Agents.
- [Minimax](https://docs.livekit.io/agents/models/tts/plugins/minimax.md): How to use the MiniMax TTS plugin for LiveKit Agents.
- [Neuphonic](https://docs.livekit.io/agents/models/tts/plugins/neuphonic.md): How to use the Neuphonic TTS plugin for LiveKit Agents.
- [OpenAI](https://docs.livekit.io/agents/models/tts/plugins/openai.md): How to use the OpenAI TTS plugin for LiveKit Agents.
- [Resemble](https://docs.livekit.io/agents/models/tts/plugins/resemble.md): How to use the Resemble AI TTS plugin for LiveKit Agents.
- [Rime](https://docs.livekit.io/agents/models/tts/plugins/rime.md): How to use the Rime TTS plugin for LiveKit Agents.
- [Sarvam](https://docs.livekit.io/agents/models/tts/plugins/sarvam.md): How to use the Sarvam TTS plugin for LiveKit Agents.
- [Smallest AI](https://docs.livekit.io/agents/models/tts/plugins/smallestai.md): How to use the Smallest AI Waves TTS plugin for LiveKit Agents.
- [Speechify](https://docs.livekit.io/agents/models/tts/plugins/speechify.md): How to use the Speechify TTS plugin for LiveKit Agents.
- [Spitch](https://docs.livekit.io/agents/models/tts/plugins/spitch.md): How to use the Spitch TTS plugin for LiveKit Agents.

#### Realtime

- [Overview](https://docs.livekit.io/agents/models/realtime.md): Guides for adding realtime model integrations to your agents.

##### Plugins

- [Azure OpenAI](https://docs.livekit.io/agents/models/realtime/plugins/azure-openai.md): How to use the Azure OpenAI Realtime API with LiveKit Agents.
- [Gemini](https://docs.livekit.io/agents/models/realtime/plugins/gemini.md): How to use the Gemini Live API with LiveKit Agents.
- [Nova Sonic](https://docs.livekit.io/agents/models/realtime/plugins/nova-sonic.md): How to use the Amazon Nova Sonic model with LiveKit Agents.
- [OpenAI](https://docs.livekit.io/agents/models/realtime/plugins/openai.md): How to use the OpenAI Realtime API with LiveKit Agents.
- [Ultravox](https://docs.livekit.io/agents/models/realtime/plugins/ultravox.md): How to use the Ultravox Realtime model with LiveKit Agents.

#### Virtual avatar

- [Overview](https://docs.livekit.io/agents/models/avatar.md): Guides for adding virtual avatars to your agents.

##### Plugins

- [Anam](https://docs.livekit.io/agents/models/avatar/plugins/anam.md): How to use the Anam virtual avatar plugin for LiveKit Agents.
- [BEY](https://docs.livekit.io/agents/models/avatar/plugins/bey.md): How to use the Beyond Presence virtual avatar plugin for LiveKit Agents.
- [Bithuman](https://docs.livekit.io/agents/models/avatar/plugins/bithuman.md): How to use the bitHuman virtual avatar plugin for LiveKit Agents.
- [Hedra](https://docs.livekit.io/agents/models/avatar/plugins/hedra.md): How to use the Hedra virtual avatar plugin for LiveKit Agents.
- [Simli](https://docs.livekit.io/agents/models/avatar/plugins/simli.md): How to use the Simli virtual avatar plugin for LiveKit Agents.
- [Tavus](https://docs.livekit.io/agents/models/avatar/plugins/tavus.md): How to use the Tavus virtual avatar plugin for LiveKit Agents.

### Reference

- [Agents framework](https://docs.livekit.io/reference.md#agents-framework/)
- [Events and error handling](https://docs.livekit.io/reference/other/events.md): Guides and reference for events and error handling in LiveKit Agents.
- [Agent CLI reference](https://docs.livekit.io/reference/other/agent-cli.md): Reference for the LiveKit Cloud agent deployment commands in the LiveKit CLI.

## Agent Frontends

### Get Started

- [Introduction](https://docs.livekit.io/frontends.md): Build frontends for your LiveKit Agents across web, mobile, hardware, and telephony platforms.
- [Web & mobile frontends](https://docs.livekit.io/frontends/start/frontends.md): Bring your agent to life through a web or mobile app.

### UI Components

- [Overview](https://docs.livekit.io/frontends/components.md): An overview of UI components for LiveKit frontends.

### Authentication

- [Overview](https://docs.livekit.io/frontends/authentication.md): An overview of authentication for LiveKit frontends.

#### Tokens

- [Overview](https://docs.livekit.io/frontends/authentication/tokens.md): Overview of access tokens, grants, and permissions.
- [Generating tokens](https://docs.livekit.io/frontends/authentication/tokens/generate.md): Step-by-step guide to generate tokens for your frontend.

### Telephony

- [Overview](https://docs.livekit.io/frontends/telephony.md): An overview of telephony integration for LiveKit frontends.
- [Agents integration](https://docs.livekit.io/frontends/telephony/agents.md): Enable your voice AI agent to make and receive phone calls.

### Reference

- [LiveKit SDKs](https://docs.livekit.io/reference.md#livekit-sdks)
- [Server APIs](https://docs.livekit.io/reference.md#server-apis)
- [UI components](https://docs.livekit.io/reference.md#ui-components)

## Telephony

### Get Started

- [Introduction](https://docs.livekit.io/telephony.md): LiveKit's telephony services enable seamless integration between traditional phone networks and LiveKit's realtime platform.
- [Phone numbers](https://docs.livekit.io/telephony/start/phone-numbers.md): How to purchase and configure phone numbers directly through LiveKit.
- [SIP trunk setup](https://docs.livekit.io/telephony/start/sip-trunk-setup.md): Guide to integrating SIP trunks with LiveKit telephony.

#### Provider-specific quickstarts

- [Overview](https://docs.livekit.io/telephony/start/providers.md)
- [Twilio](https://docs.livekit.io/telephony/start/providers/twilio.md): Step-by-step instructions for creating inbound and outbound SIP trunks using Twilio.
- [Telnyx](https://docs.livekit.io/telephony/start/providers/telnyx.md): Step-by-step instructions for creating inbound and outbound SIP trunks using Telnyx.
- [Plivo](https://docs.livekit.io/telephony/start/providers/plivo.md): Step-by-step instructions for creating inbound and outbound SIP trunks using Plivo.
- [Wavix](https://docs.livekit.io/telephony/start/providers/wavix.md): Step-by-step instructions for configuring inbound and outbound calls using Wavix and LiveKit.

### Features

- [Overview](https://docs.livekit.io/telephony/features.md): An overview of telephony features for LiveKit.
- [DTMF](https://docs.livekit.io/telephony/features/dtmf.md): Sending and receiving DTMF tones.
- [Region pinning](https://docs.livekit.io/telephony/features/region-pinning.md): Learn how to isolate LiveKit traffic to a specific region.

#### Transfers

- [Overview](https://docs.livekit.io/telephony/features/transfers.md): An overview of call transfer features for LiveKit telephony.
- [Call forwarding](https://docs.livekit.io/telephony/features/transfers/cold.md): Transfer calls to another number or SIP endpoint using SIP REFER.
- [Agent-assisted transfer](https://docs.livekit.io/telephony/features/transfers/warm.md): How to transfer a call from an AI agent to a human operator while providing a contextual summary.
- [HD voice](https://docs.livekit.io/telephony/features/hd-voice.md): LiveKit SIP supports high fidelity calls by enabling HD voice.
- [Secure trunking](https://docs.livekit.io/telephony/features/secure-trunking.md): How to enable secure trunking for LiveKit SIP.

### Accepting calls

- [Overview](https://docs.livekit.io/telephony/accepting-calls.md): An overview of accepting inbound calls with LiveKit telephony.
- [Workflow & setup](https://docs.livekit.io/telephony/accepting-calls/workflow-setup.md): Workflow and setup guide for accepting inbound calls.
- [Inbound trunk](https://docs.livekit.io/telephony/accepting-calls/inbound-trunk.md): How to create and configure an inbound trunk to accept incoming calls using a SIP provider.
- [Dispatch rule](https://docs.livekit.io/telephony/accepting-calls/dispatch-rule.md): How to create and configure a dispatch rule.
- [Twilio Voice integration](https://docs.livekit.io/telephony/accepting-calls/inbound-twilio.md): How to use LiveKit SIP with TwiML and Twilio conferencing.

### Making calls

- [Overview](https://docs.livekit.io/telephony/making-calls.md): An overview of making outbound calls with LiveKit telephony.
- [Workflow & setup](https://docs.livekit.io/telephony/making-calls/workflow-setup.md): Workflow and setup for making outbound calls.
- [Outbound trunk](https://docs.livekit.io/telephony/making-calls/outbound-trunk.md): How to create and configure a outbound trunk to make outgoing calls.
- [Outbound calls](https://docs.livekit.io/telephony/making-calls/outbound-calls.md): Create a LiveKit SIP participant to make outbound calls.

### Reference

- [SIP participant](https://docs.livekit.io/reference/telephony/sip-participant.md): Mapping a caller to a SIP participant.
- [Phone Numbers API](https://docs.livekit.io/reference/telephony/phone-numbers-api.md): Use LiveKit's Phone Number APIs to manage phone numbers for your telephony apps.
- [SIP API](https://docs.livekit.io/reference/telephony/sip-api.md): Use LiveKit's built-in SIP APIs to manage your SIP-based apps.
- [Server APIs](https://docs.livekit.io/reference.md#server-apis)
- [Troubleshooting](https://docs.livekit.io/reference/telephony/troubleshooting.md): Common issues and solutions for SIP.

## WebRTC Transport

### Get Started

- [Introduction](https://docs.livekit.io/transport.md): Build realtime applications with LiveKit's WebRTC transport layer, SDKs, and media handling capabilities.

#### SDK platform quickstarts

- [Overview](https://docs.livekit.io/transport/sdk-platforms.md)
- [React](https://docs.livekit.io/transport/sdk-platforms/react.md): Build a voice AI frontend with React in less than 10 minutes.
- [Unity (WebGL)](https://docs.livekit.io/transport/sdk-platforms/unity-web.md): Get started with LiveKit and Unity (WebGL)
- [Swift](https://docs.livekit.io/transport/sdk-platforms/swift.md): Get started with LiveKit on iOS using SwiftUI
- [Android (Compose)](https://docs.livekit.io/transport/sdk-platforms/android-compose.md): Get started with LiveKit and Android using Jetpack Compose
- [Android](https://docs.livekit.io/transport/sdk-platforms/android.md): Get started with LiveKit and Android
- [Flutter](https://docs.livekit.io/transport/sdk-platforms/flutter.md): Get started with LiveKit and Flutter
- [React Native](https://docs.livekit.io/transport/sdk-platforms/react-native.md): Get started with LiveKit and React Native
- [Expo](https://docs.livekit.io/transport/sdk-platforms/expo.md): Get started with LiveKit and Expo on React Native

### Media

- [Overview](https://docs.livekit.io/transport/media.md): An overview of realtime media components for LiveKit.
- [Camera & microphone](https://docs.livekit.io/transport/media/publish.md): Publish realtime audio and video from any device.
- [Screen sharing](https://docs.livekit.io/transport/media/screenshare.md): Publish your screen with LiveKit.
- [Subscribing to tracks](https://docs.livekit.io/transport/media/subscribe.md): Play and render realtime media tracks in your application.
- [Processing raw tracks](https://docs.livekit.io/transport/media/raw-tracks.md): How to read, process, and publish raw media tracks and files.
- [Noise & echo cancellation](https://docs.livekit.io/transport/media/noise-cancellation.md): Achieve crystal-clear audio for video conferencing and voice AI.
- [Enhanced noise cancellation](https://docs.livekit.io/transport/media/enhanced-noise-cancellation.md): LiveKit Cloud offers AI-powered noise cancellation for realtime audio.
- [Codecs & more](https://docs.livekit.io/transport/media/advanced.md): Advanced audio and video topics.

#### Stream export & import

- [Overview](https://docs.livekit.io/transport/media/ingress-egress.md): An overview of stream export and import components for LiveKit.

##### Egress

- [Overview](https://docs.livekit.io/transport/media/ingress-egress/egress.md): Use LiveKit's Egress service to record or livestream a room.
- [RoomComposite & web egress](https://docs.livekit.io/transport/media/ingress-egress/egress/composite-recording.md): LiveKit web-based recorder gives you flexible compositing options.
- [Participant & TrackComposite egress](https://docs.livekit.io/transport/media/ingress-egress/egress/participant.md): Record participants individually with the egress API.
- [Track egress](https://docs.livekit.io/transport/media/ingress-egress/egress/track.md): Track egress allows you export a single track without transcoding.
- [Auto egress](https://docs.livekit.io/transport/media/ingress-egress/egress/autoegress.md): Automatically start recording with a room.
- [Output & streaming options](https://docs.livekit.io/transport/media/ingress-egress/egress/outputs.md): Export content anywhere, in any format.
- [Custom recording templates](https://docs.livekit.io/transport/media/ingress-egress/egress/custom-template.md): Create your own recording layout to use with Room Composite Egress.

##### Ingress

- [Overview](https://docs.livekit.io/transport/media/ingress-egress/ingress.md): Use LiveKit's Ingress service to bring live streams from non-WebRTC sources into LiveKit rooms.
- [Encoder configuration](https://docs.livekit.io/transport/media/ingress-egress/ingress/encoders.md): How to configure streaming software to work with LiveKit Ingress.
- [Transcoding configuration](https://docs.livekit.io/transport/media/ingress-egress/ingress/transcode.md): Configure video and audio encoding settings for LiveKit Ingress, including presets and custom encoding options.

### Data

- [Overview](https://docs.livekit.io/transport/data.md): An overview of realtime text and data features for LiveKit.
- [Sending text](https://docs.livekit.io/transport/data/text-streams.md): Use text streams to send any amount of text between participants.
- [Sending files & bytes](https://docs.livekit.io/transport/data/byte-streams.md): Use byte streams to send files, images, or any other kind of data between participants.
- [Remote method calls](https://docs.livekit.io/transport/data/rpc.md): Use remote procedure calls (RPCs) to execute custom methods on other participants in the room and await a response.
- [Data packets](https://docs.livekit.io/transport/data/packets.md): Low-level API for high frequency or advanced use cases.

#### State synchronization

- [Overview](https://docs.livekit.io/transport/data/state.md): An overview of state synchronization components for LiveKit.
- [Participant attributes](https://docs.livekit.io/transport/data/state/participant-attributes.md): A key-value store for per-participant state.
- [Room metadata](https://docs.livekit.io/transport/data/state/room-metadata.md): Share application-specific state with all participants.

### Encryption

- [Overview](https://docs.livekit.io/transport/encryption.md): Secure your realtime media and data with end-to-end encryption.
- [Get started](https://docs.livekit.io/transport/encryption/start.md): Learn how to implement end-to-end encryption in your LiveKit applications.

### Self-hosting

- [Overview](https://docs.livekit.io/transport/self-hosting.md): An overview of self-hosting options for LiveKit servers.
- [Running locally](https://docs.livekit.io/transport/self-hosting/local.md): This will get a LiveKit instance up and running, ready to receive audio and video streams from participants.
- [Deployment](https://docs.livekit.io/transport/self-hosting/deployment.md): WebRTC servers can be tricky to deploy because of their use of UDP ports and having to know their own public IP address. This guide will help you get a secure LiveKit deployment up and running.
- [Virtual machines](https://docs.livekit.io/transport/self-hosting/vm.md): This guide helps you to set up a production-ready LiveKit server on a cloud virtual machine.
- [Kubernetes](https://docs.livekit.io/transport/self-hosting/kubernetes.md): Deploy LiveKit to Kubernetes.
- [Distributed multi-region](https://docs.livekit.io/transport/self-hosting/distributed.md): LiveKit is architected to be distributed, with homogeneous instances running across many servers. In distributed mode, Redis is required as shared data store and message bus.
- [Firewall configuration](https://docs.livekit.io/transport/self-hosting/ports-firewall.md): Reference for ports and suggested firewall rules for LiveKit.
- [Benchmarks](https://docs.livekit.io/transport/self-hosting/benchmark.md): Guide to load-testing and benchmarking your LiveKit installation.
- [Egress](https://docs.livekit.io/transport/self-hosting/egress.md): The Egress service uses Redis messaging queues to load balance and communicate with your LiveKit server.
- [Ingress](https://docs.livekit.io/transport/self-hosting/ingress.md): The Ingress service uses Redis messaging queues to communicate with your LiveKit server.
- [SIP server](https://docs.livekit.io/transport/self-hosting/sip-server.md): Setting up and configuring a self-hosted SIP server for LiveKit telephony apps.

### Reference

- [LiveKit SDKs](https://docs.livekit.io/reference.md#livekit-sdks)
- [Egress API](https://docs.livekit.io/reference/other/egress/api.md): Use LiveKit's egress service to record or livestream a Room.
- [Ingress API](https://docs.livekit.io/reference/other/ingress/api.md): Use LiveKit's ingress service to import live streams from non-WebRTC sources into LiveKit rooms.
- [Server APIs](https://docs.livekit.io/reference.md#server-apis)

## Manage & Deploy

### Get Started

- [Introduction](https://docs.livekit.io/deploy.md): Deploy, manage, and monitor your LiveKit applications with a comprehensive suite of tools and flexible hosting options.

### Agent deployment

- [Overview](https://docs.livekit.io/deploy/agents.md): Deploy your agents to LiveKit Cloud or custom environments, manage secrets and builds, and monitor your deployments.

#### LiveKit Cloud

- [Overview](https://docs.livekit.io/deploy/agents/cloud.md): An end-to-end platform for building, deploying, and operating AI agent applications.
- [Get started](https://docs.livekit.io/deploy/agents/cloud/start.md): Deploy your agents to LiveKit Cloud.
- [Secrets management](https://docs.livekit.io/deploy/agents/cloud/secrets.md): Manage secrets for your LiveKit Cloud agent deployments.
- [Log collection](https://docs.livekit.io/deploy/agents/cloud/logs.md): Monitor and debug your deployed agents with comprehensive logging.
- [Builds and Dockerfiles](https://docs.livekit.io/deploy/agents/cloud/builds.md): Guide to the LiveKit Cloud build process, plus Dockerfile templates and resources.
- [Custom deployments](https://docs.livekit.io/deploy/custom/deployments.md): Guide to running LiveKit Agents in a custom environment.

### Agent Observability

- [Overview](https://docs.livekit.io/deploy/observability.md): An overview of observability features for LiveKit Agents.
- [Insights in LiveKit Cloud](https://docs.livekit.io/deploy/observability/insights.md): View transcripts, traces, logs, and audio recordings in LiveKit Cloud.
- [Data hooks](https://docs.livekit.io/deploy/observability/data.md): Collect session recordings, transcripts, metrics, and other data within the LiveKit Agents SDK.

### Administration

- [Overview](https://docs.livekit.io/deploy/admin.md): Manage your project regions, firewalls, and quotas.
- [Regions](https://docs.livekit.io/deploy/admin/regions.md): Configure and manage agent deployments across multiple regions.
- [Sandbox](https://docs.livekit.io/deploy/admin/sandbox.md): Rapidly prototype your apps and share them with others, cutting out the boilerplate.
- [Configuring firewalls](https://docs.livekit.io/deploy/admin/firewall.md): Learn how to configure firewalls for LiveKit Cloud.
- [Quotas & limits](https://docs.livekit.io/deploy/admin/quotas-and-limits.md): Guide to the quotas and limits for LiveKit Cloud plans.
- [Billing](https://docs.livekit.io/deploy/admin/billing.md): Guide to LiveKit Cloud invoices and billing cycles.
- [Analytics API](https://docs.livekit.io/deploy/admin/analytics-api.md): Get information about your LiveKit Cloud sessions and participants

### Reference

- [Agent CLI reference](https://docs.livekit.io/reference/other/agent-cli.md): Reference for the LiveKit Cloud agent deployment commands in the LiveKit CLI.
- [Server APIs](https://docs.livekit.io/reference.md#server-apis)
- [Events and error handling](https://docs.livekit.io/reference/other/events.md): Guides and reference for events and error handling in LiveKit Agents.
- [LiveKit SFU](https://docs.livekit.io/reference/internals/livekit-sfu.md): LiveKit is an opinionated, horizontally-scaling WebRTC Selective Forwarding Unit.

## Reference

### Get Started

- [Overview](https://docs.livekit.io/reference.md): All reference documentation in the LiveKit ecosystem with links to complete docs, package registries, and source code.
- [Recipes](https://docs.livekit.io/reference/recipes.md)

### Agents framework

- [Python](https://docs.livekit.io/reference/python/v1/livekit/agents.md)
- [Node.js](https://docs.livekit.io/reference/agents-js.md)

### LiveKit SDKs

- [JavaScript](https://docs.livekit.io/reference/client-sdk-js/index.html.md)
- [Swift](https://docs.livekit.io/reference/client-sdk-swift/documentation/livekit.md)
- [Android](https://docs.livekit.io/reference/client-sdk-android/index.html.md)
- [Flutter](https://docs.livekit.io/reference/client-sdk-flutter/index.html.md)
- [React Native](https://github.com/livekit/client-sdk-react-native)
- [Unity](https://github.com/livekit/client-sdk-unity)
- [Unity (WebGL)](https://github.com/livekit/client-sdk-unity-web)
- [Node.js](https://docs.livekit.io/reference/client-sdk-node.md)
- [Rust](https://github.com/livekit/rust-sdks)
- [Python](https://docs.livekit.io/reference/python/v1/livekit/rtc/index.html.md)
- [Go](https://github.com/livekit/server-sdk-go)

### UI Components

- [React](https://docs.livekit.io/reference/components/react.md)
- [SwiftUI](https://livekit.github.io/components-swift/documentation/livekitcomponents)
- [Android](https://docs.livekit.io/reference/components/android.md): LiveKit Android Components are the easiest way to build realtime audio/video apps with Jetpack Compose on Android.

### Server APIs

- [Go](https://pkg.go.dev/github.com/livekit/server-sdk-go/v2)
- [Node](https://docs.livekit.io/reference/server-sdk-js/index.html.md)
- [Ruby](https://github.com/livekit/server-sdk-ruby)
- [Kotlin/Java](https://github.com/livekit/server-sdk-kotlin)
- [Python](https://docs.livekit.io/reference/python/v1/livekit/api.md)
- [PHP](https://github.com/agence104/livekit-server-sdk-php)

### Internals

- [LiveKit SFU](https://docs.livekit.io/reference/internals/livekit-sfu.md): LiveKit is an opinionated, horizontally-scaling WebRTC Selective Forwarding Unit.
- [Signaling Protocol](https://docs.livekit.io/reference/internals/client-protocol.md): This is an overview of the core protocol LiveKit uses to communicate with clients. It's primarily oriented towards those building new SDKs or developers interested in contributing to LiveKit.

### Telephony

- [SIP participant](https://docs.livekit.io/reference/telephony/sip-participant.md): Mapping a caller to a SIP participant.
- [SIP API](https://docs.livekit.io/reference/telephony/sip-api.md): Use LiveKit's built-in SIP APIs to manage your SIP-based apps.
- [Phone Numbers API](https://docs.livekit.io/reference/telephony/phone-numbers-api.md): Use LiveKit's Phone Number APIs to manage phone numbers for your telephony apps.
- [Troubleshooting](https://docs.livekit.io/reference/telephony/troubleshooting.md): Common issues and solutions for SIP.

### Migration Guides

- [v1 to v2 SDK migration](https://docs.livekit.io/reference/migration-guides/migrate-from-v1.md): Overview of how to migrate your applications from LiveKit SDK v1.x to v2

#### v0.x migration

- [Node.js](https://docs.livekit.io/reference/migration-guides/v0-migration/nodejs.md): Migrate your Node.js agents from version 0.x to 1.0.
- [Python](https://docs.livekit.io/reference/migration-guides/v0-migration/python.md): Migrate your Python-based agents from version v0.x to 1.0.

### Other

- [Agent CLI reference](https://docs.livekit.io/reference/other/agent-cli.md): Reference for the LiveKit Cloud agent deployment commands in the LiveKit CLI.
- [Room service API](https://docs.livekit.io/reference/other/roomservice-api.md): Use LiveKit's built-in API to manage rooms, participants, and tracks in your backend.

#### Egress

- [Egress API](https://docs.livekit.io/reference/other/egress/api.md): Use LiveKit's egress service to record or livestream a Room.
- [Egress examples](https://docs.livekit.io/reference/other/egress/examples.md): Usage examples for Egress APIs to record or livestream a room or individual tracks.

#### Ingress

- [Ingress API](https://docs.livekit.io/reference/other/ingress/api.md): Use LiveKit's ingress service to import live streams from non-WebRTC sources into LiveKit rooms.
- [Events and error handling](https://docs.livekit.io/reference/other/events.md): Guides and reference for events and error handling in LiveKit Agents.

## Recipes

- **[Voice AI quickstart](https://docs.livekit.io/agents/start/voice-ai.md)**: Create a voice AI agent in less than 10 minutes.

- **[SwiftUI Voice Agent](https://github.com/livekit-examples/agent-starter-swift)**: A native iOS, macOS, and visionOS voice AI assistant built in SwiftUI.

- **[Next.js Voice Agent](https://github.com/livekit-examples/agent-starter-react)**: A web voice AI assistant built with React and Next.js.

- **[Flutter Voice Agent](https://github.com/livekit-examples/agent-starter-flutter)**: A cross-platform voice AI assistant app built with Flutter.

- **[React Native Voice Agent](https://github.com/livekit-examples/agent-starter-react-native)**: A native voice AI assistant app built with React Native and Expo.

- **[Android Voice Agent](https://github.com/livekit-examples/agent-starter-android)**: A native Android voice AI assistant app built with Kotlin and Jetpack Compose.

- **[Web Embed Voice Agent](https://github.com/livekit-examples/agent-starter-embed)**: A voice AI agent that can be embedded in any web page.

- **[Medical Office Triage](https://github.com/livekit-examples/python-agents-examples/tree/main/complex-agents/medical_office_triage)**: Agent that triages patients based on symptoms and medical history.

- **[Personal Shopper](https://github.com/livekit-examples/python-agents-examples/tree/main/complex-agents/personal_shopper)**: AI shopping assistant that helps find products based on user preferences.

- **[Restaurant Agent](https://github.com/livekit/agents/blob/main/examples/voice_agents/restaurant_agent.py)**: A restaurant front-of-house agent that can take orders, add items to a shared cart, and checkout.

- **[LivePaint](https://github.com/livekit-examples/livepaint)**: A realtime drawing game where players compete to complete a drawing prompt while being judged by a realtime AI agent.

- **[Push-to-Talk Agent](https://github.com/livekit/agents/blob/main/examples/voice_agents/push_to_talk.py)**: A voice AI agent that uses push-to-talk for controlled multi-participant conversations, only enabling audio input when explicitly triggered.

- **[Background audio](https://github.com/livekit/agents/blob/main/examples/voice_agents/background_audio.py)**: A voice AI agent with background audio for thinking states and ambiance.

- **[Background audio example in Node.js](https://github.com/livekit/agents-js/blob/main/examples/src/background_audio.ts)**: A voice AI agent with background audio for ambiance.

- **[Uninterruptable Agent](https://docs.livekit.io/recipes/uninterruptable.md)**: An agent that continues speaking without being interrupted.

- **[Change Language](https://docs.livekit.io/recipes/changing_language.md)**: Agent that can switch between different languages during conversation.

- **[TTS Comparison](https://docs.livekit.io/recipes/tts_comparison.md)**: Compare different text-to-speech providers side by side.

- **[Transcriber](https://docs.livekit.io/recipes/transcriber.md)**: Real-time speech transcription with high accuracy.

- **[Keyword Detection](https://github.com/livekit-examples/python-agents-examples/blob/main/pipeline-stt/keyword-detection/keyword_detection.py)**: Detect specific keywords in speech in real-time.

- **[Using Twilio Voice](https://docs.livekit.io/sip/accepting-calls-twilio-voice.md)**: Use TwiML to accept incoming calls and bridge Twilio conferencing to LiveKit via SIP.

- **[IVR Agent](https://docs.livekit.io/recipes/ivr-navigator.md)**: Build a voice agent that can call external voice lines and respond to IVR flows using DTMF tones.

- **[Company Directory](https://docs.livekit.io/recipes/company-directory.md)**: Build a AI company directory agent. The agent can respond to DTMF tones and voice prompts, then redirect callers.

- **[Recording Consent](https://docs.livekit.io/recipes/recording-consent.md)**: Collect recording consent at the start of a call using an AgentTask for compliance and quality assurance.

- **[Phone Caller](https://docs.livekit.io/recipes/make_call.md)**: Agent that can make outbound phone calls and handle conversations.

- **[SIP Lifecycle](https://docs.livekit.io/recipes/sip_lifecycle.md)**: Complete lifecycle management for SIP calls.

- **[Answer Incoming Calls](https://docs.livekit.io/recipes/answer_call.md)**: Set up an agent to answer incoming SIP calls.

- **[Survey Caller](https://docs.livekit.io/recipes/survey_caller.md)**: Automated survey calling system.

- **[Chain-of-thought agent](https://docs.livekit.io/recipes/chain-of-thought.md)**: Build an agent for chain-of-thought reasoning using the `llm_node` to clean the text before TTS.

- **[LlamaIndex RAG](https://github.com/livekit/agents/tree/main/examples/voice_agents/llamaindex-rag)**: A voice AI agent that uses LlamaIndex for RAG to answer questions from a knowledge base.

- **[Moviefone](https://docs.livekit.io/recipes/moviefone.md)**: This agent uses function calling and the OpenAI API to search for movies and give you realtime information about showtimes.

- **[Context Variables](https://docs.livekit.io/recipes/context_variables.md)**: Maintain conversation context across interactions.

- **[Interrupt User](https://docs.livekit.io/recipes/interrupt_user.md)**: Example of how to implement user interruption in conversations.

- **[Long running tools](https://github.com/livekit/agents/blob/main/examples/voice_agents/long_running_function.py)**: Interruptions during long-running tools.

- **[LLM Content Filter](https://docs.livekit.io/recipes/llm_powered_content_filter.md)**: Implement content filtering in the `llm_node`.

- **[Simple Content Filter](https://docs.livekit.io/recipes/simple_content_filter.md)**: Basic content filtering implementation.

- **[Replacing LLM Output](https://docs.livekit.io/recipes/replacing_llm_output.md)**: Example of modifying LLM output before processing.

- **[Vision Assistant](https://github.com/livekit-examples/vision-demo)**: A voice AI agent with video input powered by Gemini Live.

- **[Raspberry Pi Transcriber](https://docs.livekit.io/recipes/pi_zero_transcriber.md)**: Run transcription on Raspberry Pi hardware.

- **[Pipeline Translator](https://docs.livekit.io/recipes/pipeline_translator.md)**: Implement translation in the processing pipeline.

- **[TTS Translator](https://docs.livekit.io/recipes/tts_translator.md)**: Translation with text-to-speech capabilities.

- **[LLM Metrics](https://docs.livekit.io/recipes/metrics_llm.md)**: Track and analyze LLM performance metrics.

- **[STT Metrics](https://docs.livekit.io/recipes/metrics_stt.md)**: Track and analyze speech-to-text performance metrics.

- **[TTS Metrics](https://docs.livekit.io/recipes/metrics_tts.md)**: Track and analyze text-to-speech performance metrics.

- **[VAD Metrics](https://docs.livekit.io/recipes/metrics_vad.md)**: Track and analyze voice activity detection metrics.

- **[Playing Audio](https://docs.livekit.io/recipes/playing_audio.md)**: Play audio files during agent interactions.

- **[Sound Repeater](https://docs.livekit.io/recipes/repeater.md)**: Simple sound repeating demo for testing audio pipelines.

- **[MCP Agent](https://docs.livekit.io/recipes/http_mcp_client.md)**: A voice AI agent with an integrated Model Context Protocol (MCP) client for the LiveKit API.

- **[Speedup Output Audio](https://github.com/livekit/agents/blob/main/examples/voice_agents/speedup_output_audio.py)**: Speed up the audio output of an agent.

- **[Structured Output](https://github.com/livekit/agents/blob/main/examples/voice_agents/structured_output.py)**: Handle structured output from the LLM by overriding the `llm_node` and `tts_node`.

- **[RPC + State Agent](https://github.com/livekit-examples/python-agents-examples/blob/main/rpc/rpc_agent.py)**: Voice agent with a state database updated through tool calling and queryable from the frontend with RPC.

- **[Tavus Avatar Agent](https://github.com/livekit-examples/python-agents-examples/blob/main/avatars/tavus)**: An educational AI agent that uses Tavus to create an interactive study partner.

- **[Toggle Audio](https://github.com/livekit/agents/blob/main/examples/voice_agents/toggle_io.py)**: An example of dynamically toggling audio input and output.

- **[Rover Teleop](https://github.com/livekit-examples/rover-teleop)**: Build a high performance robot tele-op system using LiveKit.

- **[VR Spatial Video](https://github.com/livekit-examples/spatial-video)**: Stream spatial video from a stereoscopic camera to a Meta Quest using LiveKit.

- **[Echo Agent](https://github.com/livekit/agents/blob/main/examples/primitives/echo-agent.py)**: Echo user audio back to them.

- **[Sync TTS Transcription](https://github.com/livekit/agents/blob/main/examples/other/text-to-speech/sync_tts_transcription.py)**: Uses manual subscription, transcription forwarding, and manually publishes audio output.

- **[Drive-thru agent](https://github.com/livekit/agents/blob/main/examples/drive-thru)**: A complex food ordering agent with tasks, tools, and a complete evaluation suite.

- **[Front-desk agent](https://github.com/livekit/agents/blob/main/examples/frontdesk)**: A calendar booking agent with tasks, tools, and evaluations.

- **[Python Voice Agent](https://github.com/livekit-examples/agent-starter-python)**: A complete sample project for a voice AI agent built with Python.

- **[Warm Transfer](https://github.com/livekit/agents/tree/main/examples/warm-transfer)**: Transfer calls from an AI agent to a human operator with context.

- **[Node.js Voice Agent](https://github.com/livekit-examples/agent-starter-node)**: A complete sample project for a voice AI agent built with Node.js.

- **[Agent-assisted warm transfer](https://docs.livekit.io/sip/transfer-warm.md)**: A comprehensive guide to transferring calls using an AI agent to provide context.

- **[Call forwarding using SIP REFER](https://docs.livekit.io/sip/transfer-cold.md)**: How to forward calls to another number or SIP endpoint with SIP REFER.

- **[Secure trunking for SIP calls](https://docs.livekit.io/sip/secure-trunking.md)**: How to enable secure trunking for LiveKit SIP.

- **[Region pinning for SIP](https://docs.livekit.io/sip/cloud.md)**: Use region pinning to restrict calls to a specific region.

- **[Agents telephony integration](https://docs.livekit.io/agents/start/telephony.md)**: Learn how to receive and make calls with a voice AI agent

---

This document was rendered at 2025-12-16T21:27:21.052Z.
For the latest version of this document, see [https://docs.livekit.io/llms.txt](https://docs.livekit.io/llms.txt).