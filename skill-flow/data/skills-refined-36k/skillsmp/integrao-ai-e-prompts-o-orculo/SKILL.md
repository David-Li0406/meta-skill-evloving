---
name: Integração AI e Prompts (O Oráculo)
description: Padronização, robustez e controle nas chamadas de IA (Gemini), separando prompts do código.
---

# Skill: Integração AI e Prompts ("O Oráculo")

Esta skill governa a inteligência do Biodiagnóstico. Seu objetivo é transformar chamadas de API frágeis ("strings soltas") em uma arquitetura robusta, testável e econômica.

## 🎯 Objetivos
- **Desacoplar Prompts**: Prompts não devem viver no meio de funções Python.
- **Resiliência**: Tratamento automático de `ResourceExhausted` (429) e timeouts.
- **Consistência**: Garantir que o JSON retornado pela IA siga sempre o mesmo schema via **Structured Outputs**.
- **Eficiência**: Uso de **Prompt Caching** para contextos repetitivos ou volumosos (PDFs longos).

## 📂 Estrutura Recomendada
- `biodiagnostico_app/ai/`: Módulo dedicado.
    - `prompts/`: Arquivos de texto ou YAML com os prompts.
        - `analise_pdf.txt`
        - `correcao_ocr.yaml`
    - `services/`: Classes que encapsulam a chamada ao Gemini.
    - `schemas/`: Definições Pydantic do formato de resposta esperado.

## 🛠️ O Gerenciador de Prompts
Evite concatenar strings gigantes no código. Use um template engine simples ou arquivos formatados.

### Exemplo de Template (Classe)

```python
# biodiagnostico_app/ai/services/prompt_manager.py
from string import Template

class PromptManager:
    @staticmethod
    def get_prompt(prompt_name: str, **kwargs) -> str:
        # Carregar de arquivo ou constante
        template_str = PROMPTS.get(prompt_name, "")
        return Template(template_str).safe_substitute(**kwargs)

# Uso
prompt = PromptManager.get_prompt("analise_pdf", texto_extraido=pdf_text)
```

## 🛡️ Tratamento de Erros e Retries
Sempre envolva chamadas de LLM com retentativas exponenciais.

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def chamar_gemini(prompt: str):
    # Lógica de chamada
    pass
```

## 🚨 Regras do Oráculo
1. **Structured Outputs Always**: Use Pydantic para definir o schema e passe para o Gemini via `response_mime_type="application/json"` e `response_schema`.
2. **Chain of Thought (CoT)**: Para análises médicas complexas, instrua a IA a "pensar passo a passo" antes de gerar o JSON final.
3. **Prompt Caching**: Ao processar múltiplos PDFs ou conversas longas, estruture o prompt para que as partes estáticas venham primeiro para aproveitar o cache.
4. **Never Trust AI**: Valide o JSON retornado com Pydantic antes de usar. Se falhar, lance `AIParsingError`.
5. **Log Everything**: Logue o token usage (se disponível) e latência para monitoramento futuro.

## 🛰️ Ferramentas da Inteligência (Scripts)

Use esses "ensaios" para economizar tempo e dinheiro com a IA:

1.  **`ensaio_ia.py`**: (O Treinador) Testa se um prompt novo funciona antes de colocá-lo no site oficial.
2.  **`contador_ia.py`**: (O Contador) Mostra quanto custou o uso do Gemini nas últimas 24 horas.
3.  **`revisor_ia.py`**: (O Revisor) Confere se as explicações da IA estão simples ou se ela está falando difícil demais.
4.  **`simulador_caso.py`**: (O Paciente Virtual) Cria casos médicos falsos para testar se a lógica clínica da IA está afiada.
5.  **`encurtador_contexto.py`**: (O Encurtador) Remove "palha" de textos grandes para a IA ler mais rápido e barato.
