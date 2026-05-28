---
name: ai-engineer
description: AI agent specialist for Faiston NEXO. Use PROACTIVELY for Google ADK agents, Bedrock AgentCore, Gemini API, ElevenLabs TTS, and AI-powered features.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# AI Engineer Skill

AI agent specialist for Faiston NEXO platform.

For detailed implementation guide, see `docs/AgentCore/IMPLEMENTATION_GUIDE.md`.

## Faiston NEXO AI Stack

| Component | Technology |
|-----------|------------|
| Framework | Google ADK (Agent Development Kit) |
| Model | Gemini 3.0 Pro (native) |
| Runtime | AWS Bedrock AgentCore |
| Auth | Cognito JWT Bearer Token |
| Memory | AgentCore Memory (STM_ONLY) |
| TTS | ElevenLabs API |
| Storage | S3 (audio files) |

## Architecture

```
Frontend (React SPA)
    |
    v
Cognito JWT Token
    |
    v
AgentCore Runtime (direct invocation)
    |
    v
BedrockAgentCoreApp
    |
    +-- NEXOAgent (RAG assistance)
    +-- FlashcardsAgent (study cards)
    +-- MindMapAgent (concept maps)
    +-- ReflectionAgent (learning analysis)
    +-- AudioClassAgent (podcast + TTS)
```

## Key Files

| Purpose | Path |
|---------|------|
| AgentCore Entry | `server/agentcore/main.py` |
| Agent Base | `server/agentcore/agents/nexo_agent.py` |
| Utilities | `server/agentcore/agents/utils.py` |
| ElevenLabs Tool | `server/agentcore/tools/elevenlabs_tool.py` |
| Implementation Guide | `docs/AgentCore/IMPLEMENTATION_GUIDE.md` |
| Frontend Client | `client/services/agentcore.ts` |
| Cognito Service | `client/services/cognito.ts` |

## Agent Actions

| Action | Agent | Purpose |
|--------|-------|---------|
| `nexo_chat` | NEXOAgent | RAG-based assistance chat |
| `generate_flashcards` | FlashcardsAgent | AI study cards |
| `generate_mindmap` | MindMapAgent | Concept visualization |
| `analyze_reflection` | ReflectionAgent | Learning feedback |
| `generate_audio_class` | AudioClassAgent | Podcast + ElevenLabs |

## Agent Implementation Pattern

```python
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

MODEL_GEMINI = "gemini-3-pro-preview"
APP_NAME = "faiston-nexo"

class MyAgent:
    def __init__(self):
        self.agent = Agent(
            model=MODEL_GEMINI,
            name="my_agent",
            description="Agent description",
            instruction=SYSTEM_PROMPT,
        )
        self.session_service = InMemorySessionService()

    async def invoke(self, prompt: str, user_id: str, session_id: str) -> str:
        content = types.Content(
            role="user",
            parts=[types.Part(text=prompt)],
        )

        await self.session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id,
        )

        runner = Runner(
            agent=self.agent,
            app_name=APP_NAME,
            session_service=self.session_service,
        )

        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content,
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    return event.content.parts[0].text
        return ""
```

## Prompt Engineering Guidelines

### System Prompt Structure

```python
SYSTEM_PROMPT = """
Você é [PERSONA] especializada em [DOMAIN].

## Personalidade
- [Trait 1]
- [Trait 2]

## Regras OBRIGATÓRIAS
1. [Rule 1]
2. [Rule 2]
3. Responda SEMPRE em português brasileiro

## Formato de Saída
[Describe expected JSON/markdown format]

## Exemplos
[Include few-shot examples if helpful]
"""
```

### JSON Output

```python
# Request JSON output in prompt
prompt = f"""
{context}

IMPORTANTE: Retorne APENAS JSON válido no formato:
{{
    "field1": "value1",
    "items": [...]
}}
"""

# Parse response safely
from server.agentcore.agents.utils import parse_json_safe
result = parse_json_safe(response)
```

## ElevenLabs TTS Integration

