# =============================================================================
# Agent Prompt Template - Faiston NEXO
# =============================================================================
# Template for creating new Google ADK agent prompts.
# Copy this file and customize for your specific agent.
# =============================================================================

# =============================================================================
# System Instruction Template
# =============================================================================

AGENT_INSTRUCTION = """
Voce e [NOME_DO_AGENTE], um especialista em [DOMINIO].

## Personalidade
- [Traco 1 - ex: Acolhedor e paciente]
- [Traco 2 - ex: Didatico e claro]
- [Traco 3 - ex: Encorajador]

## Regras OBRIGATORIAS
1. [Regra principal - ex: Use APENAS o conteudo fornecido]
2. [Regra de formato - ex: Retorne JSON valido]
3. Responda SEMPRE em portugues brasileiro
4. [Regras especificas do dominio]

## Formato de Saida (JSON)
{
  "campo1": "valor1",
  "items": [
    {"id": "1", "texto": "..."}
  ]
}

## Exemplos (Few-Shot)
# Exemplo 1
Entrada: "pergunta simples"
Saida: {"resposta": "resposta simples"}

# Exemplo 2
Entrada: "pergunta complexa"
Saida: {"resposta": "resposta detalhada"}
"""


# =============================================================================
# User Prompt Template
# =============================================================================

def build_user_prompt(
    transcription: str,
    count: int = 10,
    difficulty: str = "medium",
    custom_prompt: str = "",
) -> str:
    """
    Build the user prompt for the agent.

    Args:
        transcription: Episode transcription text
        count: Number of items to generate
        difficulty: easy, medium, or hard
        custom_prompt: Optional focus instructions

    Returns:
        Formatted user prompt string
    """
    return f"""
Gere exatamente {count} [ITEMS] no nivel de dificuldade "{difficulty}".

{f"Foco especial: {custom_prompt}" if custom_prompt else ""}

Transcricao da aula:
{transcription}

IMPORTANTE: Retorne APENAS o JSON valido, sem texto adicional.
Formato esperado:
{{
  "items": [
    {{"id": "1", "texto": "..."}}
  ]
}}
"""


# =============================================================================
# Agent Class Template
# =============================================================================

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from typing import Dict, Any

# Constants
APP_NAME = "faiston-nexo"
MODEL_GEMINI = "gemini-3-pro-preview"


class TemplateAgent:
    """
    Template Agent - [DESCRICAO DO PROPOSITO].

    [Descricao mais detalhada do que o agente faz
    e quando deve ser usado.]

    Uses Gemini 3.0 Pro for high quality generation.
    """

    def __init__(self):
        """Initialize with Gemini 3.0 Pro native."""
        self.agent = Agent(
            model=MODEL_GEMINI,
            name="template_agent",
            description="Agent that [DESCRICAO CURTA].",
            instruction=AGENT_INSTRUCTION,
        )
        self.session_service = InMemorySessionService()
        print(f"TemplateAgent initialized with model: {MODEL_GEMINI}")

    async def _setup_session_and_runner(self, user_id: str, session_id: str):
        """Set up session and runner for agent execution."""
        session = await self.session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id,
        )
        runner = Runner(
            agent=self.agent,
            app_name=APP_NAME,
            session_service=self.session_service,
        )
        return session, runner

    async def invoke(self, prompt: str, user_id: str, session_id: str) -> str:
        """
        Invoke the agent with a prompt and return the response.

        Args:
            prompt: User prompt/question
            user_id: Unique user identifier
            session_id: Unique session identifier

        Returns:
            Agent response as string
        """
        content = types.Content(
            role="user",
            parts=[types.Part(text=prompt)],
        )

        session, runner = await self._setup_session_and_runner(user_id, session_id)

        events = runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content,
        )

        async for event in events:
            if event.is_final_response():
                if event.content and event.content.parts:
                    return event.content.parts[0].text

        return ""

    async def generate(
        self,
        transcription: str,
        count: int = 10,
        difficulty: str = "medium",
        custom_prompt: str = "",
    ) -> Dict[str, Any]:
        """
        Generate items from transcription.

        Args:
            transcription: Episode transcription text
            count: Number of items to generate
            difficulty: easy, medium, or hard
            custom_prompt: Optional focus instructions

        Returns:
            Dict with items array
        """
        # Build prompt
        prompt = build_user_prompt(transcription, count, difficulty, custom_prompt)

        # Invoke agent
        response = await self.invoke(prompt, "system", "template-gen")

        # Parse JSON response
        result = self._parse_json_safe(response)

        # Validate structure
        if "items" not in result:
            result = {"items": [], "error": "Invalid response structure"}

        # Post-process: normalize fields, snap timestamps, etc.
        # [ADD YOUR POST-PROCESSING HERE]

        return result

    def _parse_json_safe(self, response: str) -> Dict[str, Any]:
        """Safely parse JSON from response with fallback."""
        import json
        import re

        try:
            json_str = self._extract_json(response)
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            return {"error": f"Failed to parse JSON: {e}", "raw_response": response}

    def _extract_json(self, response: str) -> str:
        """Extract JSON from markdown code blocks or raw text."""
        import re

        # Try markdown code block first
        json_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", response)
        if json_match:
            return json_match.group(1).strip()

        # Try raw JSON
        json_match = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", response)
        if json_match:
            return json_match.group(1).strip()

        return response.strip()
