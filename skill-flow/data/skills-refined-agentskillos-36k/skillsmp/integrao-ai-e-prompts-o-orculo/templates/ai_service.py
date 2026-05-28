import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import os
import json
from typing import Dict, Any, Optional

class AIServiceError(Exception):
    pass

class AIService:
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY não configurada")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry_if_exception_type=(Exception) # Refinar para exceções especificas do Google Generative AI
    )
    def generate_json(self, prompt: str) -> Dict[str, Any]:
        """
        Gera conteúdo JSON garantido.
        """
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            
            if not response.text:
                raise AIServiceError("Resposta vazia da IA")

            return json.loads(response.text)
            
        except json.JSONDecodeError:
            raise AIServiceError("Falha ao decodificar JSON da IA")
        except Exception as e:
            raise e # O retry vai pegar isso

    @staticmethod
    def load_prompt(prompt_path: str) -> str:
        """Carrega prompt de um arquivo."""
        # Implementar carregamento de arquivo
        return ""