```python
# server/agentcore/tools/elevenlabs_tool.py
import httpx
import boto3
from botocore.config import Config

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

# Voice IDs for Faiston NEXO
VOICES = {
    "ana": "EXAVITQu4vr4xnSDxMaL",     # Female host
    "carlos": "TX3LPaxmHKxFdv7VOQHJ",  # Male host
}

async def generate_speech(text: str, voice: str = "ana") -> bytes:
    """Generate speech using ElevenLabs."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICES[voice]}",
            headers={
                "xi-api-key": ELEVENLABS_API_KEY,
                "Content-Type": "application/json",
            },
            json={
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75,
                }
            }
        )
        return response.content

def upload_to_s3(audio_bytes: bytes, key: str) -> str:
    """Upload audio to S3 and return presigned URL."""
    # CRITICAL: Use regional endpoint
    s3 = boto3.client(
        's3',
        region_name='us-east-2',
        config=Config(
            signature_version='s3v4',
            s3={'addressing_style': 'virtual'}
        )
    )

    bucket = "faiston-nexo-audio"
    s3.put_object(Bucket=bucket, Key=key, Body=audio_bytes, ContentType="audio/mpeg")

    return s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=7200
    )
```

## AgentCore Configuration

### .bedrock_agentcore.yaml

```yaml
default_agent: faiston_nexo_agents
agents:
  faiston_nexo_agents:
    name: faiston_nexo_agents
    entrypoint: main.py
    deployment_type: direct_code_deploy
    runtime_type: PYTHON_3_11
    memory:
      mode: STM_ONLY  # Short-term memory only
    authorizerConfiguration:
      customJWTAuthorizer:
        discoveryUrl: https://cognito-idp.us-east-2.amazonaws.com/us-east-2_6Vzhr0J6M/.well-known/openid-configuration
        allowedClients:
          - dqqebean5q4fq14bkp2bofnsj
```

### Environment Variables

| Variable | Purpose | Source |
|----------|---------|--------|
| `GOOGLE_API_KEY` | Gemini API access | GitHub Secret |
| `ELEVENLABS_API_KEY` | TTS generation | GitHub Secret |
| `BEDROCK_AGENTCORE_MEMORY_ID` | Memory persistence | Auto-set |

## Frontend Integration

### AgentCore Client

```typescript
// client/services/agentcore.ts
import { getCognitoAccessToken } from './cognito';

const AGENTCORE_ENDPOINT = 'https://bedrock-agentcore.us-east-2.amazonaws.com';
const AGENTCORE_ARN = 'arn:aws:bedrock-agentcore:...';

export async function invokeAgentCore<T>(request: {
  action: string;
  [key: string]: unknown;
}): Promise<{ data: T; sessionId: string }> {
  const token = await getCognitoAccessToken();

  const response = await fetch(
    `${AGENTCORE_ENDPOINT}/runtimes/${encodeURIComponent(AGENTCORE_ARN)}/invocations?qualifier=DEFAULT`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'X-Amzn-Bedrock-AgentCore-Runtime-Session-Id': getSessionId(),
      },
      body: JSON.stringify(request),
    }
  );

  return response.json();
}
```

### Session ID Requirements

**CRITICAL**: Session ID must be >= 33 characters!

```typescript
function generateSessionId(): string {
  return `session-${crypto.randomUUID().replace(/-/g, '')}`;
  // Result: "session-a1b2c3d4e5f6g7h8i9j0..." (41 chars)
}
```

## Deployment

Deploy via GitHub Actions only:

```bash
# Trigger: push to server/agentcore/** or manual
# Workflow: .github/workflows/deploy-agentcore.yml

# Manual trigger
gh workflow run deploy-agentcore.yml -f action=deploy
```

## Token Optimization

| Strategy | Implementation |
|----------|----------------|
| Limit transcription | First 10K tokens for context |
| Summarize history | Last 10 messages only |
| Structured output | JSON mode reduces verbosity |
| Cache responses | localStorage for repeated queries |

## Error Handling

```python
try:
    response = await agent.invoke(prompt, user_id, session_id)
except Exception as e:
    # Log error
    print(f"Agent error: {e}")
    # Return graceful fallback
    return {"error": str(e), "fallback": "Desculpe, ocorreu um erro."}
```

## Output Format

- Be extremely concise
- Follow existing agent patterns
- Include error handling
- Use Brazilian Portuguese for user-facing text
- Test with real transcriptions before deployment
